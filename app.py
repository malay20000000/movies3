import pickle
import streamlit as st
import requests

# Function to fetch movie poster from TMDB
def fetch_poster(movie_id):
    try:
        # Request movie data from TMDB API
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        data = requests.get(url)
        data.raise_for_status()  # Raise exception for HTTP errors
        data = data.json()

        # Get the poster path
        poster_path = data.get('poster_path')
        if not poster_path:  # If no poster, return a default image
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
        
        # Construct full URL for poster
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"

# Function to recommend movies based on the selected movie
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:  # Get top 5 similar movies (excluding the selected movie itself)
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


# Streamlit interface
st.header('Movie Recommender System')

# Load movie list and similarity matrix from pickle files
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

# Dropdown for movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Display recommendations when button is clicked
if st.button('Show Recommendation'):
    if selected_movie not in movie_list:
        st.warning("Selected movie not found in the dataset.")
    else:
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

        # Display recommendations in columns
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0])
        with col2:
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1])
        with col3:
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2])
        with col4:
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3])
        with col5:
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4])
