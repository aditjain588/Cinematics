-- Drop tables if they exist
DROP TABLE IF EXISTS actors_movie;
DROP TABLE IF EXISTS movies_genres;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS actors;
DROP TABLE IF EXISTS directors;
DROP TABLE IF EXISTS genres;

-- Directors
CREATE TABLE directors (
    director_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Genres
CREATE TABLE genres (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Actors
CREATE TABLE actors (
    actor_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Movies
CREATE TABLE movies (
    movie_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INT,
    director_id INT REFERENCES directors(director_id) ON DELETE SET NULL
);

-- Join table: movies <-> genres
CREATE TABLE movies_genres (
    movie_id INT REFERENCES movies(movie_id) ON DELETE CASCADE,
    genre_id INT REFERENCES genres(genre_id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, genre_id)
);

-- Join table: movies <-> actors
CREATE TABLE actors_movie (
    movie_id INT REFERENCES movies(movie_id) ON DELETE CASCADE,
    actor_id INT REFERENCES actors(actor_id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, actor_id)
);

-- Sample data

-- Directors
INSERT INTO directors (name) VALUES
('Steven Spielberg'), 
('Christopher Nolan'), 
('Quentin Tarantino'),
('Karan Johar');

-- Genres
INSERT INTO genres (name) VALUES
('Action'), 
('Drama'), 
('Comedy'), 
('Thriller'),
('Romance');

-- Actors
INSERT INTO actors (name) VALUES
('Leonardo DiCaprio'),
('Brad Pitt'),
('Tom Hanks'),
('Shah Rukh Khan'),
('Kajol');

-- Movies
INSERT INTO movies (title, release_year, director_id) VALUES
('Inception', 2010, 2),
('Catch Me If You Can', 2002, 1),
('Pulp Fiction', 1994, 3),
('Dilwale Dulhania Le Jayenge', 1995, 4),
('My Name Is Khan', 2010, 4),
('Chennai Express', 2013, 4);

-- Movies <-> Genres
INSERT INTO movies_genres (movie_id, genre_id) VALUES
(1, 1), -- Inception -> Action
(1, 4), -- Inception -> Thriller
(2, 2), -- Catch Me If You Can -> Drama
(3, 1), -- Pulp Fiction -> Action
(3, 4), -- Pulp Fiction -> Thriller
(4, 5), -- DDLJ -> Romance
(4, 2), -- DDLJ -> Drama
(5, 2), -- My Name Is Khan -> Drama
(5, 5), -- My Name Is Khan -> Romance
(6, 1), -- Chennai Express -> Action
(6, 5); -- Chennai Express -> Romance

-- Movies <-> Actors
INSERT INTO actors_movie (movie_id, actor_id) VALUES
(1, 1), -- Inception -> Leonardo DiCaprio
(2, 3), -- Catch Me If You Can -> Tom Hanks
(3, 2), -- Pulp Fiction -> Brad Pitt
(4, 4), -- DDLJ -> Shah Rukh Khan
(4, 5), -- DDLJ -> Kajol
(5, 4), -- My Name Is Khan -> Shah Rukh Khan
(6, 4), -- Chennai Express -> Shah Rukh Khan
(6, 5); -- Chennai Express -> Kajol
