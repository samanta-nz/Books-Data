"""موتورهای گفتار برای ساخت روایت درس‌ها.

هر بک‌اند یک متد ``synth(text) -> (numpy int16, sample_rate)`` دارد.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np

TOOLS_DIR = Path(__file__).resolve().parent
VOICES_DIR = TOOLS_DIR / "voices"

# تنظیم آهنگ صدا
PIPER_LENGTH_SCALE = 1.06   # کمی آهسته‌تر از پیش‌فرض، مناسب آموزش
MMS_NOISE = 0.60


def _index() -> dict:
    path = VOICES_DIR / "index.json"
    if not path.exists():
        return {"voices": []}
    return json.loads(path.read_text(encoding="utf-8"))


def available() -> dict[str, dict]:
    """نگاشت نام بک‌اند → اطلاعات مدل."""
    out: dict[str, dict] = {}
    for entry in _index().get("voices", []):
        out[f"{entry['engine']}:{entry['name']}"] = entry
    return out


class Backend:
    sample_rate: int = 24000

    def synth(self, text: str) -> tuple[np.ndarray, int]:  # pragma: no cover - abstract
        raise NotImplementedError

    def close(self) -> None:
        pass


class StubBackend(Backend):
    """برای آزمون خط لوله؛ سکوت با طول تقریبی تولید می‌کند."""

    def synth(self, text: str) -> tuple[np.ndarray, int]:
        seconds = max(0.6, len(text.split()) / 2.4)
        return np.zeros(int(seconds * self.sample_rate), dtype=np.int16), self.sample_rate


class PiperBackend(Backend):
    def __init__(self, model: Path, config: Path, length_scale: float = PIPER_LENGTH_SCALE):
        from piper import PiperVoice

        self.voice = PiperVoice.load(str(model), config_path=str(config))
        self.length_scale = length_scale
        self.sample_rate = 22050

    def synth(self, text: str) -> tuple[np.ndarray, int]:
        from piper import SynthesisConfig

        cfg = SynthesisConfig(length_scale=self.length_scale)
        chunks: list[np.ndarray] = []
        sr = self.sample_rate
        for chunk in self.voice.synthesize(text, syn_config=cfg):
            sr = chunk.sample_rate
            chunks.append(np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16))
        if not chunks:
            return np.zeros(0, dtype=np.int16), sr
        return np.concatenate(chunks), sr


class MmsBackend(Backend):
    def __init__(self, model: Path, vocab: Path, meta: Path):
        import onnxruntime as ort

        from mms_text import clean_for_mms

        self._clean = clean_for_mms
        self.vocab = json.loads(vocab.read_text(encoding="utf-8"))
        self.meta = json.loads(meta.read_text(encoding="utf-8"))
        self.sample_rate = int(self.meta["sampling_rate"])
        self.session = ort.InferenceSession(
            str(model), providers=["CPUExecutionProvider"]
        )

    def synth(self, text: str) -> tuple[np.ndarray, int]:
        cleaned = self._clean(text)
        ids = [self.vocab[c] for c in cleaned if c in self.vocab]
        if not ids:
            return np.zeros(0, dtype=np.int16), self.sample_rate
        feed = {
            "input_ids": np.array([ids], dtype=np.int64),
            "attention_mask": np.ones((1, len(ids)), dtype=np.int64),
        }
        audio = self.session.run(None, feed)[0].astype(np.float32).squeeze()
        audio = np.clip(audio, -1.0, 1.0)
        return (audio * 32767).astype(np.int16), self.sample_rate


def _pick(entries: dict[str, dict], preferred: list[str]) -> dict | None:
    for key in preferred:
        if key in entries:
            return entries[key]
    return None


def make_backends(engine: str = "auto") -> dict[str, Backend]:
    """بک‌اند فرسام (مرد) و سروناز (زن) را می‌سازد."""
    entries = available()
    if engine == "stub" or not entries:
        return {"farsam": StubBackend(), "sarnaz": StubBackend()}

    farsam_entry = _pick(
        entries,
        [
            "piper:ganji_adabi",
            "piper:amir",
            "piper:gyro",
        ],
    )
    sarnaz_entry = _pick(entries, ["mms:mms-fas"])

    farsam: Backend
    if farsam_entry:
        farsam = PiperBackend(
            VOICES_DIR / farsam_entry["model"],
            VOICES_DIR / farsam_entry["config"],
        )
    else:
        farsam = StubBackend()

    if sarnaz_entry:
        sarnaz = MmsBackend(
            VOICES_DIR / sarnaz_entry["model"],
            VOICES_DIR / sarnaz_entry["vocab"],
            VOICES_DIR / sarnaz_entry["meta"],
        )
    else:
        sarnaz = farsam
    return {"farsam": farsam, "sarnaz": sarnaz}
