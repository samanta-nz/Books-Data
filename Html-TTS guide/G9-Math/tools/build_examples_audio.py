#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_examples_audio.py — ساخت فایل جدا برای هر مثال + فایل یکپارچهٔ بخش

چرا: پلیر صفحه برای هر «بخش» یک فایل دارد (`ryazif01d01--examples.weba`) و نگاشت
بسته هم همین نام را می‌خواهد. اما کاربر می‌خواهد هر مثال جداگانه پخش شود. پس این
ابزار دو خروجی می‌سازد:

  ۱) audio/ryazif01d01--examples.weba        ← فایل یکپارچهٔ بخش (برای نگاشت اصلی)
  ۲) audio-examples/ryazif01d01--example-NN.weba ← یک فایل مستقل برای هر مثال

مرز مثال‌ها از خود متن گرفته می‌شود: هر قطعه‌ای که عبارت «صورت این مثال» دارد،
آغاز یک مثال است. متن مقدمهٔ بخش از مثال اول جدا می‌شود.

خروجی جانبی: audio-examples/examples-index.json و examples.html (پلیر جدا برای هر مثال)
"""

import argparse
import html
import base64
import json
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

SR = 48000
MARKER = "صورت این مثال"
INTRO_CUT = "توضیح فعالیت کتاب"


def ffmpeg() -> str:
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def decode(src: Path, dst: Path):
    subprocess.run([ffmpeg(), "-y", "-loglevel", "error", "-i", str(src),
                    "-ac", "1", "-ar", str(SR), "-f", "wav", str(dst)], check=True)


def read_wav(p: Path) -> np.ndarray:
    with wave.open(str(p), "rb") as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype="<i2")


def to_weba(samples: np.ndarray, out: Path, bitrate: str):
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as t:
        master = Path(t.name)
    with wave.open(str(master), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(samples.astype("<i2").tobytes())
    subprocess.run([ffmpeg(), "-y", "-loglevel", "error", "-i", str(master),
                    "-vn", "-c:a", "libopus", "-b:a", bitrate, "-f", "webm",
                    str(out)], check=True)
    master.unlink(missing_ok=True)


def build_groups(parts):
    """(intro_parts, [ {index, title, parts:[...] } ])"""
    intro, groups = [], []
    for p in parts:
        if MARKER in p["text"]:
            body = p["text"]
            if not groups and not intro and INTRO_CUT in body:
                i = body.index(INTRO_CUT)
                head, tail = body[:i].strip(), body[i:].strip()
                if head:
                    intro.append({**p, "text": head, "chars": len(head)})
                body = tail
            groups.append({"index": len(groups) + 1, "parts": [{**p, "text": body,
                                                               "chars": len(body)}]})
        else:
            if groups:
                groups[-1]["parts"].append(p)
            else:
                intro.append(p)
    for g in groups:
        first = g["parts"][0]["text"]
        # عنوان کوتاه برای پلیر: بعد از «انتخاب کنین:»
        title = first.split("انتخاب کنین:")[-1].split("حالا صدا رو متوقف")[0].strip()
        title = title.strip(" «»:؛،.")
        g["title"] = (title[:110] + "…") if len(title) > 110 else title
    return intro, groups


def render_group(group, clips_dir: Path):
    audio = np.zeros(0, dtype="<i2")
    log = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for k, p in enumerate(group["parts"]):
            if k:
                audio = np.concatenate([audio, np.zeros(int(SR * 0.9), dtype="<i2")])
            src = clips_dir / f"p{p['i']:02d}.mp3"
            if not src.exists():
                raise SystemExit(f"قطعهٔ غایب: {src}")
            wav = tmp / f"c{k}.wav"
            decode(src, wav)
            chunk = read_wav(wav)
            audio = np.concatenate([audio, chunk])
            log.append({"part": p["i"], "speaker": p["speaker"],
                        "seconds": round(len(chunk) / SR, 2)})
    return audio, log


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--course-dir", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--lesson", default="ryazif01d01")
    ap.add_argument("--section", default="examples")
    ap.add_argument("--plan", type=Path, default=Path("plan.json"))
    ap.add_argument("--clips", type=Path, required=True)
    ap.add_argument("--audio-dir", type=Path, default=Path("audio"))
    ap.add_argument("--per-example-dir", type=Path, default=Path("audio-examples"))
    ap.add_argument("--bitrate", default="32k")
    ap.add_argument("--report", type=Path, default=Path("build-report.json"))
    args = ap.parse_args()

    course = args.course_dir.resolve()
    plan = json.loads((course / args.plan).read_text(encoding="utf-8"))
    node = plan["lessons"][args.lesson]["sections"][args.section]
    clips_dir = args.clips if args.clips.is_absolute() else course / args.clips
    audio_dir = args.audio_dir if args.audio_dir.is_absolute() else course / args.audio_dir

    intro, groups = build_groups(node["parts"])
    print(f"مقدمه: {len(intro)} قطعه · مثال‌ها: {len(groups)}")
    for g in groups:
        print(f"  مثال {g['index']}: parts={[p['i'] for p in g['parts']]} — {g['title'][:60]}")

    per_dir = args.per_example_dir if args.per_example_dir.is_absolute() else course / args.per_example_dir
    per_dir.mkdir(parents=True, exist_ok=True)

    full = np.zeros(int(SR * 1.0), dtype="<i2")   # مقدمه با یک ثانیه شروع
    entries, index = [], []
    for g in groups:
        samples, log = render_group(g, clips_dir)
        name = f"{args.lesson}--example-{g['index']:02d}.weba"
        out = per_dir / name
        to_weba(samples, out, args.bitrate)
        entries.append({"index": g["index"], "title": g["title"], "file": name,
                        "duration_seconds": round(len(samples) / SR, 2),
                        "bytes": out.stat().st_size, "segments": log})
        index.append({"index": g["index"], "title": g["title"], "file": name,
                      "seconds": round(len(samples) / SR, 2)})
        full = np.concatenate([full, samples, np.zeros(int(SR * 1.6), dtype="<i2")])

    combined = audio_dir / f"{args.lesson}--{args.section}.weba"
    to_weba(full, combined, args.bitrate)
    print(f"یکپارچه: {combined.name} {len(full)/SR:.1f}s {combined.stat().st_size}B")

    (per_dir / "examples-index.json").write_text(
        json.dumps({"lesson": args.lesson, "section": args.section,
                    "combined": {"file": combined.name,
                                 "duration_seconds": round(len(full) / SR, 2),
                                 "bytes": combined.stat().st_size},
                    "examples": index}, ensure_ascii=False, indent=1), encoding="utf-8")

    # گزارش برای ابزار امبد (فقط فایل یکپارچه)
    rep = args.report if args.report.is_absolute() else course / args.report
    data = {"sections": []}
    if rep.exists():
        try:
            data = json.loads(rep.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    data["sections"] = [s for s in data.get("sections", []) if s["section"] != args.section]
    data["sections"].append({"lesson": args.lesson, "section": args.section,
                             "tts_input": node.get("tts_input"),
                             "audio_filename": combined.name,
                             "audio_path": str(combined),
                             "duration_seconds": round(len(full) / SR, 2),
                             "bytes": combined.stat().st_size,
                             "parts": len(node["parts"]),
                             "examples": len(groups),
                             "per_example": entries})
    rep.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

    # صفحهٔ پلیر مستقل برای هر مثال (صدا جاسازی‌شده تا در نمایشگر فایل هم کار کند)
    cards = []
    for e in entries:
        b64 = base64.b64encode((per_dir / e["file"]).read_bytes()).decode("ascii")
        cards.append(f'''  <article class="card">
    <div class="head"><span class="num">مثال {e["index"]}</span>
      <span class="dur">{e["duration_seconds"]} ثانیه</span></div>
    <p class="title">{html.escape(e["title"])}</p>
    <audio controls preload="none" src="data:audio/webm;base64,{b64}"></audio>
    <p class="path"><code>{e["file"]}</code> · {e["bytes"]//1024} کیلوبایت</p>
  </article>''')
    page = f'''<!DOCTYPE html>
<html lang="fa" dir="rtl"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>مثال‌های حل‌شده — {args.lesson}</title>
<style>
 body{{margin:0;padding:28px 16px 60px;font-family:"Vazirmatn","Segoe UI",Tahoma,sans-serif;
   background:radial-gradient(1000px 520px at 15% -10%,#1a3329 0%,#0d1412 60%);color:#eef5f0}}
 .wrap{{max-width:820px;margin:0 auto}} h1{{font-size:1.45rem;margin:0 0 8px}}
 .sub{{color:#9db3a8;font-size:.9rem;line-height:1.9;margin:0 0 22px}}
 .card{{background:linear-gradient(180deg,rgba(255,255,255,.04),rgba(255,255,255,.01)),#151f1b;
   border:1px solid #26362e;border-radius:16px;padding:14px;margin-bottom:12px}}
 .head{{display:flex;gap:10px;align-items:center;margin-bottom:6px}}
 .num{{font-size:.8rem;color:#4ec9a0;border:1px solid rgba(78,201,160,.5);
   background:rgba(78,201,160,.1);padding:3px 10px;border-radius:999px}}
 .dur{{font-size:.75rem;color:#9db3a8}}
 .title{{font-size:.86rem;color:#cfe3d8;line-height:1.9;margin:0 0 8px}}
 audio{{width:100%}}
 .path{{font-size:.7rem;color:#7f948a;margin:6px 0 0;direction:ltr;text-align:left}}
 code{{background:rgba(255,255,255,.06);padding:1px 5px;border-radius:5px}}
 footer{{color:#9db3a8;font-size:.77rem;line-height:2;margin-top:22px;
   border-top:1px solid #26362e;padding-top:14px}}
</style></head><body><div class="wrap">
<h1>مثال‌های حل‌شده — {args.lesson}</h1>
<p class="sub">هر مثال یک فایل صوتی مستقل دارد و جداگانه پخش می‌شود. مقدمهٔ بخش و ترتیب اصلی
در پلیر خود صفحهٔ درس با فایل یکپارچه حفظ شده است.</p>
{chr(10).join(cards)}
<footer>فایل یکپارچهٔ بخش: <code>{combined.name}</code> ({len(full)/SR:.1f} ثانیه) ·
فایل‌های مستقل در <code>{args.per_example_dir}/</code> · فهرست: <code>examples-index.json</code></footer>
</div></body></html>
'''
    page_path = per_dir / "examples.html"
    page_path.write_text(page, encoding="utf-8")
    print(f"صفحهٔ مثال‌ها: {page_path} ({page_path.stat().st_size/1024/1024:.2f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
