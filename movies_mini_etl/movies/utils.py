import logging
import time

from qwikidata.sparql import return_sparql_query_results

from movies_mini_etl.movies.models import Movie, Director, Actor, Genre

logger = logging.getLogger(__name__)


class WikidataMoviesLoader():

    @classmethod
    def load_movies(cls, movies_count=5):

        wikidata_api_calls = 0
        logger.info("loading %s movies ....", movies_count)

        movies_and_director_query_string = f"""
            SELECT DISTINCT ?movie ?movieLabel ?imdbID ?director ?directorLabel WHERE {{
            ?movie wdt:P31 wd:Q11424 .
            ?movie wdt:P577 ?date .
            ?movie wdt:P345 ?imdbID .
            ?movie wdt:P57 ?director .
            FILTER (year(?date) > 2013) .
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
            }}
            LIMIT {movies_count}
            """

        try:
            movies_results = return_sparql_query_results(movies_and_director_query_string)
            wikidata_api_calls += 1
        except Exception as e:
            logger.error("Error occurred in qwikidata: %s", e)

        for movie_result in movies_results["results"]["bindings"]:

            movie, movie_wikidata_id = cls.load_movie(movie_result)

            actors_list = cls.load_movie_actors(movie_wikidata_id)
            wikidata_api_calls += 1
            movie.actors.add(*actors_list)

            genres_list = cls.load_movie_genres(movie_wikidata_id)
            wikidata_api_calls += 1
            movie.genres.add(*genres_list)

            logger.info("Movie Q%s data is saved to the database", movie_wikidata_id)
            # Handling Wikidata Query limits.
            if wikidata_api_calls % 5 == 0:
                time.sleep(5)
        logger.info("Sccessfully loaded %s movies", movies_count)

    @classmethod
    def load_movie(cls, movie_data):

        movie_wikidata_id = movie_data["movie"]["value"].split("/")[-1][1:]
        imdb_id = movie_data["imdbID"]["value"]
        movie_title = movie_data["movieLabel"]["value"]
        director_wikidata_id = movie_data["director"]["value"].split("/")[-1][1:]
        director_name = movie_data["directorLabel"]["value"]

        director, created = Director.objects.update_or_create(wikidata_id=director_wikidata_id, name=director_name)
        movie, created = Movie.objects.update_or_create(
            wikidata_id=movie_wikidata_id, imdb_id=imdb_id, title=movie_title, director=director)

        return movie, movie_wikidata_id

    @classmethod
    def load_movie_actors(cls, movie_wikidata_id):

        movie_QID = "Q"+movie_wikidata_id
        movie_actors_query_string = f"""
        SELECT ?actor ?actorLabel
        WHERE {{
        wd:{movie_QID} wdt:P161 ?actor.
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        """

        try:
            movie_actors_results = return_sparql_query_results(movie_actors_query_string)
        except Exception as e:
            logger.error("Error occurred in qwikidata: %s", e)

        actors_list = []
        for actor_result in movie_actors_results["results"]["bindings"]:
            actor_wikidata_id = actor_result["actor"]["value"].split("/")[-1][1:]
            actor_name = actor_result["actorLabel"]["value"]
            actor, created = Actor.objects.update_or_create(wikidata_id=actor_wikidata_id, name=actor_name)
            actors_list.append(actor)
        return actors_list

    @classmethod
    def load_movie_genres(cls, movie_wikidata_id):

        movie_QID = "Q"+movie_wikidata_id
        movie_genres_query_string = f"""
        SELECT ?genre ?genreLabel
        WHERE {{
        wd:{movie_QID} wdt:P136 ?genre.
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        """

        try:
            movie_genres_results = return_sparql_query_results(movie_genres_query_string)
        except Exception as e:
            logger.error("Error occurred in qwikidata: %s", e)

        genres_list = []
        for genre_result in movie_genres_results["results"]["bindings"]:
            genre_name = genre_result["genreLabel"]["value"]
            genre, created = Genre.objects.update_or_create(name=genre_name)
            genres_list.append(genre)
        return genres_list
