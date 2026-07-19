# -*- coding: utf-8 -*-
"""مدل‌های پایگاه‌داده‌ی Py Tone"""

from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(200), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    plan = db.Column(db.String(50), default="Free")           # نام پلن فعلی
    is_paid_plan = db.Column(db.Boolean, default=False)
    plan_activated_at = db.Column(db.DateTime, nullable=True)

    preferred_language = db.Column(db.String(10), default="fa")
    is_blocked = db.Column(db.Boolean, default=False)
    block_reason = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ارتباط
    usage_logs = db.relationship("UsageLog", backref="user", lazy=True)
    notes = db.relationship("Note", backref="user", lazy=True)
    quiz_attempts = db.relationship("QuizAttempt", backref="user", lazy=True)
    purchase_requests = db.relationship("PurchaseRequest", backref="user", lazy=True)
    chat_messages = db.relationship("ChatMessage", backref="user", lazy=True)

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

    def plan_info(self):
        from config import Config
        if self.is_paid_plan:
            return Config.PAID_PLANS.get(self.plan, Config.FREE_PLANS["Free"])
        return Config.FREE_PLANS.get(self.plan, Config.FREE_PLANS["Free"])

    def has_feature(self, feature_key):
        return feature_key in self.plan_info().get("features", [])

    def today_usage_seconds(self):
        today = date.today()
        log = UsageLog.query.filter_by(user_id=self.id, day=today).first()
        return log.seconds_used if log else 0

    def daily_limit_seconds(self):
        info = self.plan_info()
        minutes = info.get("daily_minutes")
        if minutes is None:
            return None  # نامحدود
        return minutes * 60

    def remaining_seconds_today(self):
        limit = self.daily_limit_seconds()
        if limit is None:
            return None
        used = self.today_usage_seconds()
        return max(0, limit - used)


class UsageLog(db.Model):
    """مقدار زمان استفاده‌ی کاربر در هر روز، برای اعمال محدودیت پلن‌های رایگان"""
    __tablename__ = "usage_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    day = db.Column(db.Date, default=date.today)
    seconds_used = db.Column(db.Integer, default=0)

    __table_args__ = (db.UniqueConstraint("user_id", "day", name="uq_user_day"),)


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    level = db.Column(db.String(30), default="مبتدی")   # مبتدی/متوسط/پیشرفته
    order_index = db.Column(db.Integer, default=0)
    summary = db.Column(db.Text)
    content_md = db.Column(db.Text)   # محتوای مقاله به‌صورت Markdown ساده
    is_free = db.Column(db.Boolean, default=True)   # آیا در پلن‌های رایگان کامل قابل مشاهده است


class Quiz(db.Model):
    __tablename__ = "quizzes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    topic = db.Column(db.String(150))
    is_free = db.Column(db.Boolean, default=True)
    questions = db.relationship("Question", backref="quiz", lazy=True, cascade="all, delete-orphan")


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255))
    option_b = db.Column(db.String(255))
    option_c = db.Column(db.String(255))
    option_d = db.Column(db.String(255))
    correct_option = db.Column(db.String(1))  # 'a' | 'b' | 'c' | 'd'
    explanation = db.Column(db.Text)


class QuizAttempt(db.Model):
    __tablename__ = "quiz_attempts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)
    score = db.Column(db.Integer, default=0)
    total = db.Column(db.Integer, default=0)
    taken_at = db.Column(db.DateTime, default=datetime.utcnow)


class Note(db.Model):
    """جزوه‌های شخصی کاربر (خودنویس یا تولیدشده توسط هوش مصنوعی)"""
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    topic = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ChatMessage(db.Model):
    """تاریخچه‌ی گفتگو با معلم هوش مصنوعی"""
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    role = db.Column(db.String(20))  # user | assistant
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PurchaseRequest(db.Model):
    """درخواست خرید پلن؛ تا وقتی تیم لیولاف تایید نکند pending می‌ماند"""
    __tablename__ = "purchase_requests"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    plan_requested = db.Column(db.String(50), nullable=False)
    full_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    country = db.Column(db.String(120))
    address = db.Column(db.String(500))

    status = db.Column(db.String(20), default="pending")  # pending | approved | rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SupportMessage(db.Model):
    """چت پشتیبانی بین کاربر و اعضای لیولاف (جدا از چت با معلم هوش مصنوعی).
    توسط کاربر در برنامه‌ی اصلی و توسط اعضا در برنامه‌ی مدیریت خوانده/نوشته می‌شود."""
    __tablename__ = "support_messages"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    admin_id = db.Column(db.Integer, nullable=True)  # به admin_users در برنامه‌ی مدیریت اشاره دارد

    sender = db.Column(db.String(10))   # 'user' | 'admin'
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read_by_admin = db.Column(db.Boolean, default=False)
    is_read_by_user = db.Column(db.Boolean, default=False)


class Announcement(db.Model):
    """اعلان‌هایی که تیم پشتیبانی/مدیریت برای کاربران ارسال می‌کند"""
    __tablename__ = "announcements"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)  # خالی = برای همه
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)


class PlatformStatus(db.Model):
    """وضعیت کلی پلتفرم (فعال/غیرفعال) - توسط برنامه‌ی مدیریت از راه دور تغییر داده می‌شود"""
    __tablename__ = "platform_status"

    id = db.Column(db.Integer, primary_key=True)
    is_online = db.Column(db.Boolean, default=True)
    offline_message = db.Column(
        db.Text,
        default="فعلا دسترسی به پلتفرم به دلایل مختلفی از طرف کاربران عادی مجاز نیست. "
                "تا اطلاع ثانوی برنامه توسط گروه برنامه‌نویسی بسته است. "
                "برای ارتباط بیشتر با تیم برنامه‌نویسی لیولاف استودیو در لینکدین تماس بگیرید."
    )
