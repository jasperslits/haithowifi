"""Internally used utilities."""

from typing import Any

from .const import (
    ADDON_TYPES,
    CONF_ADDON_TYPE,
    CONF_ADVANCED_CONFIG,
    CONF_AUTO_DETECT,
    CONF_CUSTOM_BASETOPIC,
    CONF_CUSTOM_DEVICE_NAME,
    CONF_CUSTOM_ENTITY_PREFIX,
    CONF_NONCVE_MODEL,
    MQTT_COMMAND_TOPIC,
    MQTT_DEFAULT_BASETOPIC,
    MQTT_STATETOPIC,
    NONCVE_DEVICES,
)


def get_default_mqtt_base_topic(config: dict[str, Any]) -> str:
    """Get the default MQTT base topic."""
    if config.get(CONF_AUTO_DETECT, False):
        return config[CONF_CUSTOM_BASETOPIC]
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
    return f"{get_mqtt_base_topic(config)}/{MQTT_STATETOPIC['remote']}"


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
    return f"itho_{ADDON_TYPES[config[CONF_ADDON_TYPE]]}".lower()


def get_entity_prefix(config: dict[str, Any]) -> str:
    """Get the entity prefix."""
    if config[CONF_ADVANCED_CONFIG]:
        return config[CONF_CUSTOM_ENTITY_PREFIX].lower()

    return get_default_entity_prefix(config)
