
import cartopy.crs as ccrs
import os
import cartopy
import matplotlib.pyplot as plt
import reverse_geocode

from FlightBots.Templates.SearchFilter import SearchType


def getLocation(latitude, longitude):
    coordinates = [(latitude, longitude)]
    location = (reverse_geocode.search(coordinates))
    city = (location[0]['city'])
    country = (location[0]['country'])
    return city + ", " + country + ": "

def addResponse(responses, new_reponse):
    #Check If Empty
    if len(responses) == 0:
        return [[new_reponse, 1]]
    else:
        for i in range(0, len(responses)):
            if responses[i][0] == new_reponse:
                responses[i][1] = responses[i][1] + 1
                return responses
        responses.append([new_reponse, 1])
        return responses

strFile = "SavedData/FlightData/temp_map.jpg"


def tweetMilitaryFlightLogs(logs):
    if len(logs) > 0:
        for flight in logs:
            if len(flight.logs) > 2:
                # create photo
                plt.clf() #Clear buffer
                list_of_longitudes, list_of_latitudes, img_extent = flight.getTweetData()
                last_latitude = list_of_latitudes[-1]
                last_longitude = list_of_longitudes[-1]
                string_status = getLocation(last_latitude, last_longitude)
                string_status += flight.flight.callsign if flight.flight.callsign != None else "Currently Unavailable"
                string_status += " | "
                string_status += flight.full_name if flight.full_name != None else "Currently Unavailable"
                string_status += " | "
                string_status += flight.aircraft_name if flight.aircraft_name != None else "Currently Unavailable"
                string_status += " | "
                string_status += ("Altitude: " + str(flight.logs[-1].getAltitude()))
                string_status += " | "
                string_status += ("Heading: " + str(flight.logs[-1].getHeading()))
                string_status += " | "
                string_status += ("Registration: " + flight.flight.registration)
                string_status += " | "
                string_status += ("Last Coord: " + flight.logs[-1].getCoordinates())
                ax = plt.axes(projection=ccrs.PlateCarree(), extent=img_extent)
                ax.stock_img()
                ax.add_feature(cartopy.feature.LAND)
                ax.add_feature(cartopy.feature.OCEAN)
                ax.add_feature(cartopy.feature.COASTLINE,linewidth=0.3)
                ax.add_feature(cartopy.feature.BORDERS, linestyle=':',linewidth=0.3)
                ax.add_feature(cartopy.feature.LAKES, alpha=0.5)
                ax.add_feature(cartopy.feature.RIVERS)
                plt.plot(list_of_longitudes, list_of_latitudes ,color='red')
                adjustment_lat = -0.5 if list_of_latitudes[0] < list_of_latitudes[1] else 0.5
                plt.text(list_of_longitudes[0], list_of_latitudes[0] + adjustment_lat, 'Start', horizontalalignment='center', transform=ccrs.Geodetic())
                if os.path.exists(strFile):
                    print(string_status)
                    os.remove(strFile)   # Opt.: os.system("rm "+strFile)
                    plt.show()
                    plt.savefig(strFile,bbox_inches='tight')
                    plt.clf() # Clear Buffer
                else:
                    print(string_status)
                    plt.savefig(strFile,bbox_inches='tight')
                    plt.show()
                    plt.clf() # Clear Buffer

    return

def tweetBlockedFlightLogs(logs):
    tweeted = False
    responses = []
    if len(logs) > 0:
        for flight in logs:
            if len(flight.logs) > 2:
                plt.clf() # Clear Buffer
                list_of_longitudes, list_of_latitudes, img_extent = flight.getTweetData()
                last_latitude = list_of_latitudes[-1]
                last_longitude = list_of_longitudes[-1]
                string_status = getLocation(last_latitude, last_longitude) + "Heading: " + str(flight.logs[-1].getHeading()) + " | " + "Altitude: " + str(flight.logs[-1].getAltitude())
                ax = plt.axes(projection=ccrs.PlateCarree(), extent=img_extent)
                ax.stock_img()
                ax.add_feature(cartopy.feature.LAND)
                ax.add_feature(cartopy.feature.OCEAN)
                ax.add_feature(cartopy.feature.COASTLINE,linewidth=0.3)
                ax.add_feature(cartopy.feature.BORDERS, linestyle=':',linewidth=0.3)
                ax.add_feature(cartopy.feature.LAKES, alpha=0.5)
                ax.add_feature(cartopy.feature.RIVERS)
                plt.plot(list_of_longitudes, list_of_latitudes ,color='red')
                adjustment_lat = -0.5 if list_of_latitudes[0] < list_of_latitudes[1] else 0.5
                plt.text(list_of_longitudes[0], list_of_latitudes[0] + adjustment_lat, 'Start', horizontalalignment='center', transform=ccrs.Geodetic())
                if os.path.exists(strFile):
                    os.remove(strFile)   # Opt.: os.system("rm "+strFile)
                    plt.savefig(strFile,bbox_inches='tight')
                    plt.clf() # Clear Buffer
                else:
                    plt.savefig(strFile,bbox_inches='tight')
                    plt.clf() # Clear Buffer
                temp_response = sendTweet(string_status, SearchType.blocked, last_latitude, last_longitude)
                responses = addResponse(responses, temp_response)
                if temp_response == "Sent":
                    tweeted = True
    return tweeted, responses

