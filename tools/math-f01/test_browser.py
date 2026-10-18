"""Offline browser checks. Exact native bridge signatures are mocked, not an Android device."""
from pathlib import Path
import json,re,asyncio
from playwright.async_api import async_playwright
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
OUT=ROOT/'Bucket/Html-files/app/books/C905/N2.5';REPORT=ROOT/'reports/math-f01'
INIT='''window.__nativeCalls={items:[],exams:[],states:[]};
const name=location.pathname.split('/').pop(),kind=name==='TAB02.html'?'flash':name==='TAB03.html'?'summary':'exam',key='__native:'+kind;
window.Hamyar={loadState(){return localStorage.getItem(key)||''},saveState(raw){JSON.parse(raw);localStorage.setItem(key,raw);window.__nativeCalls.states.push(raw)},recordItem(id,correct){window.__nativeCalls.items.push({id,correct})},recordExam(scorePct,total,correctCount,wrongCsv){window.__nativeCalls.exams.push({scorePct,total,correctCount,wrongCsv})}};'''
BASE='http://127.0.0.1:8765/'
def url(file):return BASE+(file.name if isinstance(file,Path) else file)
async def install_local_documents(ctx):
 async def serve(route):
  file=OUT/route.request.url.split('/')[-1].split('?')[0]
  await route.fulfill(status=200 if file.is_file() and file.parent==OUT else 404,content_type='text/html; charset=utf-8',body=file.read_text() if file.is_file() and file.parent==OUT else 'Missing document')
 await ctx.route(BASE+'**',serve)
CHECKS=[]
def checked(s):CHECKS.append(s)
async def data(p):return await p.eval_on_selector('#practice-data','el=>JSON.parse(el.textContent)')
async def saved(p,D):return await p.evaluate('id=>JSON.parse(window.__nativeCalls.states.at(-1)).documents[id]',D['id'])
def wrong(q):return next(x for x in (q['options'] if q['type']=='mcq' else ['درست','نادرست'] if q['type']=='tf' else ['-999']) if x!=q['answer'])
def fa(s):return str(s).translate(str.maketrans('0123456789','۰۱۲۳۴۵۶۷۸۹'))
async def enter(p,q,a,submit=False,index=None):
 if index is not None:await p.locator('[data-question="'+str(index)+'"]').click()
 await p.evaluate('''({id,a,submit})=>{const el=document.getElementById('q-'+id),rs=[...el.querySelectorAll('input[type=radio]')];let input;if(rs.length){input=rs.find(x=>x.value===a);if(!input)throw Error('Missing option');input.checked=true}else{input=el.querySelector('input,textarea');input.value=a}input.dispatchEvent(new Event('input',{bubbles:true}));if(submit)el.querySelector('.submit-answer').click()}''',dict(id=q['id'],a=a,submit=submit))
async def finish(p):await p.locator('#finish').click();await p.locator('#finish-yes').click()
async def no_grade(p,D):
 assert await p.locator('.feedback').count()==0
 assert not await p.locator('#final-result').is_visible()
 assert not await p.locator('#export-errors').is_visible()
 assert await p.locator('#stats').count()==0
 assert not await p.evaluate('window.__nativeCalls.items.length+window.__nativeCalls.exams.length')
 st=await saved(p,D);assert st['submitted']=={} and not st['finished'] and not st['errors'] and 'result' not in st
async def persian_visible(p):
 text=await p.locator('body').inner_text()
 vals=await p.eval_on_selector_all('input[type=text],textarea','els=>els.map(x=>x.value).join(" ")')
 labels=await p.eval_on_selector_all('[aria-label]','els=>els.map(x=>x.getAttribute("aria-label")).join(" ")')
 assert not re.search('[0-9٠-٩⁰¹²³⁴⁵⁶⁷⁸⁹]',text+vals+labels+await p.title()),re.findall('.{0,15}[0-9٠-٩⁰¹²³⁴⁵⁶⁷⁸⁹].{0,15}',text+vals+labels)
