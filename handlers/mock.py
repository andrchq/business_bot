from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline import single_back_main_menu_kb
from utils.media import get_menu_media
from utils.mock_texts import MOCK_MESSAGES

router = Router()



@router.callback_query(F.data.startswith("mock_"))
async def cb_mock_handlers(callback: CallbackQuery):
    action = callback.data
    text = MOCK_MESSAGES.get(action, "<b>Блок в разработке</b>\n\nДанный раздел скоро будет доступен.")
    
    try:
        await callback.message.delete()
    except Exception:
        pass
        
    await callback.message.answer(
        text=text,
        reply_markup=single_back_main_menu_kb(),
        parse_mode="HTML"
    )
    await callback.answer(text="Открыт инструмент", show_alert=False)
