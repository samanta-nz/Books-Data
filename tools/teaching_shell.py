"""Use the real upstream teaching shell without modifying any locked asset.

Source themes are separate real files; offline HTML embeds their exact bytes and
the exact locked files, as the provided standalone preview does.
"""
from pathlib import Path
import base64,hashlib,html,json,re,subprocess

ROOT=Path(__file__).resolve().parent.parent
TEMPLATE=ROOT/'teaching - template'
REVISION='51afd4c3a91be6026668fa248aaaa762c384bd70'
LOCKED=sorted((TEMPLATE/'assets/css/locked').glob('*.css'))

def verify_locked():
 subprocess.run(['python',str(TEMPLATE/'tools/verify_locked.py')],check=True)

def theme_css(extra=''):
 result=(TEMPLATE/'assets/css/theme/ryazif01d01.theme.css').read_text()
 result+='\n/* Dedicated assessment/card content; shared shell remains locked. */\n'
 for weight,name in [(400,'Regular'),(500,'Medium'),(700,'Bold')]:
  encoded=base64.b64encode((ROOT/f'tools/math-f01/fonts/Vazir-{name}-FD.woff2').read_bytes()).decode()
  result+='@font-face{font-family:Vazir;font-weight:'+str(weight)+';font-style:normal;font-display:swap;src:url(data:font/woff2;base64,'+encoded+') format("woff2");}\n'
 result+=(ROOT/'tools/math-f01/practice.css').read_text()+'\n'+extra
 result+='\nheader#top h1,.ftr-card strong,.ftr-card .ftr-app,.fab-title{font-weight:700}.fab-wrap button{font-weight:500}\n'
 return result

def make_page(output,packaged,title,data,body,runtime,extra_css=''):
 source=(TEMPLATE/'ryazif01d01.html').read_text()
 # Both the standalone reference and the completed modular lesson are inspected.
 assert '<header' in (TEMPLATE/'lesson-template.preview-standalone.html').read_text()
 header=re.search(r'<header\b[\s\S]*?</header>',source).group()
 header=re.sub(r'<h1>[\s\S]*?</h1>','<h1>'+html.escape('ریاضی نهم — '+data['chapterTitle'])+'</h1><p class="page-subtitle">'+html.escape(title)+'</p>',header)
 footer=re.search(r'<footer\b[\s\S]*?</footer>',source).group()
 footer=re.sub(r'<strong>[\s\S]*?</strong>','<strong>📘 '+html.escape(title)+'</strong>',footer,count=1)
 body=body.replace('class="intro','class="hero intro')
 anchors=[('main','محتوای این صفحه')]
 def section(match):
  n=sum(k.startswith('topic-') for k,_ in anchors)+1;key='topic-'+str(n)
  heading=html.unescape(re.sub('<[^>]+>','',match[1]))
  anchors.append((key,heading))
  return '<section class="summary-section lesson-section" id="'+key+'"><h2>'+match[1]+'</h2>'
 body=re.sub(r'<section class="summary-section"><h2>([\s\S]*?)</h2>',section,body)
 for key,label in [('assessment-workspace','پاسخ‌گویی به آزمون'),('question-list','سؤال‌ها'),('flash-list','کارت جاری'),('paper-pages','برگهٔ امتحان')]:
  if 'id="'+key+'"' in body:anchors.append((key,label))
 floater=source[source.index('<div class="fab-wrap"'):source.index('<script src="assets/js/locked/ui.js">')]
 floater=re.sub(r'<nav class="fab-toc"[\s\S]*?</nav>','<nav class="fab-toc" aria-label="فهرست همین صفحه">'+''.join('<a href="#'+k+'">'+label+'</a>' for k,label in anchors)+'</nav>',floater)
 floater=floater.replace('فهرست این درس','پیمایش صفحه').replace('فهرست و ابزارهای درس','فهرست و ابزارهای صفحه')
 custom=(
  "document.getElementById('motion-toggle').addEventListener('click',function(e){var stopped=document.body.classList.toggle('no-motion');e.currentTarget.setAttribute('aria-pressed',String(stopped));e.currentTarget.textContent=stopped?'ادامهٔ حرکت‌های تزئینی':'توقف حرکت‌های تزئینی';});"
  "document.querySelectorAll('.fab-toc a').forEach(function(a){a.addEventListener('click',function(){var t=document.querySelector(a.getAttribute('href'));for(var p=t;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true;});});"
 )
 motifs={0:['Σ','∪','π'],1:['{ }','∈','∅'],2:['ℝ','√','|x|'],3:['△','∠','≅'],4:['aⁿ','√','∛'],5:['x','a+b','≠'],6:['x','y','↗'],7:['P/Q','x','≠'],8:['π','△','∛']}[data['chapterNumber']]
 theme=theme_css(extra_css)+'\n:root{'+''.join('--motif-'+str(i+1)+':"'+s+'";' for i,s in enumerate(motifs))+'}\n'
 theme_path=output.parent/'assets/css/theme'/(output.stem+'.theme.css')
 app_theme=packaged.parent/'assets/css/theme'/theme_path.name
 for p in [theme_path,app_theme]:p.parent.mkdir(parents=True,exist_ok=True);p.write_text(theme)
 styles=''.join('<style data-locked-source="'+str(p.relative_to(TEMPLATE))+'">'+p.read_text()+'</style>' for p in LOCKED)
 styles+='<style data-page-theme="assets/css/theme/'+theme_path.name+'">'+theme+'</style>'
 license_match=re.search(r'<script type="text/plain" id="font-license">[\s\S]*?</script>',source)
 licenses=license_match.group().replace('id="font-license"','id="template-font-license"') if license_match else ''
 licenses+='<script type="text/plain" id="font-license">'+(ROOT/'tools/math-f01/fonts/LICENSE').read_text()+'</script>'
 jsdata=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
 eye_init=re.search(r'<script>try\{var e=localStorage[\s\S]*?</script>',source).group()
 return ('<!doctype html><html lang="fa" dir="rtl" data-eye="2" data-hamyar-fixed-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="color-scheme" content="only light"><meta name="supported-color-schemes" content="light only"><meta name="theme-color" content="#261a5e"><meta name="darkreader-lock"><meta name="hamyar-template-revision" content="'+REVISION+'"><title>'+html.escape(title)+' — همیار من</title>'+eye_init+styles+licenses+'</head><body class="book-math"><a class="skip" href="#main">رفتن به محتوای صفحه</a><div class="container">'+header+'<main id="main"><noscript><p>برای اجرای فعالیت‌ها جاوااسکریپت نمایشگر فعال باشد.</p></noscript>'+body+'<p id="storage-status" role="status"></p></main>'+footer+'</div>'+floater+'<script data-locked-source="assets/js/locked/ui.js">'+(TEMPLATE/'assets/js/locked/ui.js').read_text()+'</script><script>'+custom+'</script><script id="practice-data" type="application/json">'+jsdata+'</script>'+runtime+'</body></html>')

