# G09-English — صداگذاری درس ۱ کتاب اصلی

**وضعیت: تکمیل شد؛ هر ۴۱ بخش از ۴۱ بخش امبد شده است.**

این پوشه برای تکمیل `prospect3-lesson-01` با صدای مصوب آرتین (`voice-02`) و رها (`voice-05`) ساخته شده است. متن منبع درس ۲۴۲ نوبت گفتار دارد. شناسهٔ بخش‌ها و نام فایل‌های صوتی حفظ شده است.

## اصلاح درخواستی

در نوبت `prospect3-lesson-01-turn-035` جمله به متن زیر اصلاح شد:

> دوستی رو تصور کنین که وقتی درس رو نمی‌فهمم کمک می‌کنه و هنگام انتظار عصبانی نمی‌شه.

معادل متن قابل‌مشاهده در HTML نیز اصلاح شد. جزئیات در `source-overrides.json` ثبت است.

## بخش‌های دارای صوت در این مرحله

1. `goals`
2. `bridge-word-roles`
3. `bridge-subject-pronouns`
4. `bridge-be-present`
5. `bridge-number-articles`
6. `local-prerequisite-check`
7. `start` — با جملهٔ اصلاح‌شده
8. `prerequisites`
9. `entry`
10. `source-conversation` — هر ۱۸ نوبت کامل
11. `meaning`
12. `be-positive`
13. `negative`
14. `questions` — هر ۷ نوبت و ۱۰ مکث بلند
15. `contractions`
16. `melody`
17. `source-melody` — هر ۹ نوبت کامل
18. `speak` — هر ۵ نوبت و ۴ مکث بلند
19. `errors-summary`
20. `pron-card-guide`
21. `pron-sound-symbols`
22. `pron-voice-air`
23. `pron-persian-consonants`
24. `pron-syllables-stress`
25. `vocabulary-cards` — هر ۵۴ نوبت کامل
26. `official-pictures`
27. `source-grammar`
28. `examples`
29. `examples-02`
30. `examples-03`
31. `examples-04`
32. `examples-05`
33. `examples-06`
34. `lab`
35. `source-reading`
36. `reading`
37. `writing`
38. `quiz`
39. `listening` — هر ۱۰ نوبت و ۵ مکث بلند
40. `book-source-pages`
41. `sources`

شش بخش `local-prerequisite-check`، `entry`، `official-pictures`، `lab`، `writing` و `quiz` متن گفتاری کاملاً یکسان دارند و مطابق راهنما از یک ضبط مشترک استفاده می‌کنند؛ نام فایل و حافظهٔ پخش هر بخش مستقل است.

## قالب و رفتار پلیر

- خروجی واقعی: **WebM صوتی، Opus، تک‌کاناله، ۴۸kbps** با پسوند `.weba`.
- فشرده‌سازی برای گفتار و کاهش حجم Base64 است؛ تبدیل صرف پسوند انجام نشده است.
- صوت هر بخش به‌صورت `data:audio/webm;base64,...` داخل همان `<audio>` امبد شده است.
- هیچ پخش خودکاری اضافه نشده و همهٔ پلیرها `preload="none"` دارند.
- پخش فقط با دکمهٔ کاربر آغاز می‌شود؛ بستن بخش صدا را متوقف می‌کند و رفتار حافظهٔ موجود حفظ شده است.
- هر ۴۱ بخش صوت تولیدشده و دکمهٔ فعال دارد؛ هیچ پلیرِ خالی یا غیرفعالی باقی نمانده است.

## کنترل‌ها

- همهٔ فایلهای `.weba` این مرحله رمزگشایی و از نظر صوتی‌بودن و نبود ویدئو کنترل شدند.
- Base64 هر بخش از HTML نهایی استخراج و دوباره decode شد؛ بایت‌ها و SHA-256 آن با فایل صوتی همان بخش یکسان است.
- فایل `audio-receipt.json` مشخصات صوت، `generation-log.json` متن و شناسهٔ تولید، `embedding-receipt.json` نتیجهٔ امبد و `progress.json` فهرست دقیق بخش‌های باقی‌مانده را ثبت می‌کند.

## فایل اصلی

`prospect3-lesson-01.html`

این HTML **خروجی نهایی و خودکفای درس ۱** است. هر ۴۱ صوت به‌صورت Base64 داخل فایل قرار دارد و بررسی منابع هیچ ارجاعِ بارگذاریِ خارجی نشان نداد. کنترل نهایی در `completion-receipt.json` ثبت شده است. رسیدهای تولید دسته‌های دوم تا هفدهم نیز در `generation-log-002.json` تا `generation-log-017.json` نگهداری می‌شوند.
