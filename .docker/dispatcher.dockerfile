FROM docker:17.05.0

MAINTAINER  Alexandru Gherguț

RUN         apk add alpine-sdk --no-cache
RUN         apk add --no-cache python3 && \
                    python3 -m ensurepip && \
                    rm -r /usr/lib/python*/ensurepip && \
                    pip3 install --upgrade pip setuptools && \
                    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
                    rm -r /root/.cache
RUN         apk add --no-cache postgresql-dev python3-dev libffi-dev

COPY        requirements.txt /var/www/requirements.txt
WORKDIR     /var/www/
RUN         pip install -r requirements.txt
RUN         pip install docker-compose
RUN         apk add postgresql-client --no-cache

COPY        . .
