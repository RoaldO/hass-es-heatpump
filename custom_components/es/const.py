import homeassistant.components.climate.const
import homeassistant.const
import voluptuous as vol

DOMAIN = "es"
PLATFORMS = ["climate"]

HVAC_MODE_HEAT = homeassistant.components.climate.const.HVACMode.HEAT
HVAC_MODE_COOL = homeassistant.components.climate.const.HVACMode.COOL
HVAC_MODE_OFF = homeassistant.components.climate.const.HVACMode.OFF
SUPPORTED_MODES = [HVAC_MODE_HEAT, HVAC_MODE_COOL, HVAC_MODE_OFF]

TEMP_CELSIUS = homeassistant.const.UnitOfTemperature.CELSIUS
ATTR_TEMPERATURE = homeassistant.const.ATTR_TEMPERATURE

AUTH_SCHEMA = vol.Schema({
    vol.Required("username"): str,
    vol.Required("password"): str,
    vol.Required("api_url", default="https://www.myheatpump.com"): str,
})
