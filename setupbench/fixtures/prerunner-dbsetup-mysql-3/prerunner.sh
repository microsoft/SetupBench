#!/bin/bash
# Block default MySQL port
apt-get update && apt-get install -y netcat
nohup nc -l -p 3306 >/dev/null 2>&1 &

# Configure MySQL strict mode globally
echo "[mysqld]" >> /etc/mysql/my.cnf
echo "sql_mode=STRICT_ALL_TABLES" >> /etc/mysql/my.cnf

# Ensure permissions and path
chmod 644 /etc/mysql/my.cnf

# Delay to simulate slow MySQL startup
sleep 10
