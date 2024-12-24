"""Sensor base class."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo

from .const import (
    ADDON_TYPES,
    CONF_ADDON_TYPE,
    CONF_NONCVE_MODEL,
    DOMAIN,
    MANUFACTURER,
    NONCVE_DEVICES,
    UNITTYPE_ICONS,
)
from .definitions.base import IthoSensorEntityDescription


class IthoBaseSensor(SensorEntity):
    """Base class sharing foundation for WPU, remotes and Fans."""

    _attr_has_entity_name = True
    entity_description: IthoSensorEntityDescription

    _extra_state_attributes = None

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
            model = ADDON_TYPES[config_entry.data[CONF_ADDON_TYPE]]
            if config_entry.data[CONF_ADDON_TYPE] == "noncve":
                model = (
                    model + " - " + NONCVE_DEVICES[config_entry.data[CONF_NONCVE_MODEL]]
                )

            self._attr_device_info = DeviceInfo(
                identifiers={(DOMAIN, config_entry.data[CONF_ADDON_TYPE])},
                manufacturer=MANUFACTURER,
                model=model,
                name=ADDON_TYPES[config_entry.data[CONF_ADDON_TYPE]],
            )

        if description.unique_id is not None:
            self._attr_unique_id = f"itho_{ADDON_TYPES[config_entry.data[CONF_ADDON_TYPE]]}_{description.unique_id.lower()}"
        else:
            self._attr_unique_id = f"itho_{ADDON_TYPES[config_entry.data[CONF_ADDON_TYPE]]}_{description.key}"
        self.entity_id = f"sensor.{self._attr_unique_id}"

    @property
    def icon(self) -> str | None:
        """Pick the right icon."""

        if self.entity_description.icon is not None:
            return self.entity_description.icon
        if self.entity_description.native_unit_of_measurement in UNITTYPE_ICONS:
            return UNITTYPE_ICONS[self.entity_description.native_unit_of_measurement]
        return None
