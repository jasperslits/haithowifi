"""Init package."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import (
    CONF_ADDON_TYPE,
    CONF_ADVANCED_CONFIG,
    CONF_ENTITIES_CREATION_MODE,
    CONF_NONCVE_MODEL,
)

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the Itho Wifi add-on integration."""

    # Migrate noncve config from < v2.2.0
    # < 2.2.0 Only 1 HRU was supported. This was the HRU ECO 350
    # So, if no hru_device is setup, this has to be the hru_eco_350
    if (
        entry.data[CONF_ADDON_TYPE] == "noncve"
        and entry.data.get(CONF_NONCVE_MODEL) is None
    ):
        new_data = {**entry.data}
        new_data[CONF_NONCVE_MODEL] = "hru_eco_350"
        hass.config_entries.async_update_entry(entry, data=new_data)

    # Migrate entities_creation_mode config from < v2.2.0
    if entry.data.get(CONF_ENTITIES_CREATION_MODE) is None:
        new_data = {**entry.data}
        new_data[CONF_ENTITIES_CREATION_MODE] = "only_selected"
        hass.config_entries.async_update_entry(entry, data=new_data)

    # Migrate advanced_config config from < 2.5.0
    if entry.data.get(CONF_ADVANCED_CONFIG) is None:
        new_data = {**entry.data}
        new_data[CONF_ADVANCED_CONFIG] = False
        hass.config_entries.async_update_entry(entry, data=new_data)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the Itho Wifi add-on integration."""
    # no data stored in hass.data
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
