import streamlit as st
import requests
import folium
from datetime import datetime, timedelta
import pytz
from streamlit_folium import folium_static

API_KEY = "0191241afe2bcfeb9b49134dbbc2976c"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


# Function to get weather data
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
        return {
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"],
            "timezone": data["timezone"],
            "lat": data["coord"]["lat"],
            "lon": data["coord"]["lon"],
            "icon": data["weather"][0]["icon"]
        }
    else:
        return None


# Function to display the map with Folium
def display_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=10)
    folium.Marker([lat, lon], popup="Requested Location").add_to(m)
    folium_static(m)


# Streamlit app
st.title("☁️ Weather Checker App")

city = st.text_input("Enter a city name")

if city:
    weather = get_weather(city)
    if weather:
        st.subheader(f"Weather in {city.title()}")
        st.write(f"🌡️ Temperature: {weather['temp']}°C")
        st.write(f"🌥️ Conditions: {weather['description'].capitalize()}")
        st.write(f"💧 Humidity: {weather['humidity']}%")
        st.write(f"💨 Wind: {weather['wind']} m/s")

        # Display weather icon
        icon_url = f"http://openweathermap.org/img/wn/{weather['icon']}@2x.png"
        st.image(icon_url)

        # Language selection by user
        language = st.selectbox(
            "Choose your language",
            ["en", "fr", "es", "de", "it", "ru", "pt", "ja", "zh", "ar"]  # List of supported languages
        )

        # Function to get the local time based on timezone offset
        def get_local_time(timezone_offset):
            utc_time = datetime.utcnow()
            local_time = utc_time + timedelta(seconds=timezone_offset)
            return local_time.strftime("%A, %B %d, %Y, %H:%M")

        # Function to get the user's local time using pytz
        def get_user_local_time():
            # Using pytz to get the user's local timezone
            user_timezone = pytz.timezone("Asia/Jerusalem")  # Change this to user's timezone if needed
            local_time = datetime.now(user_timezone)
            return local_time.strftime("%A, %B %d, %Y, %H:%M")
        # Display local time
        st.write(f"🕒 Local time: {get_local_time(weather['timezone'])}")
        # Display user's local time
        st.write(f"🕰️ Your local time: {get_user_local_time()}")
        # Display map
        display_map(weather['lat'], weather['lon'])
    else:
        st.error("Could not retrieve weather data. Please check the city name.")
