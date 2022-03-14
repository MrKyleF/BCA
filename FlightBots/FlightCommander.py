#Kyle R Fogerty
#Flight Commander

from FlightBots.Helpers.FlightData import checkIfFlightDataExists, forceResetFlightData, saveFlightData
from FlightBots.Helpers.Tweet import tweetFlightData
from FlightBots.Templates.SearchFilter import SearchFilter, SearchType


class FlightCommander:
    def loadFlightData(self):
        self.flightData = forceResetFlightData()
    
    def createFilters(self, exclude=[1,2,3]):
        self.filters = []
        for i in range(0, len(SearchType)):
            if i not in exclude:
                self.filters.append(SearchFilter(filter_type=i, offset=i))

    def __init__(self, location, distance, resetData=False, exclude_filters=[]):
        self.current_index = 0
        self.location = location
        self.distance = distance
        #print("      *   Flight Data Object Not Found: Creating...   *") ref size
        print("   **     Initalizing Flight Commander                **")
        self.loadFlightData()
        print("      *   Intitalizing Flight Filters                 *")
        self.createFilters(exclude=exclude_filters)
        print("      *   Flight Filters Initialized                  *")
        print("   **     FLight Commander Initialized                **")
    
    def stopLargeNumbers(self, subtractor=1000):
        if self.current_index > subtractor:
            self.current_index -= subtractor
            for i in range(0, len(self.filters)):
                self.filters[i].stopLargeNumbers(subtractor)
    
    def step(self):
        #Get New Data
        self.flightData.query()
        #Check if time for each filter to run
        for i in range(0, len(self.filters)):
            if self.filters[i].next_index == self.current_index:
                #Search with filter
                if self.filters[i].searchWithFilters(self.flightData.getActivateFlights(), self.location, self.distance) == True:
                    #Tweet Data
                    tweetFlightData(self.filters[i].filtered_flights, self.filters[i].searchType)
                    self.filters[i].moveToNextStep()
                else:
                    self.filters[i].tryNextLoop()
        #Save Current Flight Data
        #Move To Next Index
        self.current_index += 1
        #Stop Overflow digits
        self.stopLargeNumbers()

