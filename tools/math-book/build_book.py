#!/usr/bin/env python3
"""Build all real grade-nine chapter routes plus the authorised whole-book menu."""
from pathlib import Path
import argparse,base64,copy,hashlib,html,importlib,importlib.util,json,re,subprocess,sys
from collections import Counter
from bank_core import CHAPTERS,LEVELS
from exam_cases import assessment_cases
from review_content import summary,cards
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from teaching_shell import make_page,verify_locked,register_generated
from final_questions import questions as final_questions,MARKS,GROUP_TITLES
from verify_book import run as verify
from verify_final import run as verify_final
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];OLD=HERE.parent/'math-f01'
sys.path.insert(0,str(OLD))
spec=importlib.util.spec_from_file_location('chapter_one_builder',OLD/'build.py');legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
REPORT=ROOT/'reports/math-book';VERSION='2026-10-18.book-1'

def native_text(text):
 text=str(text).translate(legacy.DIGITS)
 text=re.sub('⁻?[⁰¹²³⁴⁵⁶⁷⁸⁹]+',lambda m:'^('+''.join('−' if c=='⁻' else '۰۱۲۳۴۵۶۷۸۹'['⁰¹²³⁴⁵⁶⁷⁸⁹'.index(c)] for c in m.group())+')',text)
 return re.sub('[₀-₉]+',lambda m:'_('+''.join('۰۱۲۳۴۵۶۷۸۹'[ord(c)-8320] for c in m.group())+')',text)

def final_body(label):
 return '<section class="intro"><span class="badge">'+label+'</span><h2>خودآزمایی جامع پایان سال</h2><p>شانزده سؤال اصلی در چهار صفحه، با بارم کل بیست و زمان پیشنهادی نود دقیقه؛ پاسخ و نتیجه تا پایان پنهان می‌ماند.</p><p>راه‌حل را بنویس؛ سؤال‌های اثباتی و رسم با راهنمای بارم‌بندی بررسی می‌شوند.</p><p id="paper-progress" role="status"></p></section><section id="paper-confirm" hidden><p id="paper-warning"></p><div class="controls"><button id="paper-finish-yes" type="button">پایان آزمون و شروع بررسی</button><button id="paper-finish-no" type="button">ادامهٔ پاسخ‌گویی</button></div></section><section id="paper-result" class="result-box" tabindex="-1" aria-live="polite" hidden></section><div id="paper-pages"></div><div class="controls"><button id="paper-finish" type="button" class="primary">پایان آزمون و بررسی پاسخ‌ها</button><button id="paper-restart" type="button" hidden>آزمون دوباره</button></div>'

