"""Telegram bot handlers and menus."""
from __future__ import annotations

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from storage.database import Database

router = Router()
db = Database()

MENU_KEY = "main_menu"


def main_menu_kb() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="🚨Сигналы", callback_data="signals")
    builder.button(text="👀Мои пары", callback_data="pairs")
    builder.button(text="📊Статистика", callback_data="stats")
    builder.button(text="⚙️Настройки", callback_data="settings")
    builder.adjust(2, 2)
    return builder


@router.message(F.text == "/start")
async def cmd_start(message: Message) -> None:
    await message.answer("Главное меню", reply_markup=main_menu_kb().as_markup())


@router.message(F.text == "Показать меню")
async def show_menu(message: Message) -> None:
    await message.answer("Главное меню", reply_markup=main_menu_kb().as_markup())


@router.callback_query(F.data.in_("signals"))
async def on_signals(call: CallbackQuery) -> None:
    await call.message.edit_text("Сигналы пока отсутствуют", reply_markup=back_kb().as_markup())
    await call.answer()


@router.callback_query(F.data.in_("pairs"))
async def on_pairs(call: CallbackQuery) -> None:
    pairs = db.get_pairs()
    text = "Отслеживаемые пары:\n" + "\n".join(pairs) if pairs else "Нет пар"
    await call.message.edit_text(text, reply_markup=back_kb().as_markup())
    await call.answer()


@router.callback_query(F.data.in_("stats"))
async def on_stats(call: CallbackQuery) -> None:
    await call.message.edit_text("Статистика недоступна", reply_markup=back_kb().as_markup())
    await call.answer()


@router.callback_query(F.data.in_("settings"))
async def on_settings(call: CallbackQuery) -> None:
    await call.message.edit_text("Настройки недоступны", reply_markup=back_kb().as_markup())
    await call.answer()


@router.callback_query(F.data == "back")
async def back_to_menu(call: CallbackQuery) -> None:
    await call.message.edit_text("Главное меню", reply_markup=main_menu_kb().as_markup())
    await call.answer()


def back_kb() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Назад", callback_data="back")
    return builder

