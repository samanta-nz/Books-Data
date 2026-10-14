# باغ چهار حس — راهنمای جامع تولید صدا، بک‌گراند و رنگ‌بندی

## ۱) مشخصات فایل

- فایل HTML: `10-five-senses-garden.html` | شناسه: `cj-10` | مسیر: `Bucket/Html-files/app/calm/journey/10-five-senses-garden.html`
- تعداد فایل صوتی: ۶ (هر بخش یک فایل: `10-five-senses-garden-01.mp3` تا `-06.mp3`) | مدت کل (سرعت ۱٫۳×، با مکث‌ها): حدود ۲۰ دقیقه
- مخاطب: «تو» (مفرد) با افعال محاوره‌ای. صفحه پیوسته و همراه‌صدا است: بدون آکاردئون، بدون عنوان بخش، بدون متن اضافه.
- تم صفحه: خودکار تاریک/روشن، بدون دکمه. وب‌ویوی اپ: `setTheme('dark')` یا `setTheme('light')`.
- کنترل سرعت: آیکون چرخشی ۱۵ ثانیه‌ای، بدون متن.

## ۲) خوانش: لحن، سرعت و مکث‌ها

- **لحن کلی:** گرم و بازیگوش‌ی، مثل کسی که دستش رو گرفته و به گل‌ها و بوها ول می‌کنه. تُن نرم و یکدست، بدون اوج.
- **سبک گفتار:** محاوره‌ای مفرد (می‌تونی، بذار، ببینی، می‌شه، نمی‌خواد، اگه، یه). متن رو مثل حرف زدن بخون.
- **سرعت:** ۱٫۳× (speed=1.3). طول مکث‌ها در سرعت بالا ثابت بمونه.
- **علامت مکث:** `[مکث N ثانیه]` = N ثانیه سکوت کامل. SSML: `<break time="Ns"/>`. اگر موتور صوتی نمی‌فهمد، سکوت را بعد از تولید در ویرایش صوت اضافه کن.
- **اندازه‌ی مکث‌ها:** کوتاه ۱ تا ۳ ثانیه | متوسط ۴ تا ۶ | بلند ۸ تا ۱۵. ۱۲ تا ۱۵ فقط در پایان بخش‌ها.
- **آهنگ:** تخت و یکنواخت، با کمی لبخند در صدا در بخش بو و چشیدن. واژه‌های «نرم»، «شیرین»، «گرم» کمی کشیده‌تر.
- **خروجی صوتی:** هر بخش یک MP3 مونو، ۶۴ تا ۹۶ kbps.

## ۳) ترکیب رنگی گوی و کنترل‌ها

- **عنوان ترکیب:** «خرمانی و طلایی باغچه»
- **روشن:** صفحه #F7F3EC → #EBD9C4 | گوی خورشیدی: مرکز #FFF1C7، میانه #E0A43A، لبه #B5652B | دکمه‌ی پخش: گرادیان #E0A43A → #B5652B با آیکون سفید | نوار پیشرفت: همان | متن: #3D2A1A | پنل کنترل: شیشه‌ی سفید ۵۵٪
- **تاریک:** صفحه #130E09 → #33220F | گوی: مرکز #FFD27A، میانه #F0A36A، لبه نارنجی تیره | دکمه‌ی پخش: گرادیان #FFD27A → #F0A36A با آیکون سفید | متن: #F3E6D6 | پنل کنترل: شیشه‌ی مشکی ۲۸٪
- **نوع گوی:** خورشید (sun) با نفس ۹ ثانیه‌ای. **ذرات:** نور طلایی ملایم، گل و بوهای ریزان در لبه‌ی صحنه.

## ۴) پرامپت بک‌گراند (دقیق و کامل)

دو تصویر لازم است: روشن و تاریک (همان صحنه با ترکیب یکسان). لایه‌ی محو رنگی خودکار اضافه می‌شود.

### نسخه‌ی روشن (انگلیسی؛ Midjourney / Flux / SDXL / Imagen)

```text
A sunny walled herb and flower garden in late morning, seen at eye level along a low stone path. Lavender and rosemary bushes, a bed of ripe tomatoes on wooden stakes, a clump of mint, a small bowl of fresh bread on a wooden table in the soft-focus background, apple blossoms on a low branch, warm golden light from the side, a few petals on the path. Rich but gentle colors, airy, high-key warmth, soft focus depth, photographic with gentle film softness. Palette: #F7F3EC, #EBD9C4, #B5652B, #E0A43A. Vertical 9:16, 1080x1920 px. Phone background behind a UI: keep the central 40% (30 to 70% of the height) soft, low-detail and low-contrast for a glowing sun orb, so let the table and bushes blur in the middle; keep the bottom 35% calm and slightly darker for a control panel; sharper interest (blossoms, tomatoes) only in the top third and margins. Gentle contrast, no bright hotspots, comfortable for hour-long viewing. No text, logos, watermark, people, faces, hands, animals, insects, buildings or UI elements.
```

