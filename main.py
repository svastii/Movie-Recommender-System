import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load dataset
df = pd.read_csv('dataset/top10K-TMDB-movies.csv')

# Combine relevant features for recommendations
df['combined_features'] = df['genre'] + ' ' + df['title'] + ' ' + df['overview']
print("\nCombined Features Example:")
print(df['combined_features'].head())

df['genre'] = df['genre'].fillna("")
df['title'] = df['title'].fillna("")
df['overview'] = df['overview'].fillna("")

# Combine relevant features
df['combined_features'] = df['genre'] + ' ' + df['title'] + ' ' + df['overview']

# Check for empty dataset
if df.shape[0] == 0:
    raise ValueError("Dataset is empty. Please check the data.")

# Create the count matrix
cv = CountVectorizer(stop_words='english')
count_matrix = cv.fit_transform(df['combined_features'])


cosine_sim = cosine_similarity(count_matrix)

# Save the similarity matrix
with open('dataset/similarity.pkl', 'wb') as file:
    pickle.dump(cosine_sim, file)

print("Similarity matrix saved successfully!")
