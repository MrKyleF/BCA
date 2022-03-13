#Kyle R Fogerty
#Flight Log: Contains Past Data of Aircraft

#from Flight_Trackers.MilitaryAndBlocked.LogEntry import LogEntry
#from Flight_Trackers.MilitaryAndBlocked.FlightLogHelper import *
from FlightRadar24.api import FlightRadar24API

class LogEntry:
    def __init__(self, flight):
        self.coordinates = [flight.latitude, flight.longitude]
        self.heading = flight.heading
        self.altitude = flight.altitude
        self.ground_speed = flight.ground_speed
        self.time = flight.time
        self.on_ground = True if flight.on_ground == 1 else False
        self.veritcal_speed = flight.vertical_speed
    
    def getCoordinates(self):
        return str(self.coordinates[0]) + ", " + str(self.coordinates[1])
    
    def getLatitude(self):
        return (self.coordinates[0])
    
    def getLongitude(self):
        return (self.coordinates[1])
    
    def getAltitude(self):
        return str(self.altitude) + " ft"
    
    def getHeading(self):
        return str(self.heading)

##Input: Two Airline Codes
##Output 1: Airline_Name, CallSign, Country_Flag, Comments, Full_Name
##Output 2: None, None, None, None, None
##Dependents: 'Code_Addresses/airline_codes.csv'

#getAircraftName()
##Input: Aircraft_Code, Skip Checking second row
##Ouptut 1: Aircraft_Name
##Output 2: "Raw: (input)"
##Dependents: 'Code_Addresses/aircraft_codes.csv'

#Imports
import csv
from csv import writer
from FlightRadar24.api import FlightRadar24API

