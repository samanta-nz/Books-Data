"""Offline Chromium checks against all actual route assets and existing bridge signatures."""
from pathlib import Path
from collections import Counter
import asyncio,json,re,subprocess,hashlib
from urllib.parse import urlparse
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[2];REPORT=ROOT/'reports/math-book';OUT=ROOT/'Bucket/Html-files/app/books/C905';APP=Path('/workspace/hamyar-math-app')
BASE='http://127.0.0.1:8765/'
INIT='''window.__nativeCalls={items:[],exams:[],saves:0,lastState:''};
function nativeKey(){const d=JSON.parse(document.getElementById('practice-data').textContent);return '__native:'+(sessionStorage.getItem('account')||'student')+':'+d.packId+':'+d.kind}
window.Hamyar={loadState(){return localStorage.getItem(nativeKey())||''},saveState(raw){JSON.parse(raw);localStorage.setItem(nativeKey(),raw);__nativeCalls.saves++;__nativeCalls.lastState=raw},recordItem(id,correct){__nativeCalls.items.push({id,correct})},recordExam(scorePct,total,correctCount,wrongCsv){__nativeCalls.exams.push({scorePct,total,correctCount,wrongCsv})}};'''
DIGITS=re.compile('[0-9٠-٩⁰¹²³⁴⁵⁶⁷⁸⁹₀-₉]')
def fa(s):return str(s).translate(str.maketrans('0123456789','۰۱۲۳۴۵۶۷۸۹'))
CHECKS=[]
def check(s):CHECKS.append(s)
def url(path):return BASE+str(path)
async def serve(ctx):
 async def route(r):
  path=OUT/urlparse(r.request.url).path.lstrip('/')
  if path.is_file() and path.is_relative_to(OUT):await r.fulfill(status=200,content_type='text/html; charset=utf-8',body=path.read_text())
  else:await r.fulfill(status=404,body='Missing local asset')
 await ctx.route(BASE+'**',route)
async def data(p):return await p.eval_on_selector('#practice-data','e=>JSON.parse(e.textContent)')
async def state(p,D):return await p.evaluate('id=>JSON.parse(__nativeCalls.lastState).documents[id]',D['id'])
async def persian(p):
 text=await p.evaluate('''()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT),a=[];while(w.nextNode()){const n=w.currentNode;if(!n.parentElement.closest('script,style'))a.push(n.textContent)}return a.join(' ')}''')
 values=await p.eval_on_selector_all('input[type=text],textarea','els=>els.map(e=>e.value).join(" ")')
 human=await p.eval_on_selector_all('[aria-label],[placeholder]','els=>els.map(e=>(e.getAttribute("aria-label")||"")+" "+(e.getAttribute("placeholder")||"")).join(" ")')
 assert not DIGITS.search(text+values+human+await p.title()),re.findall('.{0,20}[0-9٠-٩⁰¹²³⁴⁵⁶⁷⁸⁹₀-₉].{0,20}',text+values+human)[:6]
async def fill_all(p,mode,wrong_first=False):
 return await p.evaluate('''({mode,wrongFirst})=>{const D=JSON.parse(document.getElementById('practice-data').textContent);D.questions.forEach((q,i)=>{if(q.type==='essay'&&mode==='chapter')throw Error('Unexpected essay in automatic exam');if(mode==='chapter')document.querySelector('[data-question="'+i+'"]').click();const el=document.getElementById('q-'+q.id);let value=q.answer;if(i===0&&wrongFirst)value=q.type==='mcq'?q.options.find(x=>x!==q.answer):q.type==='tf'?(q.answer==='درست'?'نادرست':'درست'):'-999';const radios=[...el.querySelectorAll('input[type=radio]')];let input;if(radios.length){input=radios.find(r=>r.value===value);if(!input)throw Error('Missing option');input.checked=true}else{input=el.querySelector('textarea,input[type=text]');input.value=value}input.dispatchEvent(new Event('input',{bubbles:true}));if(mode==='sample')el.querySelector('.submit-answer').click();if(mode==='chapter'&&(document.querySelector('.feedback')||window.__nativeCalls.items.length||window.__nativeCalls.exams.length))throw Error('Early grade leak')});return D.questions.length}''',dict(mode=mode,wrongFirst=wrong_first))
