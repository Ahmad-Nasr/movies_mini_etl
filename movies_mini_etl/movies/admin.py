from django.contrib import admin

from .models import Movie, Director, Actor, Genre, MovieActors, MovieGenres


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    pass


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    pass


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(MovieActors)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(MovieGenres)
class GenreAdmin(admin.ModelAdmin):
    pass
