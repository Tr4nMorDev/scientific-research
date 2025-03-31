import { useState, useEffect } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polyline,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";

const TestComponent = () => {
  const [polylineCoords, setPolylineCoords] = useState([]);
  const [map, setMap] = useState(null);

  const mapStyle = {
    width: "100%",
    height: "600px",
    margin: "20px 0",
  };

  useEffect(() => {
    if (map) {
      map.invalidateSize();
    }
  }, [map]);

  const loadRoutes = async () => {
    try {
      const response = await fetch(
        "http://router.project-osrm.org/route/v1/driving/106.68687,10.80415;106.69085,10.81118?overview=full&geometries=geojson"
      );
      const data = await response.json();

      console.log("OSRM Response:", data);

      if (!data.routes || data.routes.length === 0) {
        console.error("Không tìm thấy tuyến đường nào!");
        return;
      }

      const coordinates = data.routes[0]?.geometry?.coordinates || [];

      if (coordinates.length === 0) {
        console.error("Không có tọa độ đường!");
        return;
      }

      const formattedCoordinates = coordinates.map((coord) => [
        coord[1],
        coord[0],
      ]);

      console.log("Tọa độ Polyline:", formattedCoordinates);

      setPolylineCoords(formattedCoordinates);

      if (map && formattedCoordinates.length > 0) {
        map.fitBounds(formattedCoordinates);
      }
    } catch (error) {
      console.error("Lỗi khi gọi API OSRM:", error);
    }
  };

  return (
    <div>
      <button onClick={loadRoutes}>Tải tuyến đường</button>

      <div style={mapStyle}>
        <MapContainer
          center={[10.80415, 106.68687]}
          zoom={14}
          style={{ height: "100%", width: "100%" }}
          whenCreated={setMap}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          <Marker position={[10.80415, 106.68687]}>
            <Popup>Điểm bắt đầu</Popup>
          </Marker>

          <Marker position={[10.81118, 106.69085]}>
            <Popup>Điểm kết thúc</Popup>
          </Marker>

          {polylineCoords.length > 0 && (
            <Polyline positions={polylineCoords} color="red" />
          )}
        </MapContainer>
      </div>
    </div>
  );
};

export default TestComponent;
