#!/usr/bin/env python3
"""Embed real .weba bytes into their mapped HTML sections; never generates speech."""
from pathlib import Path
from lxml import html
import argparse,base64,json,hashlib,shutil,subprocess,os,re

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 cli=argparse.ArgumentParser(description=__doc__)
 cli.add_argument('--course-dir',type=Path,default=Path(__file__).resolve().parents[1]);cli.add_argument('--audio-dir',type=Path,required=True);cli.add_argument('--output-dir',type=Path,required=True)
 cli.add_argument('--allow-partial',action='store_true',help='Explicitly assemble only available tracks; absent tracks stay PENDING ASSET.')
 cli.add_argument('--production-manifest',type=Path,help='Optional Arena production receipt with jobs, source hashes and origin evidence.')
 args=cli.parse_args();course=args.course_dir.resolve();audios=args.audio_dir.resolve();output=args.output_dir.resolve()
 if output==course:raise SystemExit('Use a separate output directory; original prepared files are preserved.')
 if not audios.is_dir():raise SystemExit('Audio directory does not exist.')
 maps=[(p,json.loads(p.read_text())) for p in sorted(course.glob('ryazif*-section-audio.json'))]
 if not maps:raise SystemExit('No section-audio mappings found.')
 actual={}
 for p in audios.rglob('*.weba'):
  if p.name in actual:raise SystemExit('Ambiguous duplicate audio filename: '+p.name)
  actual[p.name]=p
 production={}
 if args.production_manifest:
  receipt=json.loads(args.production_manifest.read_text())
  if receipt.get('generation_platform')!='arena.ai':raise SystemExit('Production platform must match the Arena policy.')
  production={x['audio_filename']:x for x in receipt.get('jobs',[])}
 expected={s['audio_filename'] for _,m in maps for s in m['sections'] if s['status']!='N/A'}
 missing=sorted(expected-set(actual))
 if missing and not args.allow_partial:raise SystemExit('Missing '+str(len(missing))+' required audio files; no output written. First missing: '+', '.join(missing[:8])+'. Use --allow-partial only for an intentional partial assembly.')
 inspected={}
 for filename in sorted(expected&set(actual)):
  p=actual[filename]
  with p.open('rb') as f:header=f.read(4)
  if header!=b'\x1aE\xdf\xa3':raise SystemExit('Not a WebM/EBML audio container: '+filename+'; renaming an MP3/WAV is insufficient.')
  info={'sha256':digest(p),'bytes':p.stat().st_size,'duration_seconds':None,'codec_check':'NOT_RUN: ffprobe unavailable'}
  if shutil.which('ffprobe'):
   result=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,codec_name','-of','json',str(p)],capture_output=True,text=True)
   if result.returncode:raise SystemExit('Cannot decode audio container: '+filename)
   probe=json.loads(result.stdout);streams=probe.get('streams',[])
   if not any(s.get('codec_type')=='audio' for s in streams) or any(s.get('codec_type')=='video' for s in streams):raise SystemExit('Expected an audio-only WebM file: '+filename)
   info['duration_seconds']=float(probe.get('format',{}).get('duration',0))
   if info['duration_seconds']<=0:raise SystemExit('Empty or unknown audio duration: '+filename)
   info['codec_check']='PASS';info['codecs']=[s.get('codec_name') for s in streams]
  inspected[filename]=info
 # Validate source hashes and production mapping for all inputs before writing any lesson.
 for mp,m in maps:
  p=course/(m['lesson']+'.html')
  if digest(p)!=m['html_sha256']:raise SystemExit('Source HTML differs from the mapped version: '+p.name)
  if digest(course/(m['lesson']+'.md'))!=m['tts_markdown_sha256']:raise SystemExit('Master TTS differs from the mapped version: '+m['lesson'])
  for s in m['sections']:
   text=re.sub(r'<!--.*?-->','',(course/s['tts_file']).read_text(),flags=re.S)
   text='\n\n'.join(x.strip() for x in re.split(r'\n\s*\n',text) if x.strip() and not x.strip().startswith('#')).strip()
   if hashlib.sha256(text.encode()).hexdigest()!=s['tts_text_sha256']:raise SystemExit('Section TTS differs from the mapped version: '+s['tts_file'])
   if s['audio_filename'] not in inspected:continue
   if args.production_manifest:
    job=production.get(s['audio_filename'])
    if not job or job.get('tts_text_sha256')!=s['tts_text_sha256'] or job.get('html_sha256')!=m['html_sha256']:raise SystemExit('Production receipt/source mismatch: '+s['audio_filename'])
    if not job.get('origin_evidence') or job.get('audio_sha256')!=inspected[s['audio_filename']]['sha256']:raise SystemExit('Production origin or audio hash missing/mismatched: '+s['audio_filename'])
 output.mkdir(parents=True,exist_ok=True);outputs=[];embedded=0
 for mp,m in maps:
  lesson=m['lesson'];source=course/(lesson+'.html');tree=html.fromstring(source.read_text());inline=tree.get_element_by_id('hamyar-section-audio-manifest');inline_data=json.loads(inline.text)
  bysection={x['section_id']:x for x in inline_data['sections']}
  for s in m['sections']:
   filename=s['audio_filename']
   if filename not in inspected:continue
   info=inspected[filename];matches=tree.xpath('//div[@class="section-audio-player"][@data-audio-filename=$name]',name=filename)
   if len(matches)!=1:raise SystemExit('HTML binding must be unique: '+filename)
   box=matches[0];audio=box.find('audio');audio.set('src','data:audio/webm;base64,'+base64.b64encode(actual[filename].read_bytes()).decode());audio.set('data-audio-sha256',info['sha256']);box.set('data-audio-status','READY')
   for b in box.xpath('.//button[@data-audio-play or @data-audio-stop or @data-audio-restart]'):b.attrib.pop('disabled',None)
   box.xpath('.//*[@data-audio-status-text]')[0].text='برای شنیدن این بخش، پخش را بزنید.'
   changes={'status':'READY','embedded':True,'audio_sha256':info['sha256'],'audio_bytes':info['bytes'],'duration_seconds':info['duration_seconds'],'codec_check':info['codec_check']}
   s.update(changes);bysection[s['section_id']].update(changes);embedded+=1
  inline_data['audio_asset_status']='READY' if all(s['status'] in ['READY','N/A'] for s in inline_data['sections']) else 'PENDING ASSET'
  inline.text=json.dumps(inline_data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
  dest=output/source.name;temp=dest.with_suffix('.html.tmp');temp.write_text('<!DOCTYPE html>\n'+html.tostring(tree,encoding='unicode',method='html'));os.replace(temp,dest)
  m['source_html_sha256']=m['html_sha256'];m['html_sha256']=digest(dest)
  m['audio_asset_status']='READY' if all(s['status'] in ['READY','N/A'] for s in m['sections']) else 'PENDING ASSET'
  m['production_origin_verification']='RECEIPT_HASHES_CHECKED' if args.production_manifest else 'NOT_PROVIDED; local assembly only'
  (output/mp.name).write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');shutil.copy2(course/(lesson+'.md'),output/(lesson+'.md'));outputs.append({'html':dest.name,'sha256':digest(dest),'audio_status':m['audio_asset_status']})
  for s in m['sections']:
   t=output/s['tts_file'];t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(course/s['tts_file'],t)
 report={'schema_version':1,'embedded_tracks':embedded,'missing_audio_files':missing,'unmapped_audio_files':sorted(set(actual)-expected),'production_manifest_checked':bool(args.production_manifest),'outputs':outputs,'note':'Playback/listening QC of real teaching recordings remains a separate check; this tool verifies binding, bytes and available container metadata.'}
 (output/'audio-embedding-receipt.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'embedded_tracks':embedded,'missing_tracks':len(missing),'html_files':len(outputs),'output_dir':str(output)},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
