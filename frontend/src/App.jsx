import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import { Container, Typography, Button, Stack } from "@mui/material";

import MovieList from "./components/MovieList";
import MovieDetail from "./components/MovieDetail";
import ActorProfile from "./components/ActorProfile";
import DirectorProfile from "./components/DirectorProfile";
import AddActor from "./components/AddActor";
import AddDirector from "./components/AddDirector";
import AddMovie from "./components/AddMovie";

function App() {
  return (
    <Router>
      <Container maxWidth="md" style={{ padding: "20px" }}>
        {/* App Title */}
        <Typography variant="h3" align="center" gutterBottom>
          🎬 Cinematics
        </Typography>

        {/* Quick Nav Buttons */}
        <Stack
          direction="row"
          spacing={2}
          justifyContent="center"
          style={{ marginBottom: "20px" }}
        >
          <Button component={Link} to="/" variant="contained" color="primary">
            Movies
          </Button>
          <Button
            component={Link}
            to="/add-movie"
            variant="outlined"
            color="secondary"
          >
            Add Movie
          </Button>
          <Button
            component={Link}
            to="/add-actor"
            variant="outlined"
            color="secondary"
          >
            Add Actor
          </Button>
          <Button
            component={Link}
            to="/add-director"
            variant="outlined"
            color="secondary"
          >
            Add Director
          </Button>
        </Stack>

        {/* Routes */}
        <Routes>
          <Route path="/" element={<MovieList />} />
          <Route path="/movies/:id" element={<MovieDetail />} />
          <Route path="/actors/:id" element={<ActorProfile />} />
          <Route path="/directors/:id" element={<DirectorProfile />} />
          <Route path="/add-actor" element={<AddActor />} />
          <Route path="/add-director" element={<AddDirector />} />
          <Route path="/add-movie" element={<AddMovie />} />
        </Routes>
      </Container>
    </Router>
  );
}

export default App;
