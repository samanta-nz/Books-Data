#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
link_section_audio.py — ساخت نسخهٔ سبک HTML که صدا را از پوشهٔ audio/ می‌خواند

نسخهٔ «امبد» (پوشهٔ html-with-audio) صدا را به Data URI تبدیل می‌کند و برای تحویل
آفلاین خوب است، ولی حجم فایل HTML را چند ده مگابایت می‌کند. این ابزار همان HTML
امبدشده را می‌گیرد و Data URI هر بخش را به مسیر نسبی فایل .weba برمی‌گرداند.

استفاده:
    python3 tools/link_section_audio.py \
        --html html-with-audio/ryazif01d01.html \
        --audio-dir audio --output-dir html-linked
"""

import argparse
import re
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--html", type=Path, required=True)
    ap.add_argument("--audio-dir", type=Path, default=Path("audio"))
    ap.add_argument("--output-dir", type=Path, default=Path("html-linked"))
    args = ap.parse_args()

    src = args.html.read_text(encoding="utf-8")

    # هر <audio ...> با data:audio/... را به مسیر فایل بر اساس data-audio-filename همان بخش
    count = 0

    def repl(match):
        nonlocal count
        tag = match.group(0)
        m = re.search(r'src="data:audio/[^"]+"', tag)
        if not m:
            return tag
        # نام فایل از نزدیک‌ترین data-audio-filename پیش از تگ پیدا می‌شود
        start = max(0, match.start() - 20000)
        window = src[start:match.start()]
        names = re.findall(r'data-audio-filename="([^"]+)"', window)
        if not names:
            return tag
        name = names[-1]
        path = args.audio_dir.name + "/" + name
        count += 1
        return tag.replace(m.group(0), f'src="{path}"')

    out = re.sub(r"<audio\b[^>]*>", repl, src)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    dst = args.output_dir / args.html.name
    dst.write_text(out, encoding="utf-8")
    print(f"{dst}  rewrote {count} players  size={dst.stat().st_size/1024/1024:.2f} MB")
    missing = [n for n in set(re.findall(r'data-audio-filename="([^"]+)"', src))
               if not (args.audio_dir / n).exists()]
    print(f"missing audio for {len(missing)} sections: {missing[:6]}")


if __name__ == "__main__":
    main()
