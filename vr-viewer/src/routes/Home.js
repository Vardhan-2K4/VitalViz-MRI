// File: src/routes/Home.js
import React from "react";
import Taskbar from "../components/Taskbar";
import "../styles/Home.css";
import { Player } from "@lottiefiles/react-lottie-player";
import vrBackground from "../assets/vr-background.json";

function Home() {
  return (
    <div className="home-container">
      <Taskbar />

      <div className="background-animation">
        <Player
          autoplay
          loop
          src={vrBackground}
          style={{
            height: "100vh",
            width: "100%",
            position: "absolute",
            top: 0,
            left: 0,
            zIndex: 0,
          }}
        />
      </div>

      <div className="main-content">
        <div className="hero">
          <h1>Welcome to VR Health Viewer</h1>
          <p>Choose any feature from the taskbar to begin your journey.<br/>
          Look 12 o clock, once you see it you can't unsee it.
          </p>
        </div>

        <div className="about-section">
          <div className="about-card">
            <h2>About</h2>
            <p>
              We present to you an interactive 3D model which can be experienced using VR.<br/>
              The algorithm we used has a given models with mesh quality of mean = 0.69.<br/>
              To run VR we used- geometry processing, camera initialization, render creation, lighting,e.t.c.

            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;
