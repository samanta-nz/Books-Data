#!/usr/bin/env python3
"""Measure duration, volume, speech rate, and real silence intervals for a clip batch."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import imageio_ffmpeg


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    plan_path = args.plan.resolve()
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    report = {}
    for item in plan["clips"]:
        path = root / item["clip"]
        result = subprocess.run([
            ffmpeg, "-hide_banner", "-i", str(path), "-af",
            "silencedetect=noise=-45dB:d=0.25,volumedetect", "-f", "null", "-",
        ], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
        log = result.stdout
        match = re.search(r"Duration: (\d+):(\d+):(\d+(?:\.\d+)?)", log)
        duration = round(int(match.group(1)) * 3600 + int(match.group(2)) * 60 + float(match.group(3)), 3)
        silences = []
        active = None
        for line in log.splitlines():
            start = re.search(r"silence_start: (-?[\d.]+)", line)
            if start:
                active = float(start.group(1))
            end = re.search(r"silence_end: (-?[\d.]+) \| silence_duration: (-?[\d.]+)", line)
            if end and active is not None:
                silences.append({"start": round(active, 6), "end": round(float(end.group(1)), 6), "duration": round(float(end.group(2)), 6)})
                active = None
        speech = duration - sum(item["duration"] for item in silences)
        characters = len(re.sub(r"\s+", "", item["text"]))
        mean = re.search(r"mean_volume:\s*(-?[\d.]+) dB", log)
        maximum = re.search(r"max_volume:\s*(-?[\d.]+) dB", log)
        data = {
            "bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "duration": duration, "mean_volume_db": float(mean.group(1)),
            "max_volume_db": float(maximum.group(1)), "silences": silences,
            "speech_seconds": round(speech, 3), "nonwhitespace_characters": characters,
            "characters_per_speech_second": round(characters / speech, 2) if speech > 0 else None,
            "expected_segments": item["expected_segments"],
        }
        report[item["clip"]] = data
        print(f"{path.name} dur={duration:.2f}s rate={data['characters_per_speech_second']:.2f} mean={data['mean_volume_db']:.1f} max={data['max_volume_db']:.1f} silences={len(silences)} segments={item['expected_segments']}")
        if item["expected_segments"] > 1:
            for silence in silences:
                print("   ", silence)
    output = plan_path.with_name(plan_path.name.replace("generation-plan", "audio-analysis"))
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"analysis={output}")


if __name__ == "__main__":
    main()
