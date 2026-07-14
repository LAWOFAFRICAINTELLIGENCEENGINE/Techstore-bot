import streamlit as st
from groq import Groq
import json
import pandas as pd

# 1. Infrastructure Config & CSS
st.set_page_config(page_title="TechStore Infrastructure", page_icon="🛍️", layout="wide")

st.markdown("""
<style>
[data-testid="stChatInputSubmitButton"] {
    background-color: #1EBE55 !important;
    color: white !important;
    border-radius: 50% !important;
}
</style>
""", unsafe_allow_html=True)

# 2. Initialize State & Telemetry Trackers
if "messages" not in st.session_state:
    st.session_state.messages = []
if "query_count" not in st.session_state:
    st.session_state.query_count = 0 # Tracks how many questions the AI answers

# 3. Dynamic Inventory Architecture (The Real-World Data)
warehouse_database = {
    "MacBook Pro M3": {"Price (USD)": 1999, "Stock Level": 14, "Status": "In Stock"},
    "Samsung Galaxy S24": {"Price (USD)": 999, "Stock Level": 0, "Status": "Backordered"},
    "Sony WH-1000XM5": {"Price (USD)": 349, "Stock Level": 42, "Status": "In Stock"},
    "Dell XPS 15": {"Price (USD)": 1599, "Stock Level": 3, "Status": "Low Stock WARNING"}
}
inventory_json = json.dumps(warehouse_database, indent=2)

# ==========================================
# 4. MULTI-NODE ROUTING (The Sidebar)
# ==========================================
with st.sidebar:
    st.title("🎛️ System Routing")
    st.write("Select computational node:")
    
    # This creates the toggle to switch between departments
    active_node = st.radio("Active Node", ["Support Node 🎧", "Sales Node 🛒", "Admin Telemetry 📊"])
    
    st.divider()
    if st.button("🗑️ Terminate Session"):
        st.session_state.messages = []
        st.rerun()

# ==========================================
# 5. ADMIN TELEMETRY DASHBOARD
# ==========================================
if active_node == "Admin Telemetry 📊":
    st.title("📊 Executive Telemetry Dashboard")
    st.write("Secure infrastructure metrics and warehouse data.")
    
    # Create 3 columns for professional metric tracking
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total AI Queries Processed", value=st.session_state.query_count)
    col2.metric(label="Active Sessions", value="1 (You)")
    col3.metric(label="System Latency", value="<12ms")
    
    st.divider()
    
    st.subheader("📦 Live Warehouse Inventory")
    # Convert our Python dictionary into a beautiful visual table using pandas
    df = pd.DataFrame.from_dict(warehouse_database, orient='index')
    st.dataframe(df, use_container_width=True)

# ==========================================
# 6. SALES & SUPPORT AI INTERFACE
# ==========================================
else: 
    st.title(f"TechStore {active_node}")
    
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except Exception:
        st.error("Authentication Error: Missing API Credentials.")
        st.stop()

    # Dynamic System Prompts based on which node the user selected
    if active_node == "Support Node 🎧":
        system_directive = f"""You are the TechStore Support Node. Your strict objective is to handle returns, warranties, and complaints. 
        Rules: 30-day returns, 15% restocking fee on unsealed items.
        LIVE INVENTORY DATA: {inventory_json}"""
    else:
        system_directive = f"""You are the TechStore Sales Node. Your strict objective is to upsell, explain product specs, and encourage purchases. Be highly enthusiastic.
        LIVE INVENTORY DATA: {inventory_json}"""
        
    system_prompt = {"role": "system", "content": system_directive}

    # Draw previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Engine Input
    prompt = st.chat_input("Input parameters or query here...")

    if prompt:
        # Increase the query counter for the Admin Dashboard!
        st.session_state.query_count += 1
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            conversation_history = [system_prompt] + st.session_state.messages
            
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=conversation_history,
                temperature=0.2 
            )
            
            system_answer = response.choices[0].message.content
            st.write(system_answer)
            
        st.session_state.messages.append({"role": "assistant", "content": system_answer})
        st.rerun()

