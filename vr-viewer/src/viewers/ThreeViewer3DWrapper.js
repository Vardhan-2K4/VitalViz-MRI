import React, { useRef } from "react";
import { useLocation } from "react-router-dom";
import ThreeViewer3D from "./ThreeViewer3D";

function ThreeViewer3DWrapper() {
  const { state } = useLocation();
  const { plyUrl } = state || {};
  const viewerRef = useRef();

  if (!plyUrl) return <p style={{ color: "#fff" }}>No model found. Please upload again.</p>;

  const enterFullScreen = () => {
    const elem = viewerRef.current;
    if (!elem) return;
    if (elem.requestFullscreen) elem.requestFullscreen();
    else if (elem.webkitRequestFullscreen) elem.webkitRequestFullscreen();
    else if (elem.msRequestFullscreen) elem.msRequestFullscreen();
  };

  return (
    <div style={{ width: "100vw", height: "100vh", background: "#000", position: "relative" }} ref={viewerRef}>
      <button
        onClick={enterFullScreen}
        style={{
          position: "absolute",
          top: "20px",
          right: "20px",
          zIndex: 10,
          padding: "0.5rem 1rem",
          background: "#111",
          color: "#fff",
          border: "1px solid #888",
          borderRadius: "8px",
          cursor: "pointer"
        }}
      >
        View in Fullscreen
      </button>
      <ThreeViewer3D plyUrl={plyUrl} />
    </div>
  );
}

export default ThreeViewer3DWrapper;
