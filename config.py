import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_MODE = os.getenv("BOT_MODE", "business").strip().lower()

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in the environment variables.")

if BOT_MODE not in {"business", "redirect"}:
    raise ValueError("BOT_MODE must be either 'business' or 'redirect'.")

# Dictionary to store user stats temporary in memory
# Format: {user_id: {"started": True, "clicked": False}}
tracked_users = {}
