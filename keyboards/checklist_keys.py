from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from DBuse import data_getter


def checklist_kb():
    markup = ReplyKeyboardBuilder()
    btn1 = types.KeyboardButton(text="Back to start")
    markup.row(btn1)
    return markup.as_markup(resize_keyboard=True)

def checklist_group_kb():
    markup = ReplyKeyboardBuilder()
    ch_groups = data_getter('SELECT "group" FROM project.web_check_groups WHERE "group" is not NULL;')
    for ch_group in ch_groups:
        btn = types.KeyboardButton(text=f"{ch_group[0]}")
        markup.add(btn)
    markup.adjust(3,3,3)
    markup.row(types.KeyboardButton(text="Back to start"))
    return markup.as_markup(resize_keyboard=True)

def checklist_severe_kb():
    markup = ReplyKeyboardBuilder()
    ch_sev_list = data_getter('SELECT "severity" FROM project.bugseverity WHERE "severity" is not NULL;')
    for ch_severe in ch_sev_list:
        btn = types.KeyboardButton(text=f"{ch_severe[0]}")
        markup.add(btn)
    markup.adjust(3,3,3)
    markup.row(types.KeyboardButton(text="Back to start"))
    return markup.as_markup(resize_keyboard=True)

def checklist_passed_kb():
    markup = ReplyKeyboardBuilder()
    btn1 = types.KeyboardButton(text="TEST PASSED")
    btn2 = types.KeyboardButton(text="TEST FAILED")
    markup.row(btn1, btn2)
    markup.row(types.KeyboardButton(text="Back to start"))
    return markup.as_markup(resize_keyboard=True)