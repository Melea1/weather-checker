import requests
from datetime import datetime
import pytz

API_KEY = "0191241afe2bcfeb9b49134dbbc2976c"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "en"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        offset_seconds = data["timezone"]
        location_timezone = pytz.FixedOffset(offset_seconds / 60)

        # Local time (user)
        user_time = datetime.now()
        formatted_user_time = user_time.strftime("%A, %B %d, %Y, %H:%M")

        # City time (based on API's UTC offset)
        city_time = datetime.now(location_timezone)
        formatted_city_time = city_time.strftime("%A, %B %d, %Y, %H:%M")

        print(f"\n📍 Weather in {city.title()}:")
        print(f"🕒 Your local time: {formatted_user_time}")
        print(f"🕒 Local time in {city.title()}: {formatted_city_time}")
        print(f"🌡️ Temperature: {temperature}°C")
        print(f"🌥️ Conditions: {description}")
        print(f"💧 Humidity: {humidity}%")
        print(f"💨 Wind speed: {wind_speed} m/s\n")

    else:
        print("❌ Couldn't retrieve weather data. Please check the city name.")

if __name__ == "__main__":
    city = input("Enter a city name: ")
    get_weather(city)