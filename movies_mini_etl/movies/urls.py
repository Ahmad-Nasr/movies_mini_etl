from django.urls import path

from .views import MovieListView, DirectorListView, ActorListView

app_name = "movies"
urlpatterns = [
    path("", view=MovieListView.as_view(), name="list_movies"),
    path("directors", view=DirectorListView.as_view(), name="list_directors"),
    path("actors", view=ActorListView.as_view(), name="list_actors"),
]
