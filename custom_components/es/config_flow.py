import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from . import const

_LOGGER = logging.getLogger(__name__)
_LOGGER.debug("initialization started")


class EsHeatPumpConfigFlow(config_entries.ConfigFlow, domain=const.DOMAIN):
    async def async_step_user(
            self,
            user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(title=user_input[const.CONF_NAME], data=user_input)
        return self.async_show_form(step_id="user", data_schema=const.CONFIG_SCHEMA)


#class EsHeatPumpConfigFlow(config_entries.ConfigFlow, domain=const.DOMAIN):
#    """Handle a config flow for ES Heat Pump."""
#
#    VERSION = 1
#
#    async def async_step_user(self, user_input=None):
#        """Handle the initial step."""
#        _LOGGER.debug("EsHeatPumpConfigFlow.async_step_user()")
#        errors = {}
#
#        if user_input is not None:
#            url = user_input[const.CONF_URL]
#            api_key = user_input[const.CONF_API_KEY]
#            username = user_input[const.CONF_USERNAME]
#            password = user_input[const.CONF_PASSWORD]
#
#            # TODO: Perform a test API call here to validate credentials
#
#            return self.async_create_entry(title=user_input[const.CONF_NAME], data=user_input)
#
#        return self.async_show_form(step_id="user", data_schema=const.DATA_SCHEMA, errors=errors)
#
#    @staticmethod
#    @callback
#    def async_get_options_flow(config_entry):
#        return EsHeatPumpOptionsFlowHandler(config_entry)
#
#
#class EsHeatPumpOptionsFlowHandler(config_entries.OptionsFlow):
#    """Handle options flow."""
#
#    def __init__(self, config_entry):
#        """Initialize options flow."""
#        _LOGGER.debug("EsHeatPumpOptionsFlowHandler()")
#        self.config_entry = config_entry
#
#    async def async_step_init(self, user_input=None):
#        """Manage the options."""
#        _LOGGER.debug("EsHeatPumpOptionsFlowHandler.async_step_init()")
#        _LOGGER.debug(f"EsHeatPumpOptionsFlowHandler.async_step_init() {user_input=}")
#        if user_input is not None:
#            return self.async_create_entry(title="", data=user_input)
#
#        return self.async_show_form(step_id="init", data_schema=vol.Schema({
#            vol.Required(const.CONF_URL): cv.url,
#            # vol.Required(const.CONF_API_KEY): cv.string,
#            # vol.Required(const.CONF_USERNAME): cv.string,
#            # vol.Required(const.CONF_PASSWORD): cv.string,
#            # vol.Optional(const.CONF_NAME, default=const.DEFAULT_NAME): cv.string,
#            # vol.Optional(const.CONF_MIN_TEMP, default=const.DEFAULT_MIN_TEMP): vol.Coerce(float),
#            # vol.Optional(const.CONF_MAX_TEMP, default=const.DEFAULT_MAX_TEMP): vol.Coerce(float),
#        }))

_LOGGER.debug("initialization started")