### نسخه‌ی تاریک

```text
The same walled garden at warm dusk. Amber lantern light on the stone path, lavender and rosemary silhouettes, tomato plants in deep olive shadow, a soft golden glow from the bread table, faint evening haze over the beds, a few fallen petals catching light. Very low-key, quiet, soft contrast, photographic. Palette: #130E09, #33220F, #FFD27A, #F0A36A. Vertical 9:16, 1080x1920 px. Phone background behind a UI: keep the central 40% soft, low-detail and low-contrast for a glowing sun orb; keep the bottom 35% calm and darker for a control panel; interest in the top third and margins. No bright hotspots. No text, logos, watermark, people, faces, hands, animals, insects, buildings or UI elements.
```

### پرامپت منفی (هر دو نسخه)

```text
text, letters, watermark, logo, signature, people, face, hands, animals, insects, bees, buildings, cars, harsh contrast, oversaturated colors, neon, HDR halo, lens flare, chromatic aberration, noisy grain, border, frame, cartoon, illustration, 3D render look, clutter, thorns, weeds, mold
```

### مشخصات خروجی و نسخه‌ی ویدیویی اختیاری

- دو فایل `10-five-senses-garden-bg-light.webp` و `10-five-senses-garden-bg-dark.webp`، ۱۰۸۰×۱۹۲۰، کیفیت ۷۰ تا ۸۰، حداکثر ۱۵۰ تا ۲۰۰ کیلوبایت.
- لوپ ویدیویی (فعلاً نمایش داده نمی‌شود): `Seamless loop 8 to 10 seconds: petals drift slowly, leaves move in a light breeze, light shifts softly across the path. Camera locked off, 9:16, 1080x1920, 24 fps, MP4 under 1.5 MB, no audio.`

### تزریق صدا و بک‌گراند به HTML

```python
import base64, json, re, glob
n = '10-five-senses-garden'
h = open(n + '.html', encoding='utf-8').read()
uris = ['data:audio/mpeg;base64,' + base64.b64encode(open(f, 'rb').read()).decode() for f in sorted(glob.glob(n + '-0*.mp3'))]
h = re.sub(r'AUDIO=\[.*?\];', lambda m: 'AUDIO=' + json.dumps(uris) + ';', h, count=1, flags=re.S)
img = lambda p: 'data:image/webp;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
bg = 'const BG={light:"' + img(n + '-bg-light.webp') + '",dark:"' + img(n + '-bg-dark.webp') + '"};'
h = re.sub(r'const BG=\{.*?\};', lambda m: bg, h, count=1, flags=re.S)
open(n + '.html', 'w', encoding='utf-8').write(h)
```

تعداد MP3 باید ۶ باشد و ترتیب با بخش‌ها یکی.

### متن بخش‌ها برای تولید صدا

> هر بخش یک فایل صوتی است. خط «لحن» فقط برای خوانش است و خونده نمی‌شود.

#### بخش ۱: پیش از شروع، جا گرفتن
- **لحن:** گرم و ساده، کمی آروم‌تر از گفت‌وگوی عادی.

سلام. امروز قراره با هم به یه باغچهی کوچیک بریم که در آن همه‌ی حس‌ها با هم هستند. **[مکث ۳ ثانیه]**

هیچ لازم نیست چیزی رو درست انجام بدی. فقط بیا و ببین چه چیزهایی دوستت داری. **[مکث ۲ ثانیه]**

یه جای راحت پیدا کن. اگه نشستی، کمرت رو به صندلی بده. **[مکث ۳ ثانیه]**

چشم‌هات رو آروم ببند، یا نگاهت رو نرم روی زمین نگه دار. **[مکث ۴ ثانیه]**

دم و بازدم یه بار دیگه. **[مکث ۵ ثانیه]** و بازدم. **[مکث ۸ ثانیه]**

خوبه. بریم سراغ باغچه. **[مکث ۶ ثانیه]**

#### بخش ۲: ورود به باغ
- **لحن:** تصویری، با آهنگ آرام. بعد از هر توصیف مکث.

تو از در کوچه‌ای کوچیک وارد باغ می‌شی. یه راه سنگی به رنگ کمی گرم و نرم می‌ره جلو. **[مکث ۴ ثانیه]**

خورشید صبحگاهی رو روی چهره‌تون حس می‌کنی. نرم و گرم. **[مکث ۳ ثانیه]**

