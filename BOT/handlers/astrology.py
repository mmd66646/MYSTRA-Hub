from aiogram import Router, F
from aiogram.types import CallbackQuery

from BOT.keyboards.astrology import (
    astrology_month_keyboard,
    astrology_fortune_keyboard,
)
from core.astrology.engine import AstrologyEngine


router = Router()
engine = AstrologyEngine()


@router.callback_query(F.data == "astrology:menu")
async def astrology_menu(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        "🌙 <b>ماه‌شناسی MYSTRA</b>\n\n"
        "هر ماه، داستانی پنهان در خود دارد...\n"
        "ماه تولدت را انتخاب کن تا پرده از "
        "بخشی از آن برداشته شود. 🔮\n\n"
        "🕯️ <i>شاید چیزی درباره خودت بخوانی "
        "که قبلاً به آن فکر نکرده بودی.</i>",
        reply_markup=astrology_month_keyboard(),
    )


@router.callback_query(F.data.startswith("astrology:month:"))
async def astrology_month(callback: CallbackQuery):
    await callback.answer()

    try:
        month = int(callback.data.split(":")[-1])
    except (ValueError, AttributeError):
        await callback.message.edit_text(
            "❌ <b>ماه نامعتبر است.</b>\n\n"
            "لطفاً یکی از ماه‌های موجود را انتخاب کن.",
            reply_markup=astrology_month_keyboard(),
        )
        return

    result = engine.generate_result(month)

    await callback.message.edit_text(
        result,
        reply_markup=astrology_fortune_keyboard(month),
    )


@router.callback_query(F.data.startswith("astrology:fortune:"))
async def astrology_fortune(callback: CallbackQuery):
    await callback.answer("🔮 فال MYSTRA در حال آشکار شدن است...")

    try:
        month = int(callback.data.split(":")[-1])
    except (ValueError, AttributeError):
        await callback.message.edit_text(
            "❌ <b>ماه نامعتبر است.</b>\n\n"
            "لطفاً دوباره وارد ماه‌شناسی شو.",
            reply_markup=astrology_month_keyboard(),
        )
        return

    profile = engine.get_profile(month)

    if not profile:
        await callback.message.edit_text(
            "❌ <b>ماه نامعتبر است.</b>",
            reply_markup=astrology_month_keyboard(),
        )
        return

    month_data = profile["month"]

    fortune = month_data.get(
        "fortune",
        "نشانه‌ها هنوز چیزی را آشکار نکرده‌اند..."
    ).strip()

    month_name = month_data.get("name", "")

    await callback.message.edit_text(
        "🔮 <b>فال MYSTRA</b>\n\n"
        f"🌙 ماه: <b>{month_name}</b>\n\n"
        "━━━━━━━━━━━━━━\n\n"
        f"{fortune}\n\n"
        "━━━━━━━━━━━━━━\n\n"
        "🕯️ <i>همه‌ی نشانه‌ها قرار نیست "
        "همان لحظه خودشان را نشان دهند...</i>",
        reply_markup=astrology_fortune_keyboard(month),
    )