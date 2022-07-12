from fastapi import Depends

from api.v1.params.filters import film_filter_params, person_filter_parameter, genre_filter_parameter
from api.v1.params.page import page_params
from api.v1.params.sort import sort_params
from models.mixin import IndexType
from models.params import ParamsGrp, BaseParamsGrp, Filters, Page, Sort


def film_params(
        filters: Filters = Depends(film_filter_params),
        sort: Sort = Depends(sort_params),
        page: Page = Depends(page_params)
):
    return ParamsGrp(
        index=IndexType.MOVIES,
        filters=filters,
        page=page,
        sort=sort
    )


def genre_params(
        filters: Filters = Depends(genre_filter_parameter),
        sort: Sort = Depends(sort_params),
        page: Page = Depends(page_params)
):
    return ParamsGrp(
        index=IndexType.GENRE,
        filters=filters,
        page=page,
        sort=sort
    )


def person_params(
        filters: Filters = Depends(person_filter_parameter),
        sort: Sort = Depends(sort_params),
        page: Page = Depends(page_params)
):
    return ParamsGrp(
        index=IndexType.PERSON,
        filters=filters,
        page=page,
        sort=sort
    )


def popular_film_params():
    return BaseParamsGrp(
        index=IndexType.MOVIES,
        body={
            "size": 0,
            "aggs": {
                "themes": {
                    "terms": {
                        "field": "theme_md5",
                        "size": 20
                    },
                    "aggs": {
                        "top_rated_films": {
                            "top_hits": {
                                "sort": [
                                    {
                                        "imdb_rating": {
                                            "order": "desc"
                                        }
                                    }
                                ],
                                "_source": {
                                    "includes": [
                                        "theme_md5",
                                        "id",
                                        "title",
                                        "imdb_rating"
                                    ]
                                },
                                "size": 1
                            }
                        }
                    }
                }
            }
        }
    )