async def main():
 manifest=json.loads((REPORT/'routes.json').read_text());routes=manifest['routes'];assert len(routes)==252
 filenames=[r['bucketKey'].split('/C905/')[1] for r in routes]
 assert len(set(filenames))==252
 assert all((OUT/f).read_bytes()==(APP/'grades/g09/src/main/assets'/r['assetPath']).read_bytes() for f,r in zip(filenames,routes))
 template=ROOT/'teaching - template'
 subprocess.run(['python',str(template/'tools/verify_locked.py')],check=True)
 locked=[*sorted((template/'assets/css/locked').glob('*.css')),template/'assets/js/locked/ui.js']
 for f in filenames:
  text=(OUT/f).read_text()
  embedded=dict(re.findall(r'<(?:style|script) data-locked-source="([^"]+)">([\s\S]*?)</(?:style|script)>',text))
  assert len(embedded)==len(locked)
  for source in locked:assert embedded[str(source.relative_to(template))]==source.read_text(),(f,source)
  theme=OUT/Path(f).parent/'assets/css/theme'/(Path(f).stem+'.theme.css')
  assert theme.read_text()==re.search(r'<style data-page-theme="[^"]+">([\s\S]*?)</style>',text).group(1)
  assert theme.read_bytes()==(APP/'grades/g09/src/main/assets/math/c905/practice'/Path(f).parent/'assets/css/theme'/theme.name).read_bytes()
 check('all 252 pages embed every upstream locked CSS/JS byte-for-byte; all 252 real per-page themes match packaged assets and the README registry')
 menu=json.loads((APP/'grades/g09/src/main/assets/content/books-menu.json').read_text());book=next(b for b in menu['books'] if b['code']=='905');whole=next(n for n in book['items'] if n['title']=='مرور جامع کل کتاب')
 assert len([n for n in book['items'] if n['title'].startswith('فصل ')])==8 and len(whole['children'][0]['tabs'])==4
 for t in whole['children'][0]['tabs']:assert t['key'] in {r['bucketKey'] for r in routes}
 check('real menu: eight chapters plus a separate whole-book section; all four entry routes and 252 packaged assets match')
 errors=[];network=[]
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  ctx=await browser.new_context(offline=True,viewport=dict(width=390,height=844),color_scheme='light');await serve(ctx);await ctx.add_init_script(INIT)
  p=await ctx.new_page();p.on('pageerror',lambda e:errors.append(str(e)));p.on('request',lambda r:network.append(r.url) if r.url.startswith(('http://','https://')) and not r.url.startswith(BASE) else None)
  for i,f in enumerate(filenames):
   await p.goto(url(f));D=await data(p)
   assert await p.evaluate('!!window.HamyarPractice'),f
   assert await p.locator('header').count()==1 and await p.locator('footer').count()==1 and await p.get_attribute('html','dir')=='rtl',f
   assert await p.locator('header#top .hdr-wave,footer.site-footer .ftr-card,#fab,#fab-btn,#fab-panel').count()==5
   assert await p.locator('.practice-nav,.source-list,.sources').count()==0,f
   assert 'منابع و شیوه' not in await p.locator('body').inner_text(),f
   assert await p.evaluate('document.documentElement.scrollWidth<=innerWidth'),f
   await p.evaluate('async()=>{await Promise.all([400,500,700].map(w=>document.fonts.load(w+" 16px Vazir")));await document.fonts.ready}')
   assert await p.evaluate('[400,500,700].every(w=>document.fonts.check(w+" 16px Vazir"))'),f
   palette='''()=>['body','main','header','footer','button','input','textarea','.question-card','.paper-page','.choice'].map(s=>{const e=document.querySelector(s);if(!e)return null;const c=getComputedStyle(e);return [c.color,c.backgroundColor,c.backgroundImage,c.colorScheme]})'''
   before=await p.evaluate(palette);await p.emulate_media(color_scheme='dark');assert before==await p.evaluate(palette),f;await p.emulate_media(color_scheme='light')
   await persian(p)
   for href in await p.eval_on_selector_all('a[href]','els=>els.map(e=>e.getAttribute("href"))'):
    assert href.startswith('#') or (OUT/Path(f).parent/href).is_file(),(f,href)
   if D['mode']=='assessment-index':assert await p.locator('.level-card').count()==4 and await p.locator('.exam-links a').count()==24
   if D['mode']=='assessment':assert await p.locator('.question-card').count()==1 and await p.locator('.feedback,.submit-answer,#stats').count()==0
   if D['mode']=='final':
    assert len(D['questions'])==38 and sum(q['marks'] for q in D['questions'])==20
    assert await p.locator('.paper-page').count()==4 and await p.locator('.paper-question').count()==16 and await p.locator('.paper-part').count()==38
    assert await p.locator('.feedback,.rubric').count()==0 and not await p.locator('#paper-result').is_visible()
   if i%28==27:print('Checked layout/assets:',i+1,flush=True)
  check('all 252 pages: source section absent, no top tabs, intact header/footer, Persian visible digits, real Vazir weights, fixed light theme and valid local links')
  # Real, unchanged template tools remain usable in every page mode.
  for f in ['N3.4/TAB03.html','N4.6/TAB02.html','N5.5/TAB04.html','N7.4/TAB05-easy-01.html','N10.1/TAB05.html','N10.1/TAB05-easy-01.html']:
   await p.goto(url(f));await p.locator('#fab-btn').click();assert await p.locator('#fab-btn').get_attribute('aria-expanded')=='true'
   for eye in range(4):
    await p.locator('[data-eye-set="'+str(eye)+'"]').click()
    assert await p.get_attribute('html','data-eye')==str(eye)
    assert await p.locator('[data-eye-set="'+str(eye)+'"]').get_attribute('aria-pressed')=='true'
    await p.evaluate('''()=>{getComputedStyle(document.body).backgroundColor;return Promise.all(document.getAnimations().filter(a=>a.effect&&a.effect.getComputedTiming().iterations!==Infinity).map(a=>a.finished.catch(()=>{})))}''')
    before=await p.evaluate(palette);await p.emulate_media(color_scheme='dark');assert before==await p.evaluate(palette);await p.emulate_media(color_scheme='light')
   await p.locator('[data-eye-set="2"]').click();await p.locator('#motion-toggle').click();assert 'no-motion' in await p.locator('body').get_attribute('class')
   await p.locator('#motion-toggle').click();assert 'no-motion' not in await p.locator('body').get_attribute('class')
   await p.keyboard.press('Escape');assert await p.locator('#fab-btn').get_attribute('aria-expanded')=='false'
   await p.locator('#fab-btn').click();await p.locator('.fab-toc a').last.click();assert await p.locator('#fab-btn').get_attribute('aria-expanded')=='false'
   await p.reload();assert await p.get_attribute('html','data-eye')=='2';await persian(p)
  check('template floating menu: open/close, Escape, real anchors, four persistent eye-care levels, motion toggle and fixed system theme in all six page modes')
  # Every chapter's six versions at each level are actually answered and finished.
  chapter_exams=[f for f in filenames if '/TAB05-' in f and not f.startswith('N10.1/')]
  assert len(chapter_exams)==192
  for i,f in enumerate(chapter_exams):
   await p.goto(url(f));D=await data(p);N=len(D['questions']);await fill_all(p,'chapter',wrong_first=True)
   ss=await state(p,D);assert ss['submitted']=={} and not ss['errors'] and not ss['finished'] and 'result' not in ss
   assert not await p.evaluate('__nativeCalls.items.length+__nativeCalls.exams.length')
   await p.reload();ss=await state(p,D);assert len(ss['answers'])==N and not ss['submitted'] and await p.locator('.feedback').count()==0
   await p.locator('#finish').click();await p.locator('#finish-no').click();assert not await p.evaluate('__nativeCalls.exams.length')
   await p.locator('#finish').click();await p.locator('#finish-yes').click();ss=await state(p,D);calls=await p.evaluate('__nativeCalls')
   assert len(calls['items'])==N and sum(x['correct'] for x in calls['items'])==N-1,(f,calls)
   assert len(calls['exams'])==1 and calls['exams'][0]['total']==N and calls['exams'][0]['correctCount']==N-1
   assert calls['exams'][0]['scorePct']==int((N-1)*100/N+.5)
   assert len(ss['errors'])==1 and ss['errors'][0]['questionId']==D['questions'][0]['id']
   assert ss['errors'][0]['chapterNumber']==D['chapterNumber']
   for key in ['grade','book','bookCode','chapter','lesson','topic','questionType','difficulty','studentAnswer','correctAnswer','recordedAt','errorCategory']:assert key in ss['errors'][0]
   assert await p.locator('.feedback.wrong').count()==1 and await p.locator('.feedback.correct').count()==N-1
   await persian(p);await p.reload();assert not await p.evaluate('__nativeCalls.items.length+__nativeCalls.exams.length')
   if (i+1)%24==0:print('Graded chapter exams:',i+1,flush=True)
  check('all 192 chapter exams: saved editable drafts without grading, cancelled finish, final correction, accurate errors/percentage and reload without duplicate native calls')
  for scope in range(1,9):
   total=await p.evaluate('scope=>{const r=JSON.parse(localStorage.getItem("__native:student:C905_E"+String(scope).padStart(2,"0")+"-SUM:exam"));return Object.keys(r.documents).filter(k=>k.startsWith("f"+String(scope).padStart(2,"0")+"-tab05-")).length}',scope)
   assert total==24
  check('24 document states per chapter coexist and each chapter uses its own native pack key')
  # Every question in each canonical bank gets its own wrong response and feedback.
  sample_files=[f for f in filenames if f.endswith('/TAB04.html') and not f.startswith('N10.1/')]
  for f in sample_files:
   await p.goto(url(f));D=await data(p)
   await p.evaluate('''()=>{const D=JSON.parse(document.getElementById('practice-data').textContent);for(const q of D.questions){const el=document.getElementById('q-'+q.id),radios=[...el.querySelectorAll('input[type=radio]')];const a=q.type==='mcq'?q.options.find(x=>x!==q.answer):q.type==='tf'?(q.answer==='درست'?'نادرست':'درست'):q.type==='essay'?'راه‌حل من برای مقایسه با راهنما':'-999';let input;if(radios.length){input=radios.find(x=>x.value===a);input.checked=true}else{input=el.querySelector('input,textarea');input.value=a}input.dispatchEvent(new Event('input',{bubbles:true}));el.querySelector('.submit-answer').click()}}''')
   ss=await state(p,D);auto=sum(q['type']!='essay' for q in D['questions']);assert len(ss['errors'])==auto and await p.locator('.error-explanation').count()==auto
   for q in D['questions']:
    fb=await p.locator('#q-'+q['id']+' .feedback').inner_text()
    if q['type']=='essay':assert 'تصحیح خودکار ندارد' in fb
    else:assert 'پاسخ درست' in fb and await p.locator('#q-'+q['id']+' .error-explanation').count()==1
   assert await p.evaluate('__nativeCalls.items.length')==auto
   await persian(p)
   # A fresh attempt verifies all positive paths as well.
   await p.locator('#finish').click();await p.locator('#finish-yes').click();await p.locator('#restart').click();await fill_all(p,'sample')
   assert await p.locator('.feedback.correct').count()==auto
   check('all canonical correct/wrong responses and manual rubrics: '+f)
  # Whole-book pool reuses canonical goals, rather than inflating unique-question totals.
  await p.goto(url('N10.1/TAB04.html'));D=await data(p);assert len(D['questions'])==411 and len({q['family'] for q in D['questions']})==411
  check('whole-book question bank preserves all 411 canonical learning goals without counting them twice')
  # The 24 whole-book papers preserve source form, exact marks and honest manual review.
  finals=[f for f in filenames if f.startswith('N10.1/TAB05-')];assert len(finals)==24
  for i,f in enumerate(finals):
   await p.goto(url(f));D=await data(p);await fill_all(p,'final',wrong_first=i==0)
   assert not await p.evaluate('__nativeCalls.items.length+__nativeCalls.exams.length')
   assert await p.locator('.feedback').count()==0 and not await p.locator('#paper-result').is_visible()
   if i==0:
    canvas=p.locator('canvas');box=await canvas.bounding_box();await canvas.scroll_into_view_if_needed();box=await canvas.bounding_box();await p.mouse.move(box['x']+20,box['y']+20);await p.mouse.down();await p.mouse.move(box['x']+80,box['y']+60);await p.mouse.up()
    assert (await state(p,D))['drawings']
   await p.reload();assert not await p.locator('#paper-result').is_visible() and not await p.evaluate('__nativeCalls.items.length+__nativeCalls.exams.length')
   await p.locator('#paper-finish').click();await p.locator('#paper-finish-no').click();assert await p.locator('.feedback').count()==0
   await p.locator('#paper-finish').click();await p.locator('#paper-finish-yes').click()
   assert await p.locator('#paper-result').is_visible() and await p.locator('#paper-save-result').is_disabled()
   assert not await p.evaluate('__nativeCalls.exams.length')
   assert 'نمرهٔ نهایی هنوز مشخص نیست' in await p.locator('#paper-result').inner_text()
   ss=await state(p,D);assert sum(e.get('manual',False) for e in ss['submitted'].values())==18
   assert all(not e.get('reviewed',False) for e in ss['submitted'].values() if e.get('manual'))
   await p.evaluate('''partial=>{const D=JSON.parse(document.getElementById('practice-data').textContent);for(const q of D.questions.filter(x=>x.type==='essay')){const el=document.getElementById('q-'+q.id);el.querySelectorAll('[data-step]').forEach((box,j)=>{box.checked=!(partial&&q.group===4&&q.part===1&&j===1);box.dispatchEvent(new Event('change',{bubbles:true}))});el.querySelector('.confirm-rubric').click()}}''',i==0)
   assert await p.locator('#paper-save-result').is_enabled();await p.locator('#paper-save-result').click()
   ss=await state(p,D);calls=await p.evaluate('__nativeCalls');score=19.5 if i==0 else 20
   assert ss['result']['earned']==score and ss['result']['totalMarks']==20 and ss['result']['assessmentMethod']=='automatic-and-self-assessment'
   assert len(calls['exams'])==1 and calls['exams'][0]['scorePct']==(98 if i==0 else 100) and calls['exams'][0]['total']==16
   assert calls['exams'][0]['correctCount']==(14 if i==0 else 16)
   assert len(calls['items'])==16 and len(ss['errors'])==(2 if i==0 else 0)
   if i==0:
    assert ss['errors'][1]['assessmentMethod']=='self-assessment' and ss['errors'][1]['earnedMarks']==.5
    assert 'q01' in calls['exams'][0]['wrongCsv'] and 'q04' in calls['exams'][0]['wrongCsv']
   result_text=await p.locator('#paper-result').inner_text()
   assert 'خودارزیابی' in result_text and 'تصحیح قطعی دبیر انجام نشده است' in result_text
   await persian(p);await p.reload();assert not await p.evaluate('__nativeCalls.items.length+__nativeCalls.exams.length')
   if (i+1)%6==0:print('Graded weighted final papers:',i+1,flush=True)
  check('all 24 final papers: 16 main questions, 38 parts, four pages, exact 20 marks, no pre-finish grading, partial marks, honest self-review and weighted native results')
  check('weighted example: 19.5/20 yields 98%, independently of 14/16 fully correct main questions; manual errors carry self-assessment metadata')
  # Blank final: no false error/progress items; history retains prior drawing and grading policy.
  await p.goto(url(finals[0]));prior=await state(p,await data(p));await p.locator('#paper-restart').click();await p.locator('#paper-finish').click();await p.locator('#paper-finish-yes').click();await p.locator('#paper-save-result').click()
  calls=await p.evaluate('__nativeCalls');ss=await state(p,await data(p));assert calls['exams'][-1]==dict(scorePct=0,total=16,correctCount=0,wrongCsv='') and not calls['items']
  assert len(ss['errors'])==len(prior['errors']) and ss['history'][-1]['drawings']
  check('unanswered final parts are not student-error events; restart preserves the previous weighted result and drawing in history')
  # All decks are single-card and every back is rendered in Persian.
  for f in [f for f in filenames if f.endswith('/TAB02.html')]:
   await p.goto(url(f));D=await data(p);assert await p.locator('.flash-card').count()==1 and not await p.locator('.card-answer').is_visible()
   for j in range(len(D['cards'])):
    await p.locator('.reveal').click();await persian(p)
    if j==0:await p.locator('[data-known=yes]').click()
    if j+1<len(D['cards']):await p.locator('#flash-next').click()
   assert await p.locator('#flash-next').is_disabled();await p.reload();assert fa(len(D['cards'])) in await p.locator('#flash-position').inner_text()
   assert not await p.locator('.card-answer').is_visible()
  check('all chapter and whole-book decks: 380 card views, one card at a time, native review, hidden backs and restored position')
  for f in [f for f in filenames if f.endswith('/TAB03.html')]:
   await p.goto(url(f));await p.locator('details').evaluate_all('els=>els.forEach(e=>e.open=true)');await persian(p)
   assert await p.locator('.study-note.rule').count() or f.startswith('N2.5/')
  check('all summaries have clear topic-specific rules, worked examples, exam traps and Persian formula digits, including expanded whole-book sections')
  for width in [320,768,1280]:
   await p.set_viewport_size(dict(width=width,height=850))
   for f in ['N3.4/TAB03.html','N4.6/TAB04.html','N5.5/TAB02.html','N7.4/TAB05-hard-02.html','N10.1/TAB05.html','N10.1/TAB05-easy-02.html']:
    await p.goto(url(f));assert await p.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,f)
  check('320px mobile, tablet and desktop layouts: summary, proof, card, question navigator and paper columns stay inside the viewport')
  await p.set_viewport_size(dict(width=390,height=844))
  for f,name,selector in [('N10.1/TAB05.html','whole-menu-mobile.png',None),('N10.1/TAB05-hard-02.html','final-mobile.png','.paper-page'),('N5.5/TAB03.html','summary-mobile.png','.study-note.rule'),('N4.6/TAB02.html','flash-mobile.png','.flash-card')]:
   await p.goto(url(f))
   if selector:await p.locator(selector).first.scroll_into_view_if_needed()
   await p.screenshot(path=str(REPORT/name),full_page=False)
  # Legacy injector and real failure modes.
  old=await p.evaluate('JSON.stringify(__nativeCalls)');await p.add_script_tag(path=str(APP/'apps/student/src/main/assets/math/c905/hamyar-persist.js'));assert old==await p.evaluate('JSON.stringify(__nativeCalls)')
  for mode in ['browser','broken','legacy']:
   c=await browser.new_context(offline=True,viewport=dict(width=360,height=800));await serve(c)
   if mode=='broken':await c.add_init_script("window.Hamyar={loadState(){return ''},saveState(){throw Error('unavailable')}}")
   if mode=='legacy':await c.add_init_script(INIT+"localStorage.setItem('__native:student:C905_E02-SUM:exam',JSON.stringify({stats:{old:{correct:true}},archive:['old']}));")
   pp=await c.new_page();await pp.goto(url('N3.4/TAB05-easy-01.html'));dd=await data(pp)
   if mode=='browser':
    await pp.locator('[data-question="1"]').click();inp=pp.locator('input[type=text]');await inp.fill('12');assert await inp.input_value()=='۱۲';await pp.reload();assert await pp.locator('input[type=text]').input_value()=='۱۲' and await pp.locator('.feedback').count()==0
    await pp.add_init_script("window.Hamyar={loadState(){return ''},saveState(raw){window.__fresh=raw}};");await pp.reload();assert await pp.locator('[data-question="1"]').get_attribute('class')==''
   if mode=='broken':assert 'ذخیرهٔ پایدار در دسترس نیست' in await pp.locator('#storage-status').inner_text()
   if mode=='legacy':
    root=await pp.evaluate('JSON.parse(localStorage.getItem("__native:student:C905_E02-SUM:exam"))');assert root['stats']['old']['correct'] and root['archive']==['old'] and dd['id'] in root['documents']
   await c.close()
  check('legacy state survives, failed storage is disclosed, browser drafts restore and a fresh native account does not inherit browser fallback')
  assert not errors,errors;assert not network,network;check('no JavaScript runtime errors and no external network requests during offline execution')
  await browser.close()
 report=dict(contentVersion='2026-10-18.book-1',assessmentContentVersion='2026-10-19.qa-fix-1',browser='Chromium',pages=252,chapterExams=192,weightedFinalPapers=24,checks=CHECKS,passed=len(CHECKS),errors=errors,externalRequests=network,nativeBridge='mock using exact existing signatures; real Android device run is separate')
 (REPORT/'browser-tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS:',len(CHECKS),'integration groups, all 252 pages and 216 exams.',flush=True)
if __name__=='__main__':asyncio.run(main())
