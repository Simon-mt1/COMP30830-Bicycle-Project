// Script to

let value = "available_bikes";
let rendered = false;
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

async function initMap() {
  sidebar.classList.remove("open");

  if (!directionsService) {
    directionsService = new google.maps.DirectionsService();
  }
  if (!directionsRenderer) {
    directionsRenderer = new google.maps.DirectionsRenderer();
  } else {
    // Reset existing renderer
    directionsRenderer.setMap(null);
    directionsRenderer.setDirections({ routes: [] });
  }

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
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 15,
    center: dublin,
    styles: mapStyles,
    mapTypeControl: false, // Removes the map type control
    streetViewControl: false, // Removes the street view control
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
      bikesNumber.innerText =
        data["available_bikes"] +
        " / " +
        data["bike_stands"] +
        " bikes available";

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

      mapbuttons.forEach((item) => {
        item.classList.toggle("display");
      });

      backbutton.classList.remove("display");
      closeButton.disabled = false;
      document.querySelector(".map-button-box").classList.add("hide");
      directionButton.style.cursor = "not-allowed";
      directionButton.disabled = !directionButton.disabled;

      var request = {
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
      if (closeButton.innerText == "<") {
        closeButton.innerText = ">";
      } else {
        closeButton.innerText = "<";
      }
    });

    backbutton.addEventListener("click", () => {
      mapbuttons.forEach((item) => {
        item.classList.toggle("display");
      });
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
