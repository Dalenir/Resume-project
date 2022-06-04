import asyncio
import pathlib

from aiogram import Router, F
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State, StatesGroup
from aiogram.types import Message, FSInputFile

from DBuse import all_tables_dump
from handlers.bugreport_handler import bugreport_state
from handlers.checklist_handler import checklist_state
from handlers.testcase_handler import testcase_state
from keyboards.bugreport_keys import bugreport_hi_kb
from keyboards.checklist_keys import checklist_group_kb
from keyboards.main_keys import first_kb
from keyboards.testcase_keys import testcase_kb
from bata import all_data

router = Router()

class security_state(StatesGroup):
    passed = State()


@router.message(commands=["start"])
async def cmd_start(message: Message):
    await message.answer("Hello!\nEnter codephrase please:")


@router.message(commands=["result"])
async def cmd_start(message: Message):
    path = pathlib.Path(__file__).parents[1].resolve()
    all_tables_dump(f"{path}/tables_here")
    await message.answer("Your data at this moment:", reply_markup=first_kb())
    await asyncio.sleep(1)
    await message.answer_document(FSInputFile(f"{path}/tables_here/bugreports.csv"), caption="Багрепорты")
    await asyncio.sleep(1)
    await message.answer_document(FSInputFile(f"{path}/tables_here/checklist.csv"), caption="Чеклист")
    await asyncio.sleep(1)
    await message.answer_document(FSInputFile(f"{path}/tables_here/testcases.csv"), caption="Тесткейсы")


@router.message(F.text == all_data().password)
async def testcase_hi(message: Message, state=FSMContext):
    await state.set_state(security_state.passed)
    await message.answer('Ok!', reply_markup=first_kb())

@router.message(text_contains=('testcase'), content_types=types.ContentType.TEXT, text_ignore_case=True, state=security_state.passed)
async def testcase_hi(message: Message, state=FSMContext):
    await state.set_state(testcase_state.title)
    text = "Well, hello there. Let's start with some title for your testcase"
    await message.answer(text, reply_markup=testcase_kb())


@router.message(text_contains=('checklist'), content_types=types.ContentType.TEXT, text_ignore_case=True, state=security_state.passed)
async def checklist_hi(message: Message, state=FSMContext):
    await state.set_state(checklist_state.group_id)
    text = "Checklist. Fast, efficent, criptyic for new testers.\n\nHere's a list of existing groups. Send me any, or " \
           "an new one!"
    await message.answer(text, reply_markup=checklist_group_kb())


@router.message(text_contains=('bug'), content_types=types.ContentType.TEXT, text_ignore_case=True, state=security_state.passed)
async def bugreport_hi(message: Message, state=FSMContext):
    await state.set_state(bugreport_state.hi)
    text = "If you want to fill existing bugreport, send me it's number.\nIf you want to report a new one, send me 'New'"
    await message.answer(text, reply_markup=bugreport_hi_kb())
