# آبی آرام — راهنمای جامع تولید صدا، بک‌گراند و رنگ‌بندی

## ۱) مشخصات فایل

- فایل HTML: `11-calm-waterspace.html` | شناسه: `cj-11` | مسیر: `Bucket/Html-files/app/calm/journey/11-calm-waterspace.html`
- تعداد فایل صوتی: ۶ (هر بخش یک فایل: `11-calm-waterspace-01.mp3` تا `-06.mp3`) | مدت کل (سرعت ۱٫۳×، با مکث‌ها): حدود ۱۹ دقیقه
- مخاطب: «تو» (مفرد) با افعال محاوره‌ای. صفحه پیوسته و همراه‌صدا است: بدون آکاردئون، بدون عنوان بخش، بدون متن اضافه.
- تم صفحه: خودکار تاریک/روشن، بدون دکمه. وب‌ویوی اپ: `setTheme('dark')` یا `setTheme('light')`.
- کنترل سرعت: آیکون چرخشی ۱۵ ثانیه‌ای، بدون متن.

## ۲) خوانش: لحن، سرعت و مکث‌ها

- **لحن کلی:** آرام، باز و شفا، مثل کسی که کنار آب نشسته و به آن نگاه می‌کنه. تُن یکدست و پایین، در بخش آب با کشیدگی بیشتر.
- **سبک گفتار:** محاوره‌ای مفرد (می‌تونی، بذار، ببینی، می‌شه، نمی‌خواد، اگه، یه). متن را مثل حرف زدن بخون.
- **سرعت:** ۱٫۳× (speed=1.3). طول مکث‌ها در سرعت بالا ثابت بمونه.
- **علامت مکث:** `[مکث N ثانیه]` = N ثانیه سکوت کامل. SSML: `<break time="Ns"/>`. اگر موتور صوتی نمی‌فهمد، سکوت را بعد از تولید در ویرایش صوت اضافه کن.
- **اندازه‌ی مکث‌ها:** کوتاه ۱ تا ۳ ثانیه | متوسط ۴ تا ۶ | بلند ۸ تا ۱۵. ۱۲ تا ۱۵ فقط در پایان بخش‌ها.
- **آهنگ:** تخت و یکنواخت؛ یاد موج و تکرارش را در آهنگ جمله‌ها بگیر. واژه‌های «آب»، «آرام»، «نفس» کمی کشیده‌تر.
- **خروجی صوتی:** هر بخش یک MP3 مونو، ۶۴ تا ۹۶ kbps.

## ۳) ترکیب رنگی گوی و کنترل‌ها

- **عنوان ترکیب:** «فیروزه‌ی آرام و نقره‌ی آبی»
- **روشن:** صفحه #EEF6F8 → #C9E6EE | گوی قطره‌ای (drops): مرکز شفاف با شیب #1E6E8C ۳۰٪، حلقه #1E6E8C، هاله #5FB5CF | دکمه‌ی پخش: گرادیان #5FB5CF → #1E6E8C با آیکون سفید | نوار پیشرفت: همان | متن: #163A48 | پنل کنترل: شیشه‌ی سفید ۵۵٪
- **تاریک:** صفحه #07141A → #0E2D38 | گوی: مرکز شفاف با شیب #6FCFE8 ۳۰٪، حلقه #6FCFE8، هاله #8FE3F2 | دکمه‌ی پخش: گرادیان #8FE3F2 → #6FCFE8 با آیکون سفید | نوار پیشرفت: همان | متن: #DDF0F5 | پنل کنترل: شیشه‌ی مشکی ۲۸٪
- **نوع گوی:** قطره (drops) با حلقه‌ی موجی ملایم. **ذرات:** آب و مه روی سطح.

## ۴) پرامپت بک‌گراند (دقیق و کامل)

دو تصویر لازم است: روشن و تاریک.

### نسخه‌ی روشن (انگلیسی؛ Midjourney / Flux / SDXL / Imagen)

```text
A calm still lake at early morning, seen from a low wooden jetty at water level. Glassy surface reflecting a pale sky with soft pink and pearl tones, gentle concentric ripples spreading from a single drop, low dark pine-covered hills in soft haze on the far shore, faint morning mist just above the water, a few reeds at the edge of the frame. Airy, high-key, soft and quiet, photographic with gentle film softness. Palette: #EEF6F8, #C9E6EE, #1E6E8C, #5FB5CF. Vertical 9:16, 1080x1920 px. Phone background behind a UI: keep the central 40% (30 to 70% of the height) soft, low-detail and low-contrast for a glowing orb, so the horizon and reflections sit in the upper third and the water in the middle stays nearly smooth; keep the bottom 35% calm and slightly darker for a control panel. Gentle contrast, no bright hotspots, comfortable for hour-long viewing. No text, logos, watermark, people, faces, hands, animals, boats, buildings or UI elements.
```

