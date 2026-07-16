# -*- coding: utf-8 -*-
"""پر کردن پایگاه‌داده با محتوای نمونه‌ی آموزشی پایتون (مقاله + کوییز)"""

from models import db, Article, Quiz, Question

ARTICLES = [
    dict(slug="intro-to-python", title="پایتون چیست؟", level="مبتدی", order_index=1, is_free=True,
         summary="آشنایی اولیه با زبان پایتون و کاربردهای آن",
         content_md=(
             "## پایتون چیست؟\n\n"
             "پایتون یک زبان برنامه‌نویسی سطح‌بالا، ساده و همه‌منظوره است که برای وب، "
             "هوش مصنوعی، تحلیل داده و اسکریپت‌نویسی استفاده می‌شود.\n\n"
             "### چرا پایتون؟\n"
             "- نحو (syntax) ساده و شبیه به زبان انسانی\n"
             "- جامعه‌ی بزرگ و کتابخانه‌های فراوان\n"
             "- مناسب برای مبتدی‌ها\n\n"
             "```python\nprint('سلام دنیا!')\n```"
         )),
    dict(slug="variables", title="متغیرها و انواع داده", level="مبتدی", order_index=2, is_free=True,
         summary="یادگیری تعریف متغیر و آشنایی با int، float، str، bool",
         content_md=(
             "## متغیرها\n\n"
             "در پایتون برای تعریف متغیر فقط کافیست یک نام و یک مقدار انتخاب کنید:\n\n"
             "```python\nname = 'علی'\nage = 20\nheight = 1.75\nis_student = True\n```\n\n"
             "نوع متغیر را می‌توان با تابع `type()` بررسی کرد."
         )),
    dict(slug="lists-dicts", title="لیست و دیکشنری", level="متوسط", order_index=3, is_free=True,
         summary="کار با ساختارهای داده‌ی list و dict",
         content_md=(
             "## لیست (list)\n\n"
             "```python\nfruits = ['سیب', 'موز', 'پرتقال']\nfruits.append('انگور')\n```\n\n"
             "## دیکشنری (dict)\n\n"
             "```python\nstudent = {'name': 'سارا', 'age': 22}\nprint(student['name'])\n```"
         )),
    dict(slug="functions", title="توابع در پایتون", level="متوسط", order_index=4, is_free=False,
         summary="نوشتن و فراخوانی توابع، پارامترها و مقدار بازگشتی",
         content_md=(
             "## تعریف تابع\n\n"
             "```python\ndef greet(name):\n    return f'سلام {name}!'\n\nprint(greet('رضا'))\n```"
         )),
    dict(slug="oop-basics", title="مقدمه‌ای بر برنامه‌نویسی شی‌گرا", level="پیشرفته", order_index=5, is_free=False,
         summary="آشنایی با کلاس، شیء، متد و مفاهیم پایه‌ی OOP",
         content_md=(
             "## کلاس و شیء\n\n"
             "```python\nclass Dog:\n    def __init__(self, name):\n        self.name = name\n\n"
             "    def bark(self):\n        return f'{self.name} پارس می‌کند!'\n```"
         )),
]

QUIZZES = [
    dict(title="کوییز مقدماتی پایتون", topic="مبانی", is_free=True, questions=[
        dict(text="کدام دستور برای چاپ متن در پایتون استفاده می‌شود؟",
             option_a="echo", option_b="print()", option_c="console.log", option_d="printf",
             correct_option="b", explanation="در پایتون از تابع print() برای چاپ خروجی استفاده می‌شود."),
        dict(text="کدام یک نوع داده‌ی صحیح (عدد صحیح) در پایتون است؟",
             option_a="str", option_b="bool", option_c="int", option_d="list",
             correct_option="c", explanation="int معرف عدد صحیح در پایتون است."),
        dict(text="برای تعریف تابع در پایتون از چه کلمه‌ی کلیدی استفاده می‌شود؟",
             option_a="function", option_b="def", option_c="func", option_d="lambda",
             correct_option="b", explanation="کلمه‌ی کلیدی def برای تعریف تابع به‌کار می‌رود."),
    ]),
    dict(title="کوییز ساختارهای داده", topic="لیست و دیکشنری", is_free=True, questions=[
        dict(text="کدام متد یک عنصر به انتهای لیست اضافه می‌کند؟",
             option_a="add()", option_b="append()", option_c="push()", option_d="insert_end()",
             correct_option="b", explanation="متد append() عنصر را به انتهای لیست اضافه می‌کند."),
        dict(text="برای دسترسی به مقدار یک کلید در دیکشنری از چه سینتکسی استفاده می‌شود؟",
             option_a="dict.key", option_b="dict->key", option_c="dict[key]", option_d="dict(key)",
             correct_option="c", explanation="با dict[key] می‌توان به مقدار مربوط به یک کلید دسترسی پیدا کرد."),
    ]),
]


def seed_if_empty():
    if Article.query.first() is None:
        for a in ARTICLES:
            db.session.add(Article(**a))

    if Quiz.query.first() is None:
        for q in QUIZZES:
            questions_data = q.pop("questions")
            quiz = Quiz(**q)
            for qd in questions_data:
                quiz.questions.append(Question(**qd))
            db.session.add(quiz)

    db.session.commit()
