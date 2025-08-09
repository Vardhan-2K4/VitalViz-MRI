import React from "react";
import { Routes, Route } from "react-router-dom";

import Home from "./routes/Home";
import UploadPage from "./routes/UploadPage";
import ViewSelector from "./viewers/ViewSelectorWrapper";
import ThreeViewer3D from "./viewers/ThreeViewer3DWrapper";
import ThreeViewerVR from "./viewers/ThreeViewerVRWrapper";
import Demo from "./routes/Demo"; //  Import Demo component
import Chatbot from "./routes/chatbot";
function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/home" element={<Home />} />
      <Route path="/upload" element={<UploadPage />} />
      <Route path="/demo" element={<Demo />} /> {/*  Demo route added */}
      <Route path="/view-selector" element={<ViewSelector />} />
      <Route path="/viewer-3d" element={<ThreeViewer3D />} />
      <Route path="/viewer-vr" element={<ThreeViewerVR />} />
      <Route path="/chatbot" element={<Chatbot />} />
    </Routes>
  );
}

export default AppRoutes;
