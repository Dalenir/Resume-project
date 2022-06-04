from aiogram import Router, F
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State, StatesGroup

from DBuse import bugreport_insert
from ResumeBot import all_data
from filters.filters import severity_filter, bug_filter
from keyboards.bugreport_keys import bugreport_kb
from keyboards.checklist_keys import checklist_severe_kb
from keyboards.main_keys import first_kb, reject_kb
from handlers import start_hand

bot = all_data().get_bot()

class bugreport_state(StatesGroup):
    hi = State()
    title = State()
    severity_id = State()
    initial_state = State()
    steps_to_reproduce = State()
    received_result = State()
    expected_result = State()
    attachments = State()



router = Router()
router.message.filter(state = bugreport_state)


@router.message(F.text == "Back to start")
async def ch_clear(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(start_hand.security_state.passed)
    await message.answer('Never stop to QA!', reply_markup=first_kb())


@router.message(bug_filter(), content_types=types.ContentType.TEXT, state=bugreport_state.hi)
async def bug_hi(message: types.Message, bug_id, state: FSMContext):
    await state.update_data(id=bug_id)
    await state.set_state(bugreport_state.title)
    await message.answer(f'Your bug is number {bug_id}. Send me title summarizing the situation:', reply_markup=bugreport_kb())


@router.message(content_types=types.ContentType.TEXT, state=bugreport_state.title)
async def bug_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(bugreport_state.severity_id)
    await message.answer('How severe this bug?', reply_markup=checklist_severe_kb())


@router.message(severity_filter(), content_types=types.ContentType.TEXT, state=bugreport_state.severity_id)
async def bug_severity(message: types.Message, severity, state: FSMContext):
    await state.update_data(severity=severity)
    await state.set_state(bugreport_state.initial_state)
    await message.answer('Describe initial system state.', reply_markup=bugreport_kb())


@router.message(content_types=types.ContentType.TEXT, state=bugreport_state.initial_state)
async def bug_initial_state(message: types.Message, state: FSMContext):
    await state.update_data(initial_state=message.text)
    await state.set_state(bugreport_state.steps_to_reproduce)
    await message.answer('Think. What steps leads us to this bug?', reply_markup=bugreport_kb())


@router.message(content_types=types.ContentType.TEXT, state=bugreport_state.steps_to_reproduce)
async def bug_steps(message: types.Message, state: FSMContext):
    await state.update_data(steps_to_reproduce=message.text)
    await state.set_state(bugreport_state.received_result)
    await message.answer('Describe received result:', reply_markup=bugreport_kb())


@router.message(content_types=types.ContentType.TEXT, state=bugreport_state.received_result)
async def bug_received_result(message: types.Message, state: FSMContext):
    await state.update_data(received_result=message.text)
    await state.set_state(bugreport_state.expected_result)
    await message.answer('Clear. And what does you expected?', reply_markup=bugreport_kb())


@router.message(content_types=types.ContentType.TEXT, state=bugreport_state.expected_result)
async def bug_expected_result(message: types.Message, state: FSMContext):
    await state.update_data(expected_result=message.text)
    await state.set_state(bugreport_state.attachments)
    await message.answer('You can attach screenshot if you want. \n'
                         'Just send me file, or "None" if you really do not fell like it.', reply_markup=reject_kb())


#TODO: Записывать в базу данных ссылку на скриншот на сервере бота
@router.message(content_types='photo', state=bugreport_state.attachments)
async def bug_attach_photo(message: types.Message, state: FSMContext):
    file = await bot.get_file(message.photo[-1].file_id)
    file_path = file.file_path
    filename = await state.get_data()
    await bot.download_file(file_path,f'./attachments/bug_{filename["id"]}.jpg')
    final_data = await state.update_data(attachment=f'bug_{filename["id"]}')
    x = bugreport_insert(final_data, message.from_user.id)
    await message.answer(f'All done, bug {x} updated', reply_markup=first_kb())
    await state.clear()
    await state.set_state(start_hand.security_state.passed)


@router.message(F.text == 'None', state=bugreport_state.attachments)
async def bug_attach_none(message: types.Message, state: FSMContext):
    final_data = await state.update_data(attachment='None')
    x = bugreport_insert(final_data, message.from_user.id)
    await message.answer(f'All done, bug {x} updated', reply_markup=first_kb())
    await state.clear()
    await state.set_state(start_hand.security_state.passed)

