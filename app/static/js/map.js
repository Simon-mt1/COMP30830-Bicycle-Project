/**
 * Main script for rendering a customized Google Map for Dublin Bikes.
 * Supports toggling between available bikes/spaces, fetching directions,
 * and displaying station info with predictions and images.
 *
 * @module map.js
 */

let value = "available_bikes"; // Current data value being rendered on the map
let rendered = false; // Flag to prevent re-attaching listeners
let directionsService;
let directionsRenderer;
let map;
let clickedLocation = null;

const dublin = { lat: 53.349805, lng: -6.26031 };
const sidebar = document.querySelector(".sidebar");
const closeButton = document.querySelector(".close-button");
const sidebarheading = document.querySelector(".heading");
const bikesNumber = document.querySelector(".bikes-number");
const sidebarImage = document.querySelector(".sidebar-image");
const directionButton = document.querySelector(".direction-button");
const mapbuttons = document.querySelectorAll(".map-button");
const backbutton = document.querySelector(".back-button");
const directionPanel = document.querySelector(".direction-panel");

let markers = [];

/**
 * Handles toggle buttons for switching between bikes/spaces view or navigating to the nearest station.
 * @function
 * @param {MouseEvent} event - The click event from the toggle buttons.
 */
const handleMapButtonClick = (event) => {
  if (event.target.innerHTML === "Available Bikes") {
    value = "available_bikes";
  } else if (event.target.innerHTML === "Available Spaces") {
    value = "available_bike_stands";
  } else {
    goToNearestStation(markers);
    return;
  }

  const list = document.querySelectorAll(".toggle-button");

  for (let object of list) {
    object.classList.toggle("disabled");
    object.disabled = !object.disabled;
  }

  initMap();
};

/**
 * Initializes and renders the map with markers, styles, and click behavior.
 * Sets up direction services and handles sidebar display and predictions.
 * @async
 * @function initMap
 */
async function initMap() {
  sidebar.classList.remove("open");

  if (!directionsService) {
    directionsService = new google.maps.DirectionsService();
  }
  if (!directionsRenderer) {
    directionsRenderer = new google.maps.DirectionsRenderer();
  } else {
    directionsRenderer.setMap(null);
    directionsRenderer.setDirections({ routes: [] });
  }

  const mapStyles = [
    {
      featureType: "all",
      elementType: "labels",
      stylers: [{ visibility: "off" }],
    },
    {
      featureType: "road",
      elementType: "labels",
      stylers: [{ visibility: "on" }],
    },
    {
      featureType: "water",
      elementType: "geometry",
      stylers: [{ color: "#a2daf2" }],
    },
    {
      featureType: "landscape",
      elementType: "geometry",
      stylers: [{ color: "#f5f5f5" }],
    },
    {
      featureType: "road",
      elementType: "geometry",
      stylers: [{ color: "#ffffff" }],
    },
    {
      featureType: "poi",
      elementType: "geometry",
      stylers: [{ color: "#e0f2e9" }],
    },
    {
      featureType: "transit",
      elementType: "geometry",
      stylers: [{ color: "#d3d3d3" }],
    },
  ];

  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 15,
    center: dublin,
    styles: mapStyles,
    mapTypeControl: false,
    streetViewControl: false,
  });

  const currentLocation = await retrieveLocation();

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
        fillColor: `${data[value] == 0 ? "red" : "green"}`,
        fillOpacity: 1,
        strokeWeight: 2,
        strokeColor: "#ffffff",
      },
    });

    marker.addListener("click", async () => {
      directionsRenderer.setMap(map);

      closeButton.disabled = false;
      closeButton.innerText = "<";
      closeButton.style.cursor = "pointer";

      map.panTo(marker.getPosition());
      sidebarheading.innerText = data["address"];
      bikesNumber.innerText = `${data["available_bikes"]} / ${data["bike_stands"]} bikes available`;

      place = await fetchPlaces(data["address"]);
      sidebarImage.src = "";
      sidebarImage.alt = "";

      const stationData = {
        number: data.number,
        bike_stands: data.available_bike_stands,
        lat: marker.getPosition().lat(),
        lon: marker.getPosition().lng(),
        capacity: data.bike_stands,
      };

      try {
        const response = await fetch("/predict", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(stationData),
        });

        const data = await response.json();
        drawAvailableBikesCharts(data.prediction.availableBikes);
        drawAvailableSpacesCharts(data.prediction.availableSpaces);
      } catch (error) {
        console.log(`Error: ${error}`);
      }

      setTimeout(() => {
        sidebar.classList.add("open");
        map.setZoom(16);
      }, 300);

      clickedLocation = {
        lat: data["position"]["lat"],
        lng: data["position"]["lng"],
      };
    });

    markers.push(marker);
  }

  if (!rendered) {
    directionButton.addEventListener("click", () => {
      for (let marker of markers) {
        marker.setMap(null);
      }
      markers = [];

      mapbuttons.forEach((item) => item.classList.toggle("display"));

      backbutton.classList.remove("display");
      closeButton.disabled = false;
      document.querySelector(".map-button-box").classList.add("hide");
      directionButton.style.cursor = "not-allowed";
      directionButton.disabled = !directionButton.disabled;

      const request = {
        origin: currentLocation,
        destination: clickedLocation,
        travelMode: google.maps.TravelMode.DRIVING,
      };

      directionsService.route(request, (result, status) => {
        if (status == google.maps.DirectionsStatus.OK) {
          directionsRenderer.setDirections(result);

          const steps = result.routes[0].legs[0].steps;
          let directionsText = "";

          steps.forEach((step, index) => {
            directionsText += `${index + 1}. ${step.instructions.replace(
              /<[^>]+>/g,
              ""
            )}\n`;
          });

          directionPanel.innerText = directionsText;
        } else {
          console.error("Directions request failed due to " + status);
        }
      });
    });

    closeButton.addEventListener("click", () => {
      sidebar.classList.toggle("open");
      closeButton.innerText = closeButton.innerText === "<" ? ">" : "<";
    });

    backbutton.addEventListener("click", () => {
      mapbuttons.forEach((item) => item.classList.toggle("display"));
      backbutton.classList.add("display");

      closeButton.disabled = true;
      closeButton.style.cursor = "not-allowed";
      closeButton.innerText = "";

      directionButton.style.cursor = "pointer";
      directionButton.disabled = !directionButton.disabled;

      directionPanel.innerText = "";

      directionsRenderer.setMap(null);
      directionsRenderer.setDirections({ routes: [] });

      document.querySelector(".map-button-box").classList.remove("hide");

      initMap();
    });
  }

  rendered = true;
}
