"""
GenAI Telegram Bot — Entry Point

Includes a fix for the [SSL: CERTIFICATE_VERIFY_FAILED] error common on some Windows environments.
"""
import sys
import os
import logging
import ssl

# --- SSL FIX for Windows ---
# This fixes the 'certificate verify failed' error when connecting to Telegram
try:
    import certifi
    os.environ['SSL_CERT_FILE'] = certifi.where()
except ImportError:
    pass
# ---------------------------

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot.handlers import create_bot_application

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

def main():
    print("=" * 50)
    print("  🤖 GenAI Telegram Bot")
    print("  (SSL Fix Applied)")
    print("=" * 50)

    try:
        app, handlers = create_bot_application()
        print("🟢 Bot is running! check your Telegram!")
        app.run_polling(drop_pending_updates=True)

    except Exception as e:
        print(f"\n❌ Startup Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
