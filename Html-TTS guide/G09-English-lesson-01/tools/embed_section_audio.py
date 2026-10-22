#!/usr/bin/env python3
"""Embed available section WebM audio as Base64 without enabling autoplay."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
import re

READY = "صوت این بخش آمادهٔ پخش است."


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    html_path = root / "prospect3-lesson-01.html"
    binding_path = root / "audio-bindings.json"
    html = html_path.read_text(encoding="utf-8")
    bindings = json.loads(binding_path.read_text(encoding="utf-8"))
    unit = next(item for item in bindings["units"] if item["slug"] == "prospect3-lesson-01")
    audio_receipt_path = root / "audio-receipt.json"
    audio_receipt = json.loads(audio_receipt_path.read_text(encoding="utf-8")) if audio_receipt_path.exists() else {"outputs": []}
    audio_metadata = {item["file"]: item for item in audio_receipt["outputs"]}
    replacements = []
    embedded = []

    for section in unit["sections"]:
        section_id = section["section_id"]
        relative_audio = "audio/" + section["audio_file"]
        audio_path = root / relative_audio
        if not audio_path.is_file():
            continue
        audio_bytes = audio_path.read_bytes()
        if not audio_bytes.startswith(b"\x1a\x45\xdf\xa3"):
            raise RuntimeError(f"Not a WebM file: {audio_path}")
        audio_match = re.search(r'<audio\b[^>]*\bid="' + re.escape(section_id) + r'--audio"[^>]*>', html)
        if not audio_match:
            raise RuntimeError(f"Audio element not found: {section_id}")
        panel_start = html.rfind('<div class="section-player"', 0, audio_match.start())
        if panel_start < 0:
            raise RuntimeError(f"Player not found: {section_id}")
        panel_end = html.find(">", panel_start) + 1
        panel_tag = html[panel_start:panel_end]
        new_panel_tag = re.sub(r'data-audio-state="[^"]*"', 'data-audio-state="embedded"', panel_tag)
        if new_panel_tag == panel_tag and 'data-audio-state="embedded"' not in panel_tag:
            raise RuntimeError(f"Audio state missing: {section_id}")
        replacements.append((panel_start, panel_end, new_panel_tag))

        audio_tag = audio_match.group(0)
        audio_tag = re.sub(r'\s+src="[^"]*"', "", audio_tag)
        uri = "data:audio/webm;base64," + base64.b64encode(audio_bytes).decode("ascii")
        new_audio_tag = audio_tag[:-1] + ' src="' + uri + '">'
        replacements.append((audio_match.start(), audio_match.end(), new_audio_tag))

        audio_close = html.find("</audio>", audio_match.end())
        position_start = html.find('<p class="section-position"', audio_close)
        if audio_close < 0 or position_start < 0:
            raise RuntimeError(f"Player controls not found: {section_id}")
        controls = html[audio_close:position_start]
        for button in re.finditer(r"<button\b[^>]*>", controls):
            old = button.group(0)
            new = re.sub(r'\s+disabled(?:="[^"]*")?', "", old)
            replacements.append((audio_close + button.start(), audio_close + button.end(), new))
        status = re.search(r'<p class="section-audio-status"[^>]*>.*?</p>', controls, re.S)
        if not status:
            raise RuntimeError(f"Audio status not found: {section_id}")
        new_status = re.sub(r">.*</p>", ">" + READY + "</p>", status.group(0), flags=re.S)
        replacements.append((audio_close + status.start(), audio_close + status.end(), new_status))
        embedded.append((section, relative_audio, audio_path, audio_bytes))

    for start, end, value in sorted(replacements, key=lambda item: item[0], reverse=True):
        html = html[:start] + value + html[end:]

    map_match = re.search(r'(<script type="application/json" id="section-audio-map">)(.*?)(</script>)', html, re.S)
    if not map_match:
        raise RuntimeError("section-audio-map not found")
    section_map = json.loads(map_match.group(2))
    embedded_ids = {section["section_id"] for section, _, _, _ in embedded}
    for item in section_map:
        if item["section_id"] in embedded_ids:
            item["audio_status"] = "embedded"
    new_map = json.dumps(section_map, ensure_ascii=False)
    html = html[:map_match.start(2)] + new_map + html[map_match.end(2):]
    html_path.write_text(html, encoding="utf-8")

    # Verify every embedded payload by decoding it back from the final HTML.
    verification = []
    for section, relative_audio, audio_path, original_bytes in embedded:
        section_id = section["section_id"]
        match = re.search(r'<audio\b[^>]*\bid="' + re.escape(section_id) + r'--audio"[^>]*\bsrc="data:audio/webm;base64,([^"]+)"[^>]*>', html)
        if not match:
            raise RuntimeError(f"Embedded payload missing after write: {section_id}")
        decoded = base64.b64decode(match.group(1), validate=True)
        if decoded != original_bytes:
            raise RuntimeError(f"Base64 payload mismatch: {section_id}")
        section["audio_status"] = "embedded"
        section["audio_sha256"] = sha256_bytes(original_bytes)
        section["audio_bytes"] = len(original_bytes)
        verification.append({
            "section_id": section_id,
            "audio_file": section["audio_file"],
            "bytes": len(original_bytes),
            "sha256": sha256_bytes(original_bytes),
            "base64_verified": True,
            "duration_seconds": audio_metadata.get(relative_audio, {}).get("duration_seconds"),
        })

    if len(re.findall(r"<audio\b", html)) != len(unit["sections"]):
        raise RuntimeError("Unexpected audio element count")
    if len(re.findall(r'data-audio-state="embedded"', html)) != len(embedded):
        raise RuntimeError("Unexpected embedded state count")
    if re.search(r"<audio\b[^>]*\bautoplay\b", html, re.I):
        raise RuntimeError("Autoplay is not allowed")
    if len(re.findall(r'<audio\b[^>]*\bpreload="none"', html)) != len(unit["sections"]):
        raise RuntimeError("Every audio element must retain preload=none")

    bindings["status"] = "AUDIO_PRODUCTION_IN_PROGRESS" if len(embedded) < len(unit["sections"]) else "AUDIO_EMBEDDED"
    bindings["embedded_html_sha256"] = sha256_bytes(html.encode("utf-8"))
    binding_path.write_text(json.dumps(bindings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pending = [section["section_id"] for section in unit["sections"] if section["section_id"] not in embedded_ids]
    receipt = {
        "html": html_path.name,
        "html_bytes": html_path.stat().st_size,
        "html_sha256": sha256_bytes(html.encode("utf-8")),
        "mime": "audio/webm",
        "base64_verified": True,
        "autoplay": False,
        "preload": "none",
        "embedded_count": len(embedded),
        "pending_count": len(pending),
        "embedded": verification,
        "pending_sections": pending,
    }
    (root / "embedding-receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    progress = {
        "lesson": "prospect3-lesson-01",
        "status": "partial" if pending else "complete",
        "total_sections": len(unit["sections"]),
        "total_source_turns": sum(len(section["tts_turns"]) for section in unit["sections"]),
        "embedded_sections": len(embedded),
        "pending_sections_count": len(pending),
        "pending_sections": pending,
        "voices": {"آرتین": "voice-02", "رها": "voice-05"},
        "audio_format": "WebM Opus mono 48 kbps, Base64 embedded",
        "non_intrusive": {"autoplay": False, "preload": "none", "user_initiated_playback": True},
    }
    (root / "progress.json").write_text(json.dumps(progress, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(progress, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
