#Kyle R Fogerty
#Flight Commander

from FlightBots.Helpers.FlightData import checkIfFlightDataExists, forceResetFlightData, saveFlightData
from FlightBots.Helpers.Tweet import tweetFlightData
from FlightBots.Templates.SearchFilter import SearchFilter, SearchType


class FlightCommander:
    def loadFlightData(self, resetData):
        if resetData == True:
            self.flightData = forceResetFlightData()
        else:
            self.flightData = checkIfFlightDataExists()
    
    def createFilters(self, exclude=[]):
        self.filters = []
        for i in range(0, len(SearchType)):
            if i not in exclude:
                self.filters.append(SearchFilter(filter_type=i, offset=i))

    def __init__(self, resetData=False, exclude_filters=[]):
        self.current_index = 0
        #print("      *   Flight Data Object Not Found: Creating...   *") ref size
        print("   **     Initalizing Flight Commander                **")
        self.loadFlightData(resetData=resetData)
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
                if self.filters[i].searchWithFilters(self.flightData.getActivateFlights()) == True:
                    #Tweet Data
                    tweeted, response = tweetFlightData(self.filters[i].filtered_flights, self.filters[i].searchType)
                    #Print responses
                    print(self.filters[i].searchType.name.capitalize(), "Responses:")
                    for r in range(0, len(response)):
                        print(str(response[r][1]) + "x " + response[r][0])
                    #Move to Next Step
                    self.filters[i].moveToNextStep()
                else:
                    self.filters[i].tryNextLoop()
        #Save Current Flight Data
        saveFlightData(self.flightData)
        #Move To Next Index
        self.current_index += 1
        #Stop Overflow digits
        self.stopLargeNumbers()

