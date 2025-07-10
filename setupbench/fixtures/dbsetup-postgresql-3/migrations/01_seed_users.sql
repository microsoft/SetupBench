INSERT INTO users (username, email)
VALUES ('hacker', 'hacker@example.com')
ON CONFLICT DO NOTHING;
