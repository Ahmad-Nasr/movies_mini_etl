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
