# قواعد تولید محتوای همیار من

پیش از تولید یا تغییر HTML آموزشی، مرور، فلش‌کارت و آزمون، `CONTENT_RULES.md` و `teaching - template/README.md` را بخوان و فایل‌های واقعی قالب را بررسی کن. مرجع ظاهر، هدر، فوتر و ابزارها `teaching - template/lesson-template.preview-standalone.html` و نمونهٔ کامل موجود است.

فایل‌های `teaching - template/assets/css/locked/`، `teaching - template/assets/js/locked/` و `teaching - template/assets/LOCKED.sha256` را تغییر نده و `--update` اجرا نکن. قبل و بعد از تولید، verifier واقعی همان پوشه باید موفق باشد. Theme جداگانه و مسیر واقعی هر HTML ساخته‌شده را در جدول راهنما ثبت کن. مسیر و نام TABهای اپ را از منوی واقعی بگیر.

قواعد کاربر دربارهٔ نبود تب بالای HTML و منابع، ارقام فارسی، فونت واقعی وزیر، تم ثابت، بازخورد اختصاصی نمونه‌سؤال و پنهان ماندن نتیجهٔ خودآزمایی تا پایان رعایت شوند. از ذخیره‌سازی و interface واقعی اپ استفاده کن؛ API فرضی نساز. بدون دستور تازهٔ کاربر commit، push، upload، bucket sync یا release انجام نده.

## محل انتشار نتایج این نقش

طبق دستور مستقیم کاربر در ۲۰۲۶-۱۰-۱۹، نتایج `exam-content-builder` در `codex-reports/Exam-Content-Builder/YYYY-MM-DD/NNN-REFERENCE/` روی main ثبت شوند. مرجع دستور و فهرست: https://github.com/samanta-nz/Books-Data/tree/main/codex-reports/Exam-Content-Builder . پیش از انتشار، README آن مسیر را بخوان؛ تاریخ واقعی، شمارهٔ جدید، ارجاع درخواست/نسخه، manifest فایل‌ها و لینک پوشه در پرامپت ادامه لازم است. بستهٔ منتشرشده بازنویسی نشود. انتشار گزارش فقط در این مسیر به معنی مجوز merge سورس، sync باکت یا release نیست.
