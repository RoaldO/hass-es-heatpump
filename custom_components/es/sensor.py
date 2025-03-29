import logging
import random
from typing import Any

import requests
from homeassistant.helpers.entity import Entity

from . import const

_LOGGER = logging.getLogger(__name__)
_LOGGER.debug("initialization started")


class TemperatureSensor(Entity):
    def __init__(self, name, url, credentials, field):
        self._name = name
        self._url = url
        self._credentials = credentials
        self._field = field
        self._state = None
        self._available = False
        # self.update()

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
        _LOGGER.debug(f'calling update on sensor {self._name}')
        try:
            # just random for a start
            self._state = random.gauss(23.0, 0.2)
            self._available = True

            # response = requests.get(
            #     f"{self._url}/status",
            #     params={
            #         "username": self._credentials.username,
            #         "password": self._credentials._password,
            #     }
            # )
            # if response.status_code == 200:
            #     data = response.json()
            #     self._state = data.get(self._field)
            #     self._available = True
            # else:
            #     self._available = False
        except requests.RequestException as e:
            _LOGGER.error("Error fetching data from heat pump API: %s", e)
            self._available = False

_LOGGER.debug("initialization done")
