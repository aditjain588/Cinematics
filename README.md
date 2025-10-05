# Cinematics

Cinematics is a full-stack web application for managing movies, genres, actors, and directors. Users can view movies, filter by genres, and see associated ratings/reviews. The project is built with **Python Flask** for the backend and **Vite + React** for the frontend, fully Dockerized for easy setup.

## Demo
A sample video demonstrating the app's functionality is available here in project root directory.

## Features

- List, add, and delete **Movies**, **Genres**, **Actors**, and **Directors**
- Backend API filtering (e.g., filter genres by movie)
- Dummy movie ratings/reviews included
- Modular, maintainable, and testable code
- Responsive and clean UI built with React
- Fully Dockerized with `docker-compose`

## Tech Stack

- **Frontend**: React + Vite
- **Backend**: Python Flask + Flask-RESTX
- **Database**: PostgreSQL
- **Docker**: Containerization of frontend, backend, and database
- **Linting & Testing**:
  - Backend: `flake8` for linting, `pytest` for unit tests

## Project Structure

```plaintext
Cinematics/
│
├── backend/                 # Flask backend code
├── frontend/                # React frontend (Vite)
├── db/                      # Database files
├── docker-compose.yml       # Docker compose for full-stack
├── README.md                # Project documentation
└── package-lock.json        # Frontend dependency lock file
└── Demo                     # Screen recording of working app

```

## Sample Data
 - Sample data along with table schema present in db/init.sql
   
## Docker Setup
```plaintext
# Build and start containers
docker-compose up --build

# Access the application
# Frontend: http://localhost:5173
# Backend API Swagger: http://localhost:5001

# Stop containers
docker-compose down

# Start containers without rebuilding
docker-compose up

# Rebuild containers
docker-compose up --build --force-recreate

# Clean up Docker images and volumes
docker system prune -af           # Remove stopped containers, networks, dangling images
docker volume prune -f            # Remove unused volumes (database data will be lost!)

```
## Local Deployment
```plaintext
# Backend
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py

# Run linting and tests
flake8 routes models
pytest

# Frontend
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev

```
## API Endpoints

### Movies

| Method | Route          | Description       | Filters                                        |
|--------|----------------|-----------------|------------------------------------------------|
| GET    | /movies/       | List all movies  | genre_id, director_id, actor_id, release_year |
| POST   | /movies/       | Add a new movie  | N/A                                            |
| GET    | /movies/<id>   | Get movie by ID  | movie_id                                           |
| DELETE | /movies/<id>   | Delete a movie   | movie_id                                            |

### Genres

| Method | Route          | Description       | Filters        |
|--------|----------------|-----------------|----------------|
| GET    | /genres/       | List all genres  | movie_id       |
| POST   | /genres/       | Add a new genre  | N/A            |
| GET    | /genres/<id>   | Get genre by ID  | genre_id            |
| DELETE | /genres/<id>   | Delete a genre   | genre_id            |

### Actors

| Method | Route          | Description       | Filters        |
|--------|----------------|-----------------|----------------|
| GET    | /actors/       | List all actors  | movie_id, genre_id      |
| POST   | /actors/       | Add a new actor  | N/A            |
| GET    | /actors/<id>   | Get actor by ID  | actor_id           |
| DELETE | /actors/<id>   | Delete an actor  | actor_id            |

### Directors

| Method | Route          | Description       | Filters        |
|--------|----------------|-----------------|----------------|
| GET    | /directors/    | List all directors | movie_id, genre_id     |
| POST   | /directors/    | Add a new director | N/A         |
| GET    | /directors/<id>| Get director by ID | director_id         |
| DELETE | /directors/<id>| Delete a director  | director_id          |

## API Filtering Examples


### Get movie by director
- GET /movies/?director_id=1

### Get movie by actor
- GET /movies/?actor_id=1

### Get movies by genre
- GET /movies/?genre_id=2

### Get movie of director and actor
- GET /movies/?director_id=1&actor_id=1

### Get genres associated with a movie
- GET /genres/?movie_id=5

### Get actors for a movie
- GET /actors/?movie_id=3

### Get directors for a movie
- GET /directors/?movie_id=1


## Edge Cases

- Handles cases where no movies, genres, actors, or directors are available with appropriate messages
- Manages invalid filters and missing resources with proper HTTP error codes
- Backend filtering ensures the frontend always receives correct data
