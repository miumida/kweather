"""Support for K-Weather Living Jisu Sensors."""
import logging
import requests
import voluptuous as vol
import async_timeout

import homeassistant.helpers.config_validation as cv

from datetime import timedelta
from datetime import datetime
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_NAME, CONF_MONITORED_CONDITIONS)
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util import Throttle

from .const import DOMAIN, MODEL, MANUFAC, SW_VERSION, BASE_URL, _AREA_CD, CONF_AREA, _ITEMS, _ATTR

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=7200)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_AREA): cv.string,
    vol.Optional(CONF_MONITORED_CONDITIONS):
        vol.All(cv.ensure_list, [vol.In(_ITEMS)]),
})

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add a entity from a config_entry."""
    area = config_entry.data[CONF_AREA]

    sensors = []

    api = KWeatherAPI(area, hass)

    async def async_update_life_weather():
        try:
            # handled by the data update coordinator.
            await api.async_update()

            data = api.result

            rtn = {}

            for key in data:
                rtn[key] = data[key]

            #_LOGGER.error(f"[{DOMAIN}] async_update_life_weather() Error, %s", rtn )

            dt = datetime.now()
            syncdate = dt.strftime("%Y-%m-%d %H:%M:%S")
            rtn['syncdate'] = syncdate

            return rtn
        except Exception as err:
            raise UpdateFailed(f"[{DOMAIN}] Error communicating with API: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        # Name of the data. For logging purposes.
        name="kweather",
        update_method=async_update_life_weather,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=timedelta( seconds=3600 ),
    )

    await coordinator.async_config_entry_first_refresh()

    for key in _ITEMS:
       sensors += [ kweatherSensor(coordinator, key) ]

    async_add_devices(sensors, True)


class KWeatherAPI:
    """KWeather API."""

    def __init__(self, area, hass):
        """Initialize the KWeather API.."""
        self._hass  = hass
        self.area   = area
        self.result = {}

    async def async_update(self):
        """Update function for updating api information."""
        try:
            session = async_get_clientsession(self._hass, verify_ssl=False)

            url = BASE_URL.format(_AREA_CD[self.area])

            response = await session.get(url, timeout=30)
            response.raise_for_status()

            self.result = await response.json()
            #_LOGGER.error(f"[{DOMAIN}] %s", self.result)

        except Exception as ex:
            _LOGGER.error(f'[{DOMAIN}]Failed to update KWeather API status Error: %s', ex)
            raise


class kweatherSensor(CoordinatorEntity, SensorEntity):

    def __init__(self, coordinator, id):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)

        dt = datetime.now()
        self._id = id
        self._name = None
        self._syncdate = dt.strftime("%Y-%m-%d %H:%M:%S")


    @property
    def unique_id(self):
        """Return the entity ID."""
        return 'sensor.kweather_{}'.format(self._id.lower())


    @property
    def name(self):
        """Return the name of the sensor, if any."""
        if self._name is None:
            self._name = "{}지수".format(_ITEMS[self._id][0])
            return 'kweather_{}'.format(self._id.lower())
        else:
            return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return _ITEMS[self._id][1]

    @property
    def state(self):
        return str(self.coordinator.data.get("{}{}".format(self._id, "Factor"), '-'))

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this sensor."""
        return ""


    async def async_update(self):
        """Get the latest state of the sensor."""
        if self.coordinator is None:
            return

        dt = datetime.now()
        self._syncdate = dt.strftime("%Y-%m-%d %H:%M:%S")


    @property
    def extra_state_attributes(self):
        """Attributes."""

        attr = {}

        for key in _ATTR:
            attr[key] = self.coordinator.data.get("{}{}".format(self._id, key), '-')

        attr["syncdate"] = self.coordinator.data.get("syncdate", '-')

        return attr

    @property
    def device_info(self):
        """Return information about the device."""
        return {
            "identifiers": {(DOMAIN,)},
            "name": 'K-Weather 생활지수',
            "sw_version": SW_VERSION,
            "manufacturer": MANUFAC,
            "model": MODEL,
            "entry_type": "service"
        }
