#Kyle R Fogerty

from time import sleep
from FlightBots.FlightCommander import FlightCommander


class BotCommander:
    #Flights in each Zone

    def __init__(self):
        print("")
        print("*** Initializing The General ***")
        print(" ")
        lat = float(input("Enter Latitude: "))
        lon = float(input("Enter Longitude: "))
        distance = float(input("Enter Distance: (km) "))
        self.flight_commander = FlightCommander(location=[lat, lon], distance=distance)
        print("*** The General Initialized ***")


    def step(self):
        self.flight_commander.step()
        sleep(10)
    
    def run(self):
        while True:
            self.step()