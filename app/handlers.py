import app.keyboards as kb
from aiogram import filters, types, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


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
            await message.answer(text="Wrong comand! Try again!",
                                 reply_markup=kb.main_reply_keyboard())