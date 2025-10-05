import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { Card, CardContent, Typography, Chip, Grid } from "@mui/material";

function DirectorProfile() {
  const { id } = useParams();
  const [director, setDirector] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDirector = async () => {
      try {
        const response = await fetch(`http://localhost:5001/directors/${id}`);
        const data = await response.json();
        setDirector(data);
      } catch (err) {
        console.error("Failed to fetch director:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchDirector();
  }, [id]);

  if (loading) return <div>Loading director details...</div>;

  if (!director) return <div>Director not found.</div>;

  return (
    <Card sx={{ mt: 2 }}>
      <CardContent>
        <Typography variant="h4">{director.name}</Typography>

        <Typography variant="subtitle1" sx={{ mt: 2, mb: 1 }}>
          Movies:
        </Typography>
        <Grid container spacing={1}>
          {director.movies?.map(movie => (
            <Grid item key={movie.movie_id}>
              <Chip
                label={movie.title}
                component={Link}
                to={`/movies/${movie.movie_id}`}
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

export default DirectorProfile;
