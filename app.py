import streamlit as st
import json
import pandas as pd
import traceback
import logging
import time
from datetime import datetime

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

df = pd.DataFrame.from_dict(
    warehouse_database,
    orient="index"
)

st.dataframe(df, use_container_width=True)


# =====================================================
# SELF-HEALING SYSTEM
# =====================================================

logging.basicConfig(
    filename="techstore.log",
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def log_error(error):
    logging.error(traceback.format_exc())
    st.session_state.system_health["last_error"] = str(error)

def safe_execute(func, *args, retries=2, **kwargs):
    """
    Execute a function with automatic retry.
    """
    for attempt in range(retries + 1):
        try:
            return func(*args, **kwargs)

        except Exception as e:

            log_error(e)

            if attempt == retries:
                return None

            time.sleep(1)

def update_health():

    st.session_state.system_health["last_check"] = datetime.now().strftime("%H:%M:%S")

    online = 0

    for provider in st.session_state.system_health["brains"].values():

        if provider == "Online":
            online += 1

    if online == 3:
        st.session_state.system_health["status"] = "Excellent"

    elif online >= 1:
        st.session_state.system_health["status"] = "Operational"

    else:
        st.session_state.system_health["status"] = "Offline"

# =====================================================
# ADMIN MODE
# =====================================================

st.subheader("🛠️ Developer Dashboard")

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


# =====================================================
# HIDDEN AI COORDINATOR
# =====================================================

AI_MODE = "AUTO"

SYSTEM_PROMPT = """
You are TechStore Universal Super-System.

Your responsibilities include:

- Programming
- Debugging
- Software Engineering
- AI Development
- Mathematics
- Law
- Business
- Writing
- Research
- Data Analysis
- Automation
- Problem Solving

Always produce accurate, detailed and professional responses.
Never reveal your internal architecture.
Never mention hidden providers or routing.
"""

def choose_provider(prompt: str):

    prompt = prompt.lower()

    if any(word in prompt for word in [
        "python","code","bug","debug","app","streamlit",
        "flutter","html","css","javascript","api"
    ]):
        return "groq"

    if any(word in prompt for word in [
        "research","explain","science",
        "history","medical","business"
    ]):
        return "gemini"

    return "xai"

# =====================================================
# ADVANCED SYSTEM CORE
# =====================================================

from collections import deque
import hashlib

# -------- Session Initialization --------

if "response_cache" not in st.session_state:
    st.session_state.response_cache = {}

if "conversation_memory" not in st.session_state:
    st.session_state.conversation_memory = deque(maxlen=20)

if "performance" not in st.session_state:
    st.session_state.performance = {
        "total_requests": 0,
        "successful_requests": 0,
        "failed_requests": 0,
        "average_response_time": 0.0,
        "fastest_response": None,
        "slowest_response": None
    }

# -------- Cache Utilities --------

def cache_key(prompt: str):
    return hashlib.sha256(prompt.encode()).hexdigest()

def cache_get(prompt):
    return st.session_state.response_cache.get(cache_key(prompt))

def cache_save(prompt, response):
    st.session_state.response_cache[cache_key(prompt)] = response

# -------- Conversation Memory --------

def remember(role, content):
    st.session_state.conversation_memory.append({
        "role": role,
        "content": content
    })

# -------- Performance Monitor --------

def record_response(seconds, success=True):

    perf = st.session_state.performance

    perf["total_requests"] += 1

    if success:
        perf["successful_requests"] += 1
    else:
        perf["failed_requests"] += 1

    if perf["fastest_response"] is None:
        perf["fastest_response"] = seconds

    if perf["slowest_response

# =====================================================
# TECHSTORE AI ENGINE v2
# =====================================================

def ask_ai(user_prompt):

    import time

    start = time.time()

    # -----------------------------
    # CACHE CHECK
    # -----------------------------

    cached = cache_get(user_prompt)

    if cached:

        st.session_state.system_health["status"] = "Cache Hit"

        return cached

    remember("user", user_prompt)

    provider = choose_provider(user_prompt)

    answer = None

    # =====================================================
    # xAI
    # =====================================================

    if provider == "xai" and xai_client:

        try:

            response = safe_execute(

                xai_client.chat.completions.create,

                model="grok-beta",

                messages=[

                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },

                    {
                        "role": "user",
                        "content": user_prompt
                    }

                ]

            )

            if response:

                answer = response.choices[0].message.content

        except Exception as e:

            log_error(e)

    # =====================================================
    # GEMINI
    # =====================================================

    elif provider == "gemini" and gemini_model:

        try:

            response = safe_execute(

                gemini_model.generate_content,

                user_prompt

            )

            if response:

                answer = response.text

        except Exception as e:

            log_error(e)

    # =====================================================
    # GROQ
    # =====================================================

    elif provider == "groq" and groq_client:

        try:

            response = safe_execute(

                groq_client.chat.completions.create,

                model="llama-3.3-70b-versatile",

                messages=[

                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },

                    {
                        "role": "user",
                        "content": user_prompt
                    }

                ]

            )

            if response:

                answer = response.choices[0].message.content

        except Exception as e:

            log_error(e)

    # =====================================================
    # FALLBACK
    # =====================================================

    if not answer:

        answer = "⚠️ All available AI providers are currently unavailable."

        record_response(
            time.time() - start,
            success=False
        )

        return answer

    cache_save(user_prompt, answer)

    remember("assistant", answer)

    elapsed = round(time.time() - start, 2)

    st.session_state.system_health["response_time"] = elapsed

    update_health()

    record_response(elapsed)

    return answer

