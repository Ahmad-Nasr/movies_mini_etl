from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class MoviesLoadingSerializer(serializers.Serializer):
    movies_count = serializers.IntegerField(required=False)
