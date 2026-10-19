این متن را در چت **Hamyar code analyses** وارد کنید. نسخهٔ سوم جایگزین درخواست نسخهٔ دوم است؛ ارسال خودکار بین چت‌ها انجام نشده است.

```text
نقش مقصد qa-analyzer است؛ بازآزمایی ریاضی نهم، هر هشت فصل و مرور کل کتاب.
درخواست: QA-MATH9-ALL-20261018 / revision 3
packet SHA-256: ecaffd3a0f762af1d485260d97cbd908aecff495ccfbc2a4ef41b035dd2671e8
بستهٔ واقعی درخواست را دریافت و schema/hash آن را بررسی کن؛ پاسخ QA_REPORT باید دقیقاً به همین شناسه، نسخه و digest متصل باشد:
https://raw.githubusercontent.com/samanta-nz/Books-Data/refs/heads/main/codex-reports/Exam-Content-Builder/2026-10-19/002-MATH9-NATIVE-QA-20261019/QA_REQUEST.r3.json

manifest ثابت و تازه:
https://raw.githubusercontent.com/samanta-nz/Books-Data/21acf62d6e0edab2c64ac3954f81a55e612ce2f1/codex-reports/Exam-Content-Builder/2026-10-19/002-MATH9-NATIVE-QA-20261019/all-files.manifest.json
manifest SHA-256: 0cdab4dd22b2d4f2362c3b8960fc03f5e4c6ff5dd5f255adf16c781a03e908d8
ریپوی محتوا: https://github.com/samanta-nz/Books-Data
شاخهٔ محتوا: codex/g9-math-whole-book
کامیت محتوا: 2a19ac65bbc79f4ce21647c9bf463c6662f82b5b
ریپوی اصلی اپ (خصوصی): https://github.com/samanta-nz/com.hamyareman.final
شاخهٔ اصلاح اپ: codex/fix-math-account-guest-isolation
کامیت دقیق اپ: 7e2a49abb94a0fb1db15e0dfa3ffa8a7177b4b04
مبنای اپ قبل از اصلاح: 3e6e91dea23e2b373ec3c68d4b2cfc995569efd7
شاخهٔ قدیمی اپ codex/g9-math-whole-book هنوز مرجع اصلاح جدید نیست؛ همین commit دقیق را checkout کن. main اپ فقط Rules/README دارد و مبنای build نیست.

CODE_DELIVERY پذیرفته‌شده از نظر تمامیت و اتصال درخواست:
https://github.com/samanta-nz/Books-Data/blob/e733076ada32ff7385aad24d2a4da13f228dab5c/codex-reports/Hamyar%7CApp%20Development/2026-10-19/001-M9-QA-003/CODE_DELIVERY.json
شناسهٔ تحویل: CODE-DELIVERY-MATH9-ACCOUNT-20261019 / revision 1
packet SHA-256 تحویل: 09bccbb7741bc7d9039aecbe1bf677b58c066fb9da5faaed96de5ceb1da91258

هر پنج یافتهٔ M9-QA-001 تا M9-QA-005 را در برابر گزارش اصلی خودت بازآزمایی کن. چهار اصلاح محتوا همان نسخهٔ پیشین‌اند؛ هیچ HTML یا Theme یا منویی در این مرحله تغییر نکرده است. تطبیق تازهٔ ۲۵۲ HTML و ۲۵۲ Theme، اجرای مجدد ۴۴ تست core-common، verifyNoGradeDependencies و ادغام assets با کنترل منو/routes موفق‌اند. این‌ها شواهد مؤلف/توسعه‌اند، نه QA مستقل.

M9-QA-003: مسیر مهمان مستقل شده؛ legacy فقط برای owner غیرخالی و مطابق _legacy_owner مهاجرت می‌شود. حفظ دادهٔ معتبر A و auth_*، ارتقای دادهٔ قدیمی، A → خروج → مهمان، A → B، ویرایش مستقل مهمان، ساخت مجدد store و برگشت به A را بررسی کن. store برابر hamyar_math_html، کلید html:$kind:$packId و schema برابر hamyar-math-practice-1 حفظ شده‌اند. ذخیره و بازیابی پاسخ/خطا، progress و ledger را در اپ همان نسخه بررسی کن.

گوشی، شبیه‌ساز، اپ نصب‌شده و build کامل APK هنوز NOT_RUN هستند. برای پذیرش کامل runtime، اجرای واقعی دستگاه یا شبیه‌ساز و شاهد رفتار حساب‌ها لازم است. اگر در دسترس نیست، وضعیت را BLOCKED/NOT_RUN گزارش کن؛ Robolectric یا Chromium با bridge ساختگی جای آن را نمی‌گیرد.

فرم برگه‌های جامع ۱۶ سؤال/۳۸ بخش/۲۰ نمره، خودارزیابی صادقانه، پنهان‌بودن نتیجه تا پایان، feedback اختصاصی، تکرار عینی صفر، دامنه و علامت‌ها، قالب locked، ارقام فارسی/وزیر و موبایل نیز حفظ و بازآزمایی شوند. بانک همچنان ۴۱۱ سؤال و ۱۹۰ کارت دارد؛ تغییرات عددی نسخهٔ آزمون، سؤال مرجع تازه نیست.

مسیر دائمی گزارش‌های درخواست‌کننده:
https://github.com/samanta-nz/Books-Data/tree/main/codex-reports/Exam-Content-Builder
بستهٔ فعلی و شواهد هم‌نسخه:
https://github.com/samanta-nz/Books-Data/tree/main/codex-reports/Exam-Content-Builder/2026-10-19/002-MATH9-NATIVE-QA-20261019
این دو لینک را در دستورهای ادامه حفظ کن. گزارش QA را در پوشهٔ تاریخ‌دار و شماره‌دار نقش خودت منتشر و URL واقعی، commit/hash، نتیجهٔ هر پنج یافته و حدود اجرای دستگاه را به exam-content-builder برگردان؛ بستهٔ FAIL قبلی بازنویسی نشود.

release-scope در مبنا و اصلاح به دلیل نیاز به ارتقای نسخهٔ هسته FAIL است؛ این موضوع مربوط به انتشار آتی و همهٔ پایه‌های مصرف‌کنندهٔ هسته است. نسخهٔ انتشار را در این بازآزمایی تغییر نده. بانک/منو را بازتولید نکن؛ merge سورس main، bucket sync، فعال‌سازی زنده و انتشار APK مجاز نیست. ارسال یا پذیرش بین چت‌ها را بدون شاهد ثبت نکن.
```
