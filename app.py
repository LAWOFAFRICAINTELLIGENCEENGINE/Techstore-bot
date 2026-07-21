import streamlit as st
from groq import Groq
import google.generativeai as genai
from openai import OpenAI
import json
import pandas as pd
import traceback

1. Infrastructure Config & CSS

st.set_page_config(page_title="TechStore Omni-System", page_icon="🌪️", layout="wide")
st.markdown("""

<style>  
/* --- CUSTOM SEND BUTTON (Green + Arrow with Sparkle) --- */  
[data-testid="stChatInputSubmitButton"] {  
    background-color: #1EBE55 !important;  
    border-radius: 50% !important;  
    display: flex !important;  
    align-items: center !important;  
    justify-content: center !important;  
}  
/* Hide the default Streamlit plane icon */  
[data-testid="stChatInputSubmitButton"] svg {  
    display: none !important;  
}  
/* Inject the custom Sparkle + Hollow Arrow Icon */  
[data-testid="stChatInputSubmitButton"]::after {  
    content: '';  
    display: inline-block;  
    width: 20px;  
    height: 20px;  
    background-image: url("data:image/svg+xml,%3Csvg xmlns='[http://www.w3.org/2000/svg](http://www.w3.org/2000/svg)' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M22 2L11 13' /%3E%3Cpath d='M22 2l-7 20-4-9-9-4 20-7z' /%3E%3Cpath d='M5 13l1 2 2 1-2 1-1 2-1-2-2-1 2-1 1-2z' fill='white' stroke='none' /%3E%3C/svg%3E");  
    background-size: contain;  
    background-repeat: no-repeat;  
    background-position: center;  
}  
/* --- CUSTOM 3-DOTS APP MENU --- */  
/* Hide the default Streamlit hamburger menu */  
[data-testid="baseButton-header"] svg {  
    display: none !important;  
}  
/* Inject 3 vertical dots */  
[data-testid="baseButton-header"]::after {  
    content: '\\22EE';   
    font-size: 26px;  
    font-weight: bold;  
    color: inherit;  
    display: flex;  
    align-items: center;  
    justify-content: center;  
    padding-bottom: 4px;  
}  
</style>  """, unsafe_allow_html=True)

# 2. Initialize State & Telemetry Trackers 

if "messages" not in 
st.session_state:
    st.session_state.messages = []

if "query_count" not in 
st.session_state:
    st.session_state.query_count = 0 

3. Dynamic Inventory Architecture 

warehouse_database = {
    "MacBook Pro M3": {"Price (USD)": 1999, "Stock Level": 14, "Status": "In Stock"},
    "Samsung Galaxy S24": {"Price (USD)": 999, "Stock Level": 0, "Status": "Backordered"},
    "Sony WH-1000XM5": {"Price (USD)": 349, "Stock Level": 42, "Status": "In Stock"},
    "Dell XPS 15": {"Price (USD)": 1599, "Stock Level": 3, "Status": "Low Stock WARNING"}
}
inventory_json = json.dumps(warehouse_database, indent=2)

4. MASTER CONTROL (Simplified Sidebar)

with st.sidebar:
    st.title("🧠 Omni-Control")
    st.write("The 3-Brain Super-System handles all routing automatically.")
    
    st.divider()
    show_telemetry = st.toggle("📊 View Admin Telemetry")
    
    st.divider()
    if st.button("🗑️ Clear System Memory"):
        st.session_state.messages = []
        st.rerun()

5. ADMIN TELEMETRY DASHBOARD

if show_telemetry:
    st.title("📊 Super-System Telemetry")
    st.write("Secure infrastructure metrics and warehouse data.")
    
    col1, col2 = st.columns(2)
    col1.metric(label="Total AI Queries Processed", value=st.session_state.query_count)
    col2.metric(label="System Status", value="3-Brain Omni-Pipeline Online")
    
    st.divider()
    st.subheader("📦 Live Warehouse Inventory")
    df = pd.DataFrame.from_dict(warehouse_database, orient='index')
    st.dataframe(df, use_container_width=True)

