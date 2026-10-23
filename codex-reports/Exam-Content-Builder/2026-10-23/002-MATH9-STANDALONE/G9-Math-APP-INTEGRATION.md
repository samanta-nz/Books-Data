# راهنمای کامل اتصال HTMLهای ریاضی نهم به اپ

این فایل مرجع یکپارچهٔ تحویل است: قرارداد اتصال، مدل ثبت پاسخ و خطا و نتیجه، جدول تمام فایل‌ها و متن اسکریپت‌های واقعی داخل HTMLها در همین راهنما آمده‌اند. این فایل در رابط دانش‌آموز نمایش داده نمی‌شود.

## وضعیت تحویل و اجرای مستقل

۲۵۲ HTML، هشت فصل و مرور کل کتاب، ۲۱۶ آزمون مستقل، ۴۱۱ سؤال مرجع و ۱۹۰ کارت مرجع موجود است. **CSS، فونت‌ها، تم و JavaScript داخل HTML هستند؛ هیچ CSS یا JS جانبی برای اجرا لازم نیست.** فایل CSS مجزا حذف شده است؛ block `style[data-page-theme="embedded"]` تم همان فایل را دارد. appendices این راهنما نسخهٔ مرجع اسکریپت‌های موجودند؛ آن‌ها را دوباره به صفحه تزریق نکنید.

ریشهٔ ریپو `grades/g09/Bucket/Content/G09/g9-math/` است. کلید باکت از حذف `grades/g09/` حاصل می‌شود. بزرگ/کوچک بودن `Bucket/Content/G09`، `F01..F08`، `ALL` و `Hits` دقیق است. چهار سطح `easy/medium/hard/brilliant` و شش نسخه در `selftest/` هر محدوده موجودند. ۲۱۶ لینک نسبی فهرست به همان فایل‌های واقعی اشاره می‌کنند؛ فایل EX یا تدریس/PDF ساختگی اضافه نشده است.

منبع علمی از کامیت `2a19ac65bbc79f4ce21647c9bf463c6662f82b5b` ریپوی https://github.com/samanta-nz/Books-Data حفظ شده است. مسیرهای جدید در شاخه `migration/modular-grades` ریپوی https://github.com/samanta-nz/com.hamyareman.final قرار دارند. هیچ backend یا API تازه‌ای تعریف نشده است.

## رابط JavaScript موجود اپ

اپ باید `window.Hamyar` را **پیش از اجرای اسکریپت یادگیری داخل HTML** برقرار کند. runtime در شروع، reference آن را نگه می‌دارد؛ اضافه‌کردن bridge پس از اجرای موتور، اتصال آن تلاش را به‌صورت خودکار تصحیح نمی‌کند. از APIهای موجود Android استفاده شود و ورودی فقط از مسیرهای مورد اعتماد همین کتاب پذیرفته شود.

| متد واقعی | ورودی/خروجی | نقش |
|---|---|---|
| `loadState(): String` | JSON ذخیره‌شده یا رشتهٔ خالی | بارگذاری state پیش از نمایش |
| `saveState(json: String): Unit` | تمام JSON ریشه | ذخیرهٔ پیش‌نویس، پاسخ‌ها، خطاها و تاریخچه |
| `recordItem(itemId: String, correct: Boolean): Unit` | شناسه و درستی پاسخ | ثبت عملکرد و مرور فلش‌کارت در مسیر فعلی اپ |
| `recordExam(scorePct: Int, total: Int, correctCount: Int, wrongCsv: String): Unit` | درصد، تعداد سؤال اصلی، تعداد کاملاً صحیح و شناسه‌های غلط | دفتر آزمون و progress |

امضاها در `apps/student/src/main/java/com/hamyareman/ir/ui/study/MathHtmlWebView.kt` و class موجود `HamyarHtmlBridge` هستند. `recordItem` به `StudyProgressRepository.recordExercise` و برای kind=flash به `reviewCardMath` می‌رود؛ `recordExam` از `recordHtmlExam` استفاده می‌کند. خطاهای جزئی با metadata کامل در JSON `saveState` هستند؛ CSV آزمون جای JSON خطاها را نمی‌گیرد.

`saveState` و `recordExam` void هستند؛ موفق‌بودن فراخوانی JavaScript رسید durable/backend نیست. runtime فقط عدم exception را می‌بیند. صحت ذخیره باید در آزمون native با `loadState`/بازگشت به صفحه و بررسی store/ledger ثابت شود. هیچ رسید ساختگی یا API ack فرضی اضافه نشود.

## مسیر واقعی ذخیره در شاخهٔ فعلی اپ

مبنای بررسی کد این تحویل `ae74d61bc540aa03a2683604d4d841645d04c3c1` است. در این نسخه:

- `LocalStore` حساب و مهمان را جدا می‌کند؛ owner خالی از `<storeName>__guest` و حساب از `<storeName>__<StableIds.of("user",owner)>` استفاده می‌کند. legacy فقط با owner معلوم و غیرخالی مهاجرت می‌شود.
- `HamyarHtmlBridge`، owner را هنگام ساخت می‌بندد، grade را کنترل و از کلید **`html:g09:<kind>:<packId>`** استفاده می‌کند. legacy همان store با کلید `html:<kind>:<packId>` را در صورت نبود مقصد می‌خواند.
- اجرای اختصاصی ریاضی از store=`hamyar_math_html` و هویت آموزشی pack/kind استفاده می‌کند.
- **RemoteHtmlPage فعلی** در `BookNodeScreen.kt` از store=`hamyar_remote_html`، kind=`document` و packId برابر `LessonCache.keyOf(url)` یعنی SHA-256 URL استفاده می‌کند. در navigation نسبی باید binding صفحهٔ مقصد و محل ذخیره با دقت بررسی شود.
- مهاجرت خودکار بین دو store بالا، بین URL قدیمی و جدید یا بین kind=document و kind=exam از صرف حفظ JSON/شناسهٔ HTML حاصل نمی‌شود. این تحویل کد Kotlin را تغییر نداده است؛ ثبت نتایج و انتقال دادهٔ قدیمی در اپ نصب‌شده تأیید نشده است.

برای اتصال آموزشی، توسعهٔ اپ باید قبل از load هر سند، URL مجاز را با جدول پایین/manifest به `packId` و `kind` واقعی متصل کند و از class/store موجود استفاده کند. الگوی زیر **راهنمای استفاده از class واقعی است و در این تحویل در سورس native اعمال نشده**:

```kotlin
val store = LocalStore(context, "hamyar_math_html")
webView.addJavascriptInterface(
    HamyarHtmlBridge(context.applicationContext, packId, kind, store, progress),
    "Hamyar"
)
// packId و kind از manifest همین فایل، پیش از اجرای موتور HTML تعیین شوند.
```

باید تمام navigationهای مورد اعتماد، تغییر حساب، native ledger و حفظ اطلاعات موجود بررسی شوند. برای اصلاح، backend تازه، store حدسی یا حذف دادهٔ قدیمی نسازید؛ سیاست مهاجرت را با دادهٔ آزمایشی و قرارداد موجود طراحی و گزارش کنید. مسیرهای `html:g09:...` با تبدیل ارقام نمایشی یا تغییر نام فایل تغییر نکنند.

## دادهٔ هر صفحه و ساختار JSON

`script#practice-data` دادهٔ همان فایل است؛ از نام مسیر یا عنوان برای حدس هویت استفاده نشود. کلیدهای `id`، `scopeId`، `packId`، `kind`، `mode`، `contentVersion` و `variant` هویت و رفتار را تعیین می‌کنند. این تحویل آن‌ها و سؤال/پاسخ‌ها را تغییر نداده است. تغییرات ظاهریِ تم/فلوتر نباید تلاش قدیمی را با کلید جدید دوباره تصحیح کنند.

ریشه schema=`hamyar-math-practice-1` دارد و تمام سندهای همان store در `documents[practiceData.id]` جدا می‌شوند. نمونهٔ زیر فقط fixture خالی با شناسهٔ واقعی یک برگه است؛ دادهٔ دانش‌آموز واقعی نیست:

```json
{
  "schema": "hamyar-math-practice-1",
  "documents": {
    "f00-tab05-easy-01": {
      "contentVersion": "2026-10-19.qa-fix-1",
      "sessionId": "fixture-integration",
      "answers": {},
      "submitted": {},
      "errors": [],
      "history": [],
      "cards": {},
      "cardIndex": 0,
      "currentQuestion": 0,
      "finished": false,
      "examReported": false
    }
  }
}
```

`answers` پاسخ‌های پیش‌نویس؛ `submitted` نتیجهٔ هر سؤال، `errors` رویدادهای خطا، `history` تاریخچهٔ نسخه/تلاش، `cards` و `cardIndex` پیشرفت کارت، `currentQuestion` جایگاه سؤال، `finished` پایان آزمون و `examReported` پرچم ارسال event است. `sessionId` برای جلوگیری از ثبت چندبارهٔ خطای یک سؤال در همان تلاش به کار می‌رود. برای رسم و خودارزیابی، `drawings`، `manualRubrics`، `gradingPolicy` و نتیجهٔ دارای بارم نیز در state ذخیره می‌شوند.

تغییر نسخهٔ علمی با حفظ state قبلی در history انجام می‌شود؛ پاک‌کردن کل store یا تاریخچه برای به‌روزرسانی HTML مجاز فرض نشود. در نبود bridge، fallback صریحاً localStorage مرورگر است؛ این حالت ثبت در اپ معرفی نشود.

## خطای دانش‌آموز و بازخورد

رویداد خطا توسط runtime خود فایل ساخته می‌شود؛ حداقل این فیلدها را بدون حذف/تغییر نگه دارید:

| فیلد | معنی |
|---|---|
| `eventId` | `sessionId + ':' + questionId`، جلوگیری از تکرار همان تلاش |
| `questionId`, `familyId`, `examId`, `sessionId` | شناسهٔ سؤال/هدف مرجع/سند/تلاش |
| `grade`, `book`, `bookCode` | پایه و کتاب؛ C905 |
| `chapter`, `chapterNumber`, `lesson`, `topic` | طبقه‌بندی آموزشی |
| `questionType`, `difficulty` | نوع و سطح |
| `studentAnswer`, `correctAnswer` | پاسخ ثبت‌شده و کلید |
| `recordedAt` | زمان ISO استاندارد |
| `errorCategory` | تشخیص آموزشی احتمالی، بدون ادعای قطعی دربارهٔ ذهن دانش‌آموز |

در خودارزیابی ممکن است `assessmentMethod`، `earnedMarks`، `maximumMarks` و `studentDrawing` نیز وجود داشته باشد. JSON و زمان و ID ماشینی را فارسی‌سازی نکنید؛ تنها نمایش و ورودی کاربر فارسی هستند.

در بانک نمونه‌سؤال، پاسخ غلط همان لحظه زیر همان سؤال، با یک جملهٔ اختصاصی شامل علت احتمالی و مسیر صحیح ظاهر می‌شود. در پاسخ تشریحی تصحیح قطعی ادعا نمی‌شود. `recordItem` این بانک فقط برای بخش‌های خودکار است.

