# Author: Patrick Ruddiman
# Notes: Adapted from PECMAC125A.py
# <https://github.com/ControlEverythingCommunity/PECMAC/blob/master/Python/PECMAC125A.py>
# Intended to be more dynamic allowing the user to specify bus and address.

import smbus
import time


class CMAC30AI2C:
    """ Class for the Control Everyting 30 Amp AC Current Monitor  """

    # The address is 0x2A unless youve updated the jumpers
    # The bus is usually the default (1) unless you have more than one I2C device connected.

    def __init__(self, address = 0x2A, bus = 1):
        self.id = "CMAC30AI2C"
        self.address = address
        self.bus = bus

    def ident(self):

        #  Get I2C bus
        I2CBus = smbus.SMBus(self.bus)

        #  CMAC30 address, 0x2A(42)
        #  Command for reading device identification data:
        #  0x6A(106), 0x02(2), 0x00(0),0x00(0), 0x00(0) 0x00(0), 0xFE(254)
        #  Header byte-2, command-2, byte 3, 4, 5 and 6 are reserved, checksum
        command = [0x6A, 0x02, 0x00, 0x00, 0x00, 0x00, 0xFE]
        I2CBus.write_i2c_block_data(self.address, 0x92, command)

        # Take a short nap
        time.sleep(0.5)

        # Time to read the data back
        #  Read data back from 0x55(85), 3 bytes
        #  Type of Sensor, Maximum Current, No. of Channels
        identity = I2CBus.read_i2c_block_data(self.address, 0x55, 3)

        #  Convert the data
        self.maxCurrent = identity[1]
        self.numChannels = identity[2]


        #  Output data to screen
        print "ID: %s" %self.id
        print "Maximum Current : %d A" %self.maxCurrent
        print "No. of Channels : %d" %self.numChannels

    def readCurrent(self):
        #  Get I2C bus
        I2CBus = smbus.SMBus(self.bus)

        #  Command for reading current
        #  0x6A(106), 0x01(1), 0x01(1),0x0C(12), 0x00(0), 0x00(0) 0x0A(10)
        #  Header byte-2, command-1, start channel-1, stop channel-12, byte 5 and 6 reserved, checksum
        command = [0x6A, 0x01, 0x01, 0x0C, 0x00, 0x00, 0x0A]
        I2CBus.write_i2c_block_data(self.address, 0x92, command)

        time.sleep((1/60))

        #  Read data back from 0x55(85), No. of Channels * 3 bytes
        #  current MSB1, current MSB, current LSB
        data = I2CBus.read_i2c_block_data(self.address, 0x55, self.numChannels * 3)

        index = self.numChannels - 1
        #  Convert the data
        #  we use self.numChannels but in reality this could be ' 1 ' (0) since we know its only one channel;
        #  Write a new class if your sensor has more than one channel and loop over this
        #  If you are using a multi channel device this is where you loop from 0 to numChannels-1
        msb1 = data[index * 3]
        msb = data[1 + index * 3]
        lsb = data[2 + index * 3]

        #  Convert the data to ampere
        current = (msb1 * 65536 + msb * 256 + lsb) / 1000.0

        print "Current: %d Amps" %current
        return current


