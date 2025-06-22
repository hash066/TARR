import streamlit as st
import requests
import os
import sys
import plotly.graph_objects as go
from datetime import datetime
import time

# Enable import from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from blockchain.log_to_chain import log_failure_to_chain, confirm_repair, release_payment
from blockchain.failures import get_all_failures
from blockchain.send_sms import send_alert

st.set_page_config(page_title="TAR Smart Dashboard", layout="wide")

# Fetch function
def fetch_data():
    try:
        response = requests.get("https://tarr-thermobackend.onrender.com/data")
        return response.json()
    except:
        return {}

# Auto Monitor State
if "failure_logged" not in st.session_state:
    st.session_state.failure_logged = False
if "repair_confirmed" not in st.session_state:
    st.session_state.repair_confirmed = False

# ----------------------------
# LOGIN PAGE
# ----------------------------
if "role" not in st.session_state:
    st.session_state.role = None

if st.session_state.role is None:
    hide_sidebar = """
        <style>
        [data-testid="stSidebar"] { display: none; }
        footer {visibility: hidden;}
        </style>
    """
    st.markdown(hide_sidebar, unsafe_allow_html=True)

    st.markdown("""
        <div style='display:flex; flex-direction:column; align-items:center; justify-content:center; height:85vh;'>
            <h1 style='font-size: 3em;'>Welcome to TAR Smart Dashboard</h1>
            <p style='font-size:1.2em;'>Choose your role to continue</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("👤 I'm a Client", use_container_width=True):
            st.session_state.role = "Client"
            st.rerun()
    with col2:
        if st.button("🏭 I'm the Company", use_container_width=True):
            st.session_state.role = "Company"
            st.rerun()

else:
    st.sidebar.title("🢨 TAR Dashboard")
    st.sidebar.write(f"**Logged in as:** `{st.session_state.role}`")
    menu = st.sidebar.radio("Navigation", ["Live Monitor", "Log Issue", "Company Repair Panel", "Automated Faults & History", "Logout"])

    if menu == "Logout":
        st.session_state.role = None
        st.rerun()

    data = fetch_data()

    if menu == "Live Monitor":
        st.subheader("📡 Real-Time Monitoring")
        if data:
            hot = data["hot"]
            cold = data["cold"]
            delta_t = round(hot - cold, 2)
            power = data["power"]
            pressure = data["pressure"]

            st.metric("Hot Temp (°C)", hot)
            st.metric("Cold Temp (°C)", cold)
            st.metric("ΔT (°C)", delta_t)
            st.metric("Power Usage (W)", power)
            st.metric("Acoustic Pressure (Pa)", pressure)

            time_range = list(range(20))
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=time_range, y=[hot]*20, name="Hot", line=dict(color="red")))
            fig.add_trace(go.Scatter(x=time_range, y=[cold]*20, name="Cold", line=dict(color="blue")))
            fig.add_trace(go.Scatter(x=time_range, y=[delta_t]*20, name="ΔT", line=dict(color="orange")))
            fig.update_layout(title="Temperature Graph", xaxis_title="Time", yaxis_title="°C")
            st.plotly_chart(fig, use_container_width=True)

            # Automatic logic
            if delta_t < 2.0 and not st.session_state.failure_logged:
                log_failure_to_chain("Auto Detected Cooling Failure", delta_t)
                send_alert("Auto Detected Cooling Failure", delta_t)
                st.session_state.failure_logged = True
                st.session_state.repair_confirmed = False
                st.warning("❌ Cooling failure detected and logged automatically.")

            if delta_t > 5.0 and st.session_state.failure_logged and not st.session_state.repair_confirmed:
                confirm_repair()
                release_payment()
                st.session_state.repair_confirmed = True
                st.session_state.failure_logged = False
                st.success("✅ Repair confirmed and payment released automatically.")

        else:
            st.warning("⚠️ Backend not reachable")

    elif menu == "Log Issue" and st.session_state.role == "Client":
        st.subheader("📢 Report a Failure")
        reason = st.text_input("Enter issue description")
        delta_t = st.number_input("ΔT reading", min_value=0.0, step=0.1)
        if st.button("🔗 Log to Blockchain"):
            log_failure_to_chain(reason or "Cooling failure", delta_t)
            send_alert(reason or "Cooling failure", delta_t)
            st.success("✅ Logged on-chain & SMS sent!")

    elif menu == "Company Repair Panel" and st.session_state.role == "Company":
        st.subheader("🛠️ Company Repair Dashboard")
        failures = get_all_failures()
        if failures:
            for i, log in enumerate(failures[::-1]):
                with st.expander(f"Failure #{len(failures) - i} from {log['sender']}"):
                    st.markdown(f"**Reason:** {log['reason']}")
                    st.markdown(f"**ΔT:** {log['deltaT']} °C")
                    ts = datetime.fromtimestamp(log['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                    st.markdown(f"**Timestamp:** {ts}")
                    if st.button(f"✅ Confirm Repair", key=f"repair_{i}"):
                        confirm_repair()
                    if st.button(f"💸 Release Payment", key=f"pay_{i}"):
                        release_payment()
        else:
            st.info("🎉 No failures logged yet.")

    elif menu == "Automated Faults & History":
        st.subheader("📜 Smart Contract Repair History")
        failures = get_all_failures()
        if failures:
            for i, log in enumerate(failures[::-1]):
                st.markdown("---")
                st.markdown(f"### Issue #{len(failures) - i}")
                st.markdown(f"- Sender: `{log['sender']}`")
                st.markdown(f"- Reason: `{log['reason']}`")
                st.markdown(f"- ΔT: `{log['deltaT']} °C`")
                ts = datetime.fromtimestamp(log['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                st.markdown(f"- Logged At: `{ts}`")
        else:
            st.info("📦 No logs yet.")
