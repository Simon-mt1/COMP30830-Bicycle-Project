/**
 * @module charts.js
 * This module provides functionality to render line charts for bike availability and space availability
 * predictions using the Chart.js library. It dynamically updates the chart based on new prediction data.
 *
 * @requires Chart.js
 *
 */

// Select the chart canvas elements from the DOM
const availableBikes = document.querySelector(".available-bikes-chart");
const availablespaces = document.querySelector(".available-spaces-chart");

// Variables to hold Chart.js instances for bike and space availability
let availableBikesChart = null;
let availablespacesChart = null;

/**
 * Renders a line chart showing predicted available bikes over time.
 * If a chart already exists, it will be destroyed before rendering a new one.
 *
 * @function drawAvailableBikesCharts
 * @param {Object.<string, number>} prediction - An object where keys are time labels (e.g., "08:00")
 * and values are the number of available bikes at that time.
 * @returns {void}
 */
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

/**
 * Renders a line chart showing predicted available parking spaces over time.
 * If a chart already exists, it will be destroyed before rendering a new one.
 *
 * @function drawAvailableSpacesCharts
 * @param {Object.<string, number>} prediction - An object where keys are time labels (e.g., "08:00")
 * and values are the number of available spaces at that time.
 * @returns {void}
 */
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
