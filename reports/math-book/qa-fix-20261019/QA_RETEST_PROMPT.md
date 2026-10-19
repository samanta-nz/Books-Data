این متن را در چت کنترل کیفیت «Hamyar code analyses» وارد کنید. بازآزمایی محتوایی می‌تواند انجام شود؛ پذیرش کلی تا رفع M9-QA-003 باز است.

```text
بازتست ریاضی نهم؛ QA_REQUEST با شناسه QA-MATH9-ALL-20261018 اکنون revision 2 است:
https://raw.githubusercontent.com/samanta-nz/Books-Data/refs/heads/codex/g9-math-whole-book/reports/math-book/qa-fix-20261019/QA_REQUEST.r2.json

packet SHA-256 مورد انتظار: 10904e15016055bad27a19b868770a2293d4b02c25ee130fbf7a3bd6fee8b842
بستهٔ JSON واقعی را دریافت و hash/schema آن را بررسی کن. پاسخ QA_REPORT باید دقیقاً به revision و packet_sha256 همین بسته متصل باشد.
manifest تازه و ثابت:
https://raw.githubusercontent.com/samanta-nz/Books-Data/c9ad9dd3485238c07ba672f924097d538c8530f9/reports/math-book/qa-fix-20261019/all-files.manifest.json
SHA-256: 96282a60db3d5640628bc4736b2fa6619c84fe0b8124b71a19cf2ee04fa8f495
کامیت محتوا: 2a19ac65bbc79f4ce21647c9bf463c6662f82b5b
کامیت اپ: 3e6e91dea23e2b373ec3c68d4b2cfc995569efd7

ریپوها:
https://github.com/samanta-nz/Books-Data
https://github.com/samanta-nz/com.hamyareman.final
شاخهٔ هر دو: codex/g9-math-whole-book؛ اپ خصوصی است و دسترسی GitHub لازم دارد.

M9-QA-001/002/004/005 را با گزارش اصلی خودت و فایل‌های واقعی نسخهٔ تازه بازآزمایی کن: بازخورد اختصاصی پس از finish، تکرار عینی صفر، تفاوت سطح، دامنهٔ صحیح و علامت‌های خوانا. فرم ۱۶ سؤال/۳۸ بخش/۲۰ نمره، ذخیرهٔ واقعی، تاریخچهٔ نسخه و قالب/موبایل باید حفظ شده باشند.
تغییر عددها را سؤال مرجع تازه نشمار؛ بانک همچنان ۴۱۱ سؤال است.
M9-QA-003 متعلق به توسعهٔ اپ و هنوز باز است؛ CODE_REQUEST در همین پوشه است. نتیجهٔ کلی را تا اصلاح و شواهد معتبر آن PASS اعلام نکن. اگر CODE_DELIVERY کامیت تازه‌ای دارد، ابتدا تطبیق manifest/request تازه لازم است؛ با شاخهٔ متحرک یا تست bridge ساختگی، اجرای واقعی اپ را تأیید نکن.
بانک و منو را بازتولید نکن. هیچ merge، bucket sync یا release انجام نده. گزارش و بستهٔ QA_REPORT را با URL واقعی و commit/hash قابل دریافت تحویل بده.
```
