import sys
import getopt

from typing import List
from ..models.collaborative_filter import load_model as load_collaborative_filter_model


class CollaborativeFilterRecommender(object):
    """
    Collaborative filter recommender.
    """
    def __init__(self):
        self.model = load_collaborative_filter_model()

    def get_recommends(self, user_id: str, item_ids: List[str]):
        return self.model.get_recommends(user_id=user_id, item_ids=item_ids)


if __name__ == '__main__':
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
        recommender = CollaborativeFilterRecommender()
        recommends = recommender.get_recommends(user_id=uid, item_ids=iids)
