# Py Tone — Main Application

A Python learning platform from scratch with AI. This is just the “main application” (user side);
The “remote management application” will be built in the next phase and the two will be connected to the database.

## Run

```bash
cd pytone
python3 -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 app.py
```

Then open the following address in the browser:
```
http://127.0.0.1:5000
```

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
