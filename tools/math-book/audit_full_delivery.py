"""Audit the existing full book and bind every route/theme to immutable Git inputs.

This script never rebuilds educational content or changes the Application.
"""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,re,subprocess

ROOT=Path(__file__).resolve().parents[2]
def digest(data):return hashlib.sha256(data).hexdigest()
def load(path):return json.loads(path.read_text())
def write(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def git(repo,*args):return subprocess.check_output(['git',*args],cwd=repo)
def blobs(repo,commit,prefix):
 return {p:info.split()[2] for info,p in (line.split('\t',1) for line in git(repo,'ls-tree','-r',commit,'--',prefix).decode().splitlines())}
def raw(repo,commit,path):return 'https://raw.githubusercontent.com/samanta-nz/'+repo+'/'+commit+'/'+path.replace(' ','%20')

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--app',type=Path,default=Path('/workspace/hamyar-math-app'))
 parser.add_argument('--output',type=Path);parser.add_argument('--fresh-browser-evidence',action='store_true')
 parser.add_argument('--content-commit',default='42362a5f6fc6ac429eb2d0dcc506ecc398822e12');parser.add_argument('--app-commit',default='253e50cfe9487bead94ed97242ab08b0f8fed7b2');args=parser.parse_args()
 report=ROOT/'reports/math-book';out=args.output or report/'final-delivery';out.mkdir(parents=True,exist_ok=True)
 routes=load(report/'routes.json')['routes'];assert len(routes)==252
 build=load(report/'build-report.json');old=load(ROOT/'reports/math-f01/research-audit.json')
 hashes={f['path']:f['sha256'] for f in build['generatedFiles']+old['generatedFiles']};assert len(hashes)==252
 cb=blobs(ROOT,args.content_commit,'Bucket/Html-files/app/books/C905');ab=blobs(args.app,args.app_commit,'grades/g09/src/main/assets/math/c905/practice')
 template_commit='51afd4c3a91be6026668fa248aaaa762c384bd70';template=ROOT/'teaching - template'
 verified=subprocess.check_output(['python',str(template/'tools/verify_locked.py')],text=True).strip();assert verified=='OK — all locked files intact'
 locked=[*sorted((template/'assets/css/locked').glob('*.css')),template/'assets/js/locked/ui.js']
 for file in locked+[template/'assets/LOCKED.sha256']:
  assert file.read_bytes()==git(ROOT,'show',template_commit+':'+str(file.relative_to(ROOT)))
 modes=Counter();scopes={};assets=[];families=[];canonical_cards=0;payload_matches=0
 for route in routes:
  path=Path(route['bucketKey']);p=ROOT/path;body=p.read_bytes();text=body.decode()
  assert digest(body)==hashes[str(path)] and body==git(ROOT,'show',args.content_commit+':'+str(path))
  asset=Path('grades/g09/src/main/assets')/route['assetPath'];assert cb[str(path)]==ab[str(asset)]
  assert body==(args.app/asset).read_bytes()
  data=json.loads(re.search(r'<script[^>]*id="practice-data"[^>]*>([\s\S]*?)</script>',text).group(1))
  ch=data['chapterNumber'];modes[data['mode']]+=1
  info=scopes.setdefault(ch,dict(scope=ch,title=data['chapterTitle'],packId=data['packId'],directory=str(path.parent),files=0,exams=0,levels=Counter(),bankCount=0,cards=0))
  info['files']+=1
  if data['mode']=='sample':
   expected=load(ROOT/'reports/math-f01/canonical-bank.json') if ch==1 else load(report/f'bank-{ch:02d}.json')
   assert data['questions']==expected;payload_matches+=1;info['bankCount']=len(expected)
   assert len({q['family'] for q in expected})==len(expected)
   if ch:families.extend(q['family'] for q in expected)
  if data['mode']=='flash':
   info['cards']=len(data['cards'])
   if ch:canonical_cards+=len(data['cards'])
  if data['mode'] in ['assessment','final']:
   exams=load(ROOT/'reports/math-f01/assessments.json') if ch==1 else load(report/f'assessments-{ch:02d}.json')
   q=next(e['questions'] for e in exams if e['filename']==path.name)
   assert data['questions']==q;payload_matches+=1;info['exams']+=1;info['levels'][data['questions'][0]['difficulty']]+=1
   if data['mode']=='final':
    assert len(q)==38 and len({x['group'] for x in q})==16 and sum(x['marks'] for x in q)==20
    for x in q:
     if x['type']=='essay':assert sum(y['marks'] for y in x['rubric'])==x['marks']
  embedded=dict(re.findall(r'<(?:style|script) data-locked-source="([^"]+)">([\s\S]*?)</(?:style|script)>',text))
  assert len(embedded)==len(locked)
  for file in locked:assert embedded[str(file.relative_to(template))]==file.read_text()
  theme_path=path.parent/'assets/css/theme'/(path.stem+'.theme.css');theme=(ROOT/theme_path).read_bytes()
  assert theme.decode()==re.search(r'<style data-page-theme="[^"]+">([\s\S]*?)</style>',text).group(1)
  target_theme=asset.parent/'assets/css/theme'/theme_path.name
  assert cb[str(theme_path)]==ab[str(target_theme)] and theme==(args.app/target_theme).read_bytes()
  assets.append(dict(scope=ch,mode=data['mode'],packId=data['packId'],kind=route['kind'],menuNode=path.parent.name,bucketKey=str(path),assetPath=route['assetPath'],bytes=len(body),sha256=digest(body),gitBlob=cb[str(path)],url=raw('Books-Data',args.content_commit,str(path)),theme=dict(sourcePath=str(theme_path),assetPath=str(target_theme.relative_to('grades/g09/src/main/assets')),bytes=len(theme),sha256=digest(theme),gitBlob=cb[str(theme_path)],url=raw('Books-Data',args.content_commit,str(theme_path)))))
 assert set(scopes)==set(range(9))
 for info in scopes.values():assert info['files']==28 and info['exams']==24 and set(info['levels'].values())=={6} and len(info['levels'])==4
 assert len(families)==len(set(families))==411 and canonical_cards==190
 assert scopes[0]['bankCount']==411 and scopes[0]['cards']==190
 browser=load(report/'browser-tests.json');android=load(report/'android-tests.json')
 assert browser['pages']==252 and browser['chapterExams']==192 and browser['weightedFinalPapers']==24 and browser['passed']==23 and not browser['errors'] and not browser['externalRequests']
 assert android['build']=='passed' and android['byteComparisons']==252 and android['mergedThemeFiles']==252
 evidence_paths=['reports/math-book/browser-tests.json','reports/math-book/browser-tests.log','reports/math-book/android-tests.json','reports/math-book/answer-verification.json','reports/math-book/final-verification.json','reports/math-book/research-audit.json','reports/math-book/semantic-review.md','reports/math-book/research/final-blueprint.json','reports/math-book/template-audit.json','reports/math-f01/research-audit.json','reports/math-f01/semantic-review.md']
 if args.fresh_browser_evidence:evidence_paths.extend('reports/math-book/qa-fix-20261019/'+name for name in ['remediation-tests.json','mobile-tests.json','qa-input-receipt.json','remediation-summary.json','comprehensive-browser-inputs.json','comprehensive-browser-tests.json'])
 evidence=[]
 for name in evidence_paths:
  b=git(ROOT,'show',args.content_commit+':'+name);assert b==(ROOT/name).read_bytes()
  evidence.append(dict(path=name,bytes=len(b),sha256=digest(b),url=raw('Books-Data',args.content_commit,name)))
 manifest=dict(schemaVersion=1,scope='grade-nine-math-all-eight-chapters-and-whole-book',contentRepository='https://github.com/samanta-nz/Books-Data',contentCommit=args.content_commit,applicationRepository='https://github.com/samanta-nz/com.hamyareman.final',applicationCommit=args.app_commit,counts=dict(chapters=8,wholeBookScopes=1,htmlFiles=252,themeFiles=252,independentExams=216,chapterExams=192,wholeBookFinalExams=24,uniqueCanonicalQuestions=411,uniqueCanonicalCards=190),scopes=[scopes[k] for k in [1,2,3,4,5,6,7,8,0]],template=dict(repository='https://github.com/samanta-nz/Books-Data',commit=template_commit,readmeBlob=git(ROOT,'rev-parse',template_commit+':teaching - template/README.md').decode().strip(),readmeSha256=digest(git(ROOT,'show',template_commit+':teaching - template/README.md')),lockedManifestSha256=digest((template/'assets/LOCKED.sha256').read_bytes()),verifierCommand='python "teaching - template/tools/verify_locked.py"',verifierResult=verified,themeLoading='Exact theme bytes embedded in standalone HTML; same-name source theme shipped alongside.'),assets=assets,evidence=evidence,storage=dict(interface=['Hamyar.loadState','Hamyar.saveState','Hamyar.recordItem','Hamyar.recordExam'],existingStore='hamyar_math_html',accountScoped=True,newBackend=False),dependencies=[dict(id='author-verification',required=True,status='PASS',evidence='Recorded verification and byte-exact frozen-payload audit'),dict(id='independent-content-qa',required=True,status='NOT_RUN',owner='qa-analyzer'),dict(id='installed-app-compatibility',requiredFor='runtime activation',status='NOT_RUN',owner='app-development'),dict(id='bucket-sync',requiredFor='runtime activation',status='NOT_RUN',owner='content-sync'),dict(id='audio',required=False,status='N/A',reason='No audio requested in this batch')])
 if args.fresh_browser_evidence:
  regression=load(report/'qa-fix-20261019/remediation-tests.json');coverage=regression['byteCoverage']
  assert coverage['changedPagesExercised']==coverage['changedSinceComprehensive'] and coverage['unchangedPages']+coverage['changedPagesExercised']==252
  manifest['storage']['accountIsolationStatus']='M9-QA-003_OPEN_NATIVE_GUEST_LEGACY'
  manifest['priorQa']=dict(verdict='FAIL',packetSha256='80662e13947ff8ef7312ab61210e4f0ea6b652ecf126a54aa48345aaa71422c8',reportCommit='367979b00c7e192615e1c141069952d20eaef670')
  manifest['authorRemediation']=dict(findingIds=['M9-QA-001','M9-QA-002','M9-QA-004','M9-QA-005'],changedHtmlFiles=219,newCanonicalQuestionsAdded=0,canonicalPromptsCorrected=2,byteCoverage=coverage)
  for dep in manifest['dependencies']:
   if dep['id']=='independent-content-qa':dep['status']='PENDING_RETEST'
  manifest['dependencies'].append(dict(id='native-guest-legacy-isolation',requiredFor='full acceptance',status='OPEN',findingId='M9-QA-003',owner='app-development'))
 write(out/'all-files.manifest.json',manifest)
 audit=dict(contentCommit=args.content_commit,applicationCommit=args.app_commit,htmlHashMatches=252,themeHashMatches=252,sourceAndApplicationBlobMatches=504,embeddedLockedChecks=252*len(locked),payloadsComparedToExportedBanksAndExams=payload_matches,scopeCounts={str(k):v['files'] for k,v in scopes.items()},modeCounts=dict(modes),canonicalQuestions=411,canonicalCards=190,wholeBookPoolCountedTwice=False,existingBrowserEvidence=dict(passedGroups=23,exactHtmlBytesMatchBuildRecords=True,reexecuted=args.fresh_browser_evidence,bridge='mock using exact existing signatures'),existingAndroidEvidence=dict(tests=154,skipped=2,failures=0,deviceRun=False,reexecuted=False),newContentGenerated=False,existingRoutesModified=False,independentQa='PENDING_RETEST' if args.fresh_browser_evidence else 'NOT_RUN',bucketSync='NOT_RUN',apkRelease='NOT_RUN',verdict='AUTHOR_VERIFIED_EXISTING_OUTPUTS',limitations=['Independent QA receipt and runtime activation are separate steps.','No real Android-device execution is claimed.'])
 if args.fresh_browser_evidence:
  audit.update(verdict='AUTHOR_REMEDIATION_VERIFIED',newContentGenerated=True,changedHtmlFiles=219,newCanonicalQuestionsAdded=0,canonicalPromptsCorrected=2,priorQaVerdict='FAIL',accountIsolationFinding='M9-QA-003_OPEN',browserCoverage=coverage)
 write(out/'author-completion-audit.json',audit)
 print('PASS frozen full-book audit: 252 HTML, 252 themes, 216 exams, 411 canonical questions; no educational files rebuilt.')

if __name__=='__main__':main()
