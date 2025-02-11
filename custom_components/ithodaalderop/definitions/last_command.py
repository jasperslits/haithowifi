"""Definitions for Itho Last Command sensors added to MQTT."""

from homeassistant.const import EntityCategory

from .base_definitions import IthoSensorEntityDescription

LAST_CMD_SENSORS: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field="command",
        key="last_cmd_command",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:cog",
        entity_registry_enabled_default=False,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="source",
        key="last_cmd_source",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:target",
        entity_registry_enabled_default=False,
        is_selected_entity=True,
    ),
)
