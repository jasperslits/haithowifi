"""Internally used utilities."""

from typing import Any

from homeassistant.helpers.device_registry import DeviceInfo

from .const import (
    ADDON_TYPES,
    CONF_ADDON_TYPE,
    CONF_ADVANCED_CONFIG,
    CONF_AUTOTEMP_ROOM,
    CONF_AUTOTEMP_SPIDER,
    CONF_CUSTOM_BASETOPIC,
    CONF_CUSTOM_DEVICE_NAME,
    CONF_CUSTOM_ENTITY_PREFIX,
    CONF_NONCVE_MODEL,
    DOMAIN,
    MANUFACTURER,
    MAX_ROOMS,
    MQTT_COMMAND_TOPIC,
    MQTT_DEFAULT_BASETOPIC,
    MQTT_STATETOPIC,
    NONCVE_DEVICES,
)


def get_default_mqtt_base_topic(config: dict[str, Any]) -> str:
    """Get the default MQTT base topic."""
    return MQTT_DEFAULT_BASETOPIC[config[CONF_ADDON_TYPE]]


def get_mqtt_base_topic(config: dict[str, Any]) -> str:
    """Get the MQTT base topic."""
    if config[CONF_ADVANCED_CONFIG]:
        return config[CONF_CUSTOM_BASETOPIC]

    return get_default_mqtt_base_topic(config)


def get_mqtt_command_topic(config: dict[str, Any]) -> str:
    """Get the MQTT command topic."""
    return f"{get_mqtt_base_topic(config)}/{MQTT_COMMAND_TOPIC}"


def get_mqtt_state_topic(config: dict[str, Any]) -> str:
    """Get the MQTT state topic."""
    return f"{get_mqtt_base_topic(config)}/{MQTT_STATETOPIC[config[CONF_ADDON_TYPE]]}"


def get_mqtt_remote_topic(config: dict[str, Any]) -> str:
    """Get the MQTT remote topic."""
    return f"{get_mqtt_base_topic(config)}/{MQTT_STATETOPIC["remote"]}"


def get_device_model(config: dict[str, Any]) -> str:
    """Get the device model."""
    if config[CONF_ADDON_TYPE] == "noncve":
        return NONCVE_DEVICES[config[CONF_NONCVE_MODEL]]

    return ADDON_TYPES[config[CONF_ADDON_TYPE]]


def get_device_name(config: dict[str, Any]) -> str:
    """Get the device name."""
    if config[CONF_ADVANCED_CONFIG]:
        return config[CONF_CUSTOM_DEVICE_NAME]

    return get_device_model(config)


def get_default_entity_prefix(config: dict[str, Any]) -> str:
    """Get the default entity prefix."""
    return f"itho_{ADDON_TYPES[config[CONF_ADDON_TYPE]]}".replace("-","_").lower()


def get_entity_prefix(config: dict[str, Any]) -> str:
    """Get the entity prefix."""
    if config[CONF_ADVANCED_CONFIG]:
        return config[CONF_CUSTOM_ENTITY_PREFIX].lower()

    return get_default_entity_prefix(config)


def get_device_info(config: dict[str, Any]) -> DeviceInfo:
    """Get the device of the add-on."""
    return DeviceInfo(
        identifiers={(DOMAIN, get_entity_prefix(config))},
        manufacturer=MANUFACTURER,
        model=get_device_model(config),
        name=get_device_name(config),
    )


def get_room_device_info(config: dict[str, Any], room: str) -> DeviceInfo:
    """Get the device of an autotemp room."""
    name = f"Spider {room.capitalize()}"
    if config[CONF_ADVANCED_CONFIG]:
        name = f"{config[CONF_CUSTOM_DEVICE_NAME]} - {name}"
    return DeviceInfo(
        identifiers={(DOMAIN, f"{get_entity_prefix(config)}_room_{room}".lower())},
        manufacturer=MANUFACTURER,
        model=f"{ADDON_TYPES[config[CONF_ADDON_TYPE]]} Spider",
        name=name,
    )


def get_rooms(config: dict[str, Any]) -> dict[int, tuple[str, str]]:
    """Get {number: (room name, Spider name)} for the autotemp rooms in use."""
    rooms = {}
    for number in range(1, MAX_ROOMS + 1):
        room = config.get(CONF_AUTOTEMP_ROOM.format(number), "")
        if room not in ("", f"Room_{number}"):
            rooms[number] = (room, config.get(CONF_AUTOTEMP_SPIDER.format(number), ""))
    return rooms
