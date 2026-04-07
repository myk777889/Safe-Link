/**
 * script.js — SafeLink Frontend Logic
 * Handles: sending alerts, polling for alerts, displaying them
 */

// ─────────────────────────────────────────────
// SLIDER LIVE VALUES
// ─────────────────────────────────────────────
console.log("SCRIPT LOADED");

let vibRange, waterRange;

document.addEventListener("DOMContentLoaded", () => {

  vibRange = document.getElementById("vibration-range");
  waterRange = document.getElementById("water-range");

  vibRange.addEventListener("input", () => {
    document.getElementById("vib-val").textContent =
      parseFloat(vibRange.value).toFixed(1);
  });

  waterRange.addEventListener("input", () => {
    document.getElementById("water-val").textContent =
      parseFloat(waterRange.value).toFixed(1);
  });

});


// ─────────────────────────────────────────────
// TRIGGER DISASTER (Device A → Server)
// ─────────────────────────────────────────────
async function triggerAlert() {
  const vibration = parseFloat(vibRange.value);
  const water_level = parseFloat(waterRange.value);
  const box = document.getElementById("status-box");

  box.className = "";
  box.textContent = "⏳ Sending to server...";

  try {
    const res = await fetch("/trigger", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        vibration,
        water_level,
        device: "Device A"
      })
    });

    const data = await res.json();

    if (data.status === "alert_created") {
      box.className = "alert";
      box.textContent = `🚨 ${data.alert.type} | Vib: ${vibration} | Water: ${water_level}`;
    } 
    else if (data.status === "safe") {
      box.className = "safe";
      box.textContent = data.message;
    } 
    else {
      box.textContent = "⚠️ Unexpected response";
    }

  } catch (err) {
    box.textContent = "❌ Server error";
  }
}

// ─────────────────────────────────────────────
// CLEAR ALL ALERTS
// ─────────────────────────────────────────────
async function clearAlerts() {
  await fetch("/alerts", { method: "DELETE" });
  document.getElementById("status-box").textContent = "Alerts cleared.";
}


// ─────────────────────────────────────────────
// POLL SERVER FOR ALERTS (Device B behavior)
// Runs every 3 seconds automatically
// ─────────────────────────────────────────────
async function pollAlerts() {
  try {
    const res = await fetch("/alerts");
    const data = await res.json();
    const alerts = data.alerts;

    document.getElementById("last-poll").textContent =
      new Date().toLocaleTimeString();

    document.getElementById("alert-count").textContent = alerts.length;

    const list = document.getElementById("alerts-list");

    if (alerts.length === 0) {
      list.innerHTML = `<div class="no-alerts">No alerts yet.</div>`;
      return;
    }

    list.innerHTML = [...alerts].reverse().map(a => `
      <div class="alert-card ${a.severity}">
        <div class="alert-header">
          <span class="alert-type">${a.type}</span>
          <span class="alert-severity">${a.severity}</span>
        </div>
        <div class="alert-msg">${a.message}</div>
        <div class="alert-meta">
          <span>📱 ${a.device}</span>
          <span>🌀 ${a.vibration}</span>
          <span>💧 ${a.water_level}</span>
          <span>🕐 ${a.timestamp}</span>
        </div>
      </div>
    `).join("");

  } catch {
    document.getElementById("last-poll").textContent = "Server offline";
  }
}

// Start polling immediately, then every 3 seconds
pollAlerts();
setInterval(pollAlerts, 3000);
//pollAlerts();
let lastAlertCount = 0;

if (alerts.length > lastAlertCount) {
  const audio = new Audio("https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg");
  audio.play();
}
lastAlertCount = alerts.length;
