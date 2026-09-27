DIMENSION_INFO = {
    "social": {
        "name": "تعامل اجتماعی",
        "emoji": "👥",
        "high": "در ارتباط گرفتن و حضور در جمع‌ها معمولاً راحت‌تر عمل می‌کنی.",
        "low": "معمولاً ارتباط‌های محدودتر و انتخابی‌تر برایت راحت‌ترند.",
    },

    "initiative": {
        "name": "پیش‌قدمی",
        "emoji": "⚡",
        "high": "وقتی کاری نیاز به شروع داشته باشد، معمولاً منتظر دیگران نمی‌مانی.",
        "low": "اغلب ترجیح می‌دهی قبل از اقدام، شرایط را بهتر بسنجی.",
    },

    "observation": {
        "name": "مشاهده و دقت",
        "emoji": "🔍",
        "high": "قبل از تصمیم گرفتن معمولاً جزئیات و شرایط را خوب بررسی می‌کنی.",
        "low": "بیشتر تمایل داری مستقیم وارد عمل شوی تا اینکه مدت زیادی بررسی کنی.",
    },

    "independence": {
        "name": "استقلال",
        "emoji": "🧭",
        "high": "در تصمیم‌ها و مسیرت تا حد زیادی روی خودت حساب می‌کنی.",
        "low": "گرفتن نظر و همراهی دیگران می‌تواند برایت اهمیت بیشتری داشته باشد.",
    },

    "logic": {
        "name": "منطق",
        "emoji": "🧠",
        "high": "در تصمیم‌گیری معمولاً دنبال دلیل، نتیجه و شواهد می‌گردی.",
        "low": "فقط نتیجه منطقی برایت تعیین‌کننده نیست و عوامل دیگری هم مهم‌اند.",
    },

    "emotion": {
        "name": "احساس",
        "emoji": "💭",
        "high": "احساسات خودت و دیگران می‌توانند در تصمیم‌هایت نقش مهمی داشته باشند.",
        "low": "معمولاً ترجیح می‌دهی احساسات نقش کمتری در تصمیم‌گیری داشته باشند.",
    },

    "intuition": {
        "name": "شهود",
        "emoji": "✨",
        "high": "گاهی بدون داشتن تمام اطلاعات، به حس درونیت اعتماد می‌کنی.",
        "low": "معمولاً ترجیح می‌دهی قبل از اعتماد کردن، اطلاعات بیشتری داشته باشی.",
    },

    "structure": {
        "name": "ساختار",
        "emoji": "📐",
        "high": "نظم، برنامه و داشتن مسیر مشخص می‌تواند عملکردت را بهتر کند.",
        "low": "ساختار سخت‌گیرانه احتمالاً جذابیت کمتری برایت دارد.",
    },

    "flexibility": {
        "name": "انعطاف‌پذیری",
        "emoji": "🌊",
        "high": "وقتی شرایط تغییر می‌کند، معمولاً می‌توانی خودت را با وضعیت جدید هماهنگ کنی.",
        "low": "تغییر ناگهانی برنامه‌ها ممکن است برایت آزاردهنده‌تر باشد.",
    },

    "curiosity": {
        "name": "کنجکاوی",
        "emoji": "🔮",
        "high": "موضوعات جدید می‌توانند خیلی سریع توجهت را جلب کنند.",
        "low": "معمولاً ترجیح می‌دهی روی چیزهای آشناتر و کاربردی‌تر تمرکز کنی.",
    },

    "caution": {
        "name": "احتیاط",
        "emoji": "🛡️",
        "high": "قبل از وارد شدن به موقعیت‌های ناشناخته معمولاً جوانب مختلف را می‌سنجی.",
        "low": "در شرایط جدید احتمال بیشتری دارد که سریع‌تر وارد تجربه شوی.",
    },

    "risk": {
        "name": "ریسک‌پذیری",
        "emoji": "🎯",
        "high": "اگر فرصت ارزشمندی ببینی، احتمالاً از تجربه کردنش نمی‌ترسی.",
        "low": "معمولاً ترجیح می‌دهی قبل از ریسک، نتیجه احتمالی را بررسی کنی.",
    },
}


PROFILE_TITLES = {
    "social": "کاوشگر اجتماعی",
    "initiative": "شروع‌کننده",
    "observation": "ناظر دقیق",
    "independence": "مستقل",
    "logic": "تحلیل‌گر",
    "emotion": "همدل",
    "intuition": "شهودی",
    "structure": "سازمان‌دهنده",
    "flexibility": "سازگار",
    "curiosity": "کاوشگر",
    "caution": "سنجیده",
    "risk": "ماجراجو",
}


def get_dimension_description(dimension: str, raw_score: int) -> str:
    info = DIMENSION_INFO.get(dimension)

    if not info:
        return ""

    if raw_score >= 2:
        return info["high"]

    return info["low"]


def score_bar(score: int, minimum: int = -5, maximum: int = 10) -> str:
    """
    ساخت نوار ساده برای نمایش شدت ویژگی.
    """

    if score < minimum:
        score = minimum

    if score > maximum:
        score = maximum

    total_blocks = 10

    ratio = (score - minimum) / (maximum - minimum)

    filled = round(ratio * total_blocks)

    return "█" * filled + "░" * (total_blocks - filled)


def generate_result(result: dict) -> str:
    scores = result.get("scores", {})
    profile = result.get("profile", {})

    strongest = profile.get("strongest", [])

    if strongest:
        main_dimension = strongest[0][0]
        title = PROFILE_TITLES.get(
            main_dimension,
            "پروفایل منحصربه‌فرد",
        )
    else:
        title = "پروفایل متعادل"

    lines = [
        "🔮 <b>MYSTRA</b>",
        "",
        f"🧩 <b>{title}</b>",
        "",
        "پاسخ‌هات یک الگوی شخصیتی خاص رو نشون می‌دن.",
        "",
        "━━━━━━━━━━━━━━",
        "",
        "🔍 <b>ویژگی‌های برجسته</b>",
        "",
    ]

    for dimension, raw_score in strongest[:4]:
        info = DIMENSION_INFO.get(dimension)

        if not info:
            continue

        name = info["name"]
        emoji = info["emoji"]

        lines.append(
            f"{emoji} <b>{name}</b>  {score_bar(raw_score)}  {raw_score:+d}"
        )

    lines.extend([
        "",
        "━━━━━━━━━━━━━━",
        "",
        "🧠 <b>برداشت MYSTRA</b>",
        "",
    ])

    added = 0

    for dimension, raw_score in strongest:
        if added >= 3:
            break

        description = get_dimension_description(
            dimension,
            raw_score,
        )

        if not description:
            continue

        lines.append(f"• {description}")

        added += 1

    lines.extend([
        "",
        "━━━━━━━━━━━━━━",
        "",
        f"📊 پاسخ داده‌شده: "
        f"{result.get('answered', 0)} از "
        f"{result.get('total', 0)}",
        "",
        "این پروفایل بر اساس پاسخ‌های همین تست ساخته شده و "
        "تشخیص علمی یا روان‌شناختی محسوب نمی‌شود.",
    ])

    return "\n".join(lines)