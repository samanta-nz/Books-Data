# گوشه‌ی سبز شهری — راهنمای جامع تولید صدا، بک‌گراند و رنگ‌بندی

## ۱) مشخصات فایل

- فایل HTML: `09-urban-green-space.html` | شناسه: `cj-09` | مسیر: `Bucket/Html-files/app/calm/journey/09-urban-green-space.html`
- تعداد فایل صوتی: ۶ (هر بخش یک فایل: `09-urban-green-space-01.mp3` تا `-06.mp3`) | مدت کل (سرعت ۱٫۳×، با مکث‌ها): حدود ۲۱ دقیقه
- مخاطب: «تو» (مفرد) با افعال محاوره‌ای. صفحه پیوسته و همراه‌صدا است: بدون آکاردئون، بدون عنوان بخش، بدون متن اضافه.
- تم صفحه: خودکار تاریک/روشن (prefers-color-scheme)، بدون دکمه. اگر وب‌ویوی اپ تم را نمی‌رساند: `setTheme('dark')` یا `setTheme('light')`.
- نشانه‌ی آیکون سرعتی روی کنترل: از روی دکمه‌ی با آیکون چرخشی ۱۵ ثانیه‌ای (نه متن -۱۵/+۱۵).

## ۲) خوانش: لحن، سرعت و مکث‌ها

- **لحن کلی:** شاد، نزدیک و آرام، مثل کسی که وسط شهر یه نفس عمیق می‌کشه و آرام به تو می‌گه. تُن یکدست و پایین، بدون اوج دراماتیک. همراه با کمی آرام‌بخش از چشم‌انداز شهری به سمت درخت و سبزی.
- **سبک گفتار:** محاوره‌ای مفرد (می‌تونی، بذار، بریم، می‌شه، نمی‌خواد، اگه، یه). متن رو مثل حرف زدن بخون، نه مثل خوندن.
- **سرعت:** ۱٫۳× (speed=1.3). طول مکث‌ها در سرعت بالا ثابت بمونه.
- **علامت مکث:** `[مکث N ثانیه]` = N ثانیه سکوت کامل. SSML: `<break time="Ns"/>`. اگر موتور صوتی نمی‌فهمد، سکوت را بعد از تولید در ویرایش صوت اضافه کن.
- **اندازه‌ی مکث‌ها:** کوتاه ۱ تا ۳ ثانیه | متوسط ۴ تا ۶ | بلند ۸ تا ۱۵ | ۱۲ تا ۱۵ فقط در پایان بخش‌ها برای سکوت کامل.
- **آهنگ:** تخت و یکنواخت؛ پایان جمله‌ی دستوری کمی پایین. واژه‌های «نفس»، «سبز»، «آرام» کمی کشیده‌تر بیان.

## ۳) ترکیب رنگی گوی و کنترل‌ها

- **عنوان ترکیب:** «سبز شهری و نقره‌ی صبحگاهی»
- **روشن:** صفحه #F0F2EE → #D8E6D2 | گوی (sphere): مرکز سفید ۸۰٪، میانه #8BB35A، لبه #4E7F3A | دکمه‌ی پخش: گرادیان #8BB35A → #4E7F3A با آیکون سفید | نوار پیشرفت: همان | متن: #26351F | پنل کنترل: شیشه‌ی سفید ۵۵٪
- **تاریک:** صفحه #0E130D → #1E2E1A | گوی: مرکز سفید ۸۰٪، میانه #B6E36A، لبه #A3D97B | دکمه‌ی پخش: گرادیان #B6E36A → #A3D97B با آیکون سفید | متن: #E4EEDC | پنل کنترل: شیشه‌ی مشکی ۲۸٪
- **ذرات صفحه:** برگ‌های ریزنده و تابش نرم نور روز (با انیمیشن نزدیک به اورانیون عادی، نه تند).

## ۴) پرامپت بک‌گراند (دقیق و کامل)

دو تصویر لازم است: روشن و تاریک (هر دو نسبت به هم عکس با از نظر ترکیب یکسان). لایه‌ی محو رنگی روی هر تصویر به‌صورت خودکار اضافه می‌شود.

