import React from "react";
import { Link } from "react-router-dom";
import "../styles/theme.css";

function Dropdown({ label, options }) {
  return (
    <div className="dropdown">
      <span className="taskbar-link">{label} ▾</span>
      <div className="dropdown-content">
        {options.map((opt, idx) => (
          <Link key={idx} to={opt.path} className="dropdown-item">{opt.name}</Link>
        ))}
      </div>
    </div>
  );
}

export default Dropdown;
