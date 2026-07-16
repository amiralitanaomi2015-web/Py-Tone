# -*- coding: utf-8 -*-
"""
Py Tone - پلتفرم آموزش صفر تا صد پایتون با هوش مصنوعی
برنامه‌ی اصلی (کاربر عادی). این فایل به‌طور کامل مستقل است و هیچ درِ پشتی
یا مکانیزم مخفی برای دور زدن سیستم پلن‌ها ندارد. مدیریت پلن‌ها و دسترسی‌ها
باید از طریق برنامه‌ی مدیریت جداگانه (که در فاز بعدی می‌سازیم) انجام شود.
"""

import time
from datetime import date, datetime
from functools import wraps

from flask import (Flask, render_template, request, redirect, url_for,
                    session, flash, jsonify, abort)

from config import Config
from models import (db, User, UsageLog, Article, Quiz, Question, QuizAttempt,
                     Note, ChatMessage, PurchaseRequest, Announcement, PlatformStatus)
from method_finder import search_methods
from playground_runner import run_user_code
from ai_tutor import ask_ai_tutor
from mailer import send_purchase_notification
import seed_data

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


@app.template_filter("markdown")
def markdown_filter(text):
    import markdown as md
    return md.markdown(text or "", extensions=["fenced_code"])

with app.app_context():
    db.create_all()
    seed_data.seed_if_empty()
    if PlatformStatus.query.first() is None:
        db.session.add(PlatformStatus(is_online=True))
        db.session.commit()


# ---------------------------------------------------------------------------
# ابزارهای کمکی
# ---------------------------------------------------------------------------

def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    return User.query.get(uid)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user():
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def feature_required(feature_key):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            u = current_user()
            if not u.has_feature(feature_key):
                flash("این قابلیت در پلن فعلی شما موجود نیست. لطفا پلن خود را ارتقا دهید.", "warning")
                return redirect(url_for("plans"))
            return view(*args, **kwargs)
        return wrapped
    return decorator


@app.before_request
def platform_gate_and_timer():
    # وضعیت کلی پلتفرم (فعال/غیرفعال) که برنامه‌ی مدیریت از راه دور کنترل می‌کند
    status = PlatformStatus.query.first()
    allowed_paths = {"/offline"}
    if status and not status.is_online and request.path not in allowed_paths \
            and not request.path.startswith("/static"):
        return redirect(url_for("offline"))

    u = current_user()
    if u:
        if u.is_blocked:
            session.clear()
            flash("حساب کاربری شما مسدود شده است. برای اطلاعات بیشتر با پشتیبانی تماس بگیرید.", "danger")
            return redirect(url_for("login"))

        # اجرای شمارنده‌ی زمان استفاده‌ی روزانه برای پلن‌های رایگان
        limit = u.daily_limit_seconds()
        if limit is not None:
            remaining = u.remaining_seconds_today()
            if remaining <= 0 and request.endpoint not in (
                    "plans", "purchase", "logout", "static", "offline", "usage_ping"):
                return redirect(url_for("time_up"))


@app.route("/api/usage-ping", methods=["POST"])
@login_required
def usage_ping():
    """هر چند ثانیه یک‌بار از سمت کلاینت صدا زده می‌شود تا زمان استفاده ثبت شود."""
    u = current_user()
    today = date.today()
    log = UsageLog.query.filter_by(user_id=u.id, day=today).first()
    if not log:
        log = UsageLog(user_id=u.id, day=today, seconds_used=0)
        db.session.add(log)
    seconds = int(request.json.get("seconds", 5)) if request.is_json else 5
    log.seconds_used += max(1, min(seconds, 30))
    db.session.commit()
    remaining = u.remaining_seconds_today()
    return jsonify({"remaining": remaining})


# ---------------------------------------------------------------------------
# صفحات عمومی
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    if current_user():
        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/offline")
def offline():
    status = PlatformStatus.query.first()
    return render_template("offline.html", message=status.offline_message if status else "")


@app.route("/time-up")
@login_required
def time_up():
    return render_template("time_up.html")


