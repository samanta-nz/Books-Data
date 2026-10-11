#!/usr/bin/env python3
"""Stage a quiet hillside wind / distant stream for episode 12, then apply after QC.

The authoritative six-part narration lasts 7:10 at 1x with all 183 seconds
of source pauses. The generic 4+3-minute fades leave no meaningful middle,
so use the user's text-synchronized exact-symmetry policy from short episode
10: equal fades from p2s01 (entering the landscape) and p6s01 (returning).
Run without --apply first. Requires numpy, scipy, miniaudio, lameenc.
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
NAME='12-virtual-nature'
FOLDER=ROOT/'audio'/NAME
FS=24000
spec=importlib.util.spec_from_file_location('virtual_nature_mix_helpers',HERE/'mix-five-senses-garden.py')
helpers=importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)
sha,decode,encode=helpers.sha,helpers.decode,helpers.encode


def soundscape(length,scene_in,scene_out,pcm_end):
    assert 70<scene_in<100 and 320<scene_out<375 and 395<pcm_end<475
    fade=pcm_end-scene_out
    assert 60<fade<110 and scene_in+fade<scene_out
    rng=np.random.default_rng(121212)
    # Wide, gentle hillside air with a very distant trickle: no music or sharp FX.
    wind=signal.sosfilt(signal.butter(2,(130,1100),btype='bandpass',fs=FS,output='sos'),rng.standard_normal(length).astype(np.float32))
    stream=signal.sosfilt(signal.butter(2,(400,2300),btype='bandpass',fs=FS,output='sos'),rng.standard_normal(length).astype(np.float32))
    sound=(.86*wind+.24*stream).astype(np.float32)
    del wind,stream
    for start in range(0,length,FS*10):
        end=min(length,start+FS*10)
        t=np.arange(start,end,dtype=np.float64)/FS
        sound[start:end]*=(.88+.12*np.sin(2*np.pi*.061*t)).astype(np.float32)
    sound-=np.mean(sound,dtype=np.float64)
    target=.0056
    rms=float(np.sqrt(np.mean(sound.astype(np.float64)**2)))
    assert rms>.01
    sound*=target/rms
    a=round(scene_in*FS);b=round((scene_in+fade)*FS)
    c=round(scene_out*FS);d=round(pcm_end*FS)
    assert 0<a<b<c<d<=length
    env=np.full(length,.04,dtype=np.float32)
    t=np.linspace(0,1,b-a,dtype=np.float32)
    env[a:b]=.04+.96*t*t*(3-2*t)
    env[b:c]=1
    t=np.linspace(0,1,d-c,dtype=np.float32)
    env[c:d]=1-t*t*(3-2*t)
    env[d:]=0
    env[:FS]*=np.linspace(0,1,FS,dtype=np.float32)
    sound*=env
    mid=float(np.sqrt(np.mean(sound[b:c].astype(np.float64)**2)))
    assert .85*target<mid<1.15*target and np.max(np.abs(sound))<.10
    return sound,dict(fade_in_start_seconds=scene_in,fade_in_end_seconds=scene_in+fade,
      fade_out_start_seconds=scene_out,fade_out_end_seconds=pcm_end,
      fade_duration_seconds=fade,ambient_mid_rms=mid,ambient_mid_dbfs=float(20*np.log10(mid)))


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--scratch',type=Path,default=Path('.scratch/ambient-output')/NAME)
    ap.add_argument('--apply',action='store_true')
    args=ap.parse_args()
    stage=args.scratch;stage.mkdir(parents=True,exist_ok=True)
    htmlpath=ROOT/(NAME+'.html');html=htmlpath.read_text(encoding='utf8')
    assert html.count('const AUDIO=[];')==1
    assert html.count('audio: none yet (built without audio)')==1
    assert html.count('parts: 6 | audio:')==1
    paths=[FOLDER/(NAME+f'-part{i:02}-voice-review.mp3') for i in range(1,7)]
    fullpath=FOLDER/(NAME+'-full-voice-review.mp3')
    reports=[json.loads(p.with_suffix('.json').read_text(encoding='utf8')) for p in paths]
    full=json.loads(fullpath.with_suffix('.json').read_text(encoding='utf8'))
    source=json.loads((FOLDER/'source-manifest.json').read_text(encoding='utf8'))
    assert source['source_git_blob']==full['source_git_blob']=='83b56e12af0ad3d17dec6e415066f8a9e675e1d3'
    assert len(source['recorded_positions'])==len(source['positions'])==35
    assert sum(r['exact_explicit_source_pause_seconds'] for r in reports)==183
    assert all(sha(p.read_bytes())==r['mp3_sha256'] for p,r in zip(paths,reports))
    assert sha(fullpath.read_bytes())==full['mp3_sha256']
    pcm_end=full['pcm_duration_seconds']
    cues={x['id']:x for x in full['cues']}
    scene_in=cues['p2s01']['start_seconds']
    scene_out=cues['p6s01']['start_seconds']
    dryparts=[decode(p.read_bytes()) for p in paths]
    dryfull=decode(fullpath.read_bytes())
    ambient,fade=soundscape(len(dryfull),scene_in,scene_out,pcm_end)
    dry_rms=float(np.sqrt(np.mean((dryfull.astype(np.float64)/32768)**2)))
    amb_rms=float(np.sqrt(np.mean(ambient.astype(np.float64)**2)))
    relative=float(20*np.log10(dry_rms/amb_rms))
    assert relative>18 and max(np.max(abs(x.astype(np.int32))) for x in dryparts)<32767
    wetparts=[];durations=[];cursor=0
    for i,voice in enumerate(dryparts):
        start=round(cursor*FS)
        noise=ambient[start:start+len(voice)]
        if len(noise)<len(voice):noise=np.pad(noise,(0,len(voice)-len(noise)))
        y=voice.astype(np.float32)/32768+noise
        assert np.max(np.abs(y))<.975
        wet=encode(np.rint(y*32767).astype('<i2'))
        wetparts.append(wet);durations.append(len(decode(wet))/FS)
        (stage/f'part{i+1:02}.mp3').write_bytes(wet)
        cursor+=reports[i]['pcm_duration_seconds']
    assert abs(cursor-pcm_end)<.001
    y=dryfull.astype(np.float32)/32768+ambient
    assert np.max(np.abs(y))<.975
    wetfull=encode(np.rint(y*32767).astype('<i2'))
    (stage/'full.mp3').write_bytes(wetfull)
    full_seconds=len(decode(wetfull))/FS
    assert abs(full_seconds-pcm_end)<.12
    metadata=dict(episode=NAME,scene='hillside breeze and distant valley stream',seed=121212,
      narrative_fade_policy='Equal cue-synchronized fades scaled to the short source: from p2s01 landscape entrance and p6s01 return; unchanged source pauses and a continuous calm middle.',
      **fade,ambient_rms=amb_rms,ambient_dbfs=float(20*np.log10(amb_rms)),
      voice_to_ambient_db=relative,source_pause_seconds_unchanged=183,
      source_git_blob=source['source_git_blob'],dry_part_sha256=[sha(p.read_bytes()) for p in paths],
      wet_part_sha256=[sha(p) for p in wetparts],dry_full_sha256=sha(fullpath.read_bytes()),
      wet_full_sha256=sha(wetfull),wet_part_decoded_seconds=durations,
      wet_full_decoded_seconds=full_seconds)
    (stage/'mix-report.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Staged 12',round(pcm_end,2),'seconds, symmetric fades',round(fade['fade_duration_seconds'],2),
          'seconds from p2s01/p6s01, voice/ambient',round(relative,1),'dB')
    if not args.apply:return
    uri=['data:audio/mpeg;base64,'+base64.b64encode(x).decode('ascii') for x in wetparts]
    new=html.replace('const AUDIO=[];','const AUDIO='+json.dumps(uri,separators=(',',':'))+';',1)
    new=new.replace('audio: none yet (built without audio)',
      'audio: six embedded MP3 parts with minimal hillside ambience (183 source pause seconds)',1)
    assert 'const AUDIO=[];' not in new and new.count('parts: 6 | audio:')==1
    for i,(r,data,duration) in enumerate(zip(reports,wetparts,durations),1):
        r['mp3_sha256']=sha(data)
        r['mp3_decoded_duration_seconds']=duration
        r['status']='FINAL MIX WITH HILLSIDE AMBIENCE'
        r['ambience']=fade
        out=FOLDER/(NAME+f'-part{i:02}-review.mp3')
        out.write_bytes(data)
        out.with_suffix('.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    full['mp3_sha256']=sha(wetfull)
    full['mp3_decoded_duration_seconds']=full_seconds
    full['status']='FINAL MIX WITH HILLSIDE AMBIENCE'
    full['ambience']=metadata
    out=FOLDER/(NAME+'-full-review.mp3')
    out.write_bytes(wetfull)
    out.with_suffix('.json').write_text(json.dumps(full,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    htmlpath.write_text(new,encoding='utf8')
    print('Applied 12 final wet audio and six-part self-contained HTML')

if __name__=='__main__':main()
