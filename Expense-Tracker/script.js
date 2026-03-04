// Category list used across the app
const CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"];

// Chart colors (used across charts & legend)
const CHART_COLORS = [
  "#6366F1",
  "#10B981",
  "#F59E0B",
  "#EF4444",
  "#3B82F6",
  "#8B5CF6",
];

let expenses = [];
let pieChart;
let barChart;

// Utility: format currency
function formatCurrency(amount) {
  return "₹" + amount.toFixed(2);
}

// Save data to LocalStorage
function saveData() {
  try {
    localStorage.setItem("expenseTrackerData", JSON.stringify(expenses));
  } catch (err) {
    console.error("Unable to save expenses:", err);
  }
}

// Load data from LocalStorage
function loadData() {
  try {
    const raw = localStorage.getItem("expenseTrackerData");
    if (!raw) {
      expenses = [];
      return;
    }
    const parsed = JSON.parse(raw);
    if (Array.isArray(parsed)) {
      expenses = parsed;
    } else {
      expenses = [];
    }
  } catch (err) {
    console.error("Unable to load expenses:", err);
    expenses = [];
  }
}

// Add a new expense
function addExpense(title, amount, category) {
  const expense = {
    id: Date.now(),
    title,
    amount: Number(amount),
    category,
    createdAt: new Date().toISOString(),
  };

  expenses.unshift(expense);
  saveData();
  renderExpenses();
  updateDashboard();
  updateCharts();
}

// Delete an expense by id
function deleteExpense(id) {
  expenses = expenses.filter((e) => e.id !== id);
  saveData();
  renderExpenses();
  updateDashboard();
  updateCharts();
}

// Update dashboard totals
function updateDashboard() {
  const total = expenses.reduce((sum, e) => sum + e.amount, 0);
  const count = expenses.length;

  const totalEl = document.getElementById("total-expenses");
  const countEl = document.getElementById("transaction-count");

  if (totalEl) totalEl.textContent = formatCurrency(total);
  if (countEl) countEl.textContent = count.toString();
}

// Prepare chart data from expenses
function getCategoryTotals() {
  const totals = {};
  CATEGORIES.forEach((cat) => {
    totals[cat] = 0;
  });

  for (const expense of expenses) {
    if (!totals.hasOwnProperty(expense.category)) {
      totals[expense.category] = 0;
    }
    totals[expense.category] += expense.amount;
  }

  const labels = Object.keys(totals);
  const values = labels.map((cat) => totals[cat]);

  return { labels, values };
}

// Initialize or update charts
function updateCharts() {
  const { labels, values } = getCategoryTotals();

  const pieCanvas = document.getElementById("pieChart");
  const barCanvas = document.getElementById("barChart");

  const colors = CHART_COLORS;
  const backgroundColors = colors;
  const borderColors = colors;

  if (pieChart) {
    pieChart.data.labels = labels;
    pieChart.data.datasets[0].data = values;
    pieChart.update();
  } else if (pieCanvas) {
    pieChart = new Chart(pieCanvas, {
      type: "pie",
      data: {
        labels,
        datasets: [
          {
            data: values,
            backgroundColor: backgroundColors,
            borderColor: borderColors,
            borderWidth: 1.5,
          },
        ],
      },
      options: {
        plugins: {
          legend: {
            display: false,
          },
        },
      },
    });
  }

  if (barChart) {
    barChart.data.labels = labels;
    barChart.data.datasets[0].data = values;
    barChart.update();
  } else if (barCanvas) {
    barChart = new Chart(barCanvas, {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "Amount",
            data: values,
            backgroundColor: backgroundColors,
            borderColor: borderColors,
            borderWidth: 1.5,
            borderRadius: 6,
          },
        ],
      },
      options: {
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          x: {
            ticks: {
              color: "#9ca3af",
            },
            grid: {
              display: false,
            },
          },
          y: {
            ticks: {
              color: "#6b7280",
            },
            grid: {
              color: "rgba(209, 213, 219, 0.9)",
            },
          },
        },
      },
    });
  }

  renderPieLegend(labels, colors);
}

