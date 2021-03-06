import json
import logging
import sys
import urllib.request
from confidential import OPENWEATHERMAP_URL
from confidential import OPENWEATHERMAP_API_KEY
from documents.countries import COUNTRIES

logging.basicConfig(level= logging.DEBUG, filename="weatherReport.log", format='%(asctime)s - %(levelname)s = %(message)s', filemode='w')
LOGGER = logging.getLogger()

COUNTRIES_NAME = list(COUNTRIES.keys())
COUNTRIES_ALPHA_TWO_CODE = list(COUNTRIES.values())

class WeatherData:
    def __init__(self, city, windSpeed, temperature, latitude, longitude, humidex, country, mainWeatherDescription):
        LOGGER.debug("Creating one instance of class WeatherData with following attributes:")
        LOGGER.debug(f"(City = {city}, Wind speed = {windSpeed}, Temperature = {temperature}, Latitude = {latitude}, Longitude = {longitude}, Humidex = {humidex})")
        self.city = city
        self.windSpeed = windSpeed
        self.temperature = temperature
        self.latitude = latitude
        self.longitude = longitude
        self.humidex = humidex
        self.country = country
        self.mainWeatherDescription = mainWeatherDescription

def log_results_of(weatherData):
    LOGGER.debug(f"weatherReport.py : log_results_of({weatherData})")
    LOGGER.info(f"City: {weatherData.city}")
    LOGGER.info(f"Country: {weatherData.country}")
    LOGGER.info(f"Longitude: {weatherData.longitude}")
    LOGGER.info(f"Latitude: {weatherData.latitude}")
    LOGGER.info(f"Temperature: {weatherData.temperature} degrees Celcius.")
    LOGGER.info(f"Humidex: {weatherData.humidex}")
    LOGGER.info(f"Wind speed: {weatherData.windSpeed} km/h")
    LOGGER.info(f"Description: {weatherData.mainWeatherDescription}")

def request_weather_report(url):
    return urllib.request.urlopen(url)

def generate_json_for_parsing(response):
    json_data = response.read()
    LOGGER.debug(json_data)
    return json.loads(json_data)

def display_weather_report(weatherData):
    LOGGER.debug(f"weatherReport.py : display_weather_report({weatherData})")
    log_results_of(weatherData)
    print(f"City: {weatherData.city}")
    print(f"Country: {weatherData.country}")
    print(f"Longitude: {weatherData.longitude}")
    print(f"Latitude: {weatherData.latitude}")
    print(f"Temperature: {weatherData.temperature} degrees Celcius.")
    print(f"Humidex: {weatherData.humidex}")
    print(f"Wind speed: {weatherData.windSpeed} km/h")
    print(f"Description: {weatherData.mainWeatherDescription}")

def get_current_weather_in(city):
    LOGGER.info(f"weatherReport.py : get_current_weather_in({city})")
    LOGGER.debug(f"  HTTP request to: {OPENWEATHERMAP_URL}q={city}&units=metric{OPENWEATHERMAP_API_KEY}")
    response = request_weather_report(OPENWEATHERMAP_URL + str("q=" + city + "&units=metric") + OPENWEATHERMAP_API_KEY)
    if response.getcode() == 200:
        LOGGER.debug(f"  {[response.getcode()]} HTTP request successful")
        json_result = generate_json_for_parsing(response)
        city = json_result["name"]
        longitude = json_result["coord"]["lon"]
        latitude = json_result["coord"]["lat"]
        temperature = json_result["main"]["temp"]
        humidity_index = json_result["main"]["humidity"]
        wind_speed = json_result["wind"]["speed"]
        country_json = json_result["sys"]["country"]
        country_full_name = COUNTRIES_NAME[COUNTRIES_ALPHA_TWO_CODE.index(country_json)]
        mainWeatherDescription = json_result["weather"][0]["main"]
        weatherData = WeatherData(city, wind_speed, temperature, latitude, longitude, humidity_index, country_full_name, mainWeatherDescription)
        display_weather_report(weatherData)
    else:
        LOGGER.error(f"Problem with the server of openweathermap.org. Response code has the value of {response.getcode()}.")

def main():
    LOGGER.debug("WeatherReport.py : main()")
    if len(sys.argv) == 2:
        city = sys.argv[1]
        LOGGER.info(f"Analyzing city named {city}.")
        if city.count(" ") != 0:
            city = city.replace(" ", "%20")
        get_current_weather_in(city)
    else:
        LOGGER.error("Wrong number of arguments at the command line.")

if __name__ == "__main__":
    main()