# ساخت روایت صوتی درس‌های ریاضی نهم

تبدیل هر فایل `F0X/ryazifXXdYY.md` به یک فایل صوتی `.weba` (Opus در ظرف WebM) کنار همان فایل.

## چرا این‌جا و نه با API ابری

سندباکس به سرویس‌های TTS ابری (Google، Hugging Face) دسترسی ندارد؛ فقط GitHub و PyPI باز است.
بنابراین مدل‌های گفتار یک‌بار در GitHub Actions دریافت و سبک می‌شوند
(`.github/workflows/fetch-tts-voices.yml`) و در `tools/voices/` کامیت می‌شوند؛
سپس همهٔ ساخت صدا محلی و تکرارپذیر انجام می‌شود.

## صداها

| گوینده | موتور | مدل |
|---|---|---|
| فرسام (معلم) | Piper | `fa_IR-ganji_adabi-medium` (جایگزین: `amir`, `gyro`) |
| سروناز (دانش‌آموز) | VITS / MMS | `facebook/mms-tts-fas` |

## اجرا

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt

# یک درس
python build.py --files F01/ryazif01d01.md

# ۱۰ فایل بعدی (به ترتیب)
python build.py --limit 10

# آزمون خط لوله بدون مدل صدا (سکوت)
python build.py --limit 1 --engine stub --force
```

خروجی: `F01/ryazif01d01.weba` + گزارش `audio-report.md` در ریشهٔ همین پوشه + وضعیت در `build-state.json`.

## ساختار

| فایل | کار |
|---|---|
| `parse_lesson.py` | مارک‌داون → قطعه‌های گفتار/مکث (سه شکل نگارش درس‌ها را می‌شناسد) |
| `normalize_fa.py` | نرمال‌سازی فارسی: رقم، نماد ریاضی، نیم‌فاصله، حروف عربی |
| `mms_text.py` | آماده‌سازی متن برای توکنایزر MMS |
| `voices.py` | بک‌اندهای گفتار (Piper، MMS، stub) |
| `build.py` | چرخهٔ کامل: گفتار → یکسان‌سازی نرخ ۲۴k → بلندی صدا → Opus |
| `fetch_voices.py` | دریافت/سبک‌سازی مدل‌ها (فقط در Actions اجرا می‌شود) |

## تنظیم‌ها

* مکث‌ها: کوتاه ۰٫۷۵s، متوسط ۱٫۵s، بلند ۲٫۶s، فاصلهٔ تغییر گوینده ۰٫۳۵s
* `PIPER_LENGTH_SCALE = 1.06` (کمی آهسته‌تر، مناسب آموزش)
* کدگذاری: Opus مونو ۳۲kbps، بلندی هدف `-16 LUFS`
