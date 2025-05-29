from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import json


def main_reply_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🛒 Shop List")
    builder.button(text="➕ Add a product")
    builder.button(text="🎲 Decide the fate")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def shop_list():
    builder = InlineKeyboardBuilder()
    with open("app/Base.json", "r", encoding="utf-8") as file:
        data = json.load(file)
<<<<<<< HEAD
    for shop in data:
        builder.button(text=shop, callback_data=shop)
=======
    for markets in data:
        builder.button(text=markets, callback_data=markets)
>>>>>>> e4a29ad36470138c012ef0d55c17cfeceb9e00b8
    builder.button(text="🔙 Back to main menu", callback_data="backToMenu")
    builder.button(text="➕ Add a shop", callback_data="addMarket")
    builder.adjust(2, 2)
    return builder.as_markup()


def item_list(shop_item):
    builder = InlineKeyboardBuilder()
    for item in shop_item:

        if item["bought"]:
            builder.button(text="✅" + item["name"], callback_data=item["name"])
        else:
            builder.button(text="▫️" + item["name"], callback_data=item["name"])

    builder.button(text="🔙 Back to shop list", callback_data="backToShopList")
<<<<<<< HEAD
    builder.button(text="➕ Add a item", callback_data="addItem")
=======
    builder.button(text="➕ Add a pruduct", callback_data="addItem")
>>>>>>> e4a29ad36470138c012ef0d55c17cfeceb9e00b8
    builder.button(text="♻️ Clear a bought item", callback_data="DeleteItem")
    builder.adjust(2, 2)
    return builder.as_markup()
