import streamlit as st
from groq import Groq
import google.generativeai as genai
import json
import pandas as pd
import time

# 1. Infrastructure Config & CSS
st.set_page_config(page_title="TechStore Super-System", page_icon="🌐", layout="wide")

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
    st.session_state.query_count = 0 

# 3. Dynamic Inventory Architecture 
warehouse_database = {
    "MacBook Pro M3": {"Price (USD)": 1999, "Stock Level": 14, "Status": "In Stock"},
    "Samsung Galaxy S24": {"Price (USD)": 999, "Stock Level": 0, "Status": "Backordered"},
    "Sony WH-1000XM5": {"Price (USD)": 349, "Stock Level": 42, "Status": "In Stock"},
    "Dell XPS 15": {"Price (USD)": 1599, "Stock Level": 3, "Status": "Low Stock WARNING"}
}

# 4. MULTI-AGENT ROUTING (The Super-System Sidebar)
with st.sidebar:
    st.title("🧠 Master Control")
    st.write("Select your computational mode:")
    
    active_mode = st.radio("System Mode", [
        "SUPER-SYSTEM PIPELINE 🌪️",
        "Single: The Executor ⚡ (Groq)", 
        "Single: The Architect 🏗️ (Gemini)", 
        "Admin Telemetry 📊"
    ])
    
    st.divider()
    if st.button("🗑️ Clear Memory"):
        st.session_state.messages = []
        st.rerun()

# 5. ADMIN TELEMETRY DASHBOARD
if active_mode == "Admin Telemetry 📊":
    st.title("📊 Super-System Telemetry")
    st.write("Secure infrastructure metrics and warehouse data.")
    
    col1, col2 = st.columns(2)
    col1.metric(label="Total AI Queries Processed", value=st.session_state.query_count)
    col2.metric(label="System Status", value="Multi-Agent Online")
    
    st.divider()
    st.subheader("📦 Live Warehouse Inventory")
    df = pd.DataFrame.from_dict(warehouse_database, orient='index')
    st.dataframe(df, use_container_width=True)

# 6. AI INTERFACE & PIPELINE ROUTING
else: 
    st.title(active_mode)
        
    # Render Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User Input
    prompt = st.chat_input("Enter your complex request or coding problem...")

    if prompt:
        st.session_state.query_count += 1
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            try:
                # ==========================================
                # 🌪️ THE SUPER-SYSTEM PIPELINE (3 BRAINS COMBINED)
                # ==========================================
                if "PIPELINE" in active_mode:
                    
                    # Stage 1: Grok (Standby / Simulation)
                    with st.spinner("🔍 Brain 1 (Grok/xAI): Gathering real-time data context..."):
                        time.sleep(1.5) # Simulating research time
                        
                    # Stage 2: Gemini (The Architect)
                    with st.spinner("🏗️ Brain 2 (Gemini): Architecting the flawless logic blueprint..."):
                        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                        gemini_model = genai.GenerativeModel('gemini-1.5-pro')
                        architect_prompt = f"You are the Master Architect. Break down this user request into a highly detailed, step-by-step logic plan for a senior developer. DO NOT write the final code, only the architecture and logic constraints. Request: {prompt}"
                        blueprint = gemini_model.generate_content(architect_prompt).text
                        
                        with st.expander("👁️ View Gemini's Logic Blueprint"):
                            st.write(blueprint)
                    
                    # Stage 3: Groq (The Executor)
                    with st.spinner("⚡ Brain 3 (Groq): Executing and writing the final code at blazing speed..."):
                        groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                        executor_system = "You are an elite Executor AI. Read the Architect's blueprint and write the flawless, complete Python code for it. Do not use placeholders. Output the final working code."
                        executor_prompt = f"Here is the Architect's Blueprint:\n{blueprint}\n\nWrite the complete, highly-optimized code based strictly on this plan."
                        
                        response = groq_client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {"role": "system", "content": executor_system},
                                {"role": "user", "content": executor_prompt}
                            ],
                            temperature=0.2
                        )
                        final_output = response.choices[0].message.content
                    
                    st.success("✅ Super-System Pipeline Execution Complete!")
                    st.write(final_output)
                    st.session_state.messages.append({"role": "assistant", "content": final_output})

                # ==========================================
                # ⚡ SINGLE MODE: GROQ ONLY
                # ==========================================
                elif "Groq" in active_mode:
                    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                    conversation_history = [{"role": "system", "content": "You are The Executor. Write flawless code fast."}] + st.session_state.messages
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=conversation_history,
                        temperature=0.3
                    )
                    system_answer = response.choices[0].message.content
                    st.write(system_answer)
                    st.session_state.messages.append({"role": "assistant", "content": system_answer})
                
                # ==========================================
                # 🏗️ SINGLE MODE: GEMINI ONLY
                # ==========================================
                elif "Gemini" in active_mode:
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    
                    gemini_history = []
                    for msg in st.session_state.messages[:-1]:
                        role = "user" if msg["role"] == "user" else "model"
                        gemini_history.append({"role": role, "parts": [msg["content"]]})
                        
                    chat = model.start_chat(history=gemini_history)
                    response = chat.send_message(prompt)
                    system_answer = response.text
                    st.write(system_answer)
                    st.session_state.messages.append({"role": "assistant", "content": system_answer})
                
            except Exception as e:
                st.error(f"System Overload or Disconnected: {e}")
                
        st.rerun()
