from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


def main_menu_keyboard() -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🧠 شخصیت‌شناسی",
                    callback_data="personality:start",
                ),
            ],

            [
                InlineKeyboardButton(
                    text="🌙 ماه‌شناسی",
                    callback_data="astrology:menu",
                ),
                InlineKeyboardButton(
                    text="❤️ سازگاری",
                    callback_data="compatibility:menu",
                ),
            ],

            [
                InlineKeyboardButton(
                    text="💎 سنگ‌ها",
                    callback_data="stones:menu",
                ),
                InlineKeyboardButton(
                    text="🧩 تست‌های بیشتر",
                    callback_data="tests:menu",
                ),
            ],

            [
                InlineKeyboardButton(
                    text="👤 پروفایل من",
                    callback_data="profile",
                ),
                InlineKeyboardButton(
                    text="🃏 نتایج من",
                    callback_data="results",
                ),
            ],

            [
                InlineKeyboardButton(
                    text="🛠 پشتیبانی MYSTRA Hub",
                    callback_data="support",
                ),
            ],

            [
                InlineKeyboardButton(
                    text="ℹ️ درباره MYSTRA",
                    callback_data="about",
                ),
            ],
        ]
    )


def personality_options_keyboard(
    question: dict,
) -> InlineKeyboardMarkup:

    buttons = []

    for index, option in enumerate(
        question["options"]
    ):
        buttons.append(
            [
                InlineKeyboardButton(
                    text=option["text"],
                    callback_data=(
                        f"personality:answer:{index}"
                    ),
                )
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


def personality_finish_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 دوباره انجام بده",
                    callback_data="personality:start",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 منوی اصلی",
                    callback_data="menu",
                )
            ],
        ]
    )