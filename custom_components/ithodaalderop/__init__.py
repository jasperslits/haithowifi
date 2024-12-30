"""Init package."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_ADDON_TYPE, CONF_NONCVE_MODEL

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR, Platform.UPDATE]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the Itho Wifi add-on integration."""

    # Migrate noncve config < v2.2.0 to 2.2.0+
    # < 2.2.0 Only 1 HRU was supported. This was the HRU ECO 350
    # So, if no hru_device is setup, this has to be the hru_eco_350
    if (
        entry.data[CONF_ADDON_TYPE] == "noncve"
        and entry.data.get(CONF_NONCVE_MODEL) is None
    ):
        new_data = {**entry.data}
        new_data[CONF_NONCVE_MODEL] = "hru_eco_350"
        hass.config_entries.async_update_entry(entry, data=new_data)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the Itho Wifi add-on integration."""
    # no data stored in hass.data
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
