#!/usr/bin/env python3
"""Export spoken-only, speaker-labelled Arena inputs without filenames/headings/comments."""
from pathlib import Path
import argparse,json,re,hashlib

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def body(markdown):
 text=re.sub(r'<!--.*?-->','',markdown,flags=re.S)
 return '\n\n'.join(x.strip() for x in re.split(r'\n\s*\n',text) if x.strip() and not x.strip().startswith('#')).strip()
def main():
 cli=argparse.ArgumentParser(description=__doc__);cli.add_argument('--course-dir',type=Path,default=Path(__file__).resolve().parents[1]);cli.add_argument('--output-dir',type=Path,required=True);args=cli.parse_args()
 course=args.course_dir.resolve();output=args.output_dir.resolve();jobs=[];skipped=[]
 for mp in sorted(course.glob('ryazif*-section-audio.json')):
  data=json.loads(mp.read_text());lesson=data['lesson'];html=course/(lesson+'.html')
  if digest(html)!=data['html_sha256']:raise SystemExit('HTML changed since mapping: '+html.name)
  for s in data['sections']:
   if s['status']=='N/A':
    skipped.append({'lesson':lesson,'section_id':s['section_id']})
    stale=output/lesson/(Path(s['audio_filename']).stem+'.tts.txt')
    if stale.exists():stale.unlink()
    continue
   spoken=body((course/s['tts_file']).read_text())
   if hashlib.sha256(spoken.encode()).hexdigest()!=s['tts_text_sha256']:raise SystemExit('TTS changed since mapping: '+s['tts_file'])
   target=output/lesson/(Path(s['audio_filename']).stem+'.tts.txt');target.parent.mkdir(parents=True,exist_ok=True);target.write_text(spoken+'\n')
   jobs.append({'lesson':lesson,'section_id':s['section_id'],'title':s['title'],'tts_input':str(target.relative_to(output)),'audio_filename':s['audio_filename'],'html_sha256':data['html_sha256'],'tts_text_sha256':s['tts_text_sha256'],'generation_platform':'arena.ai','audio_sha256':None,'origin_evidence':None})
 output.mkdir(parents=True,exist_ok=True)
 (output/'audio-production-manifest.template.json').write_text(json.dumps({'schema_version':1,'generation_platform':'arena.ai','status':'AWAITING_REAL_AUDIO','jobs':jobs,'not_spoken_sections':skipped},ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'tts_jobs':len(jobs),'non_spoken_sections':len(skipped),'output_dir':str(output)},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
