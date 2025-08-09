# AquaRing
Developing and Visualizing medical modalities in a 3D version so that we can view them and analyze them

# 🧠 VR Health Viewer

**VR Health Viewer** is a full-stack web application that enables immersive 3D visualization of medical brain models (.nii files) using both traditional and VR (stereoscopic) viewing modes. The application supports gesture-based interaction using MediaPipe and enables real-time processing through a Flask backend.

---

## 🚀 Features

- Upload `.nii` brain MRI files
- Convert `.nii` to `.ply` 3D mesh using PyVista and medical image processing libraries
- View 3D model in browser using Three.js
- Switch between **3D Viewer** and **VR Viewer** modes
- Gesture-based model control (move, rotate, click, scroll)
- Flask + Socket.IO backend for real-time updates
- Clean UI with a cyan gradient theme
- Supports demo models and extensibility for future AI-based `.nii` generation

---

## 🧩 Tech Stack

**Frontend:**
- React.js
- Three.js
- React Router
- Custom CSS (Cyan theme)

**Backend:**
- Flask
- Flask-SocketIO + Eventlet
- MediaPipe, OpenCV
- nibabel, nilearn, pyvista, scikit-image

---

## 📁 Project Structure

vr-health-viewer/
├── backend/
│ ├── app_server.py # Flask server
│ ├── virtual_mouse.py # Gesture-based mouse control
│ ├── nii_to_ply_converter.py # NIfTI to PLY conversion
│ └── uploads/ # Uploaded files
├── frontend/
│ └── src/
│ ├── App.js
│ ├── AppRoutes.js
│ ├── viewers/
│ │ ├── ThreeViewer3D.js
│ │ └── ThreeViewerVR.js
│ ├── components/
│ │ ├── Taskbar.js
│ │ └── Dropdown.js
│ ├── styles/
│ │ ├── theme.css
│ │ └── Home.css
│ └── ViewSelector.js
└── requirements.txt

    
