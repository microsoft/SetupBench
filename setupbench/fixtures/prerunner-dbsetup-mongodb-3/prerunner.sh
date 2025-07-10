#!/bin/bash
# Block default MongoDB port
apt-get update && apt-get install -y netcat
nohup nc -l -p 27017 >/dev/null 2>&1 &

# Simulate slow service start
sleep 5

# Pre-create mongod config with replica set and custom port
mkdir -p /etc/mongod.conf.d
cat <<EOF > /etc/mongod.conf
storage:
  dbPath: /var/lib/mongodb
net:
  port: 27018
  bindIp: 127.0.0.1
replication:
  replSetName: rs0
security:
  authorization: enabled
EOF