def getAirline(iata="N/A", icao="N/A"):
    with open('Database/FlightBots_Data/airline_codes.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csv_reader:
            if (row[0] == iata and row[0] != "N/A" ) or (row[1] == icao and row[1] != "N/A"):
                airline_name = "N/A" if len(row) <= 2 else (row[2] if row[2] != '' else "N/A")                        #Airline Name From Database File
                callsign = "N/A" if len(row) <= 3 else (row[3] if row[3] != '' else "N/A")                            #Call Sign From Database File
                country_flag = "N/A" if len(row) <= 4 else (row[4] if row[4] != '' else "N/A")                        #Country Flag From Databse File
                comments = "N/A" if len(row) <= 5 else (row[5] if row[5] != '' else "N/A")                            #Comments On Airline From Database File
                full_name = str(airline_name + (": " if comments != "N/A" else "")) if airline_name != "N/A" else ""   
                full_name += (comments) if comments != "N/A" else ""                                                  #Constructed Full Name For Airline
                csvfile.close()
                return airline_name, callsign, country_flag, comments, full_name
    csvfile.close()
    return None, None, None, None, None

def writeToAircraftsUpdate(aircraft_code):
    temp_array = [aircraft_code, False]
    found = False
    with open('Database/FlightBots_Data/aircraft_codes_to_update.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csv_reader:
            if row[0] == str(temp_array[0]) and row[1] == str(False):
                found = True
                break
        csvfile.close()
    if found == False:
        with open('Database/FlightBots_Data/aircraft_codes_to_update.csv', 'a') as f_object:
            
            # Pass this file object to csv.writer()
            # and get a writer object
            writer_object = writer(f_object)
        
            # Pass the list as an argument into
            # the writerow()
            writer_object.writerow(temp_array)
        
            #Close the file object
            f_object.close()

def getAircraftName(aircraft_code = "N/A", skip_second_check=False):
    with open('Database/FlightBots_Data/aircraft_codes.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csv_reader:
            # Beed to check row 1 first
            if (row[1] == aircraft_code and row[1] != "N/A" ): # or (row[1] == aircraft_code and row[1] != "N/A"):
                aircraft_name = row[2] if row[2] != '' else "N/A"
                csvfile.close()
                return aircraft_name
        csvfile.close()
    with open('Database/FlightBots_Data/aircraft_codes.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csv_reader:
            # Beed to check row 1 first
            if (row[0] == aircraft_code and row[0] != "N/A" ): # or (row[1] == aircraft_code and row[1] != "N/A"):
                aircraft_name = row[2] if row[2] != '' else "N/A"
                csvfile.close()
                return aircraft_name
        
        csvfile.close()
    #File of missing aircraft codes
    writeToAircraftsUpdate(aircraft_code)
    return "Raw: " + aircraft_code                           #Aircraft Not Found In Database File, Return Input With Raw Prefix

#Flight Log Full Data
class FlightLog:
    #Default Information From Local Database
    def setDefaultInfomation(self):
        self.airline_name, self.callsign, self.country_flag, self.comments, self.full_name = getAirline(iata=self.flight.airline_iata, icao=self.flight.airline_icao)
        self.aircraft_name = getAircraftName(aircraft_code=self.flight.aircraft_code)

    def checkVsLastLog(self, flight):
        if len(self.logs) > 0:
            last_flight = self.logs[-1]
            if last_flight.coordinates == flight.coordinates and last_flight.heading == flight.heading and last_flight.altitude == flight.altitude:
                return False
            else:
                return True
        else:
            return True
    
    #Create Log Entry For Each Query
    def createLogEntry(self, flight):
        temp_log = LogEntry(flight)
        if self.checkVsLastLog(temp_log) == True and temp_log.altitude > 0:
            self.logs.append(temp_log)
            self.cords_lat.append(self.logs[-1].getLatitude())
            self.cords_lon.append(self.logs[-1].getLongitude())
            #Check for Max/Min Lat
            if self.cords_lat[-1] < self.range_lat[0]:
                self.range_lat[0] = self.cords_lat[-1]
            if self.cords_lat[-1] > self.range_lat[1]:
                self.range_lat[1] = self.cords_lat[-1]
            #Check for Max/Min Lon
            if self.cords_lon[-1] < self.range_lon[0]:
                self.range_lon[0] = self.cords_lon[-1]
            if self.cords_lon[-1] > self.range_lon[1]:
                self.range_lon[1] = self.cords_lon[-1]
    
    def resetUpdateFlag(self):
        self.past_flight_log_len = len(self.logs)
    
    def lastLogLengthVsNow(self):
        if self.past_flight_log_len < len(self.logs):
            return True
        else:
            return False
    
    
    def getTweetData(self):
        img_extent = ( self.range_lon[0] - 3, self.range_lon[1] + 3, self.range_lat[0] - 3, self.range_lat[1] + 3 )
        return self.cords_lon, self.cords_lat, img_extent

    def __init__(self, flight):
        self.flight = flight            #Flight Radar Flight Object
        self.logs = []                  #Logs Of This Aircraft from Queries
        self.cords_lat = []
        self.cords_lon = []
        self.range_lat = [10000, -10000]
        self.range_lon = [10000, -10000]
        self.past_flight_log_len = 0
        self.createLogEntry(flight)     #Creates First Logs
        self.setDefaultInfomation()     #Sets All Defualt Information From Local Files
        #Military Aircraft
        self.military_jet = False
        #Blocked Aircraft
        self.blocked_jet = False
        #Billionaire, Celebrity, Russian Oligarch Info
        self.billionaire_jet = False
        self.celebrity_jet = False
        self.ru_oligarch_jet = False
        self.owner = ""
        self.citzenship = ""
        self.industry = ""
    
    def setMilitaryInfo(self):
        self.military_jet = True
    
    def setBlockedInfo(self):
        self.blocked_jet = True

    def setBillionaireInfo(self, name, citizenship, industry):
        self.billionaire_jet = True
        self.owner = name
        self.citzenship = citizenship
        self.industry = industry
    
    def setCelebrityInfo(self, name):
        self.celebrity_jet = True
        self.owner = name
    
    def setRUOligarchInfo(self, name):
        self.ru_oligarch_jet = True
        self.owner = name