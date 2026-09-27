from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from BOT.keyboards.main import main_menu_keyboard
from database.database import create_or_update_user


router = Router()


def main_menu_text():
    return (
        "🔮 <b>MYSTRA Hub</b>\n\n"
        "کشف کن، مقایسه کن، بیشتر خودت رو بشناس.\n\n"
        "انتخاب کن از کجا شروع کنیم 👇"
    )


@router.message(CommandStart())
async def start_handler(message: Message):
    create_or_update_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
    )

    await message.answer(
        main_menu_text(),
        reply_markup=main_menu_keyboard(),
    )


@router.callback_query(lambda c: c.data == "menu")
async def menu_handler(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        main_menu_text(),
        reply_markup=main_menu_keyboard(),
    )


@router.callback_query(lambda c: c.data == "about")
async def about_handler(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        "ℹ️ <b>درباره MYSTRA</b>\n\n"
        "MYSTRA یک پروژه تعاملی برای کشف "
        "الگوهای شخصیتی و ساخت پروفایل‌های اختصاصیه.\n\n"
        "🧠 شخصیت‌شناسی\n"
        "🌙 ماه‌شناسی\n"
        "❤️ سازگاری\n"
        "💎 سنگ‌ها\n"
        "🃏 نتایج شخصی\n\n"
        "━━━━━━━━━━━━━━\n\n"
        "ساخته شده توسط <b>MmdMehdi</b>\n"
        "🌐 <a href=\"https://www.mmdmehdi.ir/\">mmdmehdi.ir</a>",
        reply_markup=main_menu_keyboard(),
    )


@router.callback_query(lambda c: c.data == "support")
async def support_handler(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        "🛠 <b>پشتیبانی MYSTRA Hub</b>\n\n"
        "برای ارتباط با پشتیبانی، "
        "می‌تونی با یکی از افراد زیر در ارتباط باشی:\n\n"
        "👤 <a href=\"https://t.me/Sport31Hnc\">پشتیبانی ۱</a>\n"
        "👤 <a href=\"https://t.me/AK477C4\">پشتیبانی ۲</a>\n\n"
        "━━━━━━━━━━━━━━\n\n"
        "🌐 <b>وب‌سایت MmdMehdi</b>\n"
        "<a href=\"https://www.mmdmehdi.ir/\">mmdmehdi.ir</a>",
        reply_markup=main_menu_keyboard(),
    )