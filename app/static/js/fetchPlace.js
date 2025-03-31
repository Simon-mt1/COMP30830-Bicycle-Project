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
    const address = document.querySelector(".address-text");
    address.innerText = data["places"][0]["formattedAddress"];
    placeDetail = fetchPlaceDetails(data);
  } catch (error) {
    console.error("Error fetching places:", error);
    return null;
  }
};

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
    fetchPhoto(data);
  } catch (error) {
    console.error("Error fetching place details:", error);
    return null;
  }
};

const fetchPhoto = async (place) => {
  const sideBarImage = document.querySelector(".sidebar-image");
  try {
    const params = {
      maxHeightPx: 400,
      maxWidthPx: 400,
      apiKey: googleapis, // You can pass the API key in headers if needed
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

    const imageUrl = await response.url;

    sideBarImage.style.backgroundImage = `url('${imageUrl}')`;
  } catch (error) {
    sideBarImage.style.backgroundImage = `url('./../static/images/picture not found.png')`;
    console.error("Error fetching photo:", error);
  }
};
