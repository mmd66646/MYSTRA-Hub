from collections import defaultdict
from typing import Dict, List


#analyze personality 
DIMENSIONS = [
    "social",
    "initiative",
    "observation",
    "independence",
    "logic",
    "emotion",
    "intuition",
    "structure",
    "flexibility",
    "curiosity",
    "caution",
    "risk",
]


class PersonalityEngine:
    """
    MYSTRA main persona 

    duty:
    - getting answers from user
    - محاسبه امتیاز هر بُعد شخصیتی
    - نرمال‌سازی نتایج
    - پیدا کردن نقاط برجسته پروفایل
    """

    def __init__(self, questions: List[dict]):
        self.questions = questions

    # ---------------------------------------------------------
    # محاسبه نتیجه
    # ---------------------------------------------------------

    def calculate(self, answers: Dict[int, int]) -> dict:
        """
        answers:
            {
                1: 0,
                2: 2,
                3: 1,
                ...
            }

        یا حتی:

            {
                "1": 0,
                "2": 2,
                "3": 1,
            }

        خروجی:
            {
                "raw_scores": {...},
                "scores": {...},
                "profile": {...},
                "answered": 12,
                "total": 12
            }
        """

        scores = defaultdict(int)

        answered_questions = 0

        for question in self.questions:

            question_id = question["id"]

            # اول کلید int را امتحان می‌کنیم
            option_index = answers.get(question_id)

            # اگر نبود، کلید string را امتحان می‌کنیم
            if option_index is None:
                option_index = answers.get(str(question_id))

            # این سؤال پاسخ داده نشده
            if option_index is None:
                continue

            # بررسی معتبر بودن شماره گزینه
            if not isinstance(option_index, int):
                continue

            if option_index < 0:
                continue

            if option_index >= len(question["options"]):
                continue

            # گزینه انتخاب‌شده
            option = question["options"][option_index]

            # اضافه کردن امتیازها
            for dimension, value in option["scores"].items():

                # اگر بعد جدیدی در سؤال وجود داشت،
                # بدون خراب کردن سیستم آن را قبول می‌کنیم.
                scores[dimension] += value

            answered_questions += 1

        # تبدیل امتیاز خام به ساختار قابل استفاده
        normalized_scores = self._normalize(scores)

        # ساخت پروفایل کلی
        profile = self._build_profile(normalized_scores)

        return {
            "raw_scores": dict(scores),
            "scores": normalized_scores,
            "profile": profile,
            "answered": answered_questions,
            "total": len(self.questions),
        }

    # ---------------------------------------------------------
    # Normalization
    # ---------------------------------------------------------

    def _normalize(self, scores: dict) -> dict:
        """
        امتیاز خام هر بُعد را به ساختاری خواناتر تبدیل می‌کند.

        مثال:

        {
            "social": {
                "raw": 6,
                "level": "خیلی بالا"
            }
        }
        """

        result = {}

        for dimension in DIMENSIONS:

            value = scores.get(dimension, 0)

            result[dimension] = {
                "raw": value,
                "level": self._level(value),
            }

        # اگر بعدها dimension جدیدی به questions اضافه شد،
        # آن را هم از خروجی حذف نمی‌کنیم.
        for dimension, value in scores.items():

            if dimension not in result:

                result[dimension] = {
                    "raw": value,
                    "level": self._level(value),
                }

        return result

    # ---------------------------------------------------------
    # تعیین سطح
    # ---------------------------------------------------------

    @staticmethod
    def _level(value: int) -> str:
        """
        تبدیل امتیاز عددی به سطح توصیفی.
        """

        if value >= 5:
            return "خیلی بالا"

        if value >= 3:
            return "بالا"

        if value >= 1:
            return "متوسط رو به بالا"

        if value <= -4:
            return "خیلی پایین"

        if value <= -2:
            return "پایین"

        return "متعادل"

    # ---------------------------------------------------------
    # ساخت پروفایل
    # ---------------------------------------------------------

    def _build_profile(self, scores: dict) -> dict:
        """
        قوی‌ترین و ضعیف‌ترین ابعاد را پیدا می‌کند.
        """

        raw_scores = {
            dimension: data["raw"]
            for dimension, data in scores.items()
        }

        # از بیشترین به کمترین
        strongest = sorted(
            raw_scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        # از کمترین به بیشترین
        weakest = sorted(
            raw_scores.items(),
            key=lambda item: item[1],
        )

        return {
            "strongest": strongest[:3],
            "weakest": weakest[:3],
        }

    # ---------------------------------------------------------
    # دریافت قوی‌ترین ابعاد
    # ---------------------------------------------------------

    def get_strongest_dimensions(
        self,
        result: dict,
        limit: int = 3,
    ) -> list:
        """
        مثال:

        [
            ("curiosity", 7),
            ("initiative", 6),
            ("social", 5)
        ]
        """

        strongest = result.get("profile", {}).get(
            "strongest",
            [],
        )

        return strongest[:limit]

    # ---------------------------------------------------------
    # دریافت ضعیف‌ترین ابعاد
    # ---------------------------------------------------------

    def get_weakest_dimensions(
        self,
        result: dict,
        limit: int = 3,
    ) -> list:
        """
        ضعیف‌ترین ابعاد پروفایل را برمی‌گرداند.
        """

        weakest = result.get("profile", {}).get(
            "weakest",
            [],
        )

        return weakest[:limit]

    # ---------------------------------------------------------
    # دریافت امتیاز یک بُعد
    # ---------------------------------------------------------

    def get_dimension_score(
        self,
        result: dict,
        dimension: str,
    ) -> int:
        """
        مثال:

        engine.get_dimension_score(result, "social")

        خروجی:
            5
        """

        scores = result.get("scores", {})

        dimension_data = scores.get(dimension)

        if not dimension_data:
            return 0

        return dimension_data.get("raw", 0)

    # ---------------------------------------------------------
    # دریافت سطح یک بُعد
    # ---------------------------------------------------------

    def get_dimension_level(
        self,
        result: dict,
        dimension: str,
    ) -> str:
        """
        مثال:

        engine.get_dimension_level(result, "social")

        خروجی:
            "بالا"
        """

        scores = result.get("scores", {})

        dimension_data = scores.get(dimension)

        if not dimension_data:
            return "متعادل"

        return dimension_data.get(
            "level",
            "متعادل",
        )

    # ---------------------------------------------------------
    # درصد پاسخ‌دهی
    # ---------------------------------------------------------

    @staticmethod
    def completion_percentage(result: dict) -> float:
        """
        درصد تکمیل تست را برمی‌گرداند.
        """

        total = result.get("total", 0)
        answered = result.get("answered", 0)

        if total == 0:
            return 0.0

        return round(
            (answered / total) * 100,
            1,
        )

    # ---------------------------------------------------------
    # بررسی کامل بودن تست
    # ---------------------------------------------------------

    @staticmethod
    def is_complete(result: dict) -> bool:
        """
        مشخص می‌کند همه سؤال‌ها پاسخ داده شده‌اند یا نه.
        """

        return (
            result.get("answered", 0)
            >= result.get("total", 0)
        )