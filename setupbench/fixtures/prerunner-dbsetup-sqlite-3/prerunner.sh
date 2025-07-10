#!/bin/bash
# Simulate a legacy environment with a fake broken .db file and permission issues

echo "Creating broken SQLite file..."
mkdir -p /data
echo "not-a-real-db" > /data/test.db
chmod 400 /data/test.db

# Add a dummy Python 2 symlink to mislead agents who scan for python versions
mkdir -p /opt/fakepython
ln -s /usr/bin/echo /opt/fakepython/python2

# Delay to simulate cold startup quirks
sleep 5