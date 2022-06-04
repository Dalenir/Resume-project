from aiogram import Router, F
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State, StatesGroup
from psycopg2 import sql

from DBuse import safe_data_getter, checklist_insert
from ResumeBot import all_data
from filters.filters import severity_filter
from keyboards.checklist_keys import checklist_kb, checklist_severe_kb, checklist_passed_kb
from keyboards.main_keys import first_kb, reject_kb

bot = all_data().get_bot()

class checklist_state(StatesGroup):
    group_id = State()
    object_of_assay = State()
    priority = State()
    testdata = State()
    expected_result = State()
    passed = State()



router = Router()
router.message.filter(state = checklist_state)


@router.message(F.text == "Back to start")
async def ch_clear(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Never stop to QA!', reply_markup=first_kb())


@router.message(content_types=types.ContentType.TEXT, state=checklist_state.group_id)
async def ch_group(message: types.Message, state: FSMContext):
    dnew = {'group': message.text}
    sql_query = sql.SQL('SELECT "id" FROM project.web_check_groups WHERE ({}) = ({});').format(
        sql.SQL(', ').join(map(sql.Identifier, dnew)),
        sql.SQL(", ").join(map(sql.Placeholder, dnew))
    )
    group_list = safe_data_getter(sql_query, dnew)
    if group_list == []:
        sql_query = sql.SQL('INSERT INTO project.web_check_groups ({}) VALUES ({}) RETURNING id;').format(
        sql.SQL(', ').join(map(sql.Identifier, dnew)),
        sql.SQL(", ").join(map(sql.Placeholder, dnew))
        )
        group_list = safe_data_getter(sql_query, dnew)
    await state.update_data(group_id=group_list[0][0])
    await state.set_state(checklist_state.object_of_assay)
    await message.answer('Cool. What is the subject of study?', reply_markup=checklist_kb())


@router.message(content_types=types.ContentType.TEXT, state=checklist_state.object_of_assay)
async def ch_obj(message: types.Message, state: FSMContext):
    await state.update_data(object_of_assay=message.text)
    await state.set_state(checklist_state.priority)
    await message.answer('And how severe for the project to fail it?', reply_markup=checklist_severe_kb())


@router.message(severity_filter(), content_types=types.ContentType.TEXT, state=checklist_state.priority)
async def ch_priority(message: types.Message, state: FSMContext):
    await state.update_data(priority=message.text)
    await state.set_state(checklist_state.testdata)
    await message.answer('Fantastic work! Do we need some data or additional information?\n You can send me any, or "None", if it is not required', reply_markup=reject_kb())


@router.message(content_types=types.ContentType.TEXT, state=checklist_state.testdata)
async def ch_recived(message: types.Message, state: FSMContext):
    await state.update_data(test_data=message.text)
    await state.set_state(checklist_state.passed)
    await message.answer('So was test passed?', reply_markup=checklist_passed_kb())

@router.message((F.text == 'TEST PASSED') | (F.text == 'TEST FAILED'), state=checklist_state.passed)
async def ch_passed(message: types.Message, state: FSMContext):
    if message.text == 'TEST PASSED':
        await state.update_data(passed='True')
    elif message.text == 'TEST FAILED':
        await state.update_data(passed ='False')
    final_data = await state.get_data()
    result = checklist_insert(final_data, message.from_user.id)
    if len (result) > 1:
        await message.answer(f'Number of your bug will be {result[1]}', reply_markup=first_kb())
    await state.clear()
    await message.answer('Well done! Another one?', reply_markup=first_kb())