import streamlit as st
import pickle
import requests


def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=14788497f571d94cd077467a7ba3e0fc&language=en-US')
    data = response.json()
    if 'poster_path' in data:
        return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
    else:
        return 'https://via.placeholder.com/500x750?text=No+Image+Available'  # Placeholder image if no poster


def recommend(movie):
    try:
        movie_index = movies_df[movies_df['original_title'] == movie].index[0]
    except IndexError:
        st.error(f"Movie '{movie}' not found in the dataset.")
        return [], []

    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recom_m = []
    recom_p = []
    for i in movie_list:
        movie_id = movies_df.iloc[i[0]].id
        recom_m.append(movies_df.iloc[i[0]].original_title)
        recom_p.append(fetch_poster(movie_id))
    return recom_m, recom_p


# Loading similarity matrix and movies list
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_df = pickle.load(open('movies.pkl', 'rb'))

st.title('See You at the Movies')

option = st.selectbox(
    "Select a movie to get recommendations:",
    movies_df['original_title'].values
)

if st.button("Reset"):
    st.experimental_rerun()  # This will reset the app

if st.button('Get Recommendations'):
    Recommendations, posters = recommend(option)
    if Recommendations:
        st.write("Here are your recommendations:")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.header(Recommendations[0])
            st.image(posters[0])

        with col2:
            st.header(Recommendations[1])
            st.image(posters[1])

        with col3:
            st.header(Recommendations[2])
            st.image(posters[2])

        with col4:
            st.header(Recommendations[3])
            st.image(posters[3])

        with col5:
            st.header(Recommendations[4])
            st.image(posters[4])

else:
    st.write("You selected:", option)
