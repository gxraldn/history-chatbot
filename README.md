# 🇵🇭 Maria — Philippine History Assistant

> **Your AI guide to Philippine history.** Ask Maria anything about the Philippines — from ancient pre-colonial kingdoms to modern history.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 About

**Maria** is an AI-powered chatbot built with [Streamlit](https://streamlit.io/) and [Groq](https://groq.com/) that specializes in Philippine history. She covers all major eras — from pre-colonial indigenous cultures to the modern Philippines — and responds in a warm, educational, and easy-to-understand tone.

---

## ✨ Features

- 💬 **Conversational chat interface** — powered by Streamlit's native chat UI
- 🧠 **Context-aware responses** — full conversation history sent with every message
- 🇵🇭 **Philippine history focus** — politely redirects off-topic questions back to history
- ⚡ **Fast inference** — uses Groq's LLaMA 3.3 70B model for near-instant responses
- 🛡️ **Graceful error handling** — catches rate limits and connection errors with friendly messages

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- A [Groq API key](https://console.groq.com/)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/maria-ph-history-bot.git
cd maria-ph-history-bot

# 2. Install dependencies
pip install streamlit groq

# 3. Set up your Groq API key (see Configuration below)

# 4. Run the app
streamlit run app.py
```

---

## 🔑 Configuration

Maria requires a **Groq API key** to function. You can provide it in one of two ways:

**Option 1 — Streamlit Secrets (recommended for deployment):**

Create a `.streamlit/secrets.toml` file in your project root:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

**Option 2 — Environment Variable:**

```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

---

## 🗂️ Project Structure

```
maria-ph-history-bot/
├── app.py                  # Main Streamlit application
├── .streamlit/
│   └── secrets.toml        # API keys (excluded from version control)
├── requirements.txt        # Python dependencies
└── README.md
```

**`requirements.txt`:**
```
streamlit
groq
```

---

## 🌐 Deploying to Streamlit Community Cloud

1. Push your code to a public GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and connect your repo.
3. Under **App settings → Secrets**, add your `GROQ_API_KEY`.
4. Deploy — Maria will be live in seconds!

---

## 🤖 How It Works

1. The user types a question in the chat input.
2. The full conversation history (plus a detailed system prompt) is sent to Groq's API.
3. Groq runs inference on **LLaMA 3.3 70B** and returns a response.
4. Maria's reply is displayed in the chat and stored in Streamlit's session state for multi-turn conversation.

Maria's system prompt instructs her to:
- Keep answers short and concise (3–4 sentences or bullet points)
- Only answer questions related to Philippine history, culture, and heritage
- Never fabricate or guess historical facts
- Invite users to continue asking questions

---

## ⚠️ Error Handling

| Error | Message Shown |
|---|---|
| Rate limit exceeded | "⚠️ Too many requests. Please wait a moment and try again." |
| API connection failure | "⚠️ Connection error. Please check your internet and try again." |
| Unexpected error | "⚠️ Something went wrong. Please try again in a moment." |

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- [Groq](https://groq.com/) for blazing-fast LLM inference
- [Meta AI](https://ai.meta.com/) for the LLaMA 3.3 model
- [Streamlit](https://streamlit.io/) for the chat UI framework
- The Filipino people and their rich, resilient history 🇵🇭
