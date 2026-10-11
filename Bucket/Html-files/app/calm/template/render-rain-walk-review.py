#!/usr/bin/env python3
"""Validate and render read-only episode 06 (rain walk) source-take archives.

Usage:
  python3 render-rain-walk-review.py --source /verified/read-only/06-rain-walk.md --check
  python3 render-rain-walk-review.py --source /verified/read-only/06-rain-walk.md --render

Check mode needs the standard library only. Render mode also needs numpy,
praat-parselmouth, lameenc and miniaudio. It refuses to render if a cue is
missing, a source pause differs, a discarded take is selected, or an override
is unapproved. The user chose voice-08 at normal speaking speed, rather than
the Markdown guide's 1.3x; the supplied reference recording was not used.
"""
import argparse
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import wave
from zipfile import ZipFile

CALM = Path(__file__).resolve().parents[1]
AUDIO = CALM / 'journey/audio/06-rain-walk'
SOURCE_BLOB = '0ed630cc62eb43bb8c657321a7c02195f147af9a'
LENGTHS = [11, 12, 11, 17, 12, 19]
PAUSES = [51, 81, 96, 125, 110, 93]


def source_units(path, source_hash):
    data = Path(path).read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert blob == SOURCE_BLOB and hashlib.sha256(data).hexdigest() == source_hash
    s = data.decode('utf8')
    heads = list(re.finditer(r'(?m)^### بخش [۱-۶]:.*$', s))
    assert len(heads) == 6
    out = {}
    for part, head in enumerate(heads, 1):
        block = re.sub(r'(?m)^- \*\*لحن:\*\*.*\n', '', s[head.end():].split('### بخش ', 1)[0]).strip()
        tokens = re.split(r'\*\*\[مکث ([۰-۹0-9]+) ثانیه\]\*\*', re.sub(r'\s+', ' ', block))
        phrases = [x.strip() for x in tokens[::2]]
        pauses = [int(x.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))) for x in tokens[1::2]]
        assert len(pauses) == LENGTHS[part-1] and sum(pauses) == PAUSES[part-1]
        assert len(phrases) == len(pauses)+1 and not phrases[-1]
        for n, (text, pause) in enumerate(zip(phrases, pauses), 1):
            assert text and pause > 0
            out[f'p{part}s{n:02}'] = dict(part=part, text=text, pause=pause)
    assert len(out) == 82 and sum(x['pause'] for x in out.values()) == 556
    return out


def inventory(source):
    m = json.loads((AUDIO/'source-manifest.json').read_text(encoding='utf8'))
    assert m['source_git_blob'] == SOURCE_BLOB and m['approved_speaking_speed'] == 1.0
    assert m['narrator'].startswith('voice-08')
    units = source_units(source, m['source_sha256'])
    assert len(m['positions']) == len(units) == 82
    for x, (name, orig) in zip(m['positions'], units.items()):
        assert (x['id'], x['source_text'], x['source_pause_after_seconds']) == (name, orig['text'], orig['pause'])
    notes = json.loads((AUDIO/'revision-notes.json').read_text(encoding='utf8'))
    assert notes['source_git_blob'] == SOURCE_BLOB
    replacement = notes['user_approved_replacement']['p5s11']
    assert replacement['status'] == 'recorded'
    assert replacement['source_text'] == units['p5s11']['text']
    assert replacement['source_pause_after_seconds'] == units['p5s11']['pause']
    expected = {'p2s10':'یه نفس عمیق. حالا باهم، دم',
                'p4s16':'حالا باهم، دم',
                'p5s11':replacement['record_text']}
    chosen, raw_cache, duplicates = {}, {}, {}
    for archive in sorted(AUDIO.glob('source-clips-*.zip')):
        with ZipFile(archive) as z:
            assert z.testzip() is None, f'Corrupt ZIP {archive}'
            chk = json.loads(z.read('checkpoint.json'))
            assert chk['source_git_blob'] == SOURCE_BLOB
            assert chk['voice_id'] == 'voice-08' and chk['speed'] == 1.0
            for x in chk['completed_positions']:
                ident = x['id']
                assert ident in units
                unit = units[ident]
                assert x.get('source_text', x['text']) == unit['text'], ident
                assert x['source_pause_after_seconds'] == unit['pause'], ident
                if ident != 'p5s11':
                    assert x['text'] == expected.get(ident, unit['text']), ident
                asset = x.get('raw_asset', ident+'.wav')
                key = (archive.name, asset)
                if key not in raw_cache:
                    raw_cache[key] = z.read('raw/'+asset)
                assert hashlib.sha256(raw_cache[key]).hexdigest() == x['sha256'], ident
                with wave.open(io.BytesIO(raw_cache[key])) as w:
                    assert (w.getnchannels(), w.getsampwidth(), w.getframerate()) == (1, 2, 24000)
                    assert abs(w.getnframes()/24000 - x['duration_seconds']) < 1e-5
                if ident in chosen:
                    duplicates.setdefault(ident, set()).add(chosen[ident][0].name)
                    duplicates[ident].add(archive.name)
                chosen[ident] = (archive, x, key)
    assert set(duplicates) == {'p5s11'}, duplicates
    old = {x['archive'] for x in replacement['discarded_takes']}
    assert duplicates['p5s11'] == old | {replacement['replacement_archive']}
    assert chosen['p5s11'][0].name == replacement['replacement_archive']
    assert chosen['p5s11'][1]['sha256'] == replacement['replacement_sha256']
    assert chosen['p5s11'][1]['text'] == replacement['record_text']
    missing = [x for x in units if x not in chosen]
    return units, chosen, raw_cache, missing


