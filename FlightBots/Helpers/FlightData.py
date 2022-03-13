#Kyle R Fogerty

from FlightRadar24.api import FlightRadar24API
from FlightBots.Templates.FlightLog import FlightLog
import pickle
import os

class FlightData:
    #Removes Any Flights Marked Grounded
    def removeGroundedFligts(self, logs):
        new_logs = []
        for i in range(0, len(logs)):
            if len(logs[i].logs) > 1:
                if logs[i].logs[-1].on_ground == False:
                    new_logs.append(logs[i])
        return new_logs

    #Resets all logs to not updated prior to grabbing new data
    def resetUpdateFlags(self):
        for index in range(0, len(self.activate_flights)):
            self.activate_flights[index].resetUpdateFlag()

    def query(self):
        if len(self.activate_flights) > 0: #Set All Logs To Not Updated
            self.resetUpdateFlags()
        #Get All Current Flights In Zone
        current_flights = self.fr_api.get_flights()
        #Search for flight id in current flight logs
        for flight in current_flights:
            in_db = False
            for log_index in range(0, len(self.activate_flights)):
                #Auto Add If List is empty
                if len(self.activate_flights) == 0:
                    break #Break to add sections
                #Check If Flight Exists and Adds New Entry If Exists
                elif self.activate_flights[log_index].flight.id == flight.id:
                    in_db = True
                    self.activate_flights[log_index].createLogEntry(flight)
                    break
            #Not Found in current list, adding new log
            if in_db == False:
                self.activate_flights.append(FlightLog(flight=flight))
        #Remove grounded flights
        self.activate_flights = self.removeGroundedFligts(self.activate_flights)

    #Returns Current Logs
    def getActivateFlights(self):
        return self.activate_flights
    
    def __init__(self):
        self.activate_flights = []
        self.fr_api = FlightRadar24API() #Construct API
        self.query()
        

def saveFlightData(obj):
    obj_path = 'SavedData/FlightData/flightData.pkl'
    with open(obj_path, 'wb') as outp:
        pickle.dump(obj, outp)
        outp.close()
        return obj

def checkIfFlightDataExists():
    obj_path = 'SavedData/FlightData/flightData.pkl'
    if os.path.exists(obj_path):
        print("      *   Flight Data Object Found: Loading...        *")
        with open(obj_path, 'rb') as outp:
            obj = pickle.load(outp)
            outp.close()
            obj.query()
            return obj
    else:
        print("      *   Flight Data Object Not Found: Creating...   *")
        obj = FlightData()
        return saveFlightData(obj)

def forceResetFlightData():
    print("      *   Force Reseting Flight Data                  *")
    obj_path = 'SavedData/FlightData/flightData.pkl'
    obj = FlightData()
    return saveFlightData(obj)

#obj = checkIfFlightDataExists()
#print(obj)