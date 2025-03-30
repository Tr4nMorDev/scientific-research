import { useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import CameraPopup from "./CameraPopup";
import { Polyline } from "react-leaflet";
const cameraLinks = [
  {
    from: "Camera 1",
    to: "Camera 2",
    positions: [
      [10.80415, 106.68687],
      [10.81118, 106.69085],
    ],
  },
  {
    from: "Camera 2",
    to: "Camera 3",
    positions: [
      [10.81118, 106.69085],
      [10.8083, 106.69523],
    ],
  },
  {
    from: "Camera 3",
    to: "Camera 4",
    positions: [
      [10.8083, 106.69523],
      [10.80273, 106.69455],
    ],
  },
];
const cameraLocations = [
  {
    name: "Camera 1",
    position: [10.80415, 106.68687],
    description: "Camera tại Quận 1",
    videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
  },
  {
    name: "Camera 2",
    position: [10.811321328642983, 106.69108933129165],
    description: "Camera tại Quận 3",
    videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
  },
  {
    name: "Camera 3",
    position: [10.8083, 106.69523],
    description: "Camera tại Gò Vấp",
    videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
  },
  {
    name: "Camera 4",
    position: [10.803012267360623, 106.69505443969877],
    description: "Camera tại Quận 10",
    videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
  },
  {
    name: "Camera 5",
    position: [10.803179966268125, 106.69333118776957],
    description: "Camera tại Quận 3",
    videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
  },
  {
    name: "Camera 6",
    position: [10.79878, 106.68028],
    description: "Camera tại Gò Vấp",
    videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
  },
  {
    name: "Camera 7",
    position: [10.79756, 106.69085],
    description: "Camera tại Quận 10",
    videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
  },
  {
    name: "Camera 8",
    position: [10.802793633147768, 106.69653483926268],
    description: "Camera tại Quận 3",
    videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
  },
  {
    name: "Camera 9",
    position: [10.80285477812132, 106.69857770987298],
    description: "Camera tại Gò Vấp",
    videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
  },
  {
    name: "Camera 10",
    position: [10.81122, 10669507],
    description: "Camera tại Quận 10",
    videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
  },
  {
    name: "Camera 11",
    position: [10.803295446077314, 106.69247698546036],
    description: "Camera tại Quận 10",
    videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
  },
  {
    name: "Camera 12",
    position: [10.80831511002866, 106.68823092353945],
    description: "Camera tại Quận 10",
    videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4",
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
