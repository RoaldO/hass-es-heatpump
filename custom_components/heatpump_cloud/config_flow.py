# <config_dir>/custom_components/heatpump_cloud/config_flow.py
from __future__ import annotations
import logging
import voluptuous as vol
from homeassistant import config_entries
from .api import HeatPumpCloudAPI, AuthenticationError
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

AUTH_SCHEMA = vol.Schema({
    vol.Required("username"): str,
    vol.Required("password"): str,
    vol.Required("api_url", default="https://www.myheatpump.com"): str,
    vol.Required("session_url", default="https://www.myheatpump.com/auth/session"): str,
    vol.Required("mn"): str,  # New installation identifier field
})


class HeatPumpConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            try:
                api = HeatPumpCloudAPI(
                    username=user_input["username"],
                    password=user_input["password"],
                    api_url=user_input["api_url"],
                    session_url=user_input["session_url"],
                    mn=user_input["mn"]  # Add mn to API constructor
                )
                await api.authenticate()
                return self.async_create_entry(
                    title=f"Heat Pump {user_input['mn']}",
                    data=user_input
                )
            except AuthenticationError as err:
                errors["base"] = "invalid_auth"
                _LOGGER.error("Authentication failed: %s", err)
            except Exception as err:
                errors["base"] = "unknown"
                _LOGGER.exception("Unexpected error")

        return self.async_show_form(
            step_id="user",
            data_schema=AUTH_SCHEMA,
            errors=errors
        )