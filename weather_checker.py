import requests

API_KEY = "0191241afe2bcfeb9b49134dbbc2976c"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",   # temperature in Celsius
        "lang": "en"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()

        # Extract weather details
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        # Print the results nicely
        print(f"Weather in {city}:")
        print(f"🌡️ Temperature: {temperature}°C")
        print(f"🌥️ Conditions: {description}")
        print(f"💧 Humidity: {humidity}%")
        print(f"💨 Wind speed: {wind_speed} m/s")
    else:
        print("❌ Couldn't get the weather. Please check the city name.")

# Run this block when the script is executed directly
if __name__ == "__main__":
    city = input("Enter the name of the city: ")
    get_weather(city)
