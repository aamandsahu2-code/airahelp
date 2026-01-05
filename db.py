# ============================================================
# Aira Group Manager Bot - MongoDB Database
# ============================================================

import motor.motor_asyncio
from config import MONGO_URI, DB_NAME
import logging
import asyncio

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')

# Global db variable
db = None

async def init_db():
    """Koyeb deploy के लिए जरूरी init function"""
    global db
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
        db = client[DB_NAME]
        
        # Test connection
        await db.command("ping")
        logging.info("✅ MongoDB connected successfully!")
        print("🚀 Aira MongoDB Ready!")
    except Exception as e:
        logging.error(f"❌ Failed to connect to MongoDB: {e}")
        raise

# Initialize on startup
if __name__ == "__main__":
    asyncio.run(init_db())

# ==========================================================
# 👤 USER SYSTEM (Broadcast)
# ==========================================================
async def add_user(user_id, first_name):
    await db.users.update_one(
        {"user_id": user_id},
        {"$set": {"first_name": first_name}},
        upsert=True
    )

async def get_all_users():
    cursor = db.users.find({}, {"_id": 0, "user_id": 1})
    users = []
    async for document in cursor:
        if "user_id" in document:
            users.append(document["user_id"])
    return users

# ==========================================================
# 🟢 WELCOME SYSTEM
# ==========================================================
async def set_welcome_message(chat_id, text: str):
    await db.welcome.update_one(
        {"chat_id": chat_id},
        {"$set": {"message": text}},
        upsert=True
    )

async def get_welcome_message(chat_id):
    data = await db.welcome.find_one({"chat_id": chat_id})
    return data.get("message") if data else None

# ==========================================================
# 🔒 LOCKS SYSTEM
# ==========================================================
async def set_lock(chat_id, lock_type, status: bool):
    await db.locks.update_one(
        {"chat_id": chat_id},
        {"$set": {f"locks.{lock_type}": status}},
        upsert=True
    )

async def get_locks(chat_id):
    data = await db.locks.find_one({"chat_id": chat_id})
    return data.get("locks", {}) if data else {}

# ==========================================================
# ⚠️ WARN SYSTEM
# ==========================================================
async def add_warn(chat_id: int, user_id: int) -> int:
    data = await db.warns.find_one({"chat_id": chat_id, "user_id": user_id})
    warns = data.get("count", 0) + 1 if data else 1
    await db.warns.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"count": warns}},
        upsert=True
    )
    return warns
