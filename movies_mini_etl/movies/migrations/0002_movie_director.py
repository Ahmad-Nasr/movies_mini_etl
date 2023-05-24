# Generated by Django 4.1.9 on 2023-05-24 02:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="director",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="movies", to="movies.director"
            ),
        ),
    ]
