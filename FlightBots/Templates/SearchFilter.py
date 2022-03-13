#Kyle R Fogerty
import csv
from enum import Enum

class SearchType(Enum):
    military = 0
    blocked = 1
    billionaire = 2
    celebrity = 3

class SearchFilter:
    #Check Single Flight Log For Military Attributes
    def checkSingleMilitaryFlightLog(self, flight_log):
        if flight_log.comments != None and flight_log.airline_name != None and flight_log.lastLogLengthVsNow() == True:             #Check For none fields
            lowercase_comments = flight_log.comments.lower()
            lowercase_airline_name = flight_log.airline_name.lower()
            keywords = ["force", "army","navy","unit ","squadron","special","military"]     #Keywords used to located miltary aircraft
            for keyword in range(0, len(keywords)):
                if keywords[keyword] in lowercase_comments or keywords[keyword] in lowercase_airline_name:
                    flight_log.setMilitaryInfo()
                    return flight_log                                                       #Returns with true
        return flight_log                                                                    
    
    #Check Single Flight Log for Blocked Attributes
    def checkSingleFlightLogBlocked(self, flight_log):
        if flight_log.lastLogLengthVsNow() == True: #Check if updated
            if "blocked" in flight_log.flight.aircraft_code.lower() or "blocked" in flight_log.flight.callsign.lower():
                flight_log.setBlockedInfo()
                return flight_log                                                   #Returns True, in filter
        return flight_log                                                        #Returns False, not in filter    

    
    def checkSingleFlightLogBillionaire(self, flight_log):
        if flight_log.flight.registration != None and flight_log.lastLogLengthVsNow() == True:
            with open('Database/FlightBots_Data/BillionaireJetList.csv', newline='') as csvfile:
                csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in csv_reader:
                    if row[4] == flight_log.flight.registration or row[5] == flight_log.flight.registration  or row[6] == flight_log.flight.registration:
                            flight_log.setBillionaireInfo(row[1], row[2], row[3])
                            csvfile.close()
                            return flight_log
            csvfile.close()
        return flight_log                                                  #Returns False, not in filter
    

    def checkSingleFlightLogCelebrity(self, flight_log):
        if flight_log.flight.registration != None and flight_log.lastLogLengthVsNow() == True:
            with open('Database/FlightBots_Data/CelebJetList.csv', newline='') as csvfile:
                csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in csv_reader:
                    if row[1] == flight_log.flight.registration or row[2] == flight_log.flight.registration  or row[3] == flight_log.flight.registration:
                            flight_log.setCelebrityInfo(row[0])
                            csvfile.close()
                            return flight_log
            csvfile.close()
        return flight_log                                                  #Returns False, not in filter

    def checkAllFlightLogs(self, flight_logs):
        keywords_found = []                                     #Flight Logs Containing Keywords
        for flight in flight_logs:                              
            if self.searchType == SearchType.military:
                new_log = self.checkSingleMilitaryFlightLog(flight)
                if new_log.military_jet == True:
                    keywords_found.append(new_log)  
            elif self.searchType == SearchType.blocked:
                new_log = self.checkSingleFlightLogBlocked(flight)
                if new_log.blocked_jet == True:
                    keywords_found.append(new_log)
            elif self.searchType == SearchType.billionaire:
                new_log = self.checkSingleFlightLogBillionaire(flight)     #Check Each Log for Containing Keywords & Append to found list
                if new_log.billionaire_jet == True:
                    keywords_found.append(new_log)   
            elif self.searchType == SearchType.celebrity:
                new_log = self.checkSingleFlightLogCelebrity(flight)     #Check Each Log for Containing Keywords & Append to found list
                if new_log.celebrity_jet == True:
                    keywords_found.append(new_log)                
        
        return keywords_found                                   #Return List of Flights Containing Keywords
    
    def searchWithFilters(self, logs):
        self.filtered_flights = self.checkAllFlightLogs(logs)
        return False if len(self.filtered_flights) == 0 else True
    
    def setTiming(self, offset, sleep_timer):
        self.sec_between = 120
        self.step_time = int(self.sec_between / sleep_timer)
        self.next_index = self.step_time + offset
    
    def __init__(self, filter_type=0, offset=0, sleep_timer=10):
        self.searchType = SearchType(filter_type)
        self.filtered_flights = []
        self.setTiming(offset=offset, sleep_timer=sleep_timer)
    
    def moveToNextStep(self):
        self.next_index += self.step_time
    
    def tryNextLoop(self):
        self.next_index += 1
    
    def stopLargeNumbers(self, sub):
        self.next_index -= sub


