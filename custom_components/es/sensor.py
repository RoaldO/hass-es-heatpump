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


class TemperatureSensor(Entity):
    def __init__(self, name, url, api_key, username, password, field):
        self._name = name
        self._url = url
        self._api_key = api_key
        self._username = username
        self._password = password
        self._field = field
        self._state = None
        self._available = False
        self.update()

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return TEMP_CELSIUS

    @property
    def available(self):
        return self._available

    def update(self):
        try:
            response = requests.get(f"{self._url}/status", params={"api_key": self._api_key, "username": self._username,
                                                                   "password": self._password})
            if response.status_code == 200:
                data = response.json()
                self._state = data.get(self._field)
                self._available = True
            else:
                self._available = False
        except requests.RequestException as e:
            _LOGGER.error("Error fetching data from heat pump API: %s", e)
            self._available = False
