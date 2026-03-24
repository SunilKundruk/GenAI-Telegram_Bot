# 🤖 Sunil AI Bot — GenAI Telegram Bot

A lightweight, hybrid GenAI bot for Telegram with **RAG (Retrieval-Augmented Generation)** knowledge and **Vision (Image Description)** capabilities.

## 🚀 Key Features

| Feature | Description |
|---|---|
| 📚 **RAG Pipeline** | Answers questions based on local Markdown documents (`knowledge_base/`). |
| 🖼️ **Image Vision** | Uses Gemini Vision to describe uploaded images and provide tags. |
| 💬 **Smart Memory** | Remembers the last photo sent for easier `/image` description. |
| 📝 **Conversation History** | Maintains per-user history for context and interaction summaries. |
| ⚡ **Query Caching** | Speeds up identical questions by caching RAG results. |
| 🛡️ **Robust Parsing** | Gracefully handles Telegram Markdown formatting errors. |

---

## 🛠️ Technology Stack
- **Bot Framework**: `python-telegram-bot`
- **GenAI model**: Google Gemini API (`models/gemini-flash-latest`)
- **Embeddings**: `sentence-transformers` (`all-MiniLM-L6-v2`)
- **Vector Storage**: SQLite (local `vector_store.db`)
- **Image Processing**: `Pillow`

---

## 📋 Commands

| Command | Usage |
|---|---|
| **`/start`** | Welcome message and introduction. |
| **`/help`** | Shows available commands and knowledge base topics. |
| **`/ask <query>`** | Asks a question from the knowledge base using RAG. |
| **`/image`** | Describes the last photo you sent (or a photo in current message). |
| **`/summarize`**| Summarizes your last 3 interactions with the bot. |

---

## 📂 Project Structure
- `app.py`: Main entry point.
- `config.py`: Central configuration and API key loading.
- `bot/`: Telegram bot logic and message history.
- `rag/`: RAG pipeline (chunking, embedding, retrieval).
- `vision/`: Gemini image description logic.
- `knowledge_base/`: Markdown files used for RAG.
- `utils/`: Caching and helper utilities.

---

## ⚙️ Setup Instructions

### 1. Requirements
Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file from the `.env.example`:
```
TELEGRAM_BOT_TOKEN=7123456...:your-bot-token
GEMINI_API_KEY=AIzaSy...your-gemini-key
```

### 3. Run the Bot
```bash
python app.py
```

### 4. Adding Knowledge
Simply drop any `.md` or `.txt` files into the `knowledge_base/` folder and restart the bot. It will automatically index the new content!
