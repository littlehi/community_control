"""Config flow for Community Control integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT
from homeassistant.core import callback

from .const import DOMAIN, DEFAULT_PORT, CONF_COMMAND

_LOGGER = logging.getLogger(__name__)

class CommunityControlConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Community Control."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate hex command
            try:
                bytes.fromhex(user_input[CONF_COMMAND])
            except ValueError:
                errors[CONF_COMMAND] = "invalid_command"
            
            if not errors:
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME): str,
                    vol.Required(CONF_HOST): str,
                    vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
                    vol.Required(CONF_COMMAND): str,
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return CommunityControlOptionsFlowHandler(config_entry)


class CommunityControlOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_HOST, 
                        default=self.config_entry.data.get(CONF_HOST)
                    ): str,
                    vol.Required(
                        CONF_PORT, 
                        default=self.config_entry.data.get(CONF_PORT, DEFAULT_PORT)
                    ): int,
                    vol.Required(
                        CONF_COMMAND, 
                        default=self.config_entry.data.get(CONF_COMMAND)
                    ): str,
                }
            ),
        )
