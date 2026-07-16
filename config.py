# -*- coding: utf-8 -*-
"""
تنظیمات اصلی پلتفرم Py Tone
شامل تعریف پلن‌ها، محدودیت‌ها و متغیرهای پیکربندی
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("PYTONE_SECRET_KEY", "dev-secret-change-in-production")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "data", "pytone.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ایمیلی که درخواست‌های خرید پلن به آن ارسال می‌شود
    PURCHASE_NOTIFY_EMAIL = os.environ.get("PYTONE_NOTIFY_EMAIL", "luolaf.stoudio@gmail.com")

    # تنظیمات SMTP برای ارسال ایمیل (باید توسط ادمین با مقادیر واقعی پر شود)
    SMTP_HOST = os.environ.get("PYTONE_SMTP_HOST", "")
    SMTP_PORT = int(os.environ.get("PYTONE_SMTP_PORT", "587"))
    SMTP_USER = os.environ.get("PYTONE_SMTP_USER", "")
    SMTP_PASS = os.environ.get("PYTONE_SMTP_PASS", "")

    # کلید API برای هوش مصنوعی (Anthropic) - باید توسط ادمین ست شود
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

    # سقف زمانی روزانه‌ی استفاده‌ی رایگان (به ثانیه) - نیم ساعت
    FREE_DAILY_LIMIT_SECONDS = 30 * 60

    LANGUAGES = [
        ("fa", "فارسی"), ("en", "English"), ("ar", "العربية"), ("tr", "Türkçe"),
        ("fr", "Français"), ("de", "Deutsch"), ("es", "Español"), ("ru", "Русский"),
        ("zh", "中文"), ("hi", "हिन्दी"), ("ur", "اردو"), ("ja", "日本語"),
        ("ko", "한국어"), ("it", "Italiano"), ("pt", "Português"), ("nl", "Nederlands"),
        ("sv", "Svenska"), ("pl", "Polski"), ("id", "Bahasa Indonesia"), ("vi", "Tiếng Việt"),
        ("th", "ไทย"), ("he", "עברית"), ("el", "Ελληνικά"), ("cs", "Čeština"),
        ("ro", "Română"), ("hu", "Magyar"), ("uk", "Українська"), ("az", "Azərbaycan"),
        ("ku", "Kurdî"), ("ps", "پښتو"), ("ms", "Melayu"), ("bn", "বাংলা"),
        ("fi", "Suomi"), ("da", "Dansk"), ("no", "Norsk"), ("sr", "Српски"),
        ("sk", "Slovenčina"), ("bg", "Български"), ("hr", "Hrvatski"), ("fil", "Filipino"),
    ]  # 40 زبان - ترجمه‌ی رابط کاربری برای fa/en کامل، بقیه از طریق ai_translate قابل توسعه است

    # پلن‌های رایگان
    FREE_PLANS = {
        "Rax": {
            "label": "Rax",
            "daily_minutes": 30,
            "features": ["articles_limited", "quiz_limited"],
            "desc": "پلن ورودی؛ فقط مطالعه‌ی مقاله‌های پایه و کوییزهای محدود",
        },
        "SQH": {
            "label": "SQH",
            "daily_minutes": 30,
            "features": ["articles_limited", "quiz_limited", "notes_view"],
            "desc": "دسترسی به مشاهده‌ی جزوه‌ها در کنار مقاله و کوییز محدود",
        },
        "Free": {
            "label": "Free",
            "daily_minutes": 30,
            "features": ["articles_limited", "quiz_limited", "notes_view", "playground_limited"],
            "desc": "امکان اجرای محدود کد در محیط پلی‌گراند",
        },
        "Slow": {
            "label": "Slow",
            "daily_minutes": 30,
            "features": ["articles_full", "quiz_limited", "notes_view", "playground_limited"],
            "desc": "دسترسی کامل به مقاله‌ها با سرعت پاسخ‌گویی هوش مصنوعی کندتر",
        },
        "Quiet": {
            "label": "Quiet",
            "daily_minutes": 30,
            "features": ["articles_full", "quiz_full", "notes_view", "playground_limited", "method_finder"],
            "desc": "دسترسی به ابزار جست‌وجوی متد پایتون",
        },
        "Bass": {
            "label": "Bass",
            "daily_minutes": 30,
            "features": ["articles_full", "quiz_full", "notes_view", "notes_download",
                         "playground_limited", "method_finder", "ai_tutor_limited"],
            "desc": "بهترین پلن رایگان؛ دسترسی محدود به تدریس‌خصوصی هوش مصنوعی",
        },
    }

    # پلن‌های غیررایگان (پولی)
    PAID_PLANS = {
        "Pro": {
            "label": "Pro", "tier": 1, "daily_minutes": 90,
            "features": ["articles_full", "quiz_full", "notes_full", "playground_full",
                         "method_finder", "ai_tutor_limited"],
        },
        "Plus": {
            "label": "Plus", "tier": 2, "daily_minutes": 120,
            "features": ["articles_full", "quiz_full", "notes_full", "playground_full",
                         "method_finder", "ai_tutor_limited", "exam_mode"],
        },
        "Supper": {
            "label": "Supper", "tier": 3, "daily_minutes": 180,
            "features": ["articles_full", "quiz_full", "notes_full", "playground_full",
                         "method_finder", "ai_tutor_full", "exam_mode", "priority_support"],
        },
        "VIP": {
            "label": "VIP", "tier": 4, "daily_minutes": 240,
            "features": ["articles_full", "quiz_full", "notes_full", "playground_full",
                         "method_finder", "ai_tutor_full", "exam_mode", "priority_support",
                         "certificates"],
        },
        "Max": {
            "label": "Max", "tier": 5, "daily_minutes": 360,
            "features": ["articles_full", "quiz_full", "notes_full", "playground_full",
                         "method_finder", "ai_tutor_full", "exam_mode", "priority_support",
                         "certificates", "custom_learning_path"],
        },
        "Fast": {
            "label": "Fast", "tier": 6, "daily_minutes": 480,
            "features": ["articles_full", "quiz_full", "notes_full", "playground_full",
                         "method_finder", "ai_tutor_full", "exam_mode", "priority_support",
                         "certificates", "custom_learning_path", "fast_ai_response"],
        },
        "Loud": {
            "label": "Loud", "tier": 7, "daily_minutes": 600,
            "features": ["articles_full", "quiz_full", "notes_full", "playground_full",
                         "method_finder", "ai_tutor_full", "exam_mode", "priority_support",
                         "certificates", "custom_learning_path", "fast_ai_response",
                         "voice_ai_tutor"],
        },
        "Cup": {
            "label": "Cup", "tier": 8, "daily_minutes": 900,
            "features": ["articles_full", "quiz_full", "notes_full", "playground_full",
                         "method_finder", "ai_tutor_full", "exam_mode", "priority_support",
                         "certificates", "custom_learning_path", "fast_ai_response",
                         "voice_ai_tutor", "one_on_one_session"],
        },
        "Golden": {
            "label": "Golden", "tier": 9, "daily_minutes": None,  # نامحدود
            "features": ["articles_full", "quiz_full", "notes_full", "playground_full",
                         "method_finder", "ai_tutor_full", "exam_mode", "priority_support",
                         "certificates", "custom_learning_path", "fast_ai_response",
                         "voice_ai_tutor", "one_on_one_session", "unlimited_everything"],
        },
    }

    FEATURE_LABELS = {
        "articles_limited": "مقاله‌های پایه",
        "articles_full": "همه‌ی مقاله‌ها",
        "quiz_limited": "کوییز محدود",
        "quiz_full": "کوییز نامحدود",
        "notes_view": "مشاهده‌ی جزوه",
        "notes_download": "دانلود جزوه",
        "notes_full": "جزوه‌ی کامل + دانلود",
        "playground_limited": "پلی‌گراند محدود (روزی چند اجرا)",
        "playground_full": "پلی‌گراند نامحدود",
        "method_finder": "جست‌وجوی متد پایتون",
        "ai_tutor_limited": "معلم هوش مصنوعی (محدود)",
        "ai_tutor_full": "معلم هوش مصنوعی (نامحدود)",
        "exam_mode": "حالت آزمون شبیه‌سازی‌شده",
        "priority_support": "پشتیبانی اولویت‌دار",
        "certificates": "گواهی پایان دوره",
        "custom_learning_path": "مسیر یادگیری شخصی‌سازی‌شده",
        "fast_ai_response": "پاسخ سریع‌تر هوش مصنوعی",
        "voice_ai_tutor": "تدریس صوتی هوش مصنوعی",
        "one_on_one_session": "جلسه‌ی خصوصی با تیم",
        "unlimited_everything": "دسترسی کامل و نامحدود به همه‌چیز",
    }
