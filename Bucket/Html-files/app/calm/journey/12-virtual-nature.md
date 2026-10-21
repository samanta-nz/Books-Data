# طبیعت مجازی — راهنمای جامع تولید صدا، بک‌گراند و رنگ‌بندی

## ۱) مشخصات فایل

- فایل HTML: `12-virtual-nature.html` | شناسه: `cj-12` | مسیر: `Bucket/Html-files/app/calm/journey/12-virtual-nature.html`
- تعداد فایل صوتی: ۶ (هر بخش یک فایل: `12-virtual-nature-01.mp3` تا `-06.mp3`) | مدت کل (سرعت ۱٫۳×، با مکث‌ها): حدود ۱۸ دقیقه
- مخاطب: «تو» (مفرد) با افعال محاوره‌ای. صفحه پیوسته و همراه‌صدا است: بدون آکاردئون، بدون عنوان بخش، بدون متن اضافه.
- تم صفحه: خودکار تاریک/روشن، بدون دکمه. وب‌ویوی اپ: `setTheme('dark')` یا `setTheme('light')`.
- کنترل سرعت: آیکون چرخشی ۱۵ ثانیه‌ای، بدون متن.

## ۲) خوانش: لحن، سرعت و مکث‌ها

- **لحن کلی:** آرام و با آرامش، مثل یه راهنمای مهربون که با صدای نرم تو رو به یه جای خیالی می‌بره. تُن یکدست و پایین، بدون اوج.
- **سبک گفتار:** محاوره‌ای مفرد (می‌تونی، بذار، ببینی، می‌شه، نمی‌خواد، اگه، یه). متن را مثل حرف زدن بخون.
- **سرعت:** ۱٫۳× (speed=1.3). طول مکث‌ها در سرعت بالا ثابت بمونه.
- **علامت مکث:** `[مکث N ثانیه]` = N ثانیه سکوت کامل. SSML: `<break time="Ns"/>`. اگر موتور صوتی نمی‌فهمد، سکوت را بعد از تولید در ویرایش صوت اضافه کن.
- **اندازه‌ی مکث‌ها:** کوتاه ۱ تا ۳ ثانیه | متوسط ۴ تا ۶ | بلند ۸ تا ۱۵. ۱۲ تا ۱۵ فقط در پایان بخش‌ها.
- **آهنگ:** تخت و یکنواخت. واژه‌های «تصویر»، «نفس»، «آرام» کمی کشیده‌تر. هرجا گفتی از صفحه یا دستگاه هست، لحن رو به آرامی و بدون هشدار ببر.
- **خروجی صوتی:** هر بخش یک MP3 مونو، ۶۴ تا ۹۶ kbps.

## ۳) ترکیب رنگی گوی و کنترل‌ها

- **عنوان ترکیب:** «نیلی مخملی و سفیده‌ی طلوع»
- **روشن:** صفحه #F1F4F9 → #DCE3F2 | گوی ماه‌مانند: مرکز سفید ۹۵٪، میانه #9BAEE8، لبه #4A5FA8 | دکمه‌ی پخش: گرادیان #9BAEE8 → #4A5FA8 با آیکون سفید | نوار پیشرفت: همان | متن: #202A4A | پنل کنترل: شیشه‌ی سفید ۵۵٪
- **تاریک:** صفحه #0B0E1A → #1B2140 | گوی: مرکز سفید ۹۵٪، میانه #C1CDFF، لبه #9DB0F0 | دکمه‌ی پخش: گرادیان #C1CDFF → #9DB0F0 با آیکون سفید | نوار پیشرفت: همان | متن: #E4E9FA | پنل کنترل: شیشه‌ی مشکی ۲۸٪
- **نوع گوی:** ماه (moon) با نفس ۹ ثانیه‌ای. **ذرات:** ستاره‌های نرم و گردنه‌ی نور دور از آسمان.

