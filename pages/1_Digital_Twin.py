import streamlit as st
import time
import random
import pandas as pd
from datetime import datetime

# --- Configuration de la page pour le jumeau numérique ---
st.set_page_config(
    page_title="PIONIER - Digital Twin",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS (identique à app.py, pour la cohérence) ---
st.markdown("""
<style>
/* ... Copiez-collez l'intégralité du bloc CSS de votre fichier app.py ici ... */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
body { background-color: #0E1117; color: #FAFAFA; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
.main-title { font-size: 2.5rem; font-weight: 700; color: #FFFFFF; text-align: center; margin-bottom: 1rem; text-shadow: 0 0 10px rgba(0, 150, 255, 0.5); }
.sidebar .sidebar-content { background-color: #262730; }
.twin-container { display: flex; align-items: center; justify-content: center; gap: 40px; padding: 20px; }
.twin-svg-container { flex: 1; text-align: center; }
.twin-data-container { flex: 1; background-color: #262730; border-radius: 12px; padding: 20px; border: 1px solid #434654; }
.component-detail { background-color: #1e1f26; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
.metric { display: flex; justify-content: space-between; margin-bottom: 10px; }
.metric-label { color: #B0B3B8; }
.metric-value { font-weight: 700; color: #FFFFFF; }
.health-good { color: #00FF7F; }
.health-warning { color: #FFD700; }
.health-critical { color: #FF4500; }
</style>
""", unsafe_allow_html=True)


# --- Classe AssetData (identique, pour la cohérence) ---
# ... Copiez-collez la classe AssetData complète depuis app.py ici ...
class AssetData:
    # ... (tout le code de la classe AssetData) ...
    def __init__(self, name, icon, initial_health=95):
        self.name = name
        self.icon = icon
        self.health = initial_health
        self.previous_health = initial_health
        self.temp = random.uniform(75, 85)
        self.vibration = random.uniform(2.0, 4.0)
        self.status = "Operational"
        self.last_status = "Operational"
        self.degradation_rate = random.uniform(0.05, 0.15)
        self.anomaly_chance = 0.02
        self.active_alerts = []
        self.load_factor = 1.0 # Nouveau pour la simulation

    def update(self):
        self.previous_health = self.health
        # Le taux de dégradation est maintenant affecté par la charge
        self.health -= self.degradation_rate * self.load_factor
        self.health = max(0, self.health)

        if random.random() < self.anomaly_chance:
            self.vibration += random.uniform(5, 8)
        else:
            self.vibration = (2.0 + (100 - self.health) * 0.1) * self.load_factor + random.uniform(-0.5, 0.5)
            self.temp = (75 + (100 - self.health) * 0.5) * self.load_factor + random.uniform(-2, 2)

        self._check_and_generate_alerts()
        self.last_status = self.status

    def _check_and_generate_alerts(self):
        self.active_alerts = []
        new_status = "Operational"
        if self.health > 80: new_status = "Operational"
        elif self.health > 50: new_status = "Anomaly Detected"
        elif self.health > 20: new_status = "Maintenance Required"
        else: new_status = "Imminent Failure"
        
        if new_status != self.last_status:
            if new_status == "Imminent Failure": self.add_event("error", f"Imminent failure predicted for {self.name}!")
            elif new_status == "Maintenance Required": self.add_event("error", f"Critical state reached on {self.name}.")
            elif new_status == "Anomaly Detected": self.add_event("warning", f"Performance anomaly detected on {self.name}.")
            elif new_status == "Operational" and self.last_status != "Operational": self.add_event("success", f"{self.name} is back to operational status.")
        self.status = new_status

    def trigger_catastrophic_failure(self):
        self.health = 5; self.vibration = 15.0; self.temp = 150.0; self.status = "Imminent Failure"
        self.add_event("error", f"Catastrophic failure SIMULATED on {self.name}!")
        st.toast(f"🚨 CATASTROPHIC FAILURE on {self.name}!", icon="🚨")

    def perform_maintenance(self):
        self.health = random.randint(92, 99); self.temp = random.uniform(75, 80); self.vibration = random.uniform(2.0, 3.5)
        self.status = "Operational (Post-Maintenance)"; self.degradation_rate = random.uniform(0.05, 0.15)
        self.active_alerts = []; self.add_event("success", f"Maintenance successfully performed on {self.name}.")

    def add_event(self, level, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        event = {"time": timestamp, "level": level, "message": message}
        st.session_state.event_log.insert(0, event)

# --- Initialisation de l'état (si nécessaire) ---
if 'assets' not in st.session_state:
    st.session_state.assets = {
        "P-101": AssetData("Centrifugal Pump P-101", "fa-oil-can", initial_health=90),
        "C-205": AssetData("Compressor C-205", "fa-wind", initial_health=75),
        "T-310": AssetData("Gas Turbine T-310", "fa-fan", initial_health=60),
        "R-420": AssetData("Chemical Reactor R-420", "fa-flask", initial_health=98),
    }
if 'event_log' not in st.session_state:
    st.session_state.event_log = []

# --- Logique de la page du Jumeau Numérique ---

st.markdown('<h1 class="main-title">PIONIER - Digital Twin</h1>', unsafe_allow_html=True)

# --- Sélection de l'actif pour le jumeau ---
selected_asset_key = st.sidebar.selectbox("Select an Asset for Twin View:", list(st.session_state.assets.keys()))
asset = st.session_state.assets[selected_asset_key]

# --- Panneau de Contrôle du Jumeau Numérique ---
st.sidebar.title("🔬 Twin Simulation Controls")

# Simulation "What-If"
st.sidebar.markdown("### ⚙️ What-If Scenario")
load_increase = st.sidebar.slider("Increase Load Factor:", 0.0, 2.0, 0.0, 0.1)
asset.load_factor = 1.0 + load_increase

if st.sidebar.button("Apply Load Change", type="primary"):
    st.sidebar.success(f"Load factor set to {asset.load_factor:.1f}x")
    st.rerun()

st.sidebar.markdown("---")
if st.sidebar.button("Trigger Maintenance", use_container_width=True):
    asset.perform_maintenance()
    st.rerun()
if st.sidebar.button("Simulate Failure", use_container_width=True):
    asset.trigger_catastrophic_failure()
    st.rerun()

# --- Mise à jour de l'actif en temps réel ---
asset.update()

# --- Affichage du Jumeau Numérique ---
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown('<div class="twin-svg-container">', unsafe_allow_html=True)
    
    # Définir les couleurs des composants en fonction des données
    motor_color = "health-good" if asset.temp < 100 else ("health-warning" if asset.temp < 120 else "health-critical")
    bearing_color = "health-good" if asset.vibration < 5 else ("health-warning" if asset.vibration < 8 else "health-critical")
    impeller_color = "health-good" if asset.health > 50 else ("health-warning" if asset.health > 20 else "health-critical")

    # SVG de la pompe
    st.markdown(f"""
    <svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
        <style> .health-good {{ fill: #00FF7F; }} .health-warning {{ fill: #FFD700; }} .health-critical {{ fill: #FF4500; }} </style>
        <rect x="50" y="150" width="120" height="100" rx="10" class="{motor_color}" stroke="#fff" stroke-width="2"/>
        <text x="110" y="205" text-anchor="middle" fill="white" font-family="Arial" font-size="14" font-weight="bold">MOTOR</text>
        <circle cx="250" cy="200" r="60" class="{bearing_color}" stroke="#fff" stroke-width="2"/>
        <text x="250" y="205" text-anchor="middle" fill="white" font-family="Arial" font-size="14" font-weight="bold">BEARING</text>
        <path d="M 320 200 L 360 180 L 360 220 Z" class="{impeller_color}" stroke="#fff" stroke-width="2"/>
        <text x="340" y="235" text-anchor="middle" fill="white" font-family="Arial" font-size="12">IMPELLER</text>
        <line x1="170" y1="200" x2="190" y2="200" stroke="white" stroke-width="4"/>
    </svg>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="twin-data-container">', unsafe_allow_html=True)
    st.markdown("### Asset Health & Status")
    st.metric("Overall AI Health", f"{asset.health:.1f}%", delta=f"{asset.health - asset.previous_health:.1f}%")
    st.metric("Status", asset.status)
    
    st.markdown("---")
    st.markdown("### Component-Level Data")
    
    # Détails du moteur
    st.markdown(f"""
    <div class="component-detail">
        <h4>⚙️ Motor</h4>
        <div class="metric"><span class="metric-label">Temperature:</span><span class="metric-value {motor_color}">{asset.temp:.1f} °C</span></div>
        <div class="metric"><span class="metric-label">Load Factor:</span><span class="metric-value">{asset.load_factor:.1f}x</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Détails du roulement
    st.markdown(f"""
    <div class="component-detail">
        <h4>🔄 Bearing</h4>
        <div class="metric"><span class="metric-label">Vibration:</span><span class="metric-value {bearing_color}">{asset.vibration:.2f} mm/s</span></div>
        <div class="metric"><span class="metric-label">Friction:</span><span class="metric-value">Normal</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Détails de la turbine
    st.markdown(f"""
    <div class="component-detail">
        <h4>💨 Impeller</h4>
        <div class="metric"><span class="metric-label">Imbalance:</span><span class="metric-value {impeller_color}">Low</span></div>
        <div class="metric"><span class="metric-label">RPM:</span><span class="metric-value">1800</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


# --- Boucle de simulation ---
st.caption(f"Last update: {time.strftime('%H:%M:%S')}")
time.sleep(3)
st.rerun()
