from models.content_based_model import load_model


class ContentBasedRecommender(object):
    """
    Content based recommender.
    Using example:
    recommender = ContentBasedRecommender('<path_to_pickled_model>')
    recommendations = recommender.get_recommends('<genres_str>')
    """

    def __init__(self, model_file_path: str, *args, **kwargs):
        self.model = load_model(model_file_path)

    def get_recommends(self, genres: str, *args, **kwargs):
        """
        Make predict by string of genres divided by slash.
        Example: genres="Adventure|Comedy|Fantasy|Crime"
        """
        return self.model.get_recommends(genres=genres)


if __name__ == '__main__':
    from models.content_based_model import ContentBasedModel  # noqa
    cbr = ContentBasedRecommender('models/content_based.pickle')
    print(cbr.get_recommends('Action|History|Adventure|Fantasy'))
