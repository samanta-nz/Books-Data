# Teaching Template

این پوشه مرجع ساخت فایل‌های آموزش درسی است.

## قانون اصلی

**فقط فایل‌ها و مسیرهایی که واقعاً در پوشه وجود دارند معتبرند.**

- از روی نام یا توضیح موجود در README مسیر جدید حدس نزن.
- اگر فایلی در این README ذکر شده ولی در پوشه وجود ندارد، از آن استفاده نکن.
- هیچ فایل یا پوشه‌ای با نام حدسی نساز.
- قبل از تغییر، ساختار واقعی پوشه را بررسی کن.

---

## فایل‌های اصلی

### قالب مرجع

```text
lesson-template.preview-standalone.html
```

مرجع ظاهر، ساختار صفحه، بخش‌ها، Header، Footer، منوی شناور، محافظ چشم، Quiz و رفتارهای تعاملی.

این فایل برای مشاهده و مقایسهٔ خروجی نهایی است.

---

### نمونهٔ درس ساخته‌شده

```text
ryazif01d01.html
```

نمونهٔ فعلی:

```text
ریاضی نهم
فصل 01
درس 01
```

فایل‌های درس‌های بعدی باید از همین الگوی نام‌گذاری استفاده کنند:

```text
ryazif01d02.html
ryazif01d03.html
ryazif01d04.html
...
```

الگوی عمومی:

```text
ryazif<chapter>d<lesson>.html
```

مثال:

```text
ryazif02d03.html
```

یعنی فصل 02، درس 03.

---

## Theme هر درس

Theme درس اول:

```text
assets/css/theme/ryazif01d01.theme.css
```

برای هر درس جدید یک Theme مستقل با همان نام فایل درس ساخته شود:

```text
assets/css/theme/ryazif01d02.theme.css
assets/css/theme/ryazif01d03.theme.css
...
```

Theme فقط برای موارد قابل تغییر هر درس است، از جمله:

- رنگ‌بندی
- آیکون‌های Header
- نمادهای درس
- Pattern هدر
- Accentها
- رنگ بخش‌ها
- رنگ Footer

---

## فایل‌های LOCKED

این مسیرها **نباید توسط Agent یا ابزار خودکار تغییر کنند**:

```text
assets/css/locked/
assets/js/locked/
```

همچنین فایل زیر مرجع checksum فایل‌های Locked است:

```text
assets/LOCKED.sha256
```

Agent حق اجرای حالت `--update` برای تغییر checksumها را ندارد.

---

## بررسی فایل‌های LOCKED

اسکریپت بررسی:

```text
tools/verify_locked.py
```

بعد از هر تغییر اجرا شود:

```bash
python3 tools/verify_locked.py
```

خروجی صحیح:

```text
OK — all locked files intact
```

اگر خروجی شامل این پیام بود:

```text
LOCKED FILE CHANGED:
```

کار متوقف شود و فایل Locked اصلاح یا جایگزین گردد.

---

## ساخت درس جدید

برای ساخت هر درس:

1. فایل‌های موجود در پوشه را بررسی کن.
2. `lesson-template.preview-standalone.html` را به‌عنوان مرجع ساختار و ظاهر بخوان.
3. نزدیک‌ترین درس تکمیل‌شده مانند `ryazif01d01.html` را نیز بررسی کن.
4. HTML درس جدید را با نام استاندارد بساز.
5. Theme مخصوص همان درس را در `assets/css/theme/` بساز.
6. محتوای آموزشی، فعالیت‌ها، مثال‌ها، تمرین‌ها و Quiz را داخل فایل درس پیاده‌سازی کن.
7. فایل‌های `locked` را تغییر نده.
8. `tools/verify_locked.py` را اجرا کن.
9. فایل‌های ساخته‌شده را در جدول پایین ثبت کن.

---

## فایل‌های تولیدشده

هر فایل جدیدی که ساخته می‌شود باید با **مسیر واقعی** در این جدول اضافه شود.

| درس | فایل HTML | Theme |
|---|---|---|
| ریاضی ۹، فصل 01، درس 01 | `ryazif01d01.html` | `assets/css/theme/ryazif01d01.theme.css` |
| ریاضی ۹، فصل 01، درس 02 | هنگام ساخت ثبت شود | هنگام ساخت ثبت شود |
| ریاضی ۹، فصل 01، درس 03 | هنگام ساخت ثبت شود | هنگام ساخت ثبت شود |

