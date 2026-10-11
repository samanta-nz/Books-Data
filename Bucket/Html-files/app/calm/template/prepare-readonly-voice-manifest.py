#!/usr/bin/env python3
"""Prepare a narration inventory from an authenticated Read-Only-Books-Data guide.

Use a separately fetched copy of the read-only source, NOT the local .md guide.
This is only a preparatory step: it does not generate speech or edit HTML.
Example: python3 prepare-readonly-voice-manifest.py 08-safe-mental-refuge SOURCE.md --blob GIT_BLOB
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

EPISODES = {'08-safe-mental-refuge': (5, 45, 250),
            '10-five-senses-garden': (6, 31, 164)}
DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
SOURCE_ROOT = 'https://github.com/samanta-nz/Read-Only-Books-Data/blob/main/Bucket/Html-files/app/calm/journey/'
CALM = Path(__file__).resolve().parents[1]


def prepare(episode, source, blob):
    data = Path(source).read_bytes()
    actual_blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    if blob != actual_blob:
        raise ValueError(f'Read-only source blob mismatch: expected {blob}, got {actual_blob}')
    text = data.decode('utf-8')
    heads = list(re.finditer(r'(?m)^### بخش ([۰-۹0-9]+): (.+)$', text))
    count, position_count, total_pause = EPISODES[episode]
    assert len(heads) == count, (episode, len(heads))
    positions, sections = [], []
    for i, head in enumerate(heads, 1):
        assert int(head.group(1).translate(DIGITS)) == i
        end = heads[i].start() if i < len(heads) else len(text)
        body = text[head.end():end]
        body = re.sub(r'(?m)^- \*\*لحن:\*\*.*(?:\n|$)', '', body).strip()
        pieces = re.split(r'\*\*\[مکث ([۰-۹0-9]+) ثانیه\]\*\*', re.sub(r'\s+', ' ', body))
        phrases = [p.strip() for p in pieces[::2]]
        pauses = [int(p.translate(DIGITS)) for p in pieces[1::2]]
        assert len(phrases) == len(pauses)+1 and not phrases[-1], (episode, i, phrases[-1])
        assert all(p and 0 < pause <= 15 for p, pause in zip(phrases, pauses))
        sections.append({'section': i, 'source_title':head.group(2),
                         'positions':len(pauses), 'source_pause_seconds':sum(pauses)})
        positions.extend({'id':f'p{i}s{n:02}', 'source_text':phrase,
                          'source_pause_after_seconds':pause}
                         for n,(phrase,pause) in enumerate(zip(phrases,pauses),1))
    assert len(positions) == position_count and sum(s['source_pause_seconds'] for s in sections) == total_pause
    manifest = {
        'source_url':SOURCE_ROOT+episode+'.md',
        'source_git_blob':actual_blob,
        'source_sha256':hashlib.sha256(data).hexdigest(),
        'source_title':text.splitlines()[0].lstrip('# '),
        'source_guide_speed':1.3,
        'planned_speed':1.0,
        'voice_selection':'PENDING USER CHOICE: voice-03 feminine or voice-08 masculine',
        'readiness':'Source inventory only; NO speech has been generated or approved.',
        'source_position_count':position_count,
        'source_pause_seconds':total_pause,
        'sections':sections,
        'positions':positions,
    }
    target = CALM/'journey/audio'/episode/'source-manifest.json'
    if target.exists():
        raise FileExistsError(f'Refusing to replace an existing voice inventory: {target}')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(episode, f'{count} sections, {position_count} positions, {total_pause}s of source pauses; voice pending')
    return target


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('episode', choices=EPISODES)
    ap.add_argument('source', type=Path)
    ap.add_argument('--blob', required=True)
    args = ap.parse_args()
    prepare(args.episode,args.source,args.blob)
