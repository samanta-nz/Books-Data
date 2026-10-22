#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_section_from_plan.py — چیدن قطعه‌ها بر اساس plan.json و ساخت فایل .weba

هر بخش به قطعه‌های پیوستهٔ گفتار (parts) شکسته شده است. قطعه‌ها با نام
p00.mp3, p01.mp3, ... در clips/<بخش>/ قرار می‌گیرند و به ترتیب شمارهٔ part
با سکوت‌های تعیین‌شده در plan.json به هم می‌چسبند.

استفاده:
    python3 tools/build_section_from_plan.py --lesson ryazif01d01 \
        --section ryazif01d01--concept-1 --plan plan.json \
        --clips clips/ryazif01d01--concept-1 --audio-dir audio
"""

import argparse
import json
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

SR = 48000


def ffmpeg() -> str:
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def read_wav(path: Path) -> np.ndarray:
    with wave.open(str(path), "rb") as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype="<i2")


def decode(src: Path, dst: Path):
    subprocess.run([ffmpeg(), "-y", "-loglevel", "error", "-i", str(src),
                    "-ac", "1", "-ar", str(SR), "-f", "wav", str(dst)], check=True)


def silence(seconds: float) -> np.ndarray:
    return np.zeros(int(SR * seconds), dtype="<i2")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--course-dir", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--lesson", required=True)
    ap.add_argument("--section", required=True, help="مثلاً ryazif01d01--concept-1")
    ap.add_argument("--plan", type=Path, default=Path("plan.json"))
    ap.add_argument("--clips", type=Path, required=True)
    ap.add_argument("--audio-dir", type=Path, default=Path("audio"))
    ap.add_argument("--bitrate", default="64k")
    ap.add_argument("--report", type=Path, default=Path("build-report.json"))
    args = ap.parse_args()

    course = args.course_dir.resolve()
    plan_path = args.plan if args.plan.is_absolute() else course / args.plan
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    sec = args.section.replace(args.lesson + "--", "")
    try:
        node = plan["lessons"][args.lesson]["sections"][sec]
    except KeyError:
        raise SystemExit(f"بخش {sec} در {plan_path} نیست.")

    parts, sil = node["parts"], node["silences_before"]
    clips = {p.name: p for p in args.clips.glob("*.mp3")}
    missing = [f"p{p['i']:02d}.mp3" for p in parts if f"p{p['i']:02d}.mp3" not in clips]
    if missing:
        raise SystemExit(f"{len(missing)} قطعه غایب است: {', '.join(missing[:6])}")

    audio = np.zeros(0, dtype="<i2")
    log = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for p in parts:
            name = f"p{p['i']:02d}.mp3"
            wait = sil[p["i"]] / 1000.0
            if wait > 0:
                audio = np.concatenate([audio, silence(wait)])
            wav = tmp / (name + ".wav")
            decode(clips[name], wav)
            chunk = read_wav(wav)
            audio = np.concatenate([audio, chunk])
            log.append({"part": p["i"], "speaker": p["speaker"], "source": name,
                        "silence_before_s": wait, "seconds": round(len(chunk) / SR, 2),
                        "chars": p["chars"]})

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

    info = {
        "lesson": args.lesson, "section": sec,
        "tts_input": node.get("tts_input"),
        "audio_filename": out.name, "audio_path": str(out),
        "duration_seconds": round(len(audio) / SR, 2),
        "bytes": out.stat().st_size,
        "container_ok": out.read_bytes()[:4] == b"\x1aE\xdf\xa3",
        "parts": len(parts),
        "segments": log,
    }
    rep = args.report if args.report.is_absolute() else course / args.report
    data = {"sections": []}
    if rep.exists():
        try:
            data = json.loads(rep.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    data["sections"] = [s for s in data.get("sections", []) if s["section"] != sec]
    data["sections"].append(info)
    rep.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"{out.name}  {info['duration_seconds']}s  {info['bytes']}B  "
          f"parts={info['parts']}  container_ok={info['container_ok']}")
    return 0 if info["container_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
