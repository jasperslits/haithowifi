"""Fan base class."""

from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo

from ..const import ADDON_TYPES, CONF_ADDON_TYPE, DOMAIN
from ..definitions.base_definitions import IthoFanEntityDescription


class IthoBaseFan(FanEntity):
    """Base class sharing foundation for fan entities."""

    _attr_has_entity_name = True
    entity_description: IthoFanEntityDescription

    def __init__(
        self,
        description: IthoFanEntityDescription,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the fan."""
        self.entity_description = description
        self._preset_mode = None

        self.entity_description.translation_key = self.entity_description.key

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.data[CONF_ADDON_TYPE])}
        )
        self._attr_unique_id = (
            f"itho_{ADDON_TYPES[config_entry.data[CONF_ADDON_TYPE]]}_{description.key}"
        )
        self.entity_id = f"fan.{self._attr_unique_id}"

    @property
    def preset_modes(self):
        """Return the available preset modes."""
        return self.entity_description.preset_modes

    @property
    def supported_features(self) -> FanEntityFeature:
        """Return the list of supported features."""
        return self.entity_description.supported_features

    @property
    def preset_mode(self):
        """Return the current preset mode."""
        return self._preset_mode
