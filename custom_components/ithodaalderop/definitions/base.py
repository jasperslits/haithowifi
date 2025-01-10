"""Definitions for Itho sensors added to MQTT.

A sensor entity represents passive, read-only data provided by a device. It reflects the current state or measurement of something in the environment without directly interacting with or changing the device.
A control entity represents interactive elements that allow the user to send commands or configure a device to change its state or behavior.
A diagnostic entity provides device-specific metadata or operational insights that assist in understanding the device's internal state or functioning but is not directly related to the user's environment.

https://developers.home-assistant.io/docs/core/entity/#entity-description
By default the EntityDescription instance has one required attribute named key.
This is a string which is meant to be unique for all the entity descriptions of an implementing platform.
A common use case for this attribute is to include it in the unique_id of the described entity.

The defined keys within this integration are unique per Itho device. Some are re-used for several devices, such as 'Error'.
The key is also used to define the translation_key and to setup the unique_id of each sensor
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.binary_sensor import BinarySensorEntityDescription
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.const import EntityCategory


@dataclass(frozen=False)
class IthoBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Binary Sensor entity description for Itho."""

    key: str | None = None
    state: Callable | None = None
    json_field: str | None = None
    topic: str | None = None
    icon: str | None = None
    icon_off: str | None = None
    icon_on: str | None = None
    unique_id_template: str | None = None
    unique_id: str | None = None
    entity_category: EntityCategory | None = None
    is_selected_entity: bool = False


@dataclass(frozen=False)
class IthoSensorEntityDescription(SensorEntityDescription):
    """Sensor entity description for Itho."""

    key: str | None = None
    state: Callable | None = None
    json_field: str | None = None
    topic: str | None = None
    icon: str | None = None
    unique_id_template: str | None = None
    unique_id: str | None = None
    entity_category: EntityCategory | None = None
    is_selected_entity: bool = False
