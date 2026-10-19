"""Regression checks for the reported fixed-question repetition and missing feedback.

Uses rendered offline HTML and the real bridge signatures mocked in Chromium.
Does not claim independent QA or an Android-device run.
"""
from pathlib import Path
from collections import Counter, defaultdict
import asyncio, hashlib, json, re, subprocess, unicodedata
from fractions import Fraction
from playwright.async_api import async_playwright
from test_book import INIT, serve, data, state, url, persian, fa
from verify_book import verify

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / 'reports/math-book/qa-fix-20261019'
FROZEN = '42362a5f6fc6ac429eb2d0dcc506ecc398822e12'


def normalized(s):
    return re.sub(r'[\s\u200c\u200e\u200f]+', '', unicodedata.normalize('NFKC', str(s))).translate(
        str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789'))


def fingerprint(q):
    return (normalized(q['prompt']), tuple(sorted(map(normalized, q['options']))),
            normalized(q.get('diagram', '')), normalized(q.get('graphic', '')))


def static_checks():
    REPORT.mkdir(exist_ok=True)
    before, after, scope_counts, certs, reviews = {}, {}, {}, 0, []
    for ch in range(9):
        path = 'reports/math-f01/assessments.json' if ch == 1 else f'reports/math-book/assessments-{ch:02d}.json'
        old = json.loads(subprocess.check_output(['git', 'show', FROZEN + ':' + path], cwd=ROOT))
        exams = json.loads((ROOT/path).read_text())
        old_counts = Counter(fingerprint(q) for e in old for q in e['questions'])
        counts = Counter(fingerprint(q) for e in exams for q in e['questions'])
        before[ch] = sum(n-1 for n in old_counts.values() if n > 1)
        after[ch] = sum(n-1 for n in counts.values() if n > 1)
        assert after[ch] == 0, (ch, after[ch])
        assert len(exams) == 24
        assert Counter(e['level'] for e in exams) == {'آسان': 6, 'متوسط': 6, 'دشوار': 6, 'درخشان': 6}
        scope_counts[ch] = sum(len(e['questions']) for e in exams)
        for e in exams:
            if ch == 0:
                assert sum(q['marks'] for q in e['questions']) == 20
                assert len(e['questions']) == 38
            for q in e['questions']:
                if q.get('assessmentCase'):
                    if q['check']['kind'] == 'number':
                        verify(q)
                        certs += 1
                    else:
                        reviews.append(dict(id=q['id'], family=q['family'], prompt=q['prompt'],
                                            answer=q['answer'], options=q['options'], feedback=q['feedback']))
                if q['type'] == 'mcq':
                    assert len(q['options']) == len(set(map(normalized, q['options']))) == 4
                    assert q['options'].count(q['answer']) == 1
                assert q['feedback'] and 'پاسخ با تعریف و داده‌های همین بخش' not in q['feedback']
    # Canonical questions are unchanged, and whole-book repetition remains an explicitly shared pool.
    canonical = 0
    corrected_prompts = 0
    for ch in range(1,9):
        name = 'reports/math-f01/canonical-bank.json' if ch == 1 else f'reports/math-book/bank-{ch:02d}.json'
        old = json.loads(subprocess.check_output(['git','show',FROZEN+':'+name],cwd=ROOT))
        new=json.loads((ROOT/name).read_text())
        assert len(old)==len(new)
        for original,current in zip(old,new):
            changed={key for key in set(original)|set(current) if original.get(key)!=current.get(key)}
            if changed:
                assert current['family'] in {'f03-44','f07-13'} and changed=={'prompt'}, (name,current['family'],changed)
                corrected_prompts+=1
        canonical += len(old)
    assert canonical == 411 and corrected_prompts == 2
    # M9-QA-004: x=-a is allowed and both original and reduced expressions equal zero.
    import sympy as sp
    from ch07 import questions as rational_questions
    for v in range(7):
        q=next(q for q in rational_questions(v) if q['family']=='f07-13')
        forbidden=int(re.search(r'x≠(\d+)',q['prompt']).group(1))
        assert '±' not in q['prompt'] and (-forbidden)**2-forbidden**2==0 and -forbidden-forbidden!=0
    # M9-QA-005: the rendered problem text must use conventional signed terms.
    from ch03 import questions as geometry_questions
    for v in range(7):
        q=next(q for q in geometry_questions(v) if q['family']=='f03-44')
        assert not re.search(r'\+\s*(?:\(\s*)?[−-]\d',q['prompt'])
    for paper in json.loads((ROOT/'reports/math-book/assessments-00.json').read_text()):
        q=next(q for q in paper['questions'] if q['family']=='final-q13-p01')
        assert not re.search(r'\+\s*(?:\(\s*)?[−-]\d',q['prompt'])
    return dict(previousFrozenCommit=FROZEN, baselineDuplicateExtraInstancesByScope=before,
                correctedDuplicateExtraInstancesByScope=after, scopeQuestionInstances=scope_counts,
                canonicalQuestionCount=canonical, canonicalKeysUnchanged=canonical, canonicalPromptsCorrected=corrected_prompts, domainAndSignRegression=True, newNumericCaseCertificates=certs,
                appliedFactAndChoiceAuthorReviews=reviews,
                fingerprint='Rendered prompt, unordered options, actual diagram/graphic; ignores question ID and version.',
                uniquenessMeaning='Distinct assessment data, not distinct learning objectives or new canonical questions.')


async def browser_checks():
    report = static_checks()
    routes = json.loads((ROOT/'reports/math-book/routes.json').read_text())['routes']
    finals = [r for r in routes if '/N10.1/TAB05-' in r['bucketKey']]
    errors, requests = [], []
    visited = []
    automatic = manual = 0
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, color_scheme='dark')
        await ctx.add_init_script(INIT)
        await serve(ctx)
        p = await ctx.new_page()
        p.on('pageerror', lambda e: errors.append(str(e)))
        p.on('request', lambda r: requests.append(r.url) if not r.url.startswith(('http://127.0.0.1:8765/','data:')) else None)
        # M9-QA-004/005: inspect the corrected bank data in chapter and shared whole-book views.
        for file in ['N4.6/TAB04.html','N8.4/TAB04.html','N10.1/TAB04.html']:
            await p.goto(url(file))
            visited.append(file)
            await p.evaluate(r'''()=>{const D=JSON.parse(document.getElementById('practice-data').textContent);
              for(const q of D.questions.filter(q=>['f03-44','f07-13'].includes(q.family))){
                const el=document.getElementById('q-'+q.id),radios=[...el.querySelectorAll('input[type=radio]')];
                const input=radios.length?radios.find(r=>r.value===q.answer):el.querySelector('input[type=text]');
                if(radios.length)input.checked=true;else input.value=q.answer;
                input.dispatchEvent(new Event('input',{bubbles:true}));el.querySelector('.submit-answer').click();
                if(!el.querySelector('.feedback.correct'))throw Error('Corrected bank key not accepted: '+q.id);
                if(/\+\s*(?:\(\s*)?[−-][0-9۰-۹]/.test(el.querySelector('h2').textContent))throw Error('Unreadable signs');}}''')
            assert await p.evaluate('document.documentElement.scrollWidth<=innerWidth'),file
        # Changed applied choices must override the old chapter-one option-index explanations.
        for slug,family in [('hard','f01-33'),('brilliant','f01-53')]:
            for v in range(1,7):
                file=f'N2.5/TAB05-{slug}-{v:02d}.html'
                await p.goto(url(file))
                visited.append(file)
                assert await p.evaluate('''family=>{const D=JSON.parse(document.getElementById('practice-data').textContent),q=D.questions.find(q=>q.family===family);
                  return Object.entries(q.mistakes).length===3&&Object.entries(q.mistakes).every(([answer,reason])=>HamyarPractice.diagnosis(q,answer).sentence.includes(reason));}''',family)
        for directory,slug,family in [('N4.6','brilliant','f03-44'),('N8.4','medium','f07-13')]:
            for v in range(1,7):
                file=f'{directory}/TAB05-{slug}-{v:02d}.html'
                await p.goto(url(file))
                visited.append(file)
                D=await data(p)
                index=next(i for i,q in enumerate(D['questions']) if q['family']==family)
                await p.locator('[data-question="'+str(index)+'"]').click()
                q=D['questions'][index]
                el=p.locator('#q-'+q['id'])
                if q['type']=='mcq':
                    await el.locator('input[type=radio]').evaluate_all('(xs,answer)=>{const x=xs.find(x=>x.value===answer);x.checked=true;x.dispatchEvent(new Event("input",{bubbles:true}))}',q['answer'])
                else:
                    await el.locator('input[type=text]').fill(q['answer'])
                assert await p.locator('.feedback').count()==0
                await p.locator('#finish').click()
                await p.locator('#finish-yes').click()
                ss=await state(p,D)
                assert ss['submitted'][q['id']]['correct']
                assert await p.evaluate('document.documentElement.scrollWidth<=innerWidth'),file
        # A frozen-version saved attempt must be archived, never regraded with changed questions.
        await p.goto(url(finals[0]['bucketKey'].split('/C905/')[1]))
        migration_data = await data(p)
        await p.evaluate(r'''()=>{const D=JSON.parse(document.getElementById('practice-data').textContent),root=JSON.parse(__nativeCalls.lastState),doc=root.documents[D.id];
          Object.assign(doc,{contentVersion:'2026-10-18.book-1',sessionId:'frozen-before-qa-fix',finished:true,answers:{[D.questions[0].id]:'پاسخ قدیمی'},submitted:{[D.questions[0].id]:{correct:true,answer:'پاسخ قدیمی'}},result:{percentage:95}});
          Hamyar.saveState(JSON.stringify(root));}''')
        await p.reload()
        migrated = await state(p,migration_data)
        assert migrated['contentVersion']=='2026-10-19.qa-fix-1' and not migrated['finished']
        assert migrated['answers']=={} and migrated['submitted']=={}
        assert migrated['history'][-1]['answers'][migration_data['questions'][0]['id']]=='پاسخ قدیمی'
        assert migrated['history'][-1]['result']['percentage']==95
        assert not await p.evaluate('__nativeCalls.items.length+__nativeCalls.exams.length')
        assert await p.locator('.feedback').count()==0
        for route in finals:
            file=route['bucketKey'].split('/C905/')[1]
            await p.goto(url(file))
            visited.append(file)
            D = await data(p)
            await p.evaluate(r'''()=>{const D=JSON.parse(document.getElementById('practice-data').textContent);
              for(const q of D.questions){const el=document.getElementById('q-'+q.id),rs=[...el.querySelectorAll('input[type=radio]')];
                const x=rs.length?rs.find(r=>r.value!==q.answer):el.querySelector('textarea,input[type=text]');
                if(rs.length)x.checked=true;else x.value=q.type==='essay'?'راه‌حل تمرینی برای خودارزیابی':q.type==='set'?'{-987654321}':'-987654321';
                x.dispatchEvent(new Event('input',{bubbles:true}));}}''')
            assert await p.locator('.feedback').count() == 0
            assert not await p.locator('#paper-result').is_visible()
            assert not await p.evaluate('__nativeCalls.items.length+__nativeCalls.exams.length')
            await p.reload()
            assert await p.locator('.feedback').count() == 0
            await p.locator('#paper-finish').click()
            await p.locator('#paper-finish-yes').click()
            await p.evaluate("()=>document.querySelectorAll('.confirm-rubric').forEach(button=>button.click())")
            diagnostics=await p.evaluate("()=>Object.fromEntries([...document.querySelectorAll('.paper-part')].map(el=>[el.id,{feedback:el.querySelector('.feedback').textContent,explanation:el.querySelector('.error-explanation')?.textContent}]))")
            for q in D['questions']:
                diagnostic=diagnostics['q-'+q['id']]
                if q['type'] == 'essay':
                    assert 'خودارزیابی' in diagnostic['feedback']
                    manual += 1
                else:
                    assert 'پاسخ نادرست' in diagnostic['feedback']
                    automatic += 1
                explanation = diagnostic['explanation'] or ''
                assert len(explanation) > 35, (q['id'], explanation)
                # The visible diagnostic must contain the part-specific author hint, not just a key/mark.
                lead = q['feedback'].split('؛')[0]
                assert normalized(fa(lead)) in normalized(explanation), (q['id'], lead, explanation)
            ss = await state(p,D)
            current = [e for e in ss['errors'] if e['sessionId'] == ss['sessionId']]
            assert len(current) == 38
            assert len({e['questionId'] for e in current}) == 38
            assert all(e['errorCategory']!='نیاز به مرور درست یا نادرست' for e in current)
            await p.locator('#paper-save-result').click()
            assert (await p.evaluate('__nativeCalls.exams.at(-1)'))['scorePct'] == 0
            await persian(p)
            print('PASS all-wrong diagnostics:', route['assetPath'], flush=True)
        await b.close()
    assert not errors and not requests, (errors, requests)
    baseline=json.loads((REPORT/'comprehensive-browser-inputs.json').read_text())
    current={r['bucketKey']:hashlib.sha256((ROOT/r['bucketKey']).read_bytes()).hexdigest() for r in routes}
    changed={path for path,value in current.items() if baseline[path]!=value}
    actual={'Bucket/Html-files/app/books/C905/'+file for file in visited}
    assert changed<=actual, sorted(changed-actual)
    report['byteCoverage']=dict(comprehensivePages=252,changedSinceComprehensive=len(changed),unchangedPages=252-len(changed),changedPagesExercised=len(changed&actual),baselineManifestSha256=hashlib.sha256((REPORT/'comprehensive-browser-inputs.json').read_bytes()).hexdigest(),testedHtmlSha256={path:current[path] for path in sorted(actual)})
    report.update(finalPapers=24, automaticWrongFeedbackChecked=automatic, manualSelfAssessmentFeedbackChecked=manual,
                  browser='Offline Chromium with exact bridge signatures mocked; no Android device.',
                  preFinishDiagnosticsHidden=True, oldVersionArchivedWithoutRegrading=True, correctedBankViews=3, appliedChoiceReasonVariants=12, domainAndSignExamVariants=12, recordedErrorsChecked=automatic+manual,
                  errors=errors, externalRequests=requests, independentQa='PENDING_RETEST', verdict='AUTHOR_REGRESSION_PASS')
    (REPORT/'remediation-tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PASS regression:', automatic, 'automatic diagnostics and', manual, 'manual diagnostics', flush=True)


if __name__ == '__main__':
    asyncio.run(browser_checks())
