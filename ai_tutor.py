# -*- coding: utf-8 -*-
"""
اتصال به هوش مصنوعی برای معلم/ایجنت آموزشی Py Tone.

اگر متغیر محیطی ANTHROPIC_API_KEY تنظیم شده باشد، از API واقعی Anthropic
استفاده می‌شود. در غیر این صورت یک پاسخ آموزشی محلی (fallback) بازگردانده
می‌شود تا در حالت توسعه هم بتوان رابط کاربری را تست کرد.
"""

import os
import json

SYSTEM_PROMPT = (
    "تو 'استاد پای‌تون' هستی، یک معلم هوش مصنوعی متخصص آموزش برنامه‌نویسی پایتون "
    "در پلتفرم Py Tone. با لحنی دوستانه، ساده و تشویق‌کننده تدریس کن. "
    "مثال کد بزن، مفاهیم را قدم‌به‌قدم توضیح بده، و در پایان یک تمرین کوچک پیشنهاد بده. "
    "پاسخ را به زبان درخواستی کاربر بده."
)

FALLBACK_RESPONSES = [
    "برای فعال‌سازی معلم هوش مصنوعی، ادمین باید متغیر محیطی ANTHROPIC_API_KEY را "
    "روی سرور تنظیم کند. فعلا این یک پاسخ نمونه است: بیا با هم متغیرها در پایتون رو یاد بگیریم! "
    "مثال: x = 10  →  این یعنی متغیر x مقدار 10 گرفته. حالا تو امتحان کن: متغیری به اسم name بساز "
    "و اسم خودت رو داخلش بریز.",
]


def ask_ai_tutor(user_message: str, language: str = "fa", history=None):
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return FALLBACK_RESPONSES[0]

    try:
        import urllib.request

        messages = []
        for turn in (history or [])[-10:]:
            messages.append({"role": turn["role"], "content": turn["content"]})
        messages.append({"role": "user", "content": user_message})

        payload = {
            "model": "claude-sonnet-4-6",
            "max_tokens": 800,
            "system": SYSTEM_PROMPT + f" (زبان پاسخ: {language})",
            "messages": messages,
        }

        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            parts = [block.get("text", "") for block in data.get("content", []) if block.get("type") == "text"]
            return "\n".join(parts) if parts else FALLBACK_RESPONSES[0]
    except Exception as e:
        return f"در ارتباط با هوش مصنوعی خطایی رخ داد: {e}"
