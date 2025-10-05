import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { Card, CardContent, Typography, Chip, Grid } from "@mui/material";

function MovieDetail() {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        const response = await fetch(`http://localhost:5001/movies/${id}`);
        const data = await response.json();
        setMovie(data);
      } catch (err) {
        console.error("Failed to fetch movie:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchMovie();
  }, [id]);

  if (loading) return <div>Loading movie details...</div>;
  if (!movie) return <div>Movie not found.</div>;

  return (
    <Card sx={{ mt: 2 }}>
      <CardContent>
        <Typography variant="h4">{movie.title}</Typography>
        <Typography variant="subtitle1" sx={{ mt: 1 }}>
          Year: {movie.release_year}
        </Typography>

        <Typography variant="subtitle1" sx={{ mt: 1 }}>
          Director:{" "}
          {movie.director ? (
            <Link to={`/directors/${movie.director.director_id}`}>
              {movie.director.name}
            </Link>
          ) : (
            "N/A"
          )}
        </Typography>

        <Typography variant="subtitle1" sx={{ mt: 1 }}>
          Genres:
        </Typography>
        {movie.genres?.map(genre => (
          <Chip key={genre.genre_id} label={genre.name} sx={{ mr: 1, mb: 1 }} />
        ))}

        <Typography variant="subtitle1" sx={{ mt: 2 }}>
          Cast:
        </Typography>
        <Grid container spacing={1}>
          {movie.actors?.map(actor => (
            <Grid item key={actor.actor_id}>
              <Chip
                label={actor.name}
                component={Link}
                to={`/actors/${actor.actor_id}`}
                clickable
                color="primary"
              />
            </Grid>
          ))}
        </Grid>
      </CardContent>
    </Card>
  );
}

export default MovieDetail;
