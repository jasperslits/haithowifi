"""Sensor base class."""

import json

from homeassistant.components import mqtt
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo

from ..const import (
    ADDON_TYPES,
    CONF_ADDON_TYPE,
    CONF_NONCVE_MODEL,
    DOMAIN,
    MANUFACTURER,
    NONCVE_DEVICES,
    UNITTYPE_ICONS,
)
from ..definitions.base import (
    IthoBinarySensorEntityDescription,
    IthoSensorEntityDescription,
)
from ..vars import get_device_model, get_device_name, get_entity_prefix


class IthoBaseSensor(SensorEntity):
    """Base class sharing foundation for WPU, remotes and Fans."""

    _attr_has_entity_name = True
    entity_description: IthoSensorEntityDescription

    _extra_state_attributes: list[str] | None = None

    @property
    def extra_state_attributes(self) -> list[str] | None:
        """Return the state attributes."""
        return self._extra_state_attributes

    def __init__(
        self,
        description: IthoSensorEntityDescription,
        config_entry: ConfigEntry,
        use_base_sensor_device: bool = True,
    ) -> None:
        """Initialize the sensor."""
        self.entity_description = description
        self.entity_description.translation_key = self.entity_description.key

        if use_base_sensor_device:
            self._attr_device_info = DeviceInfo(
                identifiers={
                    (DOMAIN, f"itho_wifi_addon_{get_entity_prefix(config_entry.data)}"),
                },
                manufacturer=MANUFACTURER,
                model=get_device_model(config_entry.data),
                name=get_device_name(config_entry.data),
            )

        if description.unique_id is not None:
            self._attr_unique_id = f"{get_entity_prefix(config_entry.data)}_{description.unique_id.lower()}"
        else:
            self._attr_unique_id = (
                f"{get_entity_prefix(config_entry.data)}_{description.key}"
            )

        self.entity_id = f"sensor.{self._attr_unique_id}"

    @property
    def icon(self) -> str | None:
        """Pick the right icon."""

        if self.entity_description.icon is not None:
            return self.entity_description.icon
        if self.entity_description.native_unit_of_measurement in UNITTYPE_ICONS:
            return UNITTYPE_ICONS[self.entity_description.native_unit_of_measurement]
        return None


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
            identifiers={
                (DOMAIN, f"itho_wifi_addon_{get_entity_prefix(config_entry.data)}"),
            },
            manufacturer=MANUFACTURER,
            model=get_device_model(config_entry.data),
            name=get_device_name(config_entry.data),
        )

        if description.unique_id is not None:
            self._attr_unique_id = f"{get_entity_prefix(config_entry.data)}_{description.unique_id.lower()}"
        else:
            self._attr_unique_id = (
                f"{get_entity_prefix(config_entry.data)}_{description.key}"
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
