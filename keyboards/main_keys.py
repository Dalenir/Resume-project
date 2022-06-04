from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder




def first_kb():
    markup = ReplyKeyboardBuilder()
    btn1 = types.KeyboardButton(text="New testcase")
    btn2 = types.KeyboardButton(text="Fill checklist")
    btn3 = types.KeyboardButton(text="Bugreports")
    markup.add(btn1, btn2)
    markup.row(btn3)
    return markup.as_markup(resize_keyboard=True, input_field_placeholder="Or maybe just use Jira, lol")

def reject_kb():
    markup = ReplyKeyboardBuilder()
    btn1 = types.KeyboardButton(text="None")
    btn2 = types.KeyboardButton(text="Back to start")
    markup.row(btn1)
    markup.row(btn2)
    return markup.as_markup(resize_keyboard=True)
