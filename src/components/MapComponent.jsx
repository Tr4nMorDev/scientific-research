import { useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import CameraPopup from "./CameraPopup";

const cameraLocations = [
  {
    name: "Camera 1",
    position: [10.7905, 106.7009],
    description: "Camera tại Quận 1",
    videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
  },
  {
    name: "Camera 2",
    position: [10.762622, 106.660172],
    description: "Camera tại Quận 3",
    videoUrl: "https://www.w3schools.com/html/movie.mp4",
  },
  {
    name: "Camera 3",
    position: [10.8231, 106.6297],
    description: "Camera tại Gò Vấp",
    videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
  },
  {
    name: "Camera 4",
    position: [10.7769, 106.7009],
    description: "Camera tại Quận 10",
    videoUrl: "https://www.w3schools.com/html/movie.mp4",
  },
];

const MapComponent = () => {
  const [selectedCamera, setSelectedCamera] = useState(null);

  const handleCameraClick = (camera) => {
    setSelectedCamera(camera);
  };

  const handleClose = () => {
    setSelectedCamera(null);
  };

  return (
    <div className="h-screen w-screen relative">
      <MapContainer
        center={[10.801233, 106.711221]}
        zoom={30}
        scrollWheelZoom={true}
        className="h-full w-full z-10"
      >
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {cameraLocations.map((camera, index) => (
          <Marker
            key={index}
            position={camera.position}
            eventHandlers={{
              click: () => handleCameraClick(camera),
            }}
          >
            <Popup>
              <b>{camera.name}</b>
              <br />
              {camera.description}
            </Popup>
          </Marker>
        ))}
      </MapContainer>

      {selectedCamera && (
        <CameraPopup camera={selectedCamera} onClose={handleClose} />
      )}
    </div>
  );
};

export default MapComponent;
