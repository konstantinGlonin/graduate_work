import sys
import getopt

from typing import List
from uuid import UUID
from models.collaborative_filter_model import load_model as load_collaborative_filter_model


class CollaborativeFilterRecommender(object):
    """
    Collaborative filter recommender.
    """
    def __init__(self, model_file_path: str):
        self.model = load_collaborative_filter_model(model_file_path)

    def get_recommends(self, user_id: UUID, item_ids: List[str]):
        return self.model.get_recommends(user_id=user_id, item_ids=item_ids)


if __name__ == '__main__':
    '''
    Example:
    python collaborative_filter.py --user_id=2 --item_ids=1,2,3,4,8,22,65
    returns:
    (<user_id>, {<movieId>: <predicted_rating>, ...})
    '''
    from models.collaborative_filter_model import CollaborativeFilterModel  # noqa
    opts, args = getopt.getopt(sys.argv[1:], '', ['user_id=', 'item_ids='])
    uid = None
    iids = None
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
