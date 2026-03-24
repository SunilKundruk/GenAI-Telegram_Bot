"""
Telegram bot command handlers — /ask, /image, /help, /summarize.
"""
import logging
import io
from google import genai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import config
from rag.retriever import Retriever
from rag.vector_store import VectorStore
from rag.embedder import Embedder
from vision.describer import ImageDescriber
from bot.history import MessageHistory

logger = logging.getLogger(__name__)

class BotHandlers:
    def __init__(self):
        print("🚀 Initializing bot...")
        self.embedder = Embedder()
        self.vector_store = VectorStore(self.embedder)
        self.vector_store.index_documents()
        self.retriever = Retriever(self.vector_store)
        self.image_describer = ImageDescriber()
        self.history = MessageHistory(max_messages=3)
        self.last_photo = {}  # Smart Memory: stores last photo file_id per user
        print("✅ Ready!")

    async def _safe_reply(self, update: Update, text: str, parse_mode="Markdown"):
        try:
            await update.message.reply_text(text, parse_mode=parse_mode)
        except Exception as e:
            await update.message.reply_text(text, parse_mode=None)

    async def help_command(self, u: Update, c: ContextTypes.DEFAULT_TYPE):
        await u.message.reply_text("🤖 Commands:\n/ask <query>\n/image (upload photo)\n/summarize\n/help", parse_mode="Markdown")

    async def start_command(self, u: Update, c: ContextTypes.DEFAULT_TYPE):
        await u.message.reply_text("👋 Welcome! Try `/help`.", parse_mode="Markdown")

    async def ask_command(self, u: Update, c: ContextTypes.DEFAULT_TYPE):
        user_id = u.effective_user.id
        query = " ".join(c.args)
        if not query:
            await u.message.reply_text("❌ Missing question!")
            return
        await u.message.chat.send_action("typing")
        self.history.add_user_message(user_id, query)
        res = self.retriever.retrieve_answer(query, self.history.get_history(user_id))
        ans = res["answer"]
        src = "\n\n📎 Sources: " + ", ".join([f"{s['doc']}.md" for s in res.get("sources", [])])
        self.history.add_bot_message(user_id, ans)
        await self._safe_reply(u, f"📖 *Answer:*\n{ans}{src}")

    async def image_command(self, u: Update, c: ContextTypes.DEFAULT_TYPE):
        user_id = u.effective_user.id
        
        # 1. Check current message
        photo = u.message.photo[-1] if u.message.photo else None
        
        # 2. Check if it's a reply
        if not photo and u.message.reply_to_message and u.message.reply_to_message.photo:
            photo = u.message.reply_to_message.photo[-1]
            
        # 3. Check Smart Memory (last photo sent)
        if not photo and user_id in self.last_photo:
            photo_file_id = self.last_photo[user_id]
        elif photo:
            photo_file_id = photo.file_id
        else:
            await u.message.reply_text("❌ No photo found! Send a photo first or reply to one with `/image`.")
            return

        await u.message.chat.send_action("typing")
        file = await c.bot.get_file(photo_file_id)
        img_bytes = await file.download_as_bytearray()
        
        res = self.image_describer.describe(bytes(img_bytes))
        resp = f"🖼️ *Description:*\n{res['caption']}\n\n🏷️ *Tags:* {', '.join(f'`{t}`' for t in res['tags'])}"
        self.history.add_user_message(user_id, "[Requested image description]")
        await self._safe_reply(u, resp)

    async def photo_handler(self, u: Update, c: ContextTypes.DEFAULT_TYPE):
        user_id = u.effective_user.id
        # Remember this photo for later
        self.last_photo[user_id] = u.message.photo[-1].file_id
        await u.message.reply_text("📸 Got it! You can now just type `/image` to describe this photo.", parse_mode="Markdown")

    async def summarize_command(self, u: Update, c: ContextTypes.DEFAULT_TYPE):
        user_id = u.effective_user.id
        txt = self.history.get_summary_text(user_id)
        if not txt:
            await u.message.reply_text("📝 No history.")
            return
        await u.message.chat.send_action("typing")
        try:
            client = genai.Client(api_key=config.GEMINI_API_KEY)
            resp = client.models.generate_content(model=config.LLM_MODEL, contents=f"Summarize this concisely:\n\n{txt}")
            await self._safe_reply(u, f"📝 *Summary:*\n\n{resp.text}")
        except Exception as e:
            await u.message.reply_text(f"Error: {e}")

    async def unknown_command(self, u: Update, c: ContextTypes.DEFAULT_TYPE):
        await u.message.reply_text("❓ Unknown. Type `/help`.")

def create_bot_application():
    h = BotHandlers()
    app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", h.start_command))
    app.add_handler(CommandHandler("help", h.help_command))
    app.add_handler(CommandHandler("ask", h.ask_command))
    app.add_handler(CommandHandler("image", h.image_command))
    app.add_handler(CommandHandler("summarize", h.summarize_command))
    app.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, h.photo_handler))
    app.add_handler(MessageHandler(filters.COMMAND, h.unknown_command))
    return app, h
