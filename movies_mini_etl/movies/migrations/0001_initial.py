# Generated by Django 4.1.9 on 2023-05-24 02:48

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Actor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                ("name", models.CharField(max_length=128, verbose_name="Name")),
                ("wikidata_id", models.PositiveIntegerField(verbose_name="Wikidata ID")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Director",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                ("name", models.CharField(max_length=128, verbose_name="Name")),
                ("wikidata_id", models.PositiveIntegerField(verbose_name="Wikidata ID")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                ("name", models.CharField(max_length=128, verbose_name="Name")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Movie",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                ("title", models.CharField(max_length=128, verbose_name="Title")),
                ("wikidata_id", models.PositiveIntegerField(verbose_name="Wikidata ID")),
                ("imdb_id", models.CharField(max_length=128, verbose_name="IMDB ID")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