def processor():
    spec = importlib.util.spec_from_file_location('garden_audio_process', Path(__file__).with_name('render-secret-garden-review.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.process_pcm


def encode(pcm, output):
    import lameenc
    import miniaudio
    enc = lameenc.Encoder()
    enc.set_channels(1)
    enc.set_in_sample_rate(24000)
    enc.set_bit_rate(96)
    enc.set_quality(2)
    result = bytearray()
    for i in range(0, len(pcm), 24000*5):
        result.extend(enc.encode(pcm[i:i+24000*5].tobytes()))
    result.extend(enc.flush())
    output.write_bytes(result)
    decoded = miniaudio.decode_file(str(output), output_format=miniaudio.SampleFormat.SIGNED16,
                                    nchannels=1, sample_rate=24000)
    assert abs(decoded.num_frames-len(pcm)) < 4000
    return hashlib.sha256(result).hexdigest(), decoded.num_frames/24000


def render(units, chosen, raw_cache):
    import numpy as np
    import miniaudio
    process = processor()
    rendered = {}
    whole, all_cues, overall_offset = [], [], 0
    for part, count in enumerate(LENGTHS, 1):
        chunks, cues, offset = [], [], 0
        for n in range(1, count+1):
            ident = f'p{part}s{n:02}'
            archive, item, asset = chosen[ident]
            if asset not in rendered:
                rendered[asset] = process(raw_cache[asset])
            pcm, pitch = rendered[asset]
            pause = units[ident]['pause']
            assert abs(pitch['adjusted_max_F0']/pitch['source_max_F0']-.8) < 1e-7
            cue = dict(id=ident, text=item['text'], source_text=units[ident]['text'],
                       part=part, start_seconds=overall_offset/24000,
                       part_start_seconds=offset/24000, speech_samples=len(pcm),
                       source_pause_seconds=pause, source_archive=archive.name,
                       source_max_F0=pitch['source_max_F0'], adjusted_max_F0=pitch['adjusted_max_F0'])
            cues.append(cue)
            chunks.extend([pcm, np.zeros(pause*24000, dtype='<i2')])
            offset += len(pcm)+pause*24000
            overall_offset += len(pcm)+pause*24000
        data = np.concatenate(chunks)
        assert len(data) == offset and sum(x['source_pause_seconds'] for x in cues) == PAUSES[part-1]
        out = AUDIO/f'06-rain-walk-part{part:02}-review.mp3'
        sha, duration = encode(data, out)
        decoded = miniaudio.decode_file(str(out), output_format=miniaudio.SampleFormat.SIGNED16,
                                        nchannels=1, sample_rate=24000)
        samples = np.frombuffer(decoded.samples, dtype='<i2')
        for x in cues:
            middle = x['part_start_seconds']+x['speech_samples']/24000+x['source_pause_seconds']/2
            probe = samples[int((middle-.1)*24000):int((middle+.1)*24000)]
            assert len(probe) > 0 and np.max(np.abs(probe.astype(np.int32))) < 500, x['id']
        report = dict(source_git_blob=SOURCE_BLOB, voice_id='voice-08', speed=1.0,
                      voiced_max_F0_ratio=.8, part=part, positions=count,
                      source_pause_seconds=PAUSES[part-1], pcm_duration_seconds=offset/24000,
                      mp3_decoded_duration_seconds=duration, mp3_sha256=sha, cues=cues)
        out.with_suffix('.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
        whole.append(data)
        all_cues.extend(cues)
        print(out.name, count, 'cues,', PAUSES[part-1], 'seconds explicit pause,', round(offset/24000, 2), 'seconds')
    assert len(all_cues) == 82 and sum(x['source_pause_seconds'] for x in all_cues) == 556
    full = np.concatenate(whole)
    assert len(full) == overall_offset
    out = AUDIO/'06-rain-walk-full-review.mp3'
    sha, duration = encode(full, out)
    report = dict(source_git_blob=SOURCE_BLOB, voice_id='voice-08', speed=1.0,
                  voiced_max_F0_ratio=.8, source_explicit_pause_seconds=556,
                  segment_count=82, pcm_duration_seconds=len(full)/24000,
                  mp3_decoded_duration_seconds=duration, mp3_sha256=sha, cues=all_cues,
                  user_corrected_line='بدنت چه حسی داره؟ توجه کن و عمیق‌تر احساسش کن.',
                  reference_audio_used=False)
    out.with_suffix('.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
    print('Full review:', len(full)/24000, 'seconds,', out.stat().st_size, 'bytes')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True, help='verified read-only 06-rain-walk.md')
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--check', action='store_true')
    modes.add_argument('--render', action='store_true')
    args = parser.parse_args()
    units, chosen, raw_cache, missing = inventory(args.source)
    print(f'Episode 06: {len(chosen)}/82 usable positions; 82 source pauses totaling 556 seconds; missing: {", ".join(missing) or "none"}')
    if args.render:
        if missing:
            raise SystemExit('Refusing to render incomplete episode-06 audio')
        render(units, chosen, raw_cache)


if __name__ == '__main__':
    main()