def register_generated():
 """List only files actually present, after both builders have finished."""
 directory=ROOT/'Bucket/Html-files/app/books/C905';rows=[];files=[]
 for output in sorted(directory.glob('N*/*.html')):
  theme=output.parent/'assets/css/theme'/(output.stem+'.theme.css');assert theme.is_file()
  data=json.loads(re.search(r'<script id="practice-data" type="application/json">([\s\S]*?)</script>',output.read_text()).group(1))
  path=output.relative_to(ROOT).as_posix();theme_path=theme.relative_to(ROOT).as_posix()
  rows.append('| '+data['chapterTitle']+'؛ '+data['mode']+' | `../'+path+'` | `../'+theme_path+'` |')
  files.append(dict(html=path,theme=theme_path,templateRevision=REVISION))
 readme=TEMPLATE/'README.md';text=readme.read_text();marker='\n<!-- GENERATED-MATH-PRACTICE -->'
 text=text.split(marker)[0]+marker+'\n\n## خروجی‌های واقعی مرور و آزمون ریاضی نهم\n\nاین فایل‌ها درس مستقل جدید نیستند؛ نام TAB آن‌ها از منوی واقعی اپ حفظ شده است. Theme هر فایل هم‌نام خودش و در مسیر واقعی زیر قرار دارد؛ برای اجرای مستقل آفلاین، همان Theme و فایل‌های قفل‌شده بدون تغییر داخل HTML نیز تعبیه شده‌اند.\n\n| محدوده و کاربرد | HTML واقعی | Theme واقعی |\n|---|---|---|\n'+'\n'.join(rows)+'\n'
 readme.write_text(text)
 report=dict(upstream='https://github.com/samanta-nz/Books-Data/tree/main/teaching%20-%20template',revision=REVISION,reference='teaching - template/lesson-template.preview-standalone.html',completedExample='teaching - template/ryazif01d01.html',lockedFiles={str(p.relative_to(TEMPLATE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in LOCKED+[TEMPLATE/'assets/js/locked/ui.js']},generatedFiles=files,lockedVerification='OK — all locked files intact',fontCompatibility='Actual Vazir FD 400/500/700 kept in page themes by explicit user rule; locked Vazirmatn assets remain byte-identical.')
 (ROOT/'reports/math-book/template-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 verify_locked()
