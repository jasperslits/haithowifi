"""Variables for Itho add-on."""

from typing import Any

from .const import (
    ADDON_TYPES,
    CONF_ADDON_TYPE,
    CONF_ADVANCED_CONFIG,
    CONF_CUSTOM_BASETOPIC,
    CONF_CUSTOM_DEVICE_NAME,
    CONF_CUSTOM_ENTITY_PREFIX,
    CONF_NONCVE_MODEL,
    MQTT_DEFAULT_BASETOPIC,
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
    return f"itho_{ADDON_TYPES[config[CONF_ADDON_TYPE]].lower()}"


def get_entity_prefix(config: dict[str, Any]) -> str:
    """Get the entity prefix."""
    if config[CONF_ADVANCED_CONFIG]:
        return config[CONF_CUSTOM_ENTITY_PREFIX]

    return get_default_entity_prefix(config)
