from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile

from keyboards.inline import main_menu_kb
from utils.media import get_image_path, get_menu_media, safe_edit_menu

router = Router()

start_text = (
    "Добро пожаловать в <b>Business Tool!</b>\n"
    "Этот бот не просто даёт советы — он помогает разобрать бизнес на части, "
    "выявить слабые места и усилить прибыльные направления.\n"
    "Здесь вы сможете:\n"
    "— определить реальные точки роста\n"
    "— улучшить продажи и коммуникацию\n"
    "— правильно выстроить рекламу и трафик\n"
    "— получить готовые инструменты и шаблоны\n"
    "Выбирайте, с чего хотите начать, или исследуйте всё по пути."
)

from config import tracked_users

@router.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    if user_id not in tracked_users:
        tracked_users[user_id] = {"started": True, "clicked": False}
        
    await message.answer_photo(
        photo=FSInputFile(get_image_path("main_menu")),
        caption=start_text,
        reply_markup=main_menu_kb(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "main_menu")
async def cb_main_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in tracked_users:
        tracked_users[user_id]["clicked"] = True
    else:
        tracked_users[user_id] = {"started": False, "clicked": True}
        
    await safe_edit_menu(
        callback=callback,
        image_name="main_menu",
        caption=start_text,
        reply_markup=main_menu_kb()
    )
    await callback.answer()
