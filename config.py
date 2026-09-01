import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in the environment variables.")

# Dictionary to store user stats temporary in memory
# Format: {user_id: {"started": True, "clicked": False}}
tracked_users = {}
