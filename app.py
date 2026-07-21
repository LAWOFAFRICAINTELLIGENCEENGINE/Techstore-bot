import streamlit as st
from groq import Groq
import google.generativeai as genai
from openai import OpenAI
import json
import pandas as pd
import traceback

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
