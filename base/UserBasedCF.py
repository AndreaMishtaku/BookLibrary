import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

class UserBasedCollaborativeFiltering():
    
    def __init__(self, users, books, ratings, k=10, max_rating=10.0):
        self.users = users
        self.users = self.users.reset_index()
        self.users = self.users.drop(columns=['index'])   
        self.books = books
        
        self.ratings = ratings
        self.ratings = self.ratings.reset_index()
        self.ratings = self.ratings.drop(columns=['userId'])
        
        self.k = k
        self.max_rating = max_rating
    
    def normalize(self, dataframe):
        row_sum_ratings = dataframe.sum(axis=1) 
        non_zero_count = dataframe.astype(bool).sum(axis=1)
        dataframe_mean = row_sum_ratings / non_zero_count 
        self.normalized_ratings = dataframe.subtract(dataframe_mean, axis = 0) 

    def create_similarity_matrix(self):       
        A_sparse = csr_matrix(self.ratings)
        similarities = cosine_similarity(A_sparse)   
        similarity_matrix = pd.DataFrame(data = similarities)   
        return similarity_matrix

    def get_neighbors(self, user_id, similarity_matrix):
        user_index = self.users.loc[self.users['id'] == user_id].index.values[0]
        user_similairities = similarity_matrix.iloc[user_index].values
        neighbors_index = np.delete(user_similairities, np.where(user_similairities[user_index] == user_index))
        neighbors_index = neighbors_index.argsort()[-(self.k + 1):][::-1]
        return neighbors_index    

    def score_item(self, user_id, neighbor_rating, neighbor_similarity, ratings):
        user_index = self.users.loc[self.users['id'] == user_id].index.values[0]
        active_user_mean_rating = np.mean(ratings.iloc[user_index, :])
        score = np.dot(neighbor_similarity, neighbor_rating) + active_user_mean_rating
        data = score.reshape(1, len(score))
        columns = neighbor_rating.columns
        return pd.DataFrame(data= data , columns= columns)

    def recommend(self, user_id):
        user_index = self.users.loc[self.users['id'] == user_id].index.values[0]
        user_ratings = self.ratings.iloc[user_index]
        recommendation_columns = []
        
        for i in range(len(user_ratings.index)):
            isbn = user_ratings.index[i]
            rating = user_ratings.values[i]
            if rating == 0.0:
                recommendation_columns.append(isbn)
        self.normalize(self.ratings)  
        similarity_matrix = self.create_similarity_matrix()
        neighbor_index = self.get_neighbors(user_id, similarity_matrix)
        neighbor_rating = self.normalized_ratings.loc[neighbor_index][recommendation_columns]
        neighbor_similarity = similarity_matrix[user_index].loc[neighbor_index]
        recommendation_score = self.score_item(user_id, neighbor_rating, neighbor_similarity, self.ratings)
        recommended_book_ISBNs = recommendation_score.stack().nlargest(self.k)
        recommended_book_ISBNs = [recommended_book_ISBNs.index.values[i][1] for i in range(len(recommended_book_ISBNs))]
        recommended_books = self.books.loc[self.books['ISBN'].isin(recommended_book_ISBNs)]
        return recommended_books