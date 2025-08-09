// File: src/viewers/ViewSelector.js
import React from "react";
import { Player } from "@lottiefiles/react-lottie-player";
import viewselector from "../assets/viewselector.json"; // make sure this path is correct

function ViewSelector({ onSelectMode }) {
  return (
    <div style={{ position: "relative", minHeight: "100vh", background: "#111", color: "#fff" }}>
      {/* Lottie animation background */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          height: "100vh",
          width: "100%",
          backgroundColor: "#000",
          zIndex: 0,
        }}
      >
        <Player
          autoplay
          loop
          src={viewselector}
          style={{
            height: "100vh",
            width: "100%",
            position: "absolute",
            top: 0,
            left: 0,
          }}
        />
      </div>

      {/* Optional dark overlay */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          height: "100vh",
          width: "100%",
          background: "rgba(0, 0, 0, 0.4)",
          zIndex: 1,
        }}
      />

      {/* Foreground content */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
          zIndex: 2,
          position: "relative",
          textAlign: "center",
          padding: "2rem",
        }}
      >
        <h2 style={{ color: "#fff", marginBottom: "1rem" }}>Select View Mode</h2>
        <button onClick={() => onSelectMode("3D")} style={buttonStyle}>
          View in 3D
        </button>
        <button onClick={() => onSelectMode("VR")} style={buttonStyle}>
          View in VR
        </button>
      </div>
    </div>
  );
}

const buttonStyle = {
  padding: "0.6rem 1.2rem",
  margin: "0.5rem",
  background: "#1a1a1a",
  border: "1px solid #777",
  borderRadius: "8px",
  color: "#f0f0f0",
  cursor: "pointer",
};

export default ViewSelector;
