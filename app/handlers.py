import keyboards as kb
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
