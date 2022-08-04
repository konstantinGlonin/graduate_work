import pickle
from uuid import UUID

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
        self.movies = set(pd.read_csv('../../data/movies_new.csv')['id'].values)
        self.dataset = pd.read_csv('../../data/ratings_new.csv')
        self.dataset = self.dataset.rename({'user_id': 'uid', 'film_work_id': 'iid'}, axis=1)[['uid', 'iid', 'rating']]

        min_rating = self.dataset.rating.min()
        max_rating = self.dataset.rating.max()
        self.reader = Reader(rating_scale=(min_rating, max_rating))

    def fit(self, test_size: float = .15, knn_name: str = 'pearson_baseline', user_based: bool = True):
        data = Dataset.load_from_df(self.dataset, self.reader)
        trainset, testset = train_test_split(data, test_size=test_size)
        self.algo = KNNWithMeans(k=50, sim_options={'name': knn_name, 'user_based': user_based})
        self.algo.fit(trainset)
        test_pred = self.algo.test(testset)
        return accuracy.rmse(test_pred, verbose=True)

    def __make_recommends(self, user_id: UUID):
        rates = dict()
        for item_id in self.movies:
            prediction = self.algo.predict(uid=str(user_id), iid=item_id)
            rates[item_id] = prediction.est
        sorted_rates = {k: v for k, v in sorted(rates.items(), key=lambda item: item[1], reverse=True)}
        films = [k for k in sorted_rates.keys()]

        return films[:20]

    def get_recommends(self, user_id: UUID):
        """
            Return tuple like (userId, [(itemId, predictedRating), ...]).
        """
        return self.__make_recommends(user_id)


def dump_model(model_file_path: str = 'collaborative_filter.pickle'):
    cfm = CollaborativeFilterModel()
    cfm.fit()
    with open(model_file_path, 'wb') as f:
        pickle.dump(cfm, f)


def load_model(model_file_path: str = 'collaborative_filter.pickle'):
    with open(model_file_path, 'rb') as f:
        return pickle.loads(f.read())


if __name__ == '__main__':
    dump_model('collaborative_filter.pickle')
    print(load_model('collaborative_filter.pickle').get_recommends('f0c3cebe-1032-11ed-84a8-e1444c900301'))
