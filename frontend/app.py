import streamlit as st
import pickle
import pandas as pd

# Load data and similarity matrix
movies = pd.read_csv('dataset/top10K-TMDB-movies.csv')
similarity = pickle.load(open('dataset/similarity.pkl', 'rb'))

# Function to recommend movies
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = similarity[index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        return movies.iloc[[i[0] for i in movie_list]]['title'].tolist()
    except IndexError:
        return ["Movie not found in the dataset."]

# Streamlit UI
st.title("Movie Recommender System")
movie_name = st.selectbox("Choose a movie:", movies['title'].values)

if st.button("Recommend"):
    recommendations = recommend(movie_name)
    st.write("Recommended Movies:")
    for rec in recommendations:
        st.write(rec)
