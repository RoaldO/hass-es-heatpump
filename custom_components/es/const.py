"""
Aggregation of the various constants that are available and relevant to our
domain.
"""
import logging
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
# noinspection PyUnresolvedReferences
from homeassistant.components.climate.const import HVACMode, SERVICE_SET_TEMPERATURE
# noinspection PyUnresolvedReferences
from homeassistant.const import CONF_URL, CONF_API_KEY, CONF_USERNAME, CONF_PASSWORD, CONF_NAME, UnitOfTemperature

_LOGGER = logging.getLogger(__name__)
_LOGGER.debug("initialization started")

__ALL__ = [
    "CONFIG_SCHEMA"
    "CONF_API_KEY",
    "CONF_MAX_TEMP",
    "CONF_MIN_TEMP",
    "CONF_NAME",
    "CONF_PASSWORD",
    "CONF_URL",
    "CONF_USERNAME",
    "DATA_SCHEMA",
    "DEFAULT_MAX_TEMP",
    "DEFAULT_MIN_TEMP",
    "DEFAULT_NAME",
    "DOMAIN",
    "HVACMode",
    "SERVICE_SET_TEMPERATURE",
    "TEMP_CELSIUS",
    "UPDATE_INTERVAL",
]

DOMAIN = "es"

CONF_MIN_TEMP = "min_temp"
CONF_MAX_TEMP = "max_temp"

DEFAULT_NAME = "Heat Pump"
DEFAULT_MIN_TEMP = 16
DEFAULT_MAX_TEMP = 30
UPDATE_INTERVAL = timedelta(minutes=1)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_URL): cv.url,
                vol.Required(CONF_API_KEY): cv.string,
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
                vol.Optional(CONF_MIN_TEMP, default=DEFAULT_MIN_TEMP): vol.Coerce(float),
                vol.Optional(CONF_MAX_TEMP, default=DEFAULT_MAX_TEMP): vol.Coerce(float),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_URL): str,
        vol.Required(CONF_API_KEY): str,
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
    }
)

TEMP_CELSIUS = UnitOfTemperature.CELSIUS

_LOGGER.debug("initialization done")
