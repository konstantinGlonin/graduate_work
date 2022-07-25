import pickle
from typing import List

import pandas as pd
from surprise import Dataset
from surprise import KNNWithMeans
from surprise import Reader
from surprise import accuracy
from surprise.model_selection import train_test_split


class CollaborativeFilterModel(object):
    """
    Collaborative Filter Model.
    Using example:
    from ml.models.collaborative_filter import load_model
    RecommendModel = load_model()
    recommender = RecommendModel()
    recommends = recommender.get_recommends(user_id='<user_id>', item_ids=<item_ids_list>)
    """
    recommends = None
    algo = None

    def __init__(self):
        self.movies = pd.read_csv('../data/movies.csv')
        self.ratings = pd.read_csv('../data/ratings.csv')
        movies_with_ratings = self.movies.join(
            self.ratings.set_index('movieId'), on='movieId').reset_index(drop=True)
        movies_with_ratings.dropna(inplace=True)
        self.dataset = pd.DataFrame({
            'uid': movies_with_ratings.userId,
            'iid': movies_with_ratings.title,
            'rating': movies_with_ratings.rating
        })
        min_rating = self.ratings.rating.min()
        max_rating = self.ratings.rating.max()
        self.reader = Reader(rating_scale=(min_rating, max_rating))

    def fit(self, test_size: float = .15, knn_name: str = 'pearson_baseline', user_based: bool = True):
        data = Dataset.load_from_df(self.dataset, self.reader)
        trainset, testset = train_test_split(data, test_size=test_size)
        self.algo = KNNWithMeans(k=50, sim_options={'name': knn_name, 'user_based': user_based})
        self.algo.fit(trainset)
        test_pred = self.algo.test(testset)
        return accuracy.rmse(test_pred, verbose=True)

    def __make_recommends(self, user_id: int, item_ids: List):
        rates = dict()
        for item_id in item_ids:
            prediction = self.algo.predict(uid=user_id, iid=item_id)
            rates[item_id] = prediction.est
        return user_id, rates

    def get_recommends(self, user_id: int, item_ids: List):
        return self.__make_recommends(user_id, item_ids)


def dump_model():
    cfm = CollaborativeFilterModel()
    cfm.fit()
    with open('collaborative_filter.pickle', 'wb') as f:
        pickle.dump(cfm, f)


def load_model():
    with open('collaborative_filter.pickle', 'rb') as f:
        return pickle.loads(f.read())


if __name__ == '__main__':
    dump_model()
