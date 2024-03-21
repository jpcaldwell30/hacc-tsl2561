"""Platform for sensor integration."""
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers import config_validation as cv
import voluptuous as vol
import time
import board
import busio
import adafruit_tsl2561

DOMAIN = 'tsl2561_luminosity'

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    add_entities([Tsl2561Sensor()])


class Tsl2561Sensor(RestoreEntity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        i2c = busio.I2C(board.SCL, board.SDA)
        self.tsl = adafruit_tsl2561.TSL2561(i2c)
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

    def update(self):
        """Fetch new state data for the sensor."""
        self._state, self._attributes = self._lightcheck()

    def _lightcheck(self):
        # Enable the light sensor
        self.tsl.enabled = True
        time.sleep(1)

        # Set gain 0=1x, 1=16x
        self.tsl.gain = 0

        # Set integration time (0=13.7ms, 1=101ms, 2=402ms, or 3=manual)
        self.tsl.integration_time = 2

        # Get raw (luminosity) readings individually
        broadband = self.tsl.broadband
        infrared = self.tsl.infrared

        # Get computed lux value (tsl.lux can return None or a float)
        lux = self.tsl.lux
        if lux:
            lux= round(lux, 2)

        # Disble the light sensor (to save power)
        self.tsl.enabled = False

        attributes = {
            "gain": self.tsl.gain,
            "integration_time": self.tsl.integration_time,
            "broadband": broadband,
            "infrared": infrared,
        }

        return lux, attributes
