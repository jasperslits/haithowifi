"""Sensor class for handling Autotemp sensors."""

import copy
import json

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo

from .const import (
    ADDON_TYPES,
    AUTOTEMP_ERROR,
    AUTOTEMP_MODE,
    CONF_ADDON_TYPE,
    DOMAIN,
    MANUFACTURER,
    MQTT_BASETOPIC,
    MQTT_STATETOPIC,
)
from .definitions.autotemp import (
    AUTOTEMP_COMM_SPACE_SENSOR_TEMPLATE,
    AUTOTEMP_DISTRIBUTOR_VALVE_SENSOR_TEMPLATE,
    AUTOTEMP_MALFUNCTION_VALVE_DECTECTION_DIST_SENSOR_TEMPLATE,
    AUTOTEMP_ROOM_SENSORS,
    AUTOTEMP_SENSORS,
    AUTOTEMP_VALVE_SENSOR_TEMPLATE,
)
from .definitions.base import IthoSensorEntityDescription
from .sensor_base import IthoBaseSensor


def get_autotemp_sensors(config_entry: ConfigEntry):
    """Create sensors for Autotemp."""
    sensors = []
    topic = f"{MQTT_BASETOPIC["autotemp"]}/{MQTT_STATETOPIC["autotemp"]}"
    for letter in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]:
        description = copy.deepcopy(AUTOTEMP_COMM_SPACE_SENSOR_TEMPLATE)
        description.topic = topic
        description.json_field = description.json_field.replace("X", letter)
        description.translation_placeholders = {"letter": letter}
        description.unique_id = description.unique_id_template.replace("x", letter)
        sensors.append(IthoSensorAutotemp(description, config_entry))

    for d in range(1, 4):
        for v in range(1, 13):
            d = str(d)
            v = str(v)
            description = copy.deepcopy(AUTOTEMP_DISTRIBUTOR_VALVE_SENSOR_TEMPLATE)
            description.topic = topic
            description.json_field = description.json_field.replace("X", d).replace(
                "Y", v
            )
            description.translation_placeholders = {"distributor": d, "valve": v}
            description.unique_id = description.unique_id_template.replace(
                "x", d
            ).replace("y", v)
            sensors.append(IthoSensorAutotemp(description, config_entry))

    for d in range(1, 4):
        d = str(d)
        description = copy.deepcopy(
            AUTOTEMP_MALFUNCTION_VALVE_DECTECTION_DIST_SENSOR_TEMPLATE
        )
        description.topic = topic
        description.json_field = description.json_field.replace("X", d)
        description.translation_placeholders = {"distributor": d}
        description.unique_id = description.unique_id_template.replace("x", d)
        sensors.append(IthoSensorAutotemp(description, config_entry))

    for v in range(1, 4):
        v = str(v)
        template_sensors = copy.deepcopy(list(AUTOTEMP_VALVE_SENSOR_TEMPLATE))
        for description in template_sensors:
            description.topic = topic
            description.json_field = description.json_field.replace("X", v)
            description.translation_placeholders = {"valve": v}
            description.unique_id = description.unique_id_template.replace("x", v)
            sensors.append(IthoSensorAutotemp(description, config_entry))

    for description in AUTOTEMP_SENSORS:
        description.topic = topic
        sensors.append(IthoSensorAutotemp(description, config_entry))

    # Create Room sensors
    for x in range(1, 8):
        template_sensors = copy.deepcopy(list(AUTOTEMP_ROOM_SENSORS))
        room = config_entry.data["room" + str(x)]
        if room not in ("", "Room " + str(x)):
            for description in template_sensors:
                description.json_field = description.json_field.replace("X", str(x))
                description.topic = topic
                description.room = room
                description.unique_id = f"{description.key}_{room}"
                sensors.append(IthoSensorAutotempRoom(description, config_entry))

    return sensors


class IthoSensorAutotemp(IthoBaseSensor):
    """Representation of Itho add-on sensor for Autotemp data that is updated via MQTT."""

    def __init__(
        self,
        description: IthoSensorEntityDescription,
        config_entry: ConfigEntry,
    ) -> None:
        """Construct sensor for Autotemp."""
        super().__init__(description, config_entry)

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""

        @callback
        def message_received(message):
            """Handle new MQTT messages."""
            payload = json.loads(message.payload)
            json_field = self.entity_description.json_field
            if json_field not in payload:
                value = None
            else:
                value = payload[json_field]
                if json_field == "Error":
                    self._extra_state_attributes = {
                        "Code": value,
                    }
                    value = AUTOTEMP_ERROR.get(value, "Unknown error")

                if json_field == "Mode":
                    self._extra_state_attributes = {
                        "Code": value,
                    }
                    value = AUTOTEMP_MODE.get(value, "Unknown mode")

                if json_field == "State off":
                    if value == 1:
                        value = "Off"
                    if payload["State cool"] == 1:
                        value = "Cooling"
                    if payload["State heating"] == 1:
                        value = "Heating"
                    if payload["state hand"] == 1:
                        value = "Hand"

            self._attr_native_value = value
            self.async_write_ha_state()

        await mqtt.async_subscribe(
            self.hass, self.entity_description.topic, message_received, 1
        )


class IthoSensorAutotempRoom(IthoBaseSensor):
    """Representation of Itho add-on room sensor for Autotemp data that is updated via MQTT."""

    def __init__(
        self, description: IthoSensorEntityDescription, config_entry: ConfigEntry
    ) -> None:
        """Construct sensor for Autotemp."""

        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    DOMAIN,
                    f"{config_entry.data[CONF_ADDON_TYPE]}_room_{description.room.lower()}",
                )
            },
            manufacturer=MANUFACTURER,
            model=f"{ADDON_TYPES[config_entry.data[CONF_ADDON_TYPE]]} Spider",
            name=f"Spider {description.room.capitalize()}",
            via_device=(DOMAIN, config_entry.data[CONF_ADDON_TYPE]),
        )

        super().__init__(description, config_entry, use_base_sensor_device=False)

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""

        @callback
        def message_received(message):
            """Handle new MQTT messages."""
            payload = json.loads(message.payload)
            value = payload.get(self.entity_description.json_field, None)

            self._attr_native_value = value
            self.async_write_ha_state()

        await mqtt.async_subscribe(
            self.hass, self.entity_description.topic, message_received, 1
        )