## ۴) پرامپت بک‌گراند (دقیق و کامل)

دو تصویر لازم است: روشن و تاریک.

### نسخه‌ی روشن (انگلیسی؛ Midjourney / Flux / SDXL / Imagen)

```text
A soft, abstract yet natural landscape of rolling misty hills at dawn, seen from a quiet high ridge. Gentle layers of pale lavender and blue-grey hills fading into haze, a thin band of silver light on a distant lake, a few tall soft grasses in the foreground, delicate cloud forms in a pale sky. A dreamy but grounded, quietly realistic mood, airy, high-key, soft focus depth, photographic with gentle film softness, no harsh geometry. Palette: #F1F4F9, #DCE3F2, #4A5FA8, #9BAEE8. Vertical 9:16, 1080x1920 px. Phone background behind a UI: keep the central 40% (30 to 70% of the height) soft, low-detail and low-contrast for a glowing moon orb, so the hill layers blur softly in the middle; keep the bottom 35% calm and slightly darker for a control panel; interest in the top third (clouds) and margins. Gentle contrast, no bright hotspots, comfortable for hour-long viewing. No text, logos, watermark, people, faces, hands, animals, buildings, screens, digital grids, neon or UI elements.
```

### نسخه‌ی تاریک

```text
The same misty hill landscape at deep blue night. Soft moonlight on layered hills in dark indigo, a faint silver lake far below, a few faint stars among thin clouds, mist glowing very softly lavender near the ground, grass silhouettes in the foreground. Very low-key, quiet, soft contrast, photographic. Palette: #0B0E1A, #1B2140, #C1CDFF, #9DB0F0. Vertical 9:16, 1080x1920 px. Phone background behind a UI: keep the central 40% soft, low-detail and low-contrast for a glowing moon orb; keep the bottom 35% calm and darker for a control panel; interest in the top third and margins. No bright hotspots. No text, logos, watermark, people, faces, hands, animals, buildings, screens, digital grids, neon or UI elements.
```

### پرامپت منفی (هر دو نسخه)

```text
text, letters, watermark, logo, signature, people, face, hands, animals, buildings, screens, monitors, VR headset, digital grid, pixel patterns, circuit lines, neon, harsh contrast, oversaturated colors, HDR halo, lens flare, chromatic aberration, noisy grain, border, frame, cartoon, illustration, 3D render look, clutter, storm, lightning
```

### مشخصات خروجی و نسخه‌ی ویدیویی اختیاری

- دو فایل `12-virtual-nature-bg-light.webp` و `12-virtual-nature-bg-dark.webp`، ۱۰۸۰×۱۹۲۰، کیفیت ۷۰ تا ۸۰، حداکثر ۱۵۰ تا ۲۰۰ کیلوبایت.
- لوپ ویدیویی (فعلاً نمایش داده نمی‌شود): `Seamless loop 8 to 10 seconds: clouds drift very slowly across the sky, mist moves gently between the hill layers, grass sways faintly. Camera locked off, no screens or digital elements, 9:16, 1080x1920, 24 fps, MP4 under 1.5 MB, no audio.`

## ۵) تزریق صدا و بک‌گراند به HTML

```python
import base64, json, re, glob
n = '12-virtual-nature'
h = open(n + '.html', encoding='utf-8').read()
uris = ['data:audio/mpeg;base64,' + base64.b64encode(open(f, 'rb').read()).decode() for f in sorted(glob.glob(n + '-0*.mp3'))]
h = re.sub(r'AUDIO=\[.*?\];', lambda m: 'AUDIO=' + json.dumps(uris) + ';', h, count=1, flags=re.S)
img = lambda p: 'data:image/webp;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
bg = 'const BG={light:"' + img(n + '-bg-light.webp') + '",dark:"' + img(n + '-bg-dark.webp') + '"};'
h = re.sub(r'const BG=\{.*?\};', lambda m: bg, h, count=1, flags=re.S)
open(n + '.html', 'w', encoding='utf-8').write(h)
```

