from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


class Movie(TimeStampedModel):
    title = models.CharField(_('Title'), max_length=128)
    wikidata_id = models.PositiveIntegerField(_('Wikidata ID'))
    imdb_id = models.CharField(_('IMDB ID'), max_length=128)
    director = models.ForeignKey('movies.Director', related_name='movies',
                                 null=True, on_delete=models.SET_NULL)
    actors = models.ManyToManyField('movies.Actor', through='movies.MovieActors')
    genres = models.ManyToManyField('movies.Genre', through='movies.MovieGenres')

    def __str__(self):
        return self.title


class Director(TimeStampedModel):
    name = models.CharField(_('Name'), max_length=128)
    wikidata_id = models.PositiveIntegerField(_('Wikidata ID'))

    def __str__(self):
        return self.name


class Actor(TimeStampedModel):
    name = models.CharField(_('Name'), max_length=128)
    wikidata_id = models.PositiveIntegerField(_('Wikidata ID'))

    def __str__(self):
        return self.name


class Genre(TimeStampedModel):
    name = models.CharField(_('Name'), max_length=128)

    def __str__(self):
        return self.name


class MovieActors(TimeStampedModel):
    movie = models.ForeignKey("movies.Movie", on_delete=models.CASCADE)
    actor = models.ForeignKey("movies.Actor", on_delete=models.CASCADE)


class MovieGenres(TimeStampedModel):
    movie = models.ForeignKey("movies.Movie", on_delete=models.CASCADE)
    genre = models.ForeignKey("movies.Genre", on_delete=models.CASCADE)
