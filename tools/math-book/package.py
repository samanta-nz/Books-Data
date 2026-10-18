"""Prepare local, reproducible review archives and the application patch; never publish."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json,subprocess

ROOT=Path(__file__).resolve().parents[2];REPORT=ROOT/'reports/math-book';APP=Path('/workspace/hamyar-math-app')
def read(path):return json.loads(path.read_text())
def main():
 browser=read(REPORT/'browser-tests.json');android=read(REPORT/'android-tests.json');build=read(REPORT/'build-report.json')
 assert browser['contentVersion']==build['contentVersion'] and not browser['errors'] and not browser['externalRequests']
 assert browser['pages']==252 and android['build']=='passed' and android['byteComparisons']==252
 routes=read(REPORT/'routes.json')['routes'];htmlfiles=[]
 for route in routes:
  f=ROOT/route['bucketKey'];asset=APP/'grades/g09/src/main/assets'/route['assetPath']
  assert f.read_bytes()==asset.read_bytes()
  assert f.stat().st_mtime<=(REPORT/'browser-tests.json').stat().st_mtime,'HTML changed after browser validation'
  htmlfiles.append(f)
 for f in build['generatedFiles']:assert hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()==f['sha256']
 assert len(htmlfiles)==len(set(htmlfiles))==252
 core=['apps/student/src/main/assets/math/c905/hamyar-persist.js','apps/student/src/main/java/com/hamyareman/ir/ui/study/BookNodeScreen.kt','apps/student/src/main/java/com/hamyareman/ir/ui/study/MathHtmlWebView.kt','apps/student/src/main/java/com/hamyareman/ir/ui/study/BundledMathPractice.kt','apps/student/src/test/java/com/hamyareman/ir/ui/study/BundledMathPracticeTest.kt','features/feature-study/src/main/java/com/hamyareman/ir/platform/feature/study/MathExamLedger.kt','features/feature-study/src/main/java/com/hamyareman/ir/platform/feature/study/StudyProgressRepository.kt','features/feature-study/src/test/java/com/hamyareman/ir/platform/feature/study/MathExamLedgerTest.kt','grades/g09/src/main/assets/content/books-menu.json','grades/g09/src/main/resources/math_c905.json','grades/g09/src/main/assets/content/math-practice-routes.json','patches/src/main/java/com/hamyareman/ir/ui/study/HamyarHtmlAppearance.kt']
 patch=subprocess.run(['git','diff','--binary','c09746a5210c7fc9ea4e55fc48a97127b2f5a8d9','--',*core],cwd=APP,capture_output=True,check=True).stdout
 for name in [
  'apps/student/src/main/java/com/hamyareman/ir/ui/study/BundledMathPractice.kt',
  'apps/student/src/test/java/com/hamyareman/ir/ui/study/BundledMathPracticeTest.kt',
  'grades/g09/src/main/assets/content/math-practice-routes.json']:
  if subprocess.run(['git','ls-files','--error-unmatch',name],cwd=APP,capture_output=True).returncode==0:continue
  p=subprocess.run(['git','diff','--no-index','--binary','--','/dev/null',name],cwd=APP,capture_output=True)
  assert p.returncode in (0,1);patch+=p.stdout
 (REPORT/'application-code.patch').write_bytes(patch)
 # Keep the earlier chapter-only download consistent with the newly generated HTML.
 (ROOT/'reports/math-f01/application-code.patch').write_bytes(patch)
 files=[ROOT/'CONTENT_RULES.md',ROOT/'AGENTS.md',ROOT/'tools/teaching_shell.py']+htmlfiles
 files += [f.parent/'assets/css/theme'/(f.stem+'.theme.css') for f in htmlfiles]
 for folder in [ROOT/'teaching - template',ROOT/'tools/math-f01',ROOT/'tools/math-book',ROOT/'reports/math-f01',REPORT]:
  files += [p for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.zip','.pyc') and p.name!='package.json']
 out=REPORT/'hamyar-math-book.zip'
 with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=9) as archive:
  for f in sorted(set(files)):archive.write(f,f.relative_to(ROOT))
 with ZipFile(out) as archive:assert archive.testzip() is None
 metadata=dict(path=str(out),files=len(set(files)),bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),published=False)
 (REPORT/'package.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
 subprocess.run(['python',str(ROOT/'tools/math-f01/package.py')],check=True)
 print(json.dumps(metadata,ensure_ascii=False))
if __name__=='__main__':main()
