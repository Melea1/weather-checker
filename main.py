import streamlit as st
import requests
import folium
from datetime import datetime, timedelta
import pytz
from streamlit_folium import folium_static

API_KEY = "0191241afe2bcfeb9b49134dbbc2976c"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Define translations for the UI elements
translations = {
    'en': {
        'title': '☁️ Weather Checker App',
        'enter_city': 'Enter a city name',
        'weather_in': 'Weather in',
        'temperature': '🌡️ Temperature: {}°C',
        'conditions': '🌥️ Conditions: {}',
        'humidity': '💧 Humidity: {}%',
        'wind': '💨 Wind: {} m/s',
        'weather_location_time': '🕒 Weather location time: {}',
        'your_local_time': '🕰️ Your local time: {}',
        'error': 'Could not retrieve weather data. Please check the city name.',
    },
    'fr': {
        'title': '☁️ Application de vérification météo',
        'enter_city': 'Entrez un nom de ville',
        'weather_in': 'Météo à',
        'temperature': '🌡️ Température : {}°C',
        'conditions': '🌥️ Conditions : {}',
        'humidity': '💧 Humidité : {}%',
        'wind': '💨 Vent : {} m/s',
        'weather_location_time': '🕒 Heure locale de la météo : {}',
        'your_local_time': '🕰️ Votre heure locale : {}',
        'error': 'Impossible de récupérer les données météo. Veuillez vérifier le nom de la ville.',
    },
    'he': {
        'title': '☁️ אפליקציית בדיקת מזג האוויר',
        'enter_city': 'הזן שם עיר',
        'weather_in': 'מזג האוויר ב',
        'temperature': '🌡️ טמפרטורה: {}°C',
        'conditions': '🌥️ תנאים: {}',
        'humidity': '💧 לחות: {}%',
        'wind': '💨 רוח: {} מ/ש',
        'weather_location_time': '🕒 שעה מקומית לאזור מזג האוויר: {}',
        'your_local_time': '🕰️ השעה המקומית שלך: {}',
        'error': 'לא ניתן להשיג נתוני מזג אוויר. אנא בדוק את שם העיר.',
    },
    'ar': {
        'title': '☁️ تطبيق التحقق من الطقس',
        'enter_city': 'أدخل اسم المدينة',
        'weather_in': 'الطقس في',
        'temperature': '🌡️ درجة الحرارة: {}°C',
        'conditions': '🌥️ الظروف: {}',
        'humidity': '💧 الرطوبة: {}%',
        'wind': '💨 الرياح: {} م/ث',
        'weather_location_time': '🕒 الوقت المحلي لموقع الطقس: {}',
        'your_local_time': '🕰️ وقتك المحلي: {}',
        'error': 'تعذر الحصول على بيانات الطقس. يرجى التحقق من اسم المدينة.',
    }
}


# Function to get weather data
def get_weather(city, lang):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": lang  # Language selection for weather data
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
language = st.selectbox("Choose your language", ["en", "fr", "he", "ar"])  # Languages selection

# Get the translations based on selected language
ui_text = translations[language]

# Display the title based on selected language
st.title(ui_text['title'])

city = st.text_input(ui_text['enter_city'])

if city:
    weather = get_weather(city, language)  # Pass selected language to API
    if weather:
        st.subheader(f"{ui_text['weather_in']} {city.title()}")
        st.write(ui_text['temperature'].format(weather['temp']))
        st.write(ui_text['conditions'].format(weather['description'].capitalize()))
        st.write(ui_text['humidity'].format(weather['humidity']))
        st.write(ui_text['wind'].format(weather['wind']))

        # Display weather icon
        icon_url = f"http://openweathermap.org/img/wn/{weather['icon']}@2x.png"
        st.image(icon_url)


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


        # Display local time for the city
        st.write(f"{ui_text['weather_location_time']} {get_local_time(weather['timezone'])}")

        # Display user's local time
        st.write(f"{ui_text['your_local_time']} {get_user_local_time()}")

        # Display map for the city location
        display_map(weather['lat'], weather['lon'])
    else:
        st.error(ui_text['error'])
