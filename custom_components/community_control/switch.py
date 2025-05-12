"""Switch platform for Community Control integration."""
import asyncio
import logging
import socket
import voluptuous as vol

from homeassistant.components.switch import SwitchEntity, PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, CONF_HOST, CONF_PORT
import homeassistant.helpers.config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, DEFAULT_PORT, CONF_COMMAND

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_COMMAND): cv.string,
    }
)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType = None,
) -> None:
    """Set up the Community Control switch."""
    host = config.get(CONF_HOST)
    port = config.get(CONF_PORT)
    name = config.get(CONF_NAME)
    command = config.get(CONF_COMMAND)

    async_add_entities([CommunityControlSwitch(host, port, name, command)], True)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Community Control switch from a config entry."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    
    host = config.get(CONF_HOST)
    port = config.get(CONF_PORT)
    name = config.get(CONF_NAME)
    command = config.get(CONF_COMMAND)

    async_add_entities([CommunityControlSwitch(host, port, name, command)], True)


class CommunityControlSwitch(SwitchEntity):
    """Representation of a Community Control switch."""

    def __init__(self, host, port, name, command):
        """Initialize the Community Control switch."""
        self._host = host
        self._port = port
        self._name = name
        self._command = command
        self._state = False
        self._attr_unique_id = f"community_control_{host}_{port}_{command}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self._attr_unique_id)},
            "name": self._name,
            "manufacturer": "Community Control",
            "model": "Door Control",
            "sw_version": "1.0.0",
        }

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._state

    async def async_turn_on(self, **kwargs):
        """Turn the device on."""
        await self.hass.async_add_executor_job(self._send_command)
        self._state = True
        self.async_write_ha_state()
        # Auto turn off after a short period since this is momentary
        self.hass.loop.call_later(2, self._auto_turn_off)

    def _auto_turn_off(self):
        """Turn the device off after a delay."""
        self._state = False
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the device off."""
        # For a door control, turn_off doesn't do anything
        self._state = False
        self.async_write_ha_state()

    def _send_command(self):
        """Send UDP command to the device."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # Convert hex string to bytes
            try:
                command_bytes = bytes.fromhex(self._command)
            except ValueError:
                _LOGGER.error("Invalid hex command: %s", self._command)
                return
            
            sock.sendto(command_bytes, (self._host, self._port))
            _LOGGER.debug(
                "Sent command %s to %s:%s", 
                self._command, 
                self._host, 
                self._port
            )
        except Exception as e:
            _LOGGER.error("Error sending command: %s", str(e))
        finally:
            sock.close()
