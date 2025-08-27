import streamlit as st
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load the saved data (vectorizer + dataframe)
def load_model():
    with open("recommendation_model.pkl", "rb") as file:
        model_data = pickle.load(file)
    return model_data["tfidf_vectorizer"], model_data["df_final"]

# Recommendation function
def recommend(tfidf_loaded, df_final_loaded, roomtype, country, city, propertytype):
    filtered_df = df_final_loaded[
        (df_final_loaded['roomtype'] == roomtype) &
        (df_final_loaded['country'] == country) &
        (df_final_loaded['city'] == city) &
        (df_final_loaded['propertytype'] == propertytype)
    ]

    temp = df_final_loaded[
        (df_final_loaded['country'] == country) &
        (df_final_loaded['city'] == city)
    ]

    if temp.empty or filtered_df.empty:
        return []

    idx1 = filtered_df['index'].tolist()
    temp.reset_index(inplace=True)
    idx2 = temp[temp['index'].isin(idx1)].index.tolist()

    # ✅ use transform instead of fit_transform
    vector = tfidf_loaded.transform(temp['tags']).toarray()
    similarity = cosine_similarity(vector)

    hotels = []
    for i in idx2:
        similar_hotels = sorted(list(enumerate(similarity[i])), key=lambda x: x[1], reverse=True)[0:5]
        for hotel in similar_hotels:
            hotels.append(tuple(temp.loc[hotel[0]][['hotelname', 'roomtype']]))
    return hotels


# Streamlit app
def app():
    st.title("🏨 Hotel Recommendation System")

    st.subheader("Find the best hotel for your stay!")
    roomtype = st.text_input("Room Type (e.g., Comfort Single Room)")
    country = st.text_input("Country (e.g., Germany)")
    city = st.text_input("City (e.g., Munich)")
    propertytype = st.text_input("Property Type (e.g., Hotels)")

    if st.button("Get Hotel Recommendation"):
        if roomtype and country and city and propertytype:
            tfidf_loaded, df_final_loaded = load_model()
            recommendations = recommend(tfidf_loaded, df_final_loaded, roomtype, country, city, propertytype)

            if recommendations:
                st.write("### Recommended Hotels:")
                for hotel in recommendations:
                    st.write(f"- {hotel[0]} ({hotel[1]})")
            else:
                st.write("No hotels found for the given criteria.")
        else:
            st.write("Please fill in all fields to get a hotel recommendation.")
