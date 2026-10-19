# اصلاح QA ریاضی نهم — بستهٔ ۰۰۱

محل دائمی نتایج این نقش: [Exam-Content-Builder](https://github.com/samanta-nz/Books-Data/tree/main/codex-reports/Exam-Content-Builder). انتشار این snapshot در تاریخ **۲۰۲۶-۱۰-۱۹، UTC** طبق دستور مستقیم کاربر انجام می‌شود.

**وضعیت:** اصلاح چهار یافتهٔ محتوایی انجام و توسط مؤلف بررسی شده است؛ پذیرش مستقل هنوز در انتظار بازآزمایی است. **M9-QA-003 در اپ باز است.** دریافت CODE_DELIVERY، اجرای واقعی گوشی، sync و release انجام نشده‌اند.

## ارجاع و نسخهٔ واقعی

- کار اصلی: `MATH9-ALL-COMPLETION-20261018`؛ اصلاح: `MATH9-QA-REMEDIATION-20261019`.
- [درخواست توسعه](CODE_REQUEST.json): `CODE-MATH9-ACCOUNT-20261019`، نسخهٔ ۲؛ [درخواست QA](QA_REQUEST.r2.json): `QA-MATH9-ALL-20261018`، نسخهٔ ۲.
- ریپوی محتوا: https://github.com/samanta-nz/Books-Data — شاخهٔ `codex/g9-math-whole-book`؛ snapshot گزارش پیشین: `2ffdc5b02d6ee73d60765879cbdef2a663e18de5`.
- محتوا: `2a19ac65bbc79f4ce21647c9bf463c6662f82b5b`؛ اپ: `3e6e91dea23e2b373ec3c68d4b2cfc995569efd7` در [ریپوی خصوصی اپ](https://github.com/samanta-nz/com.hamyareman.final/tree/3e6e91dea23e2b373ec3c68d4b2cfc995569efd7).
- [manifest منجمد](all-files.manifest.json)، SHA-256: `96282a60db3d5640628bc4736b2fa6619c84fe0b8124b71a19cf2ee04fa8f495`.
- [گزارش کامل مؤلف](REMEDIATION_REPORT.md)، [وضعیت فنی](delivery-status.json)، [رسید ورودی QA](qa-input-receipt.json)، [نتیجهٔ مؤلف](WORK_RESULT.r2.json).

## ادامهٔ کار

۱. متن [پرامپت توسعهٔ اپ](APP_DEVELOPMENT_PROMPT.md) در چت **Hamyar|App Development** وارد شود؛ نتیجهٔ CODE_DELIVERY با URL واقعی و commit/hash به همین سازندهٔ محتوا برگردد.

۲. پس از بررسی خروجی اپ، manifest و درخواست QA به کامیت تازه متصل شوند. [پرامپت فعلی QA](QA_RETEST_PROMPT.md) برای نسخهٔ فعلی است و پس از تغییر اپ باید نسخهٔ تازه داشته باشد.

۳. گزارش بعدی سازنده در شمارهٔ بعدی همین ساختار ثبت شود و به [این بسته](https://github.com/samanta-nz/Books-Data/tree/main/codex-reports/Exam-Content-Builder/2026-10-19/001-MATH9-QA-REMEDIATION-20261019) ارجاع بدهد.

این بسته انتقال و فهرست‌کردن شواهد موجود است؛ آزمون تازه، بستن یافتهٔ بومی، تغییر packetهای امضاشده یا پذیرش QA را ادعا نمی‌کند. ابزار ارسال رسمی بین چت‌ها در دسترس نیست (`BLOCKED_NO_TRANSPORT`).

[فهرست فایل‌ها و hashها](PACKAGE_MANIFEST.json) و [منشأ snapshot](PUBLICATION_RECORD.json) برای تطبیق بسته موجودند. فایل‌های JSON و شواهد اجرایی اصلی بدون تغییر بایت کپی شده‌اند؛ README و پرامپت‌ها برای محل انتشار جدید تنظیم شده‌اند. مسیرهای محلی داخل شواهد، مسیر زمان اجرای قبلی‌اند؛ لینک فایل‌های اصلیِ متکی بر آن‌ها در commit منبع قابل پیگیری است.
