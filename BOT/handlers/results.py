from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.database import get_latest_personality_result
from core.personality.results import generate_result
from core.personality.engine import PersonalityEngine


router = Router()


@router.callback_query(F.data == "results")
async def results_handler(callback: CallbackQuery):

    await callback.answer()

    result_row = get_latest_personality_result(
        callback.from_user.id
    )

    if not result_row:
        await callback.message.edit_text(
            "🃏 <b>نتایج من</b>\n\n"
            "هنوز هیچ نتیجه‌ای برایت ثبت نشده.\n\n"
            "🧠 اول تست شخصیت‌شناسی MYSTRA را انجام بده "
            "تا اولین پروفایل شخصیتت ساخته شود. 🔮",
            reply_markup=None,
        )
        return

    import json

    try:
        result = json.loads(
            result_row["result_json"]
        )
    except (json.JSONDecodeError, TypeError):
        await callback.message.edit_text(
            "❌ <b>خطا در بازیابی نتیجه</b>\n\n"
            "نتیجه ذخیره‌شده قابل خواندن نیست.",
        )
        return

    result_text = generate_result(result)

    await callback.message.edit_text(
        result_text,
    )