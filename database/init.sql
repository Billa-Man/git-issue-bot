CREATE TABLE IF NOT EXISTS repositories (
    id SERIAL PRIMARY KEY,
    repo_name VARCHAR(255) NOT NULL,
    description TEXT,
    stars INT DEFAULT 0,
    forks INT DEFAULT 0,
    language VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);