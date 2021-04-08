"""Support for K-Weather Living Jisu Sensors."""
import logging
import requests
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from datetime import timedelta
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_NAME, CONF_MONITORED_CONDITIONS)
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

from .const import DOMAIN, MODEL, MANUFAC, SW_VERSION

REQUIREMENTS = ['xmltodict==0.12.0']

_LOGGER = logging.getLogger(__name__)

CONF_AREA = 'area'

# 지역별 url
_JISU_URL = {
    '01' : 'https://www.kweather.co.kr/data/JISU/11B00000.xml', #서울/경기
    '02' : 'https://www.kweather.co.kr/data/JISU/11D10000.xml', #강원영서
    '03' : 'https://www.kweather.co.kr/data/JISU/11D20000.xml', #강원영동
    '04' : 'https://www.kweather.co.kr/data/JISU/11C10000.xml', #충청북도
    '05' : 'https://www.kweather.co.kr/data/JISU/11C20000.xml', #충청남도
    '06' : 'https://www.kweather.co.kr/data/JISU/11H10000.xml', #경상북도
    '07' : 'https://www.kweather.co.kr/data/JISU/11H20000.xml', #경상남도
    '08' : 'https://www.kweather.co.kr/data/JISU/11F10000.xml', #전라북도
    '09' : 'https://www.kweather.co.kr/data/JISU/11F20000.xml', #전라남도
    '10' : 'https://www.kweather.co.kr/data/JISU/11G00000.xml', #제주도
}

DEFAULT_NAME = 'kweather'

MIN_TIME_BETWEEN_SENSOR_UPDATES = timedelta(seconds=3600)

SCAN_INTERVAL = timedelta(seconds=7200)

_INFORMATIONS = {
    'picnic'     : [0,  '나들이', 'mdi:island'],
    'laundry'    : [1,  '빨래',   'mdi:tumble-dryer'],
    'carwash'    : [2,  '세차',   'mdi:car-wash'],
    'fire'       : [4,  '불조심', 'mdi:fire'],
    'exercise'   : [5,  '운동',   'mdi:weight-lifter'],

    'pollution'  : [7,  '공해',   'mdi:blur'],
    'corruption' : [12, '부패',   'mdi:emoticon-poop'],
    'uv'         : [10, '자외선', 'mdi:weather-sunny-alert'],
    'heating'    : [3,  '난방',   'mdi:hot-tub'],
    'cold'       : [6,  '감기',   'mdi:thermometer-minus'],
    'cooling'    : [8,  '냉방',   'mdi:air-filter'],
    'feel'       : [9,  '불쾌',   'mdi:emoticon-confused-outline'],
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_AREA): cv.string,
    vol.Optional(CONF_MONITORED_CONDITIONS):
        vol.All(cv.ensure_list, [vol.In(_INFORMATIONS)]),
})


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up a Air Korea Sensors."""
    name = config.get(CONF_NAME)
    area = config.get(CONF_AREA)

    informs = config.get(CONF_MONITORED_CONDITIONS) or None

    sensors = []
    if informs is not None:
        real_time_api = KWeatherAPI(area)

        for variable in informs:
            sensors += [KWeatherSensor(name, variable, _INFORMATIONS[variable], real_time_api)]

    async_add_entities(sensors, True)

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add a entity from a config_entry."""
    name = DEFAULT_NAME
    area = config_entry.data[CONF_AREA]

    informs = None

    if CONF_MONITORED_CONDITIONS in config_entry.data:
        informs = config_entry.data[CONF_MONITORED_CONDITIONS]

    sensors = []
    if informs is not None:
        real_time_api = KWeatherAPI(area)

        for variable in informs:
            sensors += [KWeatherSensor(name, variable, _INFORMATIONS[variable], real_time_api)]
    else:
        real_time_api = KWeatherAPI(area)

        for key in _INFORMATIONS:
            sensors += [KWeatherSensor(name, key, _INFORMATIONS[key], real_time_api)]

    async_add_devices(sensors, True)


class KWeatherAPI:
    """KWeather API."""

    def __init__(self, area):
        """Initialize the KWeather API.."""
        self.area = area
        self.result = {}

    def update(self):
        """Update function for updating api information."""
        try:
            url = _JISU_URL[self.area]
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            import xmltodict

            self.result = xmltodict.parse(response.content.decode('utf8'))['jisu']['ndate'][0]['jtitle']
        except Exception as ex:
            _LOGGER.error('Failed to update KWeather API status Error: %s', ex)
            raise


class KWeatherSensor(Entity):
    """Representation of a KWeather Sensor."""

    def __init__(self, name, variable, variable_info, api):
        """Initialize the KWeather sensor."""
        self._name = name
        self.var_id = variable
        self.index    = variable_info[0]
        self.var_name = variable_info[1]
        self.var_icon = variable_info[2]

        self.var_num   = None
        self.var_jnum  = None
        self.var_jtext = None

        self.api = api
        self.var_state = ''

        self.fs_name = None

    @property
    def unique_id(self):
        """Return a unique ID to use for this sensor."""
        return 'sensor.kweather_{}_{}'.format(self.api.area, self.var_id)

    @property
    def name(self):
        """Return the name of the sensor, if any."""
        if self.fs_name is None:

            self.fs_name = '{} {} Score'.format(self.api.area, self.var_id)
            return self.fs_name
        else:
            return '{} 지수'.format(self.var_name)

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self.var_icon

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.var_state

    @Throttle(MIN_TIME_BETWEEN_SENSOR_UPDATES)
    def update(self):
        """Get the latest state of the sensor."""
        if self.api is None:
            return

        self.api.update()

        self.var_state = self.api.result[self.index].get('jnum','-')
        self.var_jnum  = self.api.result[self.index].get('jnum','-')
        self.var_jtext = self.api.result[self.index].get('jtext','-')

    @property
    def device_state_attributes(self):
        """Attributes."""
        data = { 'jnum' : self.var_jnum,
                 'jtext' : self.var_jtext }
        return data

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN,)},
            "name": 'K-Weather 생활지수',
            "sw_version": SW_VERSION,
            "manufacturer": MANUFAC,
            "model": MODEL,
            "entry_type": "service"
        }
