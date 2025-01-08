const osm = "https://www.openstreetmap.org/copyright";
const copy = `© <a href='${osm}'>OpenStreetMap</a>`;
const url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
const layer = L.tileLayer(url, { attribution: copy });
const map = L.map("map", { layers: [layer] });
map.fitWorld();
map.setView([50, 15], 5)
map.addControl(new L.Control.Fullscreen());

const customIcon = (color) => {
    return L.icon({
        iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-${color}.png`,
        iconSize: [25, 41], // size of the icon
        iconAnchor: [12, 41], // point of the icon which will correspond to marker's location
        popupAnchor: [1, -34], // point from which the popup should open relative to the iconAnchor
        shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
        shadowSize: [41, 41], // size of the shadow
    });
};

if (typeof markerData !== "undefined") {
    Object.entries(markerData).forEach(([key, value]) => {
        const marker = L.marker([value.latitude, value.longitude], { icon: customIcon("violet") }).addTo(map);
        marker.bindPopup(
            `<div class="custom-popup">
                <h3>${key}</h3>
                <p>${value.popup_message}</p>
                <p><a href="${value.profile}" rel="noopener noreferrer">Visit Profile</a></p>
            </div>`, { className: 'popup-styled' });
    });
}