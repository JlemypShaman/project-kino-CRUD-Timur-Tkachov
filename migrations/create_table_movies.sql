-- migration SQL: create_table_movies.sql
CREATE TABLE IF NOT EXISTS movie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    genre VARCHAR(50) NOT NULL,
    rating FLOAT NOT NULL,
    release_year INTEGER NOT NULL
);