def tweetBillionaireFlightLogs(logs):
    tweeted = False
    responses = []
    if len(logs) > 0:
        for flight in logs:
            if len(flight.logs) > 2:
                plt.clf() #Clear buffer
                list_of_longitudes, list_of_latitudes, img_extent = flight.getTweetData()
                string_status = flight.owner + " | " + flight.industry + "    "
                last_latitude = list_of_latitudes[-1]
                last_longitude = list_of_longitudes[-1]
                string_status += getLocation(last_latitude, last_longitude)
                string_status += flight.aircraft_name if flight.aircraft_name != None else "Currently Unavailable"
                string_status += " | "
                string_status += ("Altitude: " + str(flight.logs[-1].getAltitude()))
                string_status += " | "
                string_status += ("Heading: " + str(flight.logs[-1].getHeading()))
                string_status += " | "
                string_status += ("Registration: " + flight.flight.registration)
                string_status += " | "
                string_status += ("Last Coord: " + flight.logs[-1].getCoordinates())
                ax = plt.axes(projection=ccrs.PlateCarree(), extent=img_extent)
                ax.stock_img()
                ax.add_feature(cartopy.feature.LAND)
                ax.add_feature(cartopy.feature.OCEAN)
                ax.add_feature(cartopy.feature.COASTLINE,linewidth=0.3)
                ax.add_feature(cartopy.feature.BORDERS, linestyle=':',linewidth=0.3)
                ax.add_feature(cartopy.feature.LAKES, alpha=0.5)
                ax.add_feature(cartopy.feature.RIVERS)
                plt.plot(list_of_longitudes, list_of_latitudes ,color='red')
                adjustment_lat = -0.5 if list_of_latitudes[0] < list_of_latitudes[1] else 0.5
                plt.text(list_of_longitudes[0], list_of_latitudes[0] + adjustment_lat, 'Start', horizontalalignment='center', transform=ccrs.Geodetic())
                if os.path.exists(strFile):
                    os.remove(strFile)   # Opt.: os.system("rm "+strFile)
                    plt.savefig(strFile,bbox_inches='tight')
                    plt.clf() # Clear Buffer
                else:
                    plt.savefig(strFile,bbox_inches='tight')
                    plt.clf() # Clear Buffer
                temp_response = sendTweet(string_status, SearchType.billionaire, last_latitude, last_longitude)
                responses = addResponse(responses, temp_response)
                if temp_response == "Sent":
                    tweeted = True
    return tweeted, responses

def tweetCelebrityFlightLogs(logs):
    tweeted = False
    responses = []
    if len(logs) > 0:
        for flight in logs:
            if len(flight.logs) > 2:
                plt.clf() #Clear buffer
                list_of_longitudes, list_of_latitudes, img_extent = flight.getTweetData()
                string_status = flight.owner + "    "
                last_latitude = list_of_latitudes[-1]
                last_longitude = list_of_longitudes[-1]
                string_status = getLocation(last_latitude, last_longitude)
                string_status += flight.aircraft_name if flight.aircraft_name != None else "Currently Unavailable"
                string_status += " | "
                string_status += ("Altitude: " + str(flight.logs[-1].getAltitude()))
                string_status += " | "
                string_status += ("Heading: " + str(flight.logs[-1].getHeading()))
                string_status += " | "
                string_status += ("Registration: " + flight.flight.registration)
                string_status += " | "
                string_status += ("Last Coord: " + flight.logs[-1].getCoordinates())
                ax = plt.axes(projection=ccrs.PlateCarree(), extent=img_extent)
                ax.stock_img()
                ax.add_feature(cartopy.feature.LAND)
                ax.add_feature(cartopy.feature.OCEAN)
                ax.add_feature(cartopy.feature.COASTLINE,linewidth=0.3)
                ax.add_feature(cartopy.feature.BORDERS, linestyle=':',linewidth=0.3)
                ax.add_feature(cartopy.feature.LAKES, alpha=0.5)
                ax.add_feature(cartopy.feature.RIVERS)
                plt.plot(list_of_longitudes, list_of_latitudes ,color='red')
                adjustment_lat = -0.5 if list_of_latitudes[0] < list_of_latitudes[1] else 0.5
                plt.text(list_of_longitudes[0], list_of_latitudes[0] + adjustment_lat, 'Start', horizontalalignment='center', transform=ccrs.Geodetic())
                if os.path.exists(strFile):
                    os.remove(strFile)   # Opt.: os.system("rm "+strFile)
                    plt.savefig(strFile,bbox_inches='tight')
                    plt.clf() # Clear Buffer
                else:
                    plt.savefig(strFile,bbox_inches='tight')
                    plt.clf() # Clear Buffer
                temp_response = sendTweet(string_status, SearchType.celebrity, last_latitude, last_longitude)
                responses = addResponse(responses, temp_response)
                if temp_response == "Sent":
                    tweeted = True
    return tweeted, responses

def tweetFlightData(logs, searchType):
    if searchType == SearchType.military:
        return tweetMilitaryFlightLogs(logs)
    elif searchType == SearchType.blocked:
        return tweetBlockedFlightLogs(logs)
    elif searchType == SearchType.billionaire:
        return tweetBillionaireFlightLogs(logs)
    elif searchType == SearchType.celebrity:
        return tweetCelebrityFlightLogs(logs)