## ترتیب ثبت خودآزمایی و نمرهٔ جامع

۱. هنگام انتخاب/نوشتن پاسخ فقط `saveState` پیش‌نویس انجام می‌شود؛ کلید، feedback، درصد و رویداد نتیجهٔ native نباید پیش از تأیید پایان نمایش/ارسال شود.

۲. آزمون فصل پس از تأیید پایان تصحیح می‌شود؛ برای پاسخ‌های واردشده، `recordItem` و یک `recordExam` با درصد تعداد سؤال‌ها ارسال می‌شود. reload نباید دوباره event پایان بسازد.

۳. برگهٔ جامع شانزده سؤال اصلی، سی‌وهشت بخش، چهار صفحهٔ منطقی و دقیقاً بیست نمره دارد. بیست بخش خودکار و هجده بخش راهنمای تشریحی/خودارزیابی هستند. تا بررسی rubricهای پاسخ‌های دستی و انتخاب «ثبت نتیجه»، event دفتر آزمون ارسال نمی‌شود.

۴. درصد جامع بر مبنای **بارم** است. `recordExam.total=16` تعداد سؤال اصلی است؛ درصد را از `correctCount/16` دوباره محاسبه نکنید. برای مثال نمرهٔ ۱۹٫۵ از ۲۰ به ۹۸٪ گرد می‌شود، حتی اگر تعداد سؤال کاملاً صحیح متفاوت باشد. روش `automatic-and-self-assessment` نیازمند تأیید دبیر است و نباید نمرهٔ قطعی معلم نامیده شود.

۵. شناسهٔ item آزمون فصل `D.id + '_' + q.id` است؛ برگهٔ جامع eventهای سؤال اصلی با `D.id + '_final-q' + NN` و flash با شناسهٔ کارت گزارش می‌شوند. wrongCsv همین شناسه‌های event را دارد؛ معادل questionId بخش‌های JSON نیست.

## منوی شناور تمام‌اندازه در WebView

CSS و JavaScript افزودهٔ همین تحویل، `#fab.open` و `#fab-panel` را به تمام viewport محتوای WebView گسترش می‌دهند؛ safe-area، اسکرول داخلی، دکمهٔ بستن، Escape، تلهٔ Tab و inert شدن محتوای پشت پنجره رعایت شده است. قفل‌های قالب مرجع دست‌نخورده‌اند؛ override در `style[data-webview-floater]` و رفتار مکمل در `script[data-webview-floater]` است.

اپ باید **خود WebView را با فضای محتوای صفحه اندازه دهد** و HTML را داخل Dialog کوچک native قرار ندهد. CSS نمی‌تواند اندازهٔ parent اندروید یا نوارهای سیستم را بزرگ کند. AndroidView/Compose میزبان باید از اندازهٔ محتوای کامل، مانند modifier.fillMaxSize موجود، استفاده کند؛ تغییر native در این تحویل انجام نشده است.

برای Back سخت‌افزاری، ابتدا بازبودن پنجره بررسی و دکمهٔ موجود آن کلیک شود؛ اگر باز نبود روال Back فعلی اپ ادامه یابد. عبارت DOM زیر برای استفاده در hook موجود اپ است و API تازه نیست:

```javascript
(function () {
  var wrap = document.getElementById('fab');
  var button = document.getElementById('fab-btn');
  if (wrap && button && wrap.classList.contains('open')) { button.click(); return true; }
  return false;
})();
```

این hook سخت‌افزاری در Android این تحویل نصب نشده است؛ بستن با دکمه، Escape و لینک فهرست در خود HTML موجود است. تم سیستم نباید پالت ثابت صفحه را عوض کند؛ قابلیت محافظ چشم فقط از کنترل خود دانش‌آموز پیروی می‌کند.

## دانلود، کش، رمزگشایی و آزمون پذیرش اپ

- مسیرهای نسبی `selftest/` باید در HmkWebViewClient/کش به‌عنوان HTML همان کتاب بارگذاری شوند. ۳۶ فایل اصلی در map فعلی اپ وجود دارند؛ ۲۱۶ برگه entry صریح جدا ندارند. نیاز به entry مستقل را مصرف‌کنندهٔ واقعی تعیین کند؛ حدس یا ادعای اجرای آفلاین کافی نیست.
- HTML ساده از مسیر HtmlCodec فعلی پذیرفته می‌شود. فایل‌ها در این تحویل رمزگذاری جدید نشده‌اند و کلیدی ضمیمه نیست. نسخهٔ رمزگذاری‌شده، اگر جداگانه سفارش شود، باید قالب فعلی HMK1/AES-GCM و سقف اندازهٔ واقعی LessonCache را رعایت کند.
- ETag/Last-Modified و تغییر محتوای هم‌اندازه، 304، retry و قطع/ادامه با منطق موجود حفظ شوند. URL جدید cache قدیمی را خودکار معتبر نمی‌کند. حذف گستردهٔ کش یا اطلاعات پاسخ راه‌حل مهاجرت نیست.
- قبل از پذیرش native: حساب A، خروج، مهمان، B، ویرایش مستقل مهمان و بازگشت A؛ بازکردن مجدد برگه و تشخیص اشتباه؛ عدم نتیجهٔ زودهنگام؛ یک‌بار ثبت نتیجه؛ تمام بارم بیست و خودارزیابی؛ مسیر relative و کش آفلاین؛ منوی تمام‌اندازه در portrait/landscape و Back/فوکوس را بررسی کنید.
- تست Chromium با bridge ساختگی، اجرای گوشی یا APK نیست. ثبت native در نصب واقعی و QA مستقل هنوز جداگانه لازم‌اند. merge سورس main، bucket sync زنده یا انتشار APK از این راهنما مجاز فرض نشود.

## جدول هویت تمام فایل‌های واقعی

ستون path نسبت به `grades/g09/Bucket/` است. دادهٔ کامل‌تر و SHA-256 HTML در `math9-layout-manifest.json` کنار همین راهنما آمده است.

