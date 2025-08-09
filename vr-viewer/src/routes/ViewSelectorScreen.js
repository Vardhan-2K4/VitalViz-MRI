import React from "react";
import { useNavigate } from "react-router-dom";
import ViewSelector from "../viewers/ViewSelector";

const ViewSelectorScreen = () => {
  const navigate = useNavigate();

  const handleSelectMode = (mode) => {
    if (mode === "3D") {
      navigate("/viewer-3d");
    } else if (mode === "VR") {
      navigate("/viewer-vr");
    }
  };

  return (
    <div style={{ padding: "2rem", textAlign: "center" }}>
      <h1 style={{ color: "#0ff" }}>Choose Model Viewing Mode</h1>
      <ViewSelector onSelectMode={handleSelectMode} />
    </div>
  );
};

export default ViewSelectorScreen;
