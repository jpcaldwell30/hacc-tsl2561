"""Platform for sensor integration."""
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers import config_validation as cv
from homeassistant.components.sensor import SensorDeviceClass
import voluptuous as vol
import time
from tsl2561 import TSL2561

DOMAIN = 'tsl2561_luminosity'

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    add_entities([Tsl2561Sensor()])


class Tsl2561Sensor(RestoreEntity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._attr_device_class = SensorDeviceClass.ILLUMINANCE
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'TSL2561'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "lux"

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes
        
    @property
    def icon(self):
        """Return the icon for the sensor."""
        return "mdi:brightness-6" 

    def update(self):
        """Fetch new state data for the sensor."""
        self._state, self._attributes = self._lightcheck()

    def _lightcheck(self):
        tsl = TSL2561(integration_time=0x01, busnum=1)
        lux = tsl.lux()

        attributes = {
            "gain": tsl.gain,
            "integration_time": tsl.integration_time,
        }

        return lux, attributes
