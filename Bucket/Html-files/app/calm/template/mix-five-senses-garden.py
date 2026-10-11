#!/usr/bin/env python3
"""Stage garden breeze/watering ambience for episode 10's SHORT authoritative text.

The user chose scene-synchronized EXACTLY SYMMETRIC fades, not adding pauses
or padding the 6:08 narration merely to fit the generic 4+3 minute example.
Fade in starts at p2s01; fade out starts at p6s01, finishing at PCM end.
The fade durations are both 53.28s. First build without --apply and QC it.
Requires numpy, scipy, miniaudio, lameenc. Do not run --apply twice.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import numpy as np
from scipy import signal
import lameenc
import miniaudio

FS=24000
NAME='10-five-senses-garden'
ROOT=Path(__file__).resolve().parents[1]/'journey'
FOLDER=ROOT/'audio'/NAME


def sha(data):return hashlib.sha256(data).hexdigest()

def decode(data):
    d=miniaudio.decode(data,output_format=miniaudio.SampleFormat.SIGNED16,nchannels=1,sample_rate=FS)
    assert d.sample_rate==FS and d.nchannels==1
    return np.frombuffer(d.samples,dtype='<i2').copy()

def encode(pcm):
    e=lameenc.Encoder();e.set_channels(1);e.set_in_sample_rate(FS);e.set_bit_rate(96);e.set_quality(2)
    result=bytearray()
    for i in range(0,len(pcm),FS*5):result.extend(e.encode(pcm[i:i+FS*5].tobytes()))
    result.extend(e.flush())
    return bytes(result)

def make_ambience(length,scene_in,scene_out,pcm_end):
    rng=np.random.default_rng(101010)
    # Quiet leafy breeze with a hint of garden water, distinct from the fountain in 04.
    high=signal.sosfilt(signal.butter(2,(400,3000),fs=FS,btype='bandpass',output='sos'),rng.standard_normal(length).astype(np.float32))
    low=signal.sosfilt(signal.butter(2,(160,820),fs=FS,btype='bandpass',output='sos'),rng.standard_normal(length).astype(np.float32))
    sound=(high*.8+low*.28).astype(np.float32)
    del high,low
    # Dispersed soft droplets on leaves/soil. Tapered in/out to avoid transients.
    size=round(.08*FS);t=np.arange(size,dtype=np.float32)/FS
    droplet=np.sin(2*np.pi*520*t)*(1-np.exp(-t*120))*np.exp(-t*47)
    for pos in rng.integers(0,length-size,size=rng.poisson(length/FS*1.7)):
        sound[pos:pos+size] += droplet*rng.uniform(.04,.14)
    # Very slow, low-depth natural modulation: continuous, never an audible loop.
    for a in range(0,length,FS*10):
        b=min(length,a+FS*10)
        time=np.arange(a,b,dtype=np.float64)/FS
        sound[a:b] *= (0.88+.12*np.sin(2*np.pi*.066*time)).astype(np.float32)
    sound-=np.mean(sound,dtype=np.float64)
    rms=float(np.sqrt(np.mean(sound.astype(np.float64)**2)))
    target=.0058
    sound*=target/rms
    fade=pcm_end-scene_out
    assert abs(fade-53.28)<.01 and scene_in+fade<scene_out,fade
    up_start=round(scene_in*FS);up_end=round((scene_in+fade)*FS)
    down_start=round(scene_out*FS);down_end=round(pcm_end*FS)
    assert up_end<down_start<down_end<=length
    env=np.full(length,.04,dtype=np.float32)
    x=np.linspace(0,1,up_end-up_start,dtype=np.float32)
    env[up_start:up_end]=.04+.96*x*x*(3-2*x)
    env[up_end:down_start]=1
    x=np.linspace(0,1,down_end-down_start,dtype=np.float32)
    env[down_start:down_end]=1-x*x*(3-2*x)
    env[down_end:]=0
    env[:FS]*=np.linspace(0,1,FS,dtype=np.float32)
    sound*=env
    assert np.max(np.abs(sound))<.1
    mid=np.sqrt(np.mean(sound[up_end:down_start].astype(np.float64)**2))
    assert .85*target<mid<1.15*target,mid
    return sound,dict(fade_in_start_seconds=scene_in,fade_in_end_seconds=scene_in+fade,
                      fade_out_start_seconds=scene_out,fade_out_end_seconds=pcm_end,
                      fade_duration_seconds=fade,ambient_mid_rms=float(mid),
                      ambient_mid_dbfs=float(20*np.log10(mid)))

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--scratch',type=Path,default=Path('.scratch/ambient-output')/NAME)
    ap.add_argument('--apply',action='store_true')
    args=ap.parse_args()
    out=args.scratch;out.mkdir(parents=True,exist_ok=True)
    htmlpath=ROOT/(NAME+'.html');html=htmlpath.read_text(encoding='utf8')
    assert html.count('const AUDIO=[];')==1
    assert html.count('باغ چهار حس')==3 and 'باغ پنج حس' not in html
    assert html.count('audio: none yet (built without audio)')==1
    ppaths=[FOLDER/(NAME+f'-part{i:02}-voice-review.mp3') for i in range(1,7)]
    fpath=FOLDER/(NAME+'-full-voice-review.mp3')
    reports=[json.loads(p.with_suffix('.json').read_text(encoding='utf8')) for p in ppaths]
    fullreport=json.loads(fpath.with_suffix('.json').read_text(encoding='utf8'))
    source=json.loads((FOLDER/'source-manifest.json').read_text(encoding='utf8'))
    assert source['source_git_blob']==fullreport['source_git_blob']=='913505a9193b3c2123f2b98ac2b0e61628323649'
    assert len(source['recorded_positions'])==len(source['positions'])==31
    assert sum(x['exact_explicit_source_pause_seconds'] for x in reports)==164
    assert all(sha(p.read_bytes())==r['mp3_sha256'] for p,r in zip(ppaths,reports))
    assert sha(fpath.read_bytes())==fullreport['mp3_sha256']
    pcm_end=fullreport['pcm_duration_seconds']
    cues={c['id']:c for c in fullreport['cues']}
    scene_in=cues['p2s01']['start_seconds']
    scene_out=cues['p6s01']['start_seconds']
    dryparts=[decode(p.read_bytes()) for p in ppaths]
    dryfull=decode(fpath.read_bytes())
    ambience,fade=make_ambience(len(dryfull),scene_in,scene_out,pcm_end)
    voice_rms=float(np.sqrt(np.mean((dryfull.astype(np.float64)/32768)**2)))
    ambience_rms=float(np.sqrt(np.mean(ambience.astype(np.float64)**2)))
    voice_to_amb_db=float(20*np.log10(voice_rms/ambience_rms))
    assert voice_to_amb_db>18 and max(map(lambda x: np.max(np.abs(x)),dryparts))<32767
    wetparts=[];part_durations=[];cursor=0
    for i,voice in enumerate(dryparts):
        # Start each section at its exact unencoded PCM offset: encoding padding
        # at prior section boundaries must not shift scene cue times.
        start=round(cursor*FS)
        noise=ambience[start:start+len(voice)]
        if len(noise)<len(voice):noise=np.pad(noise,(0,len(voice)-len(noise)))
        merged=voice.astype(np.float32)/32768+noise
        assert np.max(np.abs(merged))<.975
        mp3=encode(np.rint(merged*32767).astype('<i2'))
        wetparts.append(mp3);part_durations.append(len(decode(mp3))/FS)
        (out/f'part{i+1:02}.mp3').write_bytes(mp3)
        cursor+=reports[i]['pcm_duration_seconds']
    assert abs(cursor-pcm_end)<.001
    merged=dryfull.astype(np.float32)/32768+ambience
    assert np.max(np.abs(merged))<.975
    wetfull=encode(np.rint(merged*32767).astype('<i2'))
    (out/'full.mp3').write_bytes(wetfull)
    decoded_full_seconds=len(decode(wetfull))/FS
    assert abs(decoded_full_seconds-pcm_end)<.12
    metadata=dict(episode=NAME,scene='gentle leaves and distant drops',seed=101010,
       narrative_fade_policy='User requested exact symmetry scaled to the text: equal-length fades from scene entrance p2s01 and return p6s01; no new pauses.',
       **fade,ambient_rms=ambience_rms,ambient_dbfs=float(20*np.log10(ambience_rms)),
       voice_to_ambient_db=voice_to_amb_db,
       source_pause_seconds_unchanged=164,source_git_blob=source['source_git_blob'],
       dry_part_sha256=[sha(p.read_bytes()) for p in ppaths],wet_part_sha256=[sha(p) for p in wetparts],
       dry_full_sha256=sha(fpath.read_bytes()),wet_full_sha256=sha(wetfull),
       wet_part_decoded_seconds=part_durations,wet_full_decoded_seconds=decoded_full_seconds)
    (out/'mix-report.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Staged 10 garden soundscape',round(pcm_end,2),'sec;',
          'symmetric fades',round(fade['fade_duration_seconds'],2),'s at',scene_in,scene_out,
          'voice/ambient',round(voice_to_amb_db,1),'dB')
    if not args.apply:return
    uris=['data:audio/mpeg;base64,'+base64.b64encode(data).decode('ascii') for data in wetparts]
    newhtml=html.replace('const AUDIO=[];','const AUDIO='+json.dumps(uris,separators=(',',':'))+';',1)
    newhtml=newhtml.replace('باغ چهار حس','باغ پنج حس')
    newhtml=newhtml.replace('audio: none yet (built without audio)',
                            'audio: six embedded MP3 parts with minimal garden ambience (164 source pause seconds)',1)
    assert 'const AUDIO=[];' not in newhtml and newhtml.count('باغ پنج حس')==3
    for r,data,seconds in zip(reports,wetparts,part_durations):
        r['mp3_sha256']=sha(data)
        r['mp3_decoded_duration_seconds']=seconds
        r['status']='FINAL MIX WITH GARDEN AMBIENCE'
        r['ambience']=fade
    fullreport['mp3_sha256']=sha(wetfull)
    fullreport['mp3_decoded_duration_seconds']=decoded_full_seconds
    fullreport['status']='FINAL MIX WITH GARDEN AMBIENCE'
    fullreport['ambience']=metadata
    # Leave the voice-only preview tracks and their reports unchanged for audit.
    for i,(data,r) in enumerate(zip(wetparts,reports),1):
        file=FOLDER/(NAME+f'-part{i:02}-review.mp3')
        file.write_bytes(data)
        file.with_suffix('.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    wetpath=FOLDER/(NAME+'-full-review.mp3')
    wetpath.write_bytes(wetfull)
    wetpath.with_suffix('.json').write_text(json.dumps(fullreport,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    htmlpath.write_text(newhtml,encoding='utf8')
    print('Applied 10 final wet audio and self-contained HTML')

if __name__=='__main__':main()
