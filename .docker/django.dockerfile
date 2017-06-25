FROM        python:3.5.2

MAINTAINER  Alexandru Gherguț

COPY        requirements.txt /var/www/requirements.txt
WORKDIR     /var/www/
RUN         pip install -r requirements.txt

RUN         apt-get update -y
RUN         apt-get install postgresql-client -y

COPY        . .