### نسخه‌ی روشن (انگلیسی؛ Midjourney / Flux / SDXL / Imagen)

```text
A small green pocket park in a city at early morning, seen at eye level from a bench-height viewpoint. A soft grass lawn with a gravel path curving through, young birch and linden trees with light green leaves, a few low shrubs in bloom, distant blurred apartment buildings in soft pastel tones behind the trees, faint morning haze, a single empty wooden bench at the edge. Calm, human-scale, gentle daylight, airy, high-key, soft focus depth, photographic with gentle film softness. Palette: #F0F2EE, #D8E6D2, #4E7F3A, #8BB35A. Vertical 9:16, 1080x1920 px. Phone background behind a UI: keep the central 40% (30 to 70% of the height) soft, low-detail and low-contrast for a glowing orb, so let the buildings and trees blur into a soft band in the middle; keep the bottom 35% calm and slightly darker for a control panel; interest in the top third (canopy) and margins. Gentle contrast, no bright hotspots, comfortable for hour-long viewing. No text, logos, signs, watermark, people, faces, hands, animals, cars or UI elements.
```

### نسخه‌ی تاریک

```text
The same small city park at deep blue dusk. Soft street lamp glow far away, green lawn in cool blue shadow, birch leaves dark teal, distant city windows as tiny warm dots blurred into bokeh, a faint cool haze over the path, the empty bench barely visible. Very low-key, quiet, soft contrast, photographic. Palette: #0E130D, #1E2E1A, #A3D97B, #B6E36A. Vertical 9:16, 1080x1920 px. Phone background behind a UI: keep the central 40% soft, low-detail and low-contrast for a glowing orb; keep the bottom 35% calm and darker for a control panel; interest in the top third and margins. No bright hotspots. No text, logos, signs, watermark, people, faces, hands, animals, cars or UI elements.
```

### پرامپت منفی (هر دو نسخه)

```text
text, letters, signs, watermark, logo, signature, people, face, hands, animals, cars, traffic, harsh contrast, oversaturated colors, neon, HDR halo, lens flare, chromatic aberration, noisy grain, border, frame, cartoon, illustration, 3D render look, clutter, litter, graffiti
```

### مشخصات خروجی و نسخه‌ی ویدیویی اختیاری

- دو فایل `09-urban-green-space-bg-light.webp` و `09-urban-green-space-bg-dark.webp`، ۱۰۸۰×۱۹۲۰، کیفیت ۷۰ تا ۸۰، حداکثر ۱۵۰ تا ۲۰۰ کیلوبایت.
- لوپ ویدیویی (فعلاً نمایش داده نمی‌شود): `Seamless loop 8 to 10 seconds: leaves move gently in a light breeze, distant traffic is absent, a few birds never cross the frame, light shifts softly across the lawn. Camera locked off, 9:16, 1080x1920, 24 fps, MP4 under 1.5 MB, no audio.`

### تزریق صدا و بک‌گراند به HTML

```python
import base64, json, re, glob
n = '09-urban-green-space'
h = open(n + '.html', encoding='utf-8').read()
uris = ['data:audio/mpeg;base64,' + base64.b64encode(open(f, 'rb').read()).decode() for f in sorted(glob.glob(n + '-0*.mp3'))]
h = re.sub(r'AUDIO=\[.*?\];', lambda m: 'AUDIO=' + json.dumps(uris) + ';', h, count=1, flags=re.S)
img = lambda p: 'data:image/webp;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
bg = 'const BG={light:"' + img(n + '-bg-light.webp') + '",dark:"' + img(n + '-bg-dark.webp') + '"};'
h = re.sub(r'const BG=\{.*?\};', lambda m: bg, h, count=1, flags=re.S)
open(n + '.html', 'w', encoding='utf-8').write(h)
```

تعداد MP3 باید ۶ باشد و ترتیب با ترتیب بخش‌ها یکی. صفحه خودکار تاریک/روشن می‌شود.

### متن بخش‌ها برای تولید صدا

