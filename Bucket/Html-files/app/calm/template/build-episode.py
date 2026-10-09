#!/usr/bin/env python3
"""Build one calm/journey episode page from calm-journey-template.html.

The template is the single design source (colours, background, header, footer, controls,
canvas scenes). Only the episode data below is filled in; no design code is edited per episode.

Assets folder (--assets) must contain:
  NAME-01.mp3 .. NAME-06.mp3   the six narration+ambience parts, in order (mono, 64 kbps, 24 kHz)
  NAME-bg.jpg                  one vertical 9:16 background photo (light/dark is an overlay in the page)
Parts file (--parts): JSON list with exactly six section titles, in order.

Example (01-calm-forest):
  python3 build-episode.py --name 01-calm-forest --title "جنگل آرام" \
    --eyebrow "سفر صوتی آرامش / ۱" --english "Calm Forest Journey" \
    --desc "مراقبه در دل طبیعت کهن · ۶ بخش پیوسته" --disc-label "آرامش در جنگل" \
    --enso-label "حلقه ذن آرامش" --app-id cj-01 --scene mist+fireflies \
    --parts parts-01-calm-forest.json --assets ./assets --out 01-calm-forest.html
"""
import argparse
import base64
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, 'calm-journey-template.html')
UNSAFE = re.compile(r'["\'<>&\\{}]')


def data_uri(path, mime):
    with open(path, 'rb') as f:
        return f'data:{mime};base64,' + base64.b64encode(f.read()).decode('ascii')


def main():
    ap = argparse.ArgumentParser(description='Build a calm/journey episode HTML page.')
    ap.add_argument('--name', required=True, help='episode key, e.g. 01-calm-forest')
    ap.add_argument('--title', required=True, help='page title and main heading')
    ap.add_argument('--eyebrow', required=True, help='small line above the heading, e.g. "سفر صوتی آرامش / ۱"')
    ap.add_argument('--english', required=True, help='English line under the heading')
    ap.add_argument('--desc', required=True, help='description line under the heading')
    ap.add_argument('--disc-label', required=True, help='first text shown in the centre disc (before playback)')
    ap.add_argument('--enso-label', required=True, help='aria-label of the zen ring')
    ap.add_argument('--app-id', required=True, help='app id, e.g. cj-01')
    ap.add_argument('--scene', required=True, help='canvas scenes joined by +, e.g. mist+fireflies')
    ap.add_argument('--parts', required=True, help='JSON file: list of 6 section titles')
    ap.add_argument('--assets', required=True, help='folder with the 6 MP3 parts and the background JPG')
    ap.add_argument('--out', required=True, help='output HTML path')
    a = ap.parse_args()

    mp3s = sorted(glob.glob(os.path.join(a.assets, a.name + '-0[1-6].mp3')))
    if len(mp3s) != 6:
        raise SystemExit(f'expected 6 MP3 parts for {a.name}, found {len(mp3s)}')
    bg = os.path.join(a.assets, a.name + '-bg.jpg')
    if not os.path.isfile(bg):
        raise SystemExit(f'missing background: {bg}')
    with open(a.parts, encoding='utf-8') as f:
        parts = json.load(f)
    if not (isinstance(parts, list) and len(parts) == 6 and all(isinstance(p, str) and p.strip() for p in parts)):
        raise SystemExit('parts file must be a JSON list of exactly six non-empty strings')

    with open(TEMPLATE, encoding='utf-8') as f:
        h = f.read()
    h, n_note = re.subn(r'<!--TEMPLATE_NOTE.*?-->\n?', '', h, count=1, flags=re.S)
    assert n_note == 1, 'template note not found'

    text_values = {
        '{{NAME}}': a.name,
        '{{TITLE}}': a.title,
        '{{EYEBROW}}': a.eyebrow,
        '{{ENGLISH}}': a.english,
        '{{DESC}}': a.desc,
        '{{DISC_LABEL}}': a.disc_label,
        '{{ENSO_LABEL}}': a.enso_label,
        '{{APP_ID}}': a.app_id,
        '{{SCENE}}': a.scene,
    }
    for key, value in text_values.items():
        assert key in h, f'placeholder missing from template: {key}'
        assert not UNSAFE.search(value), f'unsafe character in value for {key}'
        h = h.replace(key, value)

    audio = ','.join(json.dumps(data_uri(p, 'audio/mpeg')) for p in mp3s)
    titles = ','.join(json.dumps(t, ensure_ascii=False) for t in parts)
    for key, value in (('{{AUDIO}}', audio), ('{{PART_TITLES}}', titles), ('{{BG}}', data_uri(bg, 'image/jpeg'))):
        assert h.count(key) == 1, f'{key} must appear exactly once in the template'
        h = h.replace(key, value)
    assert '{{' not in h, 'unfilled placeholder left in output'

    with open(a.out, 'w', encoding='utf-8') as f:
        f.write(h)
    print(f'wrote {a.out} ({len(h.encode("utf-8"))} bytes, {len(mp3s)} audio parts, 1 background)')


if __name__ == '__main__':
    main()
