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
        self.transformer = ColumnTransformer(
            [('genres_vectorizer', CountVectorizer(), 'genres'),
             ('title_vectorizer', CountVectorizer(), 'title')],
            remainder='drop', verbose_feature_names_out=False)
        self.tfidf_transformer = TfidfTransformer()
        self.neigh = NearestNeighbors(
            n_neighbors=neighbors_count, n_jobs=jobs_count, metric=metric)

    def fit(self):
        movie_data = pd.DataFrame(
            {'genres': [change_string(g) for g in self.movies.genres.values],
             'title': self.movies.title.values}
        )
        x_train_counts = self.transformer.fit_transform(movie_data)
        x_train_tfidf = self.tfidf_transformer.fit_transform(x_train_counts)
        self.neigh = self.neigh.fit(x_train_tfidf)
        return self

    def get_recommends(self, genres: str, title: str = None):
        """
        Return movieId list of recommended movies by string of genres divided by slash and title.
        Example: genres="Action|Sci-Fi|Thriller", title="Matrix, The (1999)"
        return: List[int] like [143559, 4467, 4911, 3489, 60074, 109042, 4899]
        """
        test = pd.DataFrame(
            {'genres': [change_string(genres)],
             'title': [title]}
        )
        predict = self.transformer.transform(test)
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


def get_recommends(model_file_path, genres, title):
    return load_model(model_file_path).get_recommends(genres, title)


if __name__ == '__main__':
    dump_model('content_based.pickle')
    print(get_recommends('content_based.pickle', 'Action|Comedy|Crime|Drama|Thriller', 'Money Train (1995)'))
