import React, { useState } from "react";
import axios from "axios";
import * as Tone from "tone";
import "./App.css";

const App = () => {
  const [progression, setProgression] = useState([]);
  const [suggestedChord, setSuggestedChord] = useState(null);
  const [probability, setProbability] = useState(null);
  const [inputChords, setInputChords] = useState("");

  const chordNotes = {
    C: ["C4", "E4", "G4"],
    G: ["G3", "B3", "D4"],
    Am: ["A3", "C4", "E4"],
    F: ["F3", "A3", "C4"],
  };

  const fetchSuggestedChord = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/api/predict", {
        chords: progression,
      });
      setSuggestedChord(response.data.chord);
      setProbability(response.data.probability);
    } catch (error) {
      alert("Error fetching suggested chord.");
    }
  };

  const addChordToProgression = (chord) => {
    setProgression([...progression, chord]);
    fetchSuggestedChord();
  };

  const deleteLastChord = () => {
    const updatedProgression = progression.slice(0, -1);
    setProgression(updatedProgression);
    fetchSuggestedChord();
  };

  const playProgression = async () => {
    await Tone.start();
    const synth = new Tone.PolySynth(Tone.Synth).toDestination();
    for (const chord of progression) {
      synth.triggerAttackRelease(chordNotes[chord], "1n");
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }
  };

  return (
    <div className="App">
      <h1>Next Chord Suggestor</h1>
      <input
        type="text"
        value={inputChords}
        onChange={(e) => setInputChords(e.target.value)}
        placeholder="Enter chords (e.g., C, G, Am)"
      />
      <button onClick={() => inputChords.split(",").map((chord) => addChordToProgression(chord.trim()))}>
        Add Chords
      </button>
      <div>
        <h3>Chord Progression:</h3>
        {progression.length ? progression.join(" → ") : "No chords yet."}
      </div>
      {suggestedChord && (
        <div>
          <h3>Suggested Chord:</h3>
          <p>
            {suggestedChord} (Probability: {probability * 100}%)
          </p>
          <button onClick={() => addChordToProgression(suggestedChord)}>Add Suggested Chord</button>
        </div>
      )}
      <button onClick={deleteLastChord}>Remove Last Chord</button>
      <button onClick={playProgression}>Play Progression</button>
    </div>
  );
};

export default App;
