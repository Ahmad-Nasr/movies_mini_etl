from django.urls import path
from django.views.generic import TemplateView

from .views import (MovieListView, DirectorListView, ActorListView,
                    GenresListView, MovieActorsListView, MovieGenresListView)

app_name = "movies"
urlpatterns = [
    path("", view=MovieListView.as_view(), name="list_movies"),
    path("directors", view=DirectorListView.as_view(), name="list_directors"),
    path("actors", view=ActorListView.as_view(), name="list_actors"),
    path("genres", view=GenresListView.as_view(), name="list_genres"),
    path("movies-actors", view=MovieActorsListView.as_view(), name="list_movies_actors"),
    path("movies-genres", view=MovieGenresListView.as_view(), name="list_movies_genres"),
    path("loader", TemplateView.as_view(template_name="movies/movies_loader.html"), name="movies_loader"),
]
