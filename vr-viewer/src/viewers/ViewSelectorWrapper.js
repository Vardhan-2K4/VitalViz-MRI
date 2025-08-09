import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import ViewSelector from "./ViewSelector";

function ViewSelectorWrapper() {
  const navigate = useNavigate();
  const location = useLocation();
  const { plyUrl } = location.state || {};

  const handleSelectMode = (mode) => {
    if (!plyUrl) {
      alert("No model found. Please upload a file first.");
      return;
    }
    if (mode === "3D") {
      navigate("/viewer-3d", { state: { plyUrl } });
    } else if (mode === "VR") {
      navigate("/viewer-vr", { state: { plyUrl } });
    }
  };

  return <ViewSelector onSelectMode={handleSelectMode} />;
}

export default ViewSelectorWrapper;
