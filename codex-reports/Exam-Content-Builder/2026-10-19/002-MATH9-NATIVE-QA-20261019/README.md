# ریاضی نهم — تطبیق اصلاح اپ و درخواست QA نسخهٔ سوم

بستهٔ **۰۰۲**؛ تاریخ ثبت **۲۰۲۶-۱۰-۱۹، UTC**؛ نقش `exam-content-builder`؛ ارجاع `MATH9-NATIVE-QA-20261019`، زیرکار `MATH9-ALL-COMPLETION-20261018`.

**نتیجهٔ این مرحله:** تحویل کد توسعه و تطابق آن با محتوای موجود بررسی شد؛ اجرای محلی ۴۴ تست هسته و ادغام دارایی‌ها موفق است. **QA مستقل و آزمون اپ نصب‌شده هنوز انجام نشده‌اند؛ پذیرش کلی اعلام نمی‌شود.**

[پوشهٔ دائمی نتایج](https://github.com/samanta-nz/Books-Data/tree/main/codex-reports/Exam-Content-Builder) · [بستهٔ قبلی](../001-MATH9-QA-REMEDIATION-20261019/README.md) · [پرامپت آمادهٔ QA](QA_RETEST_PROMPT.md)

## نسخهٔ هم‌خوان

| جزء | مرجع ثابت |
|---|---|
| محتوای علمی و HTML | `2a19ac65bbc79f4ce21647c9bf463c6662f82b5b` در [Books-Data](https://github.com/samanta-nz/Books-Data/tree/2a19ac65bbc79f4ce21647c9bf463c6662f82b5b)، شاخهٔ `codex/g9-math-whole-book` |
| اپ اصلاح‌شده | [`7e2a49abb94a0fb1db15e0dfa3ffa8a7177b4b04`](https://github.com/samanta-nz/com.hamyareman.final/commit/7e2a49abb94a0fb1db15e0dfa3ffa8a7177b4b04)، شاخهٔ `codex/fix-math-account-guest-isolation` |
| manifest تازه | [all-files.manifest.json](all-files.manifest.json)، کامیت `21acf62d6e0edab2c64ac3954f81a55e612ce2f1` |
| SHA-256 manifest | `0cdab4dd22b2d4f2362c3b8960fc03f5e4c6ff5dd5f255adf16c781a03e908d8` |
| درخواست بازآزمایی | [QA_REQUEST.r3.json](QA_REQUEST.r3.json)، `QA-MATH9-ALL-20261018`، نسخهٔ ۳ |
| SHA-256 قطعی درخواست | `ecaffd3a0f762af1d485260d97cbd908aecff495ccfbc2a4ef41b035dd2671e8` |

ریپوی اصلی اپ [com.hamyareman.final](https://github.com/samanta-nz/com.hamyareman.final) خصوصی است. شاخهٔ قدیمی اپ `codex/g9-math-whole-book` هنوز شامل اصلاح جدید نیست؛ برای QA همین کامیت دقیق اصلاح را دریافت کنید. main اپ مبنای build کامل نیست.

## آنچه بررسی شد

- [CODE_DELIVERY توسعه](https://github.com/samanta-nz/Books-Data/blob/e733076ada32ff7385aad24d2a4da13f228dab5c/codex-reports/Hamyar%7CApp%20Development/2026-10-19/001-M9-QA-003/CODE_DELIVERY.json): schema و hash قطعی، نقش‌ها، اتصال دقیق به `CODE-MATH9-ACCOUNT-20261019/r2`، ۲۷ checksum، دوازده artifact ثابت، سه فایل سورس و ۴۴ نتیجهٔ JUnit بررسی شدند؛ [رسید دریافت واقعی](code-input-receipt.json).
- diff واقعی فقط `LocalStore.kt`، وابستگی Robolectric و تست جداسازی را تغییر می‌دهد. patch تحویل‌شده با diff کامیت دقیق یکسان است. [گزارش تطبیق](compatibility-verification.json).
- هر **۲۵۲ HTML و ۲۵۲ Theme** با محتوای منجمد و assets کامیت جدید تطبیق بایت دارد. منو، routeها، metadata کارت‌ها، `MathHtmlWebView.kt` و `hamyar-persist.js` ثابت‌اند. بانک/منو/فایل آموزشی تازه‌ای تولید نشد؛ شمار همان **۴۱۱ سؤال، ۱۹۰ کارت و ۲۱۶ آزمون** است.
- اجرای تازهٔ مؤلف: **۴۴ تست JVM/Robolectric موفق، صفر شکست/خطا/skip**؛ `verifyNoGradeDependencies` و `mergeP09DebugAssets` موفق؛ خروجی ادغام‌شدهٔ همهٔ HTML/Themeها و منو/routes با سورس مطابق است. [گزارش](native-recheck.json)، [log](native-recheck.log)، [XMLهای واقعی](native-junit/). اجرای نخست فقط برای استفاده از cache وابستگی موجود متوقف شد و شاهد آن جدا حفظ شده است؛ [log اولیه](native-recheck-initial.log).
- [verifier قالب locked](locked-verification.txt) موفق است. مرورگر در این مرحله دوباره اجرا نشد؛ HTMLها و اسکریپت‌های پل دقیقاً همان بایت‌های دارای پوشش قبلی‌اند. شواهد مرورگر در manifest به کامیت محتوای اصلی متصل‌اند.

## ثبت نتایج و محدودهٔ پذیرش

قرارداد فعلی `Hamyar.loadState/saveState/recordItem/recordExam`، store برابر `hamyar_math_html`، کلید `html:$kind:$packId` و schema برابر `hamyar-math-practice-1` حفظ شده است. owner خالی اکنون از `<storeName>__guest` استفاده می‌کند؛ legacy فقط برای owner غیرخالی و مطابق مالک قبلی مهاجرت می‌شود. دادهٔ معتبر حساب، scopeهای موجود و auth حفظ می‌شوند؛ legacy بی‌صاحب در بایت‌های قبلی باقی می‌ماند و به مهمان نسبت داده نمی‌شود. [قرارداد اصلی توسعه](https://github.com/samanta-nz/Books-Data/blob/f9fd1d01fb197ab1b2be61ac01fdd4240a973c2c/codex-reports/Hamyar%7CApp%20Development/2026-10-19/001-M9-QA-003/STORAGE_CONTRACT.md).

M9-QA-003 اکنون **کد اصلاح‌شده و شاهد host دارد؛ هنوز در انتظار QA مستقل و بررسی runtime است**. چهار یافتهٔ محتوایی قبلی نیز تا بازآزمایی مستقل، پذیرش نهایی ندارند. [وضعیت دقیق](delivery-status.json) · [نتیجهٔ این مرحله](WORK_RESULT.r3.json).

## قدم بعد و موارد باز

متن [پرامپت QA](QA_RETEST_PROMPT.md) را در چت **Hamyar|code analyses** وارد کنید. هر پنج یافته باید با همین manifest و اپ بررسی شوند و گزارش QA با URL واقعی، commit/hash و اتصال به درخواست نسخهٔ سوم به همین سازنده برگردد. گزارش QA در مسیر اختصاصی همان نقش منتشر می‌شود؛ نتیجهٔ بعدی سازنده در شمارهٔ بعدی [این پوشه](https://github.com/samanta-nz/Books-Data/tree/main/codex-reports/Exam-Content-Builder) ثبت خواهد شد.

`[نیاز به تأیید]` پذیرش مستقل پنج یافته؛ رفتار ارتقای legacy، A → خروج → مهمان، A → B، ویرایش مستقل مهمان و برگشت A در اپ نصب‌شده روی دستگاه یا شبیه‌ساز؛ ثبت و بازیابی پاسخ/خطا و progress/ledger واقعی. در این مرحله دستگاه، شبیه‌ساز، WebView نصب‌شده و ساخت کامل APK همگی `NOT_RUN` هستند. اگر QA دستگاه ندارد باید این وابستگی را صریحاً مسدود اعلام کند.

release-scope در مبنا و اصلاح به دلیل نیاز به نسخهٔ هستهٔ تازه FAIL بوده است؛ این محدودیت برای انتشار آتی و بررسی تمام پایه‌های مصرف‌کنندهٔ هسته به مدیر/Release تعلق دارد. در این مرحله نسخهٔ انتشار تغییر نکرده، سورس main اپ merge نشده، bucket sync، فعال‌سازی زنده و انتشار APK انجام نشده است. انتشار این پوشه فقط گزارش است.

ارسال رسمی بین چت‌ها ابزار در دسترس ندارد (`BLOCKED_NO_TRANSPORT`)؛ تحویل از ارجاع واقعی کاربر به GitHub دریافت شد و هیچ SENT یا ACK گیرندهٔ QA ساخته نشده است.

[فهرست تمام فایل‌ها با اندازه و SHA-256](PACKAGE_MANIFEST.json).
