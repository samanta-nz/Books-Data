"""آماده‌سازی متن برای مدل MMS فارسی (توکنایزر کاراکتری)."""
from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

from normalize_fa import normalize

VOICES_DIR = Path(__file__).resolve().parent / "voices"


@lru_cache(maxsize=1)
def load_vocab() -> dict[str, int]:
    path = VOICES_DIR / "mms-fas.vocab.json"
    if not path.exists():
        raise FileNotFoundError(f"vocab پیدا نشد: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def clean_for_mms(text: str) -> str:
    """نویسه‌هایی که در واژگان مدل نیستند حذف/جایگزین می‌شوند."""
    vocab = load_vocab()
    text = normalize(text)
    text = text.replace("\u200c", "")
    text = re.sub(r"[^\w\s\u0600-\u06FF]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    keep = [c for c in text if c in vocab or c == " "]
    out = "".join(keep)
    out = re.sub(r" +", " ", out).strip()
    return out or text
