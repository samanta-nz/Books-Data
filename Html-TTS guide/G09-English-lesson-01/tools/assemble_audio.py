#!/usr/bin/env python3
"""Assemble lesson-section WebM/Opus audio from generated speech clips."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess


def ffmpeg_path() -> str:
    configured = os.environ.get("FFMPEG")
    if configured:
        return configured
    found = shutil.which("ffmpeg")
    if found:
        return found
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError as exc:
        raise SystemExit("Set FFMPEG or install imageio-ffmpeg") from exc


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def probe_and_validate(ffmpeg: str, path: Path) -> dict:
    result = subprocess.run(
        [ffmpeg, "-hide_banner", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True,
    )
    log = result.stdout
    duration = None
    match = re.search(r"Duration: (\d+):(\d+):(\d+(?:\.\d+)?)", log)
    if match:
        hours, minutes, seconds = match.groups()
        duration = round(int(hours) * 3600 + int(minutes) * 60 + float(seconds), 3)
    mean = re.search(r"mean_volume:\s*(-?[\d.]+) dB", log)
    maximum = re.search(r"max_volume:\s*(-?[\d.]+) dB", log)
    if "Audio: opus" not in log:
        raise RuntimeError(f"Not an Opus audio file: {path}")
    if re.search(r"Stream .*Video:", log):
        raise RuntimeError(f"Unexpected video stream: {path}")
    if not maximum or float(maximum.group(1)) < -60:
        raise RuntimeError(f"Silent or invalid audio: {path}")
    return {
        "duration_seconds": duration,
        "codec": "opus",
        "container": "WebM",
        "channels": 1 if "mono" in log else None,
        "video": False,
        "mean_volume_db": float(mean.group(1)) if mean else None,
        "max_volume_db": float(maximum.group(1)) if maximum else None,
        "decodes_successfully": True,
    }


def assemble(ffmpeg: str, root: Path, output: Path, inputs: list[dict]) -> None:
    command = [ffmpeg, "-y", "-hide_banner", "-loglevel", "warning"]
    for item in inputs:
        source = (root / item["path"]).resolve()
        if not source.is_file():
            raise FileNotFoundError(source)
        command += ["-i", str(source)]
    filters = []
    labels = []
    for index, item in enumerate(inputs):
        label = f"a{index}"
        chain = []
        if item.get("trim_start_seconds") is not None or item.get("trim_end_seconds") is not None:
            params = []
            if item.get("trim_start_seconds") is not None:
                params.append(f"start={float(item['trim_start_seconds']):.6f}")
            if item.get("trim_end_seconds") is not None:
                params.append(f"end={float(item['trim_end_seconds']):.6f}")
            chain += ["atrim=" + ":".join(params), "asetpts=PTS-STARTPTS"]
        chain += ["aresample=24000", "aformat=sample_fmts=fltp:channel_layouts=mono"]
        pause_ms = int(item.get("pause_after_ms", 0))
        if pause_ms:
            chain += [f"apad=pad_dur={pause_ms / 1000:.3f}"]
        filters.append(f"[{index}:a]" + ",".join(chain) + f"[{label}]")
        labels.append(f"[{label}]")
    filters.append("".join(labels) + f"concat=n={len(inputs)}:v=0:a=1[out]")
    output.parent.mkdir(parents=True, exist_ok=True)
    command += [
        "-filter_complex", ";".join(filters), "-map", "[out]", "-vn",
        "-c:a", "libopus", "-b:a", "48k", "-f", "webm", str(output),
    ]
    subprocess.run(command, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    manifest_path = args.manifest.resolve()
    spec = json.loads(manifest_path.read_text(encoding="utf-8"))
    ffmpeg = ffmpeg_path()
    receipt_path = root / spec.get("receipt", "audio-receipt.json")
    existing = json.loads(receipt_path.read_text(encoding="utf-8")) if receipt_path.exists() else {}
    previous_batches = existing.get("batches") or ([existing["batch"]] if existing.get("batch") else [])
    receipt = {
        "batch": spec.get("batch"),
        "batches": previous_batches + [spec.get("batch")],
        "codec_settings": {"codec": "libopus", "bitrate": "48k", "channels": 1},
        "outputs": existing.get("outputs", []),
    }

    for item in spec["outputs"]:
        relative = Path(item["output"])
        output = (root / relative).resolve()
        assemble(ffmpeg, root, output, item["inputs"])
        metadata = probe_and_validate(ffmpeg, output)
        receipt["outputs"].append({
            "file": str(relative), "bytes": output.stat().st_size, "sha256": sha256(output),
            "inputs": item["inputs"], **metadata,
        })
        print(f"built {relative} ({metadata['duration_seconds']}s)")

    for item in spec.get("copies", []):
        source = (root / item["source"]).resolve()
        target_relative = Path(item["target"])
        target = (root / target_relative).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        metadata = probe_and_validate(ffmpeg, target)
        receipt["outputs"].append({
            "file": str(target_relative), "bytes": target.stat().st_size, "sha256": sha256(target),
            "reused_from": item["source"], **metadata,
        })
        print(f"reused {item['source']} -> {target_relative}")

    receipt["outputs"] = list({item["file"]: item for item in receipt["outputs"]}.values())
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"receipt {receipt_path}")


if __name__ == "__main__":
    main()
