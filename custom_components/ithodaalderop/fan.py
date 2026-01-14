"""Fan component for Itho."""

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import _LOGGER, CONF_ADDON_TYPE, CONF_NONCVE_MODEL
from .fans.cve_hru200 import get_cve_hru200_fan
from .fans.hru250_300 import get_hru250_300_fan
from .fans.hru350 import get_hru350_fan
from .fans.demandflow import get_df_fan


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the MQTT fan from configuration.yaml."""

    if not await mqtt.async_wait_for_mqtt_client(hass):
        _LOGGER.error("MQTT integration is not available")
        return

    if config_entry.data[CONF_ADDON_TYPE] == "cve":
        async_add_entities(get_cve_hru200_fan(config_entry))
    elif config_entry.data[CONF_ADDON_TYPE] == "noncve":
        model = config_entry.data[CONF_NONCVE_MODEL]
        if model == "hru_eco_200":
            async_add_entities(get_cve_hru200_fan(config_entry))
        elif model in ["hru_eco_250", "hru_eco_300"]:
            async_add_entities(get_hru250_300_fan(config_entry))
        elif model == "hru_eco_350":
            async_add_entities(get_hru350_fan(config_entry))
        elif model == "demand_flow":
            async_add_entities(get_df_fan(config_entry))
