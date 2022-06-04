from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from DBuse import data_getter


def testcase_kb():
    markup = ReplyKeyboardBuilder()
    btn1 = types.KeyboardButton(text="Back to start")
    markup.row(btn1)
    return markup.as_markup(resize_keyboard=True)

def testcase_type_kb():
    markup = ReplyKeyboardBuilder()
    t_types = data_getter('SELECT type_name FROM project.testtype WHERE type_name is not NULL;')
    for t_type in t_types:
        btn = types.KeyboardButton(text=f"{t_type[0]}")
        markup.add(btn)
    markup.adjust(3,3,3)
    markup.row(types.KeyboardButton(text="Back to start"))
    return markup.as_markup(resize_keyboard=True)

def testcase_passed_kb():
    markup = ReplyKeyboardBuilder()
    btn1 = types.KeyboardButton(text="PASSED")
    btn2 = types.KeyboardButton(text="NOT PASSED")
    markup.row(btn1, btn2)
    markup.row(types.KeyboardButton(text="Back to start"))
    return markup.as_markup(resize_keyboard=True)