**فایلی که هنوز ساخته نشده نباید با مسیر فرضی به‌عنوان فایل موجود معرفی شود.**

---

## محدودیت Agent

Agent مجاز است:

```text
محتوای درس
HTML اختصاصی درس
Theme اختصاصی درس
SVG / Activity / Quiz اختصاصی همان درس
```

را ایجاد یا ویرایش کند.

Agent مجاز نیست:

```text
assets/css/locked/*
assets/js/locked/*
assets/LOCKED.sha256
```

را تغییر دهد.

---

## معیار تحویل

یک درس زمانی کامل است که:

- فایل HTML واقعی ساخته شده باشد.
- Theme مربوط به آن موجود باشد.
- صفحه در موبایل بدون Overflow نامناسب اجرا شود.
- RTL متن فارسی صحیح باشد.
- فرمول‌ها و نمودارهای لازم درست نمایش داده شوند.
- Activity و Quizهای تعاملی کار کنند.
- لینک‌های داخلی صفحه سالم باشند.
- فایل‌های Locked تغییر نکرده باشند.
- دستور زیر موفق باشد:

```bash
python3 tools/verify_locked.py
```

و در پایان:

```text
OK — all locked files intact
```

نمایش داده شود.

<!-- GENERATED-MATH-PRACTICE -->

## خروجی‌های واقعی مرور و آزمون ریاضی نهم

این فایل‌ها درس مستقل جدید نیستند؛ نام TAB آن‌ها از منوی واقعی اپ حفظ شده است. Theme هر فایل هم‌نام خودش و در مسیر واقعی زیر قرار دارد؛ برای اجرای مستقل آفلاین، همان Theme و فایل‌های قفل‌شده بدون تغییر داخل HTML نیز تعبیه شده‌اند.

