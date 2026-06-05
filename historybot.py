import streamlit as st
import os
from groq import Groq
from groq import RateLimitError, APIConnectionError

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="Maria - PH History Bot",
    page_icon="🇵🇭",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ===================== DARK THEME STYLES ONLY =====================
dark_css = """
<style>
.stApp {
    background: #12378c;
    background: linear-gradient(120deg, rgba(18, 55, 140, 1) 0%, rgba(138, 117, 117, 1) 50%, rgba(255, 255, 255, 1) 100%);
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

[data-testid="stToolbar"] {
    right: 1rem;
}

.block-container {
    padding-top: 2.5rem;
    padding-bottom: 6rem;
    max-width: 860px;
}

h1, h2, h3, p, li, div {
    color: #e5e7eb;
}

.hero-card {
    background: rgba(17, 24, 39, 0.78);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
}

.hero-title {
    font-size: 2.1rem;
    font-weight: 800;
    color: #f8fafc;
    margin-bottom: 0.35rem;
    letter-spacing: -0.03em;
}

.hero-subtitle {
    color: #cbd5e1;
    font-size: 1rem;
}

.accent {
    color: #fbbf24;
    font-weight: 700;
}

section[data-testid="stChatMessage"] {
    background: rgba(15, 23, 42, 0.88);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 18px;
    padding: 0.25rem 0.5rem;
    margin-bottom: 0.75rem;
}

section[data-testid="stChatMessage"] p {
    color: #e5e7eb !important;
}

.stChatInputContainer {
    background: #0b0f14 !important;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    padding-top: 0.75rem;
}

[data-testid="stChatInput"] {
    background: rgba(31, 41, 55, 0.98) !important;
    border: 1px solid rgba(255, 255, 255, 0.10) !important;
    border-radius: 16px !important;
    color: #f8fafc !important;
}

[data-testid="stChatInput"] input {
    color: #f8fafc !important;
    caret-color: #f8fafc !important;
}

[data-testid="stChatInput"]::placeholder {
    color: #94a3b8 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: #111827;
    border: none;
    border-radius: 12px;
    font-weight: 700;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
    color: #111827;
}

hr {
    border-color: rgba(255,255,255,0.08);
}
</style>
"""

st.markdown(dark_css, unsafe_allow_html=True)

# ===================== HEADER =====================
col1, col2 = st.columns([6, 1])
with col1:
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">🇵🇭 Maria — Philippine History Assistant</div>
            <div class="hero-subtitle">Your AI guide to Philippine history, culture, and heritage. Ask about <span class="accent">pre-colonial</span>, <span class="accent">Spanish</span>, <span class="accent">American</span>, <span class="accent">Japanese</span>, and modern Philippine history.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.empty()  # Removed the theme toggle button

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

if len(st.session_state.messages) == 0:
    st.info("Try asking: **Who was José Rizal?** or **What happened during the Katipunan?**")

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
            except Exception:
                response_text = "⚠️ Something went wrong. Please try again in a moment."

            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
