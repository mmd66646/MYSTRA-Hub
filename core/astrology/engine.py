from data.astrology.months import PERSIAN_MONTHS
from data.astrology.signs import SIGNS
from data.astrology.planets import PLANETS


class AstrologyEngine:

    def get_month(self, month: int) -> dict | None:
        return PERSIAN_MONTHS.get(month)

    def get_profile(self, month: int) -> dict | None:
        month_data = self.get_month(month)

        if not month_data:
            return None

        sign_key = month_data["sign"]
        planet_key = month_data["planet"]

        sign = SIGNS.get(sign_key, {})
        planet = PLANETS.get(planet_key, {})

        return {
            "month": month_data,
            "sign": sign,
            "planet": planet,
        }

    def generate_result(self, month: int) -> str:
        profile = self.get_profile(month)

        if not profile:
            return "❌ ماه واردشده معتبر نیست."

        month_data = profile["month"]
        sign = profile["sign"]
        planet = profile["planet"]

        keywords = sign.get("keywords", [])
        keyword_text = " • ".join(keywords)

        return (
            "🌙 <b>ماه‌شناسی MYSTRA</b>\n\n"

            f"📅 ماه تولد: <b>{month_data['name']}</b>\n"
            f"{sign.get('symbol', '')} "
            f"نشانه: <b>{sign.get('name', '')}</b>\n"
            f"🌍 عنصر: <b>{sign.get('element', month_data.get('element', ''))}</b>\n"
            f"{planet.get('symbol', '')} "
            f"سیاره: <b>{planet.get('name', '')}</b>\n\n"

            f"✨ <b>{month_data.get('theme', '')}</b>\n\n"

            "━━━━━━━━━━━━━━\n\n"

            "🔮 <b>راز ماه تو</b>\n\n"
            f"{month_data.get('mystery', '').strip()}\n\n"

            "━━━━━━━━━━━━━━\n\n"

            "🕯️ <b>آنچه درون تو پنهان است</b>\n\n"
            f"{month_data.get('hidden', '').strip()}\n\n"

            "━━━━━━━━━━━━━━\n\n"

            "✨ <b>نیروی درونی</b>\n\n"
            f"{month_data.get('strength', '').strip()}\n\n"

            "🌑 <b>سایه‌ی شخصیت</b>\n\n"
            f"{month_data.get('shadow', '').strip()}\n\n"

            "❤️ <b>در قلمرو احساس</b>\n\n"
            f"{month_data.get('love', '').strip()}\n\n"

            "🔑 <b>کلیدواژه‌های تو</b>\n"
            f"{keyword_text}\n\n"

            "━━━━━━━━━━━━━━\n\n"

            "🔮 <b>فال MYSTRA</b>\n\n"
            "برای آشکار شدن فال اختصاصی ماهت،\n"
            "روی دکمه زیر بزن... 🕯️"
        )