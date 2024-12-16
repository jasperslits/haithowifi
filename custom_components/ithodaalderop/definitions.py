"""Definitions for Itho sensors added to MQTT.

A sensor entity represents passive, read-only data provided by a device. It reflects the current state or measurement of something in the environment without directly interacting with or changing the device.
A control entity represents interactive elements that allow the user to send commands or configure a device to change its state or behavior.
A diagnostic entity provides device-specific metadata or operational insights that assist in understanding the device's internal state or functioning but is not directly related to the user's environment.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.binary_sensor import BinarySensorEntityDescription
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.const import EntityCategory


@dataclass(frozen=False)
class IthoSensorEntityDescription(SensorEntityDescription):
    """Sensor entity description for Itho."""

    state: Callable | None = None
    json_field: str | None = None
    key: str | None = None
    icon: str | None = None
    affix: str | None = None
    entity_category: EntityCategory | None = None


@dataclass(frozen=False)
class IthoBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Binary Sensor entity description for Itho."""

    state: Callable | None = None
    json_field: str | None = None
    key: str | None = None
    icon: str | None = None
    icon_off: str | None = None
    icon_on: str | None = None
    affix: str | None = None
    entity_category: EntityCategory | None = None


LASTCMDSENSORS: tuple[IthoSensorEntityDescription, ...] = (
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
