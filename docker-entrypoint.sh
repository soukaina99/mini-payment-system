#!/bin/bash
set -e


# Assign docker host IP Address
export DOCKER_HOST=$(/sbin/ip route|awk '/default/ { print $3 }')

exec "$@"
