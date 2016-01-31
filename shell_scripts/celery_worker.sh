#!/usr/bin/env bash

# Start rabbitMQ
rabbitmq-server start &

#celery -A proj beat &
celery -A twitter_bot worker -l info -B