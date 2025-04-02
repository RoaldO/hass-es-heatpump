# <config_dir>/custom_components/es/config_flow.py
from __future__ import annotations
import logging
from homeassistant import config_entries
from .api import HeatPumpCloudAPI, AuthenticationError
from . import const

_LOGGER = logging.getLogger(__name__)

class HeatPumpConfigFlow(config_entries.ConfigFlow, domain=const.DOMAIN):

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            try:
                api = HeatPumpCloudAPI(
                    user_input["username"],
                    user_input["password"],
                    user_input["api_url"]
                )
                await api.authenticate()
                return self.async_create_entry(title="Heat Pump Cloud", data=user_input)
            except AuthenticationError as err:
                _LOGGER.error("Authentication failed: %s", err)
                errors["base"] = "invalid_auth"
            except Exception as err:
                _LOGGER.exception("Unexpected error")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=const.AUTH_SCHEMA,
            errors=errors
        )
