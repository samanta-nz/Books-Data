این متن را در چت «Hamyar|App Development» وارد کنید.

```text
ادامهٔ گردش ریاضی نهم؛ نقش مقصد app-development است.
اگر نقش هنوز راه‌اندازی نشده، START_HERE.md داخل بستهٔ واقعی زیر را بخوان و راه‌اندازی کن:
https://github.com/samanta-nz/com.hamyareman.final/blob/main/Rules/app-development.rules.zip
شناسهٔ درخواست: CODE-MATH9-ACCOUNT-20261019 / revision 2 / packet SHA-256 5dd09178afe120d7edf86c2a8ed398d4e60296f00bed15ecca7f0b0a160b852e
بستهٔ واقعی CODE_REQUEST را از این نشانی دریافت و schema/hash آن را بررسی کن؛ سپس INPUT_ACK بده و M9-QA-003 را در کد واقعی بازتولید و اصلاح کن:
https://raw.githubusercontent.com/samanta-nz/Books-Data/refs/heads/codex/g9-math-whole-book/reports/math-book/qa-fix-20261019/CODE_REQUEST.json

ریپوی اصلی اپ: https://github.com/samanta-nz/com.hamyareman.final
شاخه: codex/g9-math-whole-book
کامیت فعلی متناظر با محتوای اصلاح‌شده: 3e6e91dea23e2b373ec3c68d4b2cfc995569efd7
ریپوی محتوا و گزارش‌ها: https://github.com/samanta-nz/Books-Data
این ریپوی اپ خصوصی است؛ از اتصال دارای دسترسی استفاده کن و فقط main را جست‌وجو نکن.

در LocalStore.prefsFor، owner تهی به basePrefs می‌رود و ممکن است دادهٔ legacy حساب A بعد از مهاجرت در مسیر مهمان دیده شود. جزئیات و شاهدِ تأییدشده در QA_REPORT پیوستِ packet است.
اصلاح را در ساختار فعلی انجام بده؛ دادهٔ معتبر A و رفتار کلیدهای auth حفظ شوند. API یا backend جدید نساز.
آزمون‌های A → خروج → مهمان، A → B، مستقل‌ماندن ویرایش مهمان و برگشت به A را با دادهٔ آزمایشی hamyar_math_html اجرا کن.
محتوا، منوی مرور جامع، بانک، فلش‌کارت و HTMLها آماده‌اند؛ آن‌ها را دوباره تولید یا اضافه نکن.
گزارش CODE_DELIVERY را در پاسخ به همین درخواست با commit دقیق، hash و نتایج واقعی آزمون تحویل بده. اصلاح را روی شاخهٔ کاری مجاز commit و push کن تا قابل دریافت باشد. اجرای گوشی/شبیه‌ساز را فقط اگر انجام شد تأیید کن؛ در غیر این صورت NOT_RUN بنویس.
از merge در main، bucket sync، فعال‌سازی زنده و انتشار APK خودداری کن.
گزارش و بستهٔ CODE_DELIVERY را با لینک واقعی GitHub، commit و hash قابل دریافت تحویل بده؛ مسیر محلی /workspace برای چت دیگر کافی نیست.
نتیجه باید به exam-content-builder، درخواست‌کنندهٔ همین CODE_REQUEST، برگردد تا کامیت تازهٔ اپ در manifest ثبت و برای QA هم‌نسخه تحویل شود.
```
