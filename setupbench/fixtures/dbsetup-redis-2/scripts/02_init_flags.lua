
-- Set some flags
redis.call("SET", "flags:enabled", "true")
redis.call("SET", "flags:version", "2.0")
redis.call("SET", "init_check", "done")
return "Flags initialized"
