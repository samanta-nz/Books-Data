#!/usr/bin/env python3
"""Validate source-take ZIPs and render a voice-only section preview for 08/10.

The complete episode and soundscape must be built only after every source cue
has a reviewed take. Section previews are deliberately NOT embedded into HTML.
Requires numpy, praat-parselmouth, miniaudio and lameenc for rendering;
--check needs only the Python standard library.
"""
import argparse
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import wave
from zipfile import ZipFile

CALM=Path(__file__).resolve().parents[1]
EPISODES={'08-safe-mental-refuge':(5,45,250), '10-five-senses-garden':(6,31,164)}
FS=24000


def inventory(name, source=None):
    folder=CALM/'journey/audio'/name
    m=json.loads((folder/'source-manifest.json').read_text(encoding='utf8'))
    assert m['voice_selection'].startswith('voice-08') and m['approved_speaking_speed']==1.0
    assert (len(m['sections']),len(m['positions']),m['source_pause_seconds'])==EPISODES[name]
    if source:
        data=Path(source).read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert (blob,hashlib.sha256(data).hexdigest())==(m['source_git_blob'],m['source_sha256'])
    cues={x['id']:x for x in m['positions']}
    assert len(cues)==len(m['positions'])
    seen={}
    for p in sorted(folder.glob('source-clips-batch*.zip')):
        with ZipFile(p) as z:
            assert z.testzip() is None
            chk=json.loads(z.read('checkpoint.json'))
            assert (chk['source_git_blob'],chk['source_sha256'],chk['voice_id'],chk['speed']) == (m['source_git_blob'],m['source_sha256'],'voice-08',1.0)
            for x in chk['completed_positions']:
                ident=x['id'];assert ident in cues and ident not in seen,ident
                cue=cues[ident]
                assert (x['source_text'],x['source_pause_after_seconds'])==(cue['source_text'],cue['source_pause_after_seconds']),ident
                # Only the earlier user-approved 'حالا باهم، دم' extension may alter source speech.
                expected=cue['source_text'].replace('دم،','حالا باهم، دم')
                assert x['text'] in (cue['source_text'],expected),ident
                if x['text']!=cue['source_text']:
                    assert 'reused_from_episode' in x,ident
                raw=z.read('raw/'+x['raw_asset'])
                assert hashlib.sha256(raw).hexdigest()==x['sha256'],ident
                with wave.open(io.BytesIO(raw)) as w:
                    assert (w.getnchannels(),w.getsampwidth(),w.getframerate())==(1,2,FS)
                    assert w.getnframes()/FS==x['duration_seconds']
                seen[ident]=(p.name,x,raw)
    assert set(seen)==set(m['recorded_positions'])
    missing=[x['id'] for x in m['positions'] if x['id'] not in seen]
    return m,seen,missing


def processor():
    # Use the already-approved F0 processing from episode 04 (-20% max voiced F0).
    spec=importlib.util.spec_from_file_location('voice_processing',Path(__file__).with_name('render-secret-garden-review.py'))
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.process_pcm


def render(name,part,m,seen):
    import numpy as np
    import lameenc
    import miniaudio
    cues=[x for x in m['positions'] if x['id'].startswith(f'p{part}s')]
    missing=[x['id'] for x in cues if x['id'] not in seen]
    if missing:raise ValueError(f'Refusing an incomplete section: {missing}')
    process=processor()
    chunks=[];events=[];offset=0
    for x in cues:
        archive,entry,raw=seen[x['id']]
        pcm,pitch=process(raw)
        pause=x['source_pause_after_seconds']
        events.append(dict(id=x['id'],text=entry['text'],source_pause_seconds=pause,
                           start_seconds=offset/FS,speech_samples=len(pcm),
                           source_archive=archive,**pitch))
        chunks.extend((pcm,np.zeros(FS*pause,dtype='<i2')))
        offset+=len(pcm)+FS*pause
    assert sum(x['source_pause_seconds'] for x in events)==m['sections'][part-1]['source_pause_seconds']
    joined=np.concatenate(chunks)
    assert len(joined)==offset
    enc=lameenc.Encoder();enc.set_channels(1);enc.set_in_sample_rate(FS)
    enc.set_bit_rate(96);enc.set_quality(2)
    audio=bytearray()
    for k in range(0,len(joined),FS*5):audio.extend(enc.encode(joined[k:k+FS*5].tobytes()))
    audio.extend(enc.flush())
    d=miniaudio.decode(bytes(audio),output_format=miniaudio.SampleFormat.SIGNED16,nchannels=1,sample_rate=FS)
    assert abs(d.num_frames-len(joined))<FS*.12
    folder=CALM/'journey/audio'/name
    output=folder/(name+f'-part{part:02}-voice-review.mp3')
    output.write_bytes(audio)
    report={'episode':name,'part':part,'status':'VOICE-ONLY PREVIEW; no ambience; do not embed in HTML yet',
            'source_git_blob':m['source_git_blob'],'voice_id':'voice-08','speed':1.0,
            'max_voiced_F0_ratio':.8,'positions':len(events),
            'exact_explicit_source_pause_seconds':sum(x['source_pause_seconds'] for x in events),
            'pcm_duration_seconds':len(joined)/FS,'mp3_decoded_duration_seconds':d.num_frames/FS,
            'mp3_sha256':hashlib.sha256(audio).hexdigest(),'cues':events}
    output.with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Rendered voice-only preview',name,'part',part,len(audio),'bytes,',round(len(joined)/FS,2),'seconds')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('episode',choices=EPISODES)
    ap.add_argument('--source',type=Path,help='optional authenticated Read-Only-Books-Data .md for hash verification')
    ap.add_argument('--check',action='store_true')
    ap.add_argument('--part',type=int)
    args=ap.parse_args()
    m,seen,missing=inventory(args.episode,args.source)
    print(args.episode,f'{len(seen)}/{len(m["positions"])} raw takes verified, {len(missing)} remaining')
    if args.check:return
    if args.part not in range(1,len(m['sections'])+1):ap.error('pass a valid --part for voice-only preview')
    render(args.episode,args.part,m,seen)


if __name__=='__main__':main()
