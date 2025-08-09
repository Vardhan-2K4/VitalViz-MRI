// File: src/components/Taskbar.js
import React, { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./Taskbar.css";

function Taskbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    setVisible(true);
  }, []);

  const isActive = (path) => location.pathname === path;

  return (
    <div className={`taskbar-container ${visible ? "fade-in" : ""}`}>
      <div className="taskbar-inner">
        <h3 className="taskbar-logo" onClick={() => navigate("/home")}>
          BrainVR
        </h3>
        <div className="taskbar-nav">
          <button
            className={`taskbar-button ${isActive("/home") ? "active" : ""}`}
            onClick={() => navigate("/home")}
          >
            Home
          </button>
          <button
            className={`taskbar-button ${isActive("/demo") ? "active" : ""}`}
            onClick={() => navigate("/demo")}
          >
            Demo
          </button>
          <button
            className={`taskbar-button ${isActive("/upload") ? "active" : ""}`}
            onClick={() => navigate("/upload")}
          >
            Model
          </button>
          <button
            className={`taskbar-button ${isActive("/chatbot") ? "active" : ""}`}
            onClick={() => navigate("/chatbot")}
          >
            Chatbot
          </button>
        </div>
      </div>
    </div>
  );
}

export default Taskbar;
