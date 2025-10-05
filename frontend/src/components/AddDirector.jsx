import React, { useState } from "react";
import { TextField, Button, Typography } from "@mui/material";

function AddDirector({ onAdded }) {
  const [directorName, setDirectorName] = useState("");
  const [feedback, setFeedback] = useState("");

  const handleAddDirector = async () => {
    if (!directorName) {
      setFeedback("Please enter a director's name.");
      return;
    }

    try {
      const res = await fetch("http://localhost:5001/directors/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: directorName }),
      });

      if (res.ok) {
        const data = await res.json();
        setFeedback(`Director "${data.name}" added successfully!`);
        setDirectorName("");
        if (onAdded) onAdded();
      } else {
        setFeedback("Failed to add director. Please try again.");
      }
    } catch (err) {
      console.error("Error adding director:", err);
      setFeedback("Something went wrong while adding the director.");
    }
  };

  return (
    <div style={{ marginTop: "20px" }}>
      <Typography variant="h6" gutterBottom>
        Add Director
      </Typography>

      <TextField
        label="Director Name"
        value={directorName}
        onChange={(e) => setDirectorName(e.target.value)}
        fullWidth
        margin="normal"
      />

      <Button variant="contained" onClick={handleAddDirector}>
        Add Director
      </Button>

      {feedback && (
        <Typography variant="body2" sx={{ mt: 1 }} color="textSecondary">
          {feedback}
        </Typography>
      )}
    </div>
  );
}

export default AddDirector;
