import requests

API_KEY = "0191241afe2bcfeb9b49134dbbc2976c"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "fr"
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        print(f"Météo à {city}:")
        print(f"🌡️ Température : {temperature}°C")
        open - e.gitignore
        print(f"🌥️ Conditions : {description}")
        print(f"💧 Humidité : {humidity}%")
        print(f"💨 Vent : {wind_speed} m/s")
    else:
        print("❌ Impossible d'obtenir la météo. Vérifie le nom de la ville.")

if __name__ == "__main__":
    city = input("Entrez le nom de la ville : ")
    get_weather(city)
