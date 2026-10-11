#!/usr/bin/env python3
"""Validate source-take checkpoints, then render an episode-04 listening review.

Use the verified READ-ONLY 04-secret-garden.md as --source, not a local editable
copy. --check needs only Python's standard library. Rendering also needs numpy,
praat-parselmouth, lameenc and miniaudio. This does not edit the HTML or
publish audio; it refuses to render until all 97 positions are present.

  python3 render-secret-garden-review.py --source /path/to/read-only/04-secret-garden.md --check
  python3 render-secret-garden-review.py --source /path/to/read-only/04-secret-garden.md --out /tmp/garden-review.mp3
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import wave
from zipfile import ZipFile

AUDIO = Path(__file__).resolve().parents[1] / 'journey/audio/04-secret-garden'
SOURCE_BLOB = '880c1059ebfc9cdd162fc303698db72963b45d94'
PART_LENGTHS = (13, 11, 13, 22, 14, 24)
PART_PAUSES = (52, 79, 104, 171, 132, 126)
EXHALE = ('p4s03', 'p4s05', 'p4s12', 'p4s14')
INHALE = ('p4s11', 'p4s13', 'p4s21')
OVERRIDES = {
    'p1s08': 'و با یه بازدم بلند رها کن.',
    'p3s12': 'یه نفس عمیق. حالا باهم، دم',
    **dict.fromkeys(EXHALE, 'و حالا بازدم'),
    **dict.fromkeys(INHALE, 'حالا باهم، دم'),
}


def source_units(path):
    data = Path(path).read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    if blob != SOURCE_BLOB:
        raise ValueError(f'Unexpected read-only Markdown blob {blob}; expected {SOURCE_BLOB}')
    text = data.decode('utf8')
    heads = list(re.finditer(r'(?m)^### بخش [۱-۶]:.*$', text))
    assert len(heads) == 6
    units = {}
    for part, head in enumerate(heads, 1):
        body = text[head.end():].split('### بخش ', 1)[0]
        body = re.sub(r'(?m)^- \*\*لحن:\*\*.*\n', '', body).strip()
        fields = re.split(r'\*\*\[مکث ([۰-۹0-9]+) ثانیه\]\*\*', re.sub(r'\s+', ' ', body))
        phrases = [x.strip() for x in fields[::2]]
        pauses = [int(x.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))) for x in fields[1::2]]
        assert len(pauses) == PART_LENGTHS[part - 1] and sum(pauses) == PART_PAUSES[part - 1]
        assert len(phrases) == len(pauses) + 1 and not phrases[-1]
        for n, (phrase, pause) in enumerate(zip(phrases, pauses), 1):
            assert phrase and pause > 0
            units[f'p{part}s{n:02}'] = dict(source_text=phrase, pause=pause, part=part)
    assert len(units) == 97 and sum(x['pause'] for x in units.values()) == 664
    return units


def inventory(source):
    units = source_units(source)
    notes = json.loads((AUDIO / 'revision-notes.json').read_text(encoding='utf8'))
    assert notes['read_only_source_git_sha'] == SOURCE_BLOB
    approved = notes.get('approved_remaining_wording', {})
    expected = dict(OVERRIDES)
    for ident, value in approved.items():
        assert units[ident]['source_text'] == value['source']
        assert units[ident]['pause'] == value['source_pause_after_seconds']
        expected[ident] = value['record']
    seen, raw_cache, duplicates = {}, {}, {}
    for archive in sorted(AUDIO.glob('source-clips-*.zip')):
        with ZipFile(archive) as z:
            assert z.testzip() is None, f'Corrupt archive: {archive}'
            manifest = json.loads(z.read('checkpoint.json'))
            assert manifest['source_git_sha'] == SOURCE_BLOB
            assert manifest['voice_id'] == 'voice-08' and manifest['speed'] == 1.0
            for entry in manifest['completed_positions']:
                ident = entry['id']
                assert ident in units, f'Unexpected position: {ident}'
                source_text = units[ident]['source_text']
                assert entry.get('source_text', entry['text']) == source_text, ident
                assert entry['text'] == expected.get(ident, source_text), ident
                assert entry['source_pause_after_seconds'] == units[ident]['pause'], ident
                asset = entry.get('raw_asset', ident + '.wav')
                key = (archive.name, asset)
                if key not in raw_cache:
                    raw_cache[key] = z.read('raw/' + asset)
                assert hashlib.sha256(raw_cache[key]).hexdigest() == entry['sha256'], ident
                with wave.open(io.BytesIO(raw_cache[key])) as w:
                    assert (w.getnchannels(), w.getsampwidth(), w.getframerate()) == (1, 2, 24000)
                    assert abs(w.getnframes() / 24000 - entry['duration_seconds']) < 1e-5
                if ident in seen:
                    duplicates.setdefault(ident, []).append(seen[ident][0].name)
                seen[ident] = (archive, entry, key)
    # The only superseded archive take is the fountain sentence the user asked to redo.
    assert set(duplicates) == {'p3s08'}, duplicates
    redo = notes['discarded_takes']['p3s08']
    assert redo['replacement_status'] == 'recorded'
    assert seen['p3s08'][0].name == redo['replacement_archive']
    assert seen['p3s08'][1]['sha256'] == redo['replacement_raw_sha256']
    missing = [ident for ident in units if ident not in seen]
    return units, seen, raw_cache, missing


def process_pcm(data):
    import numpy as np
    import parselmouth
    from parselmouth.praat import call

    with wave.open(io.BytesIO(data)) as w:
        count = w.getnframes()
        samples = np.frombuffer(w.readframes(count), dtype='<i2').astype(np.float64) / 32768
    sound = parselmouth.Sound(samples, sampling_frequency=24000)
    manipulation = call(sound, 'To Manipulation', .01, 60, 320)
    tier = call(manipulation, 'Extract pitch tier')
    points = call(tier, 'Get number of points')
    assert points >= 2, 'No voiced pitch points in a completed take'
    values = np.array([call(tier, 'Get value at index', i) for i in range(1, points + 1)])
    low, high = float(values.min()), float(values.max())
    assert 55 < low < high < 320
    factor = (.8 * high - low) / (high - low)
    if factor > 0:
        call(tier, 'Formula', f'{low:.17g} + (self - {low:.17g}) * {factor:.17g}')
    else:
        call(tier, 'Formula', 'self * 0.8')
    adjusted = max(call(tier, 'Get value at index', i) for i in range(1, points + 1))
    assert abs(adjusted / high - .8) < 1e-7
    call([manipulation, tier], 'Replace pitch tier')
    result = call(manipulation, 'Get resynthesis (overlap-add)')
    x = result.values[0]
    assert abs(len(x) - count) <= 24
    peak = float(np.max(abs(x)))
    assert peak > 0
    gain = min(1., .85 / peak)
    # Only the especially quiet reused exhale needs an upward level correction.
    if peak < .25:
        gain = min(6., .85 / peak, max(1., .09 / float(np.sqrt(np.mean(x*x)))))
    pcm = np.rint(np.clip(x * gain, -1., 1.) * 32767).astype('<i2')
    return pcm, dict(source_max_F0=high, adjusted_max_F0=adjusted, gain=gain)


def render(units, chosen, raw_cache, output):
    import numpy as np
    import lameenc
    import miniaudio

    output = Path(output)
    if output.suffix != '.mp3':
        raise ValueError('Output path must end in .mp3')
    processed = {}
    chunks, timing = [], []
    offset = 0
    for ident, unit in units.items():
        archive, entry, asset = chosen[ident]
        if asset not in processed:
            processed[asset] = process_pcm(raw_cache[asset])
        pcm, pitch = processed[asset]
        pause = unit['pause']
        timing.append(dict(id=ident, text=entry['text'], source_pause_seconds=pause,
                           start_seconds=offset/24000, speech_samples=len(pcm),
                           source_archive=archive.name, **pitch))
        chunks.extend((pcm, np.zeros(pause * 24000, dtype='<i2')))
        offset += len(pcm) + pause * 24000
    assert len(timing) == 97 and sum(x['source_pause_seconds'] for x in timing) == 664
    joined = np.concatenate(chunks)
    assert len(joined) == offset
    enc = lameenc.Encoder()
    enc.set_channels(1)
    enc.set_in_sample_rate(24000)
    enc.set_bit_rate(96)
    enc.set_quality(2)
    audio = bytearray()
    for i in range(0, len(joined), 5 * 24000):
        audio.extend(enc.encode(joined[i:i+5*24000].tobytes()))
    audio.extend(enc.flush())
    decoded = miniaudio.decode(bytes(audio), output_format=miniaudio.SampleFormat.SIGNED16,
                                nchannels=1, sample_rate=24000)
    assert abs(decoded.num_frames - len(joined)) < 4000
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(audio)
    report = dict(episode='04-secret-garden', section_count=6, segment_count=97,
                  exact_explicit_source_pause_seconds=664, source_git_blob=SOURCE_BLOB,
                  voice_id='voice-08', speed=1.0, max_voiced_F0_ratio=.8,
                  pcm_duration_seconds=len(joined)/24000,
                  mp3_decoded_duration_seconds=decoded.num_frames/24000,
                  mp3_sha256=hashlib.sha256(audio).hexdigest(), cues=timing)
    output.with_suffix('.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    print(f'Wrote complete review: {output} ({len(audio)} bytes, {len(joined)/24000:.2f}s)')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path, help='verified READ-ONLY Markdown')
    parser.add_argument('--check', action='store_true', help='validate without generating audio')
    parser.add_argument('--out', type=Path, help='complete listening review MP3 (render mode)')
    args = parser.parse_args()
    units, selected, raw_cache, missing = inventory(args.source)
    print(f'Episode 04: {len(selected)}/97 usable positions; 97 pauses total 664 seconds; missing: {", ".join(missing) or "none"}')
    if args.check:
        return
    if missing:
        raise SystemExit('Refusing incomplete review: supply all missing positions first')
    if not args.out:
        parser.error('--out is required unless --check is used')
    render(units, selected, raw_cache, args.out)


if __name__ == '__main__':
    main()
