from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def bugreport_kb():
    markup = ReplyKeyboardBuilder()
    btn1 = types.KeyboardButton(text="Back to start")
    markup.row(btn1)
    return markup.as_markup(resize_keyboard=True)

def bugreport_hi_kb():
    markup = ReplyKeyboardBuilder()
    btn1 = types.KeyboardButton(text="New")
    btn2 = types.KeyboardButton(text="Back to start")
    markup.row(btn1)
    markup.row(btn2)
    return markup.as_markup(resize_keyboard=True)
