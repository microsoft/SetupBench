
-- KEYS[1] = namespace
-- ARGV[1] = version, ARGV[2] = marker

local namespace = KEYS[1]
local version = ARGV[1]
local marker = ARGV[2]

redis.call("SET", namespace .. ":version", version)
redis.call("SET", namespace .. ":init_check", marker)

return "Setup complete"
