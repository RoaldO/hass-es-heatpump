"""
collection of all constants needed in the project so it provides an easier
overview for the modules of what is available.
"""
import homeassistant.components.climate.const
import homeassistant.const
import voluptuous as vol

DOMAIN = "es"
PLATFORMS = ["climate"]

HVAC_MODE_OFF = homeassistant.components.climate.const.HVACMode.OFF
HVAC_MODE_HEAT = homeassistant.components.climate.const.HVACMode.HEAT
HVAC_MODE_COOL = homeassistant.components.climate.const.HVACMode.COOL
HVAC_MODE_SANITARY_HOT_WATER = "Sanitary hot water"
HVAC_MODE_AUTO = "auto"

SUPPORTED_MODES = [
    HVAC_MODE_OFF,
    HVAC_MODE_HEAT,
    HVAC_MODE_COOL,
    HVAC_MODE_SANITARY_HOT_WATER,
    HVAC_MODE_AUTO,
]

TEMP_CELSIUS = homeassistant.const.UnitOfTemperature.CELSIUS
ATTR_TEMPERATURE = homeassistant.const.ATTR_TEMPERATURE

AUTH_SCHEMA = vol.Schema({
    vol.Required("username"): str,
    vol.Required("password"): str,
    vol.Required("api_url", default="https://www.myheatpump.com"): str,
})
