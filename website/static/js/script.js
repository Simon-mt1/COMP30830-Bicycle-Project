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
  const sidebarImage = document.querySelector(".sidebar-image");

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
      // place = fetchPlaces(data["address"]);
      // sidebarImage.src = "";
      sidebarImage.alt = "";
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

const fetchPlaces = async (place) => {
  const url = "https://places.googleapis.com/v1/places:searchText";
  const apiKey = "AIzaSyAaGUqWCizTD4mPtHVbu6okPQ2KiCx-mEk";

  const headers = {
    "X-Goog-Api-Key": apiKey,
    "X-Goog-FieldMask":
      "places.displayName,places.formattedAddress,places.id,places.name",
    "Content-Type": "application/json",
  };

  const body = JSON.stringify({
    textQuery: place + " dublin bikes",
  });

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: headers,
      body: body,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    placeDetail = fetchPlaceDetails(data);
  } catch (error) {
    console.error("Error fetching places:", error);
    return null;
  }
};

const fetchPlaceDetails = async (place) => {
  const url = "https://places.googleapis.com/v1/" + place["places"][0]["name"];
  const apiKey = "AIzaSyAaGUqWCizTD4mPtHVbu6okPQ2KiCx-mEk";

  const headers = {
    "X-Goog-Api-Key": apiKey,
    "X-Goog-FieldMask": "id,displayName,name,photos",
    "Content-Type": "application/json",
  };

  try {
    const response = await fetch(url, {
      method: "GET",
      headers: headers,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    fetchPhoto(data);
  } catch (error) {
    console.error("Error fetching place details:", error);
    return null;
  }
};

const fetchPhoto = async (place) => {
  const params = {
    maxHeightPx: 400,
    maxWidthPx: 400,
    apiKey: "AIzaSyAaGUqWCizTD4mPtHVbu6okPQ2KiCx-mEk", // You can pass the API key in headers if needed
  };

  const url =
    "https://places.googleapis.com/v1/" +
    place["photos"][0]["name"] +
    "/media" +
    "?maxHeightPx=" +
    params.maxHeightPx +
    "&maxWidthPx=" +
    params.maxWidthPx +
    "&key=" +
    params.apiKey;

  try {
    const response = await fetch(url, {
      method: "GET",
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const imageUrl = await response.url;

    sideBarImage = document.querySelector(".sidebar-image");

    sideBarImage.src = imageUrl;
    sideBarImage.alt = "Google Place Photo";
  } catch (error) {
    console.error("Error fetching photo:", error);
  }
};
