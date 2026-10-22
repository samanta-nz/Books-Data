#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analyze_voice.py — توصیف و مقایسهٔ آکوستیکی نمونه‌های صوتی

استفاده:
    python3 analyze_voice.py file1.mp3 [file2.mp3 ...]

خروجی برای هر فایل:
    - مدت، نرخ نمونه‌برداری، بیت‌ریت
    - فرکانس پایه (F0): میانه، میانگین، صدک ۵ و ۹۵  → محدودهٔ زیر و بمی
    - نسبت گفتار به سکوت و برآورد سرعت هجا در ثانیه
    - مرکز طیفی (روشنی صدا)

اگر دو فایل داده شود، شباهت آکوستیکی آن‌ها هم چاپ می‌شود (۰ تا ۱).

نیازمندی:  pip install imageio-ffmpeg numpy
"""

import json
import subprocess
import sys
import tempfile
import wave

import numpy as np

SR = 16000          # نرخ نمونه‌برداری برای تحلیل
FRAME = int(0.040 * SR)   # پنجرهٔ ۴۰ میلی‌ثانیه
HOP = int(0.010 * SR)     # گام ۱۰ میلی‌ثانیه
F0_MIN, F0_MAX = 60, 400  # بازهٔ جست‌وجوی فرکانس پایه (هرتز)


def ffmpeg_exe() -> str:
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def decode(path: str):
    """فایل صوتی را به مونو 16kHz شناور تبدیل می‌کند و متادیتا برمی‌گرداند."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav_path = tmp.name
    subprocess.run(
        [ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y",
         "-i", path, "-ac", "1", "-ar", str(SR), "-f", "wav", wav_path],
        check=True,
    )
    with wave.open(wav_path, "rb") as w:
        sr = w.getframerate()
        n = w.getnframes()
        raw = w.readframes(n)
    audio = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
    return audio, sr, n / float(sr)


def probe(path: str) -> dict:
    """مدت و مشخصات جریان را از خود ffmpeg می‌خواند."""
    out = subprocess.run(
        [ffmpeg_exe(), "-hide_banner", "-i", path],
        capture_output=True, text=True,
    ).stderr
    info = {}
    for line in out.splitlines():
        low = line.lower()
        if "duration:" in low:
            info["duration"] = line.split("Duration:")[1].split(",")[0].strip()
        if "bitrate:" in low and "duration" in low:
            info["bitrate"] = line.split("bitrate:")[1].strip()
        if "stream #" in low and "audio:" in low:
            info["stream"] = line.split("Audio:")[1].strip()
    return info