دست چپ یه بوته استینی لاوندر بوده. بیا و بین برگ‌ها بهش نزدیک بش. **[مکث ۶ ثانیه]**

از روی آن بو بکش. یه بوی تند و سرزنده می‌آیه: اسطوخودوسی، یا نعناع. **[مکث ۸ ثانیه]**

#### بخش ۳: بو و لمس
- **لحن:** نرم و بدنی، با اشاره به حس‌های جسمی. مکث‌ها را کامل رعایت کن.

حالا یه بوی دیگه رو انتخاب کن. بوی نعناع تازه، یا اسطوخودوس که اگه به برگش دست بزنی بو می‌ده. **[مکث ۴ ثانیه]**

دم، **[مکث ۴ ثانیه]** و بازدم. **[مکث ۶ ثانیه]**

حالا یه کم دستت رو به آرامی روی برگی نرم بکش. سطح برگ ملایمه و یه کم خنک. **[مکث ۵ ثانیه]**

یه تیماچی گوجه‌فرنگی بکن و ببین چقدر توی یه برگ آب هست. **[مکث ۸ ثانیه]**

باز هم بو کنی، این بار از بوی نعناع. **[مکث ۶ ثانیه]**

#### بخش ۴: چشیدن و صدا
- **لحن:** کندتر، با سکوت‌های واقعی. صداها را روی «دور» و «نزدیک» تنظیم کن.

اگه خواستی یه چیز بچشی، بهترین چیز شاید طعم نان و عسل است. فقط یه ذره بچشی، نه زیاد. **[مکث ۵ ثانیه]**

حالا گوش بده: صدای بال زدن یه زنبور، خیلی دور و آروم. **[مکث ۸ ثانیه]**

بعد برگ‌ها تو باد. صدای خشش برگ‌های چندتا سبزشون رو به هم می‌زنن. **[مکث ۸ ثانیه]**

و آن صدای آب که از گلدان می‌ریزه روی خاک. **[مکث ۸ ثانیه]**

اگه صدایی از اتاق به گوشت رسید، لازم نیست بیرونش کنی. بذار بشه بخشی از این باغ. **[مکث ۱۰ ثانیه]**

#### بخش ۵: حس‌های باغ کنار هم
- **لحن:** عمیق‌ترین و آرام‌ترین بخش. بدون فشار.

حالا همه‌ی حس‌ها رو به هم ببندیم. چشم: نور و رنگ. گوش: صدای آرام. بو: عطر گیاه. لمس: گرما و نرمی. **[مکث ۵ ثانیه]**

می‌تونی یکی رو برداشتن و عوضش کنی. دنبال یکی حس کن و برگردی. **[مکث ۴ ثانیه]**

یه نفس عمیق بکش. دم، **[مکث ۴ ثانیه]** و بازدم. **[مکث ۸ ثانیه]**

#### بخش ۶: برگشت به اتاق
- **لحن:** به‌تدریج روشن‌تر، گرم و کوتاه.

آرام از باغ بیرون بیا. اول چشم‌های بویی، بعد بوی آرام. **[مکث ۳ ثانیه]**

و با این حس‌ها به اتاق برگرد. به وزن بدنت برگرد. **[مکث ۴ ثانیه]**

چشم‌هات رو باز کن وقتی آماده بودی. **[مکث ۶ ثانیه]**

روز خوبی داشته باشی. **[مکث ۳ ثانیه]**

### یادداشت ایمنی و منابع علمی (برای اپ؛ داخل صفحه‌ی صوتی نمایش داده نمی‌شود)
- **ایمنی:** رانندگی یا کار با ماشین‌آلات گوش نده. اگر آلرژی بو یا طعم داری، این بخش‌ها را با تمرین‌های موازی عوض کن و در صورت نیاز با متخصص صحبت کن.
- Ulrich, R. S. (1984). View through a window may influence recovery from surgery. Science, 224(4647), 420–421.
- Park, B. J., Tsunetsugu, Y., Kasetani, T., Kagawa, T., & Miyazaki, Y. (2010). The physiological effects of Shinrin-yoku. Environmental Health and Preventive Medicine, 15(1), 18–26.
- Soga, M., Gaston, K. J., & Yamaura, Y. (2017). Gardening is beneficial for health: A meta-analysis. Preventive Medicine Reports, 5, 92–99.
- Zaccaro, A., et al. (2018). How breath-control can change your life: A systematic review on psycho-physiological correlates of slow breathing. Frontiers in Human Neuroscience, 12, 353.
- NCCIH (NIH). Relaxation Techniques: What You Need To Know. https://www.nccih.nih.gov/health/relaxation-techniques-what-you-need-to-know
