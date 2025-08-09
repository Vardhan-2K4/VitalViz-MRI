// File: src/routes/Demo.js
import React from "react";
import { useNavigate } from "react-router-dom";
import Taskbar from "../components/Taskbar";
import ViewSelector from "../viewers/ViewSelector"; // Reuse existing selector
import testModel from "../assets/test.ply"; // Imported model path

function Demo() {
  const navigate = useNavigate();

  const handleSelectMode = (mode) => {
    const viewerRoute = mode === "VR" ? "/viewer-vr" : "/viewer-3d";
    navigate(viewerRoute, { state: { plyUrl: testModel } });
  };

  return (
    <div style={{ height: "100vh", background: "#000" }}>
      <Taskbar />
      <div style={{ marginTop: "4rem" }}>
        <ViewSelector onSelectMode={handleSelectMode} />
      </div>
    </div>
  );
}

export default Demo;
