import pandas as pd
import pickle
import requests

# Load data
movies = pd.read_pickle('movie_list.pkl')
movies_with_overview = pd.read_csv('tmdb_5000_movies.csv')  # the one with the 'overview' column
merged = movies.merge(movies_with_overview[['title', 'overview']], on='title', how='left')

similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_title):
    """Uses TMDB API to fetch the poster URL"""
    api_key = '1742cc31b055abd4e5cd6f95cf0ea4e7'  # Replace this
    response = requests.get(
        f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
    )
    data = response.json()
    if data['results']:
        poster_path = data['results'][0].get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    return "https://via.placeholder.com/300x450?text=No+Image"

def recommend(movie):
    movie = movie.lower()
    movie_index = movies[movies['title'].str.lower() == movie].index
    if movie_index.empty:
        return [], [], [], []

    index = movie_index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    recommended_posters = []
    recommended_summaries = []
    reasons = []

    selected_tags = set(movies.iloc[index].tags.split())

    for i in distances[1:6]:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))

        # Summary
        overview_row = merged[merged['title'] == title]
        if not overview_row.empty and not pd.isna(overview_row.iloc[0]['overview']):
            recommended_summaries.append(overview_row.iloc[0]['overview'])
        else:
            recommended_summaries.append("No summary available.")

        # Tag comparison for reason
        current_tags = set(movies.iloc[i[0]].tags.split())
        common_tags = selected_tags.intersection(current_tags)
        reason = f"Recommended because it shares themes like: {', '.join(list(common_tags)[:5])}"
        reasons.append(reason)

    return recommended_movies, recommended_posters, recommended_summaries, reasons
