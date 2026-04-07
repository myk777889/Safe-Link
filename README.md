# 🚨 SafeLink — Offline Disaster Alert System

## Folder Structure
```
safelink/
├── app.py           ← Backend server (run this)
├── model.py         ← Disaster detection logic
├── requirements.txt ← Python dependencies
└── static/
    ├── index.html   ← Frontend UI
    └── script.js    ← Frontend logic
```

## Setup & Run

### Step 1: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the server
```bash
python app.py
```

### Step 3: Open in browser
- **This device:** http://localhost:5000
- **Other devices (same WiFi):** http://<YOUR-IP>:5000

### Find your IP address
- **Windows:** `ipconfig` → look for IPv4
- **Mac/Linux:** `ifconfig` or `ip a`

## Demo Flow (for judges)
1. Open app on 2 devices (same WiFi)
2. On Device A → adjust sliders → click "Simulate Disaster"
3. Device B → automatically receives the alert in 3 seconds
4. No internet used ✅

## Detection Rules (model.py)
| Condition | Result |
|-----------|--------|
| Vibration > 7.0 | 🔴 Earthquake |
| Water Level > 8.0 | 🌊 Flood |
| Both | ⚠️ CRITICAL Multi-Hazard |
