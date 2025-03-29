import logging

import requests
from homeassistant.helpers.entity import Entity

from . import const

_LOGGER = logging.getLogger(__name__)
_LOGGER.debug("initialization started")


class TemperatureSensor(Entity):
    def __init__(self, name, url, username, password, field):
        self._name = name
        self._url = url
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
        return const.TEMP_CELSIUS

    @property
    def available(self):
        return self._available

    def update(self):
        try:
            response = requests.get(
                f"{self._url}/status",
                params={
                    "username": self._username,
                    "password": self._password
                }
            )
            if response.status_code == 200:
                data = response.json()
                self._state = data.get(self._field)
                self._available = True
            else:
                self._available = False
        except requests.RequestException as e:
            _LOGGER.error("Error fetching data from heat pump API: %s", e)
            self._available = False

_LOGGER.debug("initialization done")
