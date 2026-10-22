#!/usr/bin/env python3
"""Validate the lesson HTML, embedded audio payloads, correction, and JavaScript."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    html_path = root / "prospect3-lesson-01.html"
    html = html_path.read_text(encoding="utf-8")
    binding = json.loads((root / "audio-bindings.json").read_text(encoding="utf-8"))["units"][0]
    progress = json.loads((root / "progress.json").read_text(encoding="utf-8"))
    embedded = [item for item in binding["sections"] if item["audio_status"] == "embedded"]
    pending = [item for item in binding["sections"] if item["audio_status"] != "embedded"]

    for section in embedded:
        section_id = section["section_id"]
        match = re.search(r'<audio\b[^>]*\bid="' + re.escape(section_id) + r'--audio"[^>]*\bsrc="data:audio/webm;base64,([^"]+)"', html)
        assert match, f"Missing embedded audio: {section_id}"
        raw = base64.b64decode(match.group(1), validate=True)
        assert hashlib.sha256(raw).hexdigest() == section["audio_sha256"], f"Hash mismatch: {section_id}"
        assert raw == (root / "audio" / section["audio_file"]).read_bytes(), f"Byte mismatch: {section_id}"
    for section in pending:
        match = re.search(r'<audio\b[^>]*\bid="' + re.escape(section["section_id"]) + r'--audio"[^>]*>', html)
        assert match and "data:audio/" not in match.group(0), f"Unexpected pending audio: {section['section_id']}"

    scripts = []
    node = shutil.which("node")
    with tempfile.TemporaryDirectory(prefix="g09-lesson-js-") as temporary:
        for index, match in enumerate(re.finditer(r"<script\b([^>]*)>(.*?)</script>", html, re.S | re.I)):
            attrs = match.group(1)
            if re.search(r'\btype="[^"]+"', attrs) or "src=" in attrs:
                continue
            result = {"script": index, "ok": None, "error": ""}
            if node:
                path = Path(temporary) / f"script-{index:02d}.js"
                path.write_text(match.group(2), encoding="utf-8")
                checked = subprocess.run([node, "--check", str(path)], capture_output=True, text=True)
                result.update(ok=checked.returncode == 0, error=checked.stderr.strip())
            scripts.append(result)
        assert all(item["ok"] is not False for item in scripts)

    new_sentence = "دوستی رو تصور کنین که وقتی درس رو نمی‌فهمم کمک می‌کنه و هنگام انتظار عصبانی نمی‌شه."
    old_sentence = "دوستی رو تصور کنین که وقتی درس رو نمی‌فهمید کمک می‌کند و هنگام انتظار عصبانی نمی‌شه."
    checked_sources = [
        html_path,
        root / "prospect3-lesson-01-tts.md",
        root / "prospect3-lesson-01-section-plan.json",
        root / "audio-bindings.json",
        root / "tts/prospect3-lesson-01/prospect3-lesson-01--start--8e15072791.md",
    ]
    report = {
        "html": {
            "bytes": html_path.stat().st_size,
            "sha256": hashlib.sha256(html_path.read_bytes()).hexdigest(),
            "audio_elements": len(re.findall(r"<audio\b", html)),
            "embedded_base64_audio": len(re.findall(r"data:audio/webm;base64,", html)),
            "base64_payloads_verified": len(embedded),
            "autoplay_attributes": len(re.findall(r"<audio\b[^>]*\bautoplay\b", html, re.I)),
            "preload_none": len(re.findall(r'<audio\b[^>]*\bpreload="none"', html)),
            "enabled_play_buttons": len(re.findall(r'<button type="button" data-audio-play=""(?![^>]*disabled)', html)),
            "disabled_play_buttons": len(re.findall(r'<button type="button" data-audio-play=""[^>]*disabled', html)),
        },
        "correction": {
            "new_spoken_in_section_tts": new_sentence in checked_sources[-1].read_text(encoding="utf-8"),
            "old_spoken_absent_from_active_sources": all(old_sentence not in path.read_text(encoding="utf-8") for path in checked_sources),
            "user_visible_sentence_updated": "وقتی درس را نمی‌فهمم کمک می‌کند" in html,
        },
        "javascript": {
            "node_available": bool(node),
            "checked_inline_scripts": len(scripts),
            "all_syntax_valid": all(item["ok"] is not False for item in scripts),
            "results": scripts,
        },
        "progress": progress,
    }
    total = len(binding["sections"])
    assert report["html"]["audio_elements"] == total
    assert report["html"]["embedded_base64_audio"] == len(embedded)
    assert report["html"]["autoplay_attributes"] == 0
    assert report["html"]["preload_none"] == total
    assert report["html"]["enabled_play_buttons"] == len(embedded)
    assert report["html"]["disabled_play_buttons"] == len(pending)
    assert len(embedded) == progress["embedded_sections"]
    assert len(pending) == progress["pending_sections_count"]
    assert report["javascript"]["all_syntax_valid"]
    assert all(report["correction"].values())
    (root / "qa-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"html": report["html"], "javascript_valid": True, "embedded": len(embedded), "pending": len(pending)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
