این متن را برای بررسی اتصال فایل‌های جدید در چت **Hamyar|App Development** وارد کنید. دستور انتشار APK یا آپلود باکت واقعی نیست.

```text
مرجع نتیجهٔ exam-content-builder:
https://github.com/samanta-nz/Books-Data/tree/main/codex-reports/Exam-Content-Builder
بستهٔ مشخص این کار:
https://github.com/samanta-nz/Books-Data/tree/main/codex-reports/Exam-Content-Builder/2026-10-23/001-MATH9-BUCKET-LAYOUT
این دو لینک در دستورهای ادامه حفظ شوند.

فایل‌های ریاضی نهم با نام‌گذاری ZIP bucket-sync-g09-39.09.03.zip در ریپوی اصلی اپ قرار گرفته‌اند:
https://github.com/samanta-nz/com.hamyareman.final
شاخه: migration/modular-grades
کامیت دقیق: 642662f9b1d0601b2c23c79391647b6815098e5c
پوشهٔ فایل‌ها: https://github.com/samanta-nz/com.hamyareman.final/tree/migration/modular-grades/grades/g09/Bucket/Content/G09/g9-math
manifest نگاشت و hashها:
https://github.com/samanta-nz/com.hamyareman.final/blob/642662f9b1d0601b2c23c79391647b6815098e5c/grades/g09/Bucket/math9-layout-manifest.json
SHA-256: 280cedeb5eac33662f6acf5b647357e059d4611bc8306260f1014c78536dd0f8

این تحویل ۲۵۲ HTML و ۲۵۲ Theme واقعی، ۲۱۶ آزمون مستقل، هشت فصل و ALL دارد. نمونه مسیرها:
Bucket/Content/G09/g9-math/F01/ryazif01-cards.html
Bucket/Content/G09/g9-math/F01/ryazif01-Hits.html
Bucket/Content/G09/g9-math/F01/ryazif01-Q.html
Bucket/Content/G09/g9-math/F01/ryazif01-selftest.html
Bucket/Content/G09/g9-math/F01/selftest/ryazif01-selftest-easy-01.html
Bucket/Content/G09/g9-math/ALL/ryazi-all-selftest.html
Bucket/Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-brilliant-06.html
فقط پیشوند grades/g09/ از repositoryPath حذف می‌شود تا bucketKey حاصل شود؛ حروف بزرگ/کوچک دقیق حفظ شوند. فایل‌ها را دوباره تولید یا در منو تکرار نکن. فایل‌های تدریس و PDF و EX مجزای خارج از این بانک را آماده اعلام نکن.

محتوای practice-data، سؤال/پاسخ، scriptها، document/pack/question IDs و contentVersion ثابت‌اند. همهٔ ۲۱۶ لینک فهرست اصلاح شده‌اند. ۳۶ مسیر اصلی در grade-server-map فعلی موجودند؛ برگه‌های مستقل entry صریح ندارند و از لینک نسبی باز می‌شوند. برای HmkWebViewClient/کش/آفلاین، ادامهٔ آزمون پس از reload و جلوگیری از نتیجهٔ زودرس، همین مسیرهای واقعی را بررسی کن؛ اگر به route صریح نیاز است، اصلاح محدود و مستند انجام بده.

کد فعلی RemoteHtmlPage در BookNodeScreen.kt، HamyarHtmlBridge را با hamyar_remote_html و kind=document و packId حاصل از LessonCache.keyOf(url) متصل می‌کند. bridge فعلی کلید html:g09:<kind>:<packId> می‌سازد. این با مسیر قدیمی hamyar_math_html و C905_E..-SUM یکی نیست. ثبت پاسخ و خطا، حفظ نتیجه/تاریخچه و اتصال به progress و exam ledger را با همین منوی remote بررسی کن؛ دربارهٔ انتقال دادهٔ قبلی بدون شاهد ادعای موفقیت نکن. پشتیبانی هویت آموزشی صفحه و تغییر حساب در میان navigation نیز بررسی شود؛ API/backend تازه یا حذف دادهٔ قبلی نساز.

شواهد مؤلف در گزارش: همهٔ ۲۵۲ مسیر جدید در Chromium، نه بانک و نه فهرست، هشت آزمون فصل و تمام ۲۴ برگهٔ جامع با تصحیح/خودارزیابی و ذخیره با bridge ساختگی موفق‌اند. این اجرای واقعی اپ نیست. گوشی، شبیه‌ساز و QA مستقل مسیرهای جدید NOT_RUN هستند. نتیجهٔ بررسی/اصلاح را با commit دقیق، تست واقعی و گزارش قابل دریافت در پوشهٔ نقش خودت به exam-content-builder برگردان تا QA هم‌نسخه درخواست شود.

این دستور مجوز bucket sync زنده، فعال‌سازی remoteMenu، merge سورس main یا انتشار APK نیست. آپلود object storage و رمزگذاری/کلید در این مرحله انجام نشده است. ارسال خودکار بین چت‌ها نیز انجام نشده؛ لینک خروجی و محدودیت‌های واقعی را صریح ثبت کن.
```
