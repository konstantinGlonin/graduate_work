import os
import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler


def change_string(s):
    return ' '.join(s.replace(' ', '').replace('-', '').split('|'))


class ContentBasedModel(object):
    """
    Content based prediction model for recommendations.
    """
    data_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'data'))

    def __init__(self,
                 neighbors_count: int = 10,
                 jobs_count: int = -1,
                 metric: str = 'euclidean'):
        ratings_path = f'{self.data_dir_path}/ratings.csv'
        movies_path = f'{self.data_dir_path}/movies.csv'
        self.ratings = pd.read_csv(ratings_path)
        movies = pd.read_csv(movies_path)
        mean_ratings = self.ratings.groupby('movieId')['rating'].mean()
        mean_ratings = mean_ratings.to_frame()
        ct = ColumnTransformer([
            ('scaled_mean_rating', StandardScaler(), ['rating'])
        ], remainder='passthrough')
        movies = movies.merge(mean_ratings, left_on='movieId', right_on='movieId')
        self.movies = pd.DataFrame(ct.fit_transform(movies),
                                   columns=['scaled_mean_rating', 'movieId', 'title', 'genres'])
        self.count_vect = CountVectorizer()
        self.tfidf_transformer = TfidfTransformer()
        self.neigh = NearestNeighbors(
            n_neighbors=neighbors_count, n_jobs=jobs_count, metric=metric)

    def fit(self):
        movie_genres = [change_string(g) for g in self.movies.genres.values]
        x_train_counts = self.count_vect.fit_transform(movie_genres)
        x_train_tfidf = self.tfidf_transformer.fit_transform(x_train_counts)
        self.neigh = self.neigh.fit(x_train_tfidf)
        return self

    def get_recommends(self, genres: str):
        """
        Return movieId list of recommended movies by string of genres divided by slash.
        Example: genres="Adventure|Comedy|Fantasy|Crime"
        return: List[int] like [143559, 4467, 4911, 3489, 60074, 109042, 4899]
        """
        test = change_string(genres)
        predict = self.count_vect.transform([test])
        x_tfidf2 = self.tfidf_transformer.transform(predict)
        res = self.neigh.kneighbors(x_tfidf2, return_distance=True)
        return list(self.movies.iloc[res[1][0]].sort_values(
            by=['scaled_mean_rating'], ascending=False)['movieId'].array)


def dump_model(model_path_model: str = 'content_based.pickle'):
    gcbm = ContentBasedModel()
    gcbm = gcbm.fit()
    with open(model_path_model, 'wb') as f:
        pickle.dump(gcbm, f)


def load_model(model_file_path):
    with open(model_file_path, 'rb') as f:
        return pickle.load(f)


def get_recommends(model_file_path, genres):
    return load_model(model_file_path).get_recommends(genres)


if __name__ == '__main__':
    dump_model('content_based.pickle')
    print(get_recommends('content_based.pickle', 'Action|History|Adventure|Fantasy'))
