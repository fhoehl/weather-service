#valuei -*- coding: utf-8 -*-

""" Tests """

import json
from datetime import datetime
from collections import namedtuple

import weather
from weather.records import kelvin_to_celsius

Record = namedtuple('Record', ['timestamp', 'weather', 'temperature',
                               'pressure', 'humidity'])

class TestCore(object):
    """Tests for the app's routes."""

    @classmethod
    def setup_class(cls):
        """Load test data from a json file."""

        cls.app = weather.app.test_client()
        with open('weather/tests/test_forecast_data.json', 'r') as test_data_file:
            cls.test_data = json.load(test_data_file)

    def get_first_data_point(self):
        """Returns the first record from the test data. Fields are formatted."""

        data_point = self.test_data['list'][0]
        timestamp = datetime.utcfromtimestamp(data_point['dt'])

        description = data_point['weather'][0]['description']

        # Temperature is in Celsius by default, rounded and postfixed with C
        temperature = '%iC' % kelvin_to_celsius(float(data_point['main']['temp']))

        # Humidity is postfixed with %
        humidity = '%i%%' % data_point['main']['humidity']

        pressure = data_point['main']['pressure']

        return Record(
            timestamp=timestamp,
            weather=description,
            temperature=temperature,
            pressure=pressure,
            humidity=humidity)

    def test_index(self):
        """Index"""

        response = self.app.get('/')
        doc = json.loads(response.data)
        assert doc['message'] == 'Hello World!'

    def test_get_city_data(self):
        """Test getting all the data from a record."""

        data_point = self.get_first_data_point()

        url = 'weather/london/{0}/{1}'.format(
            data_point.timestamp.strftime('%Y%m%d'),
            data_point.timestamp.strftime('%H%M'))

        response = self.app.get(url)

        doc = json.loads(response.data)

        assert doc

        assert doc['weather'] == data_point.weather

        # Temperature is in Celsius by default, rounded and postfixed with C
        assert doc['temperature'] == data_point.temperature

        # Humidity is postfixed with %
        assert doc['humidity'] == data_point.humidity

        assert doc['pressure'] == data_point.pressure

    def test_get_city_data_field(self):
        """Test getting every data field from a record."""

        data_point = self.get_first_data_point()
        data_fields = ('weather', 'temperature', 'pressure', 'humidity')

        for field in data_fields:
            url = 'weather/london/{0}/{1}/{2}'.format(
                data_point.timestamp.strftime('%Y%m%d'),
                data_point.timestamp.strftime('%H%M'),
                field)

            response = self.app.get(url)

            doc = json.loads(response.data)

            assert doc
            assert doc[field] == getattr(data_point, field)

    def test_inexisting_route(self):
        """When the requested route does not exist we should receive an error."""

        response = self.app.get('/bacon')
        assert response.status_code == 404

    def test_no_data_error(self):
        """When there is no data we should receive an error."""

        response = self.app.get('weather/london/17670812/0900')
        doc = json.loads(response.data)

        assert doc
        assert doc['status'] == 'error'
        assert doc['message'] == 'No data for 1767-08-12 09:00'

        response = self.app.get('weather/london/17670812/0900/humidity')
        doc = json.loads(response.data)

        assert doc
        assert doc['status'] == 'error'
        assert doc['message'] == 'No data for 1767-08-12 09:00'

