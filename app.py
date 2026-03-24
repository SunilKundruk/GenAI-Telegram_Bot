"""
GenAI Telegram Bot — Entry Point
"""
import sys
import os
import logging

# Path fix for local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot.handlers import create_bot_application

logging.basicConfig(level=logging.INFO)

def main():
    try:
        app, handlers = create_bot_application()
        print("🟢 Bot is starting... check your Telegram!")
        app.run_polling(drop_pending_updates=True)
    except Exception as e:
        print(f"❌ Startup Error: {e}")

if __name__ == "__main__":
    main()