تعداد MP3 باید ۶ باشد و ترتیب با بخش‌ها یکی. صفحه خودکار تاریک/روشن می‌شود.

## ۶) متن بخش‌ها برای تولید صدا

> هر بخش یک فایل صوتی است. خط «لحن» فقط برای خوانش است و خونده نمی‌شود.

#### بخش ۱: پیش از شروع، درباره‌ی این تمرین
- **لحن:** نرم و ساده، کمی آروم‌تر از گفت‌وگوی عادی.

سلام. امروز قراره یه طبیعت آرام رو تصور بکنیم، حتی اگه فقط در ذهن باشه. **[مکث ۳ ثانیه]**

بعضی وقت‌ها سخته با طبیعت واقعی باشی، و بعضی وقت‌ها شهر و صفحه و زندگی تند به تو فشار می‌آورن. این تمرین همین‌جور وقتی می‌تونه یه مکان آرام به وجود بیاره، بدون اینکه چیزی رو جایگزین خود طبیعت کنه. **[مکث ۴ ثانیه]**

جای راحتی پیدا کن. اگه نشستی، کمرت رو به صندلی بده و پاهات رو روی زمین بذار. **[مکث ۳ ثانیه]**

چشم‌هات رو آروم ببند یا نگاهت رو نرم روی زمین نگه دار. **[مکث ۴ ثانیه]**

دم و بازدم آروم. **[مکث ۴ ثانیه]** و بازدم. **[مکث ۸ ثانیه]**

خوبه. بیا بریم به طبیعت ورد کنیم. **[مکث ۶ ثانیه]**

#### بخش ۲: ورود به چشم‌انداز
- **لحن:** تصویری و آرام، با جمله‌های کشیده. بعد از هر توصیف مکث.

تصور کن از یه کوچه‌ی آرام شروع می‌کنی به بالا رفتن به تپه‌های نرم و مه‌گرفته. **[مکث ۴ ثانیه]**

روی لایه‌ی اول تپه یه علفزار بلند و بالای آن بالاشون رنگی از آبی آرام. **[مکث ۳ ثانیه]**

و بعد لایه‌های بیشتری که رو هم رو هم قرار گرفتن، هر کدوم کمی روشن‌تر از قبلی. **[مکث ۵ ثانیه]**

بالای سرت یه ابر نازک سفیده. می‌خوای چشم‌ت رو به اون بدوزی، ولی لازم نیست. **[مکث ۸ ثانیه]**

و آخر از همه و بیش از همه، یه خط نقره‌ای کمرنگ دور و بی‌رنگ و زیبا. **[مکث ۶ ثانیه]**

#### بخش ۳: صدای باد در دره
- **لحن:** کندتر و آهنگین، با سکوت‌های واقعی. صدا را روی «دور» و «نزدیک» تنظیم کن.

حالا گوش بده. باد یه بار به آرامی از روی تپه‌ها می‌آیه و با نرمی می‌ره. **[مکث ۵ ثانیه]**

یه جریان آرام دور از آن طرف دره. صداش مثل نجوایی نرم است. **[مکث ۸ ثانیه]**

اگه صدایی از اتاق واقعی به گوشت رسید، لازم نیست بیرونش کنی. بذار بشه بخشی از این نجوا. **[مکث ۱۰ ثانیه]**

وقتی محو شدی، یه صدای دیگه جایگزین می‌شه. همون آرامی. **[مکث ۸ ثانیه]**

#### بخش ۴: نفس با افق
- **لحن:** نرم و بدنی، با دستورهای تنفس. دم و بازدم را با کشیدگی صدا نشون بده.

نفس بکش و با چشم بسته با آسمان همراه شو. **[مکث ۳ ثانیه]**

دم می‌گیری، **[مکث ۴ ثانیه]** و بازدم مثل ابری که آروم می‌ره. **[مکث ۸ ثانیه]**

