"""دریافت و آماده‌سازی صداهای فارسی TTS — این اسکریپت در GitHub Actions اجرا می‌شود.

سندباکس به huggingface.co دسترسی ندارد؛ ولی runnerهای گیت‌هاب دارند.
نتیجهٔ کار (مدل‌های سبک‌شده) داخل همین پوشه کامیت می‌شود تا ساخت صدا
در سندباکس، بدون اینترنت و به‌صورت تکرارپذیر انجام شود.

صداها:
  * فرسام (معلم، مرد): Piper fa_IR  → ganji_adabi / amir
  * سروناز (دانش‌آموز، زن): MMS-TTS فارسی (facebook/mms-tts-fas) → ONNX
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VOICES = ROOT / "voices"
SAMPLES = VOICES / "samples"

PIPER_REPO = "rhasspy/piper-voices"
PIPER_VOICES = ["ganji_adabi", "amir", "gyro"]
MMS_REPO = "facebook/mms-tts-fas"

TEST_SENTENCE = (
    "سلام، من فرسام هستم. امروز با هم یاد می‌گیریم چرا هر عدد گویا را "
    "می‌شود به صورت کسری از دو عدد صحیح نوشت."
)


def log(msg: str) -> None:
    print(msg, flush=True)


# --------------------------------------------------------------------------- #
# Piper (صداهای مرد فارسی)
# --------------------------------------------------------------------------- #
def fetch_piper() -> list[dict]:
    from huggingface_hub import hf_hub_download

    out: list[dict] = []
    VOICES.mkdir(parents=True, exist_ok=True)
    for name in PIPER_VOICES:
        stem = f"fa_IR-{name}-medium"
        rel = f"fa/fa_IR/{name}/medium/{stem}"
        existing = VOICES / f"{stem}-int8.onnx"
        if existing.exists() and (VOICES / f"{stem}.onnx.json").exists():
            log(f"[piper] {name}: already present ({existing.stat().st_size / 1e6:.1f} MB)")
            out.append({
                "engine": "piper",
                "name": name,
                "model": existing.name,
                "config": f"{stem}.onnx.json",
                "bytes": existing.stat().st_size,
            })
            continue
        try:
            onnx_path = hf_hub_download(PIPER_REPO, f"{rel}.onnx")
            json_path = hf_hub_download(PIPER_REPO, f"{rel}.onnx.json")
        except Exception as exc:  # noqa: BLE001
            log(f"[piper] skip {name}: {exc}")
            continue
        dst_onnx = VOICES / f"{stem}.onnx"
        dst_json = VOICES / f"{stem}.onnx.json"
        shutil.copyfile(onnx_path, dst_onnx)
        shutil.copyfile(json_path, dst_json)
        entry = {
            "engine": "piper",
            "name": name,
            "model": dst_onnx.name,
            "config": dst_json.name,
            "bytes": dst_onnx.stat().st_size,
        }
        log(f"[piper] {name}: {entry['bytes'] / 1e6:.1f} MB")
        out.append(entry)

    # نسخهٔ سبک‌شدهٔ int8 برای حجم کمتر در گیت
    try:
        from onnxruntime.quantization import QuantType, quantize_dynamic

        for entry in list(out):
            src = VOICES / entry["model"]
            if src.stem.endswith("-int8"):
                continue
            dst = src.with_name(src.stem + "-int8.onnx")
            quantize_dynamic(str(src), str(dst), weight_type=QuantType.QInt8)
            entry["model_int8"] = dst.name
            entry["bytes_int8"] = dst.stat().st_size
            log(f"[piper-int8] {entry['name']}: {entry['bytes_int8'] / 1e6:.1f} MB")
            if entry["bytes_int8"] < entry["bytes"]:
                src.unlink()
                entry["model"] = dst.name
                entry.pop("model_int8", None)
                entry["bytes"] = entry.pop("bytes_int8")
            else:
                dst.unlink()
    except Exception as exc:  # noqa: BLE001
        log(f"[piper-int8] failed: {exc}")

    return out


# --------------------------------------------------------------------------- #
# MMS فارسی (صدای زن)
# --------------------------------------------------------------------------- #
def export_mms() -> dict | None:
    import torch
    from transformers import AutoTokenizer, VitsModel

    VOICES.mkdir(parents=True, exist_ok=True)
    log("[mms] downloading facebook/mms-tts-fas")
    model = VitsModel.from_pretrained(MMS_REPO).eval()
    tokenizer = AutoTokenizer.from_pretrained(MMS_REPO)

    class Wrapper(torch.nn.Module):
        def __init__(self, inner):  # noqa: ANN001
            super().__init__()
            self.inner = inner

        def forward(self, input_ids, attention_mask):  # noqa: ANN001
            return self.inner(input_ids=input_ids, attention_mask=attention_mask).waveform

    wrapper = Wrapper(model)
    vocab_size = int(getattr(model.config, "vocab_size", 0) or 0)
    if vocab_size <= 0:
        vocab_size = len(tokenizer)
    log(f"[mms] vocab_size={vocab_size} sr={model.config.sampling_rate}")
    dummy_ids = torch.randint(1, max(2, vocab_size - 1), (1, 24), dtype=torch.long)
    dummy_mask = torch.ones_like(dummy_ids)
    fp32_path = VOICES / "mms-fas.onnx"
    torch.onnx.export(
        wrapper,
        (dummy_ids, dummy_mask),
        str(fp32_path),
        input_names=["input_ids", "attention_mask"],
        output_names=["waveform"],
        dynamic_axes={
            "input_ids": {0: "batch", 1: "seq"},
            "attention_mask": {0: "batch", 1: "seq"},
            "waveform": {0: "batch", 1: "samples"},
        },
        opset_version=17,
        do_constant_folding=True,
        dynamo=False,
    )
    log(f"[mms] fp32 onnx {fp32_path.stat().st_size / 1e6:.1f} MB")

    # vocab توکنایزر برای اجرای مستقل در سندباکس
    vocab = tokenizer.get_vocab()
    (VOICES / "mms-fas.vocab.json").write_text(
        json.dumps(vocab, ensure_ascii=False), encoding="utf-8"
    )
    meta = {
        "repo": MMS_REPO,
        "sampling_rate": int(model.config.sampling_rate),
        "pad_token_id": int(model.config.pad_token_id),
        "vocab_size": len(vocab),
    }
    (VOICES / "mms-fas.meta.json").write_text(json.dumps(meta), encoding="utf-8")

    best = fp32_path
    candidates = [fp32_path]
    try:
        from onnxruntime.quantization import QuantType, quantize_dynamic

        int8_path = VOICES / "mms-fas-int8.onnx"
        quantize_dynamic(str(fp32_path), str(int8_path), weight_type=QuantType.QInt8)
        log(f"[mms] int8 onnx {int8_path.stat().st_size / 1e6:.1f} MB")
        candidates.append(int8_path)
    except Exception as exc:  # noqa: BLE001
        log(f"[mms-int8] failed: {exc}")

    try:
        from onnxconverter_common import float16

        fp16_path = VOICES / "mms-fas-fp16.onnx"
        model_fp16 = float16.convert_float_to_float16(
            __import__("onnx").load(str(fp32_path)), keep_io_types=True
        )
        __import__("onnx").save(model_fp16, str(fp16_path))
        log(f"[mms] fp16 onnx {fp16_path.stat().st_size / 1e6:.1f} MB")
        candidates.append(fp16_path)
    except Exception as exc:  # noqa: BLE001
        log(f"[mms-fp16] failed: {exc}")

    best = min(candidates, key=lambda p: p.stat().st_size)
    for path in candidates:
        if path != best:
            path.unlink(missing_ok=True)
    log(f"[mms] selected {best.name} ({best.stat().st_size / 1e6:.1f} MB)")

    return {
        "engine": "mms",
        "name": "mms-fas",
        "model": best.name,
        "vocab": "mms-fas.vocab.json",
        "meta": "mms-fas.meta.json",
        "bytes": best.stat().st_size,
        "sampling_rate": meta["sampling_rate"],
    }


# --------------------------------------------------------------------------- #
# نمونهٔ صوتی برای کنترل شنیداری
# --------------------------------------------------------------------------- #
def make_samples(entries: list[dict]) -> None:
    import subprocess
    import wave

    import numpy as np

    SAMPLES.mkdir(parents=True, exist_ok=True)
    sample_txt = VOICES / "sample.txt"
    sample_txt.write_text(TEST_SENTENCE, encoding="utf-8")

    # piper
    for entry in entries:
        if entry["engine"] != "piper":
            continue
        out_wav = SAMPLES / f"{entry['name']}.wav"
        model = VOICES / entry["model"]
        cfg = VOICES / entry["config"]
        try:
            from piper import PiperVoice

            voice = PiperVoice.load(str(model), config_path=str(cfg))
            with wave.open(str(out_wav), "wb") as wf:
                voice.synthesize_wav(TEST_SENTENCE, wf)
            log(f"[sample] {out_wav.name} ok")
        except Exception as exc:  # noqa: BLE001
            log(f"[sample] piper {entry['name']} failed: {exc}")

    # mms
    mms = next((e for e in entries if e["engine"] == "mms"), None)
    if mms:
        try:
            import onnxruntime as ort

            from mms_text import clean_for_mms

            vocab = json.loads((VOICES / mms["vocab"]).read_text(encoding="utf-8"))
            meta = json.loads((VOICES / mms["meta"]).read_text(encoding="utf-8"))
            ids = [vocab[c] for c in clean_for_mms(TEST_SENTENCE) if c in vocab]
            ids = ids or [meta["pad_token_id"]]
            sess = ort.InferenceSession(str(VOICES / mms["model"]), providers=["CPUExecutionProvider"])
            feed = {
                "input_ids": np.array([ids], dtype=np.int64),
                "attention_mask": np.ones((1, len(ids)), dtype=np.int64),
            }
            audio = sess.run(None, feed)[0].squeeze()
            sr = meta["sampling_rate"]
            pcm = (np.clip(audio, -1, 1) * 32767).astype("<i2")
            wav_path = SAMPLES / "mms-fas.wav"
            with wave.open(str(wav_path), "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sr)
                wf.writeframes(pcm.tobytes())
            log(f"[sample] mms-fas.wav ok ({sr} Hz)")
        except Exception as exc:  # noqa: BLE001
            log(f"[sample] mms failed: {exc}")

    for wav_path in SAMPLES.glob("*.wav"):
        mp3 = wav_path.with_suffix(".mp3")
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav_path),
             "-codec:a", "libmp3lame", "-b:a", "64k", str(mp3)],
            check=False,
        )
        if mp3.exists():
            wav_path.unlink()
            log(f"[sample] {mp3.name} {mp3.stat().st_size / 1024:.0f} KB")


def main() -> int:
    VOICES.mkdir(parents=True, exist_ok=True)
    entries: list[dict] = []
    try:
        entries += fetch_piper()
    except Exception:  # noqa: BLE001
        log("[piper] fatal:\n" + traceback.format_exc())
    try:
        mms = export_mms()
        if mms:
            entries.append(mms)
    except Exception:  # noqa: BLE001
        log("[mms] fatal:\n" + traceback.format_exc())

    try:
        make_samples(entries)
    except Exception:  # noqa: BLE001
        log("[sample] fatal:\n" + traceback.format_exc())

    (VOICES / "index.json").write_text(
        json.dumps({"voices": entries}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    log("[done] " + json.dumps([{k: e[k] for k in ("engine", "name", "model")} for e in entries], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
