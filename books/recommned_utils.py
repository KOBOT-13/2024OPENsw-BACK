import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# TF-IDF 벡터화 및 유사도 계산
def compute_content_similarity(books):

    tfidf_vectorizer_lesson = TfidfVectorizer()
    tfidf_matrix_lesson = tfidf_vectorizer_lesson.fit_transform(books['lesson'])
    cosine_sim_lesson = cosine_similarity(tfidf_matrix_lesson, tfidf_matrix_lesson)
    genre_matrix = pd.get_dummies(books['genre'])
    cosine_sim_genre = cosine_similarity(genre_matrix, genre_matrix)
    alpha = 0.5  # Adjust weight for genre vs lesson
    combined_similarity = alpha * cosine_sim_lesson + (1 - alpha) * cosine_sim_genre
    return combined_similarity

def weighted_content_similarity(user_titles, user_ratings, books, content_similarity):
    indices = []
    for title in user_titles:
        index = books[books['title'] == title].index
        if not index.empty:
            indices.append(index[0])
    
    weighted_sim_scores = np.zeros(len(books))
    for i, index in enumerate(indices):
        weighted_sim_scores += content_similarity[index] * user_ratings[i]
    
    sim_scores = list(enumerate(weighted_sim_scores))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    book_indices = [i[0] for i in sim_scores if books.iloc[i[0]]['title'] not in user_titles]
    
    top_8_indices = book_indices[:8] # Get top 8 recommendations
    return books.iloc[top_8_indices]

def compute_user_similarity(user_data, books):
    user_ratings = user_data.pivot_table(index='title', columns='user_id', values='rating').fillna(0)
    book_titles = books['title'].tolist()
    ratings_matrix = user_ratings.reindex(book_titles).fillna(0).values
    similarity = np.corrcoef(ratings_matrix)
    return similarity

def weighted_user_similarity(user_titles, user_ratings, user_similarity, books):
    indices = [books[books['title'] == title].index[0] for title in user_titles if title in books['title'].values]
    
    weighted_sim_scores = np.zeros(len(books))
    for i, index in enumerate(indices):
        weighted_sim_scores += user_similarity[index] * user_ratings[i]
    
    sim_scores = list(enumerate(weighted_sim_scores))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    book_indices = [i[0] for i in sim_scores if books.iloc[i[0]]['title'] not in user_titles]
    
    top_8_indices = book_indices[:8]
    return books.iloc[top_8_indices]

# 하이브리드 추천 시스템
def hybrid_recommendation(user_titles, user_ratings, books, content_similarity, user_similarity):
    recommended_books_content = weighted_content_similarity(user_titles, user_ratings, books, content_similarity)
    recommended_books_user = weighted_user_similarity(user_titles, user_ratings, user_similarity, books)
    
    combined_recommendations = pd.concat([recommended_books_content, recommended_books_user]).drop_duplicates()

    top_8_recommendations = combined_recommendations.head(8)
    return top_8_recommendations
