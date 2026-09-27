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
            "🌙 <b>پروفایل ماه‌شناسی MYSTRA</b>\n\n"
            f"📅 ماه: <b>{month_data['name']}</b>\n\n"
            f"{sign.get('symbol', '')} "
            f"<b>نشانه: {sign.get('name', '')}</b>\n"
            f"🌍 عنصر نمادین: <b>{sign.get('element', '')}</b>\n\n"
            f"{planet.get('symbol', '')} "
            f"سیاره مرتبط: <b>{planet.get('name', '')}</b>\n"
            f"✨ مضمون نمادین: <b>{planet.get('theme', '')}</b>\n\n"
            "🔑 <b>کلیدواژه‌ها</b>\n"
            f"{keyword_text}\n\n"
            "━━━━━━━━━━━━━━\n\n"
            "این بخش بر اساس سنت‌های نمادین طالع‌بینی ساخته شده "
            "و پیش‌بینی علمی شخصیت یا آینده محسوب نمی‌شود."
        )