### نسخه‌ی تاریک

```text
The same still lake at deep blue night. Glassy dark teal water mirroring a faint moonlit sky, soft silver ripples from a single drop, dark hills as soft silhouettes, a thin band of mist just above the surface, a few stars high above. Very low-key, quiet, soft contrast, photographic. Palette: #07141A, #0E2D38, #6FCFE8, #8FE3F2. Vertical 9:16, 1080x1920 px. Phone background behind a UI: keep the central 40% soft, low-detail and low-contrast for a glowing orb; keep the bottom 35% calm and darker for a control panel; interest in the top third and margins. No bright hotspots. No text, logos, watermark, people, faces, hands, animals, boats, buildings or UI elements.
```

### پرامپت منفی (هر دو نسخه)

```text
text, letters, watermark, logo, signature, people, face, hands, animals, boats, jetty posts with graffiti, buildings, cars, harsh contrast, oversaturated colors, neon, HDR halo, lens flare, chromatic aberration, noisy grain, border, frame, cartoon, illustration, 3D render look, clutter, waves, storm, flood, dark murky water
```

### مشخصات خروجی و نسخه‌ی ویدیویی اختیاری

- دو فایل `11-calm-waterspace-bg-light.webp` و `11-calm-waterspace-bg-dark.webp`، ۱۰۸۰×۱۹۲۰، کیفیت ۷۰ تا ۸۰، حداکثر ۱۵۰ تا ۲۰۰ کیلوبایت.
- لوپ ویدیویی (فعلاً نمایش داده نمی‌شود): `Seamless loop 8 to 10 seconds: a single ripple spreads slowly outward and fades, mist drifts very slightly, the surface shimmers faintly. Camera locked off, 9:16, 1080x1920, 24 fps, MP4 under 1.5 MB, no audio.`

### تزریق صدا و بک‌گراند به HTML

