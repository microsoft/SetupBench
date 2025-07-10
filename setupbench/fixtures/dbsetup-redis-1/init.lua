
-- Set a key to confirm initialization
redis.call("SET", "init_check", "done")
return true