6. UNIVERSAL SUPER-SYSTEM INTERFACE

else: 
    st.title("TechStore Universal Super-System 🌪️")
        
    # Render Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    # User Input
    prompt = st.chat_input("Enter your command for the Omni-System...")
    if prompt:
        # Update Telemetry & Save User Prompt
        st.session_state.query_count += 1
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            try:
                # ==============================================================
                # STAGE 1: GROK (xAI) - THE RESEARCHER & CONTEXT ENGINE
                # ==============================================================
                with st.spinner("🔍 Brain 1 (Grok/xAI): Analyzing initial parameters..."):
                    try:
                        xai_client = OpenAI(
    api_key=st.secrets["XAI_API_KEY"],
    base_url="https://api.x.ai/v1",
        )

                        grok_response = xai_client.chat.completions.create(
                            model="grok-beta",
                            messages=[
                                {"role": "system", "content": "You are Brain 1 of an elite CTO Omni-System. Analyze the user's prompt. Provide maximum context, identify edge cases, and give unfiltered structural advice."},
                                {"role": "user", "content": prompt}
                            ],
                            max_tokens=4000
                        )
                        grok_context = grok_response.choices[0].message.content
                    except Exception as e:
                        grok_context = f"Grok Bypass: xAI API key missing or invalid. Proceeding with base prompt. Error: {e}"
                    with st.expander("👁️ View Brain 1 (Grok) Context Analysis"):
                        st.write(grok_context)
                # ==============================================================
                # STAGE 2: GEMINI - THE MASTER ARCHITECT
                # ==============================================================
                with st.spinner("🏗️ Brain 2 (Gemini): Architecting response strategy..."):
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    gemini_model = genai.GenerativeModel('gemini-1.5-pro')
                    
                    architect_prompt = f"""You are Brain 2, the Master Architect. 
                    LIVE INVENTORY DATA: {inventory_json}
                    
                    USER REQUEST: "{prompt}"
                    GROK'S ANALYSIS: "{grok_context}"
                    
                    INSTRUCTIONS:
                    Synthesize the user request and Grok's analysis.
                    1. If it is a STORE QUERY: Draft a strategy on how to answer politely based on live inventory.
                    2. If it is a CODING/ENGINEERING QUERY: Draft an unlimited, highly detailed, step-by-step logic blueprint.
                    DO NOT write the final code. Only write the internal logic strategy."""
                    
                    blueprint = gemini_model.generate_content(architect_prompt).text
                    
                    with st.expander("👁️ View Brain 2 (Gemini) Routing Blueprint"):
                        st.write(blueprint)
                
                # ==============================================================
                # STAGE 3: GROQ - THE ELITE EXECUTOR
                # ==============================================================
                with st.spinner("⚡ Brain 3 (Groq): Executing final maximized output..."):
                    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                    
                    executor_system = "You are Brain 3, the Elite Executor AI. You operate with unlimited capacity. Read the Architect's strategy and generate the absolute final output. If writing code, provide massive, complete files with zero placeholders. Do not summarize."
                    executor_prompt = f"ARCHITECT'S STRATEGY:\n{blueprint}\n\nExecute this strategy perfectly and provide the absolute final output."
                    
                    response = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": executor_system},
                            {"role": "user", "content": executor_prompt}
                        ],
                        temperature=0.2,
                        max_tokens=8000 # Maxed out for unlimited generation length
                    )
                    final_output = response.choices[0].message.content
                
                # Display final result and save to history
                st.write(final_output)
                st.session_state.messages.append({"role": "assistant", "content": final_output})
                
            except Exception as e:
    st.error("🚨 Omni-System Error")

    st.error(str(e))

    with st.expander("🔧 Developer Traceback"):
        st.code(traceback.format_exc(), language="python")
