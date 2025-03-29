# <config_dir>/custom_components/heatpump_cloud/config_flow.py
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .api import HeatPumpCloudAPI
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

AUTH_SCHEMA = vol.Schema({
    vol.Required("username"): str,
    vol.Required("password"): str,
    vol.Required("api_url"): str,
})


class HeatPumpConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HeatPump Cloud."""

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle the initial step."""
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
            except Exception as err:
                _LOGGER.exception("Authentication failed")
                errors["base"] = "invalid_auth"

        return self.async_show_form(
            step_id="user",
            data_schema=AUTH_SCHEMA,
            errors=errors
        )