> هر بخش یک فایل صوتی است. خط «لحن» فقط برای تنظیم خوانش است و خونده نمی‌شود.

#### بخش ۱: پیش از شروع، نفس با شهر
- **لحن:** نرم و دوستانه، کمی آروم‌تر از گفت‌وگوی عادی.

سلام. امروز قرار نیست از شهر دور بشی، چون می‌دونی نمی‌شه. فقط چند دقیقه وسط یه فضای سبز کوچیک شهر می‌نشییم. **[مکث ۲ ثانیه]**

به شهر زیاد عادت داری و اگه چند وقت بی‌وقفه و صدا و فشار باشه، بدنت با آن هماهنگ شده. این تمرین هیچ امتحانی نیست. **[مکث ۳ ثانیه]**

حالا یه جای راحت پیدا کن. اگه نشستی، کمرت رو به صندلی بده و پاهات رو روی زمین بذار. **[مکث ۳ ثانیه]**

چشم‌هات رو آروم ببند، یا نگاهت رو نرم روی زمین نگه دار. **[مکث ۴ ثانیه]**

شونه‌هات رو یه بار بالا بیار و با یه بازدم رها کن. **[مکث ۵ ثانیه]**

دم، **[مکث ۴ ثانیه]** و بازدم. **[مکث ۸ ثانیه]**

خوبه. بیا بریم سراغ این گوشهی کوچیک. **[مکث ۶ ثانیه]**

#### بخش ۲: ورود به باغچه
- **لحن:** تصویری و آرام، با جمله‌های کشیده‌تر. بعد از هر توصیف مکث بذار.

تصور کن از یه خیابون شلوغ وارد یه باغچهی کوچیک می‌شی. یه مسیر سنگریزه از میان چمن‌ها می‌پیچه. **[مکث ۴ ثانیه]**

چمن نرمه. یه رنگ سبز روشن رو چمن داره، با چند برگ و تابیده زرد و سفید. باد ملایمی می‌آیه و برگ‌های درختها رو تکان می‌دن. **[مکث ۵ ثانیه]**

با هر قدم، صدای شهر کمی دور می‌شه و صدای برگ‌ها نزدیک می‌شه. **[مکث ۶ ثانیه]**

و یه نیمکت خالی کنار راه هست. یه نیمکت چوبی قدیمی، که از نشستن خسته شده و آرام منتظرته. **[مکث ۸ ثانیه]**

بنشین. چند ثانیه فقط نفس بکش و ببین چه چیزین نزدیکته. **[مکث ۸ ثانیه]**

#### بخش ۳: صداهای شهر در باغ
- **لحن:** کندتر و آهنگین، با سکوت‌های واقعی. صداها رو روی «دور» و «نزدیک» تنظیم کن.

حالا چشم‌هات رو ببند و فقط گوش بده. **[مکث ۵ ثانیه]**

اولین صدا برگهاست. نرم و بی‌عجله می‌رقصه. هر بار یه برگ از جایی به جای دیگه می‌ره. **[مکث ۸ ثانیه]**

دورتر، یه صدای آروم از مسیری كه هم می‌آیه، مثل قدم‌های یه آدم آرام. بدون عجله و بدون مقصد. **[مکث ۶ ثانیه]**

و یه باد ملایم توی درختها می‌چرخه. برگ‌ها به هم می‌خورن و یه صدای آرام می‌دن. **[مکث ۸ ثانیه]**

یه مرغ کوچیک روی شاخه و بعد ساکت. اگه صدای خودرو بیان نزدیک، لازم نیست دنبالش بگردی. **[مکث ۸ ثانیه]**

اگه صدای شهر بلند شد، لازم نیست حواست رو به ان بده. فقط برگرد به صدای برگ‌ها. **[مکث ۱۰ ثانیه]**

حالا با هر بازدم، از نفست خبر گرفتنی بدون عجله. **[مکث ۴ ثانیه]** بازدم. **[مکث ۶ ثانیه]**

#### بخش ۴: نشستن روی نیمکت
- **لحن:** نرم و بدنی، با دستورهای تنفس از طریق صدا.

