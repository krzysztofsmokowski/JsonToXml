'''
Entire module is written with purpose of working on json data.
In this case its taking json data with information about pollution
taken from API.
'''
import argparse
import xml.etree.cElementTree as ET
from weather_comm import WeatherStations


class XMLcreator(object):
    '''
    This class is taking stations parameter as json data in order to convert data into xml
    format.
    '''
    def __init__(self, stations):
        self.stations = stations
        self.xml_stations = ET.Element('stations')

    def _serialize(self):
        '''
        Method is serializing json from __init__ into xml format
        example input:
        [{'id': 16, 'pm10_pollution': 'Bardzo dobry', 'city': 'Dzierżoniów - Piłsudskiego'},
        {'id': 9153, 'pm25_pollution': 'Bardzo dobry', 'pm10_pollution': 'Bardzo dobry', 'city': 'Jelenia Góra - Ogińskiego'},
        {'id': 67, 'pm10_pollution': 'Dobry', 'city': 'Nowa Ruda - Srebrna'}]
        example output:
        <stations>
            <station id="83" name="chociebuz">
                    <pm10>10</pm10>
                    <pm25>430</pm25>
            </station>
        </stations>
        '''

        for station_dict in self.stations:
            station = ET.SubElement(self.xml_stations, "station", id=str(station_dict['id']), name=station_dict["city"])
            pm10 = ET.SubElement(station, 'pm10')
            if 'pm10_pollution' in station_dict:
                pm10.text = station_dict['pm10_pollution']
            else:
                pm10.text = "Brak Danych"
            pm25 = ET.SubElement(station, 'pm25')
            if 'pm25_pollution' in station_dict:
                pm25.text = station_dict['pm25_pollution']
            else:
                pm25.text = "Brak danych"

    def save(self, filename):
        '''
        Method is saving serialized xml into file specified in parameter.
        Result of method is a xml file in current dir named after filename variable.
        Args: filename (str)
        Returns: None
        '''
        tree = ET.ElementTree(self.xml_stations)
        tree.write(filename)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", action ="store_true", help="specify name of file in which you will save data")
    args = parser.parse_args()
    weather = WeatherStations("http://api.gios.gov.pl/")
    stations_list = weather.stations()
    stations = XMLcreator(stations_list)
    stations._serialize()
    stations.save('eldupa.xml')

if __name__ == '__main__':
    main()
