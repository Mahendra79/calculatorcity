const ClaculatorcityCharts = {};

function destroyExistingChart(canvasId) {
  if (ClaculatorcityCharts[canvasId]) {
    ClaculatorcityCharts[canvasId].destroy();
    delete ClaculatorcityCharts[canvasId];
  }
}

function createPieChart(canvasId, labels, data, colors) {
  const canvas = document.getElementById(canvasId);
  if (!canvas || typeof Chart === "undefined") return null;
  destroyExistingChart(canvasId);
  ClaculatorcityCharts[canvasId] = new Chart(canvas, {
    type: "pie",
    data: {
      labels,
      datasets: [{ data, backgroundColor: colors, borderWidth: 1 }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  });
  return ClaculatorcityCharts[canvasId];
}

function createLineChart(canvasId, labels, data, label, color) {
  const canvas = document.getElementById(canvasId);
  if (!canvas || typeof Chart === "undefined") return null;
  destroyExistingChart(canvasId);
  ClaculatorcityCharts[canvasId] = new Chart(canvas, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label,
        data,
        borderColor: color,
        backgroundColor: `${color}22`,
        fill: true,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  });
  return ClaculatorcityCharts[canvasId];
}

function createBarChart(canvasId, labels, datasets, options = {}) {
  const canvas = document.getElementById(canvasId);
  if (!canvas || typeof Chart === "undefined") return null;
  destroyExistingChart(canvasId);
  ClaculatorcityCharts[canvasId] = new Chart(canvas, {
    type: "bar",
    data: { labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      ...options
    }
  });
  return ClaculatorcityCharts[canvasId];
}

function createStackedBarChart(canvasId, labels, datasets) {
  return createBarChart(canvasId, labels, datasets, {
    scales: {
      x: { stacked: true },
      y: { stacked: true }
    }
  });
}
