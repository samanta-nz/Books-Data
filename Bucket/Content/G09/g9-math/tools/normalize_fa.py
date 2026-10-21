"""نرمال‌سازی متن فارسی برای موتور گفتار (Piper / VITS-MMS).

ورودی متن خام مارک‌داون درس است؛ خروجی متنی است که
- نشانه‌های مارک‌داون در آن نیست،
- رقم‌ها به واژه تبدیل شده‌اند،
- نمادهای ریاضی به واژهٔ خوانا تبدیل شده‌اند،
- نیم‌فاصله و حروف عربی یکسان‌سازی شده‌اند.
"""
from __future__ import annotations

import re

try:  # num2words اختیاری است؛ در نبودش رقم‌ها یکی‌یکی خوانده می‌شوند
    from num2words import num2words as _n2w
except Exception:  # pragma: no cover
    _n2w = None

ZWNJ = "\u200c"

_PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
_ARABIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"

_CHAR_MAP = {
    "ي": "ی",
    "ك": "ک",
    "ﻻ": "لا",
    "ۀ": "هٔ",
    "‍": "",      # ZWJ
    "ـ": "",      # کشیدگی
    "…": "...",
    "«": "",
    "»": "",
    "“": "",
    "”": "",
    '"': "",
    "*": "",
    "`": "",
    "#": " ",
    "|": " ",
    "[": " ",
    "]": " ",
    "{": " ",
    "}": " ",
    "\\": " ",
    "•": " ",
    "→": " به ",
    "←": " به ",
    "↑": " ",
    "↓": " ",
    "⬅": " ",
    "➡": " ",
    "✅": " ",
    "✳": " ",
    "⚠": " ",
}

_MATH_PHRASES = [
    ("≠", " نامساوی است با "),
    ("≤", " کوچک‌تر یا مساوی "),
    ("≥", " بزرگ‌تر یا مساوی "),
    ("≈", " تقریباً برابر "),
    ("±", " مثبت یا منفی "),
    ("√", " رادیکال "),
    ("×", " ضربدر "),
    ("÷", " تقسیم بر "),
    ("−", " منهای "),
    ("–", " تا "),
    ("—", " تا "),
    ("=", " مساوی است با "),
    ("+", " به‌علاوهٔ "),
    ("%", " درصد "),
    ("٪", " درصد "),
    ("°", " درجه "),
    ("∠", " زاویهٔ "),
    ("△", " مثلث "),
    ("⊥", " عمود بر "),
    ("∥", " موازی "),
    ("∈", " عضو "),
    ("∉", " عضو نیست "),
    ("⊂", " زیرمجموعهٔ "),
    ("∪", " اجتماع "),
    ("∩", " اشتراک "),
    ("∅", " تهی "),
    ("∞", " بی‌نهایت "),
    ("π", " پی "),
]

_LATIN_WORDS = {
    "x": "ایکس",
    "y": "وای",
    "z": "زِد",
    "a": "آ",
    "b": "ب",
    "c": "ث",
    "n": "اِن",
    "m": "اِم",
    "AB": "آ ب",
    "BC": "ب ث",
    "AC": "آ ث",
}

_SUPERSCRIPTS = {
    "²": " به توان دو ",
    "³": " به توان سه ",
    "⁴": " به توان چهار ",
}


def _digits_to_ascii(text: str) -> str:
    table = {ord(p): str(i) for i, p in enumerate(_PERSIAN_DIGITS)}
    table.update({ord(p): str(i) for i, p in enumerate(_ARABIC_DIGITS)})
    return text.translate(table)


def _number_to_words(num: str) -> str:
    num = num.replace(",", "").replace("٬", "").replace("٫", ".")
    if _n2w is None:
        return " ".join(num)
    try:
        if "." in num:
            whole, frac = num.split(".", 1)
            whole_w = _n2w(int(whole), lang="fa") if whole else "صفر"
            frac_w = " ".join(_n2w(int(d), lang="fa") for d in frac if d.isdigit())
            return f"{whole_w} ممیز {frac_w}".strip()
        return _n2w(int(num), lang="fa")
    except Exception:
        return " ".join(num)


def normalize(text: str) -> str:
    """متن مارک‌داون را به متن خوانا برای TTS تبدیل می‌کند."""
    if not text:
        return ""

    out = text
    for src, dst in _CHAR_MAP.items():
        out = out.replace(src, dst)

    for src, dst in _SUPERSCRIPTS.items():
        out = out.replace(src, dst)
    for src, dst in _MATH_PHRASES:
        out = out.replace(src, dst)

    out = _digits_to_ascii(out)

    # درصد و رقم‌های اعشاری/هزارگان
    out = re.sub(r"(\d+(?:\.\d+)?)\s*/\s*(\d+)", r"\1 تقسیم بر \2", out)
    out = re.sub(r"\d+(?:[.,]\d+)*", lambda m: " " + _number_to_words(m.group(0)) + " ", out)

    # حروف لاتین تنها (متغیرهای ریاضی)
    def _latin(match: re.Match[str]) -> str:
        token = match.group(0)
        return _LATIN_WORDS.get(token, _LATIN_WORDS.get(token.lower(), " "))

    out = re.sub(r"\b[A-Za-z]{1,3}\b", _latin, out)

    # نیم‌فاصله: حذف تا واژه یکپارچه خوانده شود
    out = out.replace(ZWNJ, "")

    # نشانه‌های اضافی
    out = re.sub(r"[\[\]{}<>_^~@$&]", " ", out)
    out = re.sub(r"\.{2,}", "،", out)
    out = re.sub(r"[ \t\u00a0]+", " ", out)
    out = re.sub(r"\s*\n\s*", "\n", out)
    out = re.sub(r" +([،؛:؟!.])", r"\1", out)
    out = re.sub(r"\n{2,}", "\n", out)

    return out.strip()
