import streamlit as st
import os
from groq import Groq
from groq import RateLimitError, APIConnectionError

# ===================== CONFIG =====================
st.set_page_config(
    page_title="Maria - PH History Bot",
    page_icon="🇵🇭",
    layout="centered"
)

# ===================== CUSTOM CSS =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Source+Sans+3:wght@300;400;500;600&display=swap');

/* ── Root & Background ── */
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"],
[data-testid="stBottomBlockContainer"], .main, section[data-testid="stSidebar"] {
    background-color: #0e0b07 !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(180,120,40,0.15) 0%, transparent 70%),
        url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23c49a2a' fill-opacity='0.045'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") !important;
}

/* ── Also kill any white block that appears behind the chat input ── */
[data-testid="stBottomBlockContainer"] {
    background-color: #0e0b07 !important;
    border-top: 1px solid rgba(196,154,42,0.15) !important;
    padding-top: 0.75rem !important;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Main container ── */
.block-container {
    max-width: 760px !important;
    padding: 2rem 1.5rem 5rem !important;
}

/* ── Header ── */
.main-header {
    text-align: center;
    padding: 3rem 0 2rem;
}
.main-header::after {
    content: '';
    display: block;
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #c49a2a, transparent);
    margin: 1.5rem auto 0;
}
.header-flag {
    font-size: 3rem;
    display: block;
    margin-bottom: 0.75rem;
    filter: drop-shadow(0 4px 16px rgba(196,154,42,0.4));
}
.header-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: #f5e9c8;
    letter-spacing: -0.5px;
    line-height: 1.15;
    margin: 0;
}
.header-title span { color: #c49a2a; }
.header-subtitle {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 0.85rem;
    color: #8a7a5a;
    margin-top: 0.5rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 300;
}
.era-strip {
    display: flex;
    gap: 0.45rem;
    justify-content: center;
    flex-wrap: wrap;
    margin: 0 0 1.75rem;
}
.era-badge {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: #9a8450;
    border: 1px solid rgba(196,154,42,0.25);
    border-radius: 20px;
    padding: 0.22rem 0.7rem;
    background: rgba(196,154,42,0.07);
}
.gold-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(196,154,42,0.3), transparent);
    margin: 1.5rem 0 1.75rem;
}

/* ── Chat message containers ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0.4rem 0 !important;
    gap: 0.75rem !important;
}

/* All paragraph text inside chat */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] div {
    color: #e8d9b4 !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-size: 0.97rem !important;
    line-height: 1.7 !important;
}

/* User bubble wrapper */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stMarkdownContainer"] {
    background: rgba(196,154,42,0.1) !important;
    border: 1px solid rgba(196,154,42,0.28) !important;
    border-radius: 16px 16px 4px 16px !important;
    padding: 0.8rem 1.1rem !important;
}

/* Assistant bubble wrapper */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stMarkdownContainer"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-left: 3px solid #c49a2a !important;
    border-radius: 4px 16px 16px 16px !important;
    padding: 0.8rem 1.1rem !important;
}

/* Avatars */
[data-testid="chatAvatarIcon-user"] {
    background: linear-gradient(135deg, #c49a2a, #8a6a18) !important;
    border-radius: 50% !important;
}
[data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(135deg, #8B1A1A, #c0392b) !important;
    border-radius: 50% !important;
}

/* ── Chat input — FULL DARK THEME ── */
[data-testid="stChatInputContainer"],
[data-testid="stChatInput"],
.stChatInput,
[data-testid="stChatInput"] > div,
[data-testid="stChatInputContainer"] > div {
    background-color: #1a1408 !important;
    border-color: rgba(196,154,42,0.3) !important;
    border-radius: 12px !important;
}
[data-testid="stChatInput"]:focus-within,
[data-testid="stChatInputContainer"]:focus-within {
    border-color: rgba(196,154,42,0.65) !important;
    box-shadow: 0 0 0 3px rgba(196,154,42,0.1) !important;
}
[data-testid="stChatInput"] textarea,
[data-testid="stChatInputContainer"] textarea {
    background-color: #1a1408 !important;
    color: #e8d9b4 !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-size: 0.95rem !important;
    caret-color: #c49a2a !important;
}
[data-testid="stChatInput"] textarea::placeholder,
[data-testid="stChatInputContainer"] textarea::placeholder {
    color: #5a4e30 !important;
    font-style: italic;
}
/* Submit button */
[data-testid="stChatInputSubmitButton"] button {
    background: rgba(196,154,42,0.15) !important;
    border-color: rgba(196,154,42,0.4) !important;
}
[data-testid="stChatInputSubmitButton"] button:hover {
    background: rgba(196,154,42,0.3) !important;
}
[data-testid="stChatInputSubmitButton"] svg {
    fill: #c49a2a !important;
    stroke: #c49a2a !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: #c49a2a !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(196,154,42,0.25); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(196,154,42,0.45); }
</style>
""", unsafe_allow_html=True)

# ===================== HEADER =====================
st.markdown("""
<div class="main-header">
    <span class="header-flag">🇵🇭</span>
    <h1 class="header-title"><span>Maria</span> — Philippine<br>History Assistant</h1>
    <p class="header-subtitle">Your AI guide through the ages</p>
</div>
<div class="era-strip">
    <span class="era-badge">Pre-colonial</span>
    <span class="era-badge">Spanish Era</span>
    <span class="era-badge">American Period</span>
    <span class="era-badge">Japanese Occupation</span>
    <span class="era-badge">Independence</span>
    <span class="era-badge">Modern PH</span>
</div>
<hr class="gold-divider">
""", unsafe_allow_html=True)

# ===================== API KEY =====================
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("Please add your Groq API Key in Streamlit secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# ===================== SYSTEM PROMPT =====================
system_prompt = """
You are Maria, a knowledgeable and passionate AI assistant specializing in Philippine history.
You cover all eras — Pre-colonial, Spanish colonial period, American period, Japanese occupation, Independence, and Modern Philippines.
Tone: Warm, engaging, educational, and easy to understand.
Core Rules:
- Keep responses short and concise. Maximum 3-4 sentences or bullet points.
- Only answer questions related to Philippine history, culture, and heritage.
- If asked about unrelated topics, politely redirect the user back to Philippine history.
- Use simple language that students and curious learners can understand.
- When mentioning key figures, briefly explain who they are.
- Never guess or fabricate historical facts.
Response Structure:
1. Answer the question clearly and concisely.
2. Add 1-2 interesting related facts if relevant.
3. End by inviting the user to ask more.
"""

# ===================== CHAT HISTORY =====================
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ===================== CHAT INPUT =====================
if prompt := st.chat_input("Ask me anything about Philippine history..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Maria is thinking..."):
            try:
                history = [{"role": "system", "content": system_prompt}]
                for m in st.session_state.messages:
                    history.append({"role": m["role"], "content": m["content"]})
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=history,
                    max_tokens=300
                )
                response_text = response.choices[0].message.content
            except RateLimitError:
                response_text = "⚠️ Too many requests. Please wait a moment and try again."
            except APIConnectionError:
                response_text = "⚠️ Connection error. Please check your internet and try again."
            except Exception as e:
                response_text = "⚠️ Something went wrong. Please try again in a moment."

            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
