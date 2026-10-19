# قرارداد ذخیره‌سازی پس از اصلاح M9-QA-003

دامنهٔ اصلاح، انتخاب SharedPreferences در `LocalStore.prefsFor` است. فرمت داده، ثبت نتایج، API، backend، منو و محتوای ریاضی بازطراحی نشده‌اند.

| مورد | قرارداد |
|---|---|
| store پل ریاضی | `hamyar_math_html` |
| کلید native | `html:$kind:$packId`؛ نمونهٔ واقعی: `html:exam:C905_E00-SUM` |
| سند نمونه | `f00-tab05-easy-01`، `contentVersion=2026-10-19.qa-fix-1` |
| قالب JSON | `schema=hamyar-math-practice-1` و `documents[documentId]`؛ کل JSON بدون تبدیل به LocalStore داده می‌شود |
| حساب شناخته‌شده | `<storeName>__<StableIds.of("user", owner)>`؛ مسیر قبلی حفظ می‌شود |
| owner خالی یا whitespace، پس از فعال‌شدن isolation | `<storeName>__guest`؛ به basePrefs برنمی‌گردد |
| مهاجرت legacy | فقط owner غیرخالی برابر `_legacy_owner`؛ base اصلی حذف نمی‌شود و scope مقدار `_scope_initialized=true` می‌گیرد |
| legacy بی‌صاحب | به مهمان یا حساب جدید نسبت داده نمی‌شود؛ بایت‌های قدیمی حفظ می‌شوند |
| کلیدهای `auth_*` | فقط در store پیش‌فرض `roozhayeman_local` همچنان از basePrefs خوانده/نوشته می‌شوند |
| کلیدهای `auth_*` در storeهای دیگر | طبق رفتار قبلی، scoped می‌مانند |
| `forAccount("")` | به مهمان متصل می‌ماند، حتی اگر `auth_user_id` بعداً تغییر کند |
| `clearAll` در scope | marker مقداردهی اولیه باقی می‌ماند تا دادهٔ پاک‌شده دوباره از legacy وارد نشود |

`MathHtmlWebView.kt`، امضاهای `saveState(String)` و `loadState(): String`، `hamyar-persist.js`، routeها، HTMLها، Themeها و شناسه‌های محتوا در این اصلاح تغییر نکرده‌اند. hash فایل‌های نماینده در `contract-evidence.json` آمده است. fixture آزمون از کلید و ساختار واقعی سند جامع استفاده می‌کند و دادهٔ آزمایشی دارد؛ دادهٔ کاربر واقعی مصرف نشده است.

Robolectric اجرای JVM کد واقعی LocalStore و ترجیحات Android را پوشش می‌دهد. این شاهد، اجرای WebView داخل اپ نصب‌شده، ورود/خروج واقعی، backend یا sync را تأیید نمی‌کند. محتوای فعلی باید توسط درخواست‌کننده با کامیت جدید اپ تطبیق داده و سپس با manifest تازه به QA تحویل شود.
