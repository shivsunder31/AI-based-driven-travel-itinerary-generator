import os
import streamlit as st
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Function to get weather data from OpenWeather API
def get_weather_data(city, start_date, end_date, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Unable to fetch weather data. Please check the city name or try again later.")
        return None

def display_weather_forecast(city, start_date, end_date, api_key):
    weather_data = get_weather_data(city, start_date, end_date, api_key)
    
    if weather_data:
        st.write(f"### Weather Forecast for {city} from {start_date} to {end_date}:")
        for forecast in weather_data['list']:
            date = forecast['dt_txt']
            temperature = forecast['main']['temp']
            description = forecast['weather'][0]['description']
            st.write(f"**Date:** {date} | **Temperature:** {temperature}°C | **Description:** {description}")

def app():
    st.title("☀️ Weather Forecast 📅")

    # Input form for weather preferences
    with st.form(key='weather_preferences'):
        city = st.text_input("🌆 Enter City Name (e.g., Bhubaneswar)")
        start_date = st.date_input("📅 Start Date")
        end_date = st.date_input("📅 End Date")
        submit_button = st.form_submit_button(label='Get Weather Forecast 🌤️')

    # Store inputs in variables
    if submit_button:
        api_key = os.getenv("OPENWEATHER_API_KEY")  # Ensure your .env file has this key
        if city and start_date and end_date:
            display_weather_forecast(city, start_date, end_date, api_key)
        else:
            st.error("Please fill in all fields.")

