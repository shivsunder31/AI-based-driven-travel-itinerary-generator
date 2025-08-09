import streamlit as st
import pickle
import pandas as pd

# Load the trained ML model
def load_model():
    with open("recommendation_model.pkl", "rb") as file:
        model = pickle.load(file)
    return model

# Function to make predictions based on user input
def predict_hotel(model, roomtype, country, city, propertytype):
    # Create a dataframe with user input
    input_data = pd.DataFrame({
        'RoomType': [roomtype],
        'Country': [country],
        'City': [city],
        'PropertyType': [propertytype]
    })
    
    # Make a prediction using the loaded model
    prediction = model.predict(input_data)
    return prediction[0]

def app():
    st.title("🏨 Hotel Recommendation System")

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

    # Input fields for hotel search
    st.subheader("Find the best hotel for your stay!")
    roomtype = st.selectbox("Room Type", ["Single", "Double", "Suite", "Deluxe"])
    country = st.text_input("Country (e.g., USA)")
    city = st.text_input("City (e.g., New York)")
    propertytype = st.selectbox("Property Type", ["Hotel", "Hostel", "Guest House", "Apartment"])

    # Button to submit and get recommendations
    if st.button("Get Hotel Recommendation"):
        if roomtype and country and city and propertytype:
            model = load_model()  # Load the saved model
            recommendation = predict_hotel(model, roomtype, country, city, propertytype)
            
            st.write(f"### Recommended Hotel: {recommendation}")
        else:
            st.write("Please fill in all fields to get a hotel recommendation.")

# You can add the module to your main.py by calling Hotel.app() in the sidebar options
