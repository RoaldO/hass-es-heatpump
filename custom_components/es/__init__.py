"""
ES Heatpump integration, implemented using http calls to myheatpump.com.
"""
import logging
from typing import Coroutine, Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import track_time_interval, async_track_time_interval

from .climate import HeatPumpEntity, Credentials
from . import const
from . import climate
from .sensor import TemperatureSensor

_LOGGER = logging.getLogger(__name__)


# def setup_platform(hass, config, add_entities, discovery_info=None):
#     """Set up the heat pump platform."""
#     _LOGGER.debug("setup_platform()")
#     url = config[const.DOMAIN][const.CONF_URL]
#     username = config[const.DOMAIN][const.CONF_USERNAME]
#     password = config[const.DOMAIN][const.CONF_PASSWORD]
#     name = config[const.DOMAIN][const.CONF_NAME]
#
#     credentials = Credentials(
#         username=config[const.DOMAIN][const.CONF_USERNAME],
#         password=config[const.DOMAIN][const.CONF_PASSWORD],
#     )
#
#     climate_entity = HeatPumpEntity(name, url, username, password)
#     sensor_entities = [
#         TemperatureSensor(
#             "Indoor Temperature",
#             url,
#             credentials,
#             "current_temperature",
#         ),
#         TemperatureSensor(
#             "Outdoor Temperature",
#             url,
#             credentials,
#             "outdoor_temperature",
#         )
#     ]
#
#     add_entities([climate_entity] + sensor_entities)
#     track_time_interval(
#         hass,
#         lambda _: [entity.update() for entity in sensor_entities],
#         const.UPDATE_INTERVAL,
#     )
#     _LOGGER.debug("setup_platform(): RETURN")


async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
) -> bool:
    """Set up the ES Heat Pump from a config entry."""
    _LOGGER.debug("async_setup_entry()")
    hass.data.setdefault(const.DOMAIN, {})
    hass.data[const.DOMAIN][entry.entry_id] = entry.data

    name = hass.data[const.DOMAIN][entry.entry_id][const.CONF_NAME]
    url = hass.data[const.DOMAIN][entry.entry_id][const.CONF_URL]
    username = hass.data[const.DOMAIN][entry.entry_id][const.CONF_USERNAME]
    password = hass.data[const.DOMAIN][entry.entry_id][const.CONF_PASSWORD]

    credentials = Credentials(
        username=username,
        password=password,
    )

    climate_entity = HeatPumpEntity(name, url, username, password)
    sensor_entities = [
        TemperatureSensor(
            "Indoor Temperature",
            url,
            credentials,
            "current_temperature",
        ),
        TemperatureSensor(
            "Outdoor Temperature",
            url,
            credentials,
            "outdoor_temperature",
        )
    ]

    async_track_time_interval(
        hass,
        lambda now: sensor_entities[0].update(),
        const.UPDATE_INTERVAL
    )
    async_track_time_interval(
        hass,
        lambda now: sensor_entities[0].update(),
        const.UPDATE_INTERVAL
    )

    track_time_interval(
        hass,
        lambda _: [entity.update() for entity in sensor_entities],
        const.UPDATE_INTERVAL,
    )

    return True
