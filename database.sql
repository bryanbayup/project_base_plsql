CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Tambahkan tabel log
CREATE TABLE user_log (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    action VARCHAR(10),
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Tambahkan trigger pada tabel user
CREATE OR REPLACE FUNCTION user_log_trigger()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO user_log (username, action) VALUES (NEW.username, 'INSERT');
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO user_log (username, action) VALUES (NEW.username, 'UPDATE');
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO user_log (username, action) VALUES (OLD.username, 'DELETE');
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER user_trigger
AFTER INSERT OR UPDATE OR DELETE
ON users
FOR EACH ROW
EXECUTE FUNCTION user_log_trigger();
