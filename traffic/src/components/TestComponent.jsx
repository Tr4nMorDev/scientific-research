import { useState } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polyline,
} from "react-leaflet";

const TestComponent = () => {
  const [polylineCoords, setPolylineCoords] = useState([]); // Thêm useState để lưu tọa độ Polyline

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

      // Chuyển đổi từ [lng, lat] -> [lat, lng] để dùng với Leaflet
      const formattedCoordinates = coordinates.map((coord) => [
        coord[1],
        coord[0],
      ]);

      console.log("Tọa độ Polyline:", formattedCoordinates);

      setPolylineCoords(formattedCoordinates); // Cập nhật tọa độ Polyline
    } catch (error) {
      console.error("Lỗi khi gọi API OSRM:", error);
    }
  };

  return (
    <div>
      <button onClick={loadRoutes}>Tải tuyến đường</button>

      <MapContainer
        center={[10.80415, 106.68687]}
        zoom={14}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

        {polylineCoords.length > 0 && (
          <Polyline positions={polylineCoords} color="red" />
        )}
      </MapContainer>
    </div>
  );
};

export default TestComponent;
