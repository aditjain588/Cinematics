import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { Card, CardContent, Typography, Chip, Grid } from "@mui/material";

function ActorProfile() {
  const { id: actorId } = useParams();
  const [actorData, setActorData] = useState(null);

  useEffect(() => {
    // Fetch actor details from API
    fetch(`http://localhost:5001/actors/${actorId}`)
      .then(response => response.json())
      .then(data => setActorData(data))
      .catch(err => console.error("Failed to load actor:", err));
  }, [actorId]);

  if (!actorData) {
    return <div>Loading actor information...</div>;
  }

  return (
    <Card sx={{ mt: 3, p: 2 }}>
      <CardContent>
        <Typography variant="h4" gutterBottom>
          {actorData.name}
        </Typography>

        <Typography variant="subtitle1" sx={{ mt: 2, mb: 1 }}>
          Movies:
        </Typography>

        <Grid container spacing={1}>
          {actorData.movies?.map(movie => (
            <Grid item key={movie.movie_id}>
              <Chip
                label={movie.title}
                component={Link}
                to={`/movies/${movie.movie_id}`}
                clickable
                color="primary"
                sx={{ cursor: "pointer" }}
              />
            </Grid>
          ))}
        </Grid>
      </CardContent>
    </Card>
  );
}

export default ActorProfile;
