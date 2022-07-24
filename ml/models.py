from abc import ABC, abstractmethod
import pandas as pd

from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.neighbors import NearestNeighbors
from surprise import KNNWithMeans, KNNBasic
from surprise import Dataset
from surprise import accuracy
from surprise import Reader
from surprise.model_selection import train_test_split
from sqlalchemy import create_engine


def change_string(s):
    return ' '.join(s.replace(' ', '').replace('-', '').split('|'))


class AbstractLoader(ABC):
    """
    Abstract class for ml data loading.
    """
    @abstractmethod
    def load(self, *args, **kwargs) -> pd.DataFrame:
        pass


class CsvLoader(AbstractLoader):
    """
    Csv data loader implementation.
    """
    def load(self, path: str) -> pd.DataFrame:
        return pd.read_csv(path)


class PgLoader(AbstractLoader):
    """
    Postgres data loader implementation.
    """
    def __init__(self, dsn: str):
        self.connection = create_engine(dsn)

    def load(self) -> pd.DataFrame:
        return pd.read_sql_query('select * from "film_work"', con=self.connection)


class AbstractModel(ABC):
    """
    Base class for ML model.
    """
    def __init__(self, loader: AbstractLoader):
        self.loader = loader

    @abstractmethod
    def load_data(self):
        pass


class ContentBasedModel(object):
    """
    Content based prediction model for recommendations.
    """

    def __init__(self,
                 neighbors_count: int = 10,
                 jobs_count: int = -1,
                 metric: str = 'euclidean'):
        self.movies = pd.read_csv('data/movies.csv')
        self.ratings = pd.read_csv('data/ratings.csv')
        self.tags = pd.read_csv('data/tags.csv')
        self.count_vect = CountVectorizer()
        self.tfidf_transformer = TfidfTransformer()
        self.neigh = NearestNeighbors(
            n_neighbors=neighbors_count, n_jobs=jobs_count, metric=metric)

    def train(self):
        movie_genres = [change_string(g) for g in self.movies.genres.values]
        x_train_counts = self.count_vect.fit_transform(movie_genres)
        x_train_tfidf = self.tfidf_transformer.fit_transform(x_train_counts)
        self.neigh.fit(x_train_tfidf)

    def predict(self, genres: str):
        """
        Make predict by string of genres divided by slash.
        Example: genres="Adventure|Comedy|Fantasy|Crime"
        """
        test = change_string(genres)
        predict = self.count_vect.transform([test])
        x_tfidf2 = self.tfidf_transformer.transform(predict)
        res = self.neigh.kneighbors(x_tfidf2, return_distance=True)
        return self.movies.iloc[res[1][0]]


class CollaborativeFilterModel(object):
    """
    Collaborative Filter Model.
    """
    def __init__(self):
        self.movies = pd.read_csv('data/movies.csv')
        self.ratings = pd.read_csv('data/ratings.csv')
        movies_with_ratings = self.movies.join(
            self.ratings.set_index('movieId'), on='movieId').reset_index(drop=True)
        movies_with_ratings.dropna(inplace=True)
