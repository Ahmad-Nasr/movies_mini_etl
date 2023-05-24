# movies_mini_etl

Mini ETL project that loads movies data from [wikidata.org](https://www.wikidata.org/), stores it to database tables, and displays it in webpages.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Screenshots
![alt text](https://lh3.googleusercontent.com/drive-viewer/AFGJ81qvLGWIKxB8YK5uYSLtuVFX6UA-1yZOE8zp65t7RnkfmMLsX3dsZu0aPSFQj_8pBTpb82hMGCT2fmAWNuG0Agc3CzPv=w1366-h643)

![alt text](https://lh3.googleusercontent.com/drive-viewer/AFGJ81p8ioJf9zRvSwkJiIhcEt3ErtV5WpW_oXDthlXNaaw5ZiQQ5ipyfl89u60TmXXcWNjTJ_QHYZSlcZmi_DV-iE5S6FSoMQ=w1366-h643)

![alt text](https://lh3.googleusercontent.com/drive-viewer/AFGJ81p3gRm5R-P1nl7Jn8Nn_r1nMLs0IEwKPbv2DRd-AJtJqWkHKFA-R4R1JdJrgGfK49mc6Vk8bKCWmOpBnbhfMbAfecIEBQ=w1366-h643)

![alt text](https://lh3.googleusercontent.com/drive-viewer/AFGJ81pfkLhsChS47Y0Ackt-w6jvSvoQNCt8-8SGK8HNCVjvODlfzr2RTIXzdeX_PdEaszTiBcdM7ALAVu4D2FDgQSpC6VWY=w1366-h643)

## Running on local machine
      
      $ docker-compose -f local.yml build
      $ docker-compose -f local.yml up
      
## Running tests
     
     $ docker-compose -f local.yml run --rm django pytest 

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).
