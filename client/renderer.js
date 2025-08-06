// Path to the exported logs JSON file
const LOGS_PATH = "../tracker/exported_logs.json";

// Fetch logs and populate the table
async function loadLogs() {
  try {
    const response = await fetch(LOGS_PATH);
    if (!response.ok) {
      throw new Error(`Failed to fetch logs: ${response.statusText}`);
    }

    const logs = await response.json();
    const tableBody = document.querySelector("#log-table tbody");

    // Clear existing rows
    tableBody.innerHTML = "";

    // Populate table with logs
    logs.forEach((log) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${log.timestamp}</td>
        <td>${log.app_name}</td>
        <td>${log.idle_time}s</td>
        <td>${log.mouse_activity}</td>
        <td>${log.keyboard_activity}</td>
        <td>${log.predicted_label}</td>
      `;
      tableBody.appendChild(row);
    });
  } catch (error) {
    console.error("Error loading logs:", error);
  }
}

// Load logs when the page is loaded
window.onload = loadLogs;
window.onload = loadLogs;

const { ipcRenderer } = require('electron');

document.getElementById('signup-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = document.getElementById('email').value;
  const response = await ipcRenderer.invoke('signup', email);
  if (response.success) {
    alert('Signed up successfully!');
  }
});

document.getElementById('start-tracker').addEventListener('click', async () => {
  const response = await ipcRenderer.invoke('start-tracker');
  if (response.success) {
    alert('Tracker started!');
    document.getElementById('start-tracker').disabled = true;
    document.getElementById('stop-tracker').disabled = false;
  }
});

document.getElementById('stop-tracker').addEventListener('click', async () => {
  const response = await ipcRenderer.invoke('stop-tracker');
  if (response.success) {
    alert('Tracker stopped!');
    document.getElementById('start-tracker').disabled = false;
    document.getElementById('stop-tracker').disabled = true;
  }
});
