from ..models.content_based import load_model as load_content_based_model


class ContentBasedRecommender(object):
    """
    Content based recommender.
    """

    def __init__(self, *args, **kwargs):
        self.model = load_content_based_model()

    def get_recommends(self, genres: str, *args, **kwargs):
        """
        Make predict by string of genres divided by slash.
        Example: genres="Adventure|Comedy|Fantasy|Crime"
        """
        return self.model.get_recommends(genres=genres)


if __name__ == '__main__':
    recommender = ContentBasedRecommender()
    recommends = recommender.get_recommends(genres='Action|History|Adventure|Fantasy')
