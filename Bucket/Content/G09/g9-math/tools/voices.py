"""موتورهای گفتار برای ساخت روایت درس‌ها.

هر بک‌اند یک متد ``synth(text) -> (numpy int16, sample_rate)`` دارد و یک
``signature`` که در کلید کش گفتار استفاده می‌شود.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

TOOLS_DIR = Path(__file__).resolve().parent
VOICES_DIR = TOOLS_DIR / "voices"

# --- تنظیم صداها -----------------------------------------------------------
PIPER_LENGTH_SCALE = 1.06   # کمی آهسته‌تر از پیش‌فرض، مناسب آموزش
SARNAZ_PITCH = 1.2225       # +۳٫۵ نیم‌پرده برای تنِ دانش‌آموز
SARNAZ_FORMANT = "shifted"


def _index() -> dict:
    path = VOICES_DIR / "index.json"
    if not path.exists():
        return {"voices": []}
    return json.loads(path.read_text(encoding="utf-8"))


def available() -> dict[str, dict]:
    return {f"{e['engine']}:{e['name']}": e for e in _index().get("voices", [])}


class Backend:
    sample_rate: int = 24000
    signature: str = "base"

    def synth(self, text: str) -> tuple[np.ndarray, int]:  # pragma: no cover
        raise NotImplementedError

    def close(self) -> None:
        pass


class StubBackend(Backend):
    """برای آزمون خط لوله؛ سکوت با طول تقریبی تولید می‌کند."""

    signature = "stub"

    def synth(self, text: str) -> tuple[np.ndarray, int]:
        seconds = max(0.6, len(text.split()) / 2.4)
        return np.zeros(int(seconds * self.sample_rate), dtype=np.int16), self.sample_rate


class PiperBackend(Backend):
    """صدای Piper؛ با pitch>1 و formant می‌توان تن صدا را تغییر داد."""

    def __init__(self, model: Path, config: Path, length_scale: float = PIPER_LENGTH_SCALE,
                 pitch: float = 1.0, formant: str = SARNAZ_FORMANT):
        from piper import PiperVoice

        self.voice = PiperVoice.load(str(model), config_path=str(config))
        self.length_scale = length_scale
        self.sample_rate = 22050
        self.pitch = pitch
        self.formant = formant
        self.signature = f"piper:{model.name}:ls{length_scale}:p{pitch}:{formant}"

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
        audio = np.concatenate(chunks)
        if self.pitch == 1.0:
            return audio, sr
        return _rubberband(audio, sr, self.pitch, self.formant), sr


class MmsBackend(Backend):
    def __init__(self, model: Path, vocab: Path, meta: Path):
        import onnxruntime as ort

        from mms_text import clean_for_mms

        self._clean = clean_for_mms
        self.vocab = json.loads(vocab.read_text(encoding="utf-8"))
        self.meta = json.loads(meta.read_text(encoding="utf-8"))
        self.sample_rate = int(self.meta["sampling_rate"])
        self.signature = f"mms:{model.name}"
        self.session = ort.InferenceSession(str(model), providers=["CPUExecutionProvider"])

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


def _rubberband(audio: np.ndarray, sr: int, pitch: float, formant: str) -> np.ndarray:
    """تغییر گام صدا با ffmpeg/rubberband (طول زمانی حفظ می‌شود)."""
    import subprocess
    import tempfile
    import wave

    from build import ffmpeg_exe

    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "in.wav"
        dst = Path(tmp) / "out.wav"
        with wave.open(str(src), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(audio.astype(np.int16).tobytes())
        subprocess.run(
            [ffmpeg_exe(), "-y", "-loglevel", "error", "-i", str(src),
             "-af", f"rubberband=pitch={pitch:.4f}:formant={formant}",
             "-ar", str(sr), "-ac", "1", str(dst)],
            check=True,
        )
        with wave.open(str(dst), "rb") as wf:
            data = wf.readframes(wf.getnframes())
    return np.frombuffer(data, dtype=np.int16)


def _pick(entries: dict[str, dict], preferred: list[str]) -> dict | None:
    for key in preferred:
        if key in entries:
            return entries[key]
    return None


def make_backends(engine: str = "auto") -> dict[str, Backend]:
    """بک‌اند فرسام (معلم) و سروناز (دانش‌آموز) را می‌سازد."""
    entries = available()
    if engine == "stub" or not entries:
        return {"farsam": StubBackend(), "sarnaz": StubBackend()}

    farsam_entry = _pick(entries, ["piper:amir", "piper:ganji_adabi", "piper:gyro"])
    sarnaz_entry = _pick(entries, ["mms:mms-fas"])

    if farsam_entry:
        farsam: Backend = PiperBackend(
            VOICES_DIR / farsam_entry["model"],
            VOICES_DIR / farsam_entry["config"],
        )
    else:
        farsam = StubBackend()

    if sarnaz_entry:
        sarnaz: Backend = MmsBackend(
            VOICES_DIR / sarnaz_entry["model"],
            VOICES_DIR / sarnaz_entry["vocab"],
            VOICES_DIR / sarnaz_entry["meta"],
        )
    elif farsam_entry:
        sarnaz = PiperBackend(
            VOICES_DIR / farsam_entry["model"],
            VOICES_DIR / farsam_entry["config"],
            pitch=SARNAZ_PITCH,
            formant=SARNAZ_FORMANT,
        )
    else:
        sarnaz = farsam
    return {"farsam": farsam, "sarnaz": sarnaz}
