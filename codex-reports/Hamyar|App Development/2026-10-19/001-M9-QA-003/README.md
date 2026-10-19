# CODE_DELIVERY — M9-QA-003

اصلاح محدود جداسازی اطلاعات حساب قبلی از مهمان در کد واقعی اپ انجام شد. owner خالی اکنون از `<storeName>__guest` استفاده می‌کند؛ مهمان دادهٔ legacy حساب A را نمی‌خواند یا ویرایش نمی‌کند. مهاجرت معتبر A، دادهٔ scope موجود و مسیر کلیدهای `auth_*` در store پیش‌فرض حفظ شده‌اند.

- درخواست: `CODE-MATH9-ACCOUNT-20261019/r2`؛ packet SHA-256: `5dd09178afe120d7edf86c2a8ed398d4e60296f00bed15ecca7f0b0a160b852e`.
- مبنای اپ: `3e6e91dea23e2b373ec3c68d4b2cfc995569efd7`؛ [کامیت اصلاح](https://github.com/samanta-nz/com.hamyareman.final/commit/7e2a49abb94a0fb1db15e0dfa3ffa8a7177b4b04) روی `codex/fix-math-account-guest-isolation`، commit دقیق: `7e2a49abb94a0fb1db15e0dfa3ffa8a7177b4b04`.
- [diff قابل اعمال](./app-fix.patch)، [manifest سورس و hashها](./source-manifest.json)، [قرارداد ذخیره‌سازی](./STORAGE_CONTRACT.md)، [شاهد قرارداد bridge و fixture](./contract-evidence.json).
- [درخواست واقعی](./CODE_REQUEST.json) و [INPUT_ACK](./INPUT_ACK.json) در همین پوشه ثبت‌اند. گیرندهٔ CODE_DELIVERY همان `exam-content-builder` است؛ ارسال خودکار میان چت‌ها انجام نشده است.

## نتیجهٔ آزمون

| کنترل | نتیجه |
|---|---|
| همان ۱۰ تست با LocalStore اصلی از کامیت مبنا | ۸ شکست؛ مسیر نشت legacy/guest بازتولید شد |
| مجموعهٔ کامل `core-common` با اصلاح | ۴۴ تست، صفر شکست، صفر skip؛ شامل هر ۱۰ تست جداسازی |
| عدم وابستگی core-common به پایه‌ها | PASS |
| اسکریپت content readiness | ۴ تست PASS |
| بررسی diff | PASS |
| ساخت کامل اپ، گوشی، شبیه‌ساز، WebView نصب‌شده، حساب واقعی، backend/sync | NOT_RUN |
| QA مستقل برای کامیت اصلاح | PENDING؛ درخواست‌کننده باید بستهٔ هماهنگ جدید تهیه کند |

[نتیجهٔ ماشین‌خوان و فهرست تست‌ها](./test-results.json)، [log بازتولید](./tests-baseline.log)، [log آزمون نهایی](./tests-fixed.log)، [XMLهای مبنا](./baseline-junit/)، [XMLهای اصلاح](./fixed-junit/) و [فهرست دستگاه‌ها](./devices.log) قابل بررسی‌اند. این آزمون‌ها کد واقعی LocalStore را در JVM با Robolectric روی Android API 28 اجرا کرده‌اند؛ جای آزمون اپ نصب‌شده نیستند. ابزارهای اجرا: JDK 21.0.12.1، Gradle 9.6.0 و compileSdk 37 مطابق پروژه.

سناریوها: مهاجرت A → خروج → مهمان؛ A → B؛ ویرایش پاسخ مهمان و بازگشت به A؛ ساخت دوبارهٔ LocalStore؛ حساب قبلاً مهاجرت‌کرده؛ مهمان bound؛ پاک‌کردن/حذف داده؛ legacy بی‌صاحب؛ انواع دادهٔ مهاجرت؛ و کلیدهای auth. fixture از `hamyar_math_html`، `html:exam:C905_E00-SUM` و سند `f00-tab05-easy-01` با schema واقعی استفاده می‌کند.

## دامنه و موارد باز

فقط LocalStore، وابستگی تست Robolectric و فایل تست تغییر کرده‌اند. ثبت نتایج، API/backend، bridge، HTML، اسکریپت‌های داخلی، منو، route، Theme، بانک و شناسه‌ها تغییر نکرده‌اند. [مقایسهٔ کل درخت دارایی‌ها](./content-integrity.json) برابری همهٔ assets پایهٔ نهم و assets مشترک اپ را ثابت می‌کند. دادهٔ legacy حذف نمی‌شود؛ دادهٔ بدون owner قابل‌اثبات به مهمان نسبت داده نمی‌شود.

کد برای بازبینی و بازآزمایی آماده است؛ پذیرش کامل runtime هنوز به اجرای دستگاه وابسته است. مالک اجرای دستگاه app-development/QA در بستهٔ بازآزمایی است. درخواست‌کننده `exam-content-builder` باید HTMLها، اسکریپت‌ها، شناسه‌ها، مسیرها و قرارداد ذخیره‌سازی را با همین کامیت تطبیق دهد، application commit جدید را در manifest درج کند و بستهٔ هم‌نسخه را برای QA آماده کند.

اسکریپت واقعی `scripts/check-release-scope.py --baseline release/published.json --grades 4 5 6 7 8 9 10 11 12` در مبنا و پس از اصلاح با `Shared changes require a new core version` متوقف شد: [قبل](./release-guard-before.log)، [بعد](./release-guard-after.log). نسخهٔ انتشار عمداً در این اصلاح تعیین نشده است؛ تغییر LocalStore مشترک است و انتشار آتی به نسخهٔ هستهٔ تازه و اعتبارسنجی همهٔ پایه‌های مصرف‌کننده توسط مدیر/Release نیاز دارد. این بسته آمادهٔ انتشار APK اعلام نمی‌شود.

هیچ merge در main اپ، bucket sync، فعال‌سازی زنده، APK یا backend منتشر نشده است. گزارش در GitHub ثبت می‌شود؛ transport بین چت‌ها `BLOCKED_NO_TRANSPORT` است و پذیرش گیرنده یا QA PASS ادعا نمی‌شود. لینک همین خروجی باید دستی به چت درخواست‌کننده منتقل شود؛ دستور بازگشت و بازآزمایی در `RETEST_PROMPT.md` ثبت خواهد شد.
