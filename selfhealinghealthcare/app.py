import streamlit as st
import os
import time
import psutil
import plotly.graph_objects as go
import datetime


st.set_page_config(page_title="Healthcare Dashboard", layout="wide")


st.markdown("""
<style>

/* REMOVE TOP SPACE */
.block-container {
    padding-top: 1rem !important;
}

/* REMOVE HEADER SPACE */
header {visibility: hidden;}

/* MAIN BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #ff9a9e, #fad0c4);
    color: black;
}

/* SIDEBAR STYLE */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ff758c, #ff7eb3);
    color: white;
}

/* SIDEBAR TEXT */
[data-testid="stSidebar"] * {
    color: white !important;
}

/* TEXT AREA */
textarea {
    color: black !important;
    background-color: #ffffff !important;
    border-radius: 10px;
}

/* KPI CARDS */
div[data-testid="stMetric"] {
    background-color: rgba(255,255,255,0.6);
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)
# TITLE
st.title("💗 AI Self-Healing Healthcare Dashboard")

st.sidebar.title("⚙️ Controls")

process_name = "notepad.exe"

if "running" not in st.session_state:
    st.session_state.running = False
if "logs" not in st.session_state:
    st.session_state.logs = []
if "cpu_data" not in st.session_state:
    st.session_state.cpu_data = []

# BUTTONS
if st.sidebar.button("▶ Start Monitoring"):
    st.session_state.running = True
    st.toast("Monitoring Started 💗")

if st.sidebar.button("⏹ Stop Monitoring"):
    st.session_state.running = False
    st.toast("Monitoring Stopped 🛑")

def is_running():
    tasks = os.popen('tasklist').read().lower()
    return process_name.lower() in tasks

col1, col2, col3 = st.columns(3)

cpu = psutil.cpu_percent()
memory = psutil.virtual_memory().percent

col1.metric("CPU Usage", f"{cpu}%")
col2.metric("Memory Usage", f"{memory}%")

status = "STOPPED"
if st.session_state.running:
    status = "RUNNING"

col3.metric("System Status", status)

if st.session_state.running:
    if not is_running():
        st.error("🔴 Service Down → Restarting...")
        st.toast("🚨 Restarting Service!", icon="🚨")

        os.system("start notepad")

        st.session_state.logs.append(
            f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ❌ Restarted Notepad"
        )
    else:
        st.success("🟢 Service Running")

        st.session_state.logs.append(
            f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ✔ System OK"
        )

st.subheader("💗 CPU Usage Monitor")

gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=cpu,
    title={'text': "CPU Usage"},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "#ff4d6d"},
        'steps': [
            {'range': [0, 50], 'color': "#ffc0cb"},
            {'range': [50, 80], 'color': "#ff85a2"},
            {'range': [80, 100], 'color': "#ff4d6d"},
        ],
    }
))

gauge.update_layout(
    height=250,
    margin=dict(l=10, r=10, t=40, b=10)
)

st.plotly_chart(gauge, use_container_width=True)



st.subheader("📜 System Logs")

if st.session_state.logs:
    st.code("\n".join(st.session_state.logs[-15:]), language="bash")
else:
    st.info("No logs yet...")

time.sleep(2)
st.rerun()