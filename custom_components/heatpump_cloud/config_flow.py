# <config_dir>/custom_components/heatpump_cloud/config_flow.py
from homeassistant import config_entries
import voluptuous as vol

PARAM_MAPPING_SCHEMA = vol.Schema({
    vol.Required("parameter"): vol.All(
        vol.Coerce(int),
        vol.Range(min=1, max=100)
    ),
    vol.Required("name"): str,
})


class HeatPumpConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    async def async_step_mapping(self, user_input=None):
        """Step for adding parameter mappings"""
        errors = {}
        mappings = self.mappings = self.handler.mappings

        if user_input is not None:
            try:
                param = user_input["parameter"]
                name = user_input["name"].strip().lower()

                if any(m["name"] == name for m in mappings.values()):
                    errors["base"] = "name_exists"
                else:
                    mappings[str(param)] = {"name": name}

                return self.async_show_form(
                    step_id="mapping",
                    data_schema=PARAM_MAPPING_SCHEMA,
                    errors=errors,
                    description_placeholders={"mapped_count": len(mappings)}
                )
            except ValueError:
                errors["base"] = "invalid_param"

        return self.async_show_form(
            step_id="mapping",
            data_schema=PARAM_MAPPING_SCHEMA,
            errors=errors,
            description_placeholders={"mapped_count": 0}
        )

    async def async_step_user(self, user_input=None):
        """Modified user step with mapping configuration"""
        # ... existing authentication logic ...

        # After successful auth
        self.mappings = {}
        return await self.async_step_mapping()