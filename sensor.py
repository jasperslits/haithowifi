#!/usr/bin/env python3
"""
Sensor component for Itho
Author: Jasper Slits
"""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components import mqtt
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant, callback

import json
from .const.const import *
from .definitions import HRUSENSORS,WPUSENSORS,AUTOTEMPSENSORS, IthoSensorEntityDescription
"""
    _LOGGER,
    DOMAIN,
    CONF_REMOTE_1,
    CONF_REMOTE_2,
    MQTT_STATETOPIC,
    CONF_ID,
    HRU_ACTUAL_MODE,
    WPU_STATUS,
    CONF_CVE_TYPE,
    CONF_USE_WPU,
    CONF_USE_AUTOTEMP,
    CONF_USE_REMOTES,
    AddOnType,
    ADDONS,
    
)
"""





async def _create_remotes(config_entry: ConfigEntry):
    
    cfg = config_entry.data
    
    if cfg[CONF_REMOTE_1] != "": 
        REMOTES = [
        IthoSensorEntityDescription(
        json_field = cfg[CONF_REMOTE_1],
        key=MQTT_STATETOPIC["remotes"],
        translation_key=cfg[CONF_REMOTE_1],
        device_class="carbon_dioxide",
        native_unit_of_measurement="ppm",
        state_class="measurement")]
        
    if cfg[CONF_REMOTE_2] != "": 
        REMOTES.append(
        IthoSensorEntityDescription(
        json_field = cfg[CONF_REMOTE_2],
        key=MQTT_STATETOPIC["remotes"],
        translation_key=cfg[CONF_REMOTE_2],
        device_class="carbon_dioxide",
        native_unit_of_measurement="ppm",
        state_class="measurement"))
    return REMOTES
    
async def _create_autotemprooms(config_entry: ConfigEntry):
    default_rooms = AUTOTEMPSENSORS
    configured_rooms = default_rooms
    return configured_rooms

async def _create_fan_sensors(config_entry: ConfigEntry,aot: AddOnType):
    if aot == AddOnType.CVE:
        default_fans = HRUSENSORS

    if aot == AddOnType.NONCVE:
        default_fans = HRUSENSORS
    default_fans = HRUSENSORS
    configured_fans = default_fans
    return configured_fans


async def async_setup_entry(
    _: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
 #   _LOGGER.warning("String is " + str(config_entry.data))
    """Set up Itho Reader sensors from config entry."""
    if config_entry.data[CONF_CVE_TYPE] == "noncve":
        async_add_entities(IthoSensor(description, config_entry,AddOnType.NONCVE) for description in await _create_fan_sensors(config_entry,AddOnType.NONCVE))
    if config_entry.data[CONF_CVE_TYPE] == "cve":
        async_add_entities(IthoSensor(description, config_entry,AddOnType.CVE) for description in await _create_fan_sensors(config_entry,AddOnType.CVE))
   #     _LOGGER.warning("CVE")
    #    async_add_entities(IthoSensor(description, config_entry,AddOnType.HRU) for description in _create_fan_sensors(config_entry))
    if config_entry.data[CONF_USE_WPU]:
        async_add_entities(IthoSensor(description, config_entry,AddOnType.WPU) for description in WPUSENSORS)
    if config_entry.data[CONF_USE_REMOTES]:
        async_add_entities(IthoSensor(description, config_entry,AddOnType.REMOTES) for description in await _create_remotes(config_entry))
    if config_entry.data[CONF_USE_AUTOTEMP]:
        async_add_entities(IthoSensor(description, config_entry,AddOnType.AUTOTEMP) for description in await _create_autotemprooms(config_entry))

class IthoSensor(SensorEntity):
    """Representation of a Itho sensor that is updated via MQTT."""

    _attr_has_entity_name = True
    entity_description: IthoSensorEntityDescription

    def __init__(
        self, description: IthoSensorEntityDescription, config_entry: ConfigEntry,aot: AddOnType
    ) -> None:
        """Initialize the sensor."""
        self.entity_description = description


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
                if self.aot == AddOnType.NONCVE and self.entity_description.json_field == "Actual Mode":
                    value = HRU_ACTUAL_MODE[value]
                
                if self.aot == AddOnType.WPU and self.entity_description.json_field == "Status":
                    value = WPU_STATUS[value]

                if self.aot == AddOnType.REMOTES:
                    value = value["co2"]

                self._attr_native_value = value

            self.async_write_ha_state()

        await mqtt.async_subscribe(
            self.hass, self.entity_description.key, message_received, 1
        )
