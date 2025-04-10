async function getCurrentLocation() {
  return new Promise((resolve, reject) => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          resolve({
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          });
        },
        (error) => {
          reject("Error getting location: " + error.message);
        }
      );
    } else {
      reject("Geolocation is not supported by this browser.");
    }
  });
}

async function retrieveLocation() {
  try {
    const location = await getCurrentLocation();
    return location;
  } catch (error) {
    console.error(error);
  }
}

async function goToNearestStation(markers) {
  const location = await retrieveLocation();

  if (!location) {
    alert("Unable to retrieve your location.");
    return;
  }

  let nearest = null;
  let minDistance = Infinity;

  for (let i = 0; i < mapData.length; i++) {
    const station = mapData[i];
    const stationPos = station["position"];

    // Skip stations with 0 of selected value
    if (station[value] === 0) continue;

    const distance = Math.sqrt(
      Math.pow(location.lat - stationPos.lat, 2) +
        Math.pow(location.lng - stationPos.lng, 2)
    );

    if (distance < minDistance) {
      minDistance = distance;
      nearest = { station, index: i };
    }
  }

  if (!nearest) {
    alert("No nearby stations with availability.");
    return;
  }

  // Trigger the nearest marker's click event to reuse logic
  google.maps.event.trigger(markers[nearest.index], "click");
}
