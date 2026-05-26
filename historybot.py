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

html, body, [data-testid="stAppViewContainer"], .stApp, [data-testid="stMain"], 
[data-testid="stVerticalBlock"], [data-testid="stBottomBlockContainer"], 
section.main, .main, .block-container {
    background-color: #0e0b07 !important;
    background-image: 
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(180,120,40,0.15) 0%, transparent 70%),
        url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23c49a2a' fill-opacity='0.045'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") !important;
    background-size: cover;
    margin: 0 !important;
    padding: 0 !important;
}

/* Force no white backgrounds */
[data-testid="stSidebar"], [data-testid="stToolbar"], footer, #MainMenu, .stDeployButton,
section.main > div, [data-testid="stChatInputContainer"] > div, 
[data-testid="stBottomBlockContainer"] > div, .stChatInput {
    background-color: #0e0b07 !important;
}

/* Chat input area - full dark */
[data-testid="stChatInputContainer"],
[data-testid="stChatInput"],
.stChatInput {
    background-color: #1a1408 !important;
    border-color: rgba(196,154,42,0.3) !important;
}

/* Remove any remaining white blocks */
div[data-testid="stBottomBlockContainer"] {
    background: #0e0b07 !important;
    border-top: 1px solid rgba(196,154,42,0.2) !important;
}

.block-container {
    max-width: 820px !important;
    padding: 2rem 1rem 5rem !important;
    margin: 0 auto;
}

/* Header */
.main-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.header-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: #f5e9c8;
    margin: 0.5rem 0;
}
.header-title span { color: #c49a2a; }
</style>
""", unsafe_allow_html=True)

# ===================== HEADER =====================
st.markdown("""
<div class="main-header">
    <h2 style="color:#c49a2a; font-size:1.1rem; letter-spacing:4px; margin:0 0 0.5rem 0;">PH</h2>
    <h1 class="header-title"><span>Maria</span> — Philippine<br>History Assistant</h1>
    <p style="color:#8a7a5a; font-size:0.9rem; margin-top:0.3rem;">YOUR AI GUIDE THROUGH THE AGES</p>
</div>
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
