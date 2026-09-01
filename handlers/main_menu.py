from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline import (
    business_analysis_kb,
    sales_and_funnels_kb,
    ads_and_traffic_kb,
    tools_and_templates_kb
)
from utils.media import get_menu_media, safe_edit_menu

router = Router()

@router.callback_query(F.data == "business_analysis")
async def cb_business_analysis(callback: CallbackQuery):
    text = (
        "<b>Экспресс-анализ бизнеса</b> помогает выявить слабые места, где теряются деньги.\n\n"
        "Ответьте на вопросы, чтобы получить рекомендации."
    )
    await safe_edit_menu(
        callback=callback,
        image_name="business_analysis",
        caption=text,
        reply_markup=business_analysis_kb()
    )
    await callback.answer()

@router.callback_query(F.data == "sales_and_funnels")
async def cb_sales_and_funnels(callback: CallbackQuery):
    text = (
        "<b>Продажи</b> — это система, а не удача.\n\n"
        "Улучшите конкретные элементы, чтобы получать больше прибыли с теми же клиентами."
    )
    await safe_edit_menu(
        callback=callback,
        image_name="sales_and_funnels",
        caption=text,
        reply_markup=sales_and_funnels_kb()
    )
    await callback.answer()

@router.callback_query(F.data == "ads_and_traffic")
async def cb_ads_and_traffic(callback: CallbackQuery):
    text = (
        "<b>Трафик</b> — топливо бизнеса.\n\n"
        "Без правильного потока клиентов даже лучший продукт не принесёт денег. "
        "Важно тестировать гипотезы, правильно выбирать аудиторию и каналы."
    )
    await safe_edit_menu(
        callback=callback,
        image_name="ads_and_traffic",
        caption=text,
        reply_markup=ads_and_traffic_kb()
    )
    await callback.answer()

@router.callback_query(F.data == "tools_and_templates")
async def cb_tools_and_templates(callback: CallbackQuery):
    text = (
        "<b>Полезные инструменты</b> для роста бизнеса: чек-листы, калькуляторы, схемы и шаблоны текстов, которые экономят время и деньги."
    )
    await safe_edit_menu(
        callback=callback,
        image_name="tools_and_templates",
        caption=text,
        reply_markup=tools_and_templates_kb()
    )
    await callback.answer()
