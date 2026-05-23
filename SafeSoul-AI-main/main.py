import os
import uuid
import base64
from datetime import datetime
from pathlib import Path
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


def get_logo_data_uri():
    logo_path = Path(__file__).with_name("icon.png")
    if not logo_path.exists():
        return ""
    return "data:image/png;base64," + base64.b64encode(logo_path.read_bytes()).decode("ascii")

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
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
        h1, h2, h3, h4, h5 { font-family: 'Space Grotesk', 'Inter', sans-serif; }

        /* App background */
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
        #MainMenu, footer, header { visibility: hidden; }
        .stDeployButton { display: none; }
        [data-testid="stAppViewBlockContainer"] {
            padding-top: 1.15rem !important;
            padding-bottom: 2rem !important;
            max-width: 1120px;
        }
        [data-testid="stAppViewContainer"] {
            backdrop-filter: blur(2px);
        }

        /* Main shell */
        .block-container {
            padding-left: 1.15rem;
            padding-right: 1.15rem;
        }

        /* Header */
        .jeeva-header {
            position: relative;
            overflow: hidden;
            isolation: isolate;
            background: linear-gradient(135deg, rgba(12, 18, 30, 0.96), rgba(9, 14, 24, 0.76));
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 28px;
            padding: 24px 26px;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 18px;
            box-shadow: var(--shadow);
            animation: panelIn 0.55s ease-out both;
        }
        .jeeva-header::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(120deg, rgba(124, 140, 255, 0.16), transparent 35%, rgba(53, 212, 255, 0.08));
            pointer-events: none;
        }
        .jeeva-header::after {
            content: '';
            position: absolute;
            right: -60px;
            top: -90px;
            width: 220px;
            height: 220px;
            background: radial-gradient(circle, rgba(124, 140, 255, 0.22), transparent 70%);
            filter: blur(8px);
            pointer-events: none;
        }
        .hero-mark {
            width: 74px;
            height: 74px;
            border-radius: 22px;
            display: grid;
            place-items: center;
            flex-shrink: 0;
            font-size: 2.1rem;
            background: linear-gradient(135deg, rgba(124, 140, 255, 0.34), rgba(53, 212, 255, 0.16));
            border: 1px solid rgba(255, 255, 255, 0.12);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08), 0 16px 30px rgba(0, 0, 0, 0.28);
            animation: float 5.5s ease-in-out infinite;
        }
        .jeeva-header-text h1 {
            color: white !important;
            font-size: 2rem !important;
            font-weight: 700 !important;
            margin: 0 !important;
            line-height: 1.2 !important;
            letter-spacing: -0.03em;
        }
        .jeeva-header-text p {
            color: rgba(231, 237, 248, 0.72) !important;
            font-size: 0.94rem !important;
            line-height: 1.6 !important;
            margin: 6px 0 0 !important;
            max-width: 60ch;
        }
        .hero-badges {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 14px;
        }
        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 7px 11px;
            border-radius: 999px;
            border: 1px solid rgba(255, 255, 255, 0.10);
            background: rgba(255, 255, 255, 0.05);
            color: rgba(231, 237, 248, 0.84);
            font-size: 0.76rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }
        .hero-badge span {
            color: var(--accent-3);
        }
        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 999px;
            padding: 7px 12px;
            margin-top: 14px;
            font-size: 0.76rem;
            color: var(--text);
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.16);
        }
        .status-dot {
            width: 8px; height: 8px;
            background: var(--accent-3);
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 0 0 rgba(110, 231, 183, 0.45);
            animation: pulseDot 1.8s ease-in-out infinite;
        }
        @keyframes pulseDot {
            0% { box-shadow: 0 0 0 0 rgba(110, 231, 183, 0.45); }
            70% { box-shadow: 0 0 0 10px rgba(110, 231, 183, 0); }
            100% { box-shadow: 0 0 0 0 rgba(110, 231, 183, 0); }
        }

        /* Intro card */
        .intro-card {
            position: relative;
            overflow: hidden;
            background: linear-gradient(135deg, rgba(12, 18, 31, 0.86), rgba(11, 16, 26, 0.72));
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            padding: 18px 20px;
            margin-bottom: 14px;
            box-shadow: 0 18px 48px rgba(0, 0, 0, 0.22);
        }
        .intro-card::before {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: inherit;
            background: linear-gradient(120deg, rgba(124, 140, 255, 0.10), transparent 40%, rgba(53, 212, 255, 0.06));
            pointer-events: none;
        }
        .intro-card p {
            color: var(--text) !important;
            font-size: 0.93rem !important;
            margin: 0 !important;
            line-height: 1.7 !important;
            position: relative;
            z-index: 1;
        }
        .intro-card strong { color: #cfd6ff !important; }
        .intro-chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 14px;
            position: relative;
            z-index: 1;
        }
        .intro-chip {
            padding: 7px 11px;
            border-radius: 999px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(255, 255, 255, 0.05);
            color: rgba(231, 237, 248, 0.8) !important;
            font-size: 0.76rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }

        /* Chat messages */
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

        /* User bubble */
        [data-testid="stChatMessage"][aria-label="user"] {
            background: linear-gradient(135deg, rgba(124, 140, 255, 0.26), rgba(53, 212, 255, 0.10)) !important;
            border-color: rgba(124, 140, 255, 0.34) !important;
        }
        [data-testid="stChatMessage"][aria-label="user"] p,
        [data-testid="stChatMessage"][aria-label="user"] span {
            color: #eef2ff !important;
            font-weight: 500 !important;
            font-size: 0.94rem !important;
        }

        /* Assistant bubble */
        [data-testid="stChatMessage"][aria-label="assistant"] {
            background: rgba(8, 13, 24, 0.84) !important;
            border-color: rgba(255, 255, 255, 0.08) !important;
        }
        [data-testid="stChatMessage"][aria-label="assistant"] * {
            color: var(--text) !important;
            font-size: 0.96rem !important;
            line-height: 1.7 !important;
        }

        [data-testid="stChatMessage"][aria-label="assistant"] strong {
            color: #cfd6ff !important;
            font-weight: 700 !important;
        }

        /* Chat input */
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

        /* Quick starters */
        .qs-label {
            text-align: center;
            color: var(--muted);
            font-size: 0.74rem;
            font-weight: 600;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin: 14px 0 8px;
        }
        div[data-testid="stHorizontalBlock"] .stButton > button {
            width: 100% !important;
            padding: 10px 8px !important;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.03)) !important;
            color: var(--text) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 16px !important;
            font-size: 0.82rem !important;
            font-weight: 600 !important;
            white-space: normal !important;
            height: auto !important;
            min-height: 52px !important;
            line-height: 1.3 !important;
            transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease, background 0.18s ease !important;
        }
        div[data-testid="stHorizontalBlock"] .stButton > button:hover {
            background: linear-gradient(135deg, rgba(124, 140, 255, 0.28), rgba(53, 212, 255, 0.14)) !important;
            color: white !important;
            border-color: rgba(110, 231, 183, 0.42) !important;
            box-shadow: 0 16px 28px rgba(0, 0, 0, 0.22) !important;
            transform: translateY(-2px) !important;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(5, 8, 15, 0.98), rgba(9, 14, 25, 0.96)) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.06);
            box-shadow: 24px 0 60px rgba(0, 0, 0, 0.22);
        }
        [data-testid="stSidebar"] > div:first-child {
            background: transparent !important;
            padding: 1.1rem 1rem 1.4rem !important;
        }
        .sb-logo {
            text-align: center;
            padding: 20px 0 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            margin-bottom: 16px;
        }
        .sb-logo .sb-icon {
            font-size: 2.4rem;
            filter: drop-shadow(0 8px 20px rgba(0, 0, 0, 0.22));
        }
        .sb-logo h2 {
            color: white !important;
            font-size: 1.22rem !important;
            font-weight: 700 !important;
            margin: 6px 0 2px !important;
            letter-spacing: -0.02em;
        }
        .sb-logo p {
            color: rgba(231, 237, 248, 0.54) !important;
            font-size: 0.74rem !important;
            margin: 0 !important;
            letter-spacing: 0.3px;
        }

        /* Stats */
        .sb-stats {
            display: flex;
            gap: 8px;
            margin-bottom: 16px;
        }
        .sb-stat {
            flex: 1;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 10px 6px;
            text-align: center;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
        }
        .sb-stat .sv { color: white; font-size: 1.18rem; font-weight: 700; display: block; }
        .sb-stat .sl { color: rgba(231, 237, 248, 0.54); font-size: 0.68rem; }

        /* Mood */
        .sb-section-label {
            color: rgba(231, 237, 248, 0.46);
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin: 14px 0 8px;
        }
        .mood-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 6px;
            margin-bottom: 16px;
        }
        .mood-chip {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 6px 4px;
            text-align: center;
            font-size: 0.75rem;
            color: rgba(231, 237, 248, 0.8);
            cursor: default;
            transition: transform 0.15s ease, background 0.15s ease, border-color 0.15s ease;
        }
        .mood-chip:hover {
            background: rgba(124, 140, 255, 0.12);
            border-color: rgba(124, 140, 255, 0.25);
            transform: translateY(-1px);
        }

        /* Sidebar cards */
        .sb-card {
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.03));
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 18px;
            padding: 14px;
            margin-bottom: 12px;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
        }
        .sb-card h4 {
            color: white !important;
            font-size: 0.82rem !important;
            font-weight: 600 !important;
            margin: 0 0 8px !important;
        }
        .sb-card ul { padding-left: 14px; margin: 0; }
        .sb-card li {
            color: rgba(231, 237, 248, 0.76) !important;
            font-size: 0.78rem !important;
            line-height: 1.7 !important;
        }
        .sb-card a { color: #8bd8ff !important; }

        /* Sidebar button */
        [data-testid="stSidebar"] .stButton > button {
            background: linear-gradient(135deg, rgba(124, 140, 255, 0.22), rgba(53, 212, 255, 0.10)) !important;
            color: white !important;
            border: 1px solid rgba(124, 140, 255, 0.28) !important;
            border-radius: 16px !important;
            font-size: 0.86rem !important;
            font-weight: 600 !important;
            width: 100% !important;
            padding: 10px !important;
            transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease !important;
            box-shadow: 0 16px 30px rgba(0, 0, 0, 0.22) !important;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            background: linear-gradient(135deg, rgba(124, 140, 255, 0.32), rgba(53, 212, 255, 0.16)) !important;
            border-color: rgba(110, 231, 183, 0.42) !important;
            transform: translateY(-1px) !important;
        }

        /* Disclaimer */
        .disclaimer {
            background: rgba(243, 194, 107, 0.08);
            border: 1px solid rgba(243, 194, 107, 0.22);
            border-radius: 18px;
            padding: 14px 18px;
            margin-top: 20px;
            backdrop-filter: blur(12px);
        }
        .disclaimer p {
            color: #f7ddb2 !important;
            font-size: 0.8rem !important;
            margin: 0 !important;
            line-height: 1.6 !important;
        }
        .disclaimer strong { color: #ffe4b5 !important; }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-6px); }
        }
        @keyframes panelIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @media (max-width: 768px) {
            [data-testid="stAppViewBlockContainer"] {
                padding-left: 0.75rem !important;
                padding-right: 0.75rem !important;
            }
            .jeeva-header {
                flex-direction: column;
                align-items: flex-start;
                padding: 20px;
                border-radius: 24px;
            }
            .hero-mark {
                width: 62px;
                height: 62px;
                border-radius: 18px;
                font-size: 1.8rem;
            }
            .jeeva-header-text h1 { font-size: 1.7rem !important; }
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


# ─────────────────────────────────────────────
# Chatbot
# ─────────────────────────────────────────────
class MentalHealthChatbot:
    def __init__(self):
        if 'user_id' not in st.session_state:
            st.session_state.user_id = str(uuid.uuid4())
            st.session_state.start_time = datetime.now()
        self.chatbot = self._init()

    def _init(self):
        API_KEY = os.getenv("GEMINI_API_KEY")
        if not API_KEY:
            st.error("GEMINI_API_KEY not found in .env", icon="🚨"); st.stop()

        sys_prompt = (
            "You are SafeSoul AI, a warm and empathetic mental health support companion. "
            "Listen actively, validate feelings without judgment, and offer gentle support. "
            "Respond to ALL messages including greetings with warmth. "
            "Ask thoughtful follow-up questions. Suggest coping strategies when helpful. "
            "Never diagnose or prescribe. Remind users to seek professional help for serious issues. "
            "Keep responses concise, warm, and conversational. Use short paragraphs."
        )

        class Session:
            def __init__(self, model, prompt):
                self.model = model
                self.prompt = prompt; self.history = []

        try:
            genai.configure(api_key=API_KEY)
            available_models = [
                model.name for model in genai.list_models()
                if "generateContent" in getattr(model, "supported_generation_methods", [])
            ]
            preferred_models = [
                "models/gemini-2.5-flash",
                "models/gemini-2.0-flash",
                "models/gemini-flash-latest",
                "models/gemini-2.0-flash-lite",
                "models/gemini-flash-lite-latest",
            ]
            chosen = next((name for name in preferred_models if name in available_models), None)
            if not chosen and available_models:
                chosen = available_models[0]
            if not chosen:
                raise RuntimeError("No Gemini models with generateContent support are available for this API key.")
            model = genai.GenerativeModel(model_name=chosen)
            st.session_state['_model'] = chosen
            return Session(model, sys_prompt)
        except Exception as e:
            st.error(f"Gemini init failed: {e}", icon="🔥"); st.stop()

    def reply(self, message):
        if not self.chatbot: return "Chatbot unavailable."
        try:
            crisis_kw = ["suicide","kill myself","end my life","want to die",
                         "harm myself","hurt myself","don't want to live","overdose"]
            crisis = any(k in message.lower() for k in crisis_kw)

            s = self.chatbot
            prompt = f"{s.prompt}\n\nUser: {message}\nAssistant:"
            resp = s.model.generate_content(prompt)
            text = resp.text if getattr(resp, "text", None) else "I'm here. Could you tell me more?"
            s.history += [{"role":"user","content":message}, {"role":"model","content":text}]

            if crisis:
                text = ("🚨 **You're not alone — please reach out right now:**\n"
                        "- 🇮🇳 iCall (India): **9152987821**\n"
                        "- 🇺🇸 US/Canada: **988**\n"
                        "- 🌍 International: [findahelpline.com](https://findahelpline.com)\n\n") + text
            return text
        except Exception as e:
            import traceback; print(traceback.format_exc())
            err = str(e)
            if "429" in err or "quota" in err.lower():
                return "I'm at my usage limit right now. Please try again in a moment. 💙"
            return f"Error: {err}"


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def _welcome():
    return {"role":"assistant","content":(
        "Hello. I’m really glad you’re here. 💙\n\n"
        "This is a calm, private space to slow down, reflect, and talk things through. "
        "Share whatever is on your mind — I’m here to listen.\n\n**How are you feeling today?**"
    )}

def _send(text):
    st.session_state.messages.append({"role":"user","content":text})
    with st.spinner("SafeSoul AI is reflecting..."):
        reply = st.session_state.bot.reply(text)
    st.session_state.messages.append({"role":"assistant","content":reply})
    st.rerun()


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="SafeSoul AI – Mental Wellness",
        page_icon="🧠", layout="centered",
        initial_sidebar_state="expanded"
    )
    inject_custom_css()
    logo_data_uri = get_logo_data_uri()

    # Init
    if 'bot' not in st.session_state:
        with st.spinner("Preparing your space..."):
            st.session_state.bot = MentalHealthChatbot()
    if 'messages' not in st.session_state:
        st.session_state.messages = [_welcome()]

    # ── Sidebar ──────────────────────────────
    with st.sidebar:
        st.markdown(f"""
        <div class="sb-logo">
            <div class="sb-icon"><img src="{logo_data_uri}" alt="SafeSoul AI logo" style="width:100%;height:100%;object-fit:contain;display:block;"/></div>
            <h2>SafeSoul AI</h2>
            <p>Mental Wellness Companion</p>
        </div>
        """, unsafe_allow_html=True)

        dur = int((datetime.now() - st.session_state.get('start_time', datetime.now())).total_seconds() / 60)
        u_msgs = sum(1 for m in st.session_state.messages if m['role'] == 'user')
        st.markdown(f"""
        <div class="sb-stats">
            <div class="sb-stat"><span class="sv">{u_msgs}</span><span class="sl">Messages</span></div>
            <div class="sb-stat"><span class="sv">{dur}m</span><span class="sl">Session</span></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sb-section-label">How are you feeling?</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="mood-grid">
            <div class="mood-chip">😊 Happy</div>
            <div class="mood-chip">😔 Sad</div>
            <div class="mood-chip">😰 Anxious</div>
            <div class="mood-chip">😤 Angry</div>
            <div class="mood-chip">😐 Neutral</div>
            <div class="mood-chip">😴 Tired</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sb-section-label">Crisis Support</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sb-card">
            <h4>🆘 Helplines</h4>
            <ul>
                <li><b>India:</b> xxxxx-xxxxx</li>
                </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sb-section-label">Wellness Tips</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sb-card">
            <h4>💡 Daily Reminders</h4>
            <ul>
                <li>Take slow, deep breaths 🌬️</li>
                <li>Drink water regularly 💧</li>
                <li>Step outside for 5 min 🌿</li>
                <li>Connect with a trusted person 🤝</li>
                <li>It's okay to ask for help 💙</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✨ Start New Conversation", key="new_chat", use_container_width=True):
            st.session_state.messages = [_welcome()]
            st.session_state.bot.chatbot.history = []
            st.toast("Fresh start! I'm here for you. 💙", icon="✨")
            st.rerun()

    # ── Main content ─────────────────────────
    # Header
    st.markdown(f"""
    <div class="jeeva-header">
        <div class="hero-mark">
            <img src="{logo_data_uri}" alt="SafeSoul AI logo" style="width:100%;height:100%;object-fit:contain;display:block;"/>
        </div>
        <div class="jeeva-header-text">
            <h1>SafeSoul AI</h1>
            <p>Your dark, calm, and compassionate mental wellness companion.</p>
            <span class="status-pill"><span class="status-dot"></span> Online &amp; Ready to Listen</span>
            <div class="hero-badges">
                <span class="hero-badge"><span>●</span> Private support</span>
                <span class="hero-badge"><span>●</span> Gentle guidance</span>
                <span class="hero-badge"><span>●</span> No judgment</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Intro
    st.markdown("""
    <div class="intro-card">
        <p>
            👋 <strong>Welcome — you’re in a safe, quiet space.</strong>
            SafeSoul AI listens without judgment and helps you explore your thoughts at your own pace.
            Share whatever’s on your mind — big or small. <strong>You are not alone.</strong>
        </p>
        <div class="intro-chip-row">
            <span class="intro-chip">Calm UI</span>
            <span class="intro-chip">Smooth replies</span>
            <span class="intro-chip">Private session</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Chat messages
    AVATARS = {
        "user":      "https://cdn-icons-png.flaticon.com/512/1144/1144760.png",
        "assistant": "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"
    }
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar=AVATARS[msg["role"]]):
            st.markdown(msg["content"])

    # Quick starters — only shown after assistant's last reply
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
        st.markdown('<div class="qs-label">💬 Quick Starters</div>', unsafe_allow_html=True)
        starters = [
            ("😟", "I'm feeling stressed and overwhelmed"),
            ("😰", "Help me manage my anxiety"),
            ("👂", "I just need someone to listen"),
            ("🧘", "Teach me a mindfulness exercise"),
        ]
        cols = st.columns(4)
        for i, (icon, text) in enumerate(starters):
            if cols[i].button(f"{icon}\n{text}", key=f"qs_{i}"):
                _send(text)

    # Input
    if user_input := st.chat_input("Share what's on your mind..."):
        _send(user_input)

    # Disclaimer
    #st.markdown("""
    #<div class="disclaimer">
    #    <p>
    #        ⚠️ <strong>SafeSoul AI is not a substitute for professional mental health care.</strong>
    #        It cannot diagnose or treat conditions. In a crisis, please call emergency services
    #       or a mental health professional immediately.
    #    </p>
    #</div>
    #""", unsafe_allow_html=False)


if __name__ == "__main__":
    main()