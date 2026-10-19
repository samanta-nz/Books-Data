#!/usr/bin/env python3
"""Build standalone HTML and the matching packaged grade-nine assets, offline."""
from pathlib import Path
import argparse, json, re, html, hashlib, shutil, base64, sys
from html.parser import HTMLParser
from collections import Counter
from bank import questions, essay_questions, LEVELS
from verify import run as verify
from research import audit, SOURCES

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
sys.path.insert(0,str(HERE.parent))
from teaching_shell import make_page,verify_locked
DEFAULT_APP=Path('/workspace/hamyar-math-app')

CARDS=[
 ('معرفی مجموعه','چه توصیفی یک مجموعه را مشخص می‌کند؟','باید بتوان عضویت هر شیء را بدون سلیقه و ابهام تعیین کرد.'),
 ('معرفی مجموعه','آیا ترتیب اعضا و تکرارشان مجموعه را عوض می‌کند؟','خیر؛ اعضای متمایز مهم‌اند. {2,5,2}={5,2}.'),
 ('معرفی مجموعه','n(A) چه چیزی را می‌شمارد؟','تعداد اعضای متمایز A؛ هر عضو تکراری یک بار شمرده می‌شود.'),
 ('معرفی مجموعه','تفاوت ∅ و {0} چیست؟','اولی هیچ عضو و دومی یک عضو به نام صفر دارد.'),
 ('معرفی مجموعه','تفاوت ∅ و {∅} چیست؟','∅ تهی است؛ {∅} یک عضو دارد و آن عضو خودش یک مجموعهٔ تهی است.'),
 ('معرفی مجموعه','آیا «سه عدد بزرگ» مجموعه‌ای مشخص است؟','خیر؛ بزرگی و اعضای دقیق تعیین نشده‌اند.'),
 ('نمایش و زیرمجموعه','نمادهای ∈ و ⊆ چه تفاوتی دارند؟','∈ رابطهٔ شیء با مجموعه است؛ ⊆ رابطهٔ دو مجموعه. از a∈A، رابطهٔ {a}⊆A نتیجه می‌شود.'),
 ('نمایش و زیرمجموعه','دو مجموعه چه وقت برابرند؟','وقتی هر عضو اولی در دومی و هر عضو دومی در اولی باشد.'),
 ('نمایش و زیرمجموعه','چگونه فهرست اعضای {x∈ℤ | −2<x≤2} را بنویسم؟','اعضا {-1,0,1,2} هستند؛ نوع عدد و باز یا بسته بودن کران مهم است.'),
 ('نمایش و زیرمجموعه','قرارداد ℕ در این بسته چیست؟','ℕ={1,2,3,…} و W={0,1,2,…}؛ هر پرسش با دامنهٔ متفاوت، آن را صریح تعیین می‌کند.'),
 ('نمایش و زیرمجموعه','آیا مجموعه زیرمجموعهٔ خودش است؟','بله؛ همهٔ اعضایش در خودش هستند.'),
 ('نمایش و زیرمجموعه','چرا تهی زیرمجموعهٔ هر مجموعه است؟','در تهی عضوی نیست که شرطِ حضور در مجموعهٔ مقصد را نقض کند.'),
 ('نمایش و زیرمجموعه','یک مجموعهٔ n عضوی چند زیرمجموعه دارد؟','2ⁿ؛ هر عضو یا انتخاب می‌شود یا نمی‌شود. تهی و خود مجموعه هم شمرده می‌شوند.'),
 ('نمایش و زیرمجموعه','زیرمجموعه‌های {a,b} کدام‌اند؟','∅، {a}، {b} و {a,b}. چهار مجموعهٔ متفاوت داریم.'),
 ('عملیات مجموعه‌ها','اجتماع A∪B چیست؟','عضوهایی که در A یا B یا هر دو هستند؛ مشترک‌ها یک بار نوشته می‌شوند.'),
 ('عملیات مجموعه‌ها','اشتراک A∩B چیست؟','عضوهایی که هم‌زمان در هر دو مجموعه قرار دارند.'),
 ('عملیات مجموعه‌ها','تفاضل A−B چیست؟','عضوهای A که در B نیستند؛ A−B معمولاً با B−A برابر نیست.'),
 ('عملیات مجموعه‌ها','رابطهٔ تعداد اعضای اجتماع چیست؟','n(A∪B)=n(A)+n(B)−n(A∩B).'),
 ('عملیات مجموعه‌ها','اگر A⊆B باشد، اجتماع و اشتراک چه می‌شوند؟','A∪B=B و A∩B=A.'),
 ('عملیات مجموعه‌ها','از A−B=∅ چه نتیجه می‌گیریم؟','همهٔ اعضای A در B هستند؛ پس A⊆B. برابری لزوماً نتیجه نمی‌شود.'),
 ('عملیات مجموعه‌ها','ناحیهٔ فقط A در نمودار ون کدام است؟','بخشی از دایرهٔ A که بیرون دایرهٔ B است؛ همان A−B.'),
 ('عملیات مجموعه‌ها','در عملیات چندمرحله‌ای از کجا شروع کنم؟','از داخل پرانتز؛ اعضای هر مرحله را جداگانه بنویس تا عضو مشترک اشتباه حذف نشود.'),
 ('مجموعه‌ها و احتمال','چه وقت P(A)=n(A)/n(S) معتبر است؟','وقتی حالت‌های فضای نمونه هم‌شانس باشند و S متناهی و غیرتهی باشد.'),
 ('مجموعه‌ها و احتمال','پیشامد ناممکن و حتمی چه احتمالی دارند؟','ناممکن صفر و حتمی یک؛ احتمال هر پیشامد بین صفر و یک است.'),
 ('مجموعه‌ها و احتمال','فضای نمونهٔ دو سکهٔ سالم چیست؟','با رعایت ترتیب: RR، RP، PR، PP؛ چهار حالت هم‌شانس.'),
 ('مجموعه‌ها و احتمال','دو تاس سالم رنگی چند حالت هم‌شانس دارند؟','36 زوج مرتب؛ (1,2) و (2,1) متفاوت‌اند.'),
 ('مجموعه‌ها و احتمال','چرا مجموع‌های دو تاس هم‌شانس نیستند؟','برای هر مجموع، تعداد زوج‌های مرتب متفاوت است؛ مجموع 2 یک حالت و مجموع 7 شش حالت دارد.'),
 ('مجموعه‌ها و احتمال','«و»، «یا» و «حداقل» را چگونه بخوانم؟','«و» اشتراک است؛ «یا» اجتماع شامل اشتراک؛ «حداقل یک» را می‌توان با حذف «هیچ» به‌دست آورد.'),
]

