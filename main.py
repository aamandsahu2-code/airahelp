# ============================================================
# Group Manager Bot - Updated Main.py
# Author: LearningBotsOfficial (https://github.com/LearningBotsOfficial) 
# ============================================================

import os
import sys
import logging
from pyrogram import Client
from pyrogram.errors import FloodWait, RPCError
from config import API_ID, API_HASH, BOT_TOKEN
from handlers import register_all_handlers
from db import db, init_db
# Top में add करो
from db import init_db, db
import asyncio

# main() में:
async def main():
    await init_db()  # Mongo connect
    register_handlers(app)
    print("Aira starting...")
    app.run()

if __name__ == "__main__":
    asyncio.run(main())

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Validate config
def validate_config():
    if not all([API_ID, API_HASH, BOT_TOKEN]):
        logger.error("❌ Missing config: API_ID, API_HASH or BOT_TOKEN")
        return False
    logger.info("✅ Config validated successfully")
    return True

async def main():
    if not validate_config():
        sys.exit(1)
    
    # Initialize database
    init_db()
    logger.info("✅ Database initialized")
    
    # Create client
    app = Client(
        "group_manager_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        in_memory=True,  # Faster for production
        workers=4
    )
    
    # Register handlers
    register_all_handlers(app)
    logger.info("✅ All handlers registered")
    
    try:
        await app.start()
        bot_me = await app.get_me()
        logger.info(f"🚀 Bot started: @{bot_me.username} (ID: {bot_me.id})")
        print(f"🤖 @{bot_me.username} is online! Press Ctrl+C to stop.")
        
        # Keep running
        await app.idle()
        
    except FloodWait as e:
        logger.warning(f"⏳ FloodWait: {e.value} seconds")
        await app.sleep(e.value)
    except RPCError as e:
        logger.error(f"❌ Telegram RPC Error: {e}")
    except KeyboardInterrupt:
        logger.info("🛑 Stopping bot...")
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}", exc_info=True)
    finally:
        await app.stop()
        logger.info("👋 Bot stopped gracefully")
        db.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
