from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, FSInputFile

from BOT.keyboards.astrology import (
    astrology_month_keyboard,
    astrology_fortune_keyboard,
)
from core.astrology.engine import AstrologyEngine


router = Router()
engine = AstrologyEngine()


ASTROLOGY_MENU_TEXT = (
    "🌙 <b>ماه‌شناسی MYSTRA</b>\n\n"
    "هر ماه، داستانی پنهان در خود دارد...\n"
    "ماه تولدت را انتخاب کن تا پرده از "
    "بخشی از آن برداشته شود. 🔮\n\n"
    "🕯️ <i>شاید چیزی درباره خودت بخوانی "
    "که قبلاً به آن فکر نکرده بودی.</i>"
)


async def show_text(callback: CallbackQuery, text: str, reply_markup):
    """
    نمایش متن بلند.
    اگر پیام فعلی عکس باشد، پاک می‌شود و پیام متنی جدید می‌آید.
    اگر پیام فعلی متنی باشد، همان ویرایش می‌شود.
    """
    message = callback.message

    if message.photo:
        await message.delete()
        await message.answer(text, reply_markup=reply_markup)
        return

    try:
        await message.edit_text(text, reply_markup=reply_markup)
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise


@router.callback_query(F.data == "astrology:menu")
async def astrology_menu(callback: CallbackQuery):
    await callback.answer()

    message = callback.message

    if message.photo:
        try:
            await message.edit_caption(
                caption=ASTROLOGY_MENU_TEXT,
                reply_markup=astrology_month_keyboard(),
            )
        except TelegramBadRequest as e:
            if "message is not modified" not in str(e):
                raise
        return

    # اگر پیام متنی بود، عکس منو را دوباره می‌فرستیم
    await message.delete()
    await message.answer_photo(
        photo=FSInputFile("cards/main_menu_fixed.png"),
        caption=ASTROLOGY_MENU_TEXT,
        reply_markup=astrology_month_keyboard(),
    )


@router.callback_query(F.data.startswith("astrology:month:"))
async def astrology_month(callback: CallbackQuery):
    await callback.answer()

    try:
        month = int(callback.data.split(":")[-1])
    except (ValueError, AttributeError):
        await show_text(
            callback,
            "❌ <b>ماه نامعتبر است.</b>\n\n"
            "لطفاً یکی از ماه‌های موجود را انتخاب کن.",
            astrology_month_keyboard(),
        )
        return

    result = engine.generate_result(month)

    await show_text(
        callback,
        result,
        astrology_fortune_keyboard(month),
    )


@router.callback_query(F.data.startswith("astrology:fortune:"))
async def astrology_fortune(callback: CallbackQuery):
    await callback.answer("🔮 فال MYSTRA در حال آشکار شدن است...")

    try:
        month = int(callback.data.split(":")[-1])
    except (ValueError, AttributeError):
        await show_text(
            callback,
            "❌ <b>ماه نامعتبر است.</b>\n\n"
            "لطفاً دوباره وارد ماه‌شناسی شو.",
            astrology_month_keyboard(),
        )
        return

    profile = engine.get_profile(month)

    if not profile:
        await show_text(
            callback,
            "❌ <b>ماه نامعتبر است.</b>",
            astrology_month_keyboard(),
        )
        return

    month_data = profile["month"]

    fortune = month_data.get(
        "fortune",
        "نشانه‌ها هنوز چیزی را آشکار نکرده‌اند..."
    ).strip()

    month_name = month_data.get("name", "")

    await show_text(
        callback,
        "🔮 <b>فال MYSTRA</b>\n\n"
        f"🌙 ماه: <b>{month_name}</b>\n\n"
        "━━━━━━━━━━━━━━\n\n"
        f"{fortune}\n\n"
        "━━━━━━━━━━━━━━\n\n"
        "🕯️ <i>همه‌ی نشانه‌ها قرار نیست "
        "همان لحظه خودشان را نشان دهند...</i>",
        astrology_fortune_keyboard(month),
    )