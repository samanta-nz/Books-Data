# نشانی‌های تحویل GitHub

نسخهٔ اصلاحی پس از گزارش FAIL: [گزارش اصلاح و درخواست بازآزمایی](qa-fix-20261019/README.md). برای وضعیت جاری این نسخه، نتیجهٔ QA قبلی را PASS فرض نکنید.


راهنمای کامل هر هشت فصل و مرور جامع: [START_HERE_ALL_MATH9.md](https://github.com/samanta-nz/Books-Data/blob/codex/g9-math-whole-book/reports/math-book/final-delivery/START_HERE_ALL_MATH9.md). manifest کامل، همهٔ ۲۵۲ HTML و Themeهای متناظر را به commit ثابت محتوا و اپ متصل می‌کند.

این مرحله پس از دستور تازهٔ کاربر برای commit و push انجام می‌شود؛ گزارش‌های آزمون قبلی مربوط به مرحلهٔ تولید و بررسی محلی‌اند.

| مورد | نشانی |
|---|---|
| پروژهٔ اصلی اپ | https://github.com/samanta-nz/com.hamyareman.final |
| سورس اپِ آماده | https://github.com/samanta-nz/com.hamyareman.final/tree/codex/g9-math-whole-book |
| کامیت اپ | https://github.com/samanta-nz/com.hamyareman.final/commit/3e6e91dea23e2b373ec3c68d4b2cfc995569efd7 |
| ریپوی اصلی محتوا | https://github.com/samanta-nz/Books-Data |
| شاخهٔ محتوا | https://github.com/samanta-nz/Books-Data/tree/codex/g9-math-whole-book |
| پرامپت قابل ارسال به ایجنت | https://github.com/samanta-nz/Books-Data/blob/codex/g9-math-whole-book/reports/math-book/APP_MENU_PROMPT.md |
| بستهٔ کوچک منو | https://github.com/samanta-nz/Books-Data/raw/refs/heads/codex/g9-math-whole-book/reports/math-book/whole-book-menu-handoff.zip |

شاخهٔ هر دو ریپو `codex/g9-math-whole-book` است. شاخهٔ محتوا از آخرین main بررسی‌شده، `51afd4c3a91be6026668fa248aaaa762c384bd70`، ساخته شده است. شاخهٔ اپ بر پایهٔ سورس واقعی `migration/modular-grades` با commit مبنای `c09746a5210c7fc9ea4e55fc48a97127b2f5a8d9` است؛ main اپ در زمان بررسی فقط commit ابتدایی و README داشت. برای دسترسی به سورس، شاخهٔ مشخص‌شده را انتخاب کنید.

محتوای منتشرشده شامل همهٔ دویست و پنجاه و دو HTML، دویست و پنجاه و دو Theme، ابزارهای تولید و کنترل کیفیت، راهنمای قالب، گزارش پژوهش و آزمون، پرامپت و بستهٔ کوچک منوی کل کتاب است. نسخهٔ متناظر assets و اتصال منو/bridge نیز در ریپوی اپ قرار دارد.

فایل ZIP بزرگِ کامل و ZIP قدیمی فصل اول، آرشیوهای محلی‌اند و در Git نگه‌داری نمی‌شوند؛ همان فایل‌های محتوایی به‌صورت عادی در ریپو موجودند. بستهٔ کوچک قابل دانلود، بیست‌وهشت HTML و Themeهای کل کتاب و JSONهای مخصوص ادغام را دارد.

هیچ force-push، ادغام در main، bucket sync یا release در این مرحله انجام نمی‌شود. تست‌های قبلی همچنان برای همان بایت‌های HTML و کد اپ معتبرند؛ commit/push، اجرای روی گوشی واقعی را تأیید نمی‌کند.
