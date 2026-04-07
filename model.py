def detect_disaster(data):
    if data.get("vibration", 0) > 7:
        return True
    if data.get("water_level", 0) > 80:
        return True
    return False
"""
model.py - SafeLink Disaster Detection Logic
Rule-based ML model (fast + reliable for hackathon demo)
"""

def detect_disaster(vibration: float, water_level: float) -> dict:
    """
    Checks sensor values and returns a disaster decision.

    Rules:
    - vibration > 7.0  → Earthquake risk
    - water_level > 8.0 → Flood risk
    - Both high         → Critical multi-hazard
    
    Returns a dict with: detected (bool), type, severity, message
    """

    earthquake = vibration > 7.0
    flood = water_level > 8.0

    if earthquake and flood:
        return {
            "detected": True,
            "type": "Multi-Hazard",
            "severity": "CRITICAL",
            "message": f"⚠️ CRITICAL: Earthquake (vibration={vibration}) + Flood (water={water_level}) detected!",
            "vibration": vibration,
            "water_level": water_level
        }
    elif earthquake:
        return {
            "detected": True,
            "type": "Earthquake",
            "severity": "HIGH",
            "message": f"🔴 Earthquake detected! Vibration level: {vibration}",
            "vibration": vibration,
            "water_level": water_level
        }
    elif flood:
        return {
            "detected": True,
            "type": "Flood",
            "severity": "HIGH",
            "message": f"🌊 Flood risk detected! Water level: {water_level}",
            "vibration": vibration,
            "water_level": water_level
        }
    else:
        return {
            "detected": False,
            "type": "None",
            "severity": "SAFE",
            "message": "✅ All systems normal.",
            "vibration": vibration,
            "water_level": water_level
        }
