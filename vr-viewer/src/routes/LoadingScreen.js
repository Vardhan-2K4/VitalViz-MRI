import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/animations.css";
import "../styles/theme.css";

function LoadingScreen() {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => navigate("/home"), 2000);
    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div className="loading-container">
      <div className="loading-spinner"></div>
      <h2 className="loading-text">Loading 3D Health Viewer...</h2>
    </div>
  );
}

export default LoadingScreen;
