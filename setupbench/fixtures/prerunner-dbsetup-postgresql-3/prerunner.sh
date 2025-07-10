#!/bin/bash
# Block port 5432
apt-get update && apt-get install -y netcat
nohup nc -l -p 5432 >/dev/null 2>&1 &

# Add broken .psqlrc to interfere with automation
echo '\\echo Welcome to the Broken PSQL' > /root/.psqlrc
