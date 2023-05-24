import logging
import time

from qwikidata.sparql import return_sparql_query_results

from movies_mini_etl.movies.models import Movie, Director, Actor, Genre

logger = logging.getLogger(__name__)


class WikidataMoviesLoader():
    """
    WikidataMoviesLoader loades movies data from "https://www.wikidata.org/" and store them to database tables. 

    WikidataMoviesLoader uses qwikidata library "https://pypi.org/project/qwikidata/" 
    that wraps communcation to SPARQL query service "https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service". 
    The retunred JSON data is parsed and stored to database tables through Django data models using Django ORM. 
    The loaded movies satisify the following conditions: 1) Has an IMDB ID 2)Produced after 2013.
    """

    @classmethod
    def load_movies(cls, movies_count=5):
        """
        loades movies data from "https://www.wikidata.org/" and store them to database tables. 
        The loaded movies data includes movie's(name, wikidata ID, IMDB ID), driector's(name,  wikidata ID), 
        actor's(name,  wikidata ID,), and genre's name.

        Arguments:
            movies_count: Count of moveis to be loaded and save to database tables.
        """

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
        """
        Parses the passed movie's and director's JSON data, and stores the parsed data to 
        the corresonding database tables through Djange data models.

        Arguments:
            movie_data: The JSON object represnting movie's data (movie wikidara id, imdb ID, movie Label) 
            and director's (director wikidara id, director Label)

        Returns:
            movie: Movie data model object
            movie_wikidata_id: Wikidata moive identifier

        Example of movie_result JSON object parsed in this method:
            {
                'movie': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q245671'},
                'director': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q6274003'},
                'imdbID': {'type': 'literal', 'value': 'tt1376213'},
                'movieLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'The Adventurer: The Curse of the Midas Box'},
                'directorLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'Jonathan Newman'}
            }
        """

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
        """
        For a given movie, with movie_wikidata_id, load all actors of this movie 
        from wikidata.org. Parse the JSON data and actors (name, wikidata_id) to database tables.

        Arguments:
            movie_wikidata_id: The wikidata id for the movie of interest

        Returns:
            actors_list: list of Actor data model objects

        Example of actor_result JSON object parsed in this method:
            {
                'actor': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q17402889'}, 
                'actorLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'Ric Reitz'}
            }
        """

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
        """
        For a given movie, with movie_wikidata_id, load all genres of this movie 
        from wikidata.org. Parse the JSON data and genres names to database tables.  

        Arguments:
            movie_wikidata_id: The wikidata id for the movie of interest.

        Returns:
            genres_list: List of Gerne data model objects.

        Example of actor_result JSON object parsed in this method:
            {
                'genre': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q20442589'}, 
                'genreLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'LGBT-related film'}
            }
        """

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
