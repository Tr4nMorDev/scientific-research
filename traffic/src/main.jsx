import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import "./index.css";
import App from "./App.jsx";
import TestComponent from "./components/TestComponent";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/map" element={<App />} />
        <Route path="/" element={<Navigate to="/map" replace />} />
        <Route path="/test" element={<TestComponent />} />
      </Routes>
    </Router>
  </StrictMode>
);