def frames(audio: np.ndarray):
    count = max(0, 1 + (len(audio) - FRAME) // HOP)
    for i in range(count):
        yield audio[i * HOP: i * HOP + FRAME]


def f0_track(audio: np.ndarray) -> np.ndarray:
    """فرکانس پایهٔ هر فریم با خودهمبستگی نرمال‌شده."""
    lag_min, lag_max = int(SR / F0_MAX), int(SR / F0_MIN)
    track = []
    for fr in frames(audio):
        x = fr - fr.mean()
        e = float(np.dot(x, x))
        if e < 1e-6:                      # سکوت
            track.append(0.0)
            continue
        ac = np.correlate(x, x, mode="full")[len(x) - 1:]
        if lag_max >= len(ac):
            track.append(0.0)
            continue
        seg = ac[lag_min:lag_max]
        if not len(seg):
            track.append(0.0)
            continue
        lag = int(np.argmax(seg)) + lag_min
        strength = ac[lag] / (ac[0] + 1e-12)
        track.append(SR / lag if strength > 0.30 else 0.0)
    return np.array(track, dtype=np.float32)


def rms_track(audio: np.ndarray) -> np.ndarray:
    return np.array([float(np.sqrt(np.mean(fr.astype(np.float64) ** 2))) for fr in frames(audio)])


def spectral_centroid(audio: np.ndarray) -> float:
    vals = []
    win = np.hanning(FRAME)
    for fr in frames(audio):
        spec = np.abs(np.fft.rfft(fr * win))
        s = spec.sum()
        if s > 1e-6:
            freqs = np.fft.rfftfreq(len(fr), 1.0 / SR)
            vals.append(float((spec * freqs).sum() / s))
    return float(np.mean(vals)) if vals else 0.0


def estimate_syllable_rate(audio: np.ndarray, rms: np.ndarray) -> float:
    """برآورد نرخ هجا از قله‌های انرژی در بازه‌های گفتاری."""
    if not len(rms):
        return 0.0
    thr = max(0.12 * float(rms.max()), 0.004)
    active = rms > thr
    voiced_time = float(active.sum()) * (HOP / SR)
    peaks, last = 0, -3
    for i, v in enumerate(active):
        if v and rms[i] >= rms[max(0, i - 1)] and rms[i] >= rms[min(len(rms) - 1, i + 1)]:
            if i - last >= 3:            # حداقل ۳۰ میلی‌ثانیه فاصله
                peaks += 1
                last = i
    return peaks / voiced_time if voiced_time > 0 else 0.0


def analyze(path: str) -> dict:
    audio, sr, dur = decode(path)
    f0 = f0_track(audio)
    voiced = f0[f0 > 0]
    rms = rms_track(audio)
    meta = probe(path)
    return {
        "file": path,
        "duration_s": round(dur, 2),
        "stream": meta.get("stream", ""),
        "bitrate": meta.get("bitrate", ""),
        "voiced_ratio": round(float(len(voiced)) / max(1, len(f0)), 3),
        "f0_median": round(float(np.median(voiced)), 1) if len(voiced) else 0.0,
        "f0_mean": round(float(np.mean(voiced)), 1) if len(voiced) else 0.0,
        "f0_p05": round(float(np.percentile(voiced, 5)), 1) if len(voiced) else 0.0,
        "f0_p25": round(float(np.percentile(voiced, 25)), 1) if len(voiced) else 0.0,
        "f0_p75": round(float(np.percentile(voiced, 75)), 1) if len(voiced) else 0.0,
        "f0_p95": round(float(np.percentile(voiced, 95)), 1) if len(voiced) else 0.0,
        "f0_std": round(float(np.std(voiced)), 1) if len(voiced) else 0.0,
        "spectral_centroid_hz": round(spectral_centroid(audio), 1),
        "syllables_per_sec": round(estimate_syllable_rate(audio, rms), 2),
        "_f0": voiced,
    }


def similarity(a: dict, b: dict) -> dict:
    """شباهت ساده بر پایهٔ میانهٔ F0، پراکندگی، مرکز طیفی و سرعت هجا."""
    def rel(x, y):
        m = max(abs(x), abs(y), 1e-9)
        return 1.0 - min(1.0, abs(x - y) / m)

    parts = {
        "pitch": rel(a["f0_median"], b["f0_median"]),
        # دامنهٔ زیر و بمی با چارک‌ها سنجیده می‌شود (IQR) تا خطای اکتاو روی صدک ۹۵ آن را خراب نکند
        "pitch_range": rel(a["f0_p75"] - a["f0_p25"], b["f0_p75"] - b["f0_p25"]),
        "brightness": rel(a["spectral_centroid_hz"], b["spectral_centroid_hz"]),
        "rate": rel(a["syllables_per_sec"], b["syllables_per_sec"]),
    }
    parts["overall"] = round(float(np.mean(list(parts.values()))), 3)
    return {k: round(v, 3) for k, v in parts.items()}


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    results = [analyze(p) for p in argv[1:]]
    clean = [{k: v for k, v in r.items() if not k.startswith("_")} for r in results]
    print(json.dumps(clean, ensure_ascii=False, indent=2))
    if len(results) == 2:
        print("\nشباهت آکوستیکی:", json.dumps(similarity(*results), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
