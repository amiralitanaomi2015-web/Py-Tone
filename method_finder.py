# -*- coding: utf-8 -*-
"""
ابزار جست‌وجوی متد پایتون:
کاربر بخشی از نام یک متد را وارد می‌کند (مثلا "app") و سیستم متدهای مشابه
را از میان انواع اصلی پایتون (str, list, dict, set, tuple) و همچنین
توابع سراسری (built-in functions) پیدا می‌کند و همراه با توضیح و مثال نشان می‌دهد.
"""

import builtins

TYPES_TO_SCAN = {
    "str": str,
    "list": list,
    "dict": dict,
    "set": set,
    "tuple": tuple,
    "int": int,
    "float": float,
}

_CACHE = None


def _clean_doc(doc):
    if not doc:
        return "توضیحی برای این متد ثبت نشده است."
    first_line = doc.strip().split("\n")[0]
    return first_line


def _build_index():
    """یک بار همه‌ی متدها و توابع را جمع‌آوری و کش می‌کند."""
    index = []

    # متدهای انواع داده‌ی اصلی
    for type_name, type_obj in TYPES_TO_SCAN.items():
        for attr_name in dir(type_obj):
            if attr_name.startswith("_"):
                continue
            try:
                attr = getattr(type_obj, attr_name)
            except Exception:
                continue
            if callable(attr):
                index.append({
                    "name": attr_name,
                    "owner": type_name,
                    "kind": "method",
                    "signature": f"{type_name}.{attr_name}(...)",
                    "doc": _clean_doc(getattr(attr, "__doc__", "")),
                })

    # توابع سراسری (built-in) مثل len, print, sorted, range, ...
    for name in dir(builtins):
        if name.startswith("_"):
            continue
        obj = getattr(builtins, name)
        if callable(obj) and not isinstance(obj, type):
            index.append({
                "name": name,
                "owner": "builtins",
                "kind": "function",
                "signature": f"{name}(...)",
                "doc": _clean_doc(getattr(obj, "__doc__", "")),
            })

    return index


def search_methods(partial_name, limit=25):
    """جست‌وجوی متدهایی که نامشان شامل partial_name است (بدون توجه به بزرگی/کوچکی حروف)."""
    global _CACHE
    if _CACHE is None:
        _CACHE = _build_index()

    partial_name = (partial_name or "").strip().lower()
    if not partial_name:
        return []

    # اول موارد «شروع‌شونده با» partial_name را بیاور، بعد موارد «شامل» partial_name
    starts_with = [m for m in _CACHE if m["name"].lower().startswith(partial_name)]
    contains = [m for m in _CACHE if partial_name in m["name"].lower() and m not in starts_with]

    results = starts_with + contains
    # حذف موارد تکراری (یک نام متد ممکن است در چند نوع تکرار شود ولی نگه‌شان می‌داریم چون owner فرق دارد)
    return results[:limit]
