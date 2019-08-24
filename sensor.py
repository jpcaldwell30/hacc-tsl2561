"""Platform for sensor integration."""
from homeassistant.helpers.restore_state import RestoreEntity

from smbus2 import SMBus
import time

TSLaddr = 0x39      #Default I2C address, alternate 0x29, 0x49
TSLcmd = 0x80       #Command
chan0 = 0x0C        #Read Channel0 sensor date
chan1 = 0x0E        #Read channel1 sensor data
TSLon = 0x03        #Switch sensors on
TSLoff = 0x00       #Switch sensors off

#Exposure settings
LowShort = 0x00     #x1 Gain 13.7 miliseconds
LowMed = 0x01       #x1 Gain 101 miliseconds
LowLong = 0x02      #x1 Gain 402 miliseconds
LowManual = 0x03    #x1 Gain Manual
HighShort = 0x10    #LowLight x16 Gain 13.7 miliseconds
HighMed = 0x11      #LowLight x16 Gain 100 miliseconds
HighLong = 0x12     #LowLight x16 Gain 402 miliseconds
HighManual = 0x13   #LowLight x16 Gain Manual


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    add_entities([Tsl2561Sensor()])


class Tsl2561Sensor(RestoreEntity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None
        self._bus = SMBus(1)

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Luminosita'

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
        self._bus.write_byte(TSLaddr, 0x00 | TSLcmd, TSLon) #Power On
        #Gain x1 at 402ms is the default so this line not required but change for different sensitivity
        self._bus.write_byte(TSLaddr, 0x01 | TSLcmd,LowLong) #Gain x1 402ms

        time.sleep(1) #give time sensor to settle

        #Read Ch0 Word
        data = self._bus.read_i2c_block_data(TSLaddr, chan0 | TSLcmd, 2)
        #Read CH1 Word
        data1 = self._bus.read_i2c_block_data(TSLaddr, chan1 | TSLcmd, 2)

        # Convert the data to Integer
        ch0 = data[1] * 256 + data[0]
        ch1 = data1[1] * 256 + data1[0]
        vResults = ch0-ch1 #get visable light results
        self._bus.write_byte(TSLaddr, 0x00 | TSLcmd, TSLoff) #switch off

        return str(vResults)
