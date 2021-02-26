import urllib.request
import json
from confidential import OPENWEATHERMAP_URL
from confidential import OPENWEATHERMAP_API_KEY

def get_wind_speed(data):
    return str(data["wind"]["speed"])

def get_temperature(data):
    return str(data["main"]["temp"])

def get_latitude_of_city(data):
    return str(data["coord"]["lat"])

def get_longitude_of_city(data):
    return str(data["coord"]["lon"])

def get_humidity_index(data):
    return str(data["main"]["humidity"])

def request_weather_report(url):
    return urllib.request.urlopen(url)

def generate_json_for_parsing(response):
    json_data = response.read()
    return json.loads(json_data)

def display_weather_report(city, longitude, latitude, temperature, humidity_index, wind_speed):
    print(f"City: {city}")
    print(f"Longitude: {longitude}")
    print(f"Latitude: {latitude}")
    print(f"Temperature: {temperature} degrees Celcius.")
    print(f"Humidex: {humidity_index}")
    print(f"Wind speed: {wind_speed} km/h")

def get_current_weather_in(city):
    response = request_weather_report(OPENWEATHERMAP_URL + str("q=" + city + "&units=metric") + OPENWEATHERMAP_API_KEY)
    if response.getcode() == 200:
        json_result = generate_json_for_parsing(response)
        city = json_result["name"]
        longitude = get_longitude_of_city(json_result)
        latitude = get_latitude_of_city(json_result)
        temperature = get_temperature(json_result)
        humidity_index = get_humidity_index(json_result)
        wind_speed = get_wind_speed(json_result)
        display_weather_report(city, longitude, latitude, temperature, humidity_index, wind_speed)
    else:
        print("Error!")

def main():
    get_current_weather_in("Toronto")

if __name__ == "__main__":
    main()