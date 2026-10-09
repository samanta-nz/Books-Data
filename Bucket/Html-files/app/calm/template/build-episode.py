#!/usr/bin/env python3
"""Build calm/journey episode pages from calm-journey-template.html.

The template is the single design source (colours, background, header, footer, controls,
canvas scenes). Each episode only fills in its data; no design code is edited per episode.

Modes:
  audio (default)  NAME-01.mp3 .. NAME-06.mp3 are embedded as data URIs (six parts).
  --no-audio       nothing is embedded: the play and skip controls stay disabled and the page
                   shows "صدای این تمرین هنوز اضافه نشده است." until the MP3 parts are added.
  --batch FILE     builds every record of a JSON list in no-audio mode
                   (episodes-no-audio.json). A record may carry its own dark palette.

Assets folder (--assets) must contain:
  NAME-bg.jpg                  one vertical 9:16 background photo (the dark overlay is in the page)
  NAME-01.mp3 .. NAME-06.mp3   audio mode only (mono, 64 kbps, 24 kHz)
Parts file (--parts): JSON list of section titles, in order.
--palette FILE (optional): JSON object with bg1, bg2, fg, accent, accent2 (hex colours, from the
  episode guide's dark palette). Without it the template's forest-green palette is kept.

Example (01-calm-forest, with audio):
  python3 build-episode.py --name 01-calm-forest --title "جنگل آرام" \
    --eyebrow "سفر صوتی آرامش / ۱" --english "Calm Forest Journey" \
    --desc "مراقبه در دل طبیعت کهن · ۶ بخش پیوسته" --disc-label "آرامش در جنگل" \
    --enso-label "حلقه ذن آرامش" --app-id cj-01 --scene mist \
    --parts parts-01-calm-forest.json --assets ./assets --out 01-calm-forest.html

Example (pages 02-12, no audio):
  python3 build-episode.py --batch episodes-no-audio.json --assets ASSETS_DIR --out-dir ../journey
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
AUDIO_NOTE = 'audio: embedded HQ MP3 (narration + ambience)'
NO_AUDIO_NOTE = 'audio: none yet (built without audio)'
BG_NOTE = 'background: embedded JPEG (dark overlay in CSS)'
PLACEHOLDER_NOTE = 'background: TEMPORARY gradient placeholder, replace with the guide image'


def data_uri(path, mime):
    with open(path, 'rb') as f:
        return f'data:{mime};base64,' + base64.b64encode(f.read()).decode('ascii')


def hex_rgb(value):
    h = str(value).strip().lstrip('#')
    if not re.fullmatch(r'[0-9A-Fa-f]{6}', h):
        raise SystemExit(f'not a six-digit hex colour: {value!r}')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def to_hex(c):
    return '#%02x%02x%02x' % tuple(int(round(x)) for x in c)


def to_csv(c):
    return ', '.join(str(int(round(x))) for x in c)


def mix(a, b, t):
    """Colour a, moved t of the way towards colour b."""
    return tuple(x * (1 - t) + y * t for x, y in zip(a, b))


def palette_values(p):
    """Each colour literal of the template mapped to this episode's colour."""
    bg1, bg2 = hex_rgb(p['bg1']), hex_rgb(p['bg2'])
    fg, a1, a2 = hex_rgb(p['fg']), hex_rgb(p['accent']), hex_rgb(p['accent2'])
    return {
        'hsl(155 45% 7%)': to_hex(bg1),                  # --bg1
        'hsl(165 55% 4%)': to_hex(bg2),                  # --bg2
        'hsl(135 25% 95%)': to_hex(fg),                  # --fg
        'hsl(140 18% 75%)': to_hex(mix(fg, bg1, 0.28)),  # --mut
        '#52c285': to_hex(a1),                           # --accent
        '#84d896': to_hex(a2),                           # --accent2
        '82, 194, 133': to_csv(a1),                      # --fx1 and every accent rgba()
        '132, 216, 150': to_csv(a2),                     # --fx2
        '12, 28, 19': to_csv(bg1),                       # --card glass tint
        '8, 20, 14': to_csv(bg1),                        # --bg-ov (image overlay)
        '16, 36, 25': to_csv(mix(bg1, bg2, 0.5)),        # --surface
        '#0c1420': to_hex(bg1),                          # theme-color
        # enso ring: gradient stops, outer guide, secondary stroke, moss nodes, leaf
        'hsl(145, 55%, 32%)': to_hex(mix(a1, bg1, 0.25)),
        'hsl(152, 65%, 24%)': to_hex(mix(a2, bg1, 0.25)),
        'hsl(140, 50%, 18%)': to_hex(mix(a1, bg2, 0.45)),
        'hsl(155, 60%, 28%)': to_hex(mix(a2, bg2, 0.35)),
        'hsl(145, 45%, 18%)': to_hex(mix(bg1, a1, 0.15)),
        'hsl(140, 50%, 10%)': to_hex(bg2),
        'hsl(145, 45%, 25%)': to_hex(mix(bg1, a1, 0.35)),
        'hsl(148, 50%, 22%)': to_hex(mix(bg1, a2, 0.35)),
        'hsl(142, 55%, 35%)': to_hex(mix(a1, a2, 0.10)),
        'hsl(142, 50%, 28%)': to_hex(mix(a1, a2, 0.40)),
        'hsl(142, 52%, 32%)': to_hex(mix(a1, a2, 0.20)),
        'hsl(145, 55%, 30%)': to_hex(mix(a1, a2, 0.30)),
        'hsl(140, 50%, 32%)': to_hex(mix(a1, a2, 0.60)),
    }


