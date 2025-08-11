import streamlit as st
import requests
import folium
from datetime import datetime, timedelta
import pytz
import matplotlib.pyplot as plt
from streamlit_folium import folium_static

API_KEY = "0191241afe2bcfeb9b49134dbbc2976c"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

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
        'weather_location_time': '🕒 Weather location time: ',
        'your_local_time': '🕰️ Your local time: ',
        'error': 'Could not retrieve weather data. Please check the city name.',
        'unit_choice': 'Choose temperature unit:',
        'highs': 'Highs',
        'lows': 'Lows',
        'forecast': 'Weather Forecast (next 3 days)',
        'share': 'Share on Twitter',
    },
    'fr': {
        'title': '☁️ Application de vérification météo',
        'enter_city': 'Entrez un nom de ville',
        'weather_in': 'Météo à',
        'temperature': '🌡️ Température : {}°C',
        'conditions': '🌥️ Conditions : {}',
        'humidity': '💧 Humidité : {}%',
        'wind': '💨 Vent : {} m/s',
        'weather_location_time': '🕒 Heure locale de la météo : ',
        'your_local_time': '🕰️ Votre heure locale : ',
        'error': 'Impossible de récupérer les données météo. Veuillez vérifier le nom de la ville.',
        'unit_choice': 'Choisissez l\'unité de température :',
        'highs': 'Températures maximales',
        'lows': 'Températures minimales',
        'forecast': 'Prévisions météo (3 prochains jours)',
        'share': 'Partager sur Twitter',
    },
    'he': {
        'title': '☁️ אפליקציית בדיקת מזג האוויר',
        'enter_city': 'הזן שם עיר',
        'weather_in': 'מזג האוויר ב',
        'temperature': '🌡️ טמפרטורה: {}°C',
        'conditions': '🌥️ תנאים: {}',
        'humidity': '💧 לחות: {}%',
        'wind': '💨 רוח: {} מ/ש',
        'weather_location_time': '🕒 שעה מקומית לאזור מזג האוויר: ',
        'your_local_time': '🕰️ השעה המקומית שלך: ',
        'error': 'לא ניתן להשיג נתוני מזג אוויר. אנא בדוק את שם העיר.',
        'unit_choice': 'בחר יחידת טמפרטורה:',
        'highs': 'חום',
        'lows': 'קור',
        'forecast': 'תחזית מזג האוויר (3 ימים)',
        'share': 'שתף בטוויטר',
    },
    'ar': {
        'title': '☁️ تطبيق التحقق من الطقس',
        'enter_city': 'أدخل اسم المدينة',
        'weather_in': 'الطقس في',
        'temperature': '🌡️ درجة الحرارة: {}°C',
        'conditions': '🌥️ الظروف: {}',
        'humidity': '💧 الرطوبة: {}%',
        'wind': '💨 الرياح: {} م/ث',
        'weather_location_time': '🕒 الوقت المحلي لموقع الطقس: ',
        'your_local_time': '🕰️ وقتك المحلي: ',
        'error': 'تعذر الحصول على بيانات الطقس. يرجى التحقق من اسم المدينة.',
        'unit_choice': 'اختر وحدة درجة الحرارة:',
        'highs': 'العليا',
        'lows': 'الدنيا',
        'forecast': 'توقعات الطقس (3 أيام)',
        'share': 'مشاركة على تويتر',
    }
}


# Function to get weather data
def get_weather(city, lang, unit_param):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": unit_param,  # Units choice (metric or imperial)
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


# Function to get 3-day forecast data
def get_forecast(city, lang, unit_param):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": unit_param,
        "lang": lang
    }
    response = requests.get(FORECAST_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["list"][:3]  # Getting forecast for the next 3 days
    else:
        return None


# Function to apply a dynamic background based on weather condition
def set_background(weather_condition):
    if 'clear' in weather_condition.lower():
        st.markdown(
            """
            <style>
            .stApp {
                background-image: url('https://images.unsplash.com/photo-1556742033-cbd6c5b2c5f4');  /* Sunny Beach */
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    elif 'rain' in weather_condition.lower():
        st.markdown(
            """
            <style>
            .stApp {
                background-image: url('https://images.unsplash.com/photo-1484642281401-45f249e63f24');  /* Rainy Day */
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #f0f8ff;  /* Light sky blue for default */
                background-size: cover;
                background-position: center;
            }
            </style>
            """,
            unsafe_allow_html=True
        )


# Streamlit app
language = st.selectbox("Choose your language", ["en", "fr", "he", "ar"])  # Languages selection

# Get the translations based on selected language
ui_text = translations[language]

# Apply CSS for RTL languages (Hebrew and Arabic)
if language in ['he', 'ar']:
    st.markdown(
        """
        <style>
        .css-1d391kg { text-align: right; direction: rtl; }
        .stButton button { direction: rtl; }
        .stTextInput input { direction: rtl; }
        .stMarkdown p { direction: rtl; }
        .stImage img { direction: rtl; }
        </style>
        """,
        unsafe_allow_html=True
    )

# Display the title based on selected language
st.title(ui_text['title'])

# Choose the temperature unit
unit = st.radio(ui_text['unit_choice'], ('Celsius', 'Fahrenheit'))
unit_param = "metric" if unit == "Celsius" else "imperial"

# Get city input
city = st.text_input(ui_text['enter_city'])

if city:
    weather = get_weather(city, language, unit_param)  # Pass selected language to API
    if weather:
        set_background(weather['description'])  # Set background dynamically
        st.subheader(f"{ui_text['weather_in']} {city.title()}")
        st.write(ui_text['temperature'].format(weather['temp']))
        st.write(ui_text['conditions'].format(weather['description'].capitalize()))
        st.write(ui_text['humidity'].format(weather['humidity']))
        st.write(ui_text['wind'].format(weather['wind']))

        # Display weather icon
        icon_url = f"http://openweathermap.org/img/wn/{weather['icon']}@2x.png"
        st.image(icon_url)

        # Display forecast for the next 3 days
        forecast_data = get_forecast(city, language, unit_param)
        if forecast_data:
            st.subheader(ui_text['forecast'])
            days = ['Day 1', 'Day 2', 'Day 3']
            highs = [f"{day['main']['temp_max']}°C" for day in forecast_data]
            lows = [f"{day['main']['temp_min']}°C" for day in forecast_data]

            for i, day in enumerate(days):
                st.write(f"{day} - Max: {highs[i]} | Min: {lows[i]}")

        # Function to get the local time based on timezone offset
        def get_local_time(timezone_offset):
            utc_time = datetime.utcnow()
            local_time = utc_time + timedelta(seconds=timezone_offset)
            return local_time.strftime("%A, %B %d, %Y %H:%M")

        # Function to get the user's local time using pytz
        def get_user_local_time():
            user_timezone = pytz.timezone("Asia/Jerusalem")
            local_time = datetime.now(user_timezone)
            return local_time.strftime("%A, %B %d, %Y %H:%M")

        # Display local time for the city
        st.write(f"{ui_text['weather_location_time']} {get_local_time(weather['timezone'])}")

        # Display user's local time
        st.write(f"{ui_text['your_local_time']} {get_user_local_time()}")

        # Display map for the city location
        display_map(weather['lat'], weather['lon'])

        # Share on Twitter
        tweet_url = f"https://twitter.com/intent/tweet?text=Weather+in+{city}+is+{weather['temp']}°C+{weather['description']}"
        st.markdown(f"[{ui_text['share']}]({tweet_url})")
    else:
        st.error(ui_text['error'])
