"""Definitions for Itho sensors added to MQTT."""

from homeassistant.const import EntityCategory

from .base import IthoSensorEntityDescription

LAST_CMD_SENSORS: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field="command",
        translation_key="last_cmd_command",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:cog",
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="source",
        translation_key="last_cmd_source",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:target",
        entity_registry_enabled_default=False,
    ),
)
