const predictionChart = document.querySelector(".prediction-chart");
let chart = null;

const drawCharts = (prediction) => {
  const keys = Object.keys(prediction);
  const values = Object.values(prediction).map((item) => Math.floor(item));

  const max = Math.max(...values);
  const min = Math.min(...values);

  if (chart !== null) {
    chart.destroy();
  }

  chart = new Chart(predictionChart, {
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
          ticks: {
            stepSize: 1,
          },
          min: min - 3,
          max: max + 3,
          beginAtZero: true,
        },
      },
    },
  });
};
