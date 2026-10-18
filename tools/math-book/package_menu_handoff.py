"""Package a portable, small whole-book handoff for an agent in another workspace."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json,subprocess

ROOT=Path(__file__).resolve().parents[2]
REPORT=ROOT/'reports/math-book'
APP=Path('/workspace/hamyar-math-app')
def read(path):return json.loads(path.read_text())
def encoded(value):return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()

def main():
 routes=[r for r in read(REPORT/'routes.json')['routes'] if r['packId']=='C905_E00-SUM']
 assert len(routes)==28
 menu=read(APP/'grades/g09/src/main/assets/content/books-menu.json')
 book=next(b for b in menu['books'] if b['code']=='905' and b['folder']=='g9-math')
 entry=next(n for n in book['items'] if n['title']=='مرور جامع کل کتاب')
 pack=next(p for p in read(APP/'grades/g09/src/main/resources/math_c905.json') if p['packId']=='C905_E00-SUM')
 support=[
  'apps/student/src/main/assets/math/c905/hamyar-persist.js',
  'apps/student/src/main/java/com/hamyareman/ir/ui/study/BookNodeScreen.kt',
  'apps/student/src/main/java/com/hamyareman/ir/ui/study/MathHtmlWebView.kt',
  'features/feature-study/src/main/java/com/hamyareman/ir/platform/feature/study/MathExamLedger.kt',
  'features/feature-study/src/main/java/com/hamyareman/ir/platform/feature/study/StudyProgressRepository.kt',
  'features/feature-study/src/test/java/com/hamyareman/ir/platform/feature/study/MathExamLedgerTest.kt',
  'patches/src/main/java/com/hamyareman/ir/ui/study/HamyarHtmlAppearance.kt',
 ]
 helpers=['apps/student/src/main/java/com/hamyareman/ir/ui/study/BundledMathPractice.kt','apps/student/src/test/java/com/hamyareman/ir/ui/study/BundledMathPracticeTest.kt']
 patch=subprocess.check_output(['git','diff','--binary','c09746a5210c7fc9ea4e55fc48a97127b2f5a8d9','--',*support,*helpers],cwd=APP)
 for name in [
  'apps/student/src/main/java/com/hamyareman/ir/ui/study/BundledMathPractice.kt',
  'apps/student/src/test/java/com/hamyareman/ir/ui/study/BundledMathPracticeTest.kt',
 ]:
  if subprocess.run(['git','ls-files','--error-unmatch',name],cwd=APP,capture_output=True).returncode==0:continue
  p=subprocess.run(['git','diff','--no-index','--binary','--','/dev/null',name],cwd=APP,capture_output=True)
  assert p.returncode in (0,1);patch+=p.stdout
 patch_path=REPORT/'bridge-support.patch';patch_path.write_bytes(patch)
 subprocess.run(['git','apply','--check','--reverse',str(patch_path)],cwd=APP,check=True)
 assert all(b'grades/g09/src/main/'+s not in patch for s in [b'assets/content/books-menu.json',b'resources/math_c905.json',b'assets/content/math-practice-routes.json'])
 files={
  'APP_MENU_PROMPT.md':(REPORT/'APP_MENU_PROMPT.md').read_bytes(),
  'menu-entry.json':encoded(entry),
  'math-practice-routes.whole-book.json':encoded(dict(schemaVersion=1,bookCode='C905',scopes=[dict(scope=0,packId='C905_E00-SUM',directory='Bucket/Html-files/app/books/C905/N10.1')],routes=routes)),
  'study-pack.whole-book.json':encoded(pack),
  'bridge-support.patch':patch,
  'CONTENT_RULES.md':(ROOT/'CONTENT_RULES.md').read_bytes(),
  'AGENTS.md':(ROOT/'AGENTS.md').read_bytes(),
 }
 for route in routes:
  source=ROOT/route['bucketKey'];asset=APP/'grades/g09/src/main/assets'/route['assetPath']
  assert source.read_bytes()==asset.read_bytes()
  files['assets/'+route['assetPath']]=source.read_bytes()
  theme=source.parent/'assets/css/theme'/(source.stem+'.theme.css')
  files['assets/'+str(Path(route['assetPath']).parent/'assets/css/theme'/theme.name)]=theme.read_bytes()
 for p in (ROOT/'teaching - template').rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts:
   body=p.read_bytes()
   if p.name=='README.md':body=body.split(b'\n<!-- GENERATED-MATH-PRACTICE -->')[0]
   files[str(p.relative_to(ROOT))]=body
 files['README.md']=('''# تحویل مستقل منوی کل کتاب ریاضی نهم

این بسته برای انتقال واقعی فایل‌ها به ایجنتی در محیط دیگر است. نوشتن مسیر محیط تولید، دسترسی به فایل ایجاد نمی‌کند. ZIP را دانلود و خود فایل را به گفتگوی ایجنت مقصد پیوست کن.

ابتدا `python validate_handoff.py` و سپس `APP_MENU_PROMPT.md` خوانده شود. فقط خروجی‌های بخش کل کتاب در این بسته‌اند: بیست‌وهشت HTML و بیست‌وهشت Theme، چهار ورودی منو، بیست‌وچهار آزمون و دادهٔ هویت/کارت‌های کل کتاب. فایل‌های فصل‌های دیگر در این بسته نیستند و نباید مسیرهای ناموجود آن‌ها را به manifest مقصد اضافه کرد.

مسیر هر `assets/<assetPath>` داخل این بسته، در اپ به `grades/g09/src/main/assets/<assetPath>` و در Books-Data به همان `bucketKey` متناظر منتقل می‌شود. Themeها کنار همان HTML باقی بمانند. پوشهٔ teaching - template نسخهٔ راهنمای مرجع و فایل‌های قفل‌شده را دارد؛ جدول خروجی‌های سایر فصل‌های محیط تولید در این بستهٔ محدود تکرار نشده است.

patch پشتیبان شامل پل و رفتار WebView است و منو، manifest یا metadata تمام فصل‌ها را جایگزین نمی‌کند. سه JSON اختصاصی، بر اساس شناسه‌ها ادغام می‌شوند؛ داده‌های موجود مقصد حفظ شوند.

این بسته و سورس اپ با اجازهٔ کاربر در شاخهٔ codex/g9-math-whole-book روی GitHub پوش شده‌اند؛ لینک‌ها داخل پرامپت‌اند. bucket sync یا release انجام نشده است. برای تغییر یا انتشار تازه توسط ایجنت مقصد، دستور همان نشست ملاک است. منوی آماده و تست‌شدهٔ محیط تولید، اثبات اجرا روی گوشی مقصد نیست.
''').encode()
 files['validate_handoff.py']=b'''"""Read-only validation of the unpacked handoff; no application changes."""
from pathlib import Path
from zipfile import ZipFile
import hashlib,json,subprocess,sys
root=Path(__file__).resolve().parent
manifest=json.loads((root/'handoff-manifest.json').read_text())
for name,expected in manifest['files'].items():
    p=root/name
    assert p.is_file(), 'Missing handoff file: '+name
    assert hashlib.sha256(p.read_bytes()).hexdigest()==expected, 'Changed handoff file: '+name
routes=json.loads((root/'math-practice-routes.whole-book.json').read_text())['routes']
assert len(routes)==28 and all(r['packId']=='C905_E00-SUM' for r in routes)
for route in routes:
    p=root/'assets'/route['assetPath']
    assert p.is_file()
    assert (p.parent/'assets/css/theme'/(p.stem+'.theme.css')).is_file()
subprocess.run([sys.executable,str(root/'teaching - template/tools/verify_locked.py')],check=True)
print('OK: portable whole-book handoff; 28 HTML, 28 themes, menu and bridge inputs intact.')
'''
 manifest=dict(schemaVersion=1,scope='grade-nine-math-whole-book-menu',sourceApplication='https://github.com/samanta-nz/com.hamyareman.final.git',sourceBaseCommit='c09746a5210c7fc9ea4e55fc48a97127b2f5a8d9',htmlFiles=28,themeFiles=28,examFiles=24,packId='C905_E00-SUM',published=True,distribution='GitHub branch codex/g9-math-whole-book',files={name:hashlib.sha256(body).hexdigest() for name,body in sorted(files.items())})
 files['handoff-manifest.json']=encoded(manifest)
 out=REPORT/'whole-book-menu-handoff.zip'
 with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=9) as z:
  for name,body in sorted(files.items()):z.writestr(name,body)
 assert out.stat().st_size<30*1024*1024,'Keep the portable handoff below the file-reading size limit.'
 with ZipFile(out) as z:assert z.testzip() is None
 meta=dict(path=str(out),bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),files=len(files),htmlFiles=28,themeFiles=28,published=True)
 (REPORT/'menu-handoff.json').write_bytes(encoded(meta));print(json.dumps(meta,ensure_ascii=False))
if __name__=='__main__':main()
