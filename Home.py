import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

client = genai.Client(api_key="AIzaSyDS69TwiF1H-Pw5OX-qWDHawQhdfdNNskw")


def generate_content(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    if response.candidates:
        return response.candidates[0].content.parts[0].text
    else:
        return "⚠️ No response from model."


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

        # Generate all content at once
        popular_places_prompt = f"Suggest popular places to visit in {destination} that match the interests of {interests}."
        travel_plan_prompt = f"Generate a travel itinerary for {destination} based on a {duration}-day trip focusing on {interests}."
        travel_tips_prompt = f"Provide travel tips for a trip to {destination}, including money-saving tips and safety advice."

        # Generate responses
        popular_places = generate_content(popular_places_prompt)
        travel_plan = generate_content(travel_plan_prompt)
        travel_tips = generate_content(travel_tips_prompt)

        # Display all responses
        st.write("### Popular Places:")
        st.write(popular_places)

        st.write("### Travel Plan:")
        st.write(travel_plan)

        st.write("### Travel Tips:")
        st.write(travel_tips)

# Ensure to call the configure function when starting the app
# configure_gemini_api()
