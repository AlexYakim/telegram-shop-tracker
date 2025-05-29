import app.keyboards as kb
from aiogram import filters, types, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from random import choice
import json
from asyncio import sleep as async_sleep
router = Router()


class ChoiceState(StatesGroup):
    MainMenu = State()
    ShopItems = State()
    ItemHandle = State()
    AddItem_SelectShop = State()
    AddItem_InputName = State()
    AddShop_InputName = State()
    CoinFlip = State()


@router.message(filters.CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    await message.delete()
    await state.set_state(ChoiceState.MainMenu)
    await message.answer(f"Welcome user #{message.from_user.id} 🤓. Select command",
                         reply_markup=kb.main_reply_keyboard())


@router.message(ChoiceState.MainMenu)
async def main_menu_handler(message: types.Message, state: FSMContext):
    await message.delete()
    match message.text:
        case "🛒 Shop List":
            await state.set_state(ChoiceState.ShopItems)
            await message.answer(text="Choose a shop ", reply_markup=kb.shop_list())
        case "➕ Add a product":
            await state.set_state(ChoiceState.AddItem_SelectShop)
            await message.answer(text="Which shop to add an item to?", reply_markup=kb.shop_list())
        case "🎲 Decide the fate":
            await state.set_state(ChoiceState.CoinFlip)
            await message.answer(text="Enter item name for decide fate of this item")
        case _:
            await message.answer(text="Wrong comand! Try again!",reply_markup=kb.main_reply_keyboard())


@router.callback_query(ChoiceState.ShopItems)
async def shop_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(callback.data)
    with open("app/Base.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    match callback.data:
        case "backToMenu":
            await state.clear()
            await state.set_state(ChoiceState.MainMenu)
            await callback.message.answer(text="🤓. Select command",
                                          reply_markup=kb.main_reply_keyboard())
        case "addShop":
            await state.clear()
            await state.set_state(ChoiceState.AddShop_InputName)
            await callback.message.answer(text="Enter a new shop name ( if you wand add more than one shop, you can"
                                               "enter them names separated by commas")
        case _:
            await state.clear()
            await state.set_state(ChoiceState.ItemHandle)
            await state.update_data(shop=callback.data)
            await callback.message.answer(text=callback.data,
                                          reply_markup=kb.item_list(data[callback.data]))


@router.callback_query(ChoiceState.ItemHandle)
async def item_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(callback.data)
    with open("app/Base.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    state_data = await state.get_data()
    shop = state_data.get("shop")
    match callback.data:
        case "DeleteItem":
            data[shop] = [item for item in data[shop] if item["bought"] == False]
            with open("app/Base.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            await callback.message.edit_reply_markup(reply_markup=kb.item_list(data[shop]))
        case "addItem":
            await state.clear()
            await state.set_state(ChoiceState.AddItem_InputName)
            await state.update_data(shop=shop)
            await callback.message.answer(text="Enter a new item name ( if you wand add more than one item, you can"
                                               "enter them names separated by commas")
        case "backToShopList":
            await state.clear()
            await state.set_state(ChoiceState.ShopItems)
            await callback.message.answer(text="Choose a shop", reply_markup=kb.shop_list())
        case _:
            for item in data[shop]:
                if item["name"] == callback.data:
                    item["bought"] = not item["bought"]
            with open("app/Base.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            await callback.message.edit_reply_markup(reply_markup=kb.item_list(data[shop]))


@router.callback_query(ChoiceState.AddItem_SelectShop)
async def add_items_select_shop(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(callback.data)
    await state.clear()
    await state.update_data(shop=callback.data)
    await state.set_state(ChoiceState.AddItem_InputName)
    await callback.message.answer(text="Enter a new item name ( if you wand add more than one item, you can"
                                       " enter them names separated by commas")


@router.message(ChoiceState.AddItem_InputName)
async def add_items_input_name(message: types.Message, state: FSMContext):
    with open("app/Base.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    state_data = await state.get_data()
    shop = state_data["shop"]
    items = message.text.split(",")
    for item in items:
        data[shop].append({"name": item, "bought": False})
    with open("app/Base.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    await state.clear()
    await state.update_data(shop=shop)
    await state.set_state(ChoiceState.ItemHandle)
    await message.answer(text=shop, reply_markup=kb.item_list(data[shop]))


@router.message(ChoiceState.AddShop_InputName)
async def add_shop_input_name(message: types.Message, state: FSMContext):
    with open("app/Base.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    shops = message.text.split(",")
    for shop in shops:
        if shop not in data:
            data[shop] = []
    with open("app/Base.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    await state.clear()
    await state.set_state(ChoiceState.ShopItems)
    await message.answer(text="Choose a shop", reply_markup=kb.shop_list())


@router.message(ChoiceState.CoinFlip)
async def coin_flip(message: types.Message, state: FSMContext):
    await message.delete()
    emojis = ["🏀", "⚽", "🎲", ]
    emoji = choice(emojis)
    throw_msg = await message.answer_dice(emoji=emoji)
    await async_sleep(3)
    value = throw_msg.dice.value
    if emoji == "🏀":
        await message.answer("🏀 Got it! Buy it!" if value == 1 else "🏀 You didn't get... Don't buy")
    elif emoji == "⚽":
        await message.answer("⚽ Goal! Buy!" if value == 1 else "⚽ Pass... Don't buy.")
    elif emoji == "🎲":
        await message.answer(f"🎲 Rolled: {value}, Buy it!" if value >= 3 else f"🎲 Rolled: {value}, Don't buy it")
    await state.clear()
    await state.set_state(ChoiceState.MainMenu)
    await message.answer(text="🤓. Select command",
                         reply_markup=kb.main_reply_keyboard())