دم، **[مکث ۵ ثانیه]** و بازدم. **[مکث ۹ ثانیه]**

بدنت سبک شده. وزنش روی صندلی یا تخت، و نفستو به آرامی حس می‌کنی. **[مکث ۴ ثانیه]**

#### بخش ۵: جای رسیدن به آرامش
- **لحن:** عمیق‌ترین و آرام‌ترین بخش. بدون فشار و بدون الزام.

حالا تو بالای این تپه‌های آرام استی. از همه‌ی چیزها دوری، فقط این روشنیِ نرم رو حس می‌کنی. **[مکث ۵ ثانیه]**

اگر ذهنتو فکری سنگین برداشته، لازم نیست آن را بگیری. می‌تونی مثل ابر به آن نگاه کنی و بذاری بره. **[مکث ۸ ثانیه]**

یه نفس عمیق دیگه. دم، **[مکث ۴ ثانیه]** و بازدم کامل. **[مکث ۵ ثانیه]**

اگر خوشت می‌آد، همین نقطه رو نگه داشته باش و ببین چند وقتی از آن دور شدی. **[مکث ۸ ثانیه]**

#### بخش ۶: برگشت به اتاق
- **لحن:** به‌تدریج روشن‌تر، با جمله‌های کوتاه و گرم.

آرام از افق برگرد. ولی این آرامش با تو می‌مونه. **[مکث ۳ ثانیه]**

حالا به بدنت برگرد. وزنت، دستها، پاها. **[مکث ۴ ثانیه]**

چشم‌هات رو آروم باز کن وقتی آماده بودی. **[مکث ۶ ثانیه]**

یه نکته‌ی کوچیک برای بعد: اگر وقت یا فضای چشم‌انداز برات نیست، همین چند نفس آرام کافیه. این هم مثل استراحت کوتاه وقتی چشم‌هات بسته بود. **[مکث ۵ ثانیه]**

اگر بعد از تمرین ناراحت یا بی‌قرار شدی، نگران نباش، تمرین را کنار بگذار و از چیزی که واقعاً اطرافت به آن نگاه کن. اگر این حس ادامه پیدا کرد، با یه متخصص سلامت روان صحبت کن. **[مکث ۳ ثانیه]**

روز خوبی داشته باشی. **[مکث ۳ ثانیه]**

### یادداشت ایمنی و منابع علمی (برای اپ؛ داخل صفحه‌ی صوتی نمایش داده نمی‌شود)
- **ایمنی:** این تمرین را هنگام رانندگی یا کار با ماشین‌آلات گوش نده. اگر وسط تمرین احساس ناخوشایند آمد، چشم‌ها را باز کن و به اتاق واقعی نگاه کن. اگر وقتی با صفحه و محیط دیجیتال سرگرمی زیاد داری، این بخش را به زمان دیگه‌ای بگذار. این تمرین جایگزین درمان نیست.
- Kaplan, S. (1995). The restorative benefits of nature: Toward an integrative framework. Journal of Environmental Psychology, 15(3), 169–182.
- Ulrich, R. S. (1984). View through a window may influence recovery from surgery. Science, 224(4647), 420–421.
- Bratman, G. N., Hamilton, J. P., Hahn, K. S., Daily, G. C., & Gross, J. J. (2015). Nature experience reduces rumination and subgenual prefrontal cortex activation. PNAS, 112(28), 8567–8572.
- Hartig, T., Mitchell, R., de Vries, S., & Frumkin, H. (2014). Nature and health. Annual Review of Public Health, 35, 207–228.
- Zaccaro, A., et al. (2018). How breath-control can change your life. Frontiers in Human Neuroscience, 12, 353.
- NCCIH (NIH). Relaxation Techniques: What You Need To Know. https://www.nccih.nih.gov/health/relaxation-techniques-what-you-need-to-know
