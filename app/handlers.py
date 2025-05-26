#from My_Buttons_class import MyButtons
from aiogram import filters, types, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(filters.CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    await message.delete()