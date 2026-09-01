from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Найти точку роста", callback_data="find_growth_point"))
    builder.row(InlineKeyboardButton(text="Анализ бизнеса", callback_data="business_analysis"))
    builder.row(InlineKeyboardButton(text="Продажи и воронки", callback_data="sales_and_funnels"))
    builder.row(InlineKeyboardButton(text="Реклама и трафик", callback_data="ads_and_traffic"))
    builder.row(InlineKeyboardButton(text="Инструменты и шаблоны", callback_data="tools_and_templates"))
    return builder.as_markup()

def growth_point_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Нет клиентов", callback_data="growth_no_clients"))
    builder.row(InlineKeyboardButton(text="Клиенты есть, но не покупают", callback_data="growth_clients_no_buy"))
    builder.row(InlineKeyboardButton(text="Покупают мало", callback_data="growth_buy_little"))
    builder.row(InlineKeyboardButton(text="Нет повторных продаж", callback_data="growth_no_repeat_sales"))
    builder.row(InlineKeyboardButton(text="Не понимаю, где проблема", callback_data="growth_dont_understand"))
    builder.row(InlineKeyboardButton(text="Перейти к Анализу бизнеса", callback_data="business_analysis"))
    builder.row(InlineKeyboardButton(text="← В меню", callback_data="main_menu"))
    return builder.as_markup()

def no_clients_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Проверить оффер", callback_data="mock_offer"))
    builder.row(InlineKeyboardButton(text="Разобрать трафик", callback_data="mock_traffic"))
    builder.row(InlineKeyboardButton(text="Перейти к Анализу бизнеса", callback_data="business_analysis"))
    builder.row(
        InlineKeyboardButton(text="← Назад", callback_data="find_growth_point"),
        InlineKeyboardButton(text="← В меню", callback_data="main_menu")
    )
    return builder.as_markup()

def clients_no_buy_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Усилить прогрев", callback_data="mock_warmup"))
    builder.row(InlineKeyboardButton(text="Найти блок покупки", callback_data="mock_funnel"))
    builder.row(InlineKeyboardButton(text="Проверить точку роста", callback_data="find_growth_point"))
    builder.row(
        InlineKeyboardButton(text="← Назад", callback_data="find_growth_point"),
        InlineKeyboardButton(text="← В меню", callback_data="main_menu")
    )
    return builder.as_markup()

def buy_little_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Увеличить чек", callback_data="mock_sales_upsale"))
    builder.row(InlineKeyboardButton(text="Структура предложения", callback_data="mock_product_line"))
    builder.row(InlineKeyboardButton(text="Проверить точку роста", callback_data="find_growth_point"))
    builder.row(
        InlineKeyboardButton(text="← Назад", callback_data="find_growth_point"),
        InlineKeyboardButton(text="← В меню", callback_data="main_menu")
    )
    return builder.as_markup()

def no_repeat_sales_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Построить систему возврата", callback_data="mock_crm"))
    builder.row(InlineKeyboardButton(text="Коммуникация с клиентом", callback_data="mock_warmup"))
    builder.row(InlineKeyboardButton(text="Проверить точку роста", callback_data="find_growth_point"))
    builder.row(
        InlineKeyboardButton(text="← Назад", callback_data="find_growth_point"),
        InlineKeyboardButton(text="← В меню", callback_data="main_menu")
    )
    return builder.as_markup()

def business_analysis_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Продукт", callback_data="mock_product_line"))
    builder.row(InlineKeyboardButton(text="Услуги", callback_data="mock_services"))
    builder.row(InlineKeyboardButton(text="Онлайн-проект", callback_data="mock_online"))
    builder.row(InlineKeyboardButton(text="Запуск", callback_data="mock_launch"))
    builder.row(InlineKeyboardButton(text="Перейти к точке роста", callback_data="find_growth_point"))
    builder.row(InlineKeyboardButton(text="← Назад", callback_data="main_menu"))
    return builder.as_markup()

def sales_and_funnels_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Привлечение", callback_data="mock_traffic_leads"))
    builder.row(InlineKeyboardButton(text="Прогрев", callback_data="mock_warmup"))
    builder.row(InlineKeyboardButton(text="Закрытие на покупку", callback_data="mock_funnel"))
    builder.row(InlineKeyboardButton(text="Повторные продажи", callback_data="mock_crm"))
    builder.row(InlineKeyboardButton(text="Проверить точку роста", callback_data="find_growth_point"))
    builder.row(InlineKeyboardButton(text="← Назад", callback_data="main_menu"))
    return builder.as_markup()

def ads_and_traffic_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Telegram Ads", callback_data="mock_channels"))
    builder.row(InlineKeyboardButton(text="Таргет", callback_data="mock_target"))
    builder.row(InlineKeyboardButton(text="Закуп рекламы", callback_data="mock_partners"))
    builder.row(InlineKeyboardButton(text="Тест гипотез", callback_data="mock_test_offers"))
    builder.row(InlineKeyboardButton(text="Проверить точку роста", callback_data="find_growth_point"))
    builder.row(InlineKeyboardButton(text="← Назад", callback_data="main_menu"))
    return builder.as_markup()

def tools_and_templates_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Чек-листы", callback_data="mock_checklists"))
    builder.row(InlineKeyboardButton(text="Калькуляторы", callback_data="mock_calc"))
    builder.row(InlineKeyboardButton(text="Готовые схемы", callback_data="mock_schemes"))
    builder.row(InlineKeyboardButton(text="Шаблоны текстов", callback_data="mock_templates"))
    builder.row(InlineKeyboardButton(text="← Назад", callback_data="main_menu"))
    return builder.as_markup()

def single_back_main_menu_kb() -> InlineKeyboardMarkup:
    """Для заглушек-моков, просто возврат в главное меню"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="← В меню", callback_data="main_menu"))
    return builder.as_markup()