| path | document id | packId | kind | mode | contentVersion |
|---|---|---|---|---|---|
| `Content/G09/g9-math/F01/ryazif01-Hits.html` | `f01-tab03` | `C905_E01-SUM` | `summary` | `summary` | `2026-10-18.2` |
| `Content/G09/g9-math/F01/ryazif01-cards.html` | `f01-tab02` | `C905_E01-SUM` | `flash` | `flash` | `2026-10-18.2` |
| `Content/G09/g9-math/F01/ryazif01-Q.html` | `f01-tab04` | `C905_E01-SUM` | `exam` | `sample` | `2026-10-18.2` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-easy-01.html` | `f01-tab05-easy-01` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-easy-02.html` | `f01-tab05-easy-02` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-easy-03.html` | `f01-tab05-easy-03` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-easy-04.html` | `f01-tab05-easy-04` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-easy-05.html` | `f01-tab05-easy-05` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-easy-06.html` | `f01-tab05-easy-06` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-medium-01.html` | `f01-tab05-medium-01` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-medium-02.html` | `f01-tab05-medium-02` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-medium-03.html` | `f01-tab05-medium-03` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-medium-04.html` | `f01-tab05-medium-04` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-medium-05.html` | `f01-tab05-medium-05` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-medium-06.html` | `f01-tab05-medium-06` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-hard-01.html` | `f01-tab05-hard-01` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-hard-02.html` | `f01-tab05-hard-02` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-hard-03.html` | `f01-tab05-hard-03` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-hard-04.html` | `f01-tab05-hard-04` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-hard-05.html` | `f01-tab05-hard-05` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-hard-06.html` | `f01-tab05-hard-06` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-brilliant-01.html` | `f01-tab05-brilliant-01` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-brilliant-02.html` | `f01-tab05-brilliant-02` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-brilliant-03.html` | `f01-tab05-brilliant-03` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-brilliant-04.html` | `f01-tab05-brilliant-04` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-brilliant-05.html` | `f01-tab05-brilliant-05` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/selftest/ryazif01-selftest-brilliant-06.html` | `f01-tab05-brilliant-06` | `C905_E01-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F01/ryazif01-selftest.html` | `f01-tab05` | `C905_E01-SUM` | `exam` | `assessment-index` | `2026-10-18.2` |
| `Content/G09/g9-math/F02/ryazif02-Hits.html` | `f02-tab03` | `C905_E02-SUM` | `summary` | `summary` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F02/ryazif02-cards.html` | `f02-tab02` | `C905_E02-SUM` | `flash` | `flash` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F02/ryazif02-Q.html` | `f02-tab04` | `C905_E02-SUM` | `exam` | `sample` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-easy-01.html` | `f02-tab05-easy-01` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-easy-02.html` | `f02-tab05-easy-02` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-easy-03.html` | `f02-tab05-easy-03` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-easy-04.html` | `f02-tab05-easy-04` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-easy-05.html` | `f02-tab05-easy-05` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-easy-06.html` | `f02-tab05-easy-06` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-medium-01.html` | `f02-tab05-medium-01` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-medium-02.html` | `f02-tab05-medium-02` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-medium-03.html` | `f02-tab05-medium-03` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-medium-04.html` | `f02-tab05-medium-04` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-medium-05.html` | `f02-tab05-medium-05` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-medium-06.html` | `f02-tab05-medium-06` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-hard-01.html` | `f02-tab05-hard-01` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-hard-02.html` | `f02-tab05-hard-02` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-hard-03.html` | `f02-tab05-hard-03` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-hard-04.html` | `f02-tab05-hard-04` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-hard-05.html` | `f02-tab05-hard-05` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-hard-06.html` | `f02-tab05-hard-06` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-brilliant-01.html` | `f02-tab05-brilliant-01` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-brilliant-02.html` | `f02-tab05-brilliant-02` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-brilliant-03.html` | `f02-tab05-brilliant-03` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-brilliant-04.html` | `f02-tab05-brilliant-04` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-brilliant-05.html` | `f02-tab05-brilliant-05` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/selftest/ryazif02-selftest-brilliant-06.html` | `f02-tab05-brilliant-06` | `C905_E02-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F02/ryazif02-selftest.html` | `f02-tab05` | `C905_E02-SUM` | `exam` | `assessment-index` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F03/ryazif03-Hits.html` | `f03-tab03` | `C905_E03-SUM` | `summary` | `summary` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F03/ryazif03-cards.html` | `f03-tab02` | `C905_E03-SUM` | `flash` | `flash` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F03/ryazif03-Q.html` | `f03-tab04` | `C905_E03-SUM` | `exam` | `sample` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-easy-01.html` | `f03-tab05-easy-01` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-easy-02.html` | `f03-tab05-easy-02` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-easy-03.html` | `f03-tab05-easy-03` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-easy-04.html` | `f03-tab05-easy-04` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-easy-05.html` | `f03-tab05-easy-05` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-easy-06.html` | `f03-tab05-easy-06` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-medium-01.html` | `f03-tab05-medium-01` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-medium-02.html` | `f03-tab05-medium-02` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-medium-03.html` | `f03-tab05-medium-03` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-medium-04.html` | `f03-tab05-medium-04` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-medium-05.html` | `f03-tab05-medium-05` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-medium-06.html` | `f03-tab05-medium-06` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-hard-01.html` | `f03-tab05-hard-01` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-hard-02.html` | `f03-tab05-hard-02` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-hard-03.html` | `f03-tab05-hard-03` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-hard-04.html` | `f03-tab05-hard-04` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-hard-05.html` | `f03-tab05-hard-05` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-hard-06.html` | `f03-tab05-hard-06` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-brilliant-01.html` | `f03-tab05-brilliant-01` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-brilliant-02.html` | `f03-tab05-brilliant-02` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-brilliant-03.html` | `f03-tab05-brilliant-03` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-brilliant-04.html` | `f03-tab05-brilliant-04` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-brilliant-05.html` | `f03-tab05-brilliant-05` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/selftest/ryazif03-selftest-brilliant-06.html` | `f03-tab05-brilliant-06` | `C905_E03-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F03/ryazif03-selftest.html` | `f03-tab05` | `C905_E03-SUM` | `exam` | `assessment-index` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F04/ryazif04-Hits.html` | `f04-tab03` | `C905_E04-SUM` | `summary` | `summary` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F04/ryazif04-cards.html` | `f04-tab02` | `C905_E04-SUM` | `flash` | `flash` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F04/ryazif04-Q.html` | `f04-tab04` | `C905_E04-SUM` | `exam` | `sample` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-easy-01.html` | `f04-tab05-easy-01` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-easy-02.html` | `f04-tab05-easy-02` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-easy-03.html` | `f04-tab05-easy-03` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-easy-04.html` | `f04-tab05-easy-04` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-easy-05.html` | `f04-tab05-easy-05` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-easy-06.html` | `f04-tab05-easy-06` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-medium-01.html` | `f04-tab05-medium-01` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-medium-02.html` | `f04-tab05-medium-02` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-medium-03.html` | `f04-tab05-medium-03` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-medium-04.html` | `f04-tab05-medium-04` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-medium-05.html` | `f04-tab05-medium-05` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-medium-06.html` | `f04-tab05-medium-06` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-hard-01.html` | `f04-tab05-hard-01` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-hard-02.html` | `f04-tab05-hard-02` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-hard-03.html` | `f04-tab05-hard-03` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-hard-04.html` | `f04-tab05-hard-04` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-hard-05.html` | `f04-tab05-hard-05` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-hard-06.html` | `f04-tab05-hard-06` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-brilliant-01.html` | `f04-tab05-brilliant-01` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-brilliant-02.html` | `f04-tab05-brilliant-02` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-brilliant-03.html` | `f04-tab05-brilliant-03` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-brilliant-04.html` | `f04-tab05-brilliant-04` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-brilliant-05.html` | `f04-tab05-brilliant-05` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/selftest/ryazif04-selftest-brilliant-06.html` | `f04-tab05-brilliant-06` | `C905_E04-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F04/ryazif04-selftest.html` | `f04-tab05` | `C905_E04-SUM` | `exam` | `assessment-index` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F05/ryazif05-Hits.html` | `f05-tab03` | `C905_E05-SUM` | `summary` | `summary` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F05/ryazif05-cards.html` | `f05-tab02` | `C905_E05-SUM` | `flash` | `flash` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F05/ryazif05-Q.html` | `f05-tab04` | `C905_E05-SUM` | `exam` | `sample` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-easy-01.html` | `f05-tab05-easy-01` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-easy-02.html` | `f05-tab05-easy-02` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-easy-03.html` | `f05-tab05-easy-03` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-easy-04.html` | `f05-tab05-easy-04` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-easy-05.html` | `f05-tab05-easy-05` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-easy-06.html` | `f05-tab05-easy-06` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-medium-01.html` | `f05-tab05-medium-01` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-medium-02.html` | `f05-tab05-medium-02` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-medium-03.html` | `f05-tab05-medium-03` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-medium-04.html` | `f05-tab05-medium-04` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-medium-05.html` | `f05-tab05-medium-05` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-medium-06.html` | `f05-tab05-medium-06` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-hard-01.html` | `f05-tab05-hard-01` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-hard-02.html` | `f05-tab05-hard-02` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-hard-03.html` | `f05-tab05-hard-03` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-hard-04.html` | `f05-tab05-hard-04` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-hard-05.html` | `f05-tab05-hard-05` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-hard-06.html` | `f05-tab05-hard-06` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-brilliant-01.html` | `f05-tab05-brilliant-01` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-brilliant-02.html` | `f05-tab05-brilliant-02` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-brilliant-03.html` | `f05-tab05-brilliant-03` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-brilliant-04.html` | `f05-tab05-brilliant-04` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-brilliant-05.html` | `f05-tab05-brilliant-05` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/selftest/ryazif05-selftest-brilliant-06.html` | `f05-tab05-brilliant-06` | `C905_E05-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F05/ryazif05-selftest.html` | `f05-tab05` | `C905_E05-SUM` | `exam` | `assessment-index` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F06/ryazif06-Hits.html` | `f06-tab03` | `C905_E06-SUM` | `summary` | `summary` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F06/ryazif06-cards.html` | `f06-tab02` | `C905_E06-SUM` | `flash` | `flash` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F06/ryazif06-Q.html` | `f06-tab04` | `C905_E06-SUM` | `exam` | `sample` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-easy-01.html` | `f06-tab05-easy-01` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-easy-02.html` | `f06-tab05-easy-02` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-easy-03.html` | `f06-tab05-easy-03` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-easy-04.html` | `f06-tab05-easy-04` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-easy-05.html` | `f06-tab05-easy-05` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-easy-06.html` | `f06-tab05-easy-06` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-medium-01.html` | `f06-tab05-medium-01` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-medium-02.html` | `f06-tab05-medium-02` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-medium-03.html` | `f06-tab05-medium-03` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-medium-04.html` | `f06-tab05-medium-04` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-medium-05.html` | `f06-tab05-medium-05` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-medium-06.html` | `f06-tab05-medium-06` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-hard-01.html` | `f06-tab05-hard-01` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-hard-02.html` | `f06-tab05-hard-02` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-hard-03.html` | `f06-tab05-hard-03` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-hard-04.html` | `f06-tab05-hard-04` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-hard-05.html` | `f06-tab05-hard-05` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-hard-06.html` | `f06-tab05-hard-06` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-brilliant-01.html` | `f06-tab05-brilliant-01` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-brilliant-02.html` | `f06-tab05-brilliant-02` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-brilliant-03.html` | `f06-tab05-brilliant-03` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-brilliant-04.html` | `f06-tab05-brilliant-04` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-brilliant-05.html` | `f06-tab05-brilliant-05` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/selftest/ryazif06-selftest-brilliant-06.html` | `f06-tab05-brilliant-06` | `C905_E06-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F06/ryazif06-selftest.html` | `f06-tab05` | `C905_E06-SUM` | `exam` | `assessment-index` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F07/ryazif07-Hits.html` | `f07-tab03` | `C905_E07-SUM` | `summary` | `summary` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F07/ryazif07-cards.html` | `f07-tab02` | `C905_E07-SUM` | `flash` | `flash` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F07/ryazif07-Q.html` | `f07-tab04` | `C905_E07-SUM` | `exam` | `sample` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-easy-01.html` | `f07-tab05-easy-01` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-easy-02.html` | `f07-tab05-easy-02` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-easy-03.html` | `f07-tab05-easy-03` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-easy-04.html` | `f07-tab05-easy-04` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-easy-05.html` | `f07-tab05-easy-05` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-easy-06.html` | `f07-tab05-easy-06` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-medium-01.html` | `f07-tab05-medium-01` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-medium-02.html` | `f07-tab05-medium-02` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-medium-03.html` | `f07-tab05-medium-03` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-medium-04.html` | `f07-tab05-medium-04` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-medium-05.html` | `f07-tab05-medium-05` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-medium-06.html` | `f07-tab05-medium-06` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-hard-01.html` | `f07-tab05-hard-01` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-hard-02.html` | `f07-tab05-hard-02` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-hard-03.html` | `f07-tab05-hard-03` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-hard-04.html` | `f07-tab05-hard-04` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-hard-05.html` | `f07-tab05-hard-05` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-hard-06.html` | `f07-tab05-hard-06` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-brilliant-01.html` | `f07-tab05-brilliant-01` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-brilliant-02.html` | `f07-tab05-brilliant-02` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-brilliant-03.html` | `f07-tab05-brilliant-03` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-brilliant-04.html` | `f07-tab05-brilliant-04` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-brilliant-05.html` | `f07-tab05-brilliant-05` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/selftest/ryazif07-selftest-brilliant-06.html` | `f07-tab05-brilliant-06` | `C905_E07-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F07/ryazif07-selftest.html` | `f07-tab05` | `C905_E07-SUM` | `exam` | `assessment-index` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F08/ryazif08-Hits.html` | `f08-tab03` | `C905_E08-SUM` | `summary` | `summary` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F08/ryazif08-cards.html` | `f08-tab02` | `C905_E08-SUM` | `flash` | `flash` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F08/ryazif08-Q.html` | `f08-tab04` | `C905_E08-SUM` | `exam` | `sample` | `2026-10-18.book-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-easy-01.html` | `f08-tab05-easy-01` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-easy-02.html` | `f08-tab05-easy-02` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-easy-03.html` | `f08-tab05-easy-03` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-easy-04.html` | `f08-tab05-easy-04` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-easy-05.html` | `f08-tab05-easy-05` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-easy-06.html` | `f08-tab05-easy-06` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-medium-01.html` | `f08-tab05-medium-01` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-medium-02.html` | `f08-tab05-medium-02` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-medium-03.html` | `f08-tab05-medium-03` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-medium-04.html` | `f08-tab05-medium-04` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-medium-05.html` | `f08-tab05-medium-05` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-medium-06.html` | `f08-tab05-medium-06` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-hard-01.html` | `f08-tab05-hard-01` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-hard-02.html` | `f08-tab05-hard-02` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-hard-03.html` | `f08-tab05-hard-03` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-hard-04.html` | `f08-tab05-hard-04` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-hard-05.html` | `f08-tab05-hard-05` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-hard-06.html` | `f08-tab05-hard-06` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-brilliant-01.html` | `f08-tab05-brilliant-01` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-brilliant-02.html` | `f08-tab05-brilliant-02` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-brilliant-03.html` | `f08-tab05-brilliant-03` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-brilliant-04.html` | `f08-tab05-brilliant-04` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-brilliant-05.html` | `f08-tab05-brilliant-05` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/selftest/ryazif08-selftest-brilliant-06.html` | `f08-tab05-brilliant-06` | `C905_E08-SUM` | `exam` | `assessment` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/F08/ryazif08-selftest.html` | `f08-tab05` | `C905_E08-SUM` | `exam` | `assessment-index` | `2026-10-18.book-1` |
| `Content/G09/g9-math/ALL/ryazi-all-Hits.html` | `f00-tab03` | `C905_E00-SUM` | `summary` | `summary` | `2026-10-18.book-1` |
| `Content/G09/g9-math/ALL/ryazi-all-cards.html` | `f00-tab02` | `C905_E00-SUM` | `flash` | `flash` | `2026-10-18.book-1` |
| `Content/G09/g9-math/ALL/ryazi-all-Q.html` | `f00-tab04` | `C905_E00-SUM` | `exam` | `sample` | `2026-10-18.book-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-easy-01.html` | `f00-tab05-easy-01` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-easy-02.html` | `f00-tab05-easy-02` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-easy-03.html` | `f00-tab05-easy-03` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-easy-04.html` | `f00-tab05-easy-04` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-easy-05.html` | `f00-tab05-easy-05` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-easy-06.html` | `f00-tab05-easy-06` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-medium-01.html` | `f00-tab05-medium-01` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-medium-02.html` | `f00-tab05-medium-02` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-medium-03.html` | `f00-tab05-medium-03` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-medium-04.html` | `f00-tab05-medium-04` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-medium-05.html` | `f00-tab05-medium-05` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-medium-06.html` | `f00-tab05-medium-06` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-hard-01.html` | `f00-tab05-hard-01` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-hard-02.html` | `f00-tab05-hard-02` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-hard-03.html` | `f00-tab05-hard-03` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-hard-04.html` | `f00-tab05-hard-04` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-hard-05.html` | `f00-tab05-hard-05` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-hard-06.html` | `f00-tab05-hard-06` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-brilliant-01.html` | `f00-tab05-brilliant-01` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-brilliant-02.html` | `f00-tab05-brilliant-02` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-brilliant-03.html` | `f00-tab05-brilliant-03` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-brilliant-04.html` | `f00-tab05-brilliant-04` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-brilliant-05.html` | `f00-tab05-brilliant-05` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/selftest/ryazi-all-selftest-brilliant-06.html` | `f00-tab05-brilliant-06` | `C905_E00-SUM` | `exam` | `final` | `2026-10-19.qa-fix-1` |
| `Content/G09/g9-math/ALL/ryazi-all-selftest.html` | `f00-tab05` | `C905_E00-SUM` | `exam` | `assessment-index` | `2026-10-18.book-1` |

## متن کامل اسکریپت‌های واقعی داخل HTMLها

این پیوست‌ها برای بازبینی و بازیابی قرارداد هستند؛ موتور HTML از پیش آن‌ها را دارد. اسکریپت plain-text مجوز فونت و JSON اختصاصی هر صفحه در این پیوست تکرار نشده‌اند؛ مجوزها داخل هر HTML حفظ شده‌اند. hash بر اساس متن دقیق block داخل HTML است. دادهٔ JSON صفحه باید قبل از موتور اصلی موجود باشد و HamyarFinal در برگه‌های جامع قبل از موتور مشترک بارگذاری شود. ترتیب دقیق هر فایل موجود، مرجع نهایی است.

### پیوست 1 — ابزار موجود قالب / مقداردهی اولیه

تعداد استفاده: `252`؛ SHA-256: `11e36e09413ed2d1fa7a45776a805b33d0ce2250ae735ef3f360e411042b0711`.

```javascript
try{var e=localStorage.getItem('lesson-eye-level');document.documentElement.setAttribute('data-eye',/^[0-3]$/.test(e||'')?e:'2')}catch(x){document.documentElement.setAttribute('data-eye','2')}
```

### پیوست 2 — ابزار موجود قالب / مقداردهی اولیه

تعداد استفاده: `252`؛ SHA-256: `65496954fa8cbebc95a402cb1b49430797cb12cc60289266365bf2d9a22d2799`.

```javascript
/* LOCKED FILE — DO NOT EDIT (humans-only). Section: floater + eye-care + progress + scroll-spy */
(function(){
  'use strict';
  var d=document,root=d.documentElement;
  var fa=function(v){return String(v).replace(/[0-9]/g,function(x){return '۰۱۲۳۴۵۶۷۸۹'[+x];});};
  var store={get:function(k){try{return localStorage.getItem(k);}catch(e){return null;}},set:function(k,v){try{localStorage.setItem(k,v);}catch(e){}}};

  /* ---- eye-care (default level 2 = strong) ---- */
  var KEY='lesson-eye-level';
  function setEye(l){
    root.setAttribute('data-eye',l);store.set(KEY,l);
    d.querySelectorAll('[data-eye-set]').forEach(function(b){b.setAttribute('aria-pressed',String(b.getAttribute('data-eye-set')===String(l)));});
  }
  var saved=store.get(KEY);setEye(/^[0-3]$/.test(saved||'')?saved:'2');
  d.querySelectorAll('[data-eye-set]').forEach(function(b){b.addEventListener('click',function(){setEye(b.getAttribute('data-eye-set'));});});

  /* ---- floater open/close ---- */
  var wrap=d.getElementById('fab'),btn=d.getElementById('fab-btn'),panel=d.getElementById('fab-panel');
  function open(v){wrap.classList.toggle('open',v);btn.setAttribute('aria-expanded',String(v));btn.setAttribute('aria-label',v?'بستن فهرست':'باز کردن فهرست و ابزارها');}
  btn.addEventListener('click',function(e){e.stopPropagation();open(!wrap.classList.contains('open'));});
  d.addEventListener('click',function(e){if(wrap.classList.contains('open')&&!wrap.contains(e.target))open(false);});
  d.addEventListener('keydown',function(e){if(e.key==='Escape'&&wrap.classList.contains('open')){open(false);btn.focus();}});
  panel.querySelectorAll('.fab-toc a').forEach(function(a){a.addEventListener('click',function(){open(false);});});
  var top=d.getElementById('go-top');
  if(top)top.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});open(false);});

  /* ---- progress ring + percent + scroll-spy ---- */
  var links=[].slice.call(d.querySelectorAll('.fab-toc a')),pct=d.getElementById('fab-pct');
  var targets=links.map(function(a){return d.querySelector(a.getAttribute('href'));});
  var tick=false;
  function update(){
    tick=false;
    var h=root.scrollHeight-window.innerHeight,p=h>0?Math.min(100,Math.max(0,Math.round(window.scrollY/h*100))):0;
    wrap.style.setProperty('--p',p);if(pct)pct.textContent=fa(p)+'٪';
    var cur=-1,line=window.innerHeight*0.35;
    targets.forEach(function(t,i){if(t&&t.getBoundingClientRect().top<=line)cur=i;});
    links.forEach(function(a,i){if(i===cur)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current');});
  }
  window.addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(update);}},{passive:true});
  window.addEventListener('resize',update);update();
})();

