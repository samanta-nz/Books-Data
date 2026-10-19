این دستور و لینک خروجی را دستی به چت «Cont|Hamyar|Exam Content Builder» منتقل کنید. ارسال خودکار یا پذیرش مقصد انجام نشده است.

```text
ادامهٔ CODE-MATH9-ACCOUNT-20261019 / revision 2؛ گیرنده exam-content-builder، همان درخواست‌کننده است.
خروجی app-development برای M9-QA-003:
https://github.com/samanta-nz/Books-Data/blob/main/codex-reports/Hamyar%7CApp%20Development/2026-10-19/001-M9-QA-003/CODE_DELIVERY.json
شناسه: CODE-DELIVERY-MATH9-ACCOUNT-20261019 / revision 1
packet SHA-256: 09bccbb7741bc7d9039aecbe1bf677b58c066fb9da5faaed96de5ceb1da91258
پس از دریافت، JSON packet را طبق HANDOFF.md canonical کن و hash آن را تطبیق بده؛ مرجع main را سپس به commit واقعی دریافتی pin کن.

گزارش و شواهد immutable:
https://github.com/samanta-nz/Books-Data/blob/f9fd1d01fb197ab1b2be61ac01fdd4240a973c2c/codex-reports/Hamyar%7CApp%20Development/2026-10-19/001-M9-QA-003/README.md
پوشهٔ نتیجهٔ مورد درخواست کاربر:
https://github.com/samanta-nz/Books-Data/tree/main/codex-reports/Hamyar%7CApp%20Development
دستور بازآزمایی:
https://github.com/samanta-nz/Books-Data/blob/main/codex-reports/Hamyar%7CApp%20Development/2026-10-19/001-M9-QA-003/RETEST_PROMPT.md

اپ: https://github.com/samanta-nz/com.hamyareman.final
شاخه: codex/fix-math-account-guest-isolation
کامیت تازهٔ دقیق: 7e2a49abb94a0fb1db15e0dfa3ffa8a7177b4b04
مبنای diff: 3e6e91dea23e2b373ec3c68d4b2cfc995569efd7
مرجع commit: https://github.com/samanta-nz/com.hamyareman.final/commit/7e2a49abb94a0fb1db15e0dfa3ffa8a7177b4b04
Patch و hash فایل‌ها در CODE_DELIVERY و source-manifest.json شواهد immutable آمده‌اند.

اصلاح فقط جداسازی LocalStore در حالت مهمان است. owner خالی از <storeName>__guest استفاده می‌کند؛ دادهٔ legacy فقط برای owner غیرخالی و برابر _legacy_owner مهاجرت می‌شود. دادهٔ A و مسیر auth_* حفظ شده‌اند. کلید html:$kind:$packId و schema hamyar-math-practice-1 تغییر نکرده‌اند.
HTMLها، اسکریپت‌ها، منوها، بانک، Themeها و routeها تغییر نکرده‌اند؛ سازگاری نسخهٔ محتوای خودت را با این commit تازه، شناسه‌ها، مسیرها، bridge و STORAGE_CONTRACT.md کنترل کن. application commit تازه را در manifest هماهنگ درج کن، hashهای واقعی و نسخهٔ قواعد/محتوا را ثبت کن و بستهٔ هم‌نسخه را برای QA آماده کن. این تحویل به‌تنهایی QA PASS نیست.

شاهد توسعه: کد مبنا ۸ شکست از ۱۰ رگرسیون؛ پس از اصلاح ۴۴ تست core-common و verifyNoGradeDependencies موفق. تست‌های جداسازی، JVM/Robolectric هستند؛ گوشی، شبیه‌ساز، اپ نصب‌شده و حساب واقعی NOT_RUN. برای بستن کامل M9-QA-003 آزمون native A -> خروج -> مهمان، A -> B، ویرایش مهمان مستقل از A و برگشت به A بعد از legacy migration، با build دقیق همین commit لازم است. نتیجهٔ هر مرحله فقط با شاهد واقعی و همان hash/commit ثبت شود.

نسخهٔ انتشار تغییر نکرده؛ check-release-scope در مبنا و خروجی به‌علت نیاز به نسخهٔ هستهٔ جدید FAIL است. این تغییر مشترک برای انتشار آتی به کنترل همهٔ پایه‌ها و نسخهٔ تازه توسط مدیر/Release نیاز دارد؛ این دستور مجوز انتشار تازه نیست.
main اپ merge نشده؛ bucket sync، فعال‌سازی زنده و انتشار APK انجام نشده‌اند. لینک نتیجهٔ تطبیق و سپس QA را نیز به چت مسئول منتقل کنید؛ SENT یا پذیرش مقصد را بدون شاهد ثبت نکنید.
```
