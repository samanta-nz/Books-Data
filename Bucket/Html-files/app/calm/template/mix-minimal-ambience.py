#!/usr/bin/env python3
"""Make quiet, original fountain/rain ambiences and mix into the existing 04/06 narration.

Install numpy, scipy, miniaudio and lameenc. Stage first to --scratch;
after QA, apply to HTML and user-facing audio with --apply.
The fade starts at p2s01 and ends after p6s01 + 180s in each episode. Input audio is read from the current self-contained HTML and full
review, checked against their timing reports. Do not run --apply twice: the
source hash checks reject audio that is already mixed.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import re

import lameenc
import miniaudio
import numpy as np
from scipy import signal

FS = 24000
ROOT = Path(__file__).resolve().parents[1] / 'journey'
SETTINGS = {
    '04-secret-garden': dict(kind='soft_fountain', target_rms=.0065, seed=4404,
                             comment_from='audio: six verified embedded MP3 parts (97 source pauses)',
                             comment_to='audio: six embedded MP3 parts with minimal fountain background (97 source pauses)'),
    '06-rain-walk': dict(kind='soft_rain', target_rms=.0075, seed=6606,
                         comment_from='audio: six verified embedded MP3 parts (82 source pauses)',
                         comment_to='audio: six embedded MP3 parts with minimal rain background (82 source pauses)'),
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def decode(data):
    result = miniaudio.decode(data, output_format=miniaudio.SampleFormat.SIGNED16,
                              nchannels=1, sample_rate=FS)
    assert result.sample_rate == FS and result.nchannels == 1
    return np.frombuffer(result.samples, dtype='<i2').copy()


def encode(pcm):
    enc = lameenc.Encoder()
    enc.set_channels(1)
    enc.set_in_sample_rate(FS)
    enc.set_bit_rate(96)
    enc.set_quality(2)
    out = bytearray()
    for i in range(0, len(pcm), FS*5):
        out.extend(enc.encode(pcm[i:i+FS*5].tobytes()))
    out.extend(enc.flush())
    return bytes(out)


def ambience(total, *, kind, target_rms, seed, fade_in_start, fade_out_start):
    """Filtered scene sound with the README's long narrative-synchronized fades.

    Four-minute arrival, gentle breathing-like middle, three-minute departure.
    No music, speech, thunder, borrowed field recordings or harsh transient FX.
    Same seeded texture spans all six section boundaries.
    """
    rng = np.random.default_rng(seed)
    raw = rng.standard_normal(total).astype(np.float32)
    if kind == 'soft_fountain':
        band = (180, 2400)
        event_rate = 2.5
    else:
        band = (360, 4100)
        event_rate = 7.0
    sos = signal.butter(2, band, btype='bandpass', fs=FS, output='sos')
    colored = signal.sosfilt(sos, raw).astype(np.float32)
    del raw
    # A very slow change in water density; never a rhythmic/music-like loop.
    for start in range(0, total, FS*10):
        stop = min(total, start+FS*10)
        t = np.arange(start, stop, dtype=np.float64) / FS
        colored[start:stop] *= (0.86 + 0.14*np.sin(2*np.pi*(0.083 if kind=='soft_fountain' else 0.057)*t)).astype(np.float32)
    # Occasional water drops: tapered so neither texture clicks nor startles.
    seconds = total / FS
    event_count = rng.poisson(seconds * event_rate)
    positions = rng.integers(0, max(1, total-3000), size=event_count)
    if kind == 'soft_fountain':
        size = int(.105*FS)
        t = np.arange(size, dtype=np.float32)/FS
        env = (1-np.exp(-t*100))*np.exp(-t*34)
        for pos in positions:
            frequency = rng.uniform(430, 830)
            chirp = np.sin(2*np.pi*frequency*t + rng.uniform(0, 2*np.pi))
            colored[pos:pos+size] += (rng.uniform(.10,.28)*env*chirp).astype(np.float32)
    else:
        size = int(.045*FS)
        t = np.arange(size, dtype=np.float32)/FS
        env = (1-np.exp(-t*250))*np.exp(-t*95)
        for pos in positions:
            click = rng.standard_normal(size).astype(np.float32)
            colored[pos:pos+size] += rng.uniform(.12,.4)*env*click
    colored -= np.mean(colored, dtype=np.float64)
    rms = float(np.sqrt(np.mean(colored.astype(np.float64)**2)))
    assert rms > .01
    colored *= target_rms/rms
    # The episode guide and README require a long rise from the scene entrance,
    # an undisturbed middle, and a three-minute fall as the guide returns home.
    start = round(fade_in_start*FS)
    up_end = start + 240*FS
    down_start = round(fade_out_start*FS)
    down_end = down_start + 180*FS
    assert 0 < start < up_end < down_start < down_end < total
    envelope = np.full(total, .04, dtype=np.float32)  # distant murmur before scene
    rise = np.linspace(0, 1, up_end-start, dtype=np.float32)
    envelope[start:up_end] = .04 + .96*(rise*rise*(3-2*rise))
    envelope[up_end:down_start] = 1
    fall = np.linspace(0, 1, down_end-down_start, dtype=np.float32)
    envelope[down_start:down_end] = 1-(fall*fall*(3-2*fall))
    envelope[down_end:] = 0
    first = min(FS, total)
    envelope[:first] *= np.linspace(0, 1, first, dtype=np.float32)
    colored *= envelope
    del envelope
    middle = colored[up_end:down_start]
    mid_rms = float(np.sqrt(np.mean(middle.astype(np.float64)**2)))
    assert .85*target_rms < mid_rms < 1.15*target_rms, (mid_rms, target_rms)
    assert np.max(np.abs(colored)) < .10
    return colored


def process(name, scratch, apply):
    setting = SETTINGS[name]
    outdir = scratch/name
    outdir.mkdir(parents=True, exist_ok=True)
    page = ROOT/(name+'.html')
    html = page.read_text(encoding='utf8')
    match = re.search(r'(?m)^const AUDIO=(\[.*?\]);$', html)
    assert match and html.count(setting['comment_from']) == 1
    uris = json.loads(match.group(1))
    assert len(uris) == 6
    folder = ROOT/'audio'/name
    fullpath = folder/(name+'-full-review.mp3')
    fullreport_path = fullpath.with_suffix('.json')
    fullreport = json.loads(fullreport_path.read_text(encoding='utf8'))
    dryfull = fullpath.read_bytes()
    assert fullreport['mp3_sha256'] == sha(dryfull)
    part_reports = []
    dryparts = []
    for i, uri in enumerate(uris, 1):
        assert uri.startswith('data:audio/mpeg;base64,')
        track = base64.b64decode(uri.split(',', 1)[1])
        if name.startswith('04'):
            report = json.loads((folder/(name+'-parts.json')).read_text(encoding='utf8'))['parts'][i-1]
        else:
            report = json.loads((folder/(name+f'-part{i:02}-review.json')).read_text(encoding='utf8'))
        assert report['mp3_sha256'] == sha(track)
        dryparts.append(track)
        part_reports.append(report)
    decoded_parts = [decode(p) for p in dryparts]
    dry_full_pcm = decode(dryfull)
    length = max(sum(len(x) for x in decoded_parts), len(dry_full_pcm))
    cues = {cue['id']:cue for cue in fullreport['cues']}
    fade_in_start = cues['p2s01']['start_seconds']
    fade_out_start = cues['p6s01']['start_seconds']
    ambient = ambience(length, fade_in_start=fade_in_start,
                       fade_out_start=fade_out_start,
                       **{k:setting[k] for k in ('kind','target_rms','seed')})
    mixed = []
    wet_part_decoded_seconds = []
    cursor = 0
    for i, voice in enumerate(decoded_parts, 1):
        x = voice.astype(np.float32)/32768
        noise = ambient[cursor:cursor+len(voice)]
        y = np.clip(x+noise, -0.975, 0.975)
        assert np.max(np.abs(x+noise)) < .975
        outpcm = np.rint(y*32767).astype('<i2')
        wet = encode(outpcm)
        decoded_wet = decode(wet)
        assert abs(len(decoded_wet)-len(voice)) < FS*.08
        wet_part_decoded_seconds.append(len(decoded_wet)/FS)
        (outdir/f'part{i:02}.mp3').write_bytes(wet)
        mixed.append(wet)
        cursor += len(voice)
    x = dry_full_pcm.astype(np.float32)/32768
    y = np.clip(x+ambient[:len(x)], -0.975, 0.975)
    assert np.max(np.abs(x+ambient[:len(x)])) < .975
    wetfull = encode(np.rint(y*32767).astype('<i2'))
    (outdir/'full.mp3').write_bytes(wetfull)
    # Compare timing and recover voice content: background must not mask narration.
    wet_full_decoded_seconds = len(decode(wetfull))/FS
    assert abs(wet_full_decoded_seconds-len(dry_full_pcm)/FS) < .08
    dry_rms = float(np.sqrt(np.mean(x.astype(np.float64)**2)))
    ambient_rms = float(np.sqrt(np.mean(ambient.astype(np.float64)**2)))
    assert ambient_rms < .15*dry_rms, (ambient_rms,dry_rms)
    mid_start = round((fade_in_start+240)*FS)
    mid_end = round(fade_out_start*FS)
    mid_rms = float(np.sqrt(np.mean(ambient[mid_start:mid_end].astype(np.float64)**2)))
    metadata = dict(episode=name, kind=setting['kind'], seed=setting['seed'],
                    fade_in_start_seconds=fade_in_start,
                    fade_in_end_seconds=fade_in_start+240,
                    fade_out_start_seconds=fade_out_start,
                    fade_out_end_seconds=fade_out_start+180,
                    fade_policy='README soundscape: 4-minute arrival, gentle breathing modulation in the middle, 3-minute departure',
                    ambient_rms=ambient_rms, ambient_dbfs=20*np.log10(ambient_rms),
                    ambient_mid_rms=mid_rms, ambient_mid_dbfs=20*np.log10(mid_rms),
                    dry_voice_rms=dry_rms, voice_to_ambient_db=20*np.log10(dry_rms/ambient_rms),
                    full_dry_sha256=sha(dryfull), full_wet_sha256=sha(wetfull),
                    part_dry_sha256=[sha(v) for v in dryparts],
                    part_wet_sha256=[sha(v) for v in mixed],
                    wet_full_decoded_seconds=wet_full_decoded_seconds,
                    wet_part_decoded_seconds=wet_part_decoded_seconds,
                    narration_pause_seconds=664 if name.startswith('04') else 556,
                    sample_rate=FS)
    (outdir/'mix-report.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(name, 'dry RMS',round(dry_rms,4),'ambience RMS',round(ambient_rms,4),
          'relative',round(metadata['voice_to_ambient_db'],1),'dB', 'full wet bytes',len(wetfull))
    if not apply:
        return
    weturis=['data:audio/mpeg;base64,'+base64.b64encode(track).decode('ascii') for track in mixed]
    line='const AUDIO='+json.dumps(weturis,separators=(',',':'))+';'
    newhtml=html[:match.start()]+line+html[match.end():]
    newhtml=newhtml.replace(setting['comment_from'], setting['comment_to'], 1)
    assert newhtml.replace(line,match.group(0)).replace(setting['comment_to'],setting['comment_from'],1) == html
    # Put all validated assets in place only after the new HTML can be reconstructed.
    fullreport['mp3_sha256'] = sha(wetfull)
    fullreport['mp3_decoded_duration_seconds'] = wet_full_decoded_seconds
    fullreport['ambience'] = metadata
    fullreport['source_narration_pause_seconds_unchanged'] = metadata['narration_pause_seconds']
    if name.startswith('04'):
        partsfile = folder/(name+'-parts.json')
        parts = json.loads(partsfile.read_text(encoding='utf8'))
        for part, data, duration in zip(parts['parts'],mixed,wet_part_decoded_seconds):
            part['mp3_sha256'] = sha(data)
            part['mp3_decoded_seconds'] = duration
        parts['ambience'] = {key:metadata[key] for key in ('kind','fade_in_start_seconds',
          'fade_in_end_seconds','fade_out_start_seconds','fade_out_end_seconds','ambient_mid_dbfs')}
        parts['source_narration_pause_seconds_unchanged'] = 664
        partsfile.write_text(json.dumps(parts,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    else:
        for i,(report,data,duration) in enumerate(zip(part_reports,mixed,wet_part_decoded_seconds),1):
            report['mp3_sha256'] = sha(data)
            report['mp3_decoded_duration_seconds'] = duration
            report['ambience'] = {key:metadata[key] for key in ('kind','fade_in_start_seconds',
              'fade_in_end_seconds','fade_out_start_seconds','fade_out_end_seconds','ambient_mid_dbfs')}
            report['source_narration_pause_seconds_unchanged'] = report['source_pause_seconds']
            (folder/(name+f'-part{i:02}-review.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
            (folder/(name+f'-part{i:02}-review.mp3')).write_bytes(data)
    fullpath.write_bytes(wetfull)
    fullreport_path.write_text(json.dumps(fullreport,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    page.write_text(newhtml,encoding='utf8')
    print('applied',name,'HTML bytes',page.stat().st_size)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--scratch', type=Path, default=Path('.scratch/ambient-output'))
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('episode', choices=['04-secret-garden','06-rain-walk','both'])
    args=ap.parse_args()
    for episode in (SETTINGS if args.episode=='both' else [args.episode]):
        process(episode,args.scratch,args.apply)


if __name__=='__main__':
    main()
