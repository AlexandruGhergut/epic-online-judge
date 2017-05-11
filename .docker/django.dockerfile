FROM        python:3.5.2

MAINTAINER  Alexandru Gherguț

COPY        . /var/www/
WORKDIR     /var/www/

RUN         apt-get update -y
RUN         pip install -r requirements.txt
RUN         apt-get install postgresql-client -y
