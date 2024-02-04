"""Platform for sensor integration."""
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers import config_validation as cv
from homeassistant.const import CONF_PIN_NUMBER
import RPi.GPIO as GPIO
import voluptuous as vol
import time

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_PIN_NUMBER, default=27): cv.positive_int,
    })
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    pin_number = config.get('pin_number', 27)  # Default to 27 if not provided
    add_entities([Tsl2561Sensor(pin_number)])


class Tsl2561Sensor(RestoreEntity):
    """Representation of a Sensor."""

    def __init__(self, pin_number):
        """Initialize the sensor."""
        self._state = None
        self._pin_number = pin_number
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'tsl2561'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "lux"

    def update(self):
        """Fetch new state data for the sensor."""
        self._state = self._lightcheck()

    def _lightcheck(self):
        LDRCount = 0 # Sets the count to 0
        GPIO.setup(self._pin_number, GPIO.OUT)
        GPIO.output(self._pin_number, GPIO.LOW)
        time.sleep(0.1) # Drains all charge from the capacitor
        GPIO.setup(self._pin_number, GPIO.IN) # Sets the pin to be input
        # While the input pin reads ‘off’ or Low, count
        while (GPIO.input(self._pin_number) == GPIO.LOW):
            LDRCount += 1 # Add one to the counter
        return LDRCount
