from models.content_based_model import load_model


class ContentBasedRecommender(object):
    """
    Content based recommender.
    Using example:
    recommender = ContentBasedRecommender('<path_to_pickled_model>')
    recommendations = recommender.get_recommends('<genres_str>', '<title_str>')
    """

    def __init__(self, model_file_path: str, *args, **kwargs):
        self.model = load_model(model_file_path)

    def get_recommends(self, genres: str, title: str, *args, **kwargs):
        """
        Make predict by string of genres divided by slash and title.
        Example: genres=Action|Comedy|Crime|Drama|Thriller", title='Money Train (1995)'
        """
        return self.model.get_recommends(genres=genres, title=title)