# ---------------------------------------------------------------------------
# احراز هویت
# ---------------------------------------------------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not first_name or not email or not password:
            flash("لطفا همه‌ی فیلدهای ضروری را پر کنید.", "danger")
            return render_template("register.html")

        if User.query.filter_by(email=email).first():
            flash("این ایمیل قبلا ثبت‌نام کرده است.", "danger")
            return render_template("register.html")

        user = User(first_name=first_name, last_name=last_name, email=email, plan="Free")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        flash("خوش آمدید! ثبت‌نام شما با موفقیت انجام شد.", "success")
        return redirect(url_for("dashboard"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("ایمیل یا رمز عبور نادرست است.", "danger")
            return render_template("login.html")

        if user.is_blocked:
            flash("حساب کاربری شما مسدود شده است.", "danger")
            return render_template("login.html")

        session["user_id"] = user.id
        return redirect(request.args.get("next") or url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ---------------------------------------------------------------------------
# داشبورد
# ---------------------------------------------------------------------------

@app.route("/dashboard")
@login_required
def dashboard():
    u = current_user()
    articles = Article.query.order_by(Article.order_index).all()
    quizzes = Quiz.query.all()
    recent_notes = Note.query.filter_by(user_id=u.id).order_by(Note.created_at.desc()).limit(5).all()
    attempts = QuizAttempt.query.filter_by(user_id=u.id).order_by(QuizAttempt.taken_at.desc()).limit(5).all()
    announcements = Announcement.query.filter(
        (Announcement.user_id == u.id) | (Announcement.user_id.is_(None))
    ).order_by(Announcement.created_at.desc()).limit(5).all()

    return render_template(
        "dashboard.html", user=u, articles=articles, quizzes=quizzes,
        recent_notes=recent_notes, attempts=attempts, announcements=announcements,
        remaining=u.remaining_seconds_today(),
    )


# ---------------------------------------------------------------------------
# مقاله‌ها
# ---------------------------------------------------------------------------

@app.route("/learn")
@login_required
def learn():
    u = current_user()
    articles = Article.query.order_by(Article.order_index).all()
    return render_template("learn.html", articles=articles, user=u)


@app.route("/learn/<slug>")
@login_required
def article_detail(slug):
    u = current_user()
    article = Article.query.filter_by(slug=slug).first_or_404()

    if not article.is_free and not u.has_feature("articles_full"):
        flash("این مقاله فقط برای پلن‌های بالاتر در دسترس است.", "warning")
        return redirect(url_for("plans"))

    return render_template("article_detail.html", article=article, user=u)


# ---------------------------------------------------------------------------
# کوییزها
# ---------------------------------------------------------------------------

@app.route("/quizzes")
@login_required
def quizzes():
    u = current_user()
    all_quizzes = Quiz.query.all()
    return render_template("quizzes.html", quizzes=all_quizzes, user=u)


@app.route("/quizzes/<int:quiz_id>", methods=["GET", "POST"])
@login_required
def quiz_take(quiz_id):
    u = current_user()
    quiz = Quiz.query.get_or_404(quiz_id)

    if not quiz.is_free and not u.has_feature("quiz_full"):
        flash("این کوییز فقط برای پلن‌های بالاتر در دسترس است.", "warning")
        return redirect(url_for("plans"))

    if request.method == "POST":
        score = 0
        results = []
        for q in quiz.questions:
            chosen = request.form.get(f"q{q.id}")
            correct = (chosen == q.correct_option)
            if correct:
                score += 1
            results.append({"question": q, "chosen": chosen, "correct": correct})

        attempt = QuizAttempt(user_id=u.id, quiz_id=quiz.id, score=score, total=len(quiz.questions))
        db.session.add(attempt)
        db.session.commit()

        return render_template("quiz_result.html", quiz=quiz, results=results, score=score, total=len(quiz.questions))

    return render_template("quiz_take.html", quiz=quiz, user=u)


# ---------------------------------------------------------------------------
# جزوه‌ها (Notes)
# ---------------------------------------------------------------------------

@app.route("/notes", methods=["GET", "POST"])
@login_required
def notes():
    u = current_user()
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        topic = request.form.get("topic", "").strip()
        if title:
            db.session.add(Note(user_id=u.id, title=title, content=content, topic=topic))
            db.session.commit()
            flash("جزوه ذخیره شد.", "success")
        return redirect(url_for("notes"))

    all_notes = Note.query.filter_by(user_id=u.id).order_by(Note.created_at.desc()).all()
    return render_template("notes.html", notes=all_notes, user=u)


@app.route("/notes/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(note_id):
    u = current_user()
    note = Note.query.filter_by(id=note_id, user_id=u.id).first_or_404()
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("notes"))


# ---------------------------------------------------------------------------
# محیط اجرای کد (Playground)
# ---------------------------------------------------------------------------

@app.route("/playground")
@login_required
def playground():
    return render_template("playground.html", user=current_user())


@app.route("/api/playground/run", methods=["POST"])
@login_required
def playground_run():
    code = request.json.get("code", "") if request.is_json else request.form.get("code", "")
    if len(code) > 5000:
        return jsonify({"ok": False, "error": "کد بیش از حد طولانی است.", "output": ""})
    result = run_user_code(code)
    return jsonify(result)


# ---------------------------------------------------------------------------
# جست‌وجوی متد پایتون (نصفه‌نویسی هوشمند)
# ---------------------------------------------------------------------------

@app.route("/methods")
@login_required
@feature_required("method_finder")
def methods_page():
    return render_template("methods.html", user=current_user())


@app.route("/api/methods/search")
@login_required
def methods_search_api():
    q = request.args.get("q", "")
    results = search_methods(q)
    return jsonify({"results": results})


# ---------------------------------------------------------------------------
# معلم هوش مصنوعی
# ---------------------------------------------------------------------------

@app.route("/ai-tutor")
@login_required
def ai_tutor_page():
    u = current_user()
    history = ChatMessage.query.filter_by(user_id=u.id).order_by(ChatMessage.created_at).all()
    return render_template("ai_tutor.html", user=u, history=history)


@app.route("/api/ai-tutor/send", methods=["POST"])
@login_required
def ai_tutor_send():
    u = current_user()
    if not (u.has_feature("ai_tutor_limited") or u.has_feature("ai_tutor_full")):
        return jsonify({"error": "این قابلیت در پلن فعلی شما فعال نیست."}), 403

    message = request.json.get("message", "").strip()
    if not message:
        return jsonify({"error": "پیام خالی است."}), 400

    history = ChatMessage.query.filter_by(user_id=u.id).order_by(ChatMessage.created_at).all()
    history_payload = [{"role": h.role, "content": h.content} for h in history]

    db.session.add(ChatMessage(user_id=u.id, role="user", content=message))
    db.session.commit()

    reply = ask_ai_tutor(message, language=u.preferred_language, history=history_payload)

    db.session.add(ChatMessage(user_id=u.id, role="assistant", content=reply))
    db.session.commit()

    return jsonify({"reply": reply})


# ---------------------------------------------------------------------------
# پلن‌ها و خرید
# ---------------------------------------------------------------------------

@app.route("/plans")
@login_required
def plans():
    u = current_user()
    return render_template("plans.html", user=u, free_plans=Config.FREE_PLANS,
                            paid_plans=Config.PAID_PLANS, feature_labels=Config.FEATURE_LABELS)


@app.route("/purchase/<plan_name>", methods=["GET", "POST"])
@login_required
def purchase(plan_name):
    u = current_user()
    if plan_name not in Config.PAID_PLANS:
        abort(404)

    if request.method == "POST":
        pr = PurchaseRequest(
            user_id=u.id,
            plan_requested=plan_name,
            full_name=request.form.get("full_name", "").strip(),
            last_name=request.form.get("last_name", "").strip(),
            email=request.form.get("email", "").strip(),
            phone=request.form.get("phone", "").strip(),
            country=request.form.get("country", "").strip(),
            address=request.form.get("address", "").strip(),
            status="pending",
        )
        db.session.add(pr)
        db.session.commit()

        send_purchase_notification(pr)

        return render_template("purchase_success.html", plan_name=plan_name)

    return render_template("purchase.html", plan_name=plan_name, plan_info=Config.PAID_PLANS[plan_name])


# ---------------------------------------------------------------------------
# پروفایل
# ---------------------------------------------------------------------------

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    u = current_user()
    if request.method == "POST":
        u.preferred_language = request.form.get("preferred_language", u.preferred_language)
        db.session.commit()
        flash("تنظیمات ذخیره شد.", "success")
        return redirect(url_for("profile"))
    return render_template("profile.html", user=u, languages=Config.LANGUAGES)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