def apply_palette(html, palette):
    values = palette_values(palette)
    for literal in values:
        if html.count(literal) < 1:
            raise SystemExit(f'template colour not found, palette cannot be applied: {literal}')
    pattern = re.compile('|'.join(re.escape(k) for k in sorted(values, key=len, reverse=True)))
    return pattern.sub(lambda m: values[m.group(0)], html)


def build_page(*, name, title, eyebrow, english, desc, disc_label, enso_label, app_id, scene,
               parts, assets, out, no_audio, palette=None, placeholder=False):
    if no_audio:
        mp3s = []
    else:
        mp3s = sorted(glob.glob(os.path.join(assets, name + '-0[1-6].mp3')))
        if len(mp3s) != 6:
            raise SystemExit(f'expected 6 MP3 parts for {name}, found {len(mp3s)}')
    bg = os.path.join(assets, name + '-bg.jpg')
    if not os.path.isfile(bg):
        raise SystemExit(f'missing background: {bg}')
    if not (isinstance(parts, list) and all(isinstance(p, str) and p.strip() for p in parts)):
        raise SystemExit(f'{name}: parts must be a list of non-empty titles')
    expected = (5, 6) if no_audio else (6,)
    if len(parts) not in expected:
        raise SystemExit(f'{name}: expected {expected} part titles, got {len(parts)}')
    if len(parts) != 6:
        print(f'WARNING {name}: {len(parts)} part titles (the guide has {len(parts)} headings), not 6')

    with open(TEMPLATE, encoding='utf-8') as f:
        h = f.read()
    h, n_note = re.subn(r'<!--TEMPLATE_NOTE.*?-->\n?', '', h, count=1, flags=re.S)
    assert n_note == 1, 'template note not found'
    if palette:
        h = apply_palette(h, palette)
    if no_audio:
        assert h.count(AUDIO_NOTE) == 1, 'audio note not found in template'
        h = h.replace(AUDIO_NOTE, NO_AUDIO_NOTE)
    if placeholder:
        assert h.count(BG_NOTE) == 1, 'background note not found in template'
        h = h.replace(BG_NOTE, PLACEHOLDER_NOTE)

    text_values = {
        '{{NAME}}': name,
        '{{TITLE}}': title,
        '{{EYEBROW}}': eyebrow,
        '{{ENGLISH}}': english,
        '{{DESC}}': desc,
        '{{DISC_LABEL}}': disc_label,
        '{{ENSO_LABEL}}': enso_label,
        '{{APP_ID}}': app_id,
        '{{SCENE}}': scene,
    }
    for key, value in text_values.items():
        assert key in h, f'placeholder missing from template: {key}'
        assert not UNSAFE.search(value), f'unsafe character in value for {key}'
        h = h.replace(key, value)

    audio = ','.join(json.dumps(data_uri(p, 'audio/mpeg')) for p in mp3s)
    titles = ','.join(json.dumps(t, ensure_ascii=False) for t in parts)
    for key, value in (('{{AUDIO}}', audio), ('{{PART_TITLES}}', titles),
                       ('{{BG}}', data_uri(bg, 'image/jpeg'))):
        assert h.count(key) == 1, f'{key} must appear exactly once in the template'
        h = h.replace(key, value)
    assert '{{' not in h, 'unfilled placeholder left in output'

    with open(out, 'w', encoding='utf-8') as f:
        f.write(h)
    mode = 'no audio' if no_audio else f'{len(mp3s)} audio parts'
    print(f'wrote {out} ({len(h.encode("utf-8"))} bytes, {mode}, 1 background)')


