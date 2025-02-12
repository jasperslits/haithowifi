"""Fan base class."""

from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo

from ..const import DOMAIN, MANUFACTURER
from ..definitions.base_definitions import IthoFanEntityDescription
from ..utils import get_device_model, get_device_name, get_entity_prefix


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
            identifiers={(DOMAIN, get_entity_prefix(config_entry.data))},
            manufacturer=MANUFACTURER,
            model=get_device_model(config_entry.data),
            name=get_device_name(config_entry.data),
        )
        self._attr_unique_id = (
            f"{get_entity_prefix(config_entry.data)}_{description.key}".lower()
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
