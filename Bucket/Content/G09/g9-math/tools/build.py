"""ساخت روایت صوتی درس‌های ریاضی نهم از فایل‌های مارک‌داون.

مسیر کار:
    md → (parse_lesson) قطعه‌های گفتار/مکث → (voices) گفتار → (scipy) یکسان‌سازی نرخ
       → (ffmpeg) بلندی صدا و کدگذاری Opus/WebM → خروجی ``*.weba`` کنار همان md

نمونه:
    python build.py --limit 1
    python build.py --files F01/ryazif01d01.md --force
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
import time
import wave
from pathlib import Path

import numpy as np
from scipy.signal import resample_poly

import parse_lesson
from normalize_fa import normalize

TOOLS_DIR = Path(__file__).resolve().parent
BASE_DIR = TOOLS_DIR.parent
OUTPUT_SR = 24000
BITRATE = "32k"
CACHE_DIR = TOOLS_DIR / ".cache"
REPORT = BASE_DIR / "audio-report.md"
STATE = TOOLS_DIR / "build-state.json"


# --------------------------------------------------------------------------- #
# ffmpeg
# --------------------------------------------------------------------------- #
def ffmpeg_exe() -> str:
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:  # noqa: BLE001
        return "ffmpeg"


def encode_weba(wav_path: Path, out_path: Path) -> None:
    cmd = [
        ffmpeg_exe(), "-y", "-loglevel", "error",
        "-i", str(wav_path),
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-ac", "1", "-ar", str(OUTPUT_SR),
        "-c:a", "libopus", "-b:a", BITRATE, "-application", "audio",
        "-f", "webm", str(out_path),
    ]
    subprocess.run(cmd, check=True)


# --------------------------------------------------------------------------- #
# کش گفتار
# --------------------------------------------------------------------------- #
def cache_key(text: str, speaker: str, engine_sig: str) -> str:
    h = hashlib.sha1(f"{engine_sig}|{speaker}|{text}".encode("utf-8")).hexdigest()
    return h[:20]


def synth_to_cache(backend, text: str, key: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    audio_path = CACHE_DIR / f"{key}.npy"
    sr_path = CACHE_DIR / f"{key}.sr"
    if audio_path.exists() and sr_path.exists():
        return audio_path
    audio, sr = backend.synth(text)
    tmp = CACHE_DIR / f"{key}.tmp.npy"
    np.save(tmp, audio)
    tmp.replace(audio_path)
    sr_path.write_text(str(sr), encoding="utf-8")
    return audio_path


def load_cached(path: Path) -> tuple[np.ndarray, int]:
    sr = int((path.with_suffix(".sr")).read_text(encoding="utf-8").strip())
    return np.load(path), sr


# --------------------------------------------------------------------------- #
# ساخت یک درس
# --------------------------------------------------------------------------- #
def resample(audio: np.ndarray, sr: int, target: int = OUTPUT_SR) -> np.ndarray:
    if sr == target or audio.size == 0:
        return audio.astype(np.int16)
    g = math.gcd(int(sr), int(target))
    up, down = target // g, sr // g
    out = resample_poly(audio.astype(np.float32), up, down)
    return np.clip(out, -32768, 32767).astype(np.int16)


def silence(seconds: float, sr: int = OUTPUT_SR) -> np.ndarray:
    return np.zeros(int(seconds * sr), dtype=np.int16)


def build_lesson(md_path: Path, backends: dict, engine_sig: str, force: bool = False,
                 verbose: bool = True) -> dict:
    out_path = md_path.with_suffix(".weba")
    started = time.time()
    plan = parse_lesson.plan(md_path)
    items = plan["items"]
    speech_items = [i for i in items if i["kind"] == "speech"]
    total_words = sum(len(i["text"].split()) for i in speech_items)

    if out_path.exists() and not force:
        return {
            "file": str(md_path.relative_to(BASE_DIR)),
            "status": "skipped",
            "output": str(out_path.relative_to(BASE_DIR)),
            "seconds": probe_duration(out_path),
        }

    pieces: list[np.ndarray] = []
    done = 0
    for item in items:
        if item["kind"] == "pause":
            pieces.append(silence(float(item["seconds"])))
            continue
        speaker = item["speaker"] or "farsam"
        backend = backends.get(speaker, backends["farsam"])
        text = normalize(item["text"])
        if not text:
            continue
        key = cache_key(text, speaker, engine_sig)
        path = CACHE_DIR / f"{key}.npy"
        if not path.exists():
            synth_to_cache(backend, text, key)
        audio, sr = load_cached(path)
        pieces.append(resample(audio, sr))
        done += 1
        if verbose and done % 25 == 0:
            print(f"    {md_path.name}: {done}/{len(speech_items)} قطعه", flush=True)

    if not pieces:
        raise RuntimeError(f"هیچ قطعه‌ای ساخته نشد: {md_path}")

    audio_all = np.concatenate(pieces)
    tmp_wav = CACHE_DIR / f"{md_path.stem}.wav"
    with wave.open(str(tmp_wav), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(OUTPUT_SR)
        wf.writeframes(audio_all.tobytes())

    encode_weba(tmp_wav, out_path)
    tmp_wav.unlink(missing_ok=True)

    seconds = probe_duration(out_path)
    return {
        "file": str(md_path.relative_to(BASE_DIR)),
        "status": "built",
        "output": str(out_path.relative_to(BASE_DIR)),
        "seconds": seconds,
        "words": total_words,
        "size_mb": round(out_path.stat().st_size / 1e6, 2),
        "elapsed_s": round(time.time() - started, 1),
    }


def probe_duration(path: Path) -> float | None:
    try:
        out = subprocess.run(
            [ffmpeg_exe(), "-hide_banner", "-i", str(path)],
            capture_output=True, text=True, check=False,
        ).stderr
        m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", out)
        if not m:
            return None
        h, mi, s = m.groups()
        return round(int(h) * 3600 + int(mi) * 60 + float(s), 1)
    except Exception:  # noqa: BLE001
        return None


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def list_lessons() -> list[Path]:
    files = sorted(
        p for p in BASE_DIR.glob("F*/*.md")
        if p.parent.name.startswith("F")
    )
    return files


def write_report(results: list[dict]) -> None:
    lines = ["# گزارش ساخت روایت صوتی — ریاضی نهم", ""]
    lines.append("| فایل | خروجی | مدت | حجم | وضعیت |")
    lines.append("|---|---|---|---|---|")
    for r in results:
        dur = r.get("seconds")
        dur_s = f"{int(dur // 60)}:{int(dur % 60):02d}" if dur else "—"
        lines.append(
            f"| `{r['file']}` | `{r.get('output', '—')}` | {dur_s} | "
            f"{r.get('size_mb', '—')} MB | {r['status']} |"
        )
    report = "\n".join(lines) + "\n"
    existing = REPORT.read_text(encoding="utf-8") if REPORT.exists() else ""
    if not existing:
        REPORT.write_text(report, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--files", nargs="*", help="مسیر نسبی فایل‌ها؛ پیش‌فرض همه")
    ap.add_argument("--limit", type=int, default=0, help="حداکثر تعداد فایل")
    ap.add_argument("--engine", default="auto", choices=["auto", "stub"])
    ap.add_argument("--force", action="store_true", help="بازسازی فایل‌های موجود")
    args = ap.parse_args(argv)

    if args.files:
        targets = [BASE_DIR / f for f in args.files]
    else:
        targets = list_lessons()
        # فقط فایل‌هایی که خروجی ندارند
        targets = [t for t in targets if args.force or not t.with_suffix(".weba").exists()]
    if args.limit:
        targets = targets[: args.limit]
    if not targets:
        print("همهٔ فایل‌ها ساخته شده‌اند.")
        return 0

    backends = voices_make(args.engine)
    engine_sig = "|".join(f"{k}:{type(v).__name__}" for k, v in backends.items())

    results = []
    t0 = time.time()
    for i, md in enumerate(targets, 1):
        print(f"[{i}/{len(targets)}] {md.relative_to(BASE_DIR)}", flush=True)
        try:
            res = build_lesson(md, backends, engine_sig, force=args.force)
        except Exception as exc:  # noqa: BLE001
            print(f"    ✗ {exc}", flush=True)
            results.append({"file": str(md.relative_to(BASE_DIR)), "status": f"error: {exc}"})
            continue
        results.append(res)
        dur = res.get("seconds")
        dur_s = f"{int(dur // 60)}:{int(dur % 60):02d}" if dur else "—"
        print(f"    → {res['status']} {dur_s} {res.get('size_mb', '')} MB", flush=True)

    STATE.write_text(
        json.dumps({"updated": time.strftime("%Y-%m-%dT%H:%M:%S"), "results": results},
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_report(results)
    print(f"پایان در {time.time() - t0:.0f} ثانیه")
    return 0


def voices_make(engine: str):
    import voices

    return voices.make_backends(engine)


if __name__ == "__main__":
    sys.exit(main())
