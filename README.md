<<<<<<< HEAD
# Py Tone — Main Application

A Python learning platform from scratch with AI. This is just the “main application” (user side);
The “remote management application” will be built in the next phase and the two will be connected to the database.

## Run
=======
# Py Tone — برنامه‌ی اصلی

پلتفرم آموزش پایتون از صفر تا صد با هوش مصنوعی. این فقط «برنامه‌ی اصلی» (سمت کاربر) است؛
«برنامه‌ی مدیریت از راه دور» در فاز بعدی ساخته می‌شود و این دو با پایگاه‌داده به هم متصل خواهند شد.

## اجرا
>>>>>>> 7f8cd5a (Adding better files to the platform)

```bash
cd pytone
python3 -m venv venv
<<<<<<< HEAD
source venv/bin/activate # Windows: venv\Scripts\activate
=======
source venv/bin/activate        # ویندوز: venv\Scripts\activate
>>>>>>> 7f8cd5a (Adding better files to the platform)
pip install -r requirements.txt
python3 app.py
```

<<<<<<< HEAD
Then open the following address in the browser:
=======
سپس آدرس زیر را در مرورگر باز کنید:
>>>>>>> 7f8cd5a (Adding better files to the platform)
```
http://127.0.0.1:5000
```

<<<<<<< HEAD
## Important settings (environment variables)

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | For the actual activation of the AI ​​tutor. Without it, the sample response (fallback) will be displayed. |
| `PYTONE_SMTP_HOST` / `PYTONE_SMTP_PORT` | SMTP server address and port for sending purchase request emails |
| `PYTONE_SMTP_USER` / `PYTONE_SMTP_PASS` | Sender email login information |
| `PYTONE_NOTIFY_EMAIL` | Email to which plan purchase requests will be sent (default: luolaf.stoudio@gmail.com) |
| `PYTONE_SECRET_KEY` | Flask security key (be sure to change for Production) |

If SMTP is not set, the program will not crash; it will just print the email text to the terminal so that it can be tested in development mode.

## File structure

```
pytone/
├── app.py # All routes and main logic
├── config.py # Define plans (6 free + 9 paid) and settings
├── models.py # Database models (SQLAlchemy)
├── method_finder.py # Python method semi-script search tool
├── playground_runner.py # Secure execution of user code
├── ai_tutor.py # Connect to Claude API for AI tutor
├── mailer.py # Send purchase request email
├── seed_data.py # Raw data (article + sample quiz)
├── templates/ # HTML pages
├── static/css/style.css # Design and color scheme
└── data/pytone.db # SQLite database (automatically created)
```

## Important security tips and limitations of this version

1. **Playground code execution**: User code with subprocess and timeout is executed and sensitive imports (`os`, `subprocess`, `socket`, ...) are blocked. This is a basic training sandbox; for real production it is recommended to use a more robust isolation service like Docker disposable or
Piston/Judge0.
2. **No backdoor**: As initially requested, the "secret code to open any account" mechanism is **not** implemented in this
program, as it is considered a serious security vulnerability. Management of plans and
user access should be done through the official admin panel (next phase) and with proper authentication.
3. **40 languages**: Multilingual structure (`config.py -> LANGUAGES`) is ready for 40 languages ​​and the user
can choose his preferred language in the profile; the AI ​​tutor responds in the same language. The full translation of the user interface (fixed site texts) is currently only Persian, and translation files need to be added for other
languages.
4. **Database**: Currently, SQLite (file `data/pytone.db`) is used, which is great for development and testing
; for thousands of simultaneous users, it is better to migrate to PostgreSQL.

## Next step

Py Tone remote management program (Livelove admin panel): blocking users, manually approving
purchases, sending notifications, turning the entire platform on/off, support chat, etc. — which will be created in a separate file and
with a shared database.
=======
## تنظیمات مهم (متغیرهای محیطی)

