import logging

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .serializers import MoviesLoadingSerializer
from movies_mini_etl.movies.utils import WikidataMoviesLoader

logger = logging.getLogger(__name__)


class LoadMoviesAPIView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MoviesLoadingSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        movies_count = serializer.validated_data.get("movies_count", 5)

        WikidataMoviesLoader.load_movies(movies_count)
        return Response(status=status.HTTP_200_OK)
