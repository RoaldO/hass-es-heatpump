import logging

import requests
from homeassistant.components.climate import ClimateEntity
from homeassistant.helpers.event import track_time_interval

from es.sensor import TemperatureSensor
from . import const

_LOGGER = logging.getLogger(__name__)
_LOGGER.debug("initialization started")


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the heat pump platform."""
    _LOGGER.debug("setup_platform()")
    url = config[const.DOMAIN][const.CONF_URL]
    api_key = config[const.DOMAIN][const.CONF_API_KEY]
    username = config[const.DOMAIN][const.CONF_USERNAME]
    password = config[const.DOMAIN][const.CONF_PASSWORD]
    name = config[const.DOMAIN][const.CONF_NAME]
    min_temp = config[const.DOMAIN][const.CONF_MIN_TEMP]
    max_temp = config[const.DOMAIN][const.CONF_MAX_TEMP]

    climate_entity = HeatPumpEntity(name, url, api_key, username, password, min_temp, max_temp)
    sensor_entities = [
        TemperatureSensor(
            "Indoor Temperature",
            url,
            api_key,
            username,
            password,
            "current_temperature",
        ),
        TemperatureSensor(
            "Outdoor Temperature",
            url,
            api_key,
            username,
            password,
            "outdoor_temperature",
        )
    ]

    add_entities([climate_entity] + sensor_entities)
    track_time_interval(
        hass,
        lambda _: [entity.update() for entity in sensor_entities],
        const.UPDATE_INTERVAL,
    )


class HeatPumpEntity(ClimateEntity):
    def __init__(self, name, url, api_key, username, password, min_temp, max_temp):
        _LOGGER.debug("HeatPumpEntity()")
        self._name = name
        self._url = url
        self._api_key = api_key
        self._username = username
        self._password = password
        self._min_temp = min_temp
        self._max_temp = max_temp
        self._current_temperature = None
        self._target_temperature = None
        self._hvac_mode = const.HVACMode.OFF
        self._available = False
        self.update()

    @property
    def name(self):
        return self._name

    @property
    def temperature_unit(self):
        return const.TEMP_CELSIUS

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
        return [const.HVACMode.HEAT, const.HVACMode.COOL, const.HVACMode.OFF]

    @property
    def supported_features(self):
        return const.SERVICE_SET_TEMPERATURE

    @property
    def available(self):
        return self._available

    def set_hvac_mode(self, hvac_mode):
        response = requests.post(
            f"{self._url}/set_mode",
            json={
                "api_key": self._api_key,
                "username": self._username,
                "password": self._password,
                "mode": hvac_mode,
            },
        )
        if response.status_code == 200:
            self._hvac_mode = hvac_mode
        self.update()

    def set_temperature(self, **kwargs):
        temperature = kwargs.get("temperature")
        if temperature is not None:
            response = requests.post(
                f"{self._url}/set_temperature",
                json={
                    "api_key": self._api_key,
                    "username": self._username,
                    "password": self._password,
                    "temperature": temperature,
                },
            )
            if response.status_code == 200:
                self._target_temperature = temperature
        self.update()

    def update(self):
        _LOGGER.debug("HeatPumpEntity.update()")
        try:
            response = requests.get(
                f"{self._url}/status",
                params={
                    "api_key": self._api_key,
                    "username": self._username,
                    "password": self._password,
                },
            )
            if response.status_code == 200:
                data = response.json()
                self._current_temperature = data.get("current_temperature")
                self._target_temperature = data.get("target_temperature")
                self._hvac_mode = data.get("hvac_mode", const.HVACMode.OFF)
                self._available = True
            else:
                self._available = False
        except requests.RequestException as e:
            _LOGGER.error("Error fetching data from heat pump API: %s", e)
            self._available = False

_LOGGER.debug("initialization done")
