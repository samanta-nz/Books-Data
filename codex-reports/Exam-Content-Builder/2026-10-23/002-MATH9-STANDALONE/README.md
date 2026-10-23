# ریاضی نهم — HTML مستقل، راهنمای اپ و ZIP

تاریخ **۲۰۲۶-۱۰-۲۳، Asia/Tehran**؛ بستهٔ **۰۰۲**؛ ارجاع `MATH9-STANDALONE-20261023`.

**درخواست اجرا شد:** ۲۵۲ فایل CSS جانبی ریاضی حذف شدند؛ تم، فونت‌ها و اسکریپت‌های لازم داخل هر ۲۵۲ HTML هستند. پنجرهٔ منوی شناور فضای کامل محتوای WebView را می‌گیرد. راهنمای کامل ثبت نتایج و متن واقعی تمام اسکریپت‌ها کنار فایل‌ها قرار دارد؛ ZIP مستقل نیز ساخته و با فایل‌های ریپو تطبیق داده شد.

[دانلود ZIP](G9-Math.zip) · [راهنمای کامل اتصال و ثبت نتایج اپ](G9-Math-APP-INTEGRATION.md) · [manifest فایل‌ها](math9-layout-manifest.json) · [رسید ZIP](G9-Math-package-receipt.json)

- ریپوی اصلی: https://github.com/samanta-nz/com.hamyareman.final ؛ شاخهٔ `migration/modular-grades`.
- کامیت تحویل: [`cc60738f504c0890e90c52460203a6d0d70bfd07`](https://github.com/samanta-nz/com.hamyareman.final/commit/cc60738f504c0890e90c52460203a6d0d70bfd07).
- [فایل‌ها در پوشهٔ باکت اپ](https://github.com/samanta-nz/com.hamyareman.final/tree/migration/modular-grades/grades/g09/Bucket/Content/G09/g9-math).
- [راهنمای کنار فایل‌های اپ](https://github.com/samanta-nz/com.hamyareman.final/blob/cc60738f504c0890e90c52460203a6d0d70bfd07/grades/g09/Bucket/G9-Math-APP-INTEGRATION.md).
- [گزارش قبلی مسیرها](../001-MATH9-BUCKET-LAYOUT/README.md) و [پوشهٔ دائمی گزارش‌های این نقش](https://github.com/samanta-nz/Books-Data/tree/main/codex-reports/Exam-Content-Builder).

## محتویات ZIP

ZIP حدود **۶۶٫۹ مگابایت** است؛ با ساختار `Bucket/Content/G09/g9-math/` باز می‌شود. **۲۵۶ فایل** دارد: ۲۵۲ HTML، یک راهنمای کامل اپ، README، manifest و SHA256SUMS. CSS/JS جانبی یا فایل کتاب‌های دیگر داخل ZIP نیست. هشت فصل، ALL و تمام ۲۱۶ آزمون مستقل حفظ شده‌اند.

SHA-256 ZIP: `34fe59d3204b0ecdafc27dba713bb32f228f5d5db2929437244a87fa7e93f72b`؛ اندازهٔ دقیق `66868738` بایت. آزمون CRC و مقایسهٔ بایت تمام ورودی‌های ZIP با فایل‌های ریپو موفق است؛ archive خودش را درون خود تکرار نمی‌کند. لینک دانلود README هم با بازکردن ZIP معتبر می‌ماند. [فهرست hash فایل‌های داخل بسته](G9-Math-FILES.sha256).

## تغییر و کنترل کیفیت

دادهٔ علمی، پاسخ‌ها، document/pack/question IDها، contentVersion و موتورهای تصحیح/ثبت قبلی ثابت‌اند. تم تعبیه‌شده با CSS قبلی بایت‌به‌بایت تطبیق شد و سپس فایل جدا حذف شد. بلوک‌های locked قالب و فایل‌های مرجع آن دست‌نخورده‌اند؛ override فلوتر در بلوک جدا و امبد است.

فلوتر از کادر ۳۲۰ پیکسلی محدود به یک پنجره در تمام viewport تبدیل شد؛ safe-area، اسکرول داخلی، تلهٔ Tab، بازگرداندن فوکوس، Escape، دکمهٔ بستن و inert شدن header/main/footer پشت آن اضافه شدند. در منبع فعلی اپ، AndroidView میزبان RemoteHtmlPage نیز `Modifier.fillMaxSize()` دارد. این تغییر CSS اندازهٔ parent/native toolbar را دست‌کاری نمی‌کند و اجرای واقعی دستگاه ادعا نشده است.

[تست مرورگر](browser-verification.json) و [log](browser-verification.log): همهٔ **۲۵۲ صفحه** در عرض ۳۲۰ و پنجرهٔ تمام‌اندازه بررسی شدند؛ مجموع **۲۹۶ بررسی باز/بستن پنجره** شامل حالت‌های landscape/desktop و آزمون‌های پاسخ موفق بود. فونت وزیر سه وزن، ارقام فارسی و عدم سرریز حفظ شد. نه بانک با پاسخ غلط، هشت آزمون فصل با پیش‌نویس/نتیجه، تمام بیست‌وچهار برگهٔ جامع با بیست نمره و خودارزیابی، نه فهرست و نه مجموعهٔ تک‌کارت آزموده شدند؛ صفر خطای JavaScript و صفر درخواست بیرونی. [تصویر پنجرهٔ تمام‌اندازه](fullscreen-floater.png).

آزمون اولیه نشان داد main داخل wrapper قالب است؛ selector مربوط به inert پس‌زمینه با ساختار واقعی اصلاح شد و کل مجموعه دوباره موفق گذشت. [log اولیه](browser-verification.initial.log) جدا نگه داشته شده است.

## راهنمای ثبت نتایج و موارد native

راهنمای کامل، امضاهای واقعی چهار متد Hamyar، ترتیب نصب bridge پیش از اجرای HTML، schema و تمام فیلدهای خطا/نتیجه/تاریخچه، جدول هویت ۲۵۲ فایل و متن کامل شش اسکریپت واقعی را در **یک فایل** دارد. هیچ اسکریپت جداگانه برای اجرای بسته لازم نیست؛ نباید موتور را دوباره تزریق کرد.

این راهنما تفاوت store آموزشی `hamyar_math_html` و store مسیر remote یعنی `hamyar_remote_html`، kind=document و packId مشتق از URL، و کلید namespaced `html:g09:...` در اپ فعلی را مشخص می‌کند؛ اتصال و مهاجرت نتیجهٔ قبلی باید توسط توسعه/QA روی اپ بررسی شود. این تحویل Kotlin، منو، backend یا API تازه‌ای تغییر نداده است. راهنمای Back سخت‌افزاری برای hook موجود توضیح داده شده؛ بستن با دکمه/Escape/فهرست داخل خود HTML فعال است.

bridge تست Chromium ساختگی با امضاهای واقعی بود. **گوشی، اپ نصب‌شده و QA مستقل این نسخه NOT_RUN هستند**؛ ثبت نهایی در اپ یا انتقال دادهٔ حساب از موفقیت مرورگر نتیجه‌گیری نشده است. APK و upload باکت واقعی انجام نشده‌اند؛ انتشار این بسته در گیت‌هاب است.

[نتیجهٔ ماشین‌خوان](RESULT.json) · [manifest اندازه و hash گزارش](PACKAGE_MANIFEST.json).
