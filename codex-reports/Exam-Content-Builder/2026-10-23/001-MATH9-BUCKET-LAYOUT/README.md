# ریاضی نهم — نام‌گذاری و پوشه‌بندی جدید باکت

تاریخ ثبت: **۲۰۲۶-۱۰-۲۳، Asia/Tehran**؛ شمارهٔ **۰۰۱**؛ ارجاع `MATH9-BUCKET-LAYOUT-20261023`.

**درخواست انجام شد:** فایل‌های قبلاً ساخته‌شده، مطابق نام‌گذاری ZIP مرجع در پوشهٔ مشترک باکت گیت‌هاب قرار گرفتند و روی شاخهٔ درخواستی push شدند. این گزارش، آپلود object storage یا تأیید رفتار اپ نصب‌شده را اعلام نمی‌کند.

- [پوشهٔ دائمی گزارش‌ها](https://github.com/samanta-nz/Books-Data/tree/main/codex-reports/Exam-Content-Builder) · [بستهٔ همین نتیجه](https://github.com/samanta-nz/Books-Data/tree/main/codex-reports/Exam-Content-Builder/2026-10-23/001-MATH9-BUCKET-LAYOUT).
- [فایل‌های ریاضی در مسیر درخواستی](https://github.com/samanta-nz/com.hamyareman.final/tree/migration/modular-grades/grades/g09/Bucket/Content/G09/g9-math).
- [کامیت واقعی](https://github.com/samanta-nz/com.hamyareman.final/commit/642662f9b1d0601b2c23c79391647b6815098e5c): `642662f9b1d0601b2c23c79391647b6815098e5c`؛ شاخه `migration/modular-grades`.
- ZIP مرجع: [bucket-sync-g09-39.09.03.zip](https://github.com/samanta-nz/com.hamyareman.final/blob/e8186d8060de309102888ccef7f14c7bcf0c383c/grades/g09/bucket-sync-g09-39.09.03.zip).
- محتوای اصلی: [Books-Data](https://github.com/samanta-nz/Books-Data/tree/2a19ac65bbc79f4ce21647c9bf463c6662f82b5b)، کامیت `2a19ac65bbc79f4ce21647c9bf463c6662f82b5b`.

## ساختار و تعداد

| مورد | مقدار |
|---|---|
| محدوده | هشت فصل `F01..F08` و مرور جامع `ALL` |
| HTML | ۲۵۲ |
| Theme واقعی هم‌نام | ۲۵۲ |
| آزمون مستقل | ۲۱۶؛ هر محدوده چهار سطح و هر سطح شش نسخه |
| لینک‌های انتخاب آزمون اصلاح‌شده | ۲۱۶ |
| فایل‌های اضافه‌شده در commit | ۵۰۶؛ شامل ۵۰۴ دارایی و دو فایل راهنما/manifest |

ریشهٔ ریپو `grades/g09/Bucket/Content/G09/g9-math/` و کلید متناظر باکت `Bucket/Content/G09/g9-math/` است؛ فقط پیشوند `grades/g09/` حذف می‌شود. `Bucket` با همین حروف نوشته شده و با `BUCKET` یا `Bucket/Bucket` جایگزین نشده است.

در هر فصل فایل‌های `ryazif01-cards.html`، `ryazif01-Hits.html`، `ryazif01-Q.html` و `ryazif01-selftest.html` مطابق جدول صریح ZIP نام‌گذاری شدند؛ فصل‌های بعد با شمارهٔ خودشان‌اند. در کل کتاب `ryazi-all-cards.html`، `ryazi-all-Hits.html`، `ryazi-all-Q.html` و `ryazi-all-selftest.html` قرار دارند.

نسخه‌های مستقل در زیرپوشهٔ `selftest/`، مثل `F01/selftest/ryazif01-selftest-easy-01.html` و `ALL/selftest/ryazi-all-selftest-brilliant-06.html` هستند. این امتداد نام‌گذاری برای حفظ ۲۴ فایل مستقل سفارش قبلی لازم است؛ ZIP فقط نام فایل ورودی خودآزمایی را مشخص می‌کند. همهٔ لینک‌های فهرست به همین مسیرها اصلاح شده‌اند. برای هر فایل، Theme در `assets/css/theme/<same-name>.theme.css` همان دایرکتوری قرار دارد.

[جدول کامل نگاشت، شناسه‌ها، اندازه و SHA-256](math9-layout-manifest.json)؛ SHA-256 این manifest: `280cedeb5eac33662f6acf5b647357e059d4611bc8306260f1014c78536dd0f8`. راهنمای داخل ریپوی مقصد [G9-Math-README.md](https://github.com/samanta-nz/com.hamyareman.final/blob/642662f9b1d0601b2c23c79391647b6815098e5c/grades/g09/Bucket/G9-Math-README.md) است.

این تحویل فقط فایل‌های موجود مرور و آزمون را پوشش می‌دهد. فایل تدریس، PDF، صوت یا EX مجزایی که در بستهٔ قبلی تولید نشده بود، با جای‌نگهدار یا کپی تکراری ساخته نشد؛ ۱۴۶ مقصد دیگرِ طرح کلی کتاب در manifest به‌عنوان خارج از این تحویل فهرست شده‌اند. شمار سؤال‌های مرجع همان ۴۱۱ و کارت‌های مرجع همان ۱۹۰ باقی است.

## کنترل کیفیت واقعی

- بایت‌های Theme، تمام بلوک‌های script و JSON سؤال‌ها در هر ۲۵۲ صفحه ثابت‌اند؛ شناسهٔ سؤال، document، pack و contentVersion تغییر نکرده است. تنها نام ارجاع Theme و لینک‌های انتخاب آزمون اصلاح شدند؛ قفل‌های قالب سالم‌اند.
- ۵۰۴ hash فایل، با نسخهٔ commit نهایی تطبیق و وجود ref دوردست تأیید شد؛ native source، منو و نسخهٔ انتشار تغییر نکرده‌اند. تغییرات هم‌زمان انگلیسی با rebase حفظ شد و هیچ مسیر انگلیسی در diff این تحویل نیست.
- [گزارش مرورگر](browser-verification.json) و [log واقعی](browser-verification.log): هر ۲۵۲ مسیر در عرض ۳۲۰، ارقام فارسی و وزن‌های وزیر، header/footer و RTL بررسی شدند؛ بدون خطای JavaScript یا درخواست بیرونی. هر نه فهرست خودآزمایی باز و لینک آزمون آن کلیک شد؛ تمام ۲۱۶ لینک نیز از نظر وجود مقصد بررسی شدند.
- بازخورد غلط و metadata خطا در هر نه بانک، ثبت نتیجه و پیش‌نویس در یک آزمون هر هشت فصل، تمام ۲۴ برگهٔ جامع با بارم بیست و خودارزیابی تشریحی، نه مجموعه فلش‌کارت تک‌کارت و شش حالت صفحه در برابر تغییر Theme سیستم بررسی شدند. [تصویر فهرست کل کتاب](renamed-whole-book-menu.png).
- bridge در Chromium ساختگی با امضاهای موجود بود؛ گوشی، شبیه‌ساز، اپ نصب‌شده و QA مستقل مسیرهای تازه `NOT_RUN` هستند. تست‌های علمی/هستهٔ قبلی دوباره اجرا نشده‌اند؛ داده/کد علمی تغییر نکرده است.

## هماهنگی بعدی با اپ

۳۶ مسیر اصلی با `grade-server-map.json` همین شاخه تطبیق دارند؛ ۲۱۶ برگهٔ مستقل در map فعلی entry جدا ندارند و از لینک نسبی فهرست وارد می‌شوند. مصرف‌کنندهٔ HmkWebViewClient، کش و بازکردن همین لینک‌ها باید روی اپ بررسی شود.

در سورس همین شاخه، `RemoteHtmlPage` از store=`hamyar_remote_html` و kind=`document` با packId حاصل از `LessonCache.keyOf(url)` استفاده می‌کند؛ `HamyarHtmlBridge` کلید namespaced=`html:g09:<kind>:<packId>` دارد. این مسیر با اجرای قدیمی `hamyar_math_html` و pack آموزشی یکی نیست. بنابراین حفظ شناسه‌های HTML به‌تنهایی تأیید مهاجرت نتیجه/پیشرفت قدیمی به مسیر remote نیست؛ این موضوع باید توسط توسعه/QA روی اپ بررسی و هر اصلاح native در نقش صاحب آن انجام شود.

[پرامپت هماهنگی با توسعهٔ اپ](APP_INTEGRATION_PROMPT.md) شامل مسیرها، commit، hash و موارد دقیق بررسی است. این پرامپت آماده است و خودکار به چت دیگری ارسال نشده است.

این درخواست، انتشار APK یا فعال‌سازی پارس‌پک نبوده است؛ انتقال واقعی به object storage، رمزگذاری جدید/دریافت کلید، تغییر remoteMenu و release انجام نشده‌اند. دستورهای وسیع‌تر داخل ZIP صرفاً منبع قرارداد نام‌گذاری بررسی شدند و به‌عنوان سفارش تغییر تمام کتاب‌ها، تولید صوت یا انتشار اجرا نشدند.

[نتیجهٔ ماشین‌خوان](RESULT.json) · [فهرست اندازه و hash فایل‌های گزارش](PACKAGE_MANIFEST.json).
