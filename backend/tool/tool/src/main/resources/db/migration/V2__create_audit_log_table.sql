CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,

    entity_type VARCHAR(100) NOT NULL,
    entity_id BIGINT NOT NULL,

    action VARCHAR(50) NOT NULL,
    performed_by VARCHAR(100),

    old_value JSONB,
    new_value JSONB,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_entity
ON audit_log(entity_type, entity_id);

CREATE INDEX idx_audit_action
ON audit_log(action);

CREATE INDEX idx_audit_created_at
ON audit_log(created_at);

CREATE INDEX idx_audit_performed_by
ON audit_log(performed_by);