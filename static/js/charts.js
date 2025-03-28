const temperatureCanvas = document.getElementById("temp");
const windspeedCanvas = document.getElementById("windspeed");
const lol = document.getElementById("new");

const temp = [];
const windSpeed = [];
const time = [];

for (let data of weatherData["hourly"]) {
  temp.push(data["temp"]);
  windSpeed.push(data["wind_speed"]);
  time.push(data["dt"]);
}

new Chart(temperatureCanvas, {
  type: "line",
  data: {
    labels: time,
    datasets: [
      {
        label: "Temperature",
        data: temp,
        borderWidth: 1,
      },
    ],
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
});

new Chart(windspeedCanvas, {
  type: "line",
  data: {
    labels: time,
    datasets: [
      {
        label: "Wind speed",
        data: windSpeed,
        borderWidth: 1,
      },
    ],
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
});

new Chart(lol, {
  type: "line",
  data: {
    labels: time,
    datasets: [
      {
        label: "Wind speed",
        data: windSpeed,
        borderWidth: 1,
      },
    ],
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
});
