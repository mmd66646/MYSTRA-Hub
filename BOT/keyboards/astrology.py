from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def astrology_month_keyboard():

    months = [
        ("🌱 فروردین", 1),
        ("🌿 اردیبهشت", 2),
        ("🌤 خرداد", 3),
        ("🌊 تیر", 4),
        ("☀️ مرداد", 5),
        ("🌾 شهریور", 6),
        ("🍂 مهر", 7),
        ("🌑 آبان", 8),
        ("🔥 آذر", 9),
        ("❄️ دی", 10),
        ("⚡ بهمن", 11),
        ("🌧 اسفند", 12),
    ]

    buttons = []

    for i in range(0, len(months), 2):

        row = []

        for name, month in months[i:i + 2]:

            row.append(
                InlineKeyboardButton(
                    text=name,
                    callback_data=f"astrology:month:{month}",
                )
            )

        buttons.append(row)

    buttons.append(
        [
            InlineKeyboardButton(
                text="🏠 منوی اصلی",
                callback_data="menu",
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


def astrology_fortune_keyboard(month: int):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔮 دریافت فال MYSTRA",
                    callback_data=f"astrology:fortune:{month}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌙 بازگشت به ماه‌شناسی",
                    callback_data=f"astrology:month:{month}",
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