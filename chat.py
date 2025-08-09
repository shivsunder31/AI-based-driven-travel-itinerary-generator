import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Function to configure the Google API
def configure_gemini_api():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to generate content using Google Gemini for each prompt
def generate_content(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

def app():
    st.title("🌍 Personalized Travel Itinerary Generator ✈️")

    st.markdown(
        """
        <style>
            .header {
                color: #ff5733;
                font-size: 36px;
                font-weight: bold;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Input form for user preferences
    with st.form(key='travel_preferences'):
        budget = st.text_input("💰 Budget (e.g., Rs. 1000)")
        interests = st.text_input("🎯 Interests (e.g., Historical, Cultural, Scenic, Adventure, Nature)")
        duration = st.number_input("📅 Trip Duration (days)", min_value=1, max_value=30, value=7)
        destination = st.text_input("🌆 Destination (e.g., Odisha, Meghalaya)")

        submit_button = st.form_submit_button(label='Generate Itinerary 🗺️')

    # Store inputs in variables
    if submit_button:
        user_preferences = {
            "Budget": budget,
            "Interests": interests,
            "Duration (days)": duration,
            "Destination": destination
        }

        st.write("### Your Travel Preferences:")
        st.json(user_preferences)

        # Initialize session state if not already done
        if 'step' not in st.session_state:
            st.session_state.step = 0

        if 'response' not in st.session_state:
            st.session_state.response = {}

        # Display buttons based on step
        if st.session_state.step == 0:
            if st.button("Get Popular Places"):
                popular_places_prompt = f"Suggest popular places to visit in {destination} that match the interests of {interests}."
                st.session_state.response['popular_places'] = generate_content(popular_places_prompt)
                st.session_state.step += 1

        elif st.session_state.step == 1:
            st.write("### Popular Places:")
            st.write(st.session_state.response['popular_places'])

            if st.button("Generate Travel Plan"):
                travel_plan_prompt = f"Generate a travel itinerary for {destination} based on a {duration}-day trip focusing on {interests}."
                st.session_state.response['travel_plan'] = generate_content(travel_plan_prompt)
                st.session_state.step += 1

        elif st.session_state.step == 2:
            st.write("### Travel Plan:")
            st.write(st.session_state.response['travel_plan'])

            if st.button("Get Travel Tips"):
                travel_tips_prompt = f"Provide travel tips for a trip to {destination}, including money-saving tips and safety advice."
                st.session_state.response['travel_tips'] = generate_content(travel_tips_prompt)
                st.session_state.step += 1

        elif st.session_state.step == 3:
            st.write("### Travel Tips:")
            st.write(st.session_state.response['travel_tips'])

# Ensure to call the configure function when starting the app
configure_gemini_api()
