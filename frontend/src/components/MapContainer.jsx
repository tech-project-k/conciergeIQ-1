import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from 'react-leaflet';
import L from 'leaflet';

// Fix Leaflet marker icons using a premium custom HTML/CSS indicator
const createCustomIcon = (type, dayNumber) => {
  const emojis = {
    hotel: "🏨",
    breakfast: "🥞",
    lunch: "🥪",
    dinner: "🍽️",
    museum: "🏛️",
    attraction: "📍",
    coffee: "☕",
    transit: "🚌",
    rest: "🛋️"
  };
  const emoji = emojis[type.toLowerCase()] || "📍";
  
  return L.divIcon({
    html: `
      <div class="relative flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-tr from-violet-600 to-indigo-600 text-sm shadow-lg border border-white/20 select-none">
        <span class="absolute -top-2 -right-2 bg-fuchsia-600 text-white rounded-full text-[10px] w-4 h-4 flex items-center justify-center font-bold">${dayNumber}</span>
        ${emoji}
      </div>
    `,
    className: 'custom-map-marker',
    iconSize: [32, 32],
    iconAnchor: [16, 16],
    popupAnchor: [0, -16]
  });
};

// Sub-component to fit map bounds automatically
function RecenterMap({ coords }) {
  const map = useMap();
  useEffect(() => {
    if (coords && coords.length > 0) {
      const bounds = L.latLngBounds(coords.map(c => [c.lat, c.lon]));
      map.fitBounds(bounds, { padding: [50, 50], maxZoom: 14, animate: true });
    }
  }, [coords, map]);
  return null;
}

export default function CustomMapContainer({ activities }) {
  // Filter activities that have valid latitude & longitude coordinates
  const validLocations = activities
    .filter(act => act.latitude !== null && act.longitude !== null)
    .map(act => ({
      id: act.id,
      name: act.name,
      type: act.type,
      day: act.day_number,
      time: act.start_time,
      address: act.address,
      lat: act.latitude,
      lon: act.longitude
    }));

  const center = validLocations.length > 0 
    ? [validLocations[0].lat, validLocations[0].lon]
    : [48.8566, 2.3522]; // Paris default

  // Compute travel polyline paths connecting sequential points
  const polylinePositions = validLocations.map(loc => [loc.lat, loc.lon]);

  return (
    <div className="w-full h-full min-h-[400px] bg-[#0b0f19] rounded-3xl overflow-hidden border border-gray-900 shadow-inner relative z-10">
      {validLocations.length === 0 ? (
        <div className="absolute inset-0 flex items-center justify-center text-gray-500 text-sm p-6 text-center">
          No map locations found. Plan a trip or add activities to visualize your route.
        </div>
      ) : (
        <MapContainer
          center={center}
          zoom={12}
          scrollWheelZoom={true}
          style={{ width: '100%', height: '100%' }}
        >
          {/* Dark Mode styled OpenStreetMap layer */}
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          
          {validLocations.map((loc, idx) => (
            <Marker
              key={loc.id || idx}
              position={[loc.lat, loc.lon]}
              icon={createCustomIcon(loc.type, loc.day)}
            >
              <Popup>
                <div className="text-slate-900 font-sans p-1">
                  <div className="font-bold text-sm text-violet-700">{loc.name}</div>
                  <div className="text-xs text-gray-500 mt-0.5">Day {loc.day} • {loc.time}</div>
                  {loc.address && <div className="text-[11px] text-gray-700 mt-1 border-t pt-1">{loc.address}</div>}
                </div>
              </Popup>
            </Marker>
          ))}

          {polylinePositions.length > 1 && (
            <Polyline
              positions={polylinePositions}
              color="#8b5cf6"
              weight={3}
              opacity={0.7}
              dashArray="5, 10"
            />
          )}

          <RecenterMap coords={validLocations} />
        </MapContainer>
      )}
    </div>
  );
}
