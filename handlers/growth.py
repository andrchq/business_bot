from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline import (
    growth_point_kb,
    no_clients_kb,
    clients_no_buy_kb,
    buy_little_kb,
    no_repeat_sales_kb
)
from utils.media import get_menu_media, safe_edit_menu

router = Router()

@router.callback_query(F.data == "find_growth_point")
async def cb_find_growth_point(callback: CallbackQuery):
    text = (
        "Поиск точки роста бизнеса — это не просто <i>«придумать новую фичу»</i>.\n"
        "Большинство предпринимателей усиливают то, что уже работает, и игнорируют слабые места.\n\n"
        "Рост почти всегда кроется в одном из ключевых элементов: привлечение клиентов, конверсия и оффер, продажи, прогрев и коммуникация, реклама и трафик.\n"
        "<b>Определите, где у вас сейчас главный затык</b>, чтобы не тратить бюджет и время зря."
    )
    await safe_edit_menu(
        callback=callback,
        image_name="growth_point",
        caption=text,
        reply_markup=growth_point_kb()
    )
    await callback.answer()

@router.callback_query(F.data == "growth_no_clients")
async def cb_growth_no_clients(callback: CallbackQuery):
    text = (
        "Если <b>клиентов нет</b>, деньги не приходят из-за системных ошибок, а не качества продукта.\n\n"
        "Возможные причины: неправильная аудитория, слабый оффер, отсутствие системного трафика.\n"
        "Если не исправить эти точки, даже лучший продукт останется невидимкой на рынке."
    )
    await safe_edit_menu(
        callback=callback,
        image_name="growth_no_clients",
        caption=text,
        reply_markup=no_clients_kb()
    )
    await callback.answer()

@router.callback_query(F.data == "growth_clients_no_buy")
async def cb_growth_clients_no_buy(callback: CallbackQuery):
    text = (
        "Если <b>люди приходят, но не покупают</b>, значит ваш прогрев и коммуникация недостаточны.\n\n"
        "Люди не доверяют, не видят ценности, сравнивают с конкурентами и не понимают, зачем покупать прямо сейчас.\n"
        "Часто это не вопрос скидок, а вопрос подачи, аргументации и логики пути клиента."
    )
    await safe_edit_menu(
        callback=callback,
        image_name="growth_clients_no_buy",
        caption=text,
        reply_markup=clients_no_buy_kb()
    )
    await callback.answer()

@router.callback_query(F.data == "growth_buy_little")
async def cb_growth_buy_little(callback: CallbackQuery):
    text = (
        "Если <b>покупают мало</b>, значит деньги уже есть, но они не собираются полностью.\n\n"
        "Частые причины: нет апсейлов и кросс-сейлов, нет причин купить больше или сейчас, нет структурированной цепочки продуктов.\n"
        "Настоящие деньги лежат в упаковке и дополнительных предложениях. Если их нет, вы оставляете прибыль на столе."
    )
    await safe_edit_menu(
        callback=callback,
        image_name="growth_buy_little",
        caption=text,
        reply_markup=buy_little_kb()
    )
    await callback.answer()

@router.callback_query(F.data == "growth_no_repeat_sales")
async def cb_growth_no_repeat_sales(callback: CallbackQuery):
    text = (
        "<b>Повторные продажи</b> — самый дешёвый и стабильный источник роста.\n"
        "Если их нет, это системная ошибка бизнеса.\n\n"
        "Возможные причины: клиенту не объяснили, что будет дальше; с ним перестали общаться после оплаты; нет экосистемы.\n\n"
        "Бизнес без возврата клиентов — это вечная гонка за новыми людьми. Постоянно тратить деньги и силы на объяснение ценности.\n"
        "Система повторных продаж превращает бизнес из режима выживания в управляемый рост, где клиент становится ресурсом, а не расходным материалом."
    )
    await safe_edit_menu(
        callback=callback,
        image_name="growth_no_repeat_sales",
        caption=text,
        reply_markup=no_repeat_sales_kb()
    )
    await callback.answer()

@router.callback_query(F.data == "growth_dont_understand")
async def cb_growth_dont_understand(callback: CallbackQuery):
    text = (
        "Понимаю вас. Иногда сложно определить проблему изнутри.\n"
        "Давайте перейдем к подробному анализу бизнеса."
    )
    from keyboards.inline import business_analysis_kb # local import to avoid circular dep if it happens
    await safe_edit_menu(
        callback=callback,
        image_name="business_analysis",
        caption=text,
        reply_markup=business_analysis_kb()
    )
    await callback.answer()
