import React from "react";
import MapComponent from "./components/MapComponent";
import LeftBar from "./components/LeftBar";
import BottomBar from "./components/BottomBar";
import "./App.css";

function App() {
  return (
    <div className="relative w-screen h-screen overflow-hidden">
      <LeftBar />
      <BottomBar />
      <div className="absolute inset-0">
        <MapComponent />
      </div>
    </div>
  );
}

export default App;
