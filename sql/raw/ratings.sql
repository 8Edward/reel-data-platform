CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT exists raw.ratings (
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    rating DECIMAL(2,1) NOT NULL,
    ts BIGINT NOT NULL
);
