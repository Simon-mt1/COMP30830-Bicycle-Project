const modal = document.querySelector(".modal");
const overlay = document.querySelector(".overlay");

const handleWeatherIconClick = (event) => {
  modal.classList.remove("transform");
  overlay.classList.remove("transform");
};

document.querySelector(".x-mark").addEventListener("click", () => {
  modal.classList.add("transform");
  overlay.classList.add("transform");
});

overlay.addEventListener("click", () => {
  modal.classList.add("transform");
  overlay.classList.add("transform");
});
