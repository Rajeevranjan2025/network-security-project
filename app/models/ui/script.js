const API_BASE = "http://127.0.0.1:8000";

// ================= DASHBOARD =================
async function loadDashboard() {
  try {
    const devicesRes = await fetch(`${API_BASE}/devices/`);
    const logsRes = await fetch(`${API_BASE}/logs/`);

    const devices = await devicesRes.json();
    const logs = await logsRes.json();

    const deviceCountEl = document.getElementById("deviceCount");
    const logCountEl = document.getElementById("logCount");
    const criticalCountEl = document.getElementById("criticalCount");

    if (!deviceCountEl || !logCountEl || !criticalCountEl) return;

    const deviceCount = Array.isArray(devices) ? devices.length : 0;
    const logCount = Array.isArray(logs) ? logs.length : 0;

    const criticalLogs = Array.isArray(logs)
      ? logs.filter(log => log.severity === "critical")
      : [];

    deviceCountEl.innerText = deviceCount;
    logCountEl.innerText = logCount;
    criticalCountEl.innerText = criticalLogs.length;

  } catch (err) {
    console.error("Dashboard error:", err);
  }
}


// ================= DEVICES =================
async function loadDevices() {
  try {
    const res = await fetch(`${API_BASE}/devices/`);
    const devices = await res.json();

    const table = document.getElementById("deviceTable");
    if (!table || !Array.isArray(devices)) return;

    table.innerHTML = "";

    devices.forEach(device => {
      const row = `
        <tr>
          <td>${device.id}</td>
          <td>${device.name}</td>
          <td>${device.type}</td>
          <td>${device.ip}</td>
          <td>${device.status}</td>
          <td>
            <button onclick="deleteDevice(${device.id})">Delete</button>
          </td>
        </tr>
      `;
      table.innerHTML += row;
    });

  } catch (err) {
    console.error("Devices error:", err);
  }
}

async function addDevice() {
  const name = document.getElementById("name")?.value;
  const type = document.getElementById("type")?.value;
  const ip = document.getElementById("ip")?.value;

  if (!name || !type || !ip) {
    alert("All fields required");
    return;
  }

  try {
    await fetch(`${API_BASE}/devices/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, type, ip })
    });

    document.getElementById("name").value = "";
    document.getElementById("type").value = "";
    document.getElementById("ip").value = "";

    loadDevices();
    loadDashboard();
  } catch (err) {
    console.error("Add device error:", err);
  }
}

async function deleteDevice(id) {
  try {
    await fetch(`${API_BASE}/devices/${id}`, { method: "DELETE" });
    loadDevices();
    loadDashboard();
  } catch (err) {
    console.error("Delete device error:", err);
  }
}


// ================= LOGS =================
async function loadLogs() {
  try {
    const res = await fetch(`${API_BASE}/logs/`);
    const logs = await res.json();

    const table = document.getElementById("logTable");
    if (!table || !Array.isArray(logs)) return;

    const filterEl = document.getElementById("severityFilter");
    const filter = filterEl ? filterEl.value : "all";

    table.innerHTML = "";

    logs.forEach(log => {
      if (filter !== "all" && log.severity !== filter) return;

      const row = `
        <tr class="${log.severity}">
          <td>${log.id}</td>
          <td>${log.device_id}</td>
          <td>${log.message}</td>
          <td>${log.severity}</td>
          <td>${new Date(log.timestamp).toLocaleString()}</td>
        </tr>
      `;
      table.innerHTML += row;
    });

  } catch (err) {
    console.error("Logs error:", err);
  }
}


// ================= RULES =================
async function loadRules() {
  try {
    const res = await fetch(`${API_BASE}/rules/`);
    const rules = await res.json();

    const table = document.getElementById("ruleTable");
    if (!table || !Array.isArray(rules)) return;

    table.innerHTML = "";

    rules.forEach(rule => {
      const row = `
        <tr>
          <td>${rule.id}</td>
          <td>${rule.device_id}</td>
          <td>${rule.rule_type}</td>
          <td>${rule.target}</td>
          <td>${rule.description}</td>
          <td>
            <button onclick="deleteRule(${rule.id})">Delete</button>
          </td>
        </tr>
      `;
      table.innerHTML += row;
    });

  } catch (err) {
    console.error("Rules error:", err);
  }
}

async function addRule() {
  const device_id = document.getElementById("ruleDeviceId")?.value;
  const rule_type = document.getElementById("ruleType")?.value;
  const target = document.getElementById("ruleTarget")?.value;
  const description = document.getElementById("ruleDescription")?.value;

  if (!device_id || !rule_type || !target || !description) {
    alert("All fields required");
    return;
  }

  try {
    await fetch(`${API_BASE}/rules/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        device_id: parseInt(device_id),
        rule_type,
        target,
        description
      })
    });

    document.getElementById("ruleDeviceId").value = "";
    document.getElementById("ruleTarget").value = "";
    document.getElementById("ruleDescription").value = "";

    loadRules();
  } catch (err) {
    console.error("Add rule error:", err);
  }
}

async function deleteRule(id) {
  try {
    await fetch(`${API_BASE}/rules/${id}`, { method: "DELETE" });
    loadRules();
  } catch (err) {
    console.error("Delete rule error:", err);
  }
}


// ================= SIMULATION =================
async function simulateAttack() {
  const statusEl = document.getElementById("simulationStatus");
  if (!statusEl) return;

  statusEl.innerText = "⏳ Simulating attack...";

  try {
    const res = await fetch(`${API_BASE}/simulate/`, { method: "POST" });
    const data = await res.json();

    if (data.status === "success") {
      statusEl.innerText = "✅ Attack simulated successfully!";
    } else {
      statusEl.innerText = "❌ " + data.message;
    }

    setTimeout(() => {
      loadDashboard();
      loadLogs();
    }, 3000);

  } catch (err) {
    console.error("Simulation error:", err);
    statusEl.innerText = "❌ Simulation failed!";
  }
}


// ================= INIT =================
document.addEventListener("DOMContentLoaded", () => {
  loadDashboard();
  loadDevices();
  loadLogs();
  loadRules();

  setInterval(loadLogs, 5000);
});
