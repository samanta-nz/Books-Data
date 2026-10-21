"""تبدیل مارک‌داون درس ریاضی به فهرست قطعه‌های صوتی (گفتار + مکث).

ساختار فایل‌های درس در فصل‌های مختلف یکسان نیست؛ این پارسر هر سه شکل رایج را می‌خواند:

1) ``**فرسام**: ...``  (فصل ۱، ۴، ۶)
2) ``### نوبتِ ۳ — سروناز`` + پاراگراف‌های بعد از آن (فصل ۲)
3) ``فرسام: ...`` بدون ستاره (فصل ۲، ۳، ۵)

خروجی: فهرستی از آیتم‌ها با کلیدهای kind/speaker/text/seconds
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

PAUSE_SECONDS = {"کوتاه": 0.75, "متوسط": 1.5, "بلند": 2.6, "": 1.2}
SPEAKER_GAP = 0.35          # فاصلهٔ خودکار هنگام تغییر گوینده
SENTENCE_MAX = 190          # بیشترین طول یک قطعهٔ گفتار (نویسه)

SPEAKERS = [("فرسام", "farsam"), ("سروناز", "sarnaz")]

# نشانه‌گذاری نوبت‌ها در همهٔ فایل‌ها
_TURN_HEADING = re.compile(
    r"^#{2,4}\s*نوبتِ?\s*\d*\s*[—–-]?\s*(?P<speaker>فرسام|سروناز)\s*$"
)
_BOLD_TURN = re.compile(r"^\*\*(?P<speaker>فرسام|سروناز)\*\*\s*:?\s*(?P<rest>.*)$")
_PLAIN_TURN = re.compile(r"^(?P<speaker>فرسام|سروناز)\s*:\s*(?P<rest>.*)$")
_PAUSE = re.compile(r"\[مکث(?:\s*(?P<kind>کوتاه|متوسط|بلند))?\]")

# جملهٔ تکراری و بی‌معنای قالب در فایل‌های فصل ۱ (بیش از ۸۰۰ بار تکرار شده)
_BOILERPLATE = {
    "بذارید دلیلش رو روشن کنیم و این مرحله رو با دقت کامل بررسی کنیم",
    "بذارید دلیلش رو روشن کنیم و این مرحله را با دقت کامل بررسی کنیم",
}

_SKIP_LINE_PATTERNS = [
    re.compile(r"^ریاضی نهم[؛،]?\s*(فصل|درس)"),
    re.compile(r"^گویندگان\s*:"),
    re.compile(r"^فایل صوتی"),
    re.compile(r"^روایت کامل"),
    re.compile(r"^متن (?:کامل|مولد)"),
    re.compile(r"^\s*پیوندها"),
    re.compile(r"^\s*منابع"),
    re.compile(r"^\s*---+\s*$"),
]


@dataclass
class Item:
    kind: str            # "speech" | "pause"
    speaker: str | None = None
    text: str = ""
    seconds: float = 0.0


def _clean_line(line: str) -> str:
    line = line.strip()
    line = re.sub(r"^\*\*(?P<t>.+?)\*\*\s*:?", r"\g<t>", line)  # **متن**:
    line = line.replace("**", "")
    line = re.sub(r"^>+\s*", "", line)
    line = re.sub(r"^[-*•]\s+", "", line)
    return line.strip()


def _is_skippable(line: str) -> bool:
    if any(p.search(line) for p in _SKIP_LINE_PATTERNS):
        return True
    normalized = line.strip().strip(":؛.").strip()
    return normalized in _BOILERPLATE


def _split_sentences(text: str) -> list[str]:
    """تقسیم به جمله‌های کوتاه‌تر برای پایداری موتور گفتار."""
    parts = re.split(r"(?<=[.!؟])\s+", text)
    chunks: list[str] = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        while len(part) > SENTENCE_MAX:
            cut = part.rfind("،", 0, SENTENCE_MAX)
            if cut < 60:
                cut = part.rfind(" ", 0, SENTENCE_MAX)
            if cut < 40:
                cut = SENTENCE_MAX
            chunks.append(part[:cut].strip(" ،"))
            part = part[cut:].strip(" ،")
        if part:
            chunks.append(part)
    return chunks


def parse_markdown(path: Path) -> list[Item]:
    raw = path.read_text(encoding="utf-8")
    items: list[Item] = []
    speaker: str | None = None
    pending_speaker: str | None = None

    def emit_pause(kind: str) -> None:
        items.append(Item(kind="pause", seconds=PAUSE_SECONDS.get(kind, 1.2)))

    for raw_line in raw.splitlines():
        line = raw_line.rstrip()

        # مکث‌های درون‌خطی
        for match in _PAUSE.finditer(line):
            kind = (match.group("kind") or "").strip()
            before = line[: match.start()].strip()
            after = line[match.end():].strip()
            if before:
                line = before
            else:
                line = after
            emit_pause(kind)
        line = _PAUSE.sub(" ", line).strip()

        if not line.strip():
            continue

        stripped = line.strip()

        # تیترها
        if stripped.startswith("#"):
            turn = _TURN_HEADING.match(stripped)
            if turn:
                pending_speaker = turn.group("speaker")
            continue

        if _is_skippable(stripped):
            continue

        # نوبت با ستاره
        m = _BOLD_TURN.match(stripped)
        if m:
            pending_speaker = m.group("speaker")
            rest = _clean_line(m.group("rest"))
            if rest and not _is_skippable(rest):
                _append_speech(items, pending_speaker, rest)
            speaker = pending_speaker
            continue

        # نوبت بدون ستاره
        m = _PLAIN_TURN.match(stripped)
        if m:
            pending_speaker = m.group("speaker")
            rest = _clean_line(m.group("rest"))
            if rest and not _is_skippable(rest):
                _append_speech(items, pending_speaker, rest)
            speaker = pending_speaker
            continue

        text = _clean_line(stripped)
        if not text:
            continue
        # ستاره‌های تکی و نشانه‌های مارک‌داون
        text = re.sub(r"[*_]{1,2}", "", text).strip()
        if not text or re.fullmatch(r"[،.:؛\-—–\s]+", text):
            continue

        active = pending_speaker or speaker
        _append_speech(items, active, text)
        if pending_speaker:
            speaker = pending_speaker
        pending_speaker = None

    return _merge(items)


def _append_speech(items: list[Item], speaker: str | None, text: str) -> None:
    if text and not re.search(r"[\w\u0600-\u06FF]", text):
        return
    for chunk in _split_sentences(text):
        if items and items[-1].kind == "speech" and items[-1].speaker != speaker:
            items.append(Item(kind="pause", seconds=SPEAKER_GAP))
        items.append(Item(kind="speech", speaker=speaker, text=chunk))


def _merge(items: list[Item]) -> list[Item]:
    """حذف مکث‌های پشت‌سرهم و مکث ابتدای فایل؛ ادغام مکث‌های همسایه."""
    out: list[Item] = []
    for item in items:
        if item.kind == "pause":
            if not out:
                continue
            if out[-1].kind == "pause":
                out[-1].seconds = max(out[-1].seconds, item.seconds)
                continue
        out.append(item)
    while out and out[-1].kind == "pause":
        out.pop()
    return out


def plan(path: Path) -> dict:
    items = parse_markdown(path)
    speech = [i for i in items if i.kind == "speech"]
    pauses = [i for i in items if i.kind == "pause"]
    words = sum(len(i.text.split()) for i in speech)
    return {
        "source": str(path),
        "items": [asdict(i) for i in items],
        "stats": {
            "speech_items": len(speech),
            "pause_items": len(pauses),
            "words": words,
            "pause_seconds": round(sum(i.seconds for i in pauses), 2),
            "estimated_speech_seconds": round(words / 2.4, 1),
            "speakers": sorted({i.speaker for i in speech if i.speaker}),
        },
    }


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: parse_lesson.py <lesson.md> [out.json] [--summary]", file=sys.stderr)
        return 2
    src = Path(argv[1])
    data = plan(src)
    if "--summary" in argv:
        s = data["stats"]
        print(f"{src.name:24s} گفتار={s['speech_items']:4d} مکث={s['pause_items']:4d} "
              f"واژه={s['words']:5d} مکث‌ثانیه={s['pause_seconds']:7.1f} "
              f"تخمین={ (s['estimated_speech_seconds'] + s['pause_seconds'])/60:5.1f} دقیقه")
    if len(argv) > 2 and argv[2].endswith(".json"):
        Path(argv[2]).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
