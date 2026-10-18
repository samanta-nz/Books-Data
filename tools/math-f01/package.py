"""Package local review artifacts; never uploads or publishes anything."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];REPORT=ROOT/'reports/math-f01'
current=ROOT/'reports/math-book/browser-tests.json'
if current.exists():
    browser=json.loads(current.read_text());android=json.loads((current.parent/'android-tests.json').read_text())
    assert browser['pages']==252 and browser['contentVersion']=='2026-10-18.book-1' and not browser['errors']
    assert android['build']=='passed' and android['mergedHtmlFiles']==252
else:
    assert json.loads((REPORT/'browser-tests.json').read_text())['contentVersion']=='2026-10-18.2'
    assert json.loads((REPORT/'android-assets-current.json').read_text())['mergeP09DebugAssets']=='passed'
files=[ROOT/'CONTENT_RULES.md']+list((ROOT/'Bucket/Html-files/app/books/C905/N2.5').glob('*.html'))
files += list((ROOT/'Bucket/Html-files/app/books/C905/N2.5/assets/css/theme').glob('*.css'))
files += [ROOT/'AGENTS.md',ROOT/'tools/teaching_shell.py']
files += [p for p in (ROOT/'teaching - template').rglob('*') if p.is_file() and '__pycache__' not in p.parts]
files += [p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
files += [p for p in REPORT.iterdir() if p.is_file() and p.suffix in ('.md','.json','.patch','.png','.txt') and not p.name.endswith('-preview.png')]
if current.exists():
    files += [current,current.parent/'android-tests.json',current.parent/'README.md',current.parent/'APP_MENU_PROMPT.md',current.parent/'routes.json']
out=REPORT/'hamyar-math-f01.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=9) as z:
 for file in sorted(set(files)):z.write(file,file.relative_to(ROOT))
with ZipFile(out) as z:assert z.testzip() is None
print('Review package:',out,'files:',len(files),'bytes:',out.stat().st_size,'sha256:',hashlib.sha256(out.read_bytes()).hexdigest())
