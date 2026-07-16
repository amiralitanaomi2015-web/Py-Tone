# -*- coding: utf-8 -*-
"""
اجرای امن (تا حد امکان) کد پایتون کاربر در محیط پلی‌گراند.

توجه مهم برای ادمین/توسعه‌دهنده:
اجرای کد دلخواه‌ی کاربر همیشه ریسک امنیتی دارد. این پیاده‌سازی یک نسخه‌ی
آموزشی و اولیه است (زیرپردازش + timeout + بدون دسترسی به شبکه‌ی محلی).
برای محیط Production واقعی حتما از sandbox قوی‌تر مثل:
  - اجرای هر درخواست داخل یک کانتینر Docker موقت و یک‌بارمصرف
  - یا سرویس‌های آماده مثل Judge0 / Piston
استفاده کنید. این تابع را می‌توانید بعدا با فراخوانی چنین سرویسی جایگزین کنید.
"""

import subprocess
import sys
import tempfile
import os

TIMEOUT_SECONDS = 5
MAX_OUTPUT_CHARS = 4000

# دستورات/ماژول‌هایی که در محیط آموزشی اجازه‌ی استفاده ندارند
BLOCKED_KEYWORDS = [
    "import os", "import sys", "import subprocess", "import socket",
    "open(", "__import__", "eval(", "exec(", "compile(",
    "import shutil", "import requests", "import urllib",
]


def run_user_code(code: str):
    """کد پایتون کاربر را اجرا می‌کند و خروجی/خطا را برمی‌گرداند."""
    lowered = code.lower()
    for kw in BLOCKED_KEYWORDS:
        if kw in lowered:
            return {
                "ok": False,
                "output": "",
                "error": f"استفاده از «{kw}» در محیط پلی‌گراند آموزشی مجاز نیست "
                          f"(به دلایل امنیتی). لطفا فقط از دستورات پایه‌ی پایتون استفاده کنید.",
            }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(code)
        tmp_path = f.name

    try:
        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
        output = (result.stdout or "") + (result.stderr or "")
        output = output[:MAX_OUTPUT_CHARS]
        return {"ok": result.returncode == 0, "output": output, "error": "" if result.returncode == 0 else "کد با خطا متوقف شد."}
    except subprocess.TimeoutExpired:
        return {"ok": False, "output": "", "error": "اجرای کد بیش از حد مجاز طول کشید (بیشتر از ۵ ثانیه)."}
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
