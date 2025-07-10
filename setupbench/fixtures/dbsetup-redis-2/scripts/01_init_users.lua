
-- Set some user keys
redis.call("SET", "user:1", "Alice")
redis.call("SET", "user:2", "Bob")
return "Users initialized"
