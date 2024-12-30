#!/usr/bin/env python3
"""Binary Sensor component for Itho.

Author: Benjamin
"""

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import _LOGGER, CONF_ADDON_TYPE
from .sensors.autotemp import get_autotemp_binary_sensors
from .sensors.fan import get_cve_binary_sensors, get_noncve_binary_sensors
from .sensors.wpu import get_wpu_binary_sensors


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Itho add-on binary sensors from config entry based on their type."""

    if not await mqtt.async_wait_for_mqtt_client(hass):
        _LOGGER.error("MQTT integration is not available")
        return

    sensors = []
    selected_sensors = []
    if config_entry.data[CONF_ADDON_TYPE] == "autotemp":
        sensors.extend(get_autotemp_binary_sensors(config_entry))

    if config_entry.data[CONF_ADDON_TYPE] == "cve":
        sensors.extend(get_cve_binary_sensors(config_entry))

    if config_entry.data[CONF_ADDON_TYPE] == "noncve":
        sensors.extend(get_noncve_binary_sensors(config_entry))

    if config_entry.data[CONF_ADDON_TYPE] == "wpu":
        sensors.extend(get_wpu_binary_sensors(config_entry))

    for sensor in sensors:
        if (
            config_entry.data[CONF_ENTITIES_CREATION_MODE] == "only_selected"
            and not sensor.entity_description.is_selected_entity
        ):
            continue
        selected_sensors.append(sensor)

    async_add_entities(selected_sensors)


class IthoBinarySensor(BinarySensorEntity):
    """Representation of a Itho add-on binary sensor that is updated via MQTT."""

    _attr_has_entity_name = True
    entity_description: IthoBinarySensorEntityDescription

    def __init__(
        self,
        description: IthoBinarySensorEntityDescription,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the binary sensor."""
        self.entity_description = description
        self.entity_description.translation_key = self.entity_description.key

        model = ADDON_TYPES[config_entry.data[CONF_ADDON_TYPE]]
        if config_entry.data[CONF_ADDON_TYPE] == "noncve":
            model = f"{model} - {NONCVE_DEVICES[config_entry.data[CONF_NONCVE_MODEL]]}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.data[CONF_ADDON_TYPE])},
            manufacturer=MANUFACTURER,
            model=model,
            name=f"Itho Daalderop {ADDON_TYPES[config_entry.data[CONF_ADDON_TYPE]]}",
        )

        self._attr_unique_id = (
            f"itho_{ADDON_TYPES[config_entry.data[CONF_ADDON_TYPE]]}_{description.key}"
        )
        self.entity_id = f"binary_sensor.{self._attr_unique_id}"

    @property
    def icon(self):
        """Icon for binary sensor."""
        if (
            self.entity_description.icon_off is not None
            and self.entity_description.icon_on is not None
        ):
            if self._attr_is_on:
                return self.entity_description.icon_on
            return self.entity_description.icon_off
        if self.entity_description.icon is not None:
            return self.entity_description.icon
        return None

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
                value = bool(payload[json_field])

            self._attr_is_on = value
            self.async_write_ha_state()

        await mqtt.async_subscribe(
            self.hass, self.entity_description.topic, message_received, 1
        )
