#!/usr/bin/env python3
"""Update durable production progress without embedding intermediate Base64 HTML."""
from __future__ import annotations
import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    binding = json.loads((root / "audio-bindings.json").read_text(encoding="utf-8"))
    unit = binding["units"][0]
    sections = unit["sections"]
    produced = [item["section_id"] for item in sections if (root / "audio" / item["audio_file"]).is_file()]
    pending = [item["section_id"] for item in sections if item["section_id"] not in produced]
    embedded = [item["section_id"] for item in sections if item.get("audio_status") == "embedded"]
    status = "production_in_progress" if pending else ("ready_for_embedding" if len(embedded) < len(sections) else "complete")
    progress = {
        "lesson": unit["slug"], "status": status,
        "total_sections": len(sections),
        "total_source_turns": sum(len(item["tts_turns"]) for item in sections),
        "produced_sections": len(produced), "produced_section_ids": produced,
        "pending_production_count": len(pending), "pending_production": pending,
        "embedded_sections": len(embedded),
        "embedding_deferred_until_complete": len(embedded) < len(sections),
        "voices": {"آرتین": "voice-02", "رها": "voice-05"},
        "audio_format": "WebM Opus mono 48 kbps; Base64 embedding after production completes",
    }
    (root / "progress.json").write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(progress, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
