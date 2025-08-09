// File: ThreeViewer3D.js
import React, { useEffect, useRef } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { PLYLoader } from "three/examples/jsm/loaders/PLYLoader";
import axios from "axios";  // Added for backend control

function ThreeViewer3D({ plyUrl }) {
  const containerRef = useRef();

  useEffect(() => {
    // Start gesture control on mount
    axios.post("http://10.1.5.50:5000/start-virtual-mouse").catch(console.error);

    const container = containerRef.current;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000000);

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 1, 1000);
    camera.position.set(0, 0, 100);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.rotateSpeed = 0.4;
    controls.zoomSpeed = 0.6;
    controls.enablePan = false;

    scene.add(new THREE.AmbientLight(0xffffff, 1.2));
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(50, 50, 50);
    scene.add(directionalLight);

    const loader = new PLYLoader();
    loader.load(
      plyUrl,
      (geometry) => {
        geometry.computeVertexNormals();
        geometry.center();

        geometry.computeBoundingBox();
        const size = new THREE.Vector3();
        geometry.boundingBox.getSize(size);
        const maxAxis = Math.max(size.x, size.y, size.z);
        geometry.scale(50 / maxAxis, 50 / maxAxis, 50 / maxAxis);

        const hasColor = geometry.hasAttribute("color");
        if (!hasColor) {
          const position = geometry.attributes.position;
          const colors = [];
          let minY = Infinity;
          let maxY = -Infinity;

          for (let i = 0; i < position.count; i++) {
            const y = position.getY(i);
            minY = Math.min(minY, y);
            maxY = Math.max(maxY, y);
          }

          for (let i = 0; i < position.count; i++) {
            const y = position.getY(i);
            const t = (y - minY) / (maxY - minY);
            const r = 1.0 * t;
            const g = 0.6 * (1 - t);
            const b = 0.6 + 0.4 * t;
            colors.push(r, g, b);
          }

          geometry.setAttribute("color", new THREE.Float32BufferAttribute(colors, 3));
        }

        const material = new THREE.MeshStandardMaterial({
          vertexColors: true,
          metalness: 0.1,
          roughness: 0.6,
          flatShading: true,
          side: THREE.DoubleSide,
        });

        const mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);
      },
      undefined,
      (error) => console.error("Error loading PLY:", error)
    );

    const animate = () => {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    const handleResize = () => {
      const width = container.clientWidth;
      const height = container.clientHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    };

    window.addEventListener("resize", handleResize);

    return () => {
      // Stop gesture control on unmount
      axios.post("http://10.1.5.50:5000/stop-virtual-mouse").catch(console.error);

      window.removeEventListener("resize", handleResize);
      container.removeChild(renderer.domElement);
      renderer.dispose();
    };
  }, [plyUrl]);

  return (
    <div
      ref={containerRef}
      style={{
        width: "100%",
        height: "100%",
        borderRadius: "12px",
        overflow: "hidden",
      }}
    />
  );
}

export default ThreeViewer3D;
