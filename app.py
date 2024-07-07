import pickle
import streamlit as st
import requests
import numpy as np
import pandas as pd

# Header
st.header('Recommender System')

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))


# Define functions books
def recommend_book(book):
    index = np.where(pt.index == book)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    recommended_book_titles = []
    recommended_book_authors = []
    recommended_book_images = []
    for i in similar_items:
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        recommended_book_titles.append(temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0])
        recommended_book_authors.append(temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0])
        recommended_book_images.append(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values[0])

    return recommended_book_titles, recommended_book_authors, recommended_book_images



#movie

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:7]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

#popular movies

def fetch_popular_movies(page_number, api_key):
    url = 'https://api.themoviedb.org/3/movie/popular'
    params = {
        'api_key': api_key,
        'language': 'en-US',
        'page': page_number
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['results']
    else:
        return None

def fetch_movie_details(movie_id, api_key):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    params = {
        'api_key': api_key,
        'language': 'en-US',
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None



#music
def recommend_music(selected_music_name, music_df, similarity_matrix):
    music_index = music_df[music_df['title'] == selected_music_name].index[0]
    distances = similarity_matrix[music_index]
    music_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_music = []
    for i in music_list:
        recommended_music.append(music_df.iloc[i[0]].title)
    return recommended_music


def load_data():
    music_dict = pickle.load(open('musicrec.pkl', 'rb'))
    music_df = pd.DataFrame(music_dict)

    similarities = pickle.load(open('similarities_music.pkl', 'rb'))

    return music_df, similarities


# CSS styling
st.markdown("""
    <style>
    .movie-title {
        font-family: Arial, sans-serif;
        font-size: 18px;
        text-align: center;
        margin-top: 10px;
    }
    .movie-poster img {
        max-width: 100%;
        height: auto;
    }
    .book-title {
        font-family: Arial, sans-serif;
        font-size: 18px;
        text-align: center;
        margin-top: 10px;
    }
    .book-author {
        font-family: Arial, sans-serif;
        font-size: 16px;
        text-align: center;
        margin-top: 5px;
        color: gray;
    }
     .big-font {
        font-size:50px !important;
    }
    .book-poster img {
        max-width: 100%;
        height: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# Navigation bar
option = st.radio(
    "Navigation",
    ['Home', 'Recommend Movies', 'Recommend Books', 'Recommend Music', 'Popular Movies', 'Popular Books'],
    horizontal=True
)

# Home
if option == 'Home':
    st.subheader('Home')
    st.markdown('<p class="big-font">Welcome to the recommender system!</p>', unsafe_allow_html=True)


# Recommend Movies

elif option == "Recommend Movies":
    st.subheader('Recommend Movies')
    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list
    )

    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

        # Display first row
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image(recommended_movie_posters[0], use_column_width=True)
            st.markdown(f'<p class="movie-title">{recommended_movie_names[0]}</p>', unsafe_allow_html=True)
        with col2:
            st.image(recommended_movie_posters[1], use_column_width=True)
            st.markdown(f'<p class="movie-title">{recommended_movie_names[1]}</p>', unsafe_allow_html=True)
        with col3:
            st.image(recommended_movie_posters[2], use_column_width=True)
            st.markdown(f'<p class="movie-title">{recommended_movie_names[2]}</p>', unsafe_allow_html=True)

        st.write("_____________________________________________________________________")
        st.write("")

        # Display second row
        col4, col5, col6 = st.columns(3)
        with col4:
            st.image(recommended_movie_posters[3], use_column_width=True)
            st.markdown(f'<p class="movie-title">{recommended_movie_names[3]}</p>', unsafe_allow_html=True)
        with col5:
            st.image(recommended_movie_posters[4], use_column_width=True)
            st.markdown(f'<p class="movie-title">{recommended_movie_names[4]}</p>', unsafe_allow_html=True)
        with col6:
            st.image(recommended_movie_posters[5], use_column_width=True)
            st.markdown(f'<p class="movie-title">{recommended_movie_names[5]}</p>', unsafe_allow_html=True)

# Recommend Books

elif option == 'Recommend Books':
    st.subheader('Recommend Books')
    book_list = popular_df['Book-Title'].values
    selected_book = st.selectbox(
        "Type or select a book from the dropdown",
        book_list
    )

    if st.button('Show Recommendation'):
        if selected_book.strip() == '':
            st.warning('Please enter a book title.')
        else:
            recommended_book_titles, recommended_book_authors, recommended_book_images = recommend_book(selected_book)

            # Display first row
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image(recommended_book_images[0], use_column_width=True)
                st.markdown(f'<p class="book-title">{recommended_book_titles[0]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="book-author">{recommended_book_authors[0]}</p>', unsafe_allow_html=True)
            with col2:
                st.image(recommended_book_images[1], use_column_width=True)
                st.markdown(f'<p class="book-title">{recommended_book_titles[1]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="book-author">{recommended_book_authors[1]}</p>', unsafe_allow_html=True)
            with col3:
                st.image(recommended_book_images[2], use_column_width=True)
                st.markdown(f'<p class="book-title">{recommended_book_titles[2]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="book-author">{recommended_book_authors[2]}</p>', unsafe_allow_html=True)

            st.write("_____________________________________________________________________")
            st.write("")

            # Display second row
            col4, col5, col6 = st.columns(3)
            with col4:
                st.image(recommended_book_images[3], use_column_width=True)
                st.markdown(f'<p class="book-title">{recommended_book_titles[3]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="book-author">{recommended_book_authors[3]}</p>', unsafe_allow_html=True)
            with col5:
                st.image(recommended_book_images[4], use_column_width=True)
                st.markdown(f'<p class="book-title">{recommended_book_titles[4]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="book-author">{recommended_book_authors[4]}</p>', unsafe_allow_html=True)


#Recommend Music

elif option == 'Recommend Music':
    music_df, similarities = load_data()
    st.title('Music Recommendation System')
    selected_music_name = st.selectbox('Select the song you like', music_df['title'].values)

    if st.button('Recommend'):
        recommendations = recommend_music(selected_music_name, music_df, similarities)

        st.subheader('Recommended Music:')
        for i, recommendation in enumerate(recommendations):
            st.write(f'{i + 1}. {recommendation}')


# Popular Movies

elif option == 'Popular Movies':
    st.title('Popular Movies')

    # Fetching popular movies
    api_key = '8265bd1679663a7ea12ac168da84d2e8'  # Replace with your actual API key
    movies = []
    for page_number in range(1, 11):  # 10 pages, each page has 20 movies
        movies += fetch_popular_movies(page_number, api_key)

    if movies:
        st.subheader('Top Movies')

        # Number of movies per row
        movies_per_row = 4
        num_movies = len(movies)
        num_rows = (num_movies + movies_per_row - 1) // movies_per_row  # Calculate number of rows needed

        # Display movies in a grid layout
        for row in range(num_rows):
            cols = st.columns(movies_per_row)
            for col_idx in range(movies_per_row):
                movie_idx = row * movies_per_row + col_idx
                if movie_idx < num_movies:
                    movie = movies[movie_idx]
                    movie_details = fetch_movie_details(movie['id'], api_key)
                    if movie_details:
                        imdb_rating = movie_details['vote_average']
                        genres = ", ".join([genre['name'] for genre in movie_details['genres']])
                    else:
                        imdb_rating = "N/A"
                        genres = "N/A"

                    with cols[col_idx]:
                        st.image(f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}", caption=movie['title'])
                        st.write(f"IMDb Rating: {imdb_rating}")
                        st.write(f"Genres: {genres}")


# Popular Books

else:
    st.subheader('Popular Books')
    num_books = len(popular_df)
    num_columns = 4
    num_rows = int(np.ceil(num_books / num_columns))

    for i in range(num_rows):
        cols = st.columns(num_columns)
        for j in range(num_columns):
            index = i * num_columns + j
            if index < num_books:
                with cols[j]:
                    st.image(popular_df.iloc[index]['Image-URL-M'], use_column_width=True)
                    st.markdown(f'<p class="book-title">{popular_df.iloc[index]["Book-Title"]}</p>',
                                unsafe_allow_html=True)
                    st.markdown(f'<p class="book-author">{popular_df.iloc[index]["Book-Author"]}</p>',
                                unsafe_allow_html=True)
                    st.write(f"Rating: {popular_df.iloc[index]['avg_rating']}")
                    st.write(f"Votes: {popular_df.iloc[index]['num_ratings']}")
                    st.write("")

# Footer
st.markdown("""
    <style>
    footer {
        text-align: center;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
st.markdown('<footer></footer>', unsafe_allow_html=True)
