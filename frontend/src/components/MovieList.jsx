import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Card, CardContent, Typography, Grid, TextField, MenuItem, Button } from "@mui/material";

function MovieList() {
  const [movies, setMovies] = useState([]);
  const [genres, setGenres] = useState([]);
  const [actors, setActors] = useState([]);
  const [directors, setDirectors] = useState([]);
  const [filters, setFilters] = useState({ genre_id: "", actor_id: "", director_id: "" });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [moviesRes, genresRes, actorsRes, directorsRes] = await Promise.all([
          fetch("http://localhost:5001/movies/"),
          fetch("http://localhost:5001/genres/"),
          fetch("http://localhost:5001/actors/"),
          fetch("http://localhost:5001/directors/"),
        ]);
        setMovies(await moviesRes.json());
        setGenres(await genresRes.json());
        setActors(await actorsRes.json());
        setDirectors(await directorsRes.json());
      } catch (err) {
        console.error("Failed to fetch data:", err);
      }
    };

    fetchData();
  }, []);

  const handleFilterChange = (e) => {
    setFilters(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSearch = () => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value) params.append(key, value);
    });
    fetch(`http://localhost:5001/movies/?${params}`)
      .then(res => res.json())
      .then(setMovies)
      .catch(err => console.error("Search failed:", err));
  };

  return (
    <>
      {/* Filters */}
      <Grid container spacing={2} sx={{ mb: 2 }}>
        <Grid item xs={3}>
          <TextField
            select
            label="Actor"
            name="actor_id"
            value={filters.actor_id}
            onChange={handleFilterChange}
            fullWidth
            sx={{
              '& .MuiInputBase-root': { minHeight: 50, display: 'flex', alignItems: 'center', paddingTop: 0, paddingBottom: 0 },
              '& .MuiSelect-select': { display: 'flex', alignItems: 'center', height: '100%', paddingTop: 0, paddingBottom: 0 },
            }}
          >
            <MenuItem value="">All</MenuItem>
            {actors.map(actor => (
              <MenuItem key={actor.actor_id} value={actor.actor_id}>{actor.name}</MenuItem>
            ))}
          </TextField>
        </Grid>

        <Grid item xs={3}>
          <TextField
            select
            label="Director"
            name="director_id"
            value={filters.director_id}
            onChange={handleFilterChange}
            fullWidth
            sx={{
              '& .MuiInputBase-root': { minHeight: 50, display: 'flex', alignItems: 'center', paddingTop: 0, paddingBottom: 0 },
              '& .MuiSelect-select': { display: 'flex', alignItems: 'center', height: '100%', paddingTop: 0, paddingBottom: 0 },
            }}
          >
            <MenuItem value="">All</MenuItem>
            {directors.map(d => (
              <MenuItem key={d.director_id} value={d.director_id}>{d.name}</MenuItem>
            ))}
          </TextField>
        </Grid>

        <Grid item xs={3}>
          <Button
            variant="contained"
            onClick={handleSearch}
            fullWidth
            sx={{ height: 50, fontSize: '1rem', fontWeight: 'bold' }}
          >
            Filter
          </Button>
        </Grid>
      </Grid>

      {/* Movie List */}
      <Grid container spacing={2}>
        {movies.map(movie => (
          <Grid item xs={12} sm={6} key={movie.movie_id}>
            <Card>
              <CardContent>
                <Typography
                  variant="h6"
                  component={Link}
                  to={`/movies/${movie.movie_id}`}
                  sx={{ textDecoration: 'none' }}
                >
                  {movie.title}
                </Typography>
                <Typography variant="body2">Year: {movie.release_year}</Typography>
                <Typography variant="body2">
                  Genres: {movie.genres?.map(g => g.name).join(", ")}
                </Typography>
                <Typography variant="body2">Director: {movie.director?.name}</Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </>
  );
}

export default MovieList;
