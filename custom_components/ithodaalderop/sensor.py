#!/usr/bin/env python3
"""Sensor component for Itho WiFi addon.

Author: Jasper
"""

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import _LOGGER, CONF_ADDON_TYPE, CONF_ENTITIES_CREATION_MODE
from .sensors.autotemp import get_autotemp_sensors
from .sensors.co2_remote import get_co2_remote_sensors
from .sensors.fan import get_cve_sensors, get_noncve_sensors
from .sensors.last_command import get_last_command_sensors
from .sensors.wpu import get_wpu_sensors


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Itho add-on sensors from config entry based on their type."""

    if not await mqtt.async_wait_for_mqtt_client(hass):
        _LOGGER.error("MQTT integration is not available")
        return

    sensors = []
    selected_sensors = []
    if config_entry.data[CONF_ADDON_TYPE] == "autotemp":
        sensors.extend(get_autotemp_sensors(config_entry))

    if config_entry.data[CONF_ADDON_TYPE] == "cve":
        sensors.extend(get_cve_sensors(config_entry))

    if config_entry.data[CONF_ADDON_TYPE] == "noncve":
        sensors.extend(get_noncve_sensors(config_entry))

    if config_entry.data[CONF_ADDON_TYPE] in ["cve", "noncve"]:
        sensors.extend(get_co2_remote_sensors(config_entry))
        sensors.extend(get_last_command_sensors(config_entry))

    if config_entry.data[CONF_ADDON_TYPE] == "wpu":
        sensors.extend(get_wpu_sensors(config_entry))

    """New parameter CONF_ENTITIES_CREATION_MODE is not present in prior releases."""
    for sensor in sensors:
        if (
            CONF_ENTITIES_CREATION_MODE not in config_entry.data
            or config_entry.data[CONF_ENTITIES_CREATION_MODE] == "only_selected"
        ) and not sensor.entity_description.is_selected_entity:
            continue
        selected_sensors.append(sensor)

    async_add_entities(selected_sensors)
