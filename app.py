import streamlit as st
from groq import Groq
import google.generativeai as genai
from openai import OpenAI
import json

# 1. System Infrastructure Setup
st.set_page_config(page_title="TechStore Omni-Pipeline", page_icon="🌪️", layout="wide")

st.markdown("""
<style>
[data-testid="stChatInputSubmitButton"] {
    background-color: #1EBE55 !important;
    color: white !important;
    border-radius: 50% !important;
}
</style>
""", unsafe_allow_html=True)

# 2. Memory and Telemetry
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Live Store Inventory
warehouse_database = {
    "MacBook Pro M3": {"Price": 1999, "Stock Level": 14, "Status": "In Stock"},
    "Samsung Galaxy S24": {"Price": 999, "Stock Level": 0, "Status": "Backordered"},
    "Sony WH-1000XM5": {"Price": 349, "Stock Level": 42, "Status": "In Stock"}
}
inventory_json = json.dumps(warehouse_database)

# 4. ONE UNIFIED INTERFACE (NO NODES, NO SWITCHING)
st.title("🌪️ The 3-Brain Omni-Pipeline")
st.caption("Powered simultaneously by xAI (Grok) ➡️ Gemini (Google) ➡️ Groq (Llama 3.3). Unlimited mode activated.")

# Render Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input
prompt = st.chat_input("Enter any command (Code, Engineering, or Customer Support)...")

if prompt:
    # Save user prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        try:
            # 

            # STAGE 1: ELON MUSK'S xAI (GROK) - THE CONTEXT ANALYZER
            # 

            with st.spinner("🧠 Brain 1 (xAI/Grok): Analyzing request and gathering unlimited context..."):
                try:
                    xai_client = OpenAI(
                        api_key=st.secrets["XAI_API_KEY"],
                        base_url="https://api.x.ai/v1",
                    )
                    grok_response = xai_client.chat.completions.create(
                        model="grok-beta",
                        messages=[
                            {"role": "system", "content": "You are Brain 1 of an Omni-Pipeline. Analyze the user's prompt. Provide deep context and technical advice. Do not limit your response."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=8000 # Unlimited generation mode
                    )
                    grok_context = grok_response.choices[0].message.content
                except Exception as e:
                    grok_context = f"xAI Bypass Warning: Proceeding to Brain 2. Error: {e}"

                with st.expander("hide Brain 1 (xAI) Output"):
                    st.write(grok_context)

            # 

            # STAGE 2: GOOGLE GEMINI - THE MASTER ROUTER & ARCHITECT
            # 

            with st.spinner("🏗️ Brain 2 (Gemini): Architecting the master strategy..."):
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                gemini_model = genai.GenerativeModel('gemini-1.5-pro')
                
                architect_prompt = f"""You are Brain 2, the Master Architect. 
                LIVE INVENTORY: {inventory_json}
                USER REQUEST: "{prompt}"
                xAI'S ANALYSIS: "{grok_context}"
                
                INSTRUCTIONS:
                1. Read the user request. Automatically decide if it is a Customer Support query OR an Engineering/Code query.
                2. If it's a Customer Support query, draft the exact logic for how the final brain should talk to the customer.
                3. If it's a Code query, draft a massive, flawless, unlimited technical blueprint for the final brain to code.
                Do not write the final code yourself. Only write the strategy."""
                
                blueprint = gemini_model.generate_content(
                    architect_prompt, 
                    generation_config={"max_output_tokens": 8192} # Unlimited generation mode
                ).text
                
                with st.expander("👁️ View Brain 2 (Gemini) Routing Blueprint"):
                    st.write(blueprint)
            
            # 

            # STAGE 3: GROQ - THE UNLIMITED EXECUTOR
            # 

            with st.spinner("⚡ Brain 3 (Groq): Writing final output..."):
                groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                
                executor_system = "You are Brain 3, the final Executor. You have unlimited output capacity. Read the Architect's strategy and write the absolute final, flawless response. If it is a coding task, write massive, complete code blocks with no omissions. If it is a customer bot task, act exactly as the customer bot."
                executor_prompt = f"ARCHITECT'S STRATEGY:\n{blueprint}\n\nExecute this flawlessly."
                
                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": executor_system},
                        {"role": "user", "content": executor_prompt}
                    ],
                    temperature=0.2,
                    max_tokens=8000 # Unlimited generation mode
                )
                final_output = response.choices[0].message.content
            
            # Display final result and save to history
            st.write(final_output)
            st.session_state.messages.append({"role": "assistant", "content": final_output})
            
        except Exception as e:
            st.error(f"Pipeline Interruption: {e}")
            
    st.rerun()
