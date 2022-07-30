import sys
import getopt

from typing import List
from models.collaborative_filter_model import load_model as load_collaborative_filter_model


class CollaborativeFilterRecommender(object):
    """
    Collaborative filter recommender.
    """
    def __init__(self, model_file_path: str):
        self.model = load_collaborative_filter_model(model_file_path)

    def get_recommends(self, user_id: str, item_ids: List[str]):
        return self.model.get_recommends(user_id=user_id, item_ids=item_ids)


if __name__ == '__main__':
    '''
    Example:
    python collaborative_filter.py --user_id=2 --item_ids=1,2,3,4,8,22,65
    returns:
    (<user_id>, {<movieId>: <predicted_rating>, ...})
    '''
    # [3771, 1275, 7302, 107723, 71160, 4915, 393, 2373, 1681, 78893]
    # [3771, 1275, 7302, 107723, 71160, 4915, 393, 2373, 1681, 78893]

    from models.collaborative_filter_model import CollaborativeFilterModel  # noqa
    opts, args = getopt.getopt(sys.argv[1:], '', ['user_id=', 'item_ids='])
    uid = 1
    iids = [131724]
    for opt, arg in opts:
        if opt == '--user_id':
            uid = arg
        if opt == '--item_ids':
            iids = arg.split(',')
    if not uid:
        print('Please provide user_id parameter')
    if not iids:
        print('Please provider item_ids parameter')
    if uid and iids:
        recommender = CollaborativeFilterRecommender('models/collaborative_filter.pickle')
        recommends = recommender.get_recommends(user_id=uid, item_ids=iids)
        print(recommends)
