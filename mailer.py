# -*- coding: utf-8 -*-
"""ارسال ایمیل اطلاع‌رسانی خرید پلن به تیم لیولاف"""

import smtplib
from email.mime.text import MIMEText
from flask import current_app


def send_purchase_notification(purchase):
    cfg = current_app.config
    host, port = cfg.get("SMTP_HOST"), cfg.get("SMTP_PORT")
    user, pwd = cfg.get("SMTP_USER"), cfg.get("SMTP_PASS")
    to_addr = cfg.get("PURCHASE_NOTIFY_EMAIL")

    body = (
        f"درخواست خرید پلن جدید در Py Tone\n\n"
        f"پلن درخواستی: {purchase.plan_requested}\n"
        f"نام: {purchase.full_name}\n"
        f"نام خانوادگی: {purchase.last_name}\n"
        f"ایمیل: {purchase.email}\n"
        f"موبایل: {purchase.phone}\n"
        f"کشور: {purchase.country}\n"
        f"آدرس: {purchase.address}\n"
        f"شناسه‌ی کاربر: {purchase.user_id}\n"
    )

    if not host or not user or not pwd:
        # SMTP پیکربندی نشده؛ فقط لاگ می‌کنیم تا در توسعه/دمو کرش نکند
        print("--- [شبیه‌سازی ارسال ایمیل - SMTP تنظیم نشده] ---")
        print(f"به: {to_addr}\n{body}")
        print("--------------------------------------------------")
        return False

    msg = MIMEText(body, _charset="utf-8")
    msg["Subject"] = f"درخواست خرید پلن {purchase.plan_requested} - Py Tone"
    msg["From"] = user
    msg["To"] = to_addr

    try:
        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(user, pwd)
            server.sendmail(user, [to_addr], msg.as_string())
        return True
    except Exception as e:
        print(f"خطا در ارسال ایمیل: {e}")
        return False