```

### پیوست 3 — ابزار موجود قالب / مقداردهی اولیه

تعداد استفاده: `252`؛ SHA-256: `deec4bdac9a374a8aba01f9be85407695579344a3f07cfaabd5f0bf4a82fd1bc`.

```javascript
document.getElementById('motion-toggle').addEventListener('click',function(e){var stopped=document.body.classList.toggle('no-motion');e.currentTarget.setAttribute('aria-pressed',String(stopped));e.currentTarget.textContent=stopped?'ادامهٔ حرکت‌های تزئینی':'توقف حرکت‌های تزئینی';});document.querySelectorAll('.fab-toc a').forEach(function(a){a.addEventListener('click',function(){var t=document.querySelector(a.getAttribute('href'));for(var p=t;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true;});});
```

### پیوست 4 — موتور مشترک پاسخ و ذخیره

تعداد استفاده: `252`؛ SHA-256: `503023d8bb2714bff4ed560caefc8124adc20d03593283bfd444108f14945c67`.

```javascript
/* Original offline learning engine; uses the existing application Hamyar bridge. */
(function () {
  'use strict';
  const D=JSON.parse(document.getElementById('practice-data').textContent), bridge=window.Hamyar;
  const isExam=D.mode==='assessment';
  const nativeStorage=!!(bridge&&typeof bridge.loadState==='function'&&typeof bridge.saveState==='function');
  const storeKey='hamyar:math:'+(D.scopeId||'f01')+':'+D.kind;
  const fa=n=>String(n).replace(/[0-9٠-٩]/g,x=>'۰۱۲۳۴۵۶۷۸۹'[/[0-9]/.test(x)?Number(x):x.charCodeAt(0)-1632]);
  const byId=id=>document.getElementById(id);
  const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function visible(s){return esc(fa(s)).replace(/⁻?[⁰¹²³⁴⁵⁶⁷⁸⁹]+/g,t=>'<sup>'+[...t].map(x=>x==='⁻'?'−':'۰۱۲۳۴۵۶۷۸۹'['⁰¹²³⁴⁵⁶⁷⁸⁹'.indexOf(x)]).join('')+'</sup>').replace(/[₀-₉]+/g,t=>'<sub>'+[...t].map(x=>'۰۱۲۳۴۵۶۷۸۹'[x.charCodeAt(0)-8320]).join('')+'</sub>');}
  function inputValue(s){return fa(s).replace(/⁻?[⁰¹²³⁴⁵⁶⁷⁸⁹]+/g,t=>'^('+[...t].map(x=>x==='⁻'?'−':'۰۱۲۳۴۵۶۷۸۹'['⁰¹²³⁴⁵⁶⁷⁸⁹'.indexOf(x)]).join('')+')').replace(/[₀-₉]+/g,t=>'_('+[...t].map(x=>'۰۱۲۳۴۵۶۷۸۹'[x.charCodeAt(0)-8320]).join('')+')');}
  function math(s){return String(s).split(/([A-Za-z0-9۰-۹٠-٩ℝℚℤℕ∅∈⊆∩∪−≤≥≠√∛π×÷:^|°²³⁰¹⁴⁵⁶⁷⁸⁹⁻ⁿ₀-₉{}\[\](),.…+*/=<> −-]+)/g).map((x,i)=>{if(i%2===0||!x.trim())return visible(x);if(i%2){const lead=x.match(/^\s*/)[0],trail=x.match(/\s*$/)[0];return visible(lead)+'<bdi dir="ltr" class="math">'+visible(x.trim()).replace(/\^\(([-−]?[۰-۹]+)\)|\^([-−]?[۰-۹]+)/g,(_,a,b)=>'<sup>'+(a||b)+'</sup>')+'</bdi>'+visible(trail);}return visible(x);}).join('');}
  function normalize(s){return String(s).trim().replace(/[۰-۹]/g,d=>String(d.charCodeAt(0)-1776)).replace(/[٠-٩]/g,d=>String(d.charCodeAt(0)-1632)).replace(/٫/g,'.').replace(/،/g,',').replace(/[−–—]/g,'-').replace(/[\s\u200c\u200d]/g,'');}
  function number(s){s=normalize(s);if(!/^[+-]?(?:\d+(?:\.\d+)?|\.\d+)(?:\/[+-]?(?:\d+(?:\.\d+)?|\.\d+))?$/.test(s))return null;const p=s.split('/'),n=Number(p[0])/(p.length===2?Number(p[1]):1);return Number.isFinite(n)&&Math.abs(n)<=1e12?n:null;}
  function set(s){s=normalize(s);if(s==='∅'||s==='{}'||s==='تهی')return [];if(!/^\{[^{}]*\}$/.test(s))return null;const p=s.slice(1,-1).split(',');if(p.some(x=>x===''))return null;const a=p.map(number);if(a.some(x=>x===null))return null;return [...new Set(a)].sort((a,b)=>a-b);}
  function equivalent(q,a){if(q.type==='text')return [q.answer,...(q.aliases||[])].some(x=>normalize(x)===normalize(a));if(q.type==='mcq'||q.type==='tf')return normalize(a)===normalize(q.answer);if(q.type==='set'){const x=set(a),y=set(q.answer);return x!==null&&y!==null&&x.length===y.length&&x.every((n,i)=>Math.abs(n-y[i])<1e-10);}const x=number(a),y=number(q.answer);return x!==null&&y!==null&&Math.abs(x-y)<1e-10;}
  let root={schema:'hamyar-math-practice-1',documents:{}},state,storageMode='memory';
  function sessionId(){return Date.now().toString(36)+'-'+Math.random().toString(36).slice(2,10);}
  function fresh(previous){
    const history=previous&&previous.history?previous.history.slice():[];
    if(previous)history.push({contentVersion:previous.contentVersion,sessionId:previous.sessionId,finishedAt:previous.finishedAt,result:previous.result,answers:previous.answers,submitted:previous.submitted,errors:previous.errors,drawings:previous.drawings,manualRubrics:previous.manualRubrics,gradingPolicy:previous.gradingPolicy});
    return {contentVersion:D.contentVersion,sessionId:sessionId(),answers:{},submitted:{},errors:previous&&previous.errors||[],history,cards:previous&&previous.cards||{},cardIndex:previous&&previous.cardIndex||0,currentQuestion:0,finished:false,examReported:false};
  }
  function load(){let raw='';if(nativeStorage){try{raw=bridge.loadState()||'';}catch(_){}}else{try{raw=localStorage.getItem(storeKey)||'';}catch(_){}}try{const r=JSON.parse(raw);if(r&&r.schema===root.schema&&r.documents)root=r;else if(r&&typeof r==='object'&&!Array.isArray(r))root=Object.assign({},r,{schema:root.schema,documents:{}});}catch(_){}state=root.documents[D.id];if(!state||state.contentVersion!==D.contentVersion)state=fresh(state);root.documents[D.id]=state;}
  function save(){root.documents[D.id]=state;const raw=JSON.stringify(root);let local=false,native=false;if(!nativeStorage){try{localStorage.setItem(storeKey,raw);local=true;}catch(_){}}else{try{bridge.saveState(raw);native=true;}catch(_){}}storageMode=native?'app':local?'browser':'memory';const el=byId('storage-status');if(el)el.textContent=storageMode==='app'?'پاسخ‌ها روی دستگاه، در اپ ذخیره شد.':storageMode==='browser'?'پاسخ‌ها در همین مرورگر ذخیره شد؛ ثبت در اپ در این محیط فعال نیست.':'ذخیرهٔ پایدار در دسترس نیست؛ با بستن صفحه پاسخ‌ها از دست می‌روند.';}
  function item(q,correct){if(bridge&&typeof bridge.recordItem==='function'){try{bridge.recordItem(D.id+'_'+q.id,correct);return true;}catch(_){}}return false;}
  // Diagnose only observable answer patterns; other causes are explicitly tentative.
  function diagnosis(q,a){
    const v=q.verify||{},n=number(a),xs=q.type==='set'?set(a):null;
    const same=ys=>xs!==null&&xs.length===new Set(ys).size&&xs.every(x=>ys.includes(x));
    let cause='احتمالاً در اجرای روش «'+q.objective+'» یکی از شرط‌های سؤال را رعایت نکرده‌ای',category='نیاز به مرور '+q.topic;
    if(q.type==='set'&&xs===null){cause='پاسخ تو به صورت یک مجموعهٔ قابل بررسی نوشته نشده است و باید اعضا را داخل آکولاد، یا مجموعهٔ تهی را با نماد ∅ بنویسی';category='قالب پاسخ مجموعه';}
    else if(q.type==='short'&&n===null){cause='پاسخ تو یک عدد یا کسر معتبر نیست و عبارت محاسباتی باید ابتدا به مقدار عددی تبدیل شود';category='قالب پاسخ عددی';}
    else if(v.op==='card'&&n===v.A.length){cause='عضوهای تکراری را دوباره شمرده‌ای، در حالی که هر مقدار متمایز فقط یک عضو است';category='شمارش عضو تکراری';}
    else if(v.op==='union'&&same(v.A.filter(x=>v.B.includes(x)))){cause='به‌جای اجتماع، فقط عضوهای مشترک را نوشته‌ای و عضوهای مخصوص هر مجموعه را کنار گذاشته‌ای';category='جابه‌جایی اجتماع و اشتراک';}
    else if(v.op==='intersection'&&same([...v.A,...v.B])){cause='به‌جای اشتراک، اجتماع را نوشته‌ای و عضوهایی را پذیرفته‌ای که فقط در یکی از دو مجموعه‌اند';category='جابه‌جایی اشتراک و اجتماع';}
    else if(v.op==='difference'&&same(v.B.filter(x=>!v.A.includes(x)))){cause='جهت تفاضل را برعکس گرفته‌ای و از مجموعهٔ دوم آغاز کرده‌ای';category='جهت تفاضل';}
    else if(v.op==='difference'&&same(v.A.filter(x=>v.B.includes(x)))){cause='عضوهای مشترک را نگه داشته‌ای، در حالی که در تفاضل باید همان عضوها حذف شوند';category='جابه‌جایی تفاضل و اشتراک';}
    else if(v.op==='regions'&&v.what==='union'&&n===v.x+v.y+2*v.z){cause='عضوهای ناحیهٔ مشترک را دو بار شمرده‌ای و یک بار از مجموع دو مجموعه کم نکرده‌ای';category='دوباره‌شماری اشتراک';}
    else if(v.op==='subsets'&&n===v.n){cause='تعداد اعضا را به‌جای تعداد زیرمجموعه‌ها نوشته‌ای و انتخابِ بودن یا نبودن هر عضو را نشمرده‌ای';category='تمایز عضو و زیرمجموعه';}
    else if(q.type==='tf'){cause='ارزش درستی گزاره را برعکس تشخیص داده‌ای و باید آن را با تعریف «'+q.objective+'» بسنجی';}
    else if(q.type==='mcq'){
      const index=q.options.findIndex(o=>normalize(o)===normalize(a));
      const reasons={
        'f01-01':[null,'«جالب» سلیقه‌ای است و معیار عضویت مشخصی به دست نمی‌دهد','تعدادِ سه، بدون تعیین اینکه کدام عددها بزرگ‌اند، اعضا را مشخص نمی‌کند','دلخواه بودنِ شهرها اجازهٔ تعیین یکتای اعضا را نمی‌دهد'],
        'f01-18':[null,'یک مجموعهٔ تک‌عضوی را با عضو داخل آن یکی گرفته‌ای','برای زیرمجموعه بودن باید عددِ داخل آکولاد عضو مستقیم A باشد، اما عضو دوم A خودش یک مجموعه است','نماد زیرمجموعه را برای یک عدد به کار برده‌ای، در حالی که این نماد دو مجموعه را مقایسه می‌کند'],
        'f01-21':[null,'وقتی A تهی باشد، هم شرط و هم نتیجه درست‌اند و مثال نقض به دست نمی‌آید','زوج انتخابی شرط اشتراک تهی را ندارد و نتیجهٔ زیرمجموعه بودن آن هم درست است','دو مجموعهٔ برابرِ ناتهی نه شرط اشتراک تهی را دارند و نه نتیجه را نقض می‌کنند'],
        'f01-33':[null,'جهت تفاضل را برعکس کرده‌ای، در حالی که A−B از اعضای A آغاز می‌شود','اشتراک، عضوهای مشترک را نگه می‌دارد ولی تفاضل همان عضوها را از A حذف می‌کند','اجتماع عضوهای هر دو مجموعه را می‌پذیرد ولی تفاضل فقط عضوهای مخصوص A را می‌خواهد'],
        'f01-53':[null,'تاس استاندارد شش وجه دارد و تعداد وجه‌ها علت نابرابری شانس مجموع‌ها نیست','هر مجموع ممکن دست‌کم یک زوج مرتب مطلوب دارد و احتمال آن صفر نیست','رعایت ترتیب دو تاس حالت‌های متمایز را حفظ می‌کند و آن‌ها را کم نمی‌کند']
      };
      cause=(reasons[q.family]||[])[index]||'گزینهٔ انتخابی تو شرط «'+q.objective+'» را برآورده نمی‌کند';
    }
    if(q.mistakes){const option=Object.keys(q.mistakes).find(x=>normalize(x)===normalize(a));if(option)cause=q.mistakes[option];}
    const guidance=q.feedback.trim().replace(/[.!؟?]+/g,'؛').replace(/[؛\s]+$/,'');
    return {category,sentence:cause+'؛ '+guidance+'؛ پاسخ درست «'+q.answer+'» است.'};
  }
  function recordError(q,a){const id=state.sessionId+':'+q.id;if(state.errors.some(x=>x.eventId===id))return;state.errors.push({eventId:id,questionId:q.id,familyId:q.family,examId:D.id,sessionId:state.sessionId,grade:9,book:'ریاضی نهم',bookCode:'C905',chapter:q.chapter||D.chapterTitle||'فصل اول: مجموعه‌ها',chapterNumber:q.chapterNumber||D.chapterNumber||1,lesson:q.lesson,topic:q.topic,questionType:q.type,difficulty:q.difficulty,studentAnswer:a,correctAnswer:q.answer,recordedAt:new Date().toISOString(),errorCategory:diagnosis(q,a).category});}
  function readAnswer(q){const el=byId('q-'+q.id);if(!el)return state.answers[q.id]||'';if(q.type==='mcq'||q.type==='tf'){const r=el.querySelector('input:checked');return r?r.value:'';}return el.querySelector('input,textarea').value.trim();}
  function inputHTML(q){if(q.type==='mcq'||q.type==='tf'){let opts=q.type==='tf'?['درست','نادرست']:q.options.slice();if(q.type==='mcq'){const k=(D.variant+Number(q.family.split('-').pop()))%opts.length;opts=opts.slice(k).concat(opts.slice(0,k));}return '<fieldset class="choices"><legend class="sr-only">گزینهٔ پاسخ</legend>'+opts.map((o,i)=>'<label class="choice"><input type="radio" name="'+q.id+'" value="'+esc(o)+'"><span><small>'+fa(i+1)+'ـ </small>'+math(o)+'</span></label>').join('')+'</fieldset>';}
    if(q.type==='essay')return '<label for="input-'+q.id+'">پاسخ تشریحی تو</label><textarea id="input-'+q.id+'" rows="4" maxlength="5000"></textarea>';
    return '<label for="input-'+q.id+'">'+(q.type==='set'?'اعضای مجموعه، مانند <bdi dir="ltr">{۲، ۵}</bdi> یا ∅':'پاسخ عددی؛ کسر مانند <bdi dir="ltr">۱/۳</bdi> هم پذیرفته می‌شود')+'</label><input id="input-'+q.id+'" type="text" dir="ltr" autocomplete="off" spellcheck="false" maxlength="500">';
  }
  function diagramMarkup(raw){const template=document.createElement('template');template.innerHTML=raw;const walk=document.createTreeWalker(template.content,NodeFilter.SHOW_TEXT);while(walk.nextNode())walk.currentNode.textContent=fa(walk.currentNode.textContent);template.content.querySelectorAll('[aria-label]').forEach(x=>x.setAttribute('aria-label',fa(x.getAttribute('aria-label'))));return template.innerHTML;}
  function venn(g){return '<figure><svg class="venn" viewBox="0 0 400 210" role="img" aria-label="'+fa(esc('نمودار ون؛ فقط A: '+g.A.join('،')+'؛ مشترک: '+g.both.join('،')+'؛ فقط B: '+g.B.join('،')))+'"><ellipse cx="155" cy="110" rx="110" ry="85" fill="#e8e1f1" stroke="#67518f"/><ellipse cx="245" cy="110" rx="110" ry="85" fill="#dcece7" fill-opacity=".6" stroke="#3a7061"/><text x="95" y="32">A</text><text x="300" y="32">B</text><text x="105" y="112">'+fa(esc(g.A.join('، ')))+'</text><text x="200" y="112">'+fa(esc(g.both.join('، ')))+'</text><text x="295" y="112">'+fa(esc(g.B.join('، ')))+'</text></svg><figcaption>هر عدد در ناحیهٔ مربوط به عضویت خودش قرار دارد.</figcaption></figure>';}
  function cardHTML(q,i,review){return '<article id="q-'+q.id+'" class="question-card"><div class="q-meta"><span>سؤال '+fa(i+1)+' از '+fa(D.questions.length)+'</span><span>'+visible(q.difficulty)+' · '+visible(q.topic)+'</span></div><h2>'+math(q.prompt)+'</h2>'+(q.graphic?venn(q.graphic):'')+(q.diagram?diagramMarkup(q.diagram):'')+inputHTML(q)+(!isExam?'<button type="button" class="submit-answer">'+(q.type==='essay'?'ثبت پاسخ و دیدن راهنما':'ثبت پاسخ')+'</button>':'')+(!isExam||review?'<div class="feedback" role="status" aria-live="polite"></div>':'')+'</article>';}
  function bindQuestion(q){const el=byId('q-'+q.id),value=state.answers[q.id]||'';el.querySelectorAll('input[type=radio]').forEach(r=>r.checked=normalize(r.value)===normalize(value));const input=el.querySelector('input[type=text],textarea');if(input)input.value=inputValue(value);
    el.querySelectorAll('input,textarea').forEach(input=>input.addEventListener('input',()=>{if(state.finished||state.submitted[q.id])return;if(input.type==='text'||input.tagName==='TEXTAREA'){const start=input.selectionStart,end=input.selectionEnd;input.value=inputValue(input.value);input.setSelectionRange(start,end);}state.answers[q.id]=readAnswer(q);save();updateStats();}));
    if(!isExam)el.querySelector('.submit-answer').onclick=()=>submit(q);
    if(!isExam||state.finished)showFeedback(q);
    if(state.finished||state.submitted[q.id])el.querySelectorAll('input,textarea,.submit-answer').forEach(x=>x.disabled=true);
  }
  function showFeedback(q){const entry=state.submitted[q.id],fb=byId('q-'+q.id).querySelector('.feedback');if(!fb)return;
    if(!entry){if(state.finished){fb.className='feedback manual';fb.innerHTML='<strong>بدون پاسخ</strong><p>پاسخ صحیح: '+math(q.answer)+'</p><p>'+math(q.feedback)+'</p>';}return;}
    if(entry.manual){fb.className='feedback manual';fb.innerHTML='<strong>پاسخ ثبت شد؛ تصحیح خودکار ندارد.</strong><p>پاسخ نمونه: '+math(q.answer)+'</p><ul>'+q.rubric.map(x=>'<li>'+math(x)+'</li>').join('')+'</ul>';}
    else{fb.className='feedback '+(entry.correct?'correct':'wrong');fb.innerHTML='<strong>'+(entry.correct?'پاسخ درست است.':'پاسخ نادرست است.')+'</strong><p class="'+(!entry.correct?'error-explanation':'learning-tip')+'">'+math(entry.correct?q.feedback:diagnosis(q,entry.answer).sentence)+'</p>';}
  }
  function grade(q,a){if(q.type==='essay'){state.submitted[q.id]={manual:true,answer:a,at:new Date().toISOString()};return;}const correct=equivalent(q,a);state.submitted[q.id]={correct,answer:a,at:new Date().toISOString(),itemReported:false};if(!correct)recordError(q,a);}
  function submit(q){if(isExam||state.submitted[q.id]||state.finished)return;const a=readAnswer(q);if(!a){byId('q-'+q.id).querySelector('.feedback').textContent='ابتدا پاسخ را وارد یا گزینه‌ای انتخاب کن.';return;}state.answers[q.id]=a;grade(q,a);save();if(!state.submitted[q.id].manual)state.submitted[q.id].itemReported=item(q,state.submitted[q.id].correct);save();bindQuestion(q);updateStats();}
  function counts(){const auto=(D.questions||[]).filter(q=>q.type!=='essay'),entries=auto.map(q=>state.submitted[q.id]),correct=entries.filter(x=>x&&x.correct).length,wrong=entries.filter(x=>x&&!x.correct).length;return {total:auto.length,correct,wrong,unanswered:auto.length-correct-wrong,pct:auto.length?Math.round(correct*100/auto.length):0,manual:D.questions.filter(q=>q.type==='essay'&&state.submitted[q.id]).length,pendingManual:D.questions.filter(q=>q.type==='essay'&&!state.submitted[q.id]).length};}
  function updateStats(){if(isExam&&!state.finished){const answered=D.questions.filter(q=>(state.answers[q.id]||'').trim()).length;byId('assessment-progress').textContent=fa(answered)+' پاسخ از '+fa(D.questions.length)+' سؤال ذخیره شده است';byId('progress').value=answered;byId('progress').max=D.questions.length;byId('question-position').textContent='سؤال '+fa(state.currentQuestion+1)+' از '+fa(D.questions.length);byId('question-navigator').innerHTML=D.questions.map((q,i)=>'<button type="button" data-question="'+i+'" class="'+(state.answers[q.id]?'answered ':'')+'"'+(i===state.currentQuestion?' aria-current="step"':'')+' aria-label="سؤال '+fa(i+1)+(state.answers[q.id]?'، دارای پاسخ':'، بدون پاسخ')+'">'+fa(i+1)+'</button>').join('');byId('question-navigator').querySelectorAll('button').forEach(b=>b.onclick=()=>moveQuestion(Number(b.dataset.question)));return;}
    if(isExam)return;const c=counts();byId('stats').innerHTML=[['کل سؤال',D.questions.length],['درست',c.correct],['غلط',c.wrong],['بدون پاسخ',c.unanswered+c.pendingManual],['تشریحی ثبت‌شده',c.manual]].map(([label,n])=>'<span>'+label+' <strong>'+fa(n)+'</strong></span>').join('');byId('progress').value=c.correct+c.wrong;byId('progress').max=c.total||1;
  }
  function moveQuestion(i){state.currentQuestion=Math.max(0,Math.min(D.questions.length-1,i));save();renderQuestions();byId('question-list').focus();}
  function finish(){if(state.finished)return;byId('finish-confirm').hidden=false;const empty=isExam?D.questions.filter(q=>!(state.answers[q.id]||'').trim()).length:counts().unanswered+counts().pendingManual;byId('finish-warning').textContent=empty?fa(empty)+' سؤال بدون پاسخ است؛ آزمون پایان یابد و پاسخ‌ها تصحیح شوند؟':'آزمون پایان یابد و پاسخ‌ها تصحیح شوند؟';byId('finish-yes').focus();}
  function commitFinish(){if(state.finished)return;if(isExam)D.questions.forEach(q=>{const a=(state.answers[q.id]||'').trim();if(a)grade(q,a);});const c=counts();state.finished=true;state.finishedAt=new Date().toISOString();state.result=c;save();
    if(isExam)D.questions.forEach(q=>{const entry=state.submitted[q.id];if(entry&&!entry.manual&&!entry.itemReported)entry.itemReported=item(q,entry.correct);});
    if(c.total&&bridge&&typeof bridge.recordExam==='function'){try{const wrong=D.questions.filter(q=>state.submitted[q.id]&&!state.submitted[q.id].manual&&!state.submitted[q.id].correct).map(q=>D.id+'_'+q.id);bridge.recordExam(c.pct,c.total,c.correct,wrong.join(','));state.examReported=true;}catch(_){}}save();renderQuestions();byId('final-result').focus();}
  function result(){const el=byId('final-result');el.hidden=!state.finished;if(!state.finished)return;const c=state.result;el.innerHTML='<h2>نتیجهٔ نهایی</h2><p class="score">'+fa(c.pct)+'٪</p><p>'+fa(c.correct)+' درست، '+fa(c.wrong)+' غلط، '+fa(c.unanswered)+' بدون پاسخ از '+fa(c.total)+' سؤال قابل تصحیح</p>'+(D.questions.some(q=>q.type==='essay')?'<p>پاسخ‌های تشریحی در درصد محاسبه نشده‌اند؛ آن‌ها را با راهنمای تصحیح مقایسه کن.</p>':'')+'<p>'+(state.examReported?'نتیجه به دفتر آزمون اپ فرستاده شد.':'نتیجهٔ این نشست در همین محیط نگه‌داری شده؛ ارسال به دفتر آزمون اپ تأیید نشده است.')+'</p>';}
  function renderQuestions(){const qs=isExam&&!state.finished?[D.questions[state.currentQuestion]]:D.questions;byId('question-list').innerHTML=qs.map(q=>cardHTML(q,D.questions.indexOf(q),state.finished)).join('');qs.forEach(bindQuestion);byId('finish-confirm').hidden=true;byId('finish').hidden=state.finished;byId('restart').hidden=!state.finished;if(isExam){byId('export-errors').hidden=!state.finished;byId('assessment-workspace').hidden=state.finished;byId('assessment-controls').hidden=state.finished;byId('review-heading').hidden=!state.finished;byId('assessment-prev').disabled=state.currentQuestion===0;byId('assessment-next').disabled=state.currentQuestion===D.questions.length-1;}updateStats();result();}
  function renderCards(){state.cardIndex=Math.max(0,Math.min(D.cards.length-1,state.cardIndex||0));const c=D.cards[state.cardIndex];byId('flash-position').textContent='کارت '+fa(state.cardIndex+1)+' از '+fa(D.cards.length);byId('flash-list').innerHTML='<article class="flash-card" aria-label="فلش‌کارت"><div class="flash-front"><p class="q-meta">'+visible(c.topic)+'</p><h2>'+math(c.front)+'</h2><button type="button" class="reveal primary">برگرداندن کارت و نمایش پاسخ</button></div><div class="card-answer" hidden><span class="badge">پشت کارت</span><p>'+math(c.back)+'</p><div class="controls"><button type="button" data-known="yes">بلد بودم</button><button type="button" data-known="no">نیاز به مرور دارم</button></div></div><p class="card-mark" role="status"></p></article>';
    const el=byId('flash-list').firstElementChild;el.querySelector('.reveal').onclick=()=>{el.querySelector('.flash-front').hidden=true;el.querySelector('.card-answer').hidden=false;};function label(){el.querySelector('.card-mark').textContent=state.cards[c.id]===true?'آخرین مرور: بلد بودم':state.cards[c.id]===false?'آخرین مرور: نیاز به مرور':'';}label();el.querySelectorAll('[data-known]').forEach(b=>b.onclick=()=>{const good=b.dataset.known==='yes';state.cards[c.id]=good;if(bridge&&typeof bridge.recordItem==='function'){try{bridge.recordItem(c.id,good);}catch(_){}}save();label();el.querySelectorAll('[data-known]').forEach(x=>x.disabled=true);});byId('flash-prev').disabled=state.cardIndex===0;byId('flash-next').disabled=state.cardIndex===D.cards.length-1;byId('flash-reviewed').textContent=fa(Object.keys(state.cards).length)+' کارت مرور شده است';}
  function exportErrors(){const errors=Object.values(root.documents).flatMap(d=>d.errors||[]),blob=new Blob([JSON.stringify({schema:root.schema,exportedAt:new Date().toISOString(),errors},null,2)],{type:'application/json'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='hamyar-math-'+(D.scopeId||'f01')+'-errors.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),0);}
  document.querySelectorAll('[data-math-text]').forEach(el=>{el.innerHTML=math(el.textContent);});
  load();window.HamyarPractice={equivalent,normalize,counts,diagnosis,documentId:D.id};save();
  if(D.mode==='final'){window.HamyarFinal.start({D,bridge,save,fa,math,inputValue,normalize,equivalent,recordError,diagramMarkup,state:()=>state,restart:()=>{state=fresh(state);save();}});return;}
  if(D.questions){renderQuestions();byId('finish').onclick=finish;byId('finish-yes').onclick=commitFinish;byId('finish-no').onclick=()=>{byId('finish-confirm').hidden=true;byId('finish').focus();};byId('restart').onclick=()=>{state=fresh(state);save();renderQuestions();};if(isExam){byId('assessment-prev').onclick=()=>moveQuestion(state.currentQuestion-1);byId('assessment-next').onclick=()=>moveQuestion(state.currentQuestion+1);}}
  if(D.cards){renderCards();byId('flash-prev').onclick=()=>{state.cardIndex--;save();renderCards();};byId('flash-next').onclick=()=>{state.cardIndex++;save();renderCards();};}
  if(byId('export-errors'))byId('export-errors').onclick=exportErrors;
})();

```

### پیوست 5 — رفتار تکمیلی پنجرهٔ تمام‌اندازه

تعداد استفاده: `252`؛ SHA-256: `c365ba54291c150b5bf9927ab184b76d1fae86404d941214f8c66ece61d9aecf`.

```javascript
/* Additive full-viewport dialog accessibility; does not replace the locked UI or learning bridge. */
(function(){'use strict';var d=document,w=d.getElementById('fab'),p=d.getElementById('fab-panel'),b=d.getElementById('fab-btn');if(!w||!p||!b)return;var opened=false,prior=[];p.tabIndex=-1;
function sync(){var on=w.classList.contains('open');if(on===opened)return;opened=on;d.documentElement.classList.toggle('hamyar-floater-open',on);if(on){p.setAttribute('aria-modal','true');prior=[].slice.call(d.querySelectorAll('header#top,main#main,footer.site-footer')).map(function(n){var old=n.hasAttribute('inert');n.setAttribute('inert','');return[n,old]});p.focus({preventScroll:true})}else{p.removeAttribute('aria-modal');prior.forEach(function(x){if(!x[1])x[0].removeAttribute('inert')});prior=[];b.focus({preventScroll:true})}}
new MutationObserver(sync).observe(w,{attributes:true,attributeFilter:['class']});sync();
d.addEventListener('keydown',function(e){if(!opened||e.key!=='Tab')return;var a=[].slice.call(w.querySelectorAll('a[href],button:not([disabled]),input:not([disabled]),[tabindex="0"]')).filter(function(n){return n.getClientRects().length&&getComputedStyle(n).visibility!=='hidden'});if(!a.length){e.preventDefault();p.focus();return}var first=a[0],last=a[a.length-1];if(e.shiftKey&&(d.activeElement===first||d.activeElement===p)){e.preventDefault();last.focus()}else if(!e.shiftKey&&(d.activeElement===last||d.activeElement===p)){e.preventDefault();first.focus()}},true);
})();

```

### پیوست 6 — موتور بارم‌بندی جامع

تعداد استفاده: `24`؛ SHA-256: `0c64fc2046f738ed7512ef04fc6d5332d80a09b72b242cc3ecbb852a777c5626`.

```javascript
/* Weighted, paper-style final exam. Manual work is disclosed as self-assessment. */
window.HamyarFinal={start:function(API){
 'use strict';
 const {D,bridge,save,fa,math,normalize,equivalent,recordError,diagramMarkup}=API;
 const $=id=>document.getElementById(id),state=()=>API.state();
 const mark=n=>fa(n).replace('.', '٫');
 const answered=q=>!!((state().answers[q.id]||'').trim()||(q.drawing&&((state().drawings||{})[q.id]||[]).length));
 function selected(q){const el=$('q-'+q.id);if(q.type==='mcq'||q.type==='tf'){const x=el.querySelector('input:checked');return x?x.value:'';}return el.querySelector('textarea,input').value.trim();}
 function input(q){
  if(q.type==='tf'||q.type==='mcq'){let options=q.type==='tf'?['درست','نادرست']:q.options.slice();if(q.type==='mcq'){const shift=(D.variant+q.group+q.part+q.level)%options.length;options=options.slice(shift).concat(options.slice(0,shift));}return '<fieldset class="choices"><legend class="sr-only">پاسخ این بخش</legend>'+options.map((x,i)=>'<label class="choice"><input type="radio" name="'+q.id+'" value="'+escape(x)+'"><span>'+fa(i+1)+'ـ '+math(x)+'</span></label>').join('')+'</fieldset>';}
  return (q.drawing?'<div class="drawing-area"><canvas id="draw-'+q.id+'" width="600" height="300" aria-label="فضای رسم گسترده؛ توضیح متنی نیز پذیرفته می‌شود"></canvas><button type="button" data-clear-drawing="'+q.id+'">پاک‌کردن رسم</button></div>':'')+'<label for="input-'+q.id+'">'+(q.type==='essay'?(q.drawing?'توضیح رسم، برای دسترسی با صفحه‌کلید':'راه‌حل و پاسخ تشریحی'):(q.type==='set'?'پاسخ به صورت مجموعه':'پاسخ کوتاه'))+'</label>'+(q.type==='essay'?'<textarea id="input-'+q.id+'" rows="3" maxlength="6000"></textarea>':'<input id="input-'+q.id+'" type="text" autocomplete="off" maxlength="500"'+(q.type==='text'?'':' dir="ltr"')+'>');
 }
 function escape(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
 function draw(q){
  const canvas=$('draw-'+q.id);if(!canvas)return;
  const ctx=canvas.getContext('2d');state().drawings=state().drawings||{};
  let strokes=state().drawings[q.id]||[],active=null;
  function paint(){ctx.clearRect(0,0,canvas.width,canvas.height);ctx.lineWidth=3;ctx.strokeStyle='#4b326f';ctx.lineCap='round';for(const line of strokes){ctx.beginPath();line.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.stroke();}}
  function point(e){const r=canvas.getBoundingClientRect();return [(e.clientX-r.left)*canvas.width/r.width,(e.clientY-r.top)*canvas.height/r.height];}
  canvas.onpointerdown=e=>{if(state().finished)return;e.preventDefault();canvas.setPointerCapture(e.pointerId);active=[point(e)];strokes.push(active);};
  canvas.onpointermove=e=>{if(!active)return;active.push(point(e));paint();};
  canvas.onpointerup=canvas.onpointercancel=()=>{if(!active)return;active=null;state().drawings[q.id]=strokes;save();progress();};
  document.querySelector('[data-clear-drawing="'+q.id+'"]').onclick=()=>{if(state().finished)return;strokes=[];state().drawings[q.id]=[];paint();save();progress();};paint();
 }
 function progress(){const n=D.questions.filter(answered).length;$('paper-progress').textContent=fa(n)+' بخش از '+fa(D.questions.length)+' بخش پاسخ دارد؛ تصحیح پس از پایان انجام می‌شود.';}
 function totals(){let earned=0,autoEarned=0,autoMax=0,pending=0,manualMax=0,manualEarned=0;for(const q of D.questions){const e=state().submitted[q.id];if(q.type==='essay'){manualMax+=q.marks;if(e&&e.manual&&!e.reviewed)pending++;if(e&&e.reviewed)manualEarned+=e.earned;}else{autoMax+=q.marks;if(e&&e.correct)autoEarned+=q.marks;}}earned=autoEarned+manualEarned;return {totalMarks:20,earned,autoEarned,autoMax,manualMax,manualEarned,pending,percentage:Math.round(earned*5),assessmentMethod:D.questions.some(q=>state().submitted[q.id]&&state().submitted[q.id].manual)?'automatic-and-self-assessment':'automatic',mainQuestions:16};}
 function manualFeedback(q,el,entry){
  const fb=el.querySelector('.feedback');if(!entry){fb.className='feedback manual';fb.innerHTML='<strong>بدون پاسخ؛ بارم این بخش صفر است.</strong><p>پاسخ نمونه: '+math(q.answer)+'</p>';return;}
  const choice=(state().manualRubrics||{})[q.id]||{};
  fb.className='feedback manual';fb.innerHTML='<strong>نیازمند ارزیابی راه‌حل؛ این بخش خودکار تصحیح نشده است.</strong><p>پاسخ نمونه: '+math(q.answer)+'</p><p class="'+(entry.reviewed&&entry.earned<q.marks?'error-explanation':'learning-tip')+'">'+math(q.feedback)+'</p><p>با راهنمای زیر نوشته یا رسم خودت را بررسی کن؛ هر مرحلهٔ درست را علامت بزن.</p><fieldset class="rubric"><legend>راهنمای بارم‌بندی و خودارزیابی</legend>'+q.rubric.map(r=>'<label><input type="checkbox" data-step="'+r.id+'"'+(choice[r.id]?' checked':'')+(entry.reviewed?' disabled':'')+'><span>'+math(r.text)+' <strong>'+mark(r.marks)+' نمره</strong></span></label>').join('')+'</fieldset><button type="button" class="confirm-rubric"'+(entry.reviewed?' disabled':'')+'>ثبت خودارزیابی این بخش</button><p class="rubric-status">'+(entry.reviewed?'طبق خودارزیابی: '+mark(entry.earned)+' از '+mark(q.marks)+'؛ تأیید دبیر انجام نشده است.':'')+'</p>';
  fb.querySelectorAll('[data-step]').forEach(box=>box.onchange=()=>{state().manualRubrics=state().manualRubrics||{};state().manualRubrics[q.id]=state().manualRubrics[q.id]||{};state().manualRubrics[q.id][box.dataset.step]=box.checked;save();});
  fb.querySelector('.confirm-rubric').onclick=()=>{if(entry.reviewed)return;const values=(state().manualRubrics||{})[q.id]||{};entry.earned=q.rubric.reduce((n,r)=>n+(values[r.id]?r.marks:0),0);entry.reviewed=true;entry.assessmentMethod='self-assessment';entry.reviewedAt=new Date().toISOString();if(entry.earned<q.marks){const oldCount=state().errors.length;recordError(q,entry.answer);if(state().errors.length>oldCount){const error=state().errors.at(-1);error.errorCategory='خودارزیابیِ بخش تشریحی؛ نیازمند تأیید دبیر';error.assessmentMethod='self-assessment';error.earnedMarks=entry.earned;error.maximumMarks=q.marks;if(q.drawing)error.studentDrawing=state().drawings[q.id];}}save();manualFeedback(q,el,entry);showResult();};
 }
 function feedback(q,el){if(!state().finished)return;const e=state().submitted[q.id],fb=el.querySelector('.feedback');if(q.type==='essay'){manualFeedback(q,el,e);return;}fb.className='feedback '+(!e?'manual':e.correct?'correct':'wrong');fb.innerHTML='<strong>'+(!e?'بدون پاسخ':e.correct?'پاسخ درست':'پاسخ نادرست')+'</strong><p>پاسخ صحیح: '+math(q.answer)+'</p>'+(e&&!e.correct?'<p class="error-explanation">'+math(window.HamyarPractice.diagnosis(q,e.answer).sentence)+'</p>':'')+'<p>بارم کسب‌شده: '+mark(e&&e.correct?q.marks:0)+' از '+mark(q.marks)+'</p>';}
 function render(){
  const labels=['الف','ب','پ','ت'];
  $('paper-pages').innerHTML=[1,2,3,4].map(page=>'<section class="paper-page" data-paper-page="'+page+'"><div class="paper-page-heading"><strong>ریاضی نهم؛ خودآزمایی جامع</strong><span>صفحهٔ '+fa(page)+' از ۴</span></div>'+Array.from({length:16},(_,i)=>i+1).filter(g=>D.questions.some(q=>q.group===g&&q.page===page)).map(g=>{const qs=D.questions.filter(q=>q.group===g);return '<section class="paper-question"><div class="paper-number">'+fa(g)+'</div><div class="paper-body"><h2>'+math(D.groupTitles[g-1])+'</h2>'+qs.map(q=>'<article id="q-'+q.id+'" class="paper-part"><h3>'+labels[q.part-1]+'ـ '+math(q.prompt)+'</h3>'+(q.diagram?diagramMarkup(q.diagram):'')+input(q)+'<p class="part-mark">بارم این بخش: '+mark(q.marks)+'</p>'+(state().finished?'<div class="feedback" role="status"></div>':'')+'</article>').join('')+'</div><div class="paper-marks"><span class="sr-only">بارم سؤال</span>'+mark(qs.reduce((n,q)=>n+q.marks,0))+'</div></section>';}).join('')+'</section>').join('');
  D.questions.forEach(q=>{const el=$('q-'+q.id),value=state().answers[q.id]||'';el.querySelectorAll('input[type=radio]').forEach(x=>x.checked=normalize(x.value)===normalize(value));const text=el.querySelector('textarea,input[type=text]');if(text)text.value=API.inputValue(value);el.querySelectorAll('input,textarea').forEach(x=>{x.disabled=state().finished;x.oninput=()=>{if(state().finished)return;if(x.type==='text'||x.tagName==='TEXTAREA'){const start=x.selectionStart,end=x.selectionEnd;x.value=API.inputValue(x.value);x.setSelectionRange(start,end);}state().answers[q.id]=selected(q);save();progress();};});if(q.drawing){draw(q);el.querySelector('[data-clear-drawing]').disabled=state().finished;}feedback(q,el);});
  $('paper-progress').hidden=state().finished;$('paper-finish').hidden=state().finished;$('paper-restart').hidden=!state().finished;$('paper-confirm').hidden=true;progress();showResult();
 }
 function showResult(){const el=$('paper-result');el.hidden=!state().finished;if(!state().finished)return;const t=totals();state().result=t;save();const done=!!state().finalized;el.innerHTML='<h2>'+(done?'نتیجهٔ ثبت‌شده':'تصحیح پس از پایان آزمون')+'</h2><p>امتیاز بخش قابل تصحیح خودکار: <strong>'+mark(t.autoEarned)+' از '+mark(t.autoMax)+'</strong></p>'+(t.pending?'<p>'+fa(t.pending)+' بخش تشریحی پاسخ دارد و نیازمند بررسی با راهنمای بارم‌بندی است؛ نمرهٔ نهایی هنوز مشخص نیست.</p>':'<p class="score">'+mark(t.earned)+' از ۲۰</p><p>درصد بر پایهٔ بارم: '+fa(t.percentage)+'٪</p>')+(t.assessmentMethod==='automatic-and-self-assessment'?'<p class="assessment-disclosure">بارم بخش تشریحی با خودارزیابی دانش‌آموز تعیین می‌شود؛ تصحیح قطعی دبیر انجام نشده است.</p>':'')+(done?'<p>'+(state().examReported?'نتیجه به دفتر آزمون اپ فرستاده شد.':'نتیجه در همین محیط نگه‌داری شده؛ ثبت در دفتر آزمون اپ تأیید نشده است.')+'</p>':'<button id="paper-save-result" type="button" class="primary"'+(t.pending?' disabled':'')+'>ثبت نتیجه'+(t.assessmentMethod==='automatic-and-self-assessment'?' با خودارزیابی بخش تشریحی':'')+'</button>');
  if(!done)$('paper-save-result').onclick=finalize;
 }
 function finish(){if(state().finished)return;$('paper-confirm').hidden=false;const missing=D.questions.filter(q=>!answered(q)).length;$('paper-warning').textContent=missing?fa(missing)+' بخش بدون پاسخ است؛ آزمون پایان یابد؟':'آزمون پایان یابد و پاسخ‌ها بررسی شوند؟';$('paper-finish-yes').focus();}
 function commitFinish(){if(state().finished)return;for(const q of D.questions){if(!answered(q))continue;const answer=(state().answers[q.id]||'').trim()||(q.drawing?'رسم ذخیره‌شده':''),at=new Date().toISOString();if(q.type==='essay')state().submitted[q.id]={manual:true,answer,at,reviewed:false};else{const correct=equivalent(q,answer);state().submitted[q.id]={correct,answer,at};if(!correct)recordError(q,answer);}}state().finished=true;state().finishedAt=new Date().toISOString();state().gradingPolicy={marks:20,mainQuestions:16,manualReview:'self-assessment disclosed; teacher approval pending',blueprint:'iran-national-math9-morning-1404'};save();render();$('paper-result').focus();}
 function finalize(){if(!state().finished||state().finalized||totals().pending)return;const t=totals(),wrong=[],groups=[];for(let g=1;g<=16;g++){const qs=D.questions.filter(q=>q.group===g);const good=qs.every(q=>{const e=state().submitted[q.id];return e&&(e.manual?e.reviewed&&e.earned===q.marks:e.correct);});const bad=qs.some(q=>{const e=state().submitted[q.id];return e&&(e.manual?e.reviewed&&e.earned<q.marks:!e.correct);});const id=D.id+'_final-q'+String(g).padStart(2,'0');groups.push({id,correct:good,answered:qs.some(answered)});if(bad)wrong.push(id);}state().finalized=true;state().finalizedAt=new Date().toISOString();state().result=t;save();
  for(const g of groups)if(g.answered&&bridge&&typeof bridge.recordItem==='function'){try{bridge.recordItem(g.id,g.correct);}catch(_){}}
  if(bridge&&typeof bridge.recordExam==='function'){try{bridge.recordExam(t.percentage,16,groups.filter(x=>x.correct).length,wrong.join(','));state().examReported=true;}catch(_){}}save();showResult();
 }
 $('paper-finish').onclick=finish;$('paper-finish-yes').onclick=commitFinish;$('paper-finish-no').onclick=()=>{$('paper-confirm').hidden=true;$('paper-finish').focus();};$('paper-restart').onclick=()=>{API.restart();render();};render();
 window.HamyarPractice.paperTotals=totals;
}};

```

### CSS افزودهٔ پنجرهٔ تمام‌اندازه

این CSS بعد از استایل‌های قالب و تم، در خود HTML امبد است؛ فایل CSS جانبی لازم نیست.

```css
/* Full WebView content viewport; the reference locked styles stay intact. */
#fab.open{inset:0;width:100%;height:100%;z-index:10000;isolation:isolate}
#fab.open #fab-panel{position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;margin:0;border:0;border-radius:0;box-sizing:border-box;padding:max(18px,env(safe-area-inset-top)) max(16px,env(safe-area-inset-right)) calc(90px + env(safe-area-inset-bottom)) max(16px,env(safe-area-inset-left));overflow-y:auto;overscroll-behavior:contain;transform:none;background:var(--card);color:var(--ink)}
#fab.open #fab-btn{position:absolute;left:max(14px,env(safe-area-inset-left));bottom:max(14px,env(safe-area-inset-bottom));z-index:2}
html.hamyar-floater-open,html.hamyar-floater-open body{overflow:hidden;overscroll-behavior:none}
@supports(height:100dvh){#fab.open{height:100dvh}}
@media print{#fab.open{display:none!important}}

```

## ارجاع گزارش و ادامه

مرجع گزارش‌های نقش: https://github.com/samanta-nz/Books-Data/tree/main/codex-reports/Exam-Content-Builder

بستهٔ این تغییر: https://github.com/samanta-nz/Books-Data/tree/main/codex-reports/Exam-Content-Builder/2026-10-23/002-MATH9-STANDALONE

در دستور بعدی، URL همین پوشه، commit فایل‌ها و hash ZIP/manifest منتقل شود؛ مسیر محلی تنها برای تحویل بین چت‌ها کافی نیست.
