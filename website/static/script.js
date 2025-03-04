// Script to initialise Google Map

function initMap() {
    // Center the map on Dublin
    const dublin = { lat: 53.349805, lng: -6.26031 };

    // Custom map styles to hide all labels except road names
    const mapStyles = [
        {
            featureType: "all",
            elementType: "labels",
            stylers: [{ visibility: "off" }], // Turn off all labels
        },
        {
            featureType: "road",
            elementType: "labels",
            stylers: [{ visibility: "on" }], // Turn on road labels
        },
        {
            featureType: "water",
            elementType: "geometry",
            stylers: [{ color: "#a2daf2" }], // Light blue for water
        },
        {
            featureType: "landscape",
            elementType: "geometry",
            stylers: [{ color: "#f5f5f5" }], // Light gray for land
        },
        {
            featureType: "road",
            elementType: "geometry",
            stylers: [{ color: "#ffffff" }], // White for roads
        },
        {
            featureType: "poi", // Points of interest (e.g., parks, schools)
            elementType: "geometry",
            stylers: [{ color: "#e0f2e9" }], // Light green for parks
        },
        {
            featureType: "transit", // Public transit (e.g., train stations)
            elementType: "geometry",
            stylers: [{ color: "#d3d3d3" }], // Light gray for transit
        },
    ];

    // Create the map with custom styles
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: dublin,
        styles: mapStyles,
        mapTypeControl: false, // Removes the map type control
        streetViewControl: false, // Removes the street view control
    });
}