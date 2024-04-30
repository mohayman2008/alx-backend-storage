#!/usr/bin/env bash

wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" > /etc/apt/sources.list.d/mongodb-org-4.2.list
sudo apt-get update
sudo apt-get install -y mongodb-org

sudo service mongod status
echo

mongo --version
echo

pip3 install pymongo
python3 -c 'print(__import__("pymongo").__version__)'
