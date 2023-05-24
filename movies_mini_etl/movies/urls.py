from django.urls import path
from django.views.generic import TemplateView

from .views import MovieListView

app_name = "movies"
urlpatterns = [
    path("", view=MovieListView.as_view(), name="list_movies"),
]