def flash_body():return '<section class="intro"><span class="badge">مرور فعال</span><h2>پاسخ را به یاد بیاور و کارت را برگردان</h2><p>هر بار یک کارت نمایش داده می‌شود؛ وضعیت مرور تو در اپ نگه‌داری می‌شود.</p></section><section class="flash-deck"><div class="deck-status"><strong id="flash-position"></strong><span id="flash-reviewed"></span></div><div id="flash-list"></div><div class="controls deck-controls"><button id="flash-prev" type="button">کارت قبلی</button><button id="flash-next" type="button">کارت بعدی</button></div></section>'

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--app',type=Path,default=Path('/workspace/hamyar-math-app'));args=parser.parse_args();app=args.app
 verify_locked()
 verification=verify();final_verification=verify_final();REPORT.mkdir(parents=True,exist_ok=True)
 subprocess.run([sys.executable,str(OLD/'build.py'),'--app',str(app)],check=True)
 menu_path=app/'grades/g09/src/main/assets/content/books-menu.json';menu=json.loads(menu_path.read_text());original_books=copy.deepcopy(menu['books']);book=next(x for x in menu['books'] if x['code']=='905')
 real=[c for c in book['items'] if c['title'].startswith('فصل ')]
 assert len(real)==8,'Actual book chapter count changed; inspect menu before building.'
 whole=next((c for c in book['items'] if c['title']=='مرور جامع کل کتاب'),None)
 if whole is None:
  position=len(book['items'])+1;node=f'N{position}.1'
  tabs=[dict(title=label,key=f'Bucket/Html-files/app/books/C905/{node}/TAB{num:02d}.html',ready=True) for num,label in [(2,'فلش‌کارت‌های کل کتاب'),(3,'خلاصه و نکات امتحانی کل کتاب'),(4,'نمونه‌سؤالات جامع کل کتاب'),(5,'خودآزمایی نهایی کل کتاب')]]
  wrap=dict(kind='wrapup',title='مرور و تمرین کل کتاب',key=None,ready=True,teachKey=None,audioKey=None,tabs=tabs,children=[])
  whole=dict(kind='container',title='مرور جامع کل کتاب',key=None,ready=True,teachKey=None,audioKey=None,tabs=[],children=[wrap]);book['items'].append(whole)
 menu_path.write_text(json.dumps(menu,ensure_ascii=False,indent=2)+'\n')
 assert [b for b in menu['books'] if b['code']!='905']==[b for b in original_books if b['code']!='905']
 runtime=(OLD/'runtime.js').read_text();final_runtime=(HERE/'final-runtime.js').read_text()
 manifest_path=app/'grades/g09/src/main/assets/content/math-practice-routes.json';routes=[r for r in json.loads(manifest_path.read_text())['routes'] if '/N2.5/' in r['bucketKey']];generated=[];scopes=[]
 banks={1:json.loads((ROOT/'reports/math-f01/canonical-bank.json').read_text())};allcards={1:[dict(id=f'f01-card-{i+1:02d}',topic=t,front=f,back=b,chapterNumber=1) for i,(t,f,b) in enumerate(legacy.CARDS)]}
 for ch in range(2,9):banks[ch]=importlib.import_module(f'ch{ch:02d}').questions(0);allcards[ch]=cards(ch)
 for ch in range(2,9):
  for i,q in enumerate(banks[ch],1):q['id']=f'f{ch:02d}-bank-q{i:02d}'
 def page(ch,directory,filename,title,body,kind,mode,qs=None,cs=None,variant=0):
  scope=f'f{ch:02d}';chapter_title=real[ch-1]['title'] if ch else 'مرور جامع کل کتاب';pack=f'C905_E{ch:02d}-SUM';id=scope+'-'+filename[:-5].lower()
  data=dict(id=id,scopeId=scope,chapterNumber=ch,chapterTitle=chapter_title,packId=pack,kind=kind,mode=mode,variant=variant,contentVersion=VERSION)
  if mode in ('assessment','final'):data['contentVersion']='2026-10-19.qa-fix-1'
  if qs is not None:data['questions']=qs
  if cs is not None:data['cards']=cs
  if mode=='final':data.update(groupTitles=GROUP_TITLES,mainQuestionMarks=MARKS,totalMarks=20,suggestedMinutes=90)
  output=ROOT/directory/filename;output.parent.mkdir(parents=True,exist_ok=True)
  asset=app/'grades/g09/src/main/assets/math/c905/practice'/directory.name/filename;asset.parent.mkdir(parents=True,exist_ok=True)
  scripts=('<script>'+final_runtime+'</script>' if mode=='final' else '')+'<script>'+runtime+'</script>'
  text=legacy.persian_html(make_page(output,asset,title,data,body,scripts,(HERE/'book.css').read_text()))
  output.write_text(text);asset.write_text(text)
  routes.append(dict(bucketKey=str(directory/filename),assetPath='math/c905/practice/'+directory.name+'/'+filename,packId=pack,kind=kind))
  generated.append(dict(path=str(directory/filename),scope=ch,mode=mode,questions=len(qs or []),sha256=hashlib.sha256(text.encode()).hexdigest()))
  return data
 for ch in [*range(2,9),0]:
  item=real[ch-1] if ch else whole;wrap=next(n for n in item['children'] if n['kind']=='wrapup');directory=Path(next(t['key'] for t in wrap['tabs'] if t['key'].endswith('/TAB02.html'))).parent
  qs=banks[ch] if ch else [copy.deepcopy(q) for n in range(1,9) for q in banks[n]]
  if not ch:
   for i,q in enumerate(qs,1):q['canonicalRefId']=q['id'];q['id']=f'f00-bank-q{i:03d}'
  cs=allcards[ch] if ch else [dict(c,topic=CHAPTERS[n]+' · '+c['topic']) for n in range(1,9) for c in allcards[n]]
  body=summary(ch) if ch else '<section class="intro"><span class="badge">نقشهٔ مرور کل کتاب</span><h2>هشت فصل، یک مسیر مرور</h2><p>تعریف‌ها و فرمول‌ها را مرور کن، خطاهای پرتکرار را بخوان و در پایان یک برگهٔ جامع بیست‌نمره‌ای را با نوشتن راه‌حل انجام بده.</p></section>'+''.join('<details class="whole-summary"><summary>'+real[n-1]['title']+'</summary>'+(legacy.SUMMARY if n==1 else summary(n))+'</details>' for n in range(1,9))
  page(ch,directory,'TAB03.html','خلاصه و نکات امتحانی '+(CHAPTERS[ch] if ch else 'کل کتاب'),body,'summary','summary')
  page(ch,directory,'TAB02.html','فلش‌کارت‌های '+(CHAPTERS[ch] if ch else 'کل کتاب'),flash_body(),'flash','flash',cs=cs)
  page(ch,directory,'TAB04.html','نمونه‌سؤالات جامع '+(CHAPTERS[ch] if ch else 'کل کتاب'),legacy.exam_body('تمرین همراه با تحلیل خطا'),'exam','sample',qs=qs)
  exams=[];slugs=['easy','medium','hard','brilliant']
  for level,(slug,label) in enumerate(zip(slugs,LEVELS),1):
   links=[]
   for v in range(1,7):
    if ch:
     items=assessment_cases(ch,[q for q in importlib.import_module(f'ch{ch:02d}').questions(v) if q['level']==level and q['type']!='essay'],v)
     for i,q in enumerate(items,1):q['id']=f'f{ch:02d}-{slug}-v{v}-q{i:02d}'
     body=legacy.exam_body('سطح '+label+' · نسخهٔ '+str(v),assessment=True);mode='assessment'
    else:items=final_questions(level,v);body=final_body('سطح '+label+' · برگهٔ '+str(v));mode='final'
    filename=f'TAB05-{slug}-{v:02d}.html';page(ch,directory,filename,('خودآزمایی '+CHAPTERS[ch] if ch else 'خودآزمایی نهایی کل کتاب')+'؛ '+label+'، نسخهٔ '+str(v),body,'exam',mode,qs=items,variant=v);links.append('<a href="'+filename+'">'+('آزمون ' if ch else 'برگهٔ نهایی ')+str(v)+'</a>');exams.append(dict(level=label,variant=v,filename=filename,questions=items))
   if v==6:exams[-1]['menu']='<section class="level-card"><h2>'+label+'</h2><p>'+('تمرین مستقل همین فصل؛ پاسخ‌ها تا پایان قابل ویرایش‌اند.' if ch else 'فرم نهایی: شانزده سؤال اصلی، بیست نمره و بارم هر بخش مشخص است.')+'</p><div class="exam-links">'+''.join(links)+'</div></section>'
  index='<section class="intro"><span class="badge">۲۴ آزمون مستقل</span><h2>'+('انتخاب سطح و آزمون فصل' if ch else 'انتخاب خودآزمایی نهایی کل کتاب')+'</h2><p>چهار سطح، هرکدام شش فایل مستقل؛ پاسخ صحیح و نتیجه پس از پایان نمایش داده می‌شود.</p></section><div class="level-grid">'+''.join(e.get('menu','') for e in exams)+'</div>'
  page(ch,directory,'TAB05.html','خودآزمایی '+(CHAPTERS[ch] if ch else 'کل کتاب')+'؛ انتخاب آزمون',index,'exam','assessment-index')
  scopes.append(dict(scope=ch,title=item['title'],directory=str(directory),packId=f'C905_E{ch:02d}-SUM',bankCount=len(qs),flashcards=len(cs),difficulty=dict(Counter(q['difficulty'] for q in qs)),types=dict(Counter(q['type'] for q in qs)),assessmentFiles=24,assessmentItems=sum(len(e['questions']) for e in exams)))
  (REPORT/f'assessments-{ch:02d}.json').write_text(json.dumps(exams,ensure_ascii=False,indent=2)+'\n')
  (REPORT/f'bank-{ch:02d}.json').write_text(json.dumps(qs,ensure_ascii=False,indent=2)+'\n')
  print('BUILT:',ch,item['title'],len(qs),'bank questions;',len(cs),'cards;',sum(len(e['questions']) for e in exams),'exam parts',flush=True)
 manifest=dict(schemaVersion=1,bookCode='C905',sourceMenu=str(menu_path),scopes=[dict(scope=1,packId='C905_E01-SUM',directory='Bucket/Html-files/app/books/C905/N2.5')]+[dict(scope=s['scope'],packId=s['packId'],directory=s['directory']) for s in scopes],routes=routes)
 assert len(routes)==252 and len({r['bucketKey'] for r in routes})==len(routes)
 manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');(REPORT/'routes.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 # Register missing study metadata and native flashcard content in the existing model.
 resource=app/'grades/g09/src/main/resources/math_c905.json';packs=json.loads(resource.read_text());template=next(x for x in packs if x['packId']=='C905_E01-SUM')
 for ch in [*range(1,9),0]:
  id=f'C905_E{ch:02d}-SUM';pack=next((p for p in packs if p['packId']==id),None)
  if pack is None:pack=copy.deepcopy(template);pack.update(packId=id,lessonId=f'E{ch:02d}-SUM',title='مرور جامع کل کتاب' if not ch else f'جمع‌بندی فصل {ch}',audioFileId='',teachHtml='',teachText='',teachSpeech='');packs.append(pack)
  values=allcards[ch] if ch else [c for n in range(1,9) for c in allcards[n]]
  pack['flashcards']=[dict(id=c['id'],front=native_text(c['front']),back=native_text(c['back']),topic=native_text(c['topic']),hint='') for c in values]
  pack['title']=('مرور جامع کل کتاب' if not ch else f'جمع‌بندی فصل {ch}').translate(legacy.DIGITS)
 resource.write_text(json.dumps(packs,ensure_ascii=False,indent=2)+'\n')
 report=dict(contentVersion=VERSION,assessmentContentVersion='2026-10-19.qa-fix-1',grade=9,book='ریاضی نهم',actualChapterCount=8,newScopes=scopes,allHtmlFiles=252,newHtmlFiles=len(generated),allChapterExams=192,wholeBookFinalExams=24,totalIndependentExamFiles=216,uniqueCanonicalQuestions=sum(len(q) for q in banks.values()),newUniqueQuestions=sum(len(banks[ch]) for ch in range(2,9)),wholeBankIsSharedCanonicalPool=True,generatedFiles=generated,verification=verification['checks'],finalVerification=final_verification,reference='teaching - template/lesson-template.preview-standalone.html',font='Vazir 30.1.0 Farsi-Digits',sourceSectionInHtml=False,storage='Existing Hamyar bridge and account-scoped LocalStore; per pack, kind and document',appMenuPath=str(menu_path),appStudyResourcePath=str(resource))
 (REPORT/'build-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 register_generated()
 print('PASS: 252 standalone HTML files and the whole-book native menu.',flush=True)
if __name__=='__main__':main()
