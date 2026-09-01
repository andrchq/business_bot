import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_MODE, BOT_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Import and register handlers
from handlers import start
from config import tracked_users
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import BaseMiddleware

# Middleware to track all buttons clicks globally
class TrackingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, CallbackQuery):
            user_id = event.from_user.id
            if user_id in tracked_users:
                tracked_users[user_id]["clicked"] = True
            else:
                tracked_users[user_id] = {"started": False, "clicked": True}
        return await handler(event, data)

dp.update.middleware(TrackingMiddleware())

# Admin command
@dp.message(Command("ad"))
async def cmd_admin_stats(message: Message):
    if message.from_user.id != 52792571:
        return
        
    total_users = len(tracked_users)
    clicked_users = sum(1 for data in tracked_users.values() if data.get("clicked"))
    
    text = (
        "<b>📊 Статистика бота:</b>\n"
        f"Всего пользователей (нажали /start или перешли): {total_users}\n"
        f"Из них нажимали кнопки: {clicked_users}"
    )
    await message.answer(text, parse_mode="HTML")

dp.include_router(start.router)
if BOT_MODE == "business":
    from handlers import growth, main_menu, mock

    dp.include_router(start.business_router)
    dp.include_router(main_menu.router)
    dp.include_router(growth.router)
    dp.include_router(mock.router)

async def main():
    # Start polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
