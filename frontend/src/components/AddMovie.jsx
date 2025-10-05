import React, { useEffect, useState } from "react";
import {
  TextField,
  Button,
  Typography,
  MenuItem,
  Select,
  InputLabel,
  FormControl,
  Chip,
  Box
} from "@mui/material";

function AddMovie({ onAdded }) {
  const [title, setTitle] = useState("");
  const [year, setYear] = useState("");
  const [actors, setActors] = useState([]);
  const [directors, setDirectors] = useState([]);
  const [genres, setGenres] = useState([]);

  const [selectedActors, setSelectedActors] = useState([]);
  const [selectedDirector, setSelectedDirector] = useState("");
  const [selectedGenres, setSelectedGenres] = useState([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("http://localhost:5001/actors/").then(r => r.json()).then(setActors);
    fetch("http://localhost:5001/directors/").then(r => r.json()).then(setDirectors);
    fetch("http://localhost:5001/genres/").then(r => r.json()).then(setGenres);
  }, []);

  const handleAdd = () => {
    if (!title || !year || selectedActors.length === 0 || !selectedDirector || selectedGenres.length === 0) {
      return setMessage("All fields are required");
    }

    fetch("http://localhost:5001/movies/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        release_year: parseInt(year),
        actor_ids: selectedActors.map(a => parseInt(a)),
        director_id: parseInt(selectedDirector),
        genre_ids: selectedGenres.map(g => parseInt(g)),
      }),
    })
      .then(res => res.json())
      .then(data => {
        setMessage(`Movie "${data.title}" added successfully`);
        setTitle("");
        setYear("");
        setSelectedActors([]);
        setSelectedDirector("");
        setSelectedGenres([]);
        onAdded?.();
      })
      .catch(() => setMessage("Error adding movie"));
  };

  return (
    <div style={{ margin: "16px 0" }}>
      <Typography variant="h6">Add Movie</Typography>

      {/* Title */}
      <TextField
        label="Title"
        value={title}
        onChange={e => setTitle(e.target.value)}
        fullWidth
        sx={{ mt: 1, mb: 1 }}
      />

      {/* Year */}
      <TextField
        label="Release Year"
        value={year}
        onChange={e => setYear(e.target.value)}
        type="number"
        fullWidth
        sx={{ mt: 1, mb: 1 }}
      />

      {/* Actors */}
      <FormControl fullWidth sx={{ mt: 1, mb: 1 }}>
        <InputLabel>Actors</InputLabel>
        <Select
          multiple
          value={selectedActors}
          onChange={e => setSelectedActors(e.target.value)}
          renderValue={(selected) => (
            <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
              {selected.map(actorId => {
                const actor = actors.find(a => a.actor_id === actorId);
                return actor ? <Chip key={actorId} label={actor.name} /> : null;
              })}
            </Box>
          )}
        >
          {actors.map(a => (
            <MenuItem key={a.actor_id} value={a.actor_id}>{a.name}</MenuItem>
          ))}
        </Select>
      </FormControl>

      {/* Director */}
      <TextField
        select
        label="Director"
        value={selectedDirector}
        onChange={e => setSelectedDirector(e.target.value)}
        fullWidth
        sx={{ mt: 1, mb: 1 }}
      >
        <MenuItem value="">Select Director</MenuItem>
        {directors.map(d => (
          <MenuItem key={d.director_id} value={d.director_id}>{d.name}</MenuItem>
        ))}
      </TextField>

      {/* Genres */}
      <FormControl fullWidth sx={{ mt: 1, mb: 1 }}>
        <InputLabel>Genres</InputLabel>
        <Select
          multiple
          value={selectedGenres}
          onChange={e => setSelectedGenres(e.target.value)}
          renderValue={(selected) => (
            <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
              {selected.map(genreId => {
                const genre = genres.find(g => g.genre_id === genreId);
                return genre ? <Chip key={genreId} label={genre.name} /> : null;
              })}
            </Box>
          )}
        >
          {genres.map(g => (
            <MenuItem key={g.genre_id} value={g.genre_id}>{g.name}</MenuItem>
          ))}
        </Select>
      </FormControl>

      <Button variant="contained" onClick={handleAdd}>
        Add Movie
      </Button>

      {message && <Typography sx={{ mt: 1 }}>{message}</Typography>}
    </div>
  );
}

export default AddMovie;