| محدوده و کاربرد | HTML واقعی | Theme واقعی |
|---|---|---|
| مرور جامع کل کتاب؛ flash | `../Bucket/Html-files/app/books/C905/N10.1/TAB02.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB02.theme.css` |
| مرور جامع کل کتاب؛ summary | `../Bucket/Html-files/app/books/C905/N10.1/TAB03.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB03.theme.css` |
| مرور جامع کل کتاب؛ sample | `../Bucket/Html-files/app/books/C905/N10.1/TAB04.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB04.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-brilliant-01.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-brilliant-01.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-brilliant-02.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-brilliant-02.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-brilliant-03.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-brilliant-03.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-brilliant-04.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-brilliant-04.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-brilliant-05.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-brilliant-05.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-brilliant-06.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-brilliant-06.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-easy-01.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-easy-01.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-easy-02.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-easy-02.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-easy-03.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-easy-03.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-easy-04.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-easy-04.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-easy-05.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-easy-05.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-easy-06.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-easy-06.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-hard-01.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-hard-01.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-hard-02.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-hard-02.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-hard-03.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-hard-03.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-hard-04.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-hard-04.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-hard-05.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-hard-05.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-hard-06.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-hard-06.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-medium-01.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-medium-01.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-medium-02.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-medium-02.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-medium-03.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-medium-03.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-medium-04.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-medium-04.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-medium-05.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-medium-05.theme.css` |
| مرور جامع کل کتاب؛ final | `../Bucket/Html-files/app/books/C905/N10.1/TAB05-medium-06.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05-medium-06.theme.css` |
| مرور جامع کل کتاب؛ assessment-index | `../Bucket/Html-files/app/books/C905/N10.1/TAB05.html` | `../Bucket/Html-files/app/books/C905/N10.1/assets/css/theme/TAB05.theme.css` |
| فصل اول: مجموعه‌ها؛ flash | `../Bucket/Html-files/app/books/C905/N2.5/TAB02.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB02.theme.css` |
| فصل اول: مجموعه‌ها؛ summary | `../Bucket/Html-files/app/books/C905/N2.5/TAB03.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB03.theme.css` |
| فصل اول: مجموعه‌ها؛ sample | `../Bucket/Html-files/app/books/C905/N2.5/TAB04.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB04.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-brilliant-01.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-brilliant-01.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-brilliant-02.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-brilliant-02.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-brilliant-03.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-brilliant-03.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-brilliant-04.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-brilliant-04.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-brilliant-05.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-brilliant-05.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-brilliant-06.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-brilliant-06.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-easy-01.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-easy-01.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-easy-02.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-easy-02.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-easy-03.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-easy-03.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-easy-04.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-easy-04.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-easy-05.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-easy-05.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-easy-06.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-easy-06.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-hard-01.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-hard-01.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-hard-02.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-hard-02.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-hard-03.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-hard-03.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-hard-04.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-hard-04.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-hard-05.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-hard-05.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-hard-06.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-hard-06.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-medium-01.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-medium-01.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-medium-02.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-medium-02.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-medium-03.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-medium-03.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-medium-04.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-medium-04.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-medium-05.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-medium-05.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment | `../Bucket/Html-files/app/books/C905/N2.5/TAB05-medium-06.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05-medium-06.theme.css` |
| فصل اول: مجموعه‌ها؛ assessment-index | `../Bucket/Html-files/app/books/C905/N2.5/TAB05.html` | `../Bucket/Html-files/app/books/C905/N2.5/assets/css/theme/TAB05.theme.css` |
| فصل ۲: عددهای حقیقی؛ flash | `../Bucket/Html-files/app/books/C905/N3.4/TAB02.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB02.theme.css` |
| فصل ۲: عددهای حقیقی؛ summary | `../Bucket/Html-files/app/books/C905/N3.4/TAB03.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB03.theme.css` |
| فصل ۲: عددهای حقیقی؛ sample | `../Bucket/Html-files/app/books/C905/N3.4/TAB04.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB04.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-brilliant-01.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-brilliant-01.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-brilliant-02.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-brilliant-02.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-brilliant-03.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-brilliant-03.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-brilliant-04.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-brilliant-04.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-brilliant-05.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-brilliant-05.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-brilliant-06.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-brilliant-06.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-easy-01.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-easy-01.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-easy-02.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-easy-02.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-easy-03.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-easy-03.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-easy-04.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-easy-04.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-easy-05.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-easy-05.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-easy-06.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-easy-06.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-hard-01.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-hard-01.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-hard-02.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-hard-02.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-hard-03.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-hard-03.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-hard-04.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-hard-04.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-hard-05.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-hard-05.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-hard-06.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-hard-06.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-medium-01.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-medium-01.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-medium-02.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-medium-02.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-medium-03.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-medium-03.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-medium-04.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-medium-04.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-medium-05.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-medium-05.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment | `../Bucket/Html-files/app/books/C905/N3.4/TAB05-medium-06.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05-medium-06.theme.css` |
| فصل ۲: عددهای حقیقی؛ assessment-index | `../Bucket/Html-files/app/books/C905/N3.4/TAB05.html` | `../Bucket/Html-files/app/books/C905/N3.4/assets/css/theme/TAB05.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ flash | `../Bucket/Html-files/app/books/C905/N4.6/TAB02.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB02.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ summary | `../Bucket/Html-files/app/books/C905/N4.6/TAB03.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB03.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ sample | `../Bucket/Html-files/app/books/C905/N4.6/TAB04.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB04.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-brilliant-01.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-brilliant-01.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-brilliant-02.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-brilliant-02.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-brilliant-03.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-brilliant-03.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-brilliant-04.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-brilliant-04.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-brilliant-05.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-brilliant-05.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-brilliant-06.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-brilliant-06.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-easy-01.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-easy-01.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-easy-02.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-easy-02.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-easy-03.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-easy-03.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-easy-04.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-easy-04.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-easy-05.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-easy-05.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-easy-06.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-easy-06.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-hard-01.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-hard-01.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-hard-02.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-hard-02.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-hard-03.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-hard-03.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-hard-04.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-hard-04.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-hard-05.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-hard-05.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-hard-06.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-hard-06.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-medium-01.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-medium-01.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-medium-02.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-medium-02.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-medium-03.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-medium-03.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-medium-04.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-medium-04.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-medium-05.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-medium-05.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment | `../Bucket/Html-files/app/books/C905/N4.6/TAB05-medium-06.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05-medium-06.theme.css` |
| فصل ۳: استدلال و اثبات در هندسه؛ assessment-index | `../Bucket/Html-files/app/books/C905/N4.6/TAB05.html` | `../Bucket/Html-files/app/books/C905/N4.6/assets/css/theme/TAB05.theme.css` |
| فصل ۴: توان و ریشه؛ flash | `../Bucket/Html-files/app/books/C905/N5.5/TAB02.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB02.theme.css` |
| فصل ۴: توان و ریشه؛ summary | `../Bucket/Html-files/app/books/C905/N5.5/TAB03.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB03.theme.css` |
| فصل ۴: توان و ریشه؛ sample | `../Bucket/Html-files/app/books/C905/N5.5/TAB04.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB04.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-brilliant-01.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-brilliant-01.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-brilliant-02.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-brilliant-02.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-brilliant-03.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-brilliant-03.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-brilliant-04.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-brilliant-04.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-brilliant-05.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-brilliant-05.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-brilliant-06.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-brilliant-06.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-easy-01.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-easy-01.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-easy-02.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-easy-02.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-easy-03.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-easy-03.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-easy-04.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-easy-04.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-easy-05.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-easy-05.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-easy-06.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-easy-06.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-hard-01.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-hard-01.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-hard-02.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-hard-02.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-hard-03.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-hard-03.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-hard-04.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-hard-04.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-hard-05.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-hard-05.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-hard-06.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-hard-06.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-medium-01.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-medium-01.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-medium-02.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-medium-02.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-medium-03.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-medium-03.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-medium-04.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-medium-04.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-medium-05.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-medium-05.theme.css` |
| فصل ۴: توان و ریشه؛ assessment | `../Bucket/Html-files/app/books/C905/N5.5/TAB05-medium-06.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05-medium-06.theme.css` |
| فصل ۴: توان و ریشه؛ assessment-index | `../Bucket/Html-files/app/books/C905/N5.5/TAB05.html` | `../Bucket/Html-files/app/books/C905/N5.5/assets/css/theme/TAB05.theme.css` |
| فصل ۵: عبارت‌های جبری؛ flash | `../Bucket/Html-files/app/books/C905/N6.4/TAB02.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB02.theme.css` |
| فصل ۵: عبارت‌های جبری؛ summary | `../Bucket/Html-files/app/books/C905/N6.4/TAB03.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB03.theme.css` |
| فصل ۵: عبارت‌های جبری؛ sample | `../Bucket/Html-files/app/books/C905/N6.4/TAB04.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB04.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-brilliant-01.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-brilliant-01.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-brilliant-02.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-brilliant-02.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-brilliant-03.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-brilliant-03.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-brilliant-04.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-brilliant-04.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-brilliant-05.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-brilliant-05.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-brilliant-06.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-brilliant-06.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-easy-01.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-easy-01.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-easy-02.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-easy-02.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-easy-03.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-easy-03.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-easy-04.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-easy-04.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-easy-05.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-easy-05.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-easy-06.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-easy-06.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-hard-01.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-hard-01.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-hard-02.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-hard-02.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-hard-03.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-hard-03.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-hard-04.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-hard-04.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-hard-05.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-hard-05.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-hard-06.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-hard-06.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-medium-01.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-medium-01.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-medium-02.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-medium-02.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-medium-03.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-medium-03.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-medium-04.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-medium-04.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-medium-05.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-medium-05.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment | `../Bucket/Html-files/app/books/C905/N6.4/TAB05-medium-06.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05-medium-06.theme.css` |
| فصل ۵: عبارت‌های جبری؛ assessment-index | `../Bucket/Html-files/app/books/C905/N6.4/TAB05.html` | `../Bucket/Html-files/app/books/C905/N6.4/assets/css/theme/TAB05.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ flash | `../Bucket/Html-files/app/books/C905/N7.4/TAB02.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB02.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ summary | `../Bucket/Html-files/app/books/C905/N7.4/TAB03.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB03.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ sample | `../Bucket/Html-files/app/books/C905/N7.4/TAB04.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB04.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-brilliant-01.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-brilliant-01.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-brilliant-02.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-brilliant-02.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-brilliant-03.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-brilliant-03.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-brilliant-04.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-brilliant-04.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-brilliant-05.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-brilliant-05.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-brilliant-06.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-brilliant-06.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-easy-01.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-easy-01.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-easy-02.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-easy-02.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-easy-03.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-easy-03.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-easy-04.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-easy-04.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-easy-05.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-easy-05.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-easy-06.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-easy-06.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-hard-01.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-hard-01.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-hard-02.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-hard-02.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-hard-03.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-hard-03.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-hard-04.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-hard-04.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-hard-05.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-hard-05.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-hard-06.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-hard-06.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-medium-01.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-medium-01.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-medium-02.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-medium-02.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-medium-03.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-medium-03.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-medium-04.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-medium-04.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-medium-05.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-medium-05.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment | `../Bucket/Html-files/app/books/C905/N7.4/TAB05-medium-06.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05-medium-06.theme.css` |
| فصل ۶: خط و معادله‌های خطی؛ assessment-index | `../Bucket/Html-files/app/books/C905/N7.4/TAB05.html` | `../Bucket/Html-files/app/books/C905/N7.4/assets/css/theme/TAB05.theme.css` |
| فصل ۷: عبارت‌های گویا؛ flash | `../Bucket/Html-files/app/books/C905/N8.4/TAB02.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB02.theme.css` |
| فصل ۷: عبارت‌های گویا؛ summary | `../Bucket/Html-files/app/books/C905/N8.4/TAB03.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB03.theme.css` |
| فصل ۷: عبارت‌های گویا؛ sample | `../Bucket/Html-files/app/books/C905/N8.4/TAB04.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB04.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-brilliant-01.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-brilliant-01.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-brilliant-02.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-brilliant-02.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-brilliant-03.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-brilliant-03.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-brilliant-04.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-brilliant-04.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-brilliant-05.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-brilliant-05.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-brilliant-06.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-brilliant-06.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-easy-01.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-easy-01.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-easy-02.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-easy-02.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-easy-03.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-easy-03.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-easy-04.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-easy-04.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-easy-05.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-easy-05.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-easy-06.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-easy-06.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-hard-01.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-hard-01.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-hard-02.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-hard-02.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-hard-03.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-hard-03.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-hard-04.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-hard-04.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-hard-05.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-hard-05.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-hard-06.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-hard-06.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-medium-01.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-medium-01.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-medium-02.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-medium-02.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-medium-03.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-medium-03.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-medium-04.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-medium-04.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-medium-05.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-medium-05.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment | `../Bucket/Html-files/app/books/C905/N8.4/TAB05-medium-06.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05-medium-06.theme.css` |
| فصل ۷: عبارت‌های گویا؛ assessment-index | `../Bucket/Html-files/app/books/C905/N8.4/TAB05.html` | `../Bucket/Html-files/app/books/C905/N8.4/assets/css/theme/TAB05.theme.css` |
| فصل ۸: حجم و مساحت؛ flash | `../Bucket/Html-files/app/books/C905/N9.4/TAB02.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB02.theme.css` |
| فصل ۸: حجم و مساحت؛ summary | `../Bucket/Html-files/app/books/C905/N9.4/TAB03.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB03.theme.css` |
| فصل ۸: حجم و مساحت؛ sample | `../Bucket/Html-files/app/books/C905/N9.4/TAB04.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB04.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-brilliant-01.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-brilliant-01.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-brilliant-02.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-brilliant-02.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-brilliant-03.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-brilliant-03.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-brilliant-04.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-brilliant-04.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-brilliant-05.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-brilliant-05.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-brilliant-06.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-brilliant-06.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-easy-01.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-easy-01.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-easy-02.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-easy-02.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-easy-03.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-easy-03.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-easy-04.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-easy-04.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-easy-05.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-easy-05.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-easy-06.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-easy-06.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-hard-01.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-hard-01.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-hard-02.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-hard-02.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-hard-03.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-hard-03.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-hard-04.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-hard-04.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-hard-05.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-hard-05.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-hard-06.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-hard-06.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-medium-01.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-medium-01.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-medium-02.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-medium-02.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-medium-03.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-medium-03.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-medium-04.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-medium-04.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-medium-05.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-medium-05.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment | `../Bucket/Html-files/app/books/C905/N9.4/TAB05-medium-06.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05-medium-06.theme.css` |
| فصل ۸: حجم و مساحت؛ assessment-index | `../Bucket/Html-files/app/books/C905/N9.4/TAB05.html` | `../Bucket/Html-files/app/books/C905/N9.4/assets/css/theme/TAB05.theme.css` |
