import streamlit as st
import json
import pandas as pd
import traceback

from groq import Groq
import google.generativeai as genai
from openai import OpenAI

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="TechStore Universal Super-System",
    page_icon="🌪️",
    layout="wide"
)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "query_count" not in st.session_state:
    st.session_state.query_count = 0

# -------------------------------------------------
# SYSTEM HEALTH
# -------------------------------------------------

if "system_health" not in st.session_state:
    st.session_state.system_health = {
        "status": "Online",
        "last_check": "Not Checked",
        "response_time": 0.0,
        "last_error": "None",
        "brains": {
            "xai": "Unknown",
            "gemini": "Unknown",
            "groq": "Unknown"
        }
    }

# -------------------------------------------------
# INVENTORY DATABASE
# -------------------------------------------------

warehouse_database = {
    "MacBook Pro M3": {
        "Price (USD)": 1999,
        "Stock Level": 14,
        "Status": "In Stock"
    },
    "Samsung Galaxy S24": {
        "Price (USD)": 999,
        "Stock Level": 0,
        "Status": "Backordered"
    },
    "Sony WH-1000XM5": {
        "Price (USD)": 349,
        "Stock Level": 42,
        "Status": "In Stock"
    },
    "Dell XPS 15": {
        "Price (USD)": 1599,
        "Stock Level": 3,
        "Status": "Low Stock Warning"
    }
}

inventory_json = json.dumps(warehouse_database, indent=2)

# =====================================================
# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.title("🌪️ Omni-Control")

    st.success("🟢 TechStore Universal Super-System Online")

    st.divider()

    st.markdown("### 🩺 Health Monitor")
    st.success("Always Active")

    st.markdown("### 📦 Inventory")
    st.success("Always Active")

    st.markdown("### 🛠️ Admin Mode")
    st.success("Always Active")

    st.divider()

    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()
        
# =====================================================
# MAIN INTERFACE
# =====================================================

st.title("🌪️ TechStore Universal Super-System")

st.caption(
    "An intelligent AI assistant for coding, research, business, writing, automation and problem solving."
)

# =====================================================
# HEALTH MONITOR
# =====================================================

health = st.session_state.system_health

col1, col2 = st.columns(2)

col1.metric("System Status", health["status"])
col2.metric("Queries", st.session_state.query_count)

st.metric("Last Check", health["last_check"])
st.metric("Response Time", f'{health["response_time"]:.2f}s')
st.metric("Last Error", health["last_error"])

# =====================================================
# INVENTORY
# =====================================================

if show_inventory:

    df = pd.DataFrame.from_dict(
        warehouse_database,
        orient="index"
    )

    st.dataframe(df, use_container_width=True)

# =====================================================
# ADMIN MODE
# =====================================================

if show_admin:

    st.subheader("Developer Dashboard")

    st.json(st.session_state.system_health)

# =====================================================
# CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

prompt = st.chat_input(
    "Ask TechStore Universal Super-System anything..."
)

# =====================================================
# AI INITIALIZATION
# =====================================================

xai_client = None
groq_client = None
gemini_model = None

# xAI
try:
    xai_client = OpenAI(
        api_key=st.secrets["XAI_API_KEY"],
        base_url="https://api.x.ai/v1"
    )
    st.session_state.system_health["brains"]["xai"] = "Online"
except Exception as e:
    st.session_state.system_health["brains"]["xai"] = "Offline"
    st.session_state.system_health["last_error"] = str(e)

# Gemini
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    gemini_model = genai.GenerativeModel("gemini-1.5-pro")
    st.session_state.system_health["brains"]["gemini"] = "Online"
except Exception as e:
    st.session_state.system_health["brains"]["gemini"] = "Offline"
    st.session_state.system_health["last_error"] = str(e)

# Groq
try:
    groq_client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )
    st.session_state.system_health["brains"]["groq"] = "Online"
except Exception as e:
    st.session_state.system_health["brains"]["groq"] = "Offline"
    st.session_state.system_health["last_error"] = str(e)

st.session_state.system_health["last_check"] = "Completed"

brains = st.session_state.system_health["brains"]

if (
    brains["xai"] == "Online"
    and brains["gemini"] == "Online"
    and brains["groq"] == "Online"
):
    st.session_state.system_health["status"] = "All AI Providers Online"
else:
    st.session_state.system_health["status"] = "Running with Available Providers"
