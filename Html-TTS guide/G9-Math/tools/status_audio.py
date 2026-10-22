#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
status_audio.py — گزارش وضعیت پوشش صدا برای یک درس

برای هر بخش از plan.json و پوشهٔ audio/ گزارش می‌دهد: چند قطعه لازم است، چند ساخته
شده، آیا فایل نهایی .weba وجود دارد و چه مدت است.

استفاده:
    python3 tools/status_audio.py --lesson ryazif01d01
"""

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--course-dir", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--lesson", default="ryazif01d01")
    ap.add_argument("--plan", type=Path, default=Path("plan.json"))
    ap.add_argument("--audio-dir", type=Path, default=Path("audio"))
    ap.add_argument("--clips-dir", type=Path, default=Path("clips"))
    ap.add_argument("--json", type=Path, default=Path("audio-status.json"))
    args = ap.parse_args()

    course = args.course_dir.resolve()
    plan = json.loads((course / args.plan).read_text(encoding="utf-8"))
    sections = plan["lessons"][args.lesson]["sections"]
    report = {"sections": []}
    # بخش‌هایی که با مسیر قدیمی (بدون plan) ساخته شده‌اند هم باید در گزارش بیایند
    legacy = {}
    rep_path = course / "build-report.json"
    if rep_path.exists():
        for s in json.loads(rep_path.read_text(encoding="utf-8")).get("sections", []):
            legacy[s["section"].replace(args.lesson + "--", "")] = s
    total_parts = done_parts = total_seconds = 0
    done_sections = 0

    for name in legacy:
        if name not in sections:
            sections[name] = {"parts": [], "legacy": True}

    for name, node in sections.items():
        parts = node["parts"]
        clips = course / args.clips_dir / f"{args.lesson}--{name}"
        if node.get("legacy"):
            have = parts
        else:
            have = [p for p in parts if (clips / f"p{p['i']:02d}.mp3").exists()]
        weba = course / args.audio_dir / f"{args.lesson}--{name}.weba"
        entry = {
            "section": name,
            "parts_required": len(parts) or legacy.get(name, {}).get("parts", 0),
            "parts_done": len(have),
            "complete": bool(node.get("legacy")) or len(have) == len(parts),
            "audio_file": weba.name if weba.exists() else None,
            "audio_seconds": (json.loads((course / "build-report.json").read_text(encoding="utf-8"))
                              if False else None),
        }
        if weba.exists():
            done_sections += 1
        report["sections"].append(entry)
        total_parts += len(parts)
        done_parts += len(have)

    rep = course / "build-report.json"
    if rep.exists():
        data = json.loads(rep.read_text(encoding="utf-8"))
        by = {s["section"].replace(args.lesson + "--", ""): s for s in data.get("sections", [])}
        for e in report["sections"]:
            s = by.get(e["section"])
            if s:
                e["audio_seconds"] = s.get("duration_seconds")
                e["audio_bytes"] = s.get("bytes")
                total_seconds += s.get("duration_seconds") or 0

    report["lesson"] = args.lesson
    report["sections_total"] = len(sections)
    report["sections_with_audio"] = done_sections
    report["parts_total"] = total_parts
    report["parts_done"] = done_parts
    report["audio_seconds_total"] = round(total_seconds, 1)
    (course / args.json).write_text(json.dumps(report, ensure_ascii=False, indent=1),
                                    encoding="utf-8")

    print(f"درس {args.lesson}: {done_sections}/{len(sections)} بخش دارای صدا · "
          f"قطعه‌ها {done_parts}/{total_parts} · {total_seconds/60:.1f} دقیقه صدا")
    print(f"{'بخش':16}{'قطعه':>12}{'صدا':>10}  وضعیت")
    for e in report["sections"]:
        mark = "✅" if e["complete"] else ("⏳" if e["parts_done"] else "—")
        secs = f"{e['audio_seconds']:.0f}s" if e.get("audio_seconds") else "-"
        print(f"{e['section']:16}{e['parts_done']:>5}/{e['parts_required']:<6}{secs:>10}  {mark}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
