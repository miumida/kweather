"""Config flow for K-Weather."""
import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import (CONF_SCAN_INTERVAL)

from .const import DOMAIN

CONF_AREA    = 'area'
CONF_NAME    = 'name'

default_area = '01'
default_name = 'kweather'

_AREA = {
    '01' : '서울/경기',
    '02' : '강원영서',
    '03' : '강원영동',
    '04' : '충청북도',
    '05' : '충청남도',
    '06' : '경상북도',
    '07' : '경상남도',
    '08' : '전라북도',
    '09' : '전라남도',
    '10' : '제주도'
}

_LOGGER = logging.getLogger(__name__)

class KWeatherConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for K-Weather."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize flow."""
        self._area: Optional[str] = None
        self._name: Optional[str] = "kweather"

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            self._area          = user_input[CONF_AREA]

            uuid = 'kweather-area-{}'.format(self._area)
            await self.async_set_unique_id(uuid)

            return self.async_create_entry(title=_AREA[self._area], data=user_input)

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is None:
            return self._show_user_form(errors)

        #return self.async_create_entry(title=DOMAIN, data=user_input)

    async def async_step_import(self, import_info):
        """Handle import from config file."""
        return await self.async_step_user(import_info)

    @callback
    def _show_user_form(self, errors=None):
        default_area       = self._area
        schema = vol.Schema(
            {
                vol.Required(CONF_AREA, default=None): vol.In(_AREA),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors or {}
        )