SUMMARY='''<section class="intro"><span class="badge">خلاصهٔ فصل و نکات امتحانی</span><h2>چهار گام برای تسلط بر مجموعه‌ها</h2><p>تعریف و نمادها را بشناس، اعضا را درست نمایش بده، عملیات را مرحله‌به‌مرحله انجام بده و برای احتمال، حالت‌های هم‌شانس را بشمار.</p><div class="summary-key"><span class="key-concept">تعریف و مفهوم</span><span class="key-rule">قاعدهٔ مهم</span><span class="key-example">مثال حل‌شده</span><span class="key-trap">دام امتحانی</span></div></section>
<section class="summary-section"><h2>۱. مجموعه و اعضای آن</h2><div class="study-note concept"><h3>تعریف روشن</h3><p>مجموعه دسته‌ای از اشیاست که بتوانیم عضویت هر شیء را بدون سلیقه تشخیص بدهیم؛ «عددهای صحیح بین ۲ و ۶» مشخص است، ولی «چند عدد بزرگ» مشخص نیست.</p></div><div class="study-note rule"><h3>مهم: فقط اعضای متمایز را بشمار</h3><p>ترتیب و تکرار، مجموعه را تغییر نمی‌دهد؛ <bdi dir="ltr">{۲،۵،۲}={۵،۲}</bdi> و تعداد اعضای آن ۲ است. تعداد اعضا را با <bdi dir="ltr">n(A)</bdi> نشان می‌دهیم.</p></div><div class="study-note trap"><h3>دام امتحانی: تهی با صفر فرق دارد</h3><p><bdi dir="ltr">∅</bdi> هیچ عضو ندارد؛ <bdi dir="ltr">{۰}</bdi> یک عضو به نام صفر دارد؛ <bdi dir="ltr">{∅}</bdi> نیز یک عضو دارد که خودش یک مجموعهٔ تهی است.</p></div></section>
<section class="summary-section"><h2>۲. نمایش، عضویت و زیرمجموعه</h2><div class="study-note concept"><h3>نمادها را دقیق بخوان</h3><p><bdi dir="ltr">a∈A</bdi> یعنی a عضو A است؛ <bdi dir="ltr">B⊆A</bdi> یعنی هر عضو B در A هم وجود دارد. دو مجموعه زمانی برابرند که دقیقاً اعضای یکسان داشته باشند.</p><p>در این بسته: <bdi dir="ltr">ℕ={۱،۲،۳،…}</bdi> و <bdi dir="ltr">W={۰،۱،۲،…}</bdi>؛ دامنهٔ هر سؤال را بخوان.</p></div><div class="study-note example"><h3>مثال: از شرط به اعضا</h3><p><bdi dir="ltr">{x∈ℤ | −۲&lt;x≤۲}={−۱،۰،۱،۲}</bdi></p><p>ابتدا عددهای صحیح را انتخاب کن؛ کران −۲ به علت علامت کوچک‌تر پذیرفته نیست و کران ۲ به علت کوچک‌تر یا مساوی پذیرفته است.</p></div><div class="study-note rule"><h3>قاعدهٔ شمارش زیرمجموعه‌ها</h3><p>تهی زیرمجموعهٔ هر مجموعه است و هر مجموعه زیرمجموعهٔ خودش است؛ یک مجموعهٔ n عضوی <bdi dir="ltr">۲ⁿ</bdi> زیرمجموعه دارد، چون برای هر عضو دو انتخابِ بودن یا نبودن داریم.</p><p>مثال: مجموعهٔ سه‌عضوی ۸ زیرمجموعه دارد؛ این عدد، تعداد اعضای مجموعه نیست.</p></div><div class="study-note trap"><h3>دام امتحانی: آکولاد را حذف نکن</h3><p>اگر <bdi dir="ltr">A={۱،{۲}}</bdi> باشد، <bdi dir="ltr">{۲}∈A</bdi> درست و <bdi dir="ltr">۲∈A</bdi> نادرست است؛ عضو دوم A خودش یک مجموعه است.</p></div></section>
<section class="summary-section"><h2>۳. اجتماع، اشتراک و تفاضل</h2><div class="study-note concept"><h3>معنای هر عمل</h3><ul class="section-list"><li><strong>اجتماع A∪B:</strong> عضوهایی که دست‌کم در یکی از دو مجموعه‌اند.</li><li><strong>اشتراک A∩B:</strong> عضوهایی که هم در A و هم در B هستند.</li><li><strong>تفاضل A−B:</strong> عضوهایی که در A هستند و در B نیستند؛ از A شروع کن و عضوهای B را حذف کن.</li></ul></div><div class="study-note example"><h3>یک مثال برای مقایسهٔ سه عمل</h3><p><bdi dir="ltr">A={۴،۷،۹}, B={۷،۹،۱۲}</bdi></p><p>اجتماع: <bdi dir="ltr">{۴،۷،۹،۱۲}</bdi>؛ اشتراک: <bdi dir="ltr">{۷،۹}</bdi>؛ تفاضل A−B: <bdi dir="ltr">{۴}</bdi>؛ تفاضل B−A: <bdi dir="ltr">{۱۲}</bdi>.</p></div><div class="study-note rule"><h3>مهم: عضو مشترک را یک بار بشمار</h3><p><bdi dir="ltr">n(A∪B)=n(A)+n(B)−n(A∩B)</bdi></p><p>مثال: ۱۲ نفر عضو A، ده نفر عضو B و ۴ نفر عضو هر دو هستند؛ پس اجتماع ۱۸ نفر است.</p></div><div class="study-note trap"><h3>دام امتحانی: جهت و پرانتز</h3><p>تفاضل معمولاً جابه‌جایی‌پذیر نیست؛ در عبارت چندمرحله‌ای ابتدا داخل پرانتز را حساب کن و هر مرحله را جدا بنویس.</p></div></section>
<section class="summary-section"><h2>۴. احتمال و فضای نمونه</h2><div class="study-note rule"><h3>قاعده با شرط مهم</h3><p>اگر فضای نمونه متناهی و حالت‌ها <strong>هم‌شانس</strong> باشند: <bdi dir="ltr">P(A)=n(A)/n(S)</bdi>؛ تعداد حالت‌های مطلوب را بر کل حالت‌ها تقسیم کن. احتمال ناممکن صفر و احتمال حتمی یک است.</p></div><div class="study-note example"><h3>مثال: دو تاس رنگی</h3><p>۶×۶ یعنی ۳۶ زوج مرتبِ هم‌شانس داریم؛ برای مجموع ۵، زوج‌های <bdi dir="ltr">(۱،۴)، (۲،۳)، (۳،۲)، (۴،۱)</bdi> مطلوب‌اند، پس احتمال <bdi dir="ltr">۴/۳۶=۱/۹</bdi> است.</p></div><div class="study-note trap"><h3>دام امتحانی: صورت سؤال را ترجمه کن</h3><ul class="section-list"><li>«و» یعنی اشتراک؛ «یا» یعنی اجتماع و شامل حالت مشترک هم می‌شود.</li><li>«دقیقاً یکی» حالت مشترک را نمی‌پذیرد؛ «حداقل یکی» را می‌توان با حذف حالت «هیچ‌کدام» شمرد.</li><li>مجموع‌های ۲ تا ۱۲ در دو تاس، هم‌شانس نیستند؛ زوج‌های مرتب را بشمار.</li><li>در برداشت بدون بازگرداندن، تعداد مهره‌های کل و رنگِ برداشته‌شده تغییر می‌کند.</li></ul></div></section>
<section class="study-note checklist"><h2>پیش از تحویل برگه بررسی کن</h2><p>دامنه و کران‌ها را خوانده‌ام؛ عضو تکراری را نشمرده‌ام؛ ∈ را با ⊆ عوض نکرده‌ام؛ جهت تفاضل را نگه داشته‌ام؛ اشتراک را دوبار نشمرده‌ام؛ هم‌شانس بودن حالت‌ها را بررسی کرده‌ام.</p></section><aside class="study-note concept"><h2>تمرین‌های سطح درخشان</h2><p>این سطح برای شمارش محدود زیرمجموعه‌ها، سه مجموعه و استدلال چندمرحله‌ای است؛ برای امتحان معمول مدرسه، ابتدا سه سطح اول را کامل کن.</p></aside>'''

