from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import LoadMoviesAPIView

router_v1 = DefaultRouter('v1')

app_name = "movies"

urlpatterns = [
    path('load-movies', LoadMoviesAPIView.as_view(), name="load_movies"),
] + router_v1.urls
