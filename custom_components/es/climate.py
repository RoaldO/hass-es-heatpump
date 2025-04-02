# <config_dir>/custom_components/es/climate.py
import typing

from homeassistant.components.climate import ClimateEntity

if typing.TYPE_CHECKING:
    from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from . import const



async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup climate platform with API instance"""
    data = hass.data[const.DOMAIN][config_entry.entry_id]
    async_add_entities([HeatPumpClimate(data["coordinator"], data["api"])])


class HeatPumpClimate(ClimateEntity):
    """Climate entity with cookie-based API"""

    def __init__(self, coordinator: "DataUpdateCoordinator", api):
        self.coordinator = coordinator
        self._api = api
        self._attr_name = "Heat Pump"
        self._attr_temperature_unit = const.TEMP_CELSIUS
        # self._attr_supported_features = SUPPORT_TARGET_TEMPERATURE
        self._attr_hvac_modes = const.SUPPORTED_MODES

    @property
    def current_temperature(self):
        return self.coordinator.data.get("current_temp") if self.coordinator.data else None

    @property
    def target_temperature(self):
        return self.coordinator.data.get("target_temp") if self.coordinator.data else None

    @property
    def hvac_mode(self):
        return self.coordinator.data.get("mode") if self.coordinator.data else None

    async def async_set_temperature(self, **kwargs):
        temperature = kwargs.get(const.ATTR_TEMPERATURE)
        if temperature is not None:
            await self._api.async_set_temperature(temperature)
            await self.coordinator.async_request_refresh()

    async def async_set_hvac_mode(self, hvac_mode):
        await self._api.async_set_mode(hvac_mode)
        await self.coordinator.async_request_refresh()