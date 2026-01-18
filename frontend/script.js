const API_BASE = "http://127.0.0.1:8000";

// ================= DASHBOARD =================
async function loadDashboard() {
  try {
    const [devicesRes, logsRes] = await Promise.all([
      fetch(`${API_BASE}/devices/`),
      fetch(`${API_BASE}/logs/`)
    ]);

    const devices = await devicesRes.json();
    const logs = await logsRes.json();

    document.getElementById("deviceCount").innerText = Array.isArray(devices) ? devices.length : 0;
    document.getElementById("logCount").innerText = Array.isArray(logs) ? logs.length : 0;

    const critical = Array.isArray(logs)
      ? logs.filter(l => l.severity === "critical").length
      : 0;

    document.getElementById("criticalCount").innerText = critical;

  } catch (err) {
    console.error("Dashboard error:", err);
  }
}

// ================= NETWORK CONTROLS =================
async function startNetwork() {
  return networkAction("/network/start", "Network started");
}

async function stopNetwork() {
  return networkAction("/network/stop", "Network stopped");
}

async function rebuildNetwork() {
  return networkAction("/network/rebuild", "Network rebuilt");
}

async function simulateAttack() {
  return networkAction("/network/simulate", "Attack started");
}

async function networkAction(endpoint, successMsg) {
  const statusEl = document.getElementById("simulationStatus");
  statusEl.innerText = "⏳ Processing...";

  try {
    const res = await fetch(`${API_BASE}${endpoint}`, { method: "POST" });
    const data = await res.json();

    if (data.status === "success" || data.status === "already_running") {
      statusEl.innerText = `✅ ${successMsg}`;
    } else {
      statusEl.innerText = `❌ ${data.message}`;
    }

    setTimeout(() => {
      fetchNetworkStatus();
      loadDashboard();
    }, 2000);

  } catch (err) {
    statusEl.innerText = "❌ Failed";
  }
}

// ================= NETWORK STATUS =================
async function fetchNetworkStatus() {
  try {
    const res = await fetch(`${API_BASE}/network/status`);
    const data = await res.json();
    updateNetworkStatusUI(data.status);
  } catch (err) {
    console.error("Status error:", err);
  }
}

function updateNetworkStatusUI(status) {
  const dot = document.getElementById("statusDot");
  const text = document.getElementById("statusText");

  dot.className = "status-dot " + status;
  text.innerText = "Network Status: " + status.toUpperCase();
}

// ================= INIT =================
document.addEventListener("DOMContentLoaded", () => {
  loadDashboard();
  fetchNetworkStatus();
  setInterval(fetchNetworkStatus, 3000);
});
