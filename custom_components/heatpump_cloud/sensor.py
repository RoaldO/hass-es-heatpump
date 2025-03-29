# <config_dir>/custom_components/heatpump_cloud/sensor.py
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up sensors based on configured mappings"""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    mappings = config_entry.data.get("parameter_mappings", {})

    entities = []
    for param, mapping in mappings.items():
        entities.append(HeatPumpSensor(
            coordinator,
            param,
            mapping["name"],
            config_entry.entry_id
        ))

    async_add_entities(entities)


class HeatPumpSensor(SensorEntity):
    """Representation of a mapped heat pump sensor"""

    def __init__(self, coordinator, parameter, name, entry_id):
        self.coordinator = coordinator
        self.parameter = parameter
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_{parameter}"

    @property
    def state(self):
        """Return the parsed value of the parameter"""
        return self.coordinator.data.get(f"par{self.parameter}")

    @property
    def available(self):
        """Return True if entity is available"""
        return self.coordinator.last_update_success and f"par{self.parameter}" in self.coordinator.data