| متغیر | توضیح |
|---|---|
| `ANTHROPIC_API_KEY` | برای فعال شدن واقعی معلم هوش مصنوعی. بدون آن، پاسخ نمونه (fallback) نمایش داده می‌شود. |
| `PYTONE_SMTP_HOST` / `PYTONE_SMTP_PORT` | آدرس و پورت سرور SMTP برای ارسال ایمیل درخواست خرید |
| `PYTONE_SMTP_USER` / `PYTONE_SMTP_PASS` | اطلاعات ورود به ایمیل ارسال‌کننده |
| `PYTONE_NOTIFY_EMAIL` | ایمیلی که درخواست‌های خرید پلن به آن ارسال می‌شود (پیش‌فرض: luolaf.stoudio@gmail.com) |
| `PYTONE_SECRET_KEY` | کلید امنیتی Flask (برای Production حتما تغییر بدهید) |

اگر SMTP تنظیم نشود، برنامه کرش نمی‌کند؛ فقط متن ایمیل را در ترمینال چاپ می‌کند تا در حالت توسعه هم قابل تست باشد.

## ساختار فایل‌ها

```
pytone/
├── app.py              # همه‌ی route ها و منطق اصلی
├── config.py            # تعریف پلن‌ها (۶ رایگان + ۹ پولی) و تنظیمات
├── models.py             # مدل‌های پایگاه‌داده (SQLAlchemy)
├── method_finder.py      # ابزار جست‌وجوی نصفه‌نویسی متد پایتون
├── playground_runner.py  # اجرای امن‌شده‌ی کد کاربر
├── ai_tutor.py            # اتصال به Claude API برای معلم هوش مصنوعی
├── mailer.py              # ارسال ایمیل درخواست خرید
├── seed_data.py           # داده‌ی اولیه (مقاله + کوییز نمونه)
├── templates/             # صفحات HTML (شامل صفحه‌ی پشتیبانی /support)
├── static/css/style.css   # طراحی و رنگ‌بندی
└── data/pytone.db          # پایگاه‌داده‌ی SQLite (خودکار ساخته می‌شود)
```

## نکات مهم امنیتی و محدودیت‌های این نسخه

1. **پلی‌گراند اجرای کد**: کد کاربر با subprocess و timeout اجرا می‌شود و import های
   حساس (`os`, `subprocess`, `socket`, ...) بلاک شده‌اند. این یک sandbox آموزشیِ اولیه است؛
   برای Production واقعی توصیه می‌شود از یک سرویس ایزوله‌ی قوی‌تر مثل Docker یک‌بارمصرف یا
   Piston/Judge0 استفاده شود.
2. **بدون درِ پشتی**: طبق درخواست اولیه، مکانیزم «کد مخفی برای باز کردن هر اکانتی» در این
   برنامه پیاده‌سازی **نشده** است، چون یک آسیب‌پذیری امنیتی جدی محسوب می‌شود. مدیریت پلن‌ها و
   دسترسی کاربران باید از طریق پنل مدیریت رسمی (فاز بعدی) و با احراز هویت درست انجام شود.
3. **۴۰ زبان**: ساختار چندزبانه (`config.py -> LANGUAGES`) برای ۴۰ زبان آماده است و کاربر
   می‌تواند زبان ترجیحی خود را در پروفایل انتخاب کند؛ معلم هوش مصنوعی به همان زبان پاسخ
   می‌دهد. ترجمه‌ی کامل رابط کاربری (متن‌های ثابت سایت) فعلاً فقط فارسی است و برای بقیه‌ی
   زبان‌ها باید فایل‌های ترجمه اضافه شود.
4. **پایگاه‌داده**: فعلاً SQLite (فایل `data/pytone.db`) استفاده شده که برای توسعه و تست
   عالی است؛ برای هزاران کاربر همزمان بهتر است به PostgreSQL مهاجرت شود.

## برنامه‌ی دوم: پنل مدیریت از راه دور

پوشه‌ی جداگانه‌ی `pytone-admin` همین کنار این پروژه ساخته شده و به همان فایل
پایگاه‌داده وصل می‌شود (`pytone/data/pytone.db`). با آن اعضای تیم لیولاف می‌توانند:
کاربران را مسدود/رفع‌مسدود کنند، خرید پلن را تایید/رد کنند، اعلان بفرستند، با
کاربران چت پشتیبانی کنند، و کل پلتفرم را روشن/خاموش کنند. راهنمای کامل در
`pytone-admin/README.md` است. **این دو پوشه باید کنار هم باشند** تا مسیر نسبی
پایگاه‌داده‌ی مشترک درست کار کند.
>>>>>>> 7f8cd5a (Adding better files to the platform)
