"""Provenance records actual inspected content; failed pages are never counted."""
SOURCES = [
 dict(id='faradars',title='فرادرس؛ راهنمای تدریس فصل اول',url='https://blog.faradars.org/تدریس-فصل-اول-ریاضی-نهم-راهنمای-کامل/',years=[],regions=[],role='تطبیق سرفصل',review='متن واقعی صفحه بررسی شد؛ سال آزمون ندارد.'),
 dict(id='openstax',title='OpenStax؛ Basic Set Concepts',url='https://openstax.org/books/contemporary-mathematics/pages/1-1-basic-set-concepts',years=[],regions=[],role='مرجع مفهومی',review='تعریف مجموعه، عضویت، تهی، تعداد اعضا و برابری بررسی شد.'),
 dict(id='gharavi',title='گردآوری مهدی غروی؛ فصل اول، خرداد ۱۴۰۲ و ۱۴۰۳',url='https://www.scribd.com/document/890121118/1-14018305993',years=[1402,1403],regions=['سمنان','کرمانشاه','خراسان رضوی','خوزستان','آذربایجان شرقی','گیلان','یزد','همدان','خراسان جنوبی','کردستان','البرز','گلستان','هرمزگان','آذربایجان غربی','بوشهر','فارس','لرستان','مرکزی','تهران','ایلام','اصفهان','چهارمحال و بختیاری','قزوین','کرمان','سیستان و بلوچستان','زنجان','کهگیلویه و بویراحمد','کشوری'],role='سبک امتحانی و پالایش الگوها',review='متن سؤال‌های فصل مشاهده شد. انتساب استان‌ها از گردآوری ثانویه است؛ اصل همهٔ برگه‌های استانی جداگانه احراز نشده است. موارد دارای OCR خراب حذف شدند.'),
 dict(id='mamoallemim',title='ما معلمیم؛ نمونه سؤال فصل اول با پاسخنامه، ۸ صفحه',url='https://www.mamoallemim.com/wp-content/uploads/2024/10/نمونه-سوال-فصل-اول-ریاضی-نهم-با-پاسخنامه.pdf',years=[1403],regions=[],role='تنوع نوع سؤال',review='متن سؤال و پاسخنامهٔ PDF بررسی شد؛ ۱۴۰۳ سال انتشار است، نه انتساب به امتحان رسمی. پاسخ تبدیل {3x|x∈W,-3<x<5} در منبع با قید روی x سازگار نیست و استفاده نشد.'),
 dict(id='bekhun',title='بخون؛ مجموعه‌ها، نمونه سؤال و پاسخ',url='https://bekhun.com/exam-season1-math9/',years=[1403],regions=[],role='شناسایی ابهام و خطای پاسخنامه',review='متن واقعی و پاسخنامه بررسی شد. پاسخ تهیِ دارای یک عضو و پاسخ عدد نه مثبت نه منفی غلط‌اند؛ پاسخ‌های منبع مرجع قطعی نیستند.'),
 dict(id='school1401',title='مدرسهٔ محدثه ۱، ناحیهٔ ۳ تبریز؛ ۱۴۰۱/۱۰/۱۹، دبیر شهنازی',url='https://www.scribd.com/document/967002702/ریاضی-نهم-1401-شهنازی-محدثه-1',years=[1401],regions=['آذربایجان شرقی'],role='آزمون مدرسه',review='سربرگ و سؤال‌های متنی مرتبط با فصل اول بررسی شد؛ سؤال‌های صرفاً تصویری و سایر فصل‌ها وارد استخراج نشدند.'),
 dict(id='national1404',title='هماهنگ کشوری ریاضی نهم؛ ۱۴۰۴/۰۳/۰۴، نسخهٔ صبح',url='https://dl.heyvagroup.com/admin/Files/upload/159824234سوالات%20امتحان%20نهایی%20ریاضی%20پایه%20نهم%20کشوری%20خرداد%20۱۴۰۴.pdf',years=[1404],regions=['کشوری'],role='آزمون رسمی بازنشرشده',review='PDF چهارضفحه‌ای با سربرگ مرکز ارزشیابی بررسی شد؛ سؤال ۲الف و بخش متنی ۴ج استخراج شد. سؤال‌های تصویری دارای OCR ناقص وارد بانک نشدند.'),
]
ATTEMPTS = [
 dict(url='https://gama.ir/test/detail/4151/نمونه-سوالات-طبقه-بندی-شده-فصل-اول-ریاضی-نهم-مجموعه-ها',status='صفحهٔ مورد اشارهٔ قالب در ابزار وب قابل دسترسی نبود؛ کد تصحیحی از آن کپی نشده است.'),
 dict(url='https://gama.ir/azmoon',status='به papers هدایت شد؛ متن آزمون آنلاین و اسکریپت تصحیح در دسترس قرار نگرفت.'),
 dict(url='https://blog.faradars.org/نمونه-سوال-ریاضی-نهم-فصل-اول/',status='نشانی نمونه سؤال قالب و نسخهٔ amp قابل دسترسی نبود.'),
 dict(url='https://blog.filimo.school/nemoone/nemoone-math/nemoone-math-9th/s1-5/',status='صفحه و PDF باز شدند، اما PDF متن استخراج‌پذیر نداشت؛ در آمار سؤال استخراج‌شده شمرده نشد.'),
 dict(url='https://asgharbojari19.blogfa.com/',status='آرشیو ۱۴۰۰ بررسی شد؛ لینک PDF مربوط به فصل اول باز نشد و در پوشش محتوایی آن سال شمرده نشد.'),
 dict(url='https://www.kanoon.ir/Downloads/ExamQuestion/41793',status='نسخهٔ ۱۴۰۱ البرز باز نشد.'),
 dict(url='https://www.kanoon.ir/Downloads/ExamQuestion/29663',status='PDF منتسب به ۱۴۰۰ بدون متن قابل بررسی و با خطای تصویر؛ سؤال استخراج نشد.'),
 dict(url='https://www.heyvagroup.com/shownews/12700/سوالات-امتحان-نهایی-ریاضی-پایه-نهم-کشوری-خرداد-۱۴۰۴.html',status='صفحهٔ واسط برای یافتن PDF رسمی؛ جدا از PDF به‌عنوان مجموعه سؤال شمرده نشد.'),
]

