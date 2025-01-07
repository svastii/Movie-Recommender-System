import streamlit as st
import pickle
import pandas as pd
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Load data and similarity matrix
movies = pd.read_csv('dataset/top10K-TMDB-movies.csv')
similarity = pickle.load(open('dataset/similarity.pkl', 'rb'))

# Fetch OMDB API key from .env file
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

# Function to fetch movie poster from OMDB API
def fetch_poster(movie_title):
    try:
        url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('Poster', "https://via.placeholder.com/500x750?text=No+Image+Available")
        return "https://via.placeholder.com/500x750?text=No+Image+Available"
    except Exception:
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Image"

# Function to recommend movies
def recommend(movie):
    if movie not in movies['title'].values:
        return ["Movie not found in the dataset."], []
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    posters = []
    for i in movie_list:
        title = movies.iloc[i[0]]['title']
        recommended_movies.append(title)
        posters.append(fetch_poster(title))
    return recommended_movies, posters

# Streamlit UI
st.markdown(
    """
    <style>
    .title {
        font-size: 30px;
        font-weight: bold;
        text-align: center;
        color: #ffffff;
    }
    .recommend-button {
        display: block;
        margin: 0 auto;
        background-color: #FF4B4B;
        color: white;
        font-size: 16px;
        font-weight: bold;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
    }
    .movie-title {
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="title">Movie Recommender System</div>', unsafe_allow_html=True)

# Dropdown for movie selection
movie_name = st.selectbox("Select a movie from the dropdown:", movies['title'].values)

# Recommend button
if st.button("Show Recommend", key="recommend_button"):
    recommendations, posters = recommend(movie_name)
    if recommendations[0] == "Movie not found in the dataset.":
        st.error("Movie not found in the dataset. Please try another movie.")
    else:
        st.write("Recommended Movies:")
        cols = st.columns(5)  # Create columns for horizontal layout
        for idx, (title, poster) in enumerate(zip(recommendations, posters)):
            with cols[idx]:
                st.image(poster, use_container_width=True)
                st.markdown(f'<div class="movie-title">{title}</div>', unsafe_allow_html=True)