def main():
    ap = argparse.ArgumentParser(description='Build calm/journey episode HTML pages.')
    ap.add_argument('--name', help='episode key, e.g. 01-calm-forest')
    ap.add_argument('--title', help='page title and main heading')
    ap.add_argument('--eyebrow', help='small line above the heading, e.g. "سفر صوتی آرامش / ۱"')
    ap.add_argument('--english', help='English line under the heading')
    ap.add_argument('--desc', help='description line under the heading')
    ap.add_argument('--disc-label', help='first text shown in the centre disc (before playback)')
    ap.add_argument('--enso-label', help='aria-label of the zen ring')
    ap.add_argument('--app-id', help='app id, e.g. cj-01')
    ap.add_argument('--scene', help='canvas scenes joined by +, e.g. mist or waves+mist')
    ap.add_argument('--parts', help='JSON file: list of the section titles (six)')
    ap.add_argument('--assets', required=True,
                    help='folder with the background JPG (and the six MP3 parts in audio mode)')
    ap.add_argument('--out', help='output HTML path (single episode)')
    ap.add_argument('--no-audio', action='store_true', help='build without embedded audio')
    ap.add_argument('--palette', help='JSON file: bg1, bg2, fg, accent, accent2 (hex colours)')
    ap.add_argument('--batch', help='JSON list of episode records, built without audio')
    ap.add_argument('--out-dir', help='output folder for --batch')
    a = ap.parse_args()

    if a.batch:
        if not a.out_dir:
            ap.error('--batch needs --out-dir')
        with open(a.batch, encoding='utf-8') as f:
            records = json.load(f)
        names = [r['name'] for r in records]
        if len(set(names)) != len(names):
            raise SystemExit('duplicate episode names in the batch file')
        os.makedirs(a.out_dir, exist_ok=True)
        for r in records:
            build_page(name=r['name'], title=r['title'], eyebrow=r['eyebrow'], english=r['english'],
                       desc=r['desc'], disc_label=r['disc_label'], enso_label=r['enso_label'],
                       app_id=r['app_id'], scene=r['scene'], parts=r['parts'], assets=a.assets,
                       out=os.path.join(a.out_dir, r['name'] + '.html'), no_audio=True,
                       palette=r.get('palette'), placeholder=r.get('background') == 'placeholder')
        return

    single = {'name': a.name, 'title': a.title, 'eyebrow': a.eyebrow, 'english': a.english,
              'desc': a.desc, 'disc-label': a.disc_label, 'enso-label': a.enso_label,
              'app-id': a.app_id, 'scene': a.scene, 'parts': a.parts, 'out': a.out}
    missing = [f'--{k}' for k, v in single.items() if not v]
    if missing:
        ap.error('missing: ' + ', '.join(missing))
    with open(a.parts, encoding='utf-8') as f:
        parts = json.load(f)
    palette = None
    if a.palette:
        with open(a.palette, encoding='utf-8') as f:
            palette = json.load(f)
    build_page(name=a.name, title=a.title, eyebrow=a.eyebrow, english=a.english, desc=a.desc,
               disc_label=a.disc_label, enso_label=a.enso_label, app_id=a.app_id, scene=a.scene,
               parts=parts, assets=a.assets, out=a.out, no_audio=a.no_audio, palette=palette)


if __name__ == '__main__':
    main()
