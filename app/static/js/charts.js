const availableBikes = document.querySelector(".available-bikes-chart");
const availablespaces = document.querySelector(".available-spaces-chart");
let availableBikesChart = null;
let availablespacesChart = null;

const drawAvailableBikesCharts = (prediction) => {
  const keys = Object.keys(prediction);
  const values = Object.values(prediction);

  const max = Math.max(...values);
  const min = Math.min(...values);

  if (availableBikesChart !== null) {
    availableBikesChart.destroy();
  }

  availableBikesChart = new Chart(availableBikes, {
    type: "line",
    data: {
      labels: keys,
      datasets: [
        {
          label: "Available bikes",
          data: values,
        },
      ],
    },
    options: {
      scales: {
        y: {
          title: {
            display: true,
            text: "Available Bikes",
            font: {
              weight: "bold",
              size: 12,
            },
          },
          ticks: {
            stepSize: 1,
          },
          min: min - 3,
          max: max + 3,
          beginAtZero: true,
        },
        x: {
          title: {
            display: true,
            text: "Time (hours)",
            font: {
              weight: "bold",
              size: 12,
            },
          },
        },
      },
    },
  });
};

const drawAvailableSpacesCharts = (prediction) => {
  const keys = Object.keys(prediction);
  const values = Object.values(prediction);

  const max = Math.max(...values);
  const min = Math.min(...values);

  if (availablespacesChart !== null) {
    availablespacesChart.destroy();
  }

  availablespacesChart = new Chart(availablespaces, {
    type: "line",
    data: {
      labels: keys,
      datasets: [
        {
          label: "Available spaces",
          data: values,
        },
      ],
    },
    options: {
      scales: {
        y: {
          title: {
            display: true,
            text: "Available spaces",
            font: {
              weight: "bold",
              size: 12,
            },
          },
          ticks: {
            stepSize: 1,
          },
          min: min - 3,
          max: max + 3,
          beginAtZero: true,
        },
        x: {
          title: {
            display: true,
            text: "Time (hours)",
            font: {
              weight: "bold",
              size: 12,
            },
          },
        },
      },
    },
  });
};
