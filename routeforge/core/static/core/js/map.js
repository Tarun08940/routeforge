const map = L.map("map").setView([12.9716, 77.5946], 10);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
}).addTo(map);

let pickupMarker = null;
let dropMarker = null;

map.on("click", async (e) => {
  if (!pickupMarker) {
    pickupMarker = L.marker(e.latlng).addTo(map).bindPopup("Pickup").openPopup();
  } else if (!dropMarker) {
    dropMarker = L.marker(e.latlng).addTo(map).bindPopup("Drop").openPopup();

    const res = await fetch("/api/route", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        pickup: pickupMarker.getLatLng(),
        drop: dropMarker.getLatLng(),
      }),
    });

    const data = await res.json();
    document.getElementById("result").innerText =
      `Distance: ${data.distance_km} km | ETA: ${data.estimated_time_min} min`;
  }
});
