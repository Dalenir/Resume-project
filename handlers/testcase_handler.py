from aiogram import Router, F
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State, StatesGroup

from DBuse import testcase_insert_former
from ResumeBot import all_data
from filters.filters import type_filter
from keyboards.main_keys import first_kb, reject_kb
from keyboards.testcase_keys import testcase_type_kb, testcase_passed_kb, testcase_kb
from handlers import start_hand

bot = all_data().get_bot()

class testcase_state(StatesGroup):
    title = State()
    type = State()
    testdata = State()
    initial_state = State()
    steps = State()
    expected_result = State()
    recived_result = State()
    passed = State()

router = Router()
router.message.filter(state = testcase_state)


@router.message(F.text == "Back to start")
async def t_clear(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(start_hand.security_state.passed)
    await message.answer('Another day, another hi.', reply_markup=first_kb())


@router.message(content_types=types.ContentType.TEXT, state=testcase_state.title)
async def t_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(testcase_state.type)
    await message.answer('Ok. Now choose one of the types:', reply_markup=testcase_type_kb())


@router.message(type_filter(), content_types=types.ContentType.TEXT, state=testcase_state.type)
async def t_types(message: types.Message, state: FSMContext):
    await state.update_data(type_id=message.text)
    await state.set_state(testcase_state.testdata)
    await message.answer('Seems valid for me.\nWhat about data, required for test?\n'
                         '<i>If required none, send me "None"</i>', parse_mode="HTML", reply_markup=reject_kb())

@router.message(content_types=types.ContentType.TEXT, state=testcase_state.testdata)
async def t_data(message: types.Message, state: FSMContext):
    await state.update_data(testdata=message.text)
    await state.set_state(testcase_state.initial_state)
    await message.answer('Initial state. What was it?', reply_markup=testcase_kb())

@router.message(content_types=types.ContentType.TEXT, state=testcase_state.initial_state)
async def t_initial_state(message: types.Message, state: FSMContext):
    await state.update_data(initial_state=message.text)
    await state.set_state(testcase_state.steps)
    await message.answer('The most boring part: steps to reproduce', reply_markup=testcase_kb())


@router.message(content_types=types.ContentType.TEXT, state=testcase_state.steps)
async def t_steps(message: types.Message, state: FSMContext):
    await state.update_data(steps=message.text)
    await state.set_state(testcase_state.expected_result)
    await message.answer('What was the expected result?', reply_markup=testcase_kb())

@router.message(content_types=types.ContentType.TEXT, state=testcase_state.expected_result)
async def t_expected_result(message: types.Message, state: FSMContext):
    await state.update_data(expected_result=message.text)
    await state.set_state(testcase_state.recived_result)
    await message.answer('And what was received?', reply_markup=testcase_kb())

@router.message(content_types=types.ContentType.TEXT, state=testcase_state.recived_result)
async def t_expected_result(message: types.Message, state: FSMContext):
    await state.update_data(received_result=message.text)
    await state.set_state(testcase_state.passed)
    await message.answer('So test was passed?', reply_markup=testcase_passed_kb())

@router.message((F.text == 'PASSED') | (F.text == 'NOT PASSED'), state=testcase_state.passed)
async def t_expected_result(message: types.Message, state: FSMContext):
    await state.update_data(passed=message.text)
    final_data = await state.get_data()
    result = testcase_insert_former(final_data, message.from_user.id)
    print (final_data)
    if len (result) > 1:
        await message.answer(f'Number of your bug will be {result[1]}', reply_markup=first_kb())
    await state.clear()
    await state.set_state(start_hand.security_state.passed)
    await message.answer('Well done! Another one?', reply_markup=first_kb())
