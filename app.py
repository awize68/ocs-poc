# app.py (Version sans authentification)
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import data_services as ds

# --- Configuration de la page ---
st.set_page_config(
    page_title="OCS Cognitive Layer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Fonctions pour afficher le contenu (inchangées) ---
def show_energy_dashboard():
    st.header("⚡ Energy Consumption (Last 24h)")
    energy_data = ds.get_realistic_energy_metrics()
    df = pd.DataFrame([{
        "Time": d.timestamp.strftime("%H:%M"),
        "Consumption (kWh)": d.value_kwh
    } for d in energy_data])
    
    fig = px.line(df, x="Time", y="Consumption (kWh)", title='Real-time Energy Profile')
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

def show_maintenance_alerts():
    st.header("🔧 Predictive Maintenance Alerts")
    alerts = ds.get_maintenance_alerts()
    for alert in alerts:
        severity = "🔴 Critical" if alert.probability > 0.8 else "🟡 Warning"
        with st.expander(f"{severity} | {alert.equipment_id}"):
            st.write(f"**Issue:** {alert.alert_type}")
            st.write(f"**Details:** {alert.message}")
            st.write(f"**Failure Probability:** {alert.probability:.0%}")
            st.write(f"**Estimated Failure Date:** {alert.predicted_failure_date.strftime('%Y-%m-%d')}")

def show_security_events():
    st.header("🛡️ Recent Security Events")
    events = ds.get_security_events()
    for event in events:
        severity_icon = "🔴" if event.severity == "High" else "🟡"
        with st.expander(f"{severity_icon} | {event.event_type} at {event.location}"):
            st.write(f"**Description:** {event.description}")
            st.write(f"**Timestamp:** {event.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")


# --- Logique Principale de l'Application (SIMPLIFIÉE) ---
# Toute la logique de `check_password` a été supprimée.

st.title("OCS Cognitive Layer Dashboard")
#st.markdown("Welcome to the Digital Twin control center for your building.")
st.markdown('<h1 class="main-title">PIONIER - Fleet Overview</h1>', unsafe_allow_html=True)
# Utiliser des colonnes pour une mise en page
col1, col2 = st.columns(2)

with col1:
    with st.expander("📊 Energy Analytics", expanded=True):
        show_energy_dashboard()

with col2:
    with st.expander("🔧 Maintenance Alerts", expanded=True):
        show_maintenance_alerts()

# La section sécurité peut prendre toute la largeur
st.divider()
with st.expander("🛡️ Security Events", expanded=True):
    show_security_events()
