// File: src/routes/UploadPage.js
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Player } from "@lottiefiles/react-lottie-player";
import uploadfilesbackground from "../assets/uploadfilesbackground.json";

const FLASK_URL = "http://10.1.5.50:5000";

function UploadPage() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a NIfTI (.nii) file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    setUploading(true);

    console.log(`Uploading file to Flask backend at: ${FLASK_URL}/upload`);

    try {
      const response = await axios.post(`${FLASK_URL}/upload`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        withCredentials: false,
      });

      const { model_url } = response.data;
      const fullUrl = `${FLASK_URL}${model_url}`;
      console.log("Upload successful. Model URL:", fullUrl);
      navigate("/view-selector", { state: { plyUrl: fullUrl } });
    } catch (error) {
      console.error("Upload failed:", error);
      if (error.response) {
        console.error("Server responded with:", error.response.data);
        alert(`Upload failed: ${error.response.data.error || 'Unknown server error'}`);
      } else if (error.request) {
        console.error("No response received:", error.request);
        alert("Upload failed: No response from server.");
      } else {
        alert(`Upload failed: ${error.message}`);
      }
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={{ position: "relative", minHeight: "100vh", background: "#111", color: "#fff" }}>
      {/* Background Animation */}
      <div style={{ position: "absolute", top: 0, left: 0, height: "100vh", width: "100%", backgroundColor: "#000", zIndex: 0 }}>
        <Player
          autoplay
          loop
          src={uploadfilesbackground}
          style={{
            height: "100vh",
            width: "100%",
            position: "absolute",
            top: 0,
            left: 0,
          }}
        />
      </div>

      {/* Optional Dark Overlay for Contrast */}
      <div style={{
        position: "absolute",
        top: 0,
        left: 0,
        height: "100vh",
        width: "100%",
        background: "rgba(0, 0, 0, 0.4)",
        zIndex: 1,
      }} />

      {/* Upload UI */}
      <div style={{ position: "relative", zIndex: 2, padding: "2rem", textAlign: "center" }}>
        <h2>Upload a Brain MRI (.nii) File</h2>
        <input type="file" accept=".nii,.nii.gz" onChange={handleFileChange} style={{ margin: "1rem 0" }} />
        <br />
        <button
          onClick={handleUpload}
          disabled={uploading}
          style={{
            padding: "0.6rem 1.2rem",
            background: "#1a1a1a",
            border: "1px solid #777",
            borderRadius: "8px",
            color: "#f0f0f0",
            cursor: "pointer",
          }}
        >
          {uploading ? "Uploading..." : "Upload and Proceed"}
        </button>
      </div>
    </div>
  );
}

export default UploadPage;
