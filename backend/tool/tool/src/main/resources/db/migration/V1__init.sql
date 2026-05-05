CREATE TABLE survey (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    title VARCHAR(255) NOT NULL,
    description TEXT,

    status VARCHAR(50) NOT NULL,
    score INT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    created_by VARCHAR(100),

    is_deleted BOOLEAN DEFAULT FALSE
);

-- Indexes (VERY IMPORTANT)
CREATE INDEX idx_status ON survey(status);
CREATE INDEX idx_created_at ON survey(created_at);