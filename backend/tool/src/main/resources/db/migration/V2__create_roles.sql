CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Seed default roles
INSERT INTO roles (name) VALUES
('ADMIN'),
('MANAGER'),
('VIEWER');