حالا نشستن رو بیار این نیمکتی که کنار باغه و با شهر فاصله داره. **[مکث ۳ ثانیه]**

دم می‌گیری، **[مکث ۴ ثانیه]** و بازدم به آرامی. **[مکث ۸ ثانیه]**

باز هم. دم، **[مکث ۴ ثانیه]** و بازدم. **[مکث ۸ ثانیه]**

حس کن که شانه‌هات سنگینیه‌ی کمی رو به زمین می‌دن. **[مکث ۵ ثانیه]**

و فکرت رو به رگشون نرم می‌کنی، از سبزِ تیره به سبزِ روشن. **[مکث ۸ ثانیه]**

#### بخش ۵: نفس با چشم‌انداز شهری
- **لحن:** عمیق‌ترین و آرام‌ترین بخش. جمله‌ها کوتاه و بدون فشار.

حالا می‌تونی چشم‌هات رو باز کنی یا همون‌طور بسته بمونی. **[مکث ۳ ثانیه]**

به وزن بدنت توجه کن و یه نفس عمیق بکش. **[مکث ۴ ثانیه]** و بازدم. **[مکث ۸ ثانیه]**

لازم نیست چیزی رو حل کنی. این جا لازم نیست بخشی از برنامه‌ی روز باشه. **[مکث ۵ ثانیه]**

نفس بعدی، **[مکث ۴ ثانیه]** و بازدم کامل. **[مکث ۶ ثانیه]**

به آن نقطه‌ی سبز دور به خودت بگو که هر وقت بخوای می‌تونی بهش برگردی. **[مکث ۵ ثانیه]**

#### بخش ۶: برگشت به روز
- **لحن:** به‌تدریج روشن‌تر و پرانرژی‌تر؛ تمام نرم و گرم.

از یه نیمکت بلند شو و با آرامش به سمت راه برگرد. **[مکث ۳ ثانیه]**

دوباره صداهای شهر و برگ‌ها رو کنار هم می‌شنوی. اون همونیه که وقت شروع کردیم. **[مکث ۵ ثانیه]**

چشم‌هات رو باز کن و اتاق رو ببین. اگه هنوز باز نیستی، نگاهت رو آروم به اتاق برگردون. **[مکث ۶ ثانیه]**

یه نکته برای بعد: در روزهای شلوغ، همین سه نفس در وسط راه کافیه. مغزت این مسیر رو یاد بگیره. **[مکث ۵ ثانیه]**

اگه بعد از تمرین نگران شدی، نگران نباش، این هم گاهی اتفاق می‌افته. اگه این حس ادامه پیدا کرد، با یه متخصص سلامت روان صحبت کن. **[مکث ۳ ثانیه]**

روز خوبی داشته باشی. **[مکث ۳ ثانیه]**

### یادداشت ایمنی و منابع علمی (برای اپ؛ داخل صفحه‌ی صوتی نمایش داده نمی‌شود)

- **ایمنی:** رانندگی یا کار با ماشین‌آلات را با این تمرین نشونید. اگر وسط تمرین احساس ناخوشایند یا بی‌قراری پیدا کردی، چشم‌ها را باز کن و اگر لازم بود با یک متخصص صحبت کن.
- Hartig, T., Mitchell, R., de Vries, S., & Frumkin, H. (2014). Nature and health. Annual Review of Public Health, 35, 207–228.
- Wolch, J., Byrne, J., & Newell, J. P. (2014). Urban green space, public health, and environmental justice: The challenge of making cities 'just green enough'. Landscape and Urban Planning, 125, 234–244.
- Ulrich, R. S. (1984). View through a window may influence recovery from surgery. Science, 224(4647), 420–421.
- Zaccaro, A., et al. (2018). How breath-control can change your life: A systematic review on psycho-physiological correlates of slow breathing. Frontiers in Human Neuroscience, 12, 353.
- NCCIH (NIH). Relaxation Techniques: What You Need To Know. https://www.nccih.nih.gov/health/relaxation-techniques-what-you-need-to-know
