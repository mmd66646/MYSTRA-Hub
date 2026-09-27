from aiogram import Router, F
from aiogram.types import CallbackQuery

from BOT.keyboards.astrology import astrology_month_keyboard
from core.astrology.engine import AstrologyEngine


router = Router()
engine = AstrologyEngine()


@router.callback_query(F.data == "astrology:menu")
async def astrology_menu(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        "🌙 <b>ماه‌شناسی MYSTRA</b>\n\n"
        "ماه تولدت رو انتخاب کن تا "
        "پروفایل نمادینش رو ببینی. ✨",
        reply_markup=astrology_month_keyboard(),
    )


@router.callback_query(F.data.startswith("astrology:month:"))
async def astrology_month(callback: CallbackQuery):
    await callback.answer()

    try:
        month = int(callback.data.split(":")[-1])
    except (ValueError, AttributeError):
        await callback.message.edit_text(
            "❌ ماه نامعتبره."
        )
        return

    result = engine.generate_result(month)

    await callback.message.edit_text(
        result,
        reply_markup=astrology_month_keyboard(),
    )