# بسته‌های تحویل مرحلهٔ بعد

این فایل‌ها برای ارسال دستی یا انتقال با ابزار رسمی آماده شده‌اند. در این محیط ابزار ارسال بین چت‌ها وجود ندارد؛ هیچ ارسال یا پذیرش از سوی گیرنده ثبت نشده است.

- QA: [QA_REQUEST.json](handoffs/QA_REQUEST.json)، مقصد `qa-analyzer` / `01a144f7-5dfc-72e2-b905-b961a4bb4075` / `durable`؛ درخواست کنترل علمی و فنی مستقل همین manifest است.
- Sync: [SYNC_REQUEST.blocked-draft.json](handoffs/SYNC_REQUEST.blocked-draft.json)، مقصد `content-sync` / `01a14505-1829-728f-8deb-6c6ab6cb6071` / `durable`؛ پیش‌نویس مسدود، `execute=false`، فاقد مجوز اجرا و فاقد مقصد زنده است.
- [WORK_RESULT.json](WORK_RESULT.json) نتیجهٔ مستقلِ سفارش مستقیم کاربر و [INPUT_ACK.json](INPUT_ACK.json) فقط پذیرش ورودی‌اند.
- [delivery-status.json](delivery-status.json) وضعیت تولید، QA، دستگاه، انتقال، GitHub و انتشار را جدا نگه می‌دارد.

manifest واقعی پیش از ساخت این درخواست‌ها در GitHub پوش شده است:

`https://raw.githubusercontent.com/samanta-nz/Books-Data/d15af17b4fadd51c515898e37bd6b2501dd09a10/reports/math-book/final-delivery/all-files.manifest.json`

SHA-256 آن: `26e6293ae93647674aae3f6f84a61c4a6de31637aa0282897db6090d8b28699c`

درخواست QA باید با پاسخ `QA_REPORT` به همان نقش سازنده برگردد؛ مؤلف اصلاح علمی را انجام می‌دهد. درخواست Sync فعلی قابل اجرا نیست؛ پس از رسید QA هم‌نسخه، احراز سازگاری اپ نصب‌شده و مجوز مشخص، نسخهٔ تازهٔ درخواست با مقصد واقعی لازم است. محتوا، منو و بانک آماده را دوباره تولید یا اضافه نکنید.

مرجع کامل: [START_HERE_ALL_MATH9.md](START_HERE_ALL_MATH9.md). همهٔ artifactهای داخل بسته‌ها دارای URL واقعی، commit و hash هستند؛ state انتقال، جای رسید واقعی را نمی‌گیرد.
