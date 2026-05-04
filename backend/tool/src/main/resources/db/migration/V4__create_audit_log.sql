DROP TABLE IF EXISTS audit_log;

CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    entity_name VARCHAR(100),
    entity_id BIGINT,
    action VARCHAR(20),
    old_value JSONB,
    new_value JSONB,
    username VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);