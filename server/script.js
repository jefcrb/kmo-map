const startLat = 51.229926952938165;
const startLon = 4.417909787251215;
const radiusInKm = 0.3;

var map = L.map('map').setView([startLat, startLon], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

L.marker([startLat, startLon])
    .addTo(map)
    .bindPopup("Center Point")
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

// Mapping of contact types to user-friendly labels
var contactLabels = {
    'TEL': 'Telephone',
    'EMAIL': 'Email',
    // Add other mappings if necessary
};

// Fetch data from data.json
fetch('data.json')
    .then(response => response.json())
    .then(data => {
        data.forEach(entry => {
            // Extract latitude and longitude
            var lat = entry.Latitude;
            var lon = entry.Longitude;

            // Calculate distance from the given point
            var distance = calculateDistance(startLat, startLon, lat, lon);

            // If the distance is within the specified radius, add the marker
            if (distance <= radiusInKm) {
                // Create a marker
                var marker = L.marker([lat, lon]).addTo(map);

                // Build the contact information
                var contactInfo = '';
                if (entry.Contacts) {
                    for (var contactType in entry.Contacts) {
                        var label = contactLabels[contactType] || contactType;
                        contactInfo += `<strong>${label}:</strong> ${entry.Contacts[contactType]}<br/>`;
                    }
                } else {
                    contactInfo = 'No contact information available.<br/>';
                }

                // Create a popup with extra information
                var popupContent = `
                    <strong>${entry.Denomination}</strong><br/>
                    Address: ${entry.FullAddress}<br/>
                    ${contactInfo}
                    Entity Number: ${entry.EntityNumber}
                `;

                marker.bindPopup(popupContent);
            }
        });
    })
    .catch(error => console.error('Error loading the data:', error));
