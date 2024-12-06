"""Init package."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_ADDON_TYPE, CONF_HRU_DEVICE

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the Itho Wifi add-on integration."""

    if entry.data[CONF_ADDON_TYPE] == "noncve":
        new_data = {**entry.data}
        if new_data.get(CONF_HRU_DEVICE) is None:
            new_data[CONF_HRU_DEVICE] = "hru_eco_350"
            hass.config_entries.async_update_entry(entry, data=new_data)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the Itho Wifi add-on integration."""
    # no data stored in hass.data
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