async def main():
 errors=[];network=[]
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  ctx=await browser.new_context(viewport=dict(width=390,height=844),color_scheme='light',offline=True)
  await install_local_documents(ctx);await ctx.add_init_script(INIT)
  p=await ctx.new_page();p.on('pageerror',lambda e:errors.append(str(e)));p.on('request',lambda r:network.append(r.url) if r.url.startswith(('https://','http://')) and not r.url.startswith(BASE) else None)
  await p.goto(url('TAB05.html'));assert await p.locator('.level-card').count()==4 and await p.locator('.exam-links a').count()==24
  await p.screenshot(path=str(REPORT/'menu-mobile.png'),full_page=True);checked('four levels with six independently runnable HTML files each')
  files=sorted(OUT.glob('*.html'));assert len(files)==28
  for file in files:
   await p.goto(url(file))
   assert await p.locator('header').count()==1 and await p.locator('footer').count()==1 and await p.get_attribute('html','dir')=='rtl'
   assert await p.locator('.practice-nav').count()==0 and await p.locator('.source-list a').count()==0
   assert await p.locator('.source-list,.sources').count()==0
   assert 'منابع و شیوه' not in await p.locator('body').inner_text()
   assert await p.evaluate('document.documentElement.scrollWidth<=innerWidth'),file.name
   for href in await p.eval_on_selector_all('a[href]','els=>els.map(e=>e.getAttribute("href"))'):
    assert href.startswith('#') or (OUT/href.split('#')[0]).is_file(),(file.name,href)
   await p.evaluate('async()=>{await Promise.all([400,500,700].map(n=>document.fonts.load(n+" 16px Vazir")));await document.fonts.ready}')
   assert await p.evaluate('document.fonts.check("400 16px Vazir")&&document.fonts.check("500 16px Vazir")&&document.fonts.check("700 16px Vazir")')
   assert await p.locator('body').evaluate('e=>getComputedStyle(e).fontFamily.startsWith("Vazir,")')
   palette='''()=>['body','main','header','footer','button','input','.question-card','.flash-card'].map(s=>{const e=document.querySelector(s);if(!e)return null;const c=getComputedStyle(e);return [c.color,c.backgroundColor,c.backgroundImage,c.colorScheme]})'''
   before=await p.evaluate(palette);await p.emulate_media(color_scheme='dark');assert before==await p.evaluate(palette),file.name
   await p.emulate_media(color_scheme='light');await persian_visible(p)
   if not file.name.startswith('TAB05-'):continue
   D=await data(p);assert D['mode']=='assessment' and len(D['questions'])==14
   assert await p.locator('.question-card').count()==1 and await p.locator('.submit-answer').count()==0
   await no_grade(p,D)
   for i,q in enumerate(D['questions']):
    await enter(p,q,wrong(q) if i==0 else q['answer'],index=i)
    await no_grade(p,D)
   # Answers remain editable. A wrong choice can be replaced, with no grading.
   await enter(p,D['questions'][1],wrong(D['questions'][1]),index=1)
   await enter(p,D['questions'][1],D['questions'][1]['answer'])
   await p.reload();await no_grade(p,D)
   assert (await saved(p,D))['currentQuestion']==1
   await p.locator('#finish').click();await p.locator('#finish-no').click();await no_grade(p,D)
   await finish(p)
   calls=await p.evaluate('window.__nativeCalls');assert len(calls['items'])==14 and sum(x['correct'] for x in calls['items'])==13
   assert calls['exams']==[dict(scorePct=93,total=14,correctCount=13,wrongCsv=D['id']+'_'+D['questions'][0]['id'])]
   st=await saved(p,D);assert len(st['errors'])==1
   e=st['errors'][0]
   for field in ['eventId','questionId','grade','book','chapter','lesson','topic','questionType','difficulty','studentAnswer','correctAnswer','recordedAt','errorCategory']:assert field in e
   assert await p.locator('.question-card').count()==14 and await p.locator('.feedback.wrong').count()==1 and await p.locator('.feedback.correct').count()==13
   assert '۹۳٪' in await p.locator('#final-result').inner_text();await persian_visible(p)
   await p.locator('#finish-yes').evaluate('e=>e.click()');assert await p.evaluate('window.__nativeCalls.exams.length')==1
   await p.reload();assert await p.locator('#final-result').is_visible() and not await p.evaluate('window.__nativeCalls.items.length+window.__nativeCalls.exams.length')
   checked('delayed grading, editable saved drafts, cancellation, final grading, error payload and idempotent reload: '+file.name)
  checked('all 28 pages: no top tabs, plain sources, Persian visible digits, embedded Vazir weights, fixed theme and intact header/footer')
  await p.goto(url('TAB05-easy-01.html'));await p.locator('#restart').click();await finish(p)
  assert (await p.evaluate('window.__nativeCalls.exams'))[-1]==dict(scorePct=0,total=14,correctCount=0,wrongCsv='')
  assert '۱۴ بدون پاسخ' in await p.locator('#final-result').inner_text()
  allstate=await p.evaluate('JSON.parse(localStorage.getItem("__native:exam"))');assert sum(k.startswith('f01-tab05-') for k in allstate['documents'])==24
  checked('24 states coexist; unanswered items are not logged as student mistakes; retry archives the previous attempt')
  await p.goto(url('TAB04.html'));D=await data(p);assert D['mode']=='sample' and await p.locator('.question-card').count()==60
  for q in D['questions']:
   if q['type']=='essay':
    await enter(p,q,'پاسخ من 12 برای مقایسه با راهنما',submit=True)
    assert 'تصحیح خودکار ندارد' in await p.locator('#q-'+q['id']+' .feedback').inner_text()
   else:
    await enter(p,q,wrong(q),submit=True)
    fb=p.locator('#q-'+q['id']+' .error-explanation');assert await fb.count()==1
    text=await fb.inner_text();assert 'پاسخ درست' in text and text.endswith('است.') and text.count('.')==1,(q['id'],text)
    assert fa(q['answer']) in text
  st=await saved(p,D);assert len(st['errors'])==56 and len({e['eventId'] for e in st['errors']})==56
  assert await p.evaluate('window.__nativeCalls.items.length')==56
  await finish(p);assert (await p.evaluate('window.__nativeCalls.exams'))[-1]['total']==56
  await persian_visible(p)
  checked('all 56 automatic sample questions: immediate one-sentence error analysis, own answer and unique detailed error; four essays use rubrics only')
  await p.screenshot(path=str(REPORT/'samples-mobile.png'),full_page=False)
  checks=await p.evaluate('''()=>{const e=HamyarPractice.equivalent,d=HamyarPractice.diagnosis;return [e({type:'short',answer:'1/2'},'۱/۲'),e({type:'short',answer:'1/2'},'٠٫٥'),e({type:'set',answer:'{2,5}'},'{۵،۲،۲}'),e({type:'set',answer:'∅'},'{}'),!e({type:'short',answer:'3'},'abc3'),!e({type:'short',answer:'3'},'1/0'),!e({type:'short',answer:'3'},'3+0'),!e({type:'set',answer:'{2,5}'},'2,5'),!e({type:'short',answer:'0'},'Infinity'),e({type:'mcq',answer:'بین 2 و 5'},'بین ۲ و ۵'),d({type:'set',answer:'{1,2,3}',verify:{op:'union',A:[1,2],B:[2,3]},feedback:'عضوها را یک بار بنویس',objective:'اجتماع'},'{۲}').category==='جابه‌جایی اجتماع و اشتراک',d({type:'short',answer:'2',verify:{op:'card',A:[1,2,1]},feedback:'تکرار را حذف کن',objective:'شمارش'},'۳').category==='شمارش عضو تکراری'];}''')
  assert all(checks),checks;checked('strict numeric/set parsing and answer-specific diagnosis: repeated members, union/intersection and Persian MCQ values')
  # Positive paths include real typing/paste normalization and every automatically graded answer.
  await p.locator('#restart').click();D=await data(p)
  for q in D['questions']:
   if q['type']!='essay':await enter(p,q,q['answer'],submit=True)
  assert await p.locator('.feedback.correct').count()==56
  await persian_visible(p);checked('all 56 correct canonical answers accepted, with Persian input conversion')
  await p.goto(url('TAB02.html'));assert await p.locator('.flash-card').count()==1 and await p.locator('.card-answer:visible').count()==0
  await p.locator('.reveal').click();await p.locator('[data-known=yes]').click()
  assert await p.evaluate('window.__nativeCalls.items')==[dict(id='f01-card-01',correct=True)]
  for i in range(1,28):
   await p.locator('#flash-next').click();assert await p.locator('.flash-card').count()==1
   assert await p.locator('.card-answer:visible').count()==0 and fa(i+1) in await p.locator('#flash-position').inner_text()
   await p.locator('.reveal').click();await persian_visible(p)
  assert await p.locator('#flash-next').is_disabled();await p.reload();assert '۲۸' in await p.locator('#flash-position').inner_text()
  await p.locator('#flash-prev').click();assert '۲۷' in await p.locator('#flash-position').inner_text()
  await p.screenshot(path=str(REPORT/'flash-mobile.png'),full_page=True)
  checked('28 flashcards in one file, exactly one card displayed, front/back, native self-review and restored position')
  await p.goto(url('TAB03.html'))
  colors=await p.eval_on_selector_all('.summary-key span','els=>els.map(e=>getComputedStyle(e).backgroundColor)')
  assert len(set(colors))==4 and await p.locator('.study-note.trap').count()==4
  await p.screenshot(path=str(REPORT/'summary-mobile.png'),full_page=True)
  checked('summary uses explicit labels and four distinct concept/rule/example/exam-trap colors')
  await p.goto(url('TAB05-hard-01.html'));await p.locator('#restart').click();await p.screenshot(path=str(REPORT/'exam-mobile.png'),full_page=False)
  old=await p.evaluate('JSON.stringify(window.__nativeCalls)');await p.add_script_tag(path='/workspace/hamyar-math-app/apps/student/src/main/assets/math/c905/hamyar-persist.js');assert old==await p.evaluate('JSON.stringify(window.__nativeCalls)')
  checked('legacy persistence injection cannot grade early or overwrite document state')
  # Faults and legacy content migrations are isolated from the main browser state.
  for mode in ['browser','broken','migration','legacy']:
   c=await browser.new_context(offline=True,viewport=dict(width=360,height=800));await install_local_documents(c)
   if mode=='broken':await c.add_init_script("window.Hamyar={loadState(){return ''},saveState(){throw Error('unavailable')}}")
   if mode=='migration':await c.add_init_script(INIT+'''localStorage.setItem('__native:exam',JSON.stringify({schema:'hamyar-math-practice-1',documents:{'f01-tab05-easy-01':{contentVersion:'2026-10-18.1',sessionId:'old',answers:{old:'answer'},submitted:{old:{correct:false}},errors:[{eventId:'preserved'}],history:[],cards:{},finished:false}}}));''')
   if mode=='legacy':await c.add_init_script(INIT+'''localStorage.setItem('__native:exam',JSON.stringify({stats:{old:{correct:true}},archive:['old']}));''')
   pp=await c.new_page();await pp.goto(url('TAB05-easy-01.html'));dd=await data(pp)
   if mode=='browser':
    await enter(pp,dd['questions'][2],'123',index=2)
    assert await pp.locator('input[type=text]').input_value()=='۱۲۳'
    await pp.reload();assert await pp.locator('input[type=text]').input_value()=='۱۲۳' and await pp.locator('.feedback').count()==0
    assert 'ثبت در اپ در این محیط فعال نیست' in await pp.locator('#storage-status').inner_text()
    await pp.add_init_script("window.Hamyar={loadState(){return ''},saveState(raw){window.__saved=raw}}")
    await pp.reload();assert await pp.locator('[data-question="2"]').get_attribute('class')==''
   if mode=='broken':assert 'ذخیرهٔ پایدار در دسترس نیست' in await pp.locator('#storage-status').inner_text()
   if mode=='migration':
    ss=await saved(pp,dd);assert ss['submitted']=={} and ss['answers']=={} and ss['errors']==[dict(eventId='preserved')]
    assert ss['history'][0]['submitted']['old']['correct'] is False and not await pp.locator('#final-result').is_visible()
   if mode=='legacy':
    ss=await pp.evaluate('JSON.parse(localStorage.getItem("__native:exam"))');assert ss['stats']['old']['correct'] and ss['archive']==['old'] and dd['id'] in ss['documents']
   await c.close()
  checked('browser drafts, explicit storage failure, native-account isolation and lossless legacy/version migration')
  for width in [320,768,1280]:
   await p.set_viewport_size(dict(width=width,height=850))
   for name in ['TAB05.html','TAB05-hard-02.html','TAB04.html','TAB02.html','TAB03.html']:
    await p.goto(url(name));assert await p.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,name)
    await persian_visible(p)
  checked('320px mobile, tablet and desktop stay within viewport with Persian text/digits')
  assert not errors,errors;assert not network,network
  checked('no JavaScript errors or external requests during offline execution')
  await browser.close()
 (REPORT/'browser-tests.json').write_text(json.dumps(dict(browser='Chromium',contentVersion='2026-10-18.2',nativeBridge='mock using exact existing signatures',checks=CHECKS,passed=len(CHECKS),errors=errors,networkRequests=network),ensure_ascii=False,indent=2)+'\n')
 print(f'PASS: {len(CHECKS)} browser groups; 28 pages; 24 delayed-grading exams.')
if __name__=='__main__':asyncio.run(main())
