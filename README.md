# Weather service 🌧⛅️☀️

You can try it here: `http://178.62.22.6/weather/london/20161125/0300`

# How to run the service?

```bash
python -m weather.run
```

The service will be available at localhost:5000.

# How to run tests?

```bash
python -m weather.test
```

And code coverage?

```bash
python -m weather.test --cov=weather
```

# How to run build, test and run with Docker?

First build the image:

```bash
docker build -t weather-service-image .
```

Tests will be executed during the build.

After building lets run the service 🚀. Make sure to provide an .env file with
the API keys for Open Weather Map.

```bash
cat .env
OPENWEATHERMAP_APIKEY=5bad................
```


```bash
docker run --name weather-service -p 5000:5000 --env-file .env -t weather-service-image
```

# Questions

> If I wanted the temperature in Kelvin rather than celcius, how could I specify this in API calls?

I would allow passing a unit parameter to the endpoints. The parameter would
them be used in the API to make the conversion.

e.g. curl http://<host:ip>/weather/london/20160706/0900?unit=metric
e.g. curl http://<host:ip>/weather/london/20160706/0900?unit=imperial

> How would you test this REST service?

There is some test in the repo. I’m using a static json file to test the
endpoints.

> How would you check the code coverage of your tests?

I’m using pytest so I would use the pytest-cov plugin to do that.

```bash
python -m weather.test --cov=weather
```

> How could the API be documented for third-parties to use?

I don’t really have an opinion on that. I used in the past http://swagger.io
which was quite a good way to define and generate documentation.

> How would you restrict access to this API?

OAuth keys or API keys. Whitelisting of ip or domains. Setup rate limits.

> What would you suggest is needed to do daily forecast recoveries from openweather.org, keeping the web service up to date?

If we were keeping the service up to date for a list of specific cities, I would
probably use task workers schedule with cron. The API is updated every 3 hours -
the workers would be run at the same time. I might use CouchDB as I would be
able to store the JSON doc from the API and have a easy way to find things.

