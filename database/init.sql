-- BOOKMARKED REPOSITORIES
CREATE TABLE IF NOT EXISTS bookmarkedrepositories (
    id SERIAL PRIMARY KEY,
    website VARCHAR(255) NOT NULL,
    user_id INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- BOOKMARKED ISSUES
CREATE TABLE IF NOT EXISTS bookmarkedissues (
    id SERIAL PRIMARY KEY,
    website VARCHAR(255) NOT NULL,
    user_id INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CHAT HISTORY
CREATE TABLE chat_history (
    id SERIAL PRIMARY KEY,
    role VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);