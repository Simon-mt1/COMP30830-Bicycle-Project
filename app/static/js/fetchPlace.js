/**
 * @module fetchPlaces
 * This module fetches information about Dublin Bikes-related locations using the Google Places API.
 * It retrieves basic place details and a photo, then displays the address and sets the sidebar image.
 *
 * @requires Google Places API
 */

/**
 * Searches for a place related to Dublin Bikes using Google's Places Text Search API.
 *
 * @async
 * @function fetchPlaces
 * @param {string} place - The user-provided text query to search for (e.g., street name or landmark).
 * @returns {Promise<void>}
 */
const fetchPlaces = async (place) => {
  const url = "https://places.googleapis.com/v1/places:searchText";
  const apiKey = googleapis;

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

    // Display the formatted address in the sidebar
    const address = document.querySelector(".address-text");
    address.innerText = data["places"][0]["formattedAddress"];

    // Fetch more details like photos
    placeDetail = fetchPlaceDetails(data);
  } catch (error) {
    console.error("Error fetching places:", error);
    return null;
  }
};

/**
 * Fetches detailed information about a selected place, including photos.
 *
 * @async
 * @function fetchPlaceDetails
 * @param {Object} place - The place data object returned from `fetchPlaces`.
 * @returns {Promise<void>}
 */
const fetchPlaceDetails = async (place) => {
  try {
    const url =
      "https://places.googleapis.com/v1/" + place["places"][0]["name"];
    const apiKey = googleapis;

    const headers = {
      "X-Goog-Api-Key": apiKey,
      "X-Goog-FieldMask": "id,displayName,name,photos",
      "Content-Type": "application/json",
    };

    const response = await fetch(url, {
      method: "GET",
      headers: headers,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();

    // Fetch and display the image
    fetchPhoto(data);
  } catch (error) {
    console.error("Error fetching place details:", error);
    return null;
  }
};

/**
 * Fetches a photo of the place and displays it as the sidebar background.
 *
 * @async
 * @function fetchPhoto
 * @param {Object} place - The place object containing photo metadata.
 * @returns {Promise<void>}
 */
const fetchPhoto = async (place) => {
  const sideBarImage = document.querySelector(".sidebar-image");

  try {
    const params = {
      maxHeightPx: 400,
      maxWidthPx: 400,
      apiKey: googleapis,
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

    const response = await fetch(url, {
      method: "GET",
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // Set the photo as sidebar background
    const imageUrl = await response.url;
    sideBarImage.style.backgroundImage = `url('${imageUrl}')`;
  } catch (error) {
    // Use fallback image if fetch fails
    sideBarImage.style.backgroundImage = `url('./../static/images/picture not found.png')`;
    console.error("Error fetching photo:", error);
  }
};
