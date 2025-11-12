# data_services.py
import random
from datetime import datetime, timedelta
from typing import List

# Schémas de données (similaires aux Pydantic models pour la clarté)
class EnergyMetric:
    def __init__(self, timestamp, value_kwh):
        self.timestamp = timestamp
        self.value_kwh = value_kwh

class MaintenanceAlert:
    def __init__(self, equipment_id, alert_type, probability, message, predicted_failure_date):
        self.equipment_id = equipment_id
        self.alert_type = alert_type
        self.probability = probability
        self.message = message
        self.predicted_failure_date = predicted_failure_date

class SecurityEvent:
    def __init__(self, timestamp, event_type, severity, location, description):
        self.timestamp = timestamp
        self.event_type = event_type
        self.severity = severity
        self.location = location
        self.description = description

def get_realistic_energy_metrics() -> List[EnergyMetric]:
    """Génère des données de consommation énergétique réalistes sur 24h."""
    data_points = []
    base_time = datetime.now() - timedelta(hours=24)
    night_baseline, day_baseline = 120, 250
    
    for i in range(96):
        current_time = base_time + timedelta(minutes=i * 15)
        hour = current_time.hour
        
        if 0 <= hour < 6: base = night_baseline
        elif 6 <= hour < 9: base = night_baseline + (day_baseline - night_baseline) * ((hour - 6) / 3)
        elif 9 <= hour < 17: base = day_baseline
        elif 17 <= hour < 21: base = day_baseline - (day_baseline - night_baseline) * ((hour - 17) / 4)
        else: base = night_baseline
            
        noise = random.uniform(-0.10, 0.10)
        value = base * (1 + noise)
        
        if random.random() < 0.05:
            value += random.uniform(50, 150)
            
        data_points.append(EnergyMetric(timestamp=current_time, value_kwh=round(value, 2)))
        
    return data_points

def get_maintenance_alerts() -> List[MaintenanceAlert]:
    return [
        MaintenanceAlert("AHU-ROOF-01", "Bearing Wear", 0.85, "Vibration analysis indicates high probability of bearing failure.", datetime.now() + timedelta(days=21)),
        MaintenanceAlert("PUMP-B2-03", "Motor Overheating", 0.62, "Motor temperature consistently above operational threshold.", datetime.now() + timedelta(days=45))
    ]

def get_security_events() -> List[SecurityEvent]:
    return [
        SecurityEvent(datetime.now() - timedelta(minutes=5), "Door Forced Open", "High", "Server Room - Level 3", "Access control logs show forced entry on main door."),
        SecurityEvent(datetime.now() - timedelta(hours=2), "Unauthorized Access Attempt", "Medium", "Main Entrance", "Invalid badge scanned 3 times in a row.")
    ]
