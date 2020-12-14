""" K-Weather Living Jisu Sensor For Home Assistant """
import voluptuous as vol

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import CONF_NAME, CONF_MONITORED_CONDITIONS
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, PLATFORM

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

CONF_AREA = 'area'

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.All(
#            cv.deprecated(CONF_NAME, invalidation_version="0.110"),
            vol.Schema({vol.Optional(CONF_NAME, default=DOMAIN): cv.string}),
            vol.Schema({vol.Required(CONF_AREA): cv.string}),
            vol.Schema({vol.Optional(CONF_MONITORED_CONDITIONS): vol.All(cv.ensure_list, [vol.In(_INFORMATIONS)])}),
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up local_ip from configuration.yaml."""
    conf = config.get(DOMAIN)
#    if conf:
#        hass.async_create_task(
#            hass.config_entries.flow.async_init(
#                DOMAIN, data=conf, context={"source": SOURCE_IMPORT}
#            )
#        )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up kweather from a config entry."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, PLATFORM)
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    return await hass.config_entries.async_forward_entry_unload(entry, PLATFORM)
