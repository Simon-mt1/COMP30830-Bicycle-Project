/**
 * Handles modal and overlay display for the weather information popup.
 */

// DOM references
const modal = document.querySelector(".modal");
const overlay = document.querySelector(".overlay");

// Opens the modal by removing the "transform" class
const handleWeatherIconClick = (event) => {
  modal.classList.remove("transform");
  overlay.classList.remove("transform");
};

// Closes the modal when the 'X' button is clicked
document.querySelector(".x-mark").addEventListener("click", () => {
  modal.classList.add("transform");
  overlay.classList.add("transform");
});

// Closes the modal when the overlay background is clicked
overlay.addEventListener("click", () => {
  modal.classList.add("transform");
  overlay.classList.add("transform");
});
