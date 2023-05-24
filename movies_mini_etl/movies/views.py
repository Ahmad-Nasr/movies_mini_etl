from django.views.generic import ListView

from movies_mini_etl.movies.models import Movie, Director, Actor, Genre, MovieActors, MovieGenres


class MovieListView(ListView):
    model = Movie
    context_object_name = 'movies'
    template_name = 'movies/movie_table.html'


class DirectorListView(ListView):
    model = Director
    context_object_name = 'directors'
    template_name = 'movies/director_table.html'


class ActorListView(ListView):
    model = Actor
    context_object_name = 'actors'
    template_name = 'movies/actor_table.html'


class GenresListView(ListView):
    model = Genre
    context_object_name = 'genres'
    template_name = 'movies/genre_table.html'


class MovieActorsListView(ListView):
    model = MovieActors
    context_object_name = 'movies_actors'
    template_name = 'movies/movies_actors_table.html'
