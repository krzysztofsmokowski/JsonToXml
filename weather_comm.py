'''
Entire module is used for requesting different data from url passed in __init__
of this module.
Main purpose is to close data in json format for further actions.
'''
import json
import requests
from requests.compat import urljoin


class WeatherStations(object):
    '''
    This class is containing modules that are requesting pollution data from weather API.
    '''
    def __init__(self, url):
        self.url = url

    def _ask_api(self, endpoint):
        request = requests.get(urljoin(self.url, endpoint))
        return request.json()

    def station_info(self, station_id):
        '''
        This method communicates with HTTP API and returns json with the result of http get.
        This method is taking only one parameter.
        Input: station_id (int)
        Method returns json with info about station that is requested with use of station_id parameter
        '''
        return self._ask_api("pjp-api/rest/aqindex/getIndex/{}".format(station_id))

    def stations_summary(self, counter=2):
        '''
        Method with no input, communicates with API and returns IDs of every station in form of list.
        Args: none
        Returns: dict of id's (every ID is in INT form) and cities.
        eg:  {14: "WRoclaw", 18: "Poznan"}
        TODO: REMOVE HACK RELATED TO API ANTI SPAM.
        '''
        request_json = self._ask_api("pjp-api/rest/station/findAll")
        station_dict = {}
        count = 0
        for station in request_json:
            if count < counter:
                station_dict[station["id"]] = station["stationName"]
                count += 1
        return station_dict

    def stations(self):
        '''
        Returns: nested structure which contains stations and their paramteres.
        return {id: city, pm10_pollution: pm10, pm25_pollution: pm25}
        ex: [{'id':14, 'city': "wroclaw", "pm10_pollution": 25, "pm25_pollution": 10},
        {18: "poznan", "pm10_pollution": 25, "pm25_pollution": 10}]
        '''
        stations_summary = self.stations_summary()
        list_of_stations = []
        for station_id in stations_summary:
            station_data = {}
            station_data['id'] = station_id
            station_data['city'] = stations_summary[station_id]
            station = self.station_info(station_id)
            if station["pm10IndexLevel"]:
                station_data["pm10_pollution"] = station["pm10IndexLevel"]["indexLevelName"]
            if station["pm25IndexLevel"]:
                station_data["pm25_pollution"] = station["pm25IndexLevel"]["indexLevelName"]
            list_of_stations.append(station_data)
        return list_of_stations
