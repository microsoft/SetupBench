# Block default Redis port
apt-get update && apt-get install -y netcat
nohup nc -l -p 6379 >/dev/null 2>&1 &

# Create a broken background process to confuse the agent
nohup sh -c 'while true; do echo "fake redis running"; sleep 60; done' >/tmp/fake-redis.log 2>&1 &

# Create custom redis.conf with one malformed line
mkdir -p /etc/redis
cat <<EOF > /etc/redis/redis.conf
bind 127.0.0.1
port 6380
daemonize yes
requirepass benchmark_pass
user benchmark_user on >benchmark_pass ~setup:* allcommands allkeys
save 900 1
this_is_not_a_valid_directive true
EOF

# Delay to simulate cold start
sleep 10