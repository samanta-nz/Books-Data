#!/usr/bin/env python3
"""Build one calm/journey episode page from calm-journey-template.html.

Inputs (in --assets):  NAME-01.mp3 .. NAME-06.mp3   (mono, 64 kbps, 24 kHz)
                       NAME-bg-light.webp, NAME-bg-dark.webp   (1080x1920)
Output (--out):        the finished single-file HTML page (audio and backgrounds embedded as data URIs)

Example:
  python3 build-episode.py --name 01-calm-forest --title "جنگل آرام" \
    --subtitle "حدود ۲۳ دقیقه • با صدای خانم" --app-id cj-01 --scene mist+fireflies \
    --enso-label "حلقه‌ی ذن جنگل" --assets ./assets --out 01-calm-forest.html
"""
import argparse
import base64
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, 'calm-journey-template.html')


def data_uri(path, mime):
    with open(path, 'rb') as f:
        return f'data:{mime};base64,' + base64.b64encode(f.read()).decode()


def main():
    ap = argparse.ArgumentParser(description='Build a calm/journey episode HTML page.')
    ap.add_argument('--name', required=True, help='episode key, e.g. 01-calm-forest')
    ap.add_argument('--title', required=True, help='page title and heading')
    ap.add_argument('--subtitle', required=True, help='line under the heading, e.g. "حدود ۲۳ دقیقه • با صدای خانم"')
    ap.add_argument('--app-id', required=True, help='app id, e.g. cj-01')
    ap.add_argument('--scene', required=True, help='canvas scenes joined by +, e.g. mist+fireflies')
    ap.add_argument('--enso-label', required=True, help='aria-label of the zen ring')
    ap.add_argument('--assets', required=True, help='folder with the 6 MP3 parts and the 2 WebP backgrounds')
    ap.add_argument('--out', required=True, help='output HTML path')
    a = ap.parse_args()

    mp3s = sorted(glob.glob(os.path.join(a.assets, a.name + '-0[1-6].mp3')))
    if len(mp3s) != 6:
        raise SystemExit(f'expected 6 MP3 parts for {a.name}, found {len(mp3s)}')
    light = os.path.join(a.assets, a.name + '-bg-light.webp')
    dark = os.path.join(a.assets, a.name + '-bg-dark.webp')
    for p in (light, dark):
        if not os.path.isfile(p):
            raise SystemExit(f'missing background: {p}')

    with open(TEMPLATE, encoding='utf-8') as f:
        h = f.read()
    h, n_note = re.subn(r'<!--TEMPLATE_NOTE.*?-->\n?', '', h, count=1, flags=re.S)
    assert n_note == 1, 'template note not found'

    values = {
        '{{NAME}}': a.name,
        '{{TITLE}}': a.title,
        '{{SUBTITLE}}': a.subtitle,
        '{{APP_ID}}': a.app_id,
        '{{SCENE}}': a.scene,
        '{{ENSO_LABEL}}': a.enso_label,
    }
    for key, value in values.items():
        assert key in h, f'placeholder missing from template: {key}'
        h = h.replace(key, value)

    audio = json.dumps([data_uri(p, 'audio/mpeg') for p in mp3s])
    h, n_audio = re.subn(r'const AUDIO=\[\];', lambda m: 'const AUDIO=' + audio + ';', h, count=1)
    bg = ('const BG={light:"' + data_uri(light, 'image/webp') + '",dark:"' + data_uri(dark, 'image/webp') + '"};')
    h, n_bg = re.subn(r'const BG=\{light:"",dark:""\};', lambda m: bg, h, count=1)
    assert n_audio == 1 and n_bg == 1, 'AUDIO or BG placeholder not found'
    assert '{{' not in h, 'unfilled placeholder left in output'

    with open(a.out, 'w', encoding='utf-8') as f:
        f.write(h)
    print(f'wrote {a.out} ({len(h.encode("utf-8"))} bytes, {len(mp3s)} audio parts)')


if __name__ == '__main__':
    main()
