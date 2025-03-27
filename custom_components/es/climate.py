import logging
import requests
import voluptuous as vol
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    HVAC_MODE_HEAT, HVAC_MODE_COOL, HVAC_MODE_OFF, SUPPORT_TARGET_TEMPERATURE)
from homeassistant.const import TEMP_CELSIUS, CONF_NAME, CONF_URL, CONF_API_KEY, CONF_USERNAME, CONF_PASSWORD
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import track_time_interval
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)

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


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the heat pump platform."""
    url = config[DOMAIN][CONF_URL]
    api_key = config[DOMAIN][CONF_API_KEY]
    username = config[DOMAIN][CONF_USERNAME]
    password = config[DOMAIN][CONF_PASSWORD]
    name = config[DOMAIN][CONF_NAME]
    min_temp = config[DOMAIN][CONF_MIN_TEMP]
    max_temp = config[DOMAIN][CONF_MAX_TEMP]

    climate_entity = HeatPumpEntity(name, url, api_key, username, password, min_temp, max_temp)
    sensor_entities = [
        TemperatureSensor("Indoor Temperature", url, api_key, username, password, "current_temperature"),
        TemperatureSensor("Outdoor Temperature", url, api_key, username, password, "outdoor_temperature")
    ]

    add_entities([climate_entity] + sensor_entities)
    track_time_interval(hass, lambda _: [entity.update() for entity in sensor_entities], UPDATE_INTERVAL)


class HeatPumpEntity(ClimateEntity):
    def __init__(self, name, url, api_key, username, password, min_temp, max_temp):
        self._name = name
        self._url = url
        self._api_key = api_key
        self._username = username
        self._password = password
        self._min_temp = min_temp
        self._max_temp = max_temp
        self._current_temperature = None
        self._target_temperature = None
        self._hvac_mode = HVAC_MODE_OFF
        self._available = False
        self.update()

    @property
    def name(self):
        return self._name

    @property
    def temperature_unit(self):
        return TEMP_CELSIUS

    @property
    def current_temperature(self):
        return self._current_temperature

    @property
    def target_temperature(self):
        return self._target_temperature

    @property
    def hvac_mode(self):
        return self._hvac_mode

    @property
    def hvac_modes(self):
        return [HVAC_MODE_HEAT, HVAC_MODE_COOL, HVAC_MODE_OFF]

    @property
    def supported_features(self):
        return SUPPORT_TARGET_TEMPERATURE

    @property
    def available(self):
        return self._available

    def set_hvac_mode(self, hvac_mode):
        response = requests.post(f"{self._url}/set_mode",
                                 json={"api_key": self._api_key, "username": self._username, "password": self._password,
                                       "mode": hvac_mode})
        if response.status_code == 200:
            self._hvac_mode = hvac_mode
        self.update()

    def set_temperature(self, **kwargs):
        temperature = kwargs.get("temperature")
        if temperature is not None:
            response = requests.post(f"{self._url}/set_temperature",
                                     json={"api_key": self._api_key, "username": self._username,
                                           "password": self._password, "temperature": temperature})
            if response.status_code == 200:
                self._target_temperature = temperature
        self.update()

    def update(self):
        try:
            response = requests.get(f"{self._url}/status", params={"api_key": self._api_key, "username": self._username,
                                                                   "password": self._password})
            if response.status_code == 200:
                data = response.json()
                self._current_temperature = data.get("current_temperature")
                self._target_temperature = data.get("target_temperature")
                self._hvac_mode = data.get("hvac_mode", HVAC_MODE_OFF)
                self._available = True
            else:
                self._available = False
        except requests.RequestException as e:
            _LOGGER.error("Error fetching data from heat pump API: %s", e)
            self._available = False


