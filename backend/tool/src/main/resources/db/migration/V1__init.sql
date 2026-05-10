CREATE TABLE roles(
    id UUID PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE users(
    id UUID PRIMARY KEY,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role_id UUID REFERENCES roles(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE survey(
    id UUID PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    status VARCHAR(50),
    score INT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    deleted BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_survey_status ON survey(status);
CREATE INDEX idx_survey_created ON survey(created_at);