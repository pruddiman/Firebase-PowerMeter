# Author: Patrick Ruddiman
# Notes: Uses the firebase python plugin for firebase communication
# Data are stored in the following format:
#
# /data/YEAR/MONTH/DAY/HOUR/MINUTE/SECOND
#
# For example: /data/2018/2/5/14/30/10 will return the power measurement taken at 14:30:10 on February 5th 2018
# The object looks like this: {"current": I, "voltage": V, "watts": W}


from firebase import firebase
import sys
import datetime as _d
import time as _t


class fbDatastore:

    def __init__(self, address):
        self.address = address
        self.firebase = firebase.FirebaseApplication(self.address, authentication=None)
        auth = firebase.FirebaseAuthentication('AUTH_KEYHERE', 'EMAIL@DOMAIN.COM', extra={'id': 'USERID'})
        self.firebase.authentication = auth

    def setEnergy(self, kWh):
        # Use current year and month for the keys in the DB
        year = _d.datetime.fromtimestamp(int(_t.time())).strftime("%Y")
        month = _d.datetime.fromtimestamp(int(_t.time())).strftime("%B")

        try:
            # Write MTD Energy usage
            self.firebase.put("/Energy/"+year, month, kWh)
        except:
            self.reportError(sys.exc_info()[0])

    def getEnergy(self):
        # Use current year and month for the keys in the DB
        year = _d.datetime.fromtimestamp(int(_t.time())).strftime("%Y")
        month = _d.datetime.fromtimestamp(int(_t.time())).strftime("%B")
        
        Energy = self.firebase.get("/Energy/"+year, month)
        return Energy

    # Voltage is hard-coded here. It might be nice to add an AC voltage sensor for better accuracy
    # TODO:Add an I2C voltage sensor
    def writeNewPowerEntry(self, timestamp, current, voltage=115):

        try:
            # Update live stats
            self.firebase.put('/', 'live', {"current": current, "voltage": voltage, "watts": current*voltage})
        except:
            self.reportError(sys.exc_info()[0])
        
        # Store the rest by date:
        year = _d.datetime.fromtimestamp(timestamp).strftime("%Y")
        month = _d.datetime.fromtimestamp(timestamp).strftime("%B")
        day = _d.datetime.fromtimestamp(timestamp).strftime("%-d")
        hour = _d.datetime.fromtimestamp(timestamp).strftime("%-H")
        minute = _d.datetime.fromtimestamp(timestamp).strftime("%-M")
        second = _d.datetime.fromtimestamp(timestamp).strftime("%-S")

        try:
            # Write to DB
            self.firebase.put('/data/'+year+'/'+month+'/'+day+'/'+hour+'/'+minute, second, {"current": current, 'voltage': voltage, 'watts':current*voltage, "timestamp": timestamp})
        except Exception as e:
            self.reportError(str(e))


    def reportError(self, error):
        self.firebase.put_async('/error', int(_t.time()), error)
