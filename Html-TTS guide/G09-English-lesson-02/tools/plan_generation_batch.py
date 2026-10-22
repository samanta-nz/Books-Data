#!/usr/bin/env python3
"""Plan same-voice speech clips from registered lesson turns and pause markers."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

PAUSES = {"کوتاه": 700, "متوسط": 2000, "بلند": 8000}


def clean(value: str) -> str:
    value = re.sub(r"\[زبان: (?:fa|en)\]", "", value)
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"(?<=[A-Za-z])\s*’\s*s\b", "’s", value)
    return re.sub(r"\s+([.,!?])", r"\1", value)


def timeline(turn: dict) -> list[dict]:
    parts = re.split(r"\[مکث (کوتاه|متوسط|بلند)\]", turn["spoken"])
    result = []
    for index in range(0, len(parts), 2):
        text = clean(parts[index])
        if not text:
            continue
        marker = parts[index + 1] if index + 1 < len(parts) else None
        final = re.fullmatch(r"\[مکث (کوتاه|متوسط|بلند)\]", turn.get("pause") or "")
        pause = PAUSES[marker] if marker else (PAUSES[final.group(1)] if final else 0)
        result.append({
            "turn_id": turn["id"], "segment_index": len(result) + 1,
            "speaker": turn["speaker"], "text": text, "pause_after_ms": pause,
        })
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--batch", required=True)
    parser.add_argument("--sections", nargs="+", required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    sections = json.loads((root / "prospect3-lesson-02-section-plan.json").read_text(encoding="utf-8"))
    clips = []
    for section_id in args.sections:
        section = next(item for item in sections if item["section_id"] == section_id)
        grouped: dict[str, list[dict]] = {}
        for turn in section["tts_turns"]:
            grouped.setdefault(turn["speaker"], []).extend(timeline(turn))
        for speaker, segments in grouped.items():
            chunks = []
            current = []
            for segment in segments:
                candidate = current + [segment]
                size = len("\n\n".join(item["text"] for item in candidate))
                if current and size > 1500:
                    chunks.append(current)
                    current = [segment]
                else:
                    current = candidate
            if current:
                chunks.append(current)
            for chunk_index, chunk in enumerate(chunks, 1):
                tokens = []
                for segment in chunk:
                    match = re.search(r"turn-(\d+)$", segment["turn_id"])
                    token = match.group(1) if match else "instruction"
                    if token not in tokens:
                        tokens.append(token)
                role = "a" if speaker == "آرتین" else "r"
                suffix = f"-part-{chunk_index:02d}" if len(chunks) > 1 else ""
                filename = f"{section_id}-{role}-{'-'.join(tokens)}{suffix}.mp3"
                text = "\n\n".join(item["text"] for item in chunk)
                assert len(text) <= 1500
                clips.append({
                    "clip": "work/clips/" + filename, "section_id": section_id,
                    "speaker": speaker, "voice_id": "voice-02" if speaker == "آرتین" else "voice-05",
                    "turn_ids": list(dict.fromkeys(item["turn_id"] for item in chunk)),
                    "text": text, "characters": len(text),
                    "expected_segments": len(chunk), "segments": chunk,
                })
    output = root / "work" / f"batch-{args.batch}-generation-plan.json"
    if output.exists():
        raise SystemExit(f"Refusing to overwrite {output}")
    output.write_text(json.dumps({"batch": args.batch, "status": "planned", "sections": args.sections, "clips": clips}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for index, clip in enumerate(clips, 1):
        print(f"{index:02d} {Path(clip['clip']).name} chars={clip['characters']} segments={clip['expected_segments']} voice={clip['voice_id']}")
    print(f"clips={len(clips)} plan={output}")


if __name__ == "__main__":
    main()
