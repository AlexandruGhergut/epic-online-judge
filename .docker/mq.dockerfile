FROM        rabbitmq:3.6.9-management

COPY        .docker/scripts /tmp
WORKDIR     /tmp

RUN        echo '[{rabbit, [{loopback_users, []}]}].' > /etc/rabbitmq/rabbitmq.config
RUN        chmod 666 /etc/rabbitmq/rabbitmq.config
