#!/usr/bin/env python3
"""
Sensor component for Itho
Author: Jasper Slits
"""
from typing import List
import voluptuous as vol
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import urllib.error
import re
import json
from .const.const import (
    _LOGGER,
    DOMAIN,
    CONF_HRU_STATETOPIC,
    CONF_WPU_STATETOPIC,
    CONF_AUTOTEMP_STATETOPIC,
    CONF_ID,
    HRU_ACTUAL_MODE,
    WPU_STATUS,
    CONF_USE_HRU,
    CONF_USE_WPU,
    CONF_USE_AUTOTEMP,
    CONF_USE_REMOTES,
    AddOnType,
    ADDONS
)



from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_RESOURCES
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components import mqtt
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.util import slugify
from .definitions import HRUSENSORS,WPUSENSORS,AUTOTEMPSENSORS, IthoSensorEntityDescription

async def async_setup_entry(
    _: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Itho Reader sensors from config entry."""
    if config_entry.data[CONF_USE_HRU]:
        async_add_entities(IthoSensor(description, config_entry,AddOnType.HRU) for description in HRUSENSORS)
    if config_entry.data[CONF_USE_WPU]:
        async_add_entities(IthoSensor(description, config_entry,AddOnType.WPU) for description in WPUSENSORS)
    #if config_entry.data[CONF_USE_REMOTES]:

    #if config_entry.data[CONF_USE_AUTOTEMP]:


class IthoSensor(SensorEntity):
    """Representation of a Itho sensor that is updated via MQTT."""

    _attr_has_entity_name = True
    entity_description: IthoSensorEntityDescription

    def __init__(
        self, description: IthoSensorEntityDescription, config_entry: ConfigEntry,aot: AddOnType
    ) -> None:
        """Initialize the sensor."""
        self.entity_description = description

        slug = slugify(description.key.replace("/", "_"))
        self.entity_id = f"sensor.{ADDONS[aot].lower()}_{description.translation_key}"
        self._attr_unique_id = f"{config_entry.entry_id}-{description.translation_key}"
        self.aot = aot
    
    @property
    def name(self):
        return self.entity_description.translation_key.replace("_"," ").capitalize()

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""

        @callback
        def message_received(message):
            """Handle new MQTT messages."""
           # _LOGGER.info(message)
            if message.payload == "":
                self._attr_native_value = None
            elif self.entity_description.state is not None:
                # Perform optional additional parsing
                self._attr_native_value = self.entity_description.state(message.payload)
            else:
                payload = json.loads(message.payload)
                value = payload[self.entity_description.json_field]
                if self.aot == AddOnType.HRU and self.entity_description.json_field == "Actual Mode":
                    value = HRU_ACTUAL_MODE[value]
                
                if self.aot == AddOnType.WPU and self.entity_description.json_field == "Status":
                    value = WPU_STATUS[value]
                
                self._attr_native_value = value

            self.async_write_ha_state()

        await mqtt.async_subscribe(
            self.hass, self.entity_description.key, message_received, 1
        )
