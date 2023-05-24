import pytest
from unittest.mock import patch

from movies_mini_etl.movies.utils import WikidataMoviesLoader


class TestWikidataMoviesLoader:

    @pytest.mark.django_db
    def test_load_movie_actors(self):
        """
        Test case for load_movie_actors method of the WikidataMoviesLoader.
        """
        movie_wikidata_id = '1392744'
        mocked_response = {
            "head": {"vars": ["actor", "actorLabel"]},
            "results": {
                "bindings": [
                    {"actor": {"type": "uri", "value": "http://www.wikidata.org/entity/Q38111"},
                     "actorLabel": {"xml:lang": "en", "type": "literal", "value": "Leonardo DiCaprio"}}
                ]
            }
        }

        with patch("movies_mini_etl.movies.utils.return_sparql_query_results") as mocked_return_sparql_query_results:
            mocked_return_sparql_query_results.return_value = mocked_response
            actors_list = WikidataMoviesLoader.load_movie_actors(movie_wikidata_id)

        assert len(actors_list) == 1
        assert actors_list[0].name == "Leonardo DiCaprio"
        assert actors_list[0].wikidata_id == "38111"

    @pytest.mark.django_db
    def test_load_movie_genres(self):
        """
        Test case for load_movie_genres method of the WikidataMoviesLoader.
        """
        movie_wikidata_id = '1392744'
        mocked_response = {"head": {"vars": ["genre", "genreLabel"]},
                           "results": {
                               "bindings": [
                                   {"genre": {
                                       "type": "uri", "value": "http://www.wikidata.org/entity/Q130232"},
                                       "genreLabel": {"xml:lang": "en", "type": "literal", "value": "drama film"}
                                    }]}}

        with patch("movies_mini_etl.movies.utils.return_sparql_query_results") as mocked_return_sparql_query_results:
            mocked_return_sparql_query_results.return_value = mocked_response
            genres_list = WikidataMoviesLoader.load_movie_genres(movie_wikidata_id)

        assert len(genres_list) == 1
        assert genres_list[0].name == "drama film"

    @pytest.mark.django_db
    def test_load_movie(self):
        """
        Test case submit_greeting method of the greetings API client.
        """
        movie_data = {
            "movie": {"type": "uri", "value": "http://www.wikidata.org/entity/Q245671"},
            "director": {"type": "uri", "value": "http://www.wikidata.org/entity/Q6274003"},
            "imdbID": {"type": "literal", "value": "tt1376213"},
            "movieLabel": {"xml:lang": "en", "type": "literal", "value": "The Adventurer: The Curse of the Midas Box"},
            "directorLabel": {"xml:lang": "en", "type": "literal", "value": "Jonathan Newman"}
        }
        movie, movie_wikidata_id = WikidataMoviesLoader.load_movie(movie_data)

        assert movie_wikidata_id == '245671'
        assert movie.title == 'The Adventurer: The Curse of the Midas Box'
        assert movie.imdb_id == 'tt1376213'
        assert movie.director.name == 'Jonathan Newman'
        assert movie.director.wikidata_id == '6274003'
