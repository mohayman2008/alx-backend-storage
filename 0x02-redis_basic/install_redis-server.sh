#!/usr/bin/env bash

sudo apt-get update
sudo apt-get -y install redis-server
sudo service redis-server start
pip3 install redis


## Uncomment the following line to bind the server only to loopback IPv4 network interface ##
# sed -i "s/bind .*/bind 127.0.0.1/g" /etc/redis/redis.conf
