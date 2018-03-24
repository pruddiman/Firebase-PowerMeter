# Author: Patrick Ruddiman

from I2CCMAC.CMAC30AI2C import CMAC30AI2C
from datastore.fbDatastore import fbDatastore
import time
import datetime

database = fbDatastore('FIREBASE_DATASTORE_URL')
month = datetime.date.today().month


def calcDeltaWh(_energy, last_time, current_time, current):

    if month != datetime.date.today().month:
        global month
        month = datetime.date.today().month
        database.setEnergy(0)

    deltaT = (current_time-last_time)
    e = _energy + (((current*115)*(deltaT))/(60*60))
    database.setEnergy(e)
    return e


def main():
    energy = database.getEnergy()
    if energy is None:
        database.setEnergy(0)
        energy = 0
    
    start = time.time()
    device = CMAC30AI2C(0x2A, 1)
    device.ident()
    while True:
        now = int(time.time())
        current = device.readCurrent()
        database.writeNewPowerEntry(now, current)
        energy = calcDeltaWh(energy, start, now, current)
        start = int(now)
        time.sleep(10)


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    print "Power Meter Monitor \n"
    
    main()
