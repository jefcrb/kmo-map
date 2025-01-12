const startLat = 51.229926952938165;
const startLon = 4.417909787251215;
const radiusInKm = 0.3;

var map = L.map('map').setView([startLat, startLon], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

L.marker([startLat, startLon])
    .addTo(map)
    .bindPopup("Center")
    .openPopup();

function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const distance = R * c;
    return distance;
}

var contactLabels = {
    'TEL': 'Telephone',
    'EMAIL': 'Email',
};

fetch('data.json')
    .then(response => response.json())
    .then(data => {
        data.forEach(entry => {
            var lat = entry.Latitude;
            var lon = entry.Longitude;

            var distance = calculateDistance(startLat, startLon, lat, lon);

            if (distance <= radiusInKm) {
                var marker = L.marker([lat, lon]).addTo(map);

                var contactInfo = '';
                if (entry.Contacts) {
                    for (var contactType in entry.Contacts) {
                        var label = contactLabels[contactType] || contactType;
                        contactInfo += `<strong>${label}:</strong> ${entry.Contacts[contactType]}<br/>`;
                    }
                } else {
                    contactInfo = 'Geen contactinformatie<br/>';
                }

                var popupContent = `
                    <strong>${entry.Denomination}</strong><br/>
                    Adres: ${entry.FullAddress}<br/>
                    ${contactInfo}<br/>
                    Entity Number: ${entry.EntityNumber}<br/>
                    Omzet: ${entry.omzet}
                `;

                marker.bindPopup(popupContent);
            }
        });
    })
    .catch(error => console.error('Fout:', error));
