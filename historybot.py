import streamlit as st
import os
from groq import Groq
from groq import RateLimitError, APIConnectionError

# ===================== CONFIG =====================
st.set_page_config(page_title="Maria - PH History Bot", page_icon="🇵🇭", layout="centered")
st.title("Philippine History Assistant")
st.markdown("**Your AI guide to Philippine history** — Ask me anything!")

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

# Display chat history
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
                # Build full conversation history
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