```python
import base64, json, re, glob
n = '11-calm-waterspace'
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

#### بخش ۱: پیش از شروع، کنار آب
- **لحن:** گرم و ساده، کمی آروم‌تر از گفت‌وگوی عادی.

سلام. امروز قراره با هم یه دریاچهی آرام رو ببینیم. چند دقیقه بیشتر نیست و هیچ امتحانی در کار نیست. **[مکث ۳ ثانیه]**

آب به آرامی به آدم این احساس رو می‌ده که چیزی به او فشار نمی‌آره. بسیاریم از ما وقتی آرام‌ترین لحظه‌مون کنار آب بوده. **[مکث ۳ ثانیه]**

یه جای راحت پیدا کن. اگه نشستی، کمرت رو به صندلی بده و پاهات رو روی زمین بذار. **[مکث ۴ ثانیه]**

چشم‌هات رو آروم ببند یا نگاهت رو نرم روی آب نگه دار. **[مکث ۵ ثانیه]**

دم و بازدم. **[مکث ۴ ثانیه]** و بازدم آروم. **[مکث ۸ ثانیه]**

خوبه. بیا بریم نزدیک‌تر. **[مکث ۶ ثانیه]**

#### بخش ۲: نزدیک شدن به آب
- **لحن:** تصویری و آرام، با جمله‌های کشیده. بعد از هر توصیف مکث.

تصور کن یه مسیر چوبی کوچیک تو رو به سمت آب می‌بره. چوب‌ها کمی چرب و گرم‌رنگ هستن. **[مکث ۴ ثانیه]**

با هر قدم، صدای آب نزدیک‌تر می‌شه. به انتهای چوب رسیدی. **[مکث ۶ ثانیه]**

بشین روی چوب و پاها رو تو آب بذار. آب سرده، ولی خوشاینده. **[مکث ۸ ثانیه]**

به آن نقطه‌ی آرام دور نگاه کن. آسمان مونده و تکه‌ای از کوه خاموش به آب افتاده. **[مکث ۵ ثانیه]**

#### بخش ۳: قطره و حلقه‌ها
- **لحن:** آهسته و کمی آهنگین. بین توصیف‌ها سکوت واقعی بگذار.

حالا چشم‌هات رو آروم ببند و فقط به صدای آب گوش بده. **[مکث ۵ ثانیه]**

یک قطره کوچیک از بالا می‌افته و وقتی به آب می‌رسه، یه حلقه‌ی نرم می‌سازه. **[مکث ۸ ثانیه]**

این حلقه کش می‌آه بیرون، آروم، تا جایی که محو بشه. **[مکث ۸ ثانیه]**

و بعد حلقه‌ای دیگه، از جای دورتر. آب برگشته به حالت آینه. **[مکث ۵ ثانیه]**

به فکرتون نگاه کن. هر فکر یه قطره‌ست که رو آب افتاده و به آرامی محو شده. **[مکث ۸ ثانیه]**

#### بخش ۴: نفس با آرامش آب
- **لحن:** نرم و درونی، با دستورهای تنفس. دم و بازدم را با کشیدگی صدا نشون بده.

حالا نفس با آرامش آب هماهنگ کن. **[مکث ۳ ثانیه]**

وقتی آب آرام می‌آید، تو هم نفس بکش. دم، **[مکث ۴ ثانیه]** و بازدم، مثل آبی که آروم می‌ره و برمی‌گرده. **[مکث ۸ ثانیه]**

دم، **[مکث ۵ ثانیه]** و بازدم. **[مکث ۹ ثانیه]**

بدنت داره آروم می‌شه. یه سنگینیِ خوب روی صندلی. **[مکث ۴ ثانیه]**

#### بخش ۵: سپردن به آب
- **لحن:** عمیق‌ترین و آرام‌ترین بخش. کندتر بخون و بدون فشار.

حالا چشم‌هات رو آروم ببند و بذار آب به آرومی چشم‌انداز شما رو بشوره. **[مکث ۵ ثانیه]**

و اگه فکری آمد، لازم نیست نگهش داری. مثل یه قطره روی آب، به آرامی محو می‌شه. **[مکث ۸ ثانیه]**

با هر بازدم، سطح آب یه کم صاف‌تر می‌شه. **[مکث ۴ ثانیه]** بازدم. **[مکث ۸ ثانیه]**

نفس بعدی رو یه کم عمیق‌تر بکش. **[مکث ۴ ثانیه]** و بازدم کامل. **[مکث ۵ ثانیه]**

#### بخش ۶: برگشت از کنار آب
- **لحن:** به‌تدریج روشن‌تر و پرانرژی‌تر؛ همچنان نرم.

آرام از چوب بلند شو. قدم‌هات رو توی راه برگشتی بذار. **[مکث ۳ ثانیه]**

آب دور شده. سطحش آرامه. هر وقت خواستی، می‌تونی برگردی. **[مکث ۶ ثانیه]**

بدنت رو حس کن روی صندلی، وزنت، دستها، پاها. **[مکث ۴ ثانیه]**

چشم‌هات رو باز کن و اتاق رو ببین. **[مکث ۶ ثانیه]**

روز خوبی داشته باشی. **[مکث ۳ ثانیه]**

### یادداشت ایمنی و منابع علمی (برای اپ؛ داخل صفحه‌ی صوتی نمایش داده نمی‌شود)
- **ایمنی:** این تمرین رو هنگام رانندگی یا کار با ماشین‌آلات گوش نده. اگر وسط تمرین ترس یا خاطره‌ی آب به سراغت آمد، چشم‌ها را باز کن و به اتاق واقعی نگاه کن. این تمرین جایگزین درمان نیست.
- White, M., Smith, A., Humphryes, K., Pahl, S., Snelling, D., & Depledge, M. (2010). Blue space: The importance of water for preference, affect, and restorativeness ratings of natural and built scenes. Journal of Environmental Psychology, 30(4), 482–493.
- Völker, S., & Kistemann, T. (2011). The impact of blue space on human health and well-being. International Journal of Hygiene and Environmental Health, 214(6), 449–460.
- Gascon, M., et al. (2017). Outdoor blue spaces, human health and well-being: A systematic review of quantitative studies. International Journal of Hygiene and Environmental Health, 220(8), 1207–1221.
- Zaccaro, A., et al. (2018). How breath-control can change your life. Frontiers in Human Neuroscience, 12, 353.
- NCCIH (NIH). Relaxation Techniques: What You Need To Know. https://www.nccih.nih.gov/health/relaxation-techniques-what-you-need-to-know
