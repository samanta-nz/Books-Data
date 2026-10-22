#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_section_audio.py — چیدن قطعه‌های صدای یک بخش و ساخت فایل .weba

منطق:
  ۱) فایل `arena-input/<درس>/<بخش>.tts.txt` را می‌خواند و ترتیب بلوک‌های گفتار و
     نشانگرهای مکث را بیرون می‌کشد.
  ۲) برای هر بلوک گفتار، فایل mp3 تولیدشده را به ترتیب برمی‌دارد.
  ۳) بین بلوک‌ها سکوت می‌گذارد: [مکث کوتاه] ۰.۶ ثانیه، [مکث متوسط] ۱.۲ ثانیه،
     [مکث بلند] ۲.۵ ثانیه.
  ۴) خروجی را به WebM/Opus با پسوند .weba تبدیل می‌کند (طبق راهنمای بسته).

استفاده:
    python3 tools/build_section_audio.py \
        --lesson ryazif01d01 --section ryazif01d01--goals \
        --clips clips/ryazif01d01--goals \
        --audio-dir audio

نام فایل‌های قطعه در پوشهٔ clips باید به ترتیب شماره‌گذاری شده باشند: 01.mp3, 02.mp3, ...
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

PAUSES = {"کوتاه": 0.6, "متوسط": 1.2, "بلند": 2.5}
SR = 48000


def ffmpeg() -> str:
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def parse_tts(path: Path):
    """ترتیب بلوک‌ها: ('speak', gوینده, متن) و ('pause', نوع, None)."""
    raw = path.read_text(encoding="utf-8")
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    items = []
    for chunk in re.split(r"\n\s*\n", raw):
        chunk = chunk.strip()
        if not chunk or chunk.startswith("#"):
            continue
        m = re.match(r"^\[مکث\s+(کوتاه|متوسط|بلند)\]$", chunk)
        if m:
            items.append(("pause", m.group(1), None))
            continue
        m = re.match(r"^\*\*(فرسام|سروناز):\*\*\s*(.*)$", chunk, flags=re.S)
        if m:
            text = " ".join(m.group(2).split())
            if text:
                items.append(("speak", m.group(1), text))
            continue
        items.append(("speak", "فرسام", " ".join(chunk.split())))
    return items


def decode_to_wav(src: Path, dst: Path):
    subprocess.run([ffmpeg(), "-y", "-loglevel", "error", "-i", str(src),
                    "-ac", "1", "-ar", str(SR), "-f", "wav", str(dst)], check=True)


def write_silence(dst: Path, seconds: float):
    n = int(SR * seconds)
    with wave.open(str(dst), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b"\x00\x00" * n)


def concat(data: np.ndarray, addition: np.ndarray) -> np.ndarray:
    return np.concatenate([data, addition])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--course-dir", type=Path,
                    default=Path(__file__).resolve().parents[1])
    ap.add_argument("--lesson", required=True)
    ap.add_argument("--section", required=True, help="مثلاً ryazif01d01--goals")
    ap.add_argument("--clips", type=Path, required=True, help="پوشهٔ قطعه‌های mp3")
    ap.add_argument("--audio-dir", type=Path, default=Path("audio"))
    ap.add_argument("--bitrate", default="64k")
    ap.add_argument("--report", type=Path, default=Path("build-report.json"))
    args = ap.parse_args()

    course = args.course_dir.resolve()
    tts_path = course / "arena-input" / args.lesson / f"{args.section}.tts.txt"
    if not tts_path.exists():
        raise SystemExit(f"فایل متن بخش پیدا نشد: {tts_path}")

    items = parse_tts(tts_path)
    speak_items = [x for x in items if x[0] == "speak"]
    clips = sorted(args.clips.glob("*.mp3"))
    if len(clips) != len(speak_items):
        raise SystemExit(
            f"تعداد قطعه‌ها ({len(clips)}) با تعداد بلوک‌های گفتار ({len(speak_items)}) برابر نیست.")
    for dup, n in ((1, len(clips)),):
        if len(set(p.name for p in clips)) != n:
            raise SystemExit("نام فایل تکراری در پوشهٔ قطعه‌ها.")

    audio = None
    log = []
    idx = 0
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for kind, name, text in items:
            if kind == "pause":
                sil = tmp / f"sil_{name}.wav"
                if not sil.exists():
                    write_silence(sil, PAUSES[name])
                with wave.open(str(sil), "rb") as w:
                    chunk = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2")
                audio = chunk if audio is None else concat(audio, chunk)
                log.append({"type": "pause", "kind": name, "seconds": PAUSES[name]})
                continue
            src = clips[idx]
            idx += 1
            wav = tmp / f"clip_{idx:03d}.wav"
            decode_to_wav(src, wav)
            with wave.open(str(wav), "rb") as w:
                chunk = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2")
            seconds = len(chunk) / SR
            audio = chunk if audio is None else concat(audio, chunk)
            log.append({"type": "speech", "speaker": name, "file": src.name,
                        "seconds": round(seconds, 2), "chars": len(text)})

    if audio is None:
        raise SystemExit("هیچ گفتاری در متن بخش پیدا نشد.")

    args.audio_dir.mkdir(parents=True, exist_ok=True)
    out = args.audio_dir / f"{args.section}.weba"
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as t:
        master = Path(t.name)
    with wave.open(str(master), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(audio.astype("<i2").tobytes())
    subprocess.run([ffmpeg(), "-y", "-loglevel", "error", "-i", str(master),
                    "-vn", "-c:a", "libopus", "-b:a", args.bitrate,
                    "-f", "webm", str(out)], check=True)
    master.unlink(missing_ok=True)

    head = out.read_bytes()[:4]
    info = {
        "lesson": args.lesson,
        "section": args.section,
        "tts_input": str(tts_path.relative_to(course)),
        "audio_filename": out.name,
        "audio_path": str(out),
        "duration_seconds": round(len(audio) / SR, 2),
        "bytes": out.stat().st_size,
        "container_ok": head == b"\x1aE\xdf\xa3",
        "segments": log,
    }
    if args.report.exists():
        try:
            data = json.loads(args.report.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {"sections": []}
    else:
        data = {"sections": []}
    data["sections"] = [s for s in data.get("sections", []) if s["section"] != args.section]
    data["sections"].append(info)
    args.report.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(info, ensure_ascii=False, indent=2))
    if not info["container_ok"]:
        raise SystemExit("خروجی کانتینر WebM/EBML نیست.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
