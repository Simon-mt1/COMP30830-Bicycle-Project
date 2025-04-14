/**
 * @module fetchLocation.js
 * This module provides functions for retrieving the user's current location and navigating
 * to the nearest available station on a map using the Google Maps API.
 *
 * It assumes `mapData` is an array of station objects, and each station has a `position` (with `lat` and `lng`)
 * and a `value` key that represents availability (e.g., bikes or spaces).
 *
 * @requires Google Maps JavaScript API
 */

/**
 * Gets the current geolocation of the user using the browser's `navigator.geolocation` API.
 *
 * @async
 * @function getCurrentLocation
 * @returns {Promise<{lat: number, lng: number}>} A promise that resolves with an object containing `lat` and `lng`.
 * @throws Will reject the promise if geolocation fails or is not supported.
 */
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

/**
 * Wraps the `getCurrentLocation` function with error handling.
 *
 * @async
 * @function retrieveLocation
 * @returns {Promise<{lat: number, lng: number}|undefined>} The user's location or undefined if an error occurs.
 */
async function retrieveLocation() {
  try {
    const location = await getCurrentLocation();
    return location;
  } catch (error) {
    console.error(error);
  }
}

/**
 * Finds and navigates to the nearest available station using the provided markers array.
 * Triggers the click event on the nearest marker to leverage existing click handler logic.
 *
 * @async
 * @function goToNearestStation
 * @param {google.maps.Marker[]} markers - An array of Google Maps Marker objects corresponding to each station.
 * @returns {void}
 */
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

    // Skip stations with 0 available bikes or spaces (depending on the selected value)
    if (station[value] === 0) continue;

    // Calculate straight-line distance (Pythagorean)
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

  // Simulate a click on the nearest station's marker
  google.maps.event.trigger(markers[nearest.index], "click");
}
