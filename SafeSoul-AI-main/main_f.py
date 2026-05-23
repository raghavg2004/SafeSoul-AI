import os
import uuid
import base64
from datetime import datetime
from pathlib import Path
import streamlit as st
# Assuming database.py exists and works if you uncomment sentiment lines
# from database import SentimentVectorDatabase
from google import genai
from google.genai import types
from dotenv import load_dotenv
import random
import html # Import the html module for escaping

# Load environment variables from .env file
load_dotenv()


def get_logo_data_uri():
    logo_path = Path(__file__).with_name("icon.png")
    if not logo_path.exists():
        return ""
    return "data:image/png;base64," + base64.b64encode(logo_path.read_bytes()).decode("ascii")

# --- Custom CSS Styling ---
def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

        :root {
            --bg-0: #04070d;
            --bg-1: #08111d;
            --panel: rgba(10, 15, 25, 0.76);
            --panel-strong: rgba(11, 18, 31, 0.92);
            --stroke: rgba(255, 255, 255, 0.08);
            --stroke-strong: rgba(124, 140, 255, 0.28);
            --text: #e7edf8;
            --muted: #8e9cbc;
            --accent: #7c8cff;
            --accent-2: #35d4ff;
            --accent-3: #6ee7b7;
            --warning: #f3c26b;
            --shadow: 0 24px 70px rgba(0, 0, 0, 0.42);
        }

        * { font-family: 'Inter', sans-serif; box-sizing: border-box; }
        h1, h2, h3, h4, h5, h6 { font-family: 'Space Grotesk', 'Inter', sans-serif; color: var(--text) !important; }
        p, li { color: rgba(231, 237, 248, 0.86) !important; }

        .stApp {
            color: var(--text);
            background:
                radial-gradient(circle at 16% 16%, rgba(124, 140, 255, 0.16), transparent 28%),
                radial-gradient(circle at 84% 0%, rgba(53, 212, 255, 0.12), transparent 26%),
                radial-gradient(circle at 50% 100%, rgba(110, 231, 183, 0.08), transparent 22%),
                linear-gradient(160deg, #03050a 0%, #07111d 42%, #050912 100%);
        }
        .stApp::before {
            content: '';
            position: fixed;
            inset: 0;
            pointer-events: none;
            background-image:
                linear-gradient(rgba(255, 255, 255, 0.025) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.025) 1px, transparent 1px);
            background-size: 42px 42px;
            mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.75), transparent 85%);
            opacity: 0.45;
        }
        .stApp::after {
            content: '';
            position: fixed;
            inset: auto -10% -18% auto;
            width: 34vw;
            height: 34vw;
            pointer-events: none;
            background: radial-gradient(circle, rgba(124, 140, 255, 0.14), transparent 70%);
            filter: blur(18px);
            opacity: 0.8;
        }

        [data-testid="stAppViewBlockContainer"] {
            padding-top: 1.15rem !important;
            padding-bottom: 2rem !important;
            max-width: 1120px;
        }
        .block-container {
            padding-left: 1.15rem;
            padding-right: 1.15rem;
        }

        .intro-section {
            position: relative;
            overflow: hidden;
            background: linear-gradient(135deg, rgba(12, 18, 31, 0.86), rgba(11, 16, 26, 0.72));
            padding: 22px 22px 18px;
            border-radius: 24px;
            margin-bottom: 22px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: var(--shadow);
        }
        .intro-section::before {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: inherit;
            background: linear-gradient(120deg, rgba(124, 140, 255, 0.10), transparent 40%, rgba(53, 212, 255, 0.06));
            pointer-events: none;
        }
        .intro-section h2 {
            color: #eef2ff !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 10px;
            margin-top: 0;
            position: relative;
            z-index: 1;
        }
        .intro-section h3 {
            color: #cfd6ff !important;
            margin-top: 15px;
            position: relative;
            z-index: 1;
        }
        .intro-section p {
            position: relative;
            z-index: 1;
            line-height: 1.75;
        }
        .intro-section .stButton>button {
            background: linear-gradient(135deg, rgba(124, 140, 255, 0.22), rgba(53, 212, 255, 0.10)) !important;
            color: white !important;
            border-radius: 16px;
            padding: 10px 18px;
            margin: 5px;
            border: 1px solid rgba(124, 140, 255, 0.28) !important;
            box-shadow: 0 16px 30px rgba(0, 0, 0, 0.22);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }
        .intro-section .stButton>button:hover {
            background: linear-gradient(135deg, rgba(124, 140, 255, 0.32), rgba(53, 212, 255, 0.16)) !important;
            transform: translateY(-1px);
        }

        .stChatMessage {
            position: relative;
            border-radius: 22px !important;
            padding: 10px 16px !important;
            margin: 10px 0 !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            box-shadow: 0 18px 40px rgba(0, 0, 0, 0.18) !important;
            backdrop-filter: blur(18px);
            animation: messageIn 0.3s ease-out;
        }
        @keyframes messageIn {
            from { opacity: 0; transform: translateY(10px) scale(0.98); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }
        [data-testid="stChatMessage"][aria-label="user"] {
            background: linear-gradient(135deg, rgba(124, 140, 255, 0.26), rgba(53, 212, 255, 0.10)) !important;
            border-color: rgba(124, 140, 255, 0.34) !important;
        }
        [data-testid="stChatMessage"][aria-label="user"] p,
        [data-testid="stChatMessage"][aria-label="user"] span {
            color: #eef2ff !important;
        }
        [data-testid="stChatMessage"][aria-label="assistant"] {
            background: rgba(8, 13, 24, 0.84) !important;
            border-color: rgba(255, 255, 255, 0.08) !important;
        }
        [data-testid="stChatMessage"][aria-label="assistant"] p,
        [data-testid="stChatMessage"][aria-label="assistant"] li,
        [data-testid="stChatMessage"][aria-label="assistant"] strong {
            color: var(--text) !important;
        }
        [data-testid="stChatMessage"][aria-label="assistant"] strong {
            color: #cfd6ff !important;
            font-weight: 700;
        }

        [data-testid="stChatInput"] {
            background: transparent !important;
            padding-top: 0.6rem;
        }
        [data-testid="stChatInput"] > div {
            border-radius: 22px !important;
            border: 1px solid rgba(124, 140, 255, 0.25) !important;
            background: rgba(8, 13, 24, 0.88) !important;
            box-shadow: 0 18px 46px rgba(0, 0, 0, 0.26) !important;
            backdrop-filter: blur(18px);
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }
        [data-testid="stChatInput"] > div:focus-within {
            border-color: rgba(110, 231, 183, 0.55) !important;
            box-shadow: 0 0 0 1px rgba(110, 231, 183, 0.12), 0 18px 46px rgba(0, 0, 0, 0.28) !important;
            transform: translateY(-1px);
        }
        [data-testid="stChatInput"] textarea {
            color: var(--text) !important;
            -webkit-text-fill-color: var(--text) !important;
            caret-color: var(--accent-3) !important;
            background: transparent !important;
            font-size: 0.96rem !important;
            font-weight: 500 !important;
        }
        [data-testid="stChatInput"] textarea::placeholder {
            color: rgba(167, 180, 206, 0.78) !important;
            opacity: 1 !important;
        }

        div[data-testid="stHorizontalBlock"] .stButton>button {
            width: 100%;
            margin: 4px 0;
            white-space: normal;
            height: auto;
            padding: 10px 12px;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.03)) !important;
            color: var(--text) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 16px;
            transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease, background 0.18s ease;
        }
        div[data-testid="stHorizontalBlock"] .stButton>button:hover {
            background: linear-gradient(135deg, rgba(124, 140, 255, 0.28), rgba(53, 212, 255, 0.14)) !important;
            border-color: rgba(110, 231, 183, 0.42) !important;
            box-shadow: 0 16px 28px rgba(0, 0, 0, 0.22) !important;
            transform: translateY(-2px) !important;
        }

        .stSidebar > div:first-child {
            background: linear-gradient(180deg, rgba(5, 8, 15, 0.98), rgba(9, 14, 25, 0.96)) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.06);
            padding: 1.1rem 1rem 1.4rem !important;
            box-shadow: 24px 0 60px rgba(0, 0, 0, 0.22);
        }

        .stSidebar .sidebar-section {
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.03)) !important;
            padding: 15px;
            border-radius: 18px;
            margin-bottom: 15px;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
        }
        .stSidebar .sidebar-section *:not(a) {
            color: inherit !important;
        }
        .stSidebar .sidebar-section h3 {
            color: white !important;
            margin-top: 0;
            padding-bottom: 5px;
            border-bottom: 1px solid rgba(255,255,255,0.12);
        }
        .stSidebar .sidebar-section a {
            color: #8bd8ff !important;
            text-decoration: underline;
        }
        .stSidebar .stButton>button {
            background: linear-gradient(135deg, rgba(124, 140, 255, 0.22), rgba(53, 212, 255, 0.10)) !important;
            color: white !important;
            border: 1px solid rgba(124, 140, 255, 0.28) !important;
            width: 100%;
            margin: 10px 0;
            border-radius: 16px;
            box-shadow: 0 16px 30px rgba(0, 0, 0, 0.22);
            transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
        }
        .stSidebar .stButton>button:hover {
            background: linear-gradient(135deg, rgba(124, 140, 255, 0.32), rgba(53, 212, 255, 0.16)) !important;
            border-color: rgba(110, 231, 183, 0.42) !important;
            transform: translateY(-1px) !important;
        }

        #disclaimer {
            margin-top: 30px;
            padding: 20px;
            background: rgba(243, 194, 107, 0.08);
            border-radius: 18px;
            border: 1px solid rgba(243, 194, 107, 0.22);
            backdrop-filter: blur(12px);
        }
        #disclaimer h3 {
            color: #ffe4b5 !important;
            margin-top: 0;
        }
        #disclaimer p, #disclaimer li, #disclaimer strong {
            color: #f7ddb2 !important;
            font-size: 0.95em;
        }
        #disclaimer strong { font-weight: bold; }

        @media (max-width: 768px) {
            [data-testid="stAppViewBlockContainer"] {
                padding-left: 0.75rem !important;
                padding-right: 0.75rem !important;
            }
            .mood-grid { grid-template-columns: repeat(2, 1fr); }
        }

        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }

    </style>
    """, unsafe_allow_html=True)

class MentalHealthChatbot:
    def __init__(self):
        """Initialize the chatbot application."""
        if 'user_id' not in st.session_state:
            st.session_state.user_id = str(uuid.uuid4())
            st.session_state.start_time = datetime.now()
        self.chatbot = self.initialize_chatbot()

    def initialize_chatbot(self):
        """Initialize and return the Gemini chatbot instance."""
        API_KEY = os.getenv("GEMINI_API_KEY")
        if not API_KEY:
            st.error("Gemini API key not found. Please set the GEMINI_API_KEY environment variable.", icon="🚨")
            st.stop()

        system_instruction = (
            "You are SafeSoul AI, a warm, empathetic AI mental health support companion. "
            "Your role is to listen, validate feelings, and offer gentle emotional support. "
            "You respond to ALL messages — including short greetings like hi or hello — with warmth and care. "
            "You ask thoughtful follow-up questions to understand how the user is feeling. "
            "You suggest evidence-based coping strategies when appropriate. "
            "You always remind users you are not a substitute for professional help when discussing serious issues. "
            "You never diagnose, prescribe, or give medical advice. "
            "Keep responses concise, warm, and conversational."
        )

        self._api_key = API_KEY

        # Store system instruction for use in process_user_message
        self._system_instruction = system_instruction
        # Try models in order of preference
        try:
            client = genai.Client(api_key=API_KEY)
            # Try models in order - gemini-2.5-flash first as confirmed working
            model_names = [
                "gemini-2.5-flash",
                "gemini-2.5-flash-preview-05-20",
                "gemini-2.0-flash",
                "gemini-1.5-flash",
            ]
            class ChatSession:
                def __init__(self, client, model, sys_prompt):
                    self.client = client
                    self.model = model
                    self.sys_prompt = sys_prompt
                    self.history = []

            # Pick the first model that exists in the account
            last_err = None
            for model_name in model_names:
                try:
                    # Lightweight check - list models and see if ours is available
                    available = [m.name for m in client.models.list()]
                    match = next((m for m in available if model_name in m), None)
                    chosen = match.replace("models/", "") if match else model_name
                    return ChatSession(client, chosen, system_instruction)
                except Exception as e:
                    last_err = e
                    continue

            # Fallback: just use gemini-2.5-flash without checking
            return ChatSession(client, "gemini-2.5-flash", system_instruction)
        except Exception as e:
            st.error(f"Could not initialize Gemini client: {e}", icon="🔥")
            st.stop()

    def process_user_message(self, message):
        """Process a user message and generate a response."""
        if not self.chatbot:
            return "Sorry, the chatbot is not available right now."
        try:
            crisis_keywords = [
                "suicide", "kill myself", "end my life", "want to die",
                "harm myself", "hurt myself", "don't want to live", "no reason to live",
                "overdose", "hopeless and want out"
            ]
            crisis_detected = any(keyword in message.lower() for keyword in crisis_keywords)

            session = self.chatbot
            # Build conversation history
            contents = []
            for h in session.history:
                contents.append(types.Content(role=h["role"], parts=[types.Part(text=h["content"])]))
            contents.append(types.Content(role="user", parts=[types.Part(text=message)]))

            response = session.client.models.generate_content(
                model=session.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=session.sys_prompt,
                    temperature=0.7,
                )
            )
            response_text = response.text if response.text else "I'm here to listen. Could you tell me a bit more about that?"
            # Update history
            session.history.append({"role": "user", "content": message})
            session.history.append({"role": "model", "content": response_text})

            if crisis_detected:
                crisis_message = (
                    "\n\n"
                    "**🚨 Important:** It sounds like you're going through immense pain right now. "
                    "Please know that you're not alone and help is available. "
                    "Reaching out is a sign of strength. Here are some resources that can provide immediate support:\n"
                    "- **Emergency:** Call **911** (US/Canada) or your local emergency number immediately.\n"
                    "- **988 Suicide & Crisis Lifeline:** Call or text **988** (US).\n"
                    "- **Crisis Text Line:** Text **HOME** to **741741** (US/Canada), **85258** (UK).\n"
                    "- **Befrienders Worldwide:** Find a helpline in your country: [https://www.befrienders.org](https://www.befrienders.org)\n"
                    "**Please reach out to one of these resources now.**"
                )
                response_text = crisis_message + "\n\n" + response_text

            return response_text

        except Exception as e:
            import traceback
            print("========= GEMINI ERROR =========")
            print(traceback.format_exc())
            print("================================")
            error_details = str(e)
            if "quota" in error_details.lower() or "429" in error_details:
                return "I am currently at my usage limit. Please try again in a moment."
            elif "api_key" in error_details.lower() or "403" in error_details:
                return "There seems to be an issue with my API key. Please check your GEMINI_API_KEY in the .env file."
            else:
                return f"Something went wrong: {error_details}"

# --- Introduction and Disclaimer Content ---
def display_introduction():
    # --- FIX: Added unsafe_allow_html=True ---
    st.markdown("""
    <div class="intro-section">
        <h2>Supportive Conversations When You Need Them</h2>
        <p>
            Our AI companion, SafeSoul AI, is here to listen, support, and offer a calm presence
            through difficult moments. While not a replacement for professional help,
            we aim to provide a compassionate space for you to express yourself and explore coping strategies.
        </p>
        <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:14px;position:relative;z-index:1;">
            <span style="padding:7px 11px;border-radius:999px;border:1px solid rgba(255,255,255,0.08);background:rgba(255,255,255,0.05);color:#e7edf8;font-size:0.76rem;font-weight:600;">Calm UI</span>
            <span style="padding:7px 11px;border-radius:999px;border:1px solid rgba(255,255,255,0.08);background:rgba(255,255,255,0.05);color:#e7edf8;font-size:0.76rem;font-weight:600;">Smooth replies</span>
            <span style="padding:7px 11px;border-radius:999px;border:1px solid rgba(255,255,255,0.08);background:rgba(255,255,255,0.05);color:#e7edf8;font-size:0.76rem;font-weight:600;">Private session</span>
        </div>
    </div>
    """, unsafe_allow_html=True) # <-- THIS IS THE FIX




def display_disclaimer():
    st.markdown('<a name="disclaimer"></a>', unsafe_allow_html=True) # Anchor for scrolling via URL
    # --- FIX: Added unsafe_allow_html=True ---
    st.markdown("""
    <div id="disclaimer">
        <h3>Important Disclaimer</h3>
        <p>
            <strong>SafeSoul AI is an AI chatbot and not a substitute for professional mental health care, diagnosis, or treatment.</strong>
            It cannot provide medical advice or crisis intervention.
        </p>
        <p>
            <strong>If you are experiencing a crisis or emergency:</strong>
        </p>
        <ul>
            <li>Please call your local emergency number (like <strong>112</strong> in the India) immediately.</li>
            <li>Contact a mental health professional.</li>
            <li>Find international helplines via <strong>Befrienders Worldwide</strong>.</li>
        </ul>
        <p>
            Your conversations here are intended for general support and exploration. Please prioritize professional help for serious concerns.
        </p>
    </div>
    """, unsafe_allow_html=True) # <-- THIS IS THE FIX


# --- Main Application ---
def main():
    st.set_page_config(
        page_title="SafeSoul AI - Mental Health Support",
        page_icon="🧠",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    inject_custom_css() # Apply styling
    logo_data_uri = get_logo_data_uri()

    # --- Header ---
    st.markdown(f"""
        <div style="
            position:relative;
            overflow:hidden;
            background: linear-gradient(135deg, rgba(12, 18, 31, 0.96), rgba(11, 16, 26, 0.76));
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 28px;
            padding: 24px 26px;
            margin-bottom: 16px;
            box-shadow: 0 24px 70px rgba(0,0,0,0.42);
            display:flex;
            align-items:center;
            gap:18px;
        ">
             <div style="width:74px;height:74px;border-radius:22px;display:grid;place-items:center;background:linear-gradient(135deg, rgba(124, 140, 255, 0.34), rgba(53, 212, 255, 0.16));border:1px solid rgba(255,255,255,0.12);box-shadow:inset 0 1px 0 rgba(255,255,255,0.08), 0 16px 30px rgba(0,0,0,0.28);overflow:hidden;flex-shrink:0;">
                 <img src="{logo_data_uri}" alt="SafeSoul AI logo" style="width:100%;height:100%;object-fit:contain;display:block;"/>
             </div>
             <div style="flex:1;">
                <h1 style="margin:0; color:#EEF2FF; font-family:'Space Grotesk','Inter',sans-serif; letter-spacing:-0.03em;">SafeSoul AI</h1>
                <p style="margin:6px 0 0; color:rgba(231,237,248,0.72); line-height:1.6; max-width:60ch;">Your dark, calm, and compassionate mental wellness companion.</p>
                <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:14px;">
                    <span style="padding:7px 11px;border-radius:999px;border:1px solid rgba(255,255,255,0.10);background:rgba(255,255,255,0.05);color:#e7edf8;font-size:0.76rem;font-weight:600;">Private support</span>
                    <span style="padding:7px 11px;border-radius:999px;border:1px solid rgba(255,255,255,0.10);background:rgba(255,255,255,0.05);color:#e7edf8;font-size:0.76rem;font-weight:600;">Gentle guidance</span>
                    <span style="padding:7px 11px;border-radius:999px;border:1px solid rgba(255,255,255,0.10);background:rgba(255,255,255,0.05);color:#e7edf8;font-size:0.76rem;font-weight:600;">No judgment</span>
                </div>
             </div>
        </div>
    """, unsafe_allow_html=True)

    # --- Introduction Section ---
    display_introduction()

    # --- Initialize Chatbot ---
    if 'chatbot_instance' not in st.session_state:
        with st.spinner("🌟 Preparing your supportive space..."):
            st.session_state.chatbot_instance = MentalHealthChatbot()
        if 'messages' not in st.session_state:
            # Initial message setup
             st.session_state.messages = [{
                "role": "assistant",
                "content": """
                <div style='padding: 10px; border-radius: 15px;'>
                    <p>Hello there! I'm SafeSoul AI, ready to listen whenever you'd like to share.
                    How are you feeling today? Remember to check the information above if this is your first time here.</p>
                    <div style='text-align: center; margin-top: 10px;'>🌱</div>
                </div>
                """,
                "is_html": True # Flag this as HTML content
            }]


    # --- Display Chat Messages ---
    for message in st.session_state.messages:
        avatar_url = "https://cdn-icons-png.flaticon.com/512/1144/1144760.png" if message["role"] == "user" else "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"
        with st.chat_message(message["role"], avatar=avatar_url):
            # --- FIX: Check the 'is_html' flag before rendering ---
            if message.get("is_html", False): # Default to False if key missing
                st.markdown(message["content"], unsafe_allow_html=True)
            else:
                # Render as plain markdown (safer default for user input or non-HTML bot responses)
                st.markdown(message["content"])

    # --- Quick Responses ---
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
        st.markdown("<div style='text-align: center; margin: 15px 0; color: #8e9cbc; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase;'>Quick Chat Starters</div>", unsafe_allow_html=True)
        quick_responses = [
            "I'm feeling a bit stressed lately.",
            "Can we talk about managing anxiety?",
            "I just need someone to listen.",
            "Suggest a simple mindfulness exercise."
        ]
        cols = st.columns(len(quick_responses))
        for i, response in enumerate(quick_responses):
            if cols[i].button(response, key=f"quick_{i}"):
                st.session_state.messages.append({"role": "user", "content": response})
                with st.spinner("SafeSoul AI is thinking..."):
                    bot_response_text = st.session_state.chatbot_instance.process_user_message(response)

                    # --- FIX: Escape AI response text before adding custom HTML ---
                    safe_response_html = html.escape(bot_response_text).replace('\n', '<br/>')
                    emoji_html = f"""<div style='text-align: center; margin-top: 15px;'>
                                        {random.choice(['🌸', '🧘‍♀️', '☕', '✨', '🌱'])}
                                    </div>"""
                    formatted_response = f"""
                    <div style='padding: 10px; border-radius: 15px;'>
                        <p>{safe_response_html}</p>
                        {emoji_html}
                    </div>
                    """
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": formatted_response,
                        "is_html": True # Flag as HTML
                    })
                st.rerun()

    # --- User Input Field ---
    if user_input := st.chat_input("Share your thoughts or feelings here..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("SafeSoul AI is listening and reflecting..."):
            response_text = st.session_state.chatbot_instance.process_user_message(user_input)

             # --- FIX: Escape AI response text before adding custom HTML ---
            safe_response_html = html.escape(response_text).replace('\n', '<br/>')
            emoji_html = f"""<div style='text-align: center; margin-top: 15px;'>
                                 {random.choice(['💬', '👂', '💖', '🤝', '💡'])}
                             </div>"""
            formatted_response = f"""
            <div style='padding: 10px; border-radius: 15px;'>
                <p>{safe_response_html}</p>
                {emoji_html}
            </div>
            """
            st.session_state.messages.append({
                "role": "assistant",
                "content": formatted_response,
                "is_html": True # Flag as HTML
            })
        st.rerun()

    # --- Sidebar Content ---
    with st.sidebar:
        st.markdown("---")
        #st.markdown(
        #    """
        #    <div class="sidebar-section">
        #        <h3>🆘 Crisis Support</h3>
        #        <p><strong>If you are in immediate danger, please call your local emergency services.</strong></p>
        #        <ul>
        #            <li><b>India:</b> xxxxx-xxxxx (Vandrevala Fdn)</li>
        #         </ul>
        #    </div>
        #    """, unsafe_allow_html=True)
        st.markdown(
            """
            <div class="sidebar-section">
                <h3>💡 Wellness Tips</h3>
                <p>Remember to:</p>
                <ul>
                    <li>Stay hydrated.</li>
                    <li>Take short breaks.</li>
                    <li>Practice mindful breathing.</li>
                    <li>Connect with loved ones.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("---")
        if st.button("🔄 Start New Chat Session", key="new_chat_sidebar", use_container_width=True):
             st.session_state.messages = [{
                "role": "assistant",
                "content": """
                <div style='padding: 10px; border-radius: 15px;'>
                    <p>Starting fresh! I'm here and ready to listen. What's on your mind?</p>
                    <div style='text-align: center; margin-top: 10px;'>✨</div>
                </div>
                """,
                "is_html": True
            }]
             # Optionally reset Gemini history if needed/possible
             # st.session_state.chatbot_instance.chatbot.history.clear()
             st.toast("New chat session started!", icon="✅")
             st.rerun()

    # --- Disclaimer Section (at the bottom) ---
    display_disclaimer() # Ensure this is called to display it


if __name__ == "__main__":
    main()