import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load your combined CSV (must include 'title' and 'tags' columns)
movies = pd.read_csv("combined_movies.csv")

# Fill NaNs
movies['tags'] = movies['tags'].fillna('')

# Vectorization
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

# Cosine similarity
similarity = cosine_similarity(vectors)

# Save files
pickle.dump(movies, open('movie_list.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))
print("✅ movie_list.pkl and similarity.pkl generated successfully.")