// Custom legend for pie chart
function renderPieLegend(labels, colors) {
  const legendContainer = document.getElementById("pie-legend");
  if (!legendContainer) return;

  legendContainer.innerHTML = "";

  labels.forEach((label, index) => {
    const item = document.createElement("div");
    item.className = "chart-legend-item";

    const colorDot = document.createElement("span");
    colorDot.className = "chart-legend-color";
    colorDot.style.backgroundColor = colors[index % colors.length];

    const text = document.createElement("span");
    text.textContent = label;

    item.appendChild(colorDot);
    item.appendChild(text);

    legendContainer.appendChild(item);
  });
}

// Render expenses list
function renderExpenses() {
  const listEl = document.getElementById("expense-list");
  const emptyStateEl = document.getElementById("empty-state");

  if (!listEl) return;

  listEl.innerHTML = "";

  if (expenses.length === 0) {
    if (emptyStateEl) emptyStateEl.style.display = "block";
    return;
  }

  if (emptyStateEl) emptyStateEl.style.display = "none";

  expenses.forEach((expense) => {
    const li = document.createElement("li");
    li.className = "expense-item";

    const main = document.createElement("div");
    main.className = "expense-main";

    const titleEl = document.createElement("p");
    titleEl.className = "expense-title";
    titleEl.textContent = expense.title;

    const metaEl = document.createElement("p");
    metaEl.className = "expense-meta";

    const date = new Date(expense.createdAt);
    const dateString = date.toLocaleDateString(undefined, {
      month: "short",
      day: "numeric",
    });

    const chip = document.createElement("span");
    const categoryClass =
      "expense-chip-" + String(expense.category || "").toLowerCase();
    chip.className = "expense-chip " + categoryClass;

    const dot = document.createElement("span");
    dot.className = "expense-chip-dot";

    const catLabel = document.createElement("span");
    catLabel.textContent = expense.category;

    chip.appendChild(dot);
    chip.appendChild(catLabel);

    metaEl.textContent = dateString + " • ";
    metaEl.appendChild(chip);

    main.appendChild(titleEl);
    main.appendChild(metaEl);

    const amountEl = document.createElement("span");
    amountEl.className = "expense-amount";
    amountEl.textContent = formatCurrency(expense.amount);

    const deleteBtn = document.createElement("button");
    deleteBtn.className = "delete-btn";
    deleteBtn.type = "button";
    deleteBtn.innerHTML = "×";
    deleteBtn.title = "Delete expense";
    deleteBtn.addEventListener("click", () => deleteExpense(expense.id));

    li.appendChild(main);
    li.appendChild(amountEl);
    li.appendChild(deleteBtn);

    listEl.appendChild(li);
  });
}

// Handle form submission
function handleFormSubmit(event) {
  event.preventDefault();

  const titleInput = document.getElementById("title");
  const amountInput = document.getElementById("amount");
  const categorySelect = document.getElementById("category");

  const title = titleInput.value.trim();
  const amount = parseFloat(amountInput.value);
  const category = categorySelect.value;

  if (!title || !amount || amount <= 0 || !category) {
    return;
  }

  addExpense(title, amount, category);

  // Reset inputs
  titleInput.value = "";
  amountInput.value = "";
  categorySelect.value = "";
  titleInput.focus();
}

// Clear all expenses
function clearAllExpenses() {
  if (expenses.length === 0) return;
  expenses = [];
  saveData();
  renderExpenses();
  updateDashboard();
  updateCharts();
}

// Initialize app on DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("expense-form");
  const clearAllBtn = document.getElementById("clear-all");

  if (form) {
    form.addEventListener("submit", handleFormSubmit);
  }

  if (clearAllBtn) {
    clearAllBtn.addEventListener("click", clearAllExpenses);
  }

  loadData();
  renderExpenses();
  updateDashboard();
  updateCharts();
});

