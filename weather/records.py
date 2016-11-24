# -*- coding: utf-8 -*-

import os
import json
import logging
from datetime import datetime
from calendar import timegm
from collections import OrderedDict

import requests

logging.basicConfig(level=logging.ERROR)
LOGGER = logging.getLogger(__name__)

OPEN_WEATHER_MAP_API_URL = 'http://api.openweathermap.org/data/2.5/forecast'
COUNTRY_CODE = 'uk'
API_KEY = os.getenv('OPENWEATHERMAP_APIKEY', '')

def kelvin_to_celsius(kelvin):
    return int(round(kelvin - 273.15))

def celsius_to_kelvin(celsius):
    return int(round(celsius + 273.15))

class Records(object):
    def __init__(self, offline=False):
        self.data = dict()
        self.offline = offline

        # We load some old data anyway... Useful for tests.
        with open('./weather/tests/test_forecast_data.json', 'r') as data_file:
            data = json.load(data_file)
            records = OrderedDict([(record['dt'], record) for record in data['list']])
            self.data['london'] = records

    def nearest_timestamp(self, timestamp_str):
        """Return the nearest timestamp that fit the data range of the API.
        e.g. 13:17 will be converted in 13:15."""

        timestamp = datetime.utcfromtimestamp(timestamp_str)

        # The API gives us data every 3h, eg: 00:00, 1:00 ... 21:00
        midvalues = [0, 3, 6, 9, 12, 15, 18, 21, 24]

        nearest_timestamp = timestamp.replace(hour=midvalues[timestamp.hour / 3],
                                              minute=0,
                                              second=0,
                                              microsecond=0)

        return timegm(nearest_timestamp.timetuple())

    def find(self, city, timestamp, field=None):
        """Returns a record that match the given parameters. Returns None when
        no data is available."""

        timestamp = self.nearest_timestamp(timestamp)

        if city.lower() in self.data:
            utcnow = datetime.utcnow()
            earliest_record = self.data[city].iterkeys().next()
            delta = utcnow - datetime.utcfromtimestamp(earliest_record)

            # Sync data if we are an hour behind
            if delta.total_seconds() > 3600:
                self.__sync(city)

            if timestamp in self.data[city]:
                record = self.data[city][timestamp]
                return_data = dict(weather=record['weather'][0]['description'],
                                   temperature='%iC' % kelvin_to_celsius(float(record['main']['temp'])),
                                   pressure=record['main']['pressure'],
                                   humidity='%i%%' % record['main']['humidity'])
                if not field:
                    return return_data
                elif field in return_data:
                    return {field: return_data[field]}
        return None

    def __sync(self, city):
        if self.offline:
            return

        payload = dict(q=','.join([city, COUNTRY_CODE]),
                       mode='json',
                       appid=API_KEY)

        try:
            response = requests.get(OPEN_WEATHER_MAP_API_URL, params=payload, timeout=2).json()
            records = {record['dt']: record for record in response['list']}
            self.data[city] = records
        except Exception, exception:
            LOGGER.error('Error accessing the open weather map API.')
            LOGGER.error(exception)

