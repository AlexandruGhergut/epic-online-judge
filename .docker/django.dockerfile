FROM        python:3.5.2

MAINTAINER  Alexandru Gherguț

COPY        . /var/www/
WORKDIR     /var/www/

RUN         pip install -r requirements.txt
RUN         python manage.py makemigrations
RUN         python manage.py migrate

ENTRYPOINT  ["python", "manage.py", "runserver", "0.0.0.0:8000"]
