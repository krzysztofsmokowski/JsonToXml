from weather_comm import WeatherStations
import unittest
from unittest.mock import MagicMock





class WeatherStationsTest(unittest.TestCase):
    def test_stations_summary_without_counter(self):
        weather = WeatherStations('')
        weather._ask_api = MagicMock(return_value=[
            {'id':1, 'stationName':'Wroclaw'},
            {'id':2, 'stationName':'Poznan'}
            ])
        self.assertEqual({1: "Wroclaw", 2: "Poznan"}, weather.stations_summary())

    def test_stations_summary_without_counter_3_items(self):
        weather = WeatherStations('x')
        weather._ask_api = MagicMock(return_value=[
            {'id':1, 'stationName':'Wroclaw'},
            {'id':2, 'stationName':'Poznan'},
            {'id':3, 'stationName':'Horzuf'}
            ])
        summary = weather.stations_summary()
        self.assertEqual({1: "Wroclaw", 2: "Poznan"}, summary)

    def test_stations_summary_with_counter_1(self):
        weather = WeatherStations('')
        weather._ask_api = MagicMock(return_value=[
            {'id':1, 'stationName':'Wroclaw'},
            {'id':2, 'stationName':'Poznan'}
            ])
        summary = weather.stations_summary(counter=1)
        self.assertEqual({1: "Wroclaw"}, summary)

    def test_stations_summary_with_counter_0(self):
        weather = WeatherStations('')
        weather._ask_api = MagicMock(return_value=[
            {'id':1, 'stationName':'Wroclaw'},
            {'id':2, 'stationName':'Poznan'}
            ])
        summary = weather.stations_summary(counter=0)
        self.assertEqual({}, summary)


    def test_stations_one_station(self):
        weather = WeatherStations('')
        weather.stations_summary = MagicMock(return_value={1: "Wroclaw"})
        weather.station_info = MagicMock()
        weather.station_info.side_effect = [{"pm10IndexLevel":{"indexLevelName":1}, "pm25IndexLevel":None}]
        list_of_stations = weather.stations()
        self.assertEqual([{'city': 'Wroclaw', 'id': 1, 'pm10_pollution': 1}], list_of_stations)


    def test_stations_zero_stations(self):
        weather = WeatherStations('')
        weather.stations_summary = MagicMock(return_value={})
        list_of_stations = weather.stations()
        self.assertEqual([], list_of_stations)


    def test_stations_two_stations(self):
        weather = WeatherStations('')
        weather.stations_summary = MagicMock(return_value={1049568: "Wroclaw", 43895:"Poznan"})
        weather.station_info = MagicMock()
        def my_side_effect(station_id):
            if station_id == 1049568:
                return {"pm10IndexLevel":{"indexLevelName":1}, "pm25IndexLevel":None}
            if station_id == 43895:
                return {"pm10IndexLevel":{"indexLevelName":3}, "pm25IndexLevel":None}
        weather.station_info.side_effect = my_side_effect
        list_of_stations = weather.stations()
        self.assertEqual([{'city': 'Wroclaw', 'id': 1049568, 'pm10_pollution': 1}, {'city': 'Poznan', 'id': 43895, 'pm10_pollution': 3}], list_of_stations)






if __name__ == '__main__':
    unittest.main()
