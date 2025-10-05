import React, { useState } from "react";
import { TextField, Button, Typography } from "@mui/material";

function AddActor({ onAdded }) {
  const [actorName, setActorName] = useState("");
  const [feedback, setFeedback] = useState("");

  const handleAddActor = () => {
    if (!actorName) {
      setFeedback("Please enter the actor's name.");
      return;
    }

    fetch("http://localhost:5001/actors/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: actorName }),
    })
      .then(response => response.json())
      .then(data => {
        setFeedback(`Actor "${data.name}" added successfully!`);
        setActorName("");
        if (onAdded) onAdded();
      })
      .catch(err => {
        console.error("Error adding actor:", err);
        setFeedback("Failed to add actor. Try again.");
      });
  };

  return (
    <div style={{ margin: "16px 0" }}>
      <Typography variant="h6" gutterBottom>
        Add Actor
      </Typography>

      <TextField
        label="Actor Name"
        value={actorName}
        onChange={e => setActorName(e.target.value)}
        fullWidth
        sx={{ mt: 1, mb: 2 }}
      />

      <Button variant="contained" onClick={handleAddActor}>
        Add Actor
      </Button>

      {feedback && (
        <Typography sx={{ mt: 1 }} color="textSecondary">
          {feedback}
        </Typography>
      )}
    </div>
  );
}

export default AddActor;
