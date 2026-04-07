"""
app.py - SafeLink Backend Server
Runs locally on WiFi — no internet needed.
Other devices on the same WiFi can connect to this server.
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from model import detect_disaster
import datetime
import os

app = Flask(__name__, static_folder="static")
CORS(app)  # Allow all devices on the network to connect

# In-memory alert store (no database needed for hackathon)
alerts = []


# ─────────────────────────────────────────────
# ROUTE 1: Serve the frontend (index.html)
# ─────────────────────────────────────────────
@app.route("/")
def index():
     return render_template("index.html")

# ─────────────────────────────────────────────
# ROUTE 2: Trigger a disaster check (POST)
# Called by: Device A when user clicks button
# ─────────────────────────────────────────────
@app.route("/trigger", methods=["POST"])
def trigger():
    data = request.get_json()

    device = data.get("device", "Device A")

    vibration = float(data.get("vibration", 0))
    water_level = float(data.get("water_level", 0))

    result = detect_disaster(vibration, water_level)

    if result["detected"]:
        alert = {
            "id": len(alerts) + 1,
            "type": result["type"],
            "severity": result["severity"],
            "message": result["message"],
            "vibration": vibration,
            "water_level": water_level,
            "device": device,  # FIXED typo
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        alerts.append(alert)
        return jsonify({"status": "alert_created", "alert": alert})
    else:
        return jsonify({"status": "safe", "message": result["message"]})


# ─────────────────────────────────────────────
# ROUTE 3: Get all alerts (GET)
# Called by: Device B to check for alerts
# ─────────────────────────────────────────────
@app.route("/alerts", methods=["GET"])
def get_alerts():
    return jsonify({"alerts": alerts}), 200


# ─────────────────────────────────────────────
# ROUTE 4: Clear all alerts (DELETE)
# ─────────────────────────────────────────────

@app.route("/alerts", methods=["DELETE"])
def clear_alerts():
    alerts.clear()
    return jsonify({"status": "cleared"}), 200


# ─────────────────────────────────────────────
# START SERVER
# host="0.0.0.0" → makes it accessible on local WiFi
# port=5000 → other devices use http://<your-ip>:5000
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🚀 SafeLink Server Starting...")
    print("📡 Accessible on your local WiFi network")
    print("🌐 Open on this device: http://localhost:5000")
    print("📱 Open on other devices: http://<YOUR-IP>:5000\n")
    app.run(host="0.0.0.0", port=5000, debug=True)