DIGITS=str.maketrans('0123456789٠١٢٣٤٥٦٧٨٩','۰۱۲۳۴۵۶۷۸۹۰۱۲۳۴۵۶۷۸۹')
class PersianHTML(HTMLParser):
    """Convert human-facing text without touching paths, identifiers or script data."""
    def __init__(self):super().__init__(convert_charrefs=False);self.parts=[];self.raw=0
    def handle_starttag(self,tag,attrs):
        self.parts.append(self.get_starttag_text())
        if tag in ('script','style'):self.raw+=1
    def handle_startendtag(self,tag,attrs):self.parts.append(self.get_starttag_text())
    def handle_endtag(self,tag):
        self.parts.append('</'+tag+'>')
        if tag in ('script','style'):self.raw-=1
    def handle_data(self,data):self.parts.append(data if self.raw else data.translate(DIGITS))
    def handle_entityref(self,name):self.parts.append('&'+name+';')
    def handle_charref(self,name):self.parts.append('&#'+name+';')
    def handle_comment(self,data):self.parts.append('<!--'+data+'-->')
    def handle_decl(self,decl):self.parts.append('<!'+decl+'>')
def persian_html(text):
    parser=PersianHTML();parser.feed(text);return ''.join(parser.parts)

def jsjson(obj):return json.dumps(obj,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')

def exam_body(label,assessment=False):
    ending='<section id="finish-confirm" hidden role="region" aria-label="تأیید پایان آزمون"><p id="finish-warning"></p><div class="controls"><button id="finish-yes" type="button">پایان آزمون و تصحیح</button><button id="finish-no" type="button">ادامهٔ پاسخ‌گویی</button></div></section><section id="final-result" class="result-box" tabindex="-1" aria-live="polite" hidden></section>'
    if assessment:
        return '<section class="intro assessment-intro"><span class="badge">'+label+'</span><h2>خودآزمایی مستقل</h2><p>پاسخ‌ها تا پایان قابل تغییرند؛ تصحیح، پاسخ صحیح و نتیجه فقط پس از پایان آزمون نمایش داده می‌شوند.</p></section><div id="assessment-workspace"><div class="assessment-status"><strong id="question-position"></strong><span id="assessment-progress" role="status"></span></div><progress id="progress" value="0" max="14" aria-label="پیشرفت پاسخ‌گویی"></progress><nav id="question-navigator" aria-label="رفتن به سؤال"></nav></div>'+ending+'<h2 id="review-heading" hidden>مرور پاسخ‌ها پس از آزمون</h2><div id="question-list" tabindex="-1"></div><div id="assessment-controls" class="controls"><button id="assessment-prev" type="button">سؤال قبلی</button><button id="assessment-next" type="button" class="primary">سؤال بعدی</button></div><div class="controls end-controls"><button type="button" class="primary" id="finish">پایان آزمون و تصحیح</button><button type="button" id="restart" hidden>آزمون دوباره</button><button type="button" id="export-errors">دریافت خطاهای ثبت‌شده</button></div>'
    return '<section class="intro"><span class="badge">'+label+'</span><h2>تمرین همراه با بازخورد</h2><p>پاسخ هر سؤال را ثبت کن؛ اگر اشتباه باشد، علت احتمالی و راه درست همان‌جا توضیح داده می‌شود. سؤال‌های تشریحی راهنمای تصحیح دارند.</p><div id="stats" aria-live="polite"></div><progress id="progress" value="0" max="1" aria-label="تعداد پاسخ ثبت‌شده"></progress></section><div id="question-list" tabindex="-1"></div><div class="controls"><button type="button" class="primary" id="finish">پایان تمرین و محاسبهٔ نتیجه</button><button type="button" id="restart" hidden>تمرین دوباره</button><button type="button" id="export-errors">دریافت خطاهای ثبت‌شده</button></div>'+ending

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--app',type=Path,default=DEFAULT_APP);args=parser.parse_args()
    verify()
    menu_path=args.app/'grades/g09/src/main/assets/content/books-menu.json'
    menu=json.loads(menu_path.read_text())
    book=next(b for b in menu['books'] if b['code']=='905' and b['subject']=='ریاضی نهم')
    chapter=next(n for n in book['items'] if n['title'].startswith('فصل ۱:'))
    wrap=next(n for n in chapter['children'] if n['kind']=='wrapup')
    keys={str(i):t['key'] for i,t in enumerate(wrap['tabs'],1)}
    assert '/C905/N2.5/TAB02.html' in keys['2']
    directory=Path(keys['2']).parent
    output=REPO/directory;output.mkdir(parents=True,exist_ok=True)
    packaged=args.app/'grades/g09/src/main/assets/math/c905/practice/N2.5';packaged.mkdir(parents=True,exist_ok=True)
    verify_locked()
    runtime=(HERE/'runtime.js').read_text()
    routes=[];generated=[];version='2026-10-18.2'
    report=audit()
    def page(filename,title,body,kind,questions_=None,cards=None,variant=0,mode=None):
        docid='f01-'+filename[:-5].lower()
        data=dict(id=docid,kind=kind,variant=variant,contentVersion=version,mode=mode or kind,scopeId='f01',packId='C905_E01-SUM',chapterNumber=1,chapterTitle='فصل اول: مجموعه‌ها')
        if mode=='assessment':data['contentVersion']='2026-10-19.qa-fix-1'
        if questions_ is not None:data['questions']=questions_
        if cards is not None:data['cards']=cards
        text=make_page(output/filename,packaged/filename,title,data,body,'<script>'+runtime+'</script>')
        text=persian_html(text)
        (output/filename).write_text(text)
        (packaged/filename).write_text(text)
        key=str(directory/filename)
        routes.append(dict(bucketKey=key,assetPath='math/c905/practice/N2.5/'+filename,packId='C905_E01-SUM',kind=kind))
        generated.append(dict(path=key,sha256=hashlib.sha256(text.encode()).hexdigest(),kind=kind,questionCount=len(questions_ or [])))
    canonical=questions(0)+essay_questions()
    for index,q in enumerate(canonical,1):
        q['id']=f'f01-bank-q{index:02d}'
        q['sources']=['openstax','gharavi'] if q['level']<=2 else ['mamoallemim'] if q['level']==3 else []
        q['provenanceRelation']='تطبیق مفهومی؛ متن و مقدارها تألیفی' if q['sources'] else 'تألیفی تکمیلی؛ مبتنی بر شمارش متناهی و صحت‌سنجی مستقل'
    page('TAB03.html','جمع‌بندی فصل و نکات امتحانی',SUMMARY,'summary')
    cards=[dict(id=f'f01-card-{i+1:02d}',topic=t,front=f,back=b) for i,(t,f,b) in enumerate(CARDS)]
    page('TAB02.html','فلش‌کارت‌های فصل اول','<section class="intro"><span class="badge">مرور فعال</span><h2>اول پاسخ را به یاد بیاور، بعد کارت را برگردان</h2><p>انتخاب «بلد بودم» یا «نیاز به مرور» در اپ به برنامهٔ مرور موجود فرستاده می‌شود؛ این انتخاب خودارزیابی است.</p></section><section class="flash-deck"><div class="deck-status"><strong id="flash-position"></strong><span id="flash-reviewed"></span></div><div id="flash-list"></div><div class="controls deck-controls"><button id="flash-prev" type="button">کارت قبلی</button><button id="flash-next" type="button">کارت بعدی</button></div></section>','flash',cards=cards)
    page('TAB04.html','نمونه‌سؤالات جامع فصل اول',exam_body('بانک سؤال با هدف‌های آموزشی مستقل'),'exam',canonical,mode='sample')
    slugs=['easy','medium','hard','brilliant'];exams=[]
    for level,(slug,label) in enumerate(zip(slugs,LEVELS),1):
        links=[]
        for v in range(1,7):
            sys.path.insert(0,str(HERE.parent/'math-book'))
            from exam_cases import assessment_cases
            qs=assessment_cases(1,[q for q in questions(v) if q['level']==level],v)
            for i,q in enumerate(qs,1):
                q['id']=f'f01-{slug}-v{v}-q{i:02d}'
                q['sources']=['gharavi'] if level<3 else []
                q['origin']='نسخهٔ عددی تألیفی از خانوادهٔ '+q['family']
            filename=f'TAB05-{slug}-{v:02d}.html'
            page(filename,f'خودآزمایی {label} — نسخهٔ {v}',exam_body('سطح '+label+' · نسخهٔ '+str(v),assessment=True),'exam',qs,variant=v,mode='assessment')
            exams.append(dict(level=label,version=v,filename=filename,questions=qs))
            links.append('<a href="'+filename+'">آزمون '+str(v)+'</a>')
        links_html=''.join(links)
        notes=['تعریف، نماد و یک محاسبهٔ مستقیم','نمایش مجموعه، شمارش و احتمال مرکب','ترکیب چند رابطه و حل مسئلهٔ معکوس','تمرین تکمیلیِ شمارش و استدلال؛ فراتر از سطح معمول امتحان'][level-1]
        exams[-1]['levelMenu']='<section class="level-card"><h2>'+label+'</h2><p>'+notes+'</p><div class="exam-links">'+links_html+'</div></section>'
    index='<section class="intro"><span class="badge">۲۴ خودآزمایی مستقل</span><h2>سطح را انتخاب کن و پیش برو</h2><p>چهار سطح، هرکدام شش فایل مستقل؛ هر فایل بدون اینترنت اجرا و تصحیح می‌شود. سؤال‌های یک سطح هدف‌های مشترکی دارند و نسخه‌ها برای تمرین با مقدارهای متفاوت طراحی شده‌اند.</p></section><div class="level-grid">'+''.join(e.get('levelMenu','') for e in exams)+'</div>'
    page('TAB05.html','خودآزمایی فصل اول؛ انتخاب سطح و آزمون',index,'exam',mode='assessment-index')
    manifest=dict(schemaVersion=1,bookCode='C905',chapter=1,sourceMenu=str(menu_path),routes=routes)
    manifest_path=args.app/'grades/g09/src/main/assets/content/math-practice-routes.json'
    if manifest_path.exists():
        previous=json.loads(manifest_path.read_text())
        others=[r for r in previous.get('routes',[]) if '/N2.5/' not in r['bucketKey']]
        if others:manifest['routes']+=others;manifest.pop('chapter',None)
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    reports=REPO/'reports/math-f01';reports.mkdir(parents=True,exist_ok=True)
    report.update(dict(contentVersion=version,sharedContentRules='CONTENT_RULES.md',displayFont='Vazir 30.1.0 Farsi-Digits',assessmentGrading='only after explicit finish',learnerSources='omitted from learner HTML; provenance in separate report',grade=9,book='ریاضی نهم',chapter='فصل اول: مجموعه‌ها',appSourceCommit='c09746a5210c7fc9ea4e55fc48a97127b2f5a8d9',
        template='teaching - template/lesson-template.preview-standalone.html',reviewedSources=len(SOURCES),years=[1401,1402,1403,1404],
        finalBankCount=len(canonical),difficulty=dict(Counter(q['difficulty'] for q in canonical)),types=dict(Counter(q['type'] for q in canonical)),
        flashcards=len(cards),assessmentFiles=len(exams),assessmentItems=sum(len(x['questions']) for x in exams),generatedFiles=generated,
        answerChecks=392,notes=['آزمون‌های درخشان تمرین تکمیلی‌اند.','پوشش واقعی سال ۱۴۰۵ احراز نشد؛ جست‌وجو انجام شد.','اجرای اندروید روی دستگاه واقعی جدا از آزمایش Chromium گزارش می‌شود.']))
    (reports/'research-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (reports/'canonical-bank.json').write_text(json.dumps(canonical,ensure_ascii=False,indent=2)+'\n')
    (reports/'assessments.json').write_text(json.dumps(exams,ensure_ascii=False,indent=2)+'\n')
    (reports/'routes.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['rawCount','duplicateCount','rejectedCount','retainedSourcePatterns','finalBankCount','difficulty','types','flashcards','assessmentFiles','assessmentItems']},ensure_ascii=False))

if __name__=='__main__':main()
