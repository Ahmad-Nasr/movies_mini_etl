from django.urls import include, path
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from movies_mini_etl.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls
urlpatterns += [
    path("movies/", include('movies_mini_etl.movies.api.routers', namespace="movies_api")),
]