# =====================================================
# PROJECT BUILDER
# =====================================================

def detect_project_request(prompt):

    keywords = [

        "build",

        "create",

        "develop",

        "make",

        "generate",

        "application",

        "website",

        "app",

        "system",

        "software"

    ]

    return any(word in prompt.lower() for word in keywords)


def create_project_plan(prompt):

    return f"""
PROJECT ANALYSIS

User Request:
{prompt}

Execution Plan

1. Analyze Requirements

2. Choose Best Architecture

3. Create Folder Structure

4. Generate Files

5. Review Generated Code

6. Produce Final Project


# =====================================================
# PROMPT OPTIMIZER
# =====================================================

def optimize_prompt(prompt):

    if len(prompt) < 15:

        prompt += """

Please provide a professional, detailed,
well-structured response with complete code
where applicable.



    return prompt.strip()

    # =====================================================
# CODE VALIDATOR
# =====================================================

def validate_code(response):

    issues = []

    if "TODO" in response:

        issues.append("Contains TODO.")

    if "FIXME" in response:

        issues.append("Contains FIXME.")

    if "pass" in response:

        issues.append("Contains unfinished code.")

    return issues

cache_save(user_prompt, answer)

remember("assistant", answer)

elapsed = round(time.time() - start, 2)

st.session_state.system_health["response_time"] = elapsed

update_health()

record_response(elapsed)

# -------------------------------------------------
# PROJECT BUILDER
# -------------------------------------------------

if detect_project_request(user_prompt):

    plan = create_project_plan(user_prompt)

    answer = plan + "\n\n" + answer

# -------------------------------------------------
# PROJECT ANALYZER (PART 6)
# -------------------------------------------------

if detect_project_request(user_prompt):

    project = analyze_project(user_prompt)

    structure = generate_structure(project)

    answer = structure + "\n\n" + answer

# -------------------------------------------------
# CODE VALIDATOR
# -------------------------------------------------

issues = validate_code(answer)

if issues:

    answer += "\n\n⚠ Validation Report:\n"

    for issue in issues:

        answer += f"- {issue}\n"

# -------------------------------------------------
# RESPONSE ENHANCER
# -------------------------------------------------

answer = improve_response(answer)

return answer