# Source numbers, not copied prose. Each row is a reviewed raw candidate.
# Equal family means the same teaching objective and solving method.
RAW_MAP = {
 'gharavi':[(1,'nested-empty'),(2,'cardinality'),(3,'empty-singleton'),(4,'self-subset'),(5,'empty-subset'),(6,'empty-singleton'),(7,'defined'),(8,'defined'),(9,'defined'),(10,'empty-singleton'),(11,'empty-singleton'),(12,'defined'),(14,'empty-singleton'),(15,'subsets'),(16,'defined'),(17,'defined'),(18,'cardinality'),(20,'empty-subset'),(21,'subsets'),(23,'subsets-divisors'),(24,'subsets'),(25,'empty-subset'),(26,'subsets'),(28,'subsets'),(30,'subset'),(31,'equal-parameter'),(32,'equal-parameter'),(34,'equal-parameter'),(35,'subset-minimum'),(36,'list-subsets'),(37,'list-subsets'),(38,'builder'),(39,'linear-image'),(40,'linear-image'),(41,'linear-image'),(42,'builder'),(43,'linear-image'),(44,'linear-image'),(45,'builder'),(46,'set-identity'),(47,'union-count'),(50,'subset-difference'),(52,'disjoint-example'),(53,'set-operations'),(54,'nested-operations'),(56,'nested-operations'),(59,'builder-operations'),(60,'set-operations'),(61,'set-operations'),(62,'set-operations'),(64,'set-operations'),(65,'set-operations'),(68,'nested-operations'),(69,'union-count'),(84,'sample-count'),(85,'single-die'),(86,'single-die'),(87,'coins-exact'),(88,'die-prime'),(89,'single-die'),(91,'dice-sum'),(92,'dice-threshold'),(93,'coins-exact'),(94,'coins-exact'),(95,'dice-sum'),(96,'die-prime'),(97,'die-prime'),(98,'dice-both'),(99,'cards-threshold'),(100,'cards-and'),(101,'cards-complement'),(112,'cards-property')],
 'mamoallemim':[('1a','empty-singleton'),('1b','subset-transitive'),('1c','subset-disjoint-counterexample'),('1d','set-identity'),('2a','cardinality'),('2b','builder'),('2d','subsets'),('3','set-operations'),('4a','builder'),('4b','square-image'),('5-1','defined'),('5-2','builder'),('5-3','set-operations'),('5-4','single-die'),('8a','coins-atleast'),('8b','coins-exact'),('8c','impossible-event'),('9a','dice-sum'),('9b','dice-both'),('9c','dice-modulo'),('10b','cards-property'),('10c','cards-and')],
 'school1401':[('1a','self-subset'),('1c','set-identity'),('2a','subsets'),('3-1','defined'),('3-2','single-die'),('5','equal-parameter'),('6a','builder'),('6b','builder'),('8','dice-both')],
 'national1404':[('2a','cardinality'),('4c','builder')],
}
EXCLUDED = [
 dict(source='gharavi',locator='13',reason='ابهام در تعیین سه عدد اول کمتر از ده؛ چهار عدد اول در این بازه وجود دارد.'),
 dict(source='gharavi',locator='29',reason='متن OCR گزینه‌ها چند گزارهٔ درست را القا می‌کند؛ اصل تصویر احراز نشد.'),
 dict(source='mamoallemim',locator='4c',reason='اختلاف قید روی x با پاسخنامه؛ از بازنویسی مبهم صرف‌نظر شد.'),
 dict(source='bekhun',locator='بخش معرفی، پاسخ ۱پ',reason='کلید پاسخ، تهی را دارای یک عضو اعلام کرده؛ مردود.'),
 dict(source='bekhun',locator='بخش معرفی، پاسخ ۲الف',reason='عدد نه مثبت نه منفی صفر است؛ پاسخ تهی در منبع مردود.'),
]

def audit():
    rows=[]; representatives={}
    for source,items in RAW_MAP.items():
        for locator,family in items:
            uid=f'{source}:{locator}'
            duplicate=representatives.get(family)
            row=dict(id=uid,sourceId=source,locator=str(locator),semanticFamily=family,
                     decision='duplicate' if duplicate else 'retain-pattern',duplicateOf=duplicate)
            rows.append(row);representatives.setdefault(family,uid)
    return dict(sources=SOURCES,attempts=ATTEMPTS,candidates=rows,excluded=EXCLUDED,
        rawCount=len(rows)+len(EXCLUDED),duplicateCount=sum(x['decision']=='duplicate' for x in rows),
        rejectedCount=len(EXCLUDED),retainedSourcePatterns=len(representatives),
        note='منبع فقط برای اهداف و سبک به‌کار رفته؛ سؤال‌های HTML تألیفی‌اند. تعداد الگوهای منبع با تعداد هدف‌های تألیفی بانک یکی نیست. نسخه‌های عددی خودآزمایی به‌عنوان سؤال یکتای بانک شمرده نمی‌شوند.')
