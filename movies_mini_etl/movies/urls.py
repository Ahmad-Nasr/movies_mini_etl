from django.urls import path

from .views import (MovieListView, DirectorListView, ActorListView, GenresListView)

app_name = "movies"
urlpatterns = [
    path("", view=MovieListView.as_view(), name="list_movies"),
    path("directors", view=DirectorListView.as_view(), name="list_directors"),
    path("actors", view=ActorListView.as_view(), name="list_actors"),
    path("genres", view=GenresListView.as_view(), name="list_genres"),

]
