from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import json


def main_reply_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🛒 Список магазинов")
    builder.button(text="➕ Добавить товар")
    builder.button(text="🎲 Монетка (решить судьбу)")
    builder.button(text="⚙️ Настройки (будет позже)")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def market_list():
    builder = InlineKeyboardBuilder()
    with open("Base.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    for markets in data:
        builder.button(text=markets, callback_data=markets)
    builder.button(text="🔙 Назад в главное меню", callback_data="backToMenu")
    builder.button(text="➕ Добавить магазин", callback_data="addMarket")
    builder.adjust(2, 2)
    return builder.as_markup()


def item_list(market_item):
    builder = InlineKeyboardBuilder()
    for item in market_item:

        if item["bought"]:
            builder.button(text="✅" + item["name"], callback_data=item["name"])
        else:
            builder.button(text="▫️" + item["name"], callback_data=item["name"])

    builder.button(text="🔙 Назад к списку магазинов", callback_data="backToMarketList")
    builder.button(text="➕ Добавить товар", callback_data="addItem")
    builder.button(text="♻️ Очистить купленные товары", callback_data="DeleteItem")
    builder.adjust(2, 2)
    return builder.as_markup()
