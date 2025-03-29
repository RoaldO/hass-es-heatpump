# <config_dir>/custom_components/heatpump_cloud/__init__.py
PLATFORMS = ["climate", "sensor"]  # Add sensor platform

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up with installation identifier"""
    api = HeatPumpCloudAPI(
        username=entry.data["username"],
        password=entry.data["password"],
        api_url=entry.data["api_url"],
        session_url=entry.data["session_url"],
        mn=entry.data["mn"]  # Pass mn from config
    )

    # Rest of the setup remains the same
    try:
        await api.authenticate()
    except Exception as err:
        _LOGGER.error("Initial authentication failed: %s", err)
        return False

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"heatpump_{entry.data['mn']}",
        update_method=api.async_get_status,
        update_interval=timedelta(seconds=30),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "api": api
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Add parameter mappings to coordinator data
    coordinator.data["parameter_mappings"] = entry.data.get("parameter_mappings", {})

    # Forward to both climate and sensor platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True