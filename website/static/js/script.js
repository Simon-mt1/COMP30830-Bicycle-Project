// Script to initialise Google Map

let value = "available_bikes";

function handleButtonClick(event) {
  if (event.target.innerHTML === "Available Bikes") {
    value = "available_bikes";
  } else {
    value = "available_bike_stands";
  }

  const list = document.querySelectorAll(".map-button");

  for (let object of list) {
    object.classList.toggle("disabled");
    if (object.disabled == true) {
      object.disabled = false;
    } else {
      object.disabled = true;
    }
  }

  initMap();
}

async function initMap() {
  // Center the map on Dublin
  const dublin = { lat: 53.349805, lng: -6.26031 };
  const sidebar = document.querySelector(".sidebar");
  const closeButton = document.querySelector(".close-button");
  const sidebarheading = document.querySelector(".heading");
  const bikesNumber = document.querySelector(".bikes-number");
  const spacesNumber = document.querySelector(".spaces-number");

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

  const markers = [];
  for (let data of mapData) {
    const marker = new google.maps.Marker({
      position: { lat: data["position"]["lat"], lng: data["position"]["lng"] },
      map: map,
      title: data["address"],
      label: {
        text: `${data[value]}`,
        color: "#ffffff",
        fontSize: "14px",
        fontWeight: "bold",
      },
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 17,
        fillColor: "#ff5733",
        fillOpacity: 1,
        strokeWeight: 2,
        strokeColor: "#ffffff",
      },
    });

    marker.addListener("click", () => {
      map.panTo(marker.getPosition());
      sidebarheading.innerText = data["address"];
      bikesNumber.innerText = data["available_bikes"];
      spacesNumber.innerText = data["available_bike_stands"] + " P";
      setTimeout(() => {
        sidebar.classList.add("open");
        map.setZoom(16);
      }, 300);
    });

    closeButton.addEventListener("click", () => {
      sidebar.classList.remove("open");
    });

    markers.push(marker);
  }
}
