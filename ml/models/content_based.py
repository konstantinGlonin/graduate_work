import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.neighbors import NearestNeighbors


def change_string(s):
    return ' '.join(s.replace(' ', '').replace('-', '').split('|'))


class GenresContentBasedModel(object):
    """
    Content based prediction model for recommendations by genres.
    Using example:
    RecommendModel = load_model()
    recommender = RecommendModel()
    recommends = recommender.get_recommends('<genres_str>')
    """

    def __init__(self,
                 neighbors_count: int = 10,
                 jobs_count: int = -1,
                 metric: str = 'euclidean'):
        self.movies = pd.read_csv('../data/movies.csv')
        self.ratings = pd.read_csv('../data/ratings.csv')
        self.count_vect = CountVectorizer()
        self.tfidf_transformer = TfidfTransformer()
        self.neigh = NearestNeighbors(
            n_neighbors=neighbors_count, n_jobs=jobs_count, metric=metric)

    def fit(self):
        movie_genres = [change_string(g) for g in self.movies.genres.values]
        x_train_counts = self.count_vect.fit_transform(movie_genres)
        x_train_tfidf = self.tfidf_transformer.fit_transform(x_train_counts)
        self.neigh.fit(x_train_tfidf)

    def get_recommends(self, genres: str):
        """
        Return recommendations by string of genres divided by slash.
        Example: genres="Adventure|Comedy|Fantasy|Crime"
        """
        test = change_string(genres)
        predict = self.count_vect.transform([test])
        x_tfidf2 = self.tfidf_transformer.transform(predict)
        res = self.neigh.kneighbors(x_tfidf2, return_distance=True)
        return self.movies.iloc[res[1][0]]


def dump_model():
    gcbm = GenresContentBasedModel()
    gcbm.fit()
    with open('content_based.pickle', 'wb') as f:
        pickle.dump(gcbm, f)


def load_model():
    with open('content_based.pickle', 'rb') as f:
        return pickle.loads(f.read())


if __name__ == '__main__':
    dump_model()
