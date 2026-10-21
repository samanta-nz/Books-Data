#!/usr/bin/env python3
"""Stage and verify a minimal five-part refuge soundscape before embedding.

The 5-section Read-Only guide contains 45 source pauses / 250s. The scene
enters quietly from the first safety instruction, becomes fully audible at
p3s01 (first invitation to listen), then recedes from p4s07 (grounding) to
the end: cue-aligned ~4min arrival / ~3min departure as required by README.
Run WITHOUT --apply first. Requires numpy, scipy, miniaudio and lameenc.
"""
import argparse
import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import numpy as np
from scipy import signal

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent/'journey'
NAME='08-safe-mental-refuge'
FOLDER=ROOT/'audio'/NAME
FS=24000
spec=importlib.util.spec_from_file_location('garden_mix_helpers',HERE/'mix-five-senses-garden.py')
helpers=importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)
sha,decode,encode=helpers.sha,helpers.decode,helpers.encode


def soundscape(length,arrival_end,departure_start,pcm_end):
    assert 215<arrival_end<250 and 375<departure_start<430
    assert 550<pcm_end<620 and arrival_end<departure_start
    rng=np.random.default_rng(80808)
    leaves=signal.sosfilt(signal.butter(2,(420,2700),btype='bandpass',fs=FS,output='sos'),rng.standard_normal(length).astype(np.float32))
    wind=signal.sosfilt(signal.butter(2,(130,720),btype='bandpass',fs=FS,output='sos'),rng.standard_normal(length).astype(np.float32))
    sound=(.86*leaves+.22*wind).astype(np.float32)
    del leaves,wind
    # Rare gentle, very distant birds. Tapered so there are no alarming clicks.
    size=round(.40*FS);t=np.arange(size,dtype=np.float32)/FS
    window=np.sin(np.pi*t/(size/FS))**2
    for pos in rng.integers(0,length-size,size=rng.poisson(length/FS*.085)):
        freq=rng.uniform(700,950)
        bird=np.sin(2*np.pi*(freq*t+190*t*t))
        sound[pos:pos+size] += (.10*window*bird).astype(np.float32)
    for a in range(0,length,FS*10):
        b=min(length,a+FS*10)
        times=np.arange(a,b,dtype=np.float64)/FS
        sound[a:b] *= (.88+.12*np.sin(2*np.pi*.067*times)).astype(np.float32)
    sound-=np.mean(sound,dtype=np.float64)
    rms=float(np.sqrt(np.mean(sound.astype(np.float64)**2)))
    assert rms>.01
    target=.0058
    sound*=target/rms
    up_end=round(arrival_end*FS);down_start=round(departure_start*FS);down_end=round(pcm_end*FS)
    assert 0<up_end<down_start<down_end<=length
    envelope=np.full(length,0,dtype=np.float32)
    rise=np.linspace(0,1,up_end,dtype=np.float32)
    envelope[:up_end]=.04+.96*rise*rise*(3-2*rise)
    envelope[up_end:down_start]=1
    fall=np.linspace(0,1,down_end-down_start,dtype=np.float32)
    envelope[down_start:down_end]=1-fall*fall*(3-2*fall)
    envelope[down_end:]=0
    envelope[:FS]*=np.linspace(0,1,FS,dtype=np.float32)
    sound*=envelope
    assert np.max(np.abs(sound))<.1
    mid=float(np.sqrt(np.mean(sound[up_end:down_start].astype(np.float64)**2)))
    assert .85*target<mid<1.15*target
    return sound,dict(fade_in_start_seconds=0,fade_in_end_seconds=arrival_end,
      fade_out_start_seconds=departure_start,fade_out_end_seconds=pcm_end,
      fade_in_duration_seconds=arrival_end,fade_out_duration_seconds=pcm_end-departure_start,
      ambient_mid_rms=mid,ambient_mid_dbfs=float(20*np.log10(mid)))


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--scratch',type=Path,default=Path('.scratch/ambient-output')/NAME)
    ap.add_argument('--apply',action='store_true')
    args=ap.parse_args()
    output=args.scratch;output.mkdir(parents=True,exist_ok=True)
    htmlpath=ROOT/(NAME+'.html');html=htmlpath.read_text(encoding='utf8')
    assert html.count('const AUDIO=[];')==1
    assert html.count('audio: none yet (built without audio)')==1
    assert html.count('parts: 6 | audio:')==1 and 'const PART_TITLES=[' in html
    ppaths=[FOLDER/(NAME+f'-part{i:02}-voice-review.mp3') for i in range(1,6)]
    fpath=FOLDER/(NAME+'-full-voice-review.mp3')
    parts=[json.loads(p.with_suffix('.json').read_text(encoding='utf8')) for p in ppaths]
    full=json.loads(fpath.with_suffix('.json').read_text(encoding='utf8'))
    manifest=json.loads((FOLDER/'source-manifest.json').read_text(encoding='utf8'))
    assert manifest['source_git_blob']==full['source_git_blob']=='e97fbe19aea76c41300be99f72ad9a4b4c16d780'
    assert len(manifest['positions'])==len(manifest['recorded_positions'])==45
    assert sum(p['exact_explicit_source_pause_seconds'] for p in parts)==250
    assert all(sha(p.read_bytes())==report['mp3_sha256'] for p,report in zip(ppaths,parts))
    assert sha(fpath.read_bytes())==full['mp3_sha256']
    pcm_end=full['pcm_duration_seconds']
    cues={x['id']:x for x in full['cues']}
    arrival_end=cues['p3s01']['start_seconds']
    departure_start=cues['p4s07']['start_seconds']
    dryparts=[decode(p.read_bytes()) for p in ppaths]
    dryfull=decode(fpath.read_bytes())
    ambience,fade=soundscape(len(dryfull),arrival_end,departure_start,pcm_end)
    dry_rms=float(np.sqrt(np.mean((dryfull.astype(np.float64)/32768)**2)))
    amb_rms=float(np.sqrt(np.mean(ambience.astype(np.float64)**2)))
    relative=float(20*np.log10(dry_rms/amb_rms))
    assert relative>18 and max(np.max(np.abs(x.astype(np.int32))) for x in dryparts)<32767
    wetparts=[];durations=[];cursor=0
    for i,voice in enumerate(dryparts):
        # Use cue-based PCM offsets rather than concatenated MP3 decoder padding.
        start=round(cursor*FS)
        noise=ambience[start:start+len(voice)]
        if len(noise)<len(voice):noise=np.pad(noise,(0,len(voice)-len(noise)))
        merged=voice.astype(np.float32)/32768+noise
        assert np.max(np.abs(merged))<.975
        wet=encode(np.rint(merged*32767).astype('<i2'))
        wetparts.append(wet);durations.append(len(decode(wet))/FS)
        (output/f'part{i+1:02}.mp3').write_bytes(wet)
        cursor+=parts[i]['pcm_duration_seconds']
    assert abs(cursor-pcm_end)<.001
    merged=dryfull.astype(np.float32)/32768+ambience
    assert np.max(np.abs(merged))<.975
    wetfull=encode(np.rint(merged*32767).astype('<i2'))
    (output/'full.mp3').write_bytes(wetfull)
    full_seconds=len(decode(wetfull))/FS
    assert abs(full_seconds-pcm_end)<.12
    metadata=dict(episode=NAME,scene='soft forest leaves, wind and distant birds',seed=80808,
      narrative_fade_policy='README: 4-minute arrival to p3s01 scene sounds, continuous subtle middle, 3-minute departure from p4s07 grounding; all boundaries tied exactly to source cues.',
      **fade,ambient_rms=amb_rms,ambient_dbfs=float(20*np.log10(amb_rms)),
      voice_to_ambient_db=relative,source_pause_seconds_unchanged=250,
      source_git_blob=manifest['source_git_blob'],dry_part_sha256=[sha(p.read_bytes()) for p in ppaths],
      wet_part_sha256=[sha(p) for p in wetparts],dry_full_sha256=sha(fpath.read_bytes()),
      wet_full_sha256=sha(wetfull),wet_part_decoded_seconds=durations,
      wet_full_decoded_seconds=full_seconds)
    (output/'mix-report.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Staged 08 refuge soundscape',round(pcm_end,2),'sec; fade in',arrival_end,
          'fade out',round(pcm_end-departure_start,2),'sec; voice/ambient',round(relative,1),'dB')
    if not args.apply:return
    uris=['data:audio/mpeg;base64,'+base64.b64encode(v).decode('ascii') for v in wetparts]
    new=html.replace('const AUDIO=[];','const AUDIO='+json.dumps(uris,separators=(',',':'))+';',1)
    new=new.replace('parts: 6 | audio:','parts: 5 | audio:',1)
    new=new.replace('audio: none yet (built without audio)',
        'audio: five embedded MP3 parts with minimal forest ambience (250 source pause seconds)',1)
    assert new.count('parts: 5 | audio:')==1
    # Leave the dry voice-only reviews untouched for source/prosody auditing.
    for i,(data,report,duration) in enumerate(zip(wetparts,parts,durations),1):
        report['mp3_sha256']=sha(data)
        report['mp3_decoded_duration_seconds']=duration
        report['status']='FINAL MIX WITH SAFE FOREST AMBIENCE'
        report['ambience']=fade
        target=FOLDER/(NAME+f'-part{i:02}-review.mp3')
        target.write_bytes(data)
        target.with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    full['mp3_sha256']=sha(wetfull)
    full['mp3_decoded_duration_seconds']=full_seconds
    full['status']='FINAL MIX WITH SAFE FOREST AMBIENCE'
    full['ambience']=metadata
    target=FOLDER/(NAME+'-full-review.mp3')
    target.write_bytes(wetfull)
    target.with_suffix('.json').write_text(json.dumps(full,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    htmlpath.write_text(new,encoding='utf8')
    print('Applied 08 final wet audio and five-part self-contained HTML')

if __name__=='__main__':main()
