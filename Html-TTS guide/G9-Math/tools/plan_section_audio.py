#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plan_section_audio.py — ساخت نقشهٔ قطعه‌های صدا برای هر بخش درس

چرا این ابزار: متن هر بخش صدها بلوک گفتار دارد و ساخت یک فایل برای هر بلوک عملی نیست.
اینجا بلوک‌های پشت‌سرهمِ یک گوینده که فقط با مکث کوتاه/متوسط از هم جدا شده‌اند به یک
قطعهٔ پیوسته تبدیل می‌شوند؛ اما هر [مکث بلند] مرز قطعی است و در فایل نهایی سکوت واقعی
می‌گیرد (چون همان‌جاست که دانش‌آموز باید فکر کند).

هر قطعهٔ بلندتر از ۱۴۰۰ نویسه (سقف تولید صدا) روی مرز جمله شکسته می‌شود.

خروجی: plan.json
    {"lessons": {"ryazif01d01": {"sections": {
        "goals": {"parts": [{"i":0,"speaker":"فرسام","text":"...","chars":123}, ...],
                  "silences_before": [0, 2500, ...]}}}}}
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_section_audio import parse_tts  # noqa: E402

MAX_CHARS = 1400
PAUSE_MS = {"کوتاه": 600, "متوسط": 1200, "بلند": 2500}
SENT_SPLIT = re.compile(r"(?<=[.!?؟؛:])\s+")


def split_long(text: str, limit: int = MAX_CHARS):
    """شکستن متن بلند روی مرز جمله تا حداکثر limit نویسه."""
    if len(text) <= limit:
        return [text]
    sentences = SENT_SPLIT.split(text)
    out, cur = [], ""
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        if not cur:
            cur = s
        elif len(cur) + 1 + len(s) <= limit:
            cur += " " + s
        else:
            out.append(cur)
            cur = s
    if cur:
        out.append(cur)
    # اگر جملهٔ تکی از سقف بلندتر بود، با ویرگول بشکن
    final = []
    for chunk in out:
        while len(chunk) > limit:
            cut = chunk.rfind("،", 0, limit)
            if cut < limit * 0.5:
                cut = chunk.rfind(" ", 0, limit)
            if cut <= 0:
                cut = limit
            final.append(chunk[:cut + 1].strip())
            chunk = chunk[cut + 1:].strip()
        if chunk:
            final.append(chunk)
    return final


def plan_section(items):
    """items → (parts, silences_before)"""
    parts = []
    silences = []
    pending = 0          # سکوت انباشتهٔ قبل از قطعهٔ بعدی
    run_speaker = None
    buffer = []

    def flush():
        nonlocal buffer, run_speaker, pending
        if not buffer:
            return
        text = " ".join(" ".join(buffer).split())
        chunks = split_long(text)
        for k, ch in enumerate(chunks):
            parts.append({"i": len(parts), "speaker": run_speaker, "text": ch,
                          "chars": len(ch)})
            silences.append(pending if k == 0 else 350)
            pending = 0
        buffer = []

    for kind, name, text in items:
        if kind == "pause":
            if name == "بلند":
                flush()
                run_speaker = None
                pending += PAUSE_MS["بلند"]
            elif run_speaker is None:
                pending += PAUSE_MS[name]
            # مکث کوتاه/متوسط داخل گفتار پیوسته: در متن با مرز جمله پوشش داده می‌شود
            continue
        if run_speaker is not None and name != run_speaker:
            flush()
            pending += PAUSE_MS["متوسط"]
        run_speaker = name
        buffer.append(text)
    flush()
    return parts, silences


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--course-dir", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--lesson", required=True)
    ap.add_argument("--sections", nargs="*", help="اگر خالی باشد، همهٔ بخش‌های درس")
    ap.add_argument("--out", type=Path, default=Path("plan.json"))
    args = ap.parse_args()

    course = args.course_dir.resolve()
    src = course / "arena-input" / args.lesson
    if not src.is_dir():
        raise SystemExit(f"پوشهٔ ورودی درس پیدا نشد: {src}")

    files = sorted(src.glob("*.tts.txt"))
    if args.sections:
        want = set(args.sections)
        files = [p for p in files
                 if p.name.replace(".tts.txt", "").replace(args.lesson + "--", "") in want]
    if not files:
        raise SystemExit("هیچ فایل متنی پیدا نشد.")

    sections = {}
    total_parts = total_chars = 0
    for p in files:
        sec = p.name.replace(".tts.txt", "").replace(args.lesson + "--", "")
        parts, silences = plan_section(parse_tts(p))
        sections[sec] = {"tts_input": str(p.relative_to(course)),
                         "parts": parts, "silences_before": silences}
        total_parts += len(parts)
        total_chars += sum(x["chars"] for x in parts)
        speakers = {}
        for x in parts:
            speakers[x["speaker"]] = speakers.get(x["speaker"], 0) + 1
        print(f"{sec:14} parts={len(parts):3d} chars={sum(x['chars'] for x in parts):5d} "
              f"speakers={speakers} max_part={max(x['chars'] for x in parts)}")

    existing = {}
    if args.out.exists():
        try:
            existing = json.loads(args.out.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = {}
    lessons = existing.get("lessons", {})
    lessons.setdefault(args.lesson, {}).setdefault("sections", {}).update(sections)
    existing["lessons"] = lessons
    existing["max_chars"] = MAX_CHARS
    args.out.write_text(json.dumps(existing, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nنوشته شد: {args.out} — parts={total_parts} chars={total_chars}")


if __name__ == "__main__":
    main()
