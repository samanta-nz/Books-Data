#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_catalog.py — ساخت catalog.html (کاتالوگ شماره‌دار نمونه‌های صدا)

صداها به‌صورت base64 داخل خروجی جاسازی می‌شوند تا فایل بدون سرور و بدون اینترنت
در هر مرورگری پخش شود.

اجرا (از ریشهٔ مخزن):
    python voice-samples/build_catalog.py

نیازمندی: pip install imageio-ffmpeg numpy
"""

import base64
import hashlib
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze_voice as av

OUT = "voice-samples/catalog.html"

# (شماره, مسیر, جنس, مرحله, وضعیت, توضیح)
# وضعیت: approved | rejected | archive
SAMPLES = [
    (1, "voice-samples/samples/sample-fa-female.mp3", "زن", "دور ۱ — کوتاه", "rejected",
     "اولین نمونهٔ ساخته‌شده؛ ۲۴۶ هرتز، دور از مرجع."),
    (2, "voice-samples/samples/sample-fa-male.mp3", "مرد", "دور ۱ — کوتاه", "rejected",
     "اولین نمونهٔ مرد؛ ۱۲۹ هرتز با سرعت گفتار کند."),
    (3, "voice-samples/candidates/cand-a-female.mp3", "زن", "دور ۲ — کوتاه", "approved",
     "✅ صدای زن تأییدشده. همین فایل در approved/female-approved.mp3 بایگانی شده است."),
    (4, "voice-samples/candidates/cand-b-female.mp3", "زن", "دور ۲ — کوتاه", "rejected",
     "کاندید B؛ به مرجع نزدیک بود (۰٫۹۳۷) ولی تأیید نشد."),
    (5, "voice-samples/candidates/cand-a-male.mp3", "مرد", "دور ۲ — کوتاه", "rejected",
     "کاندید A مرد؛ ۱۰۷ هرتز ولی بسیار یکنواخت (IQR ۳۶٫۵)."),
    (6, "voice-samples/candidates/cand-b-male.mp3", "مرد", "دور ۲ — کوتاه", "rejected",
     "کاندید B مرد؛ ۱۵۲ هرتز، روشن و بالاتر از مرجع."),
    (7, "voice-samples/candidates/r3-cand-c-male.mp3", "مرد", "دور ۳ — کوتاه", "rejected",
     "کاندید C؛ ۱۱۸ هرتز با IQR فقط ۲۰٫۸ — خیلی یکنواخت."),
    (8, "voice-samples/candidates/r3-cand-d-male.mp3", "مرد", "دور ۳ — کوتاه", "rejected",
     "کاندید D؛ ۱۱۸ هرتز با IQR ۴۷٫۳."),
    (9, "voice-samples/candidates/r3-cand-e-male.mp3", "مرد", "دور ۳ — کوتاه", "rejected",
     "کاندید E؛ بالاترین امتیاز مرد در دور سوم (۰٫۸۵۷) ولی تأیید نشد."),
    (10, "voice-samples/candidates/r3-cand-f-male.mp3", "مرد", "دور ۳ — کوتاه", "approved",
     "✅ «صوت ۴» — صدای مرد تأییدشده. همین فایل در approved/male-approved.mp3 بایگانی شده است."),
    (11, "voice-samples/long/long-female-approved.mp3", "زن", "طولانی — ۱۰۴۷ نویسه", "approved",
     "✅ نمونهٔ طولانی صدای زن تأییدشده (#۳) — همین متن برای مرد هم خوانده شده."),
    (12, "voice-samples/long/long-male-e.mp3", "مرد", "طولانی — ۱۰۴۷ نویسه", "rejected",
     "نمونهٔ طولانی با کاندید E؛ جایگزین تأییدنشده."),
    (13, "voice-samples/long/long-male-f.mp3", "مرد", "طولانی — ۱۰۴۷ نویسه", "approved",
     "✅ نمونهٔ طولانی رسمی صدای مرد تأییدشده (#۱۰)."),
    (14, "voice-samples/long/long-female-uncertain-04.mp3", "زن", "طولانی — بایگانی", "archive",
     "بایگانی: نمونهٔ طولانی ساخته‌شده با کاندید B (#۴) پیش از نهایی‌شدن انتخاب زن."),
]

REFS = [
    ("مرجع زن (گفتگوی قبلی)", "voice-samples/voice-00-female.mp3",
     "۲۱٫۴۸ ثانیه · F0 ۱۸۸٫۲ · IQR ۱۰۲٫۸ · MD5 6478f350…a8d624"),
    ("مرجع مرد (گفتگوی قبلی)", "voice-samples/voice-02-male.mp3",
     "۲۱٫۸۴ ثانیه · F0 ۱۰۳٫۹ · IQR ۹۴٫۷ · MD5 f43e99d9…dcc723"),
]

STATUS = {
    "approved": ("✅ تأییدشده", "ok"),
    "rejected": ("✕ رد شده", "rj"),
    "archive": ("◻ بایگانی", "al"),
}

FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def fa(x):
    return str(x).translate(FA)


def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def datauri(path):
    b64 = base64.b64encode(open(path, "rb").read()).decode("ascii")
    return "data:audio/mpeg;base64," + b64


def raw_link(path):
    return ("https://github.com/samanta-nz/Books-Data/raw/"
            "arena/b7d9df99-books-data/" + path)


def main():
    ref_f = av.analyze("voice-samples/voice-00-female.mp3")
    ref_m = av.analyze("voice-samples/voice-02-male.mp3")

    rows, missing = [], []
    for num, path, role, stage, status, note in SAMPLES:
        if not os.path.exists(path):
            missing.append(path)
            continue
        r = av.analyze(path)
        sim = av.similarity(r, ref_f if role == "زن" else ref_m)["overall"]
        rows.append(dict(num=num, path=path, role=role, stage=stage, status=status,
                         note=note, r=r, sim=sim, iqr=round(r["f0_p75"] - r["f0_p25"], 1),
                         size=os.path.getsize(path), md5=md5(path)))
    if missing:
        print("فایل‌های گم‌شده:", missing)

    table, cards = [], []
    for x in rows:
        label, cls = STATUS[x["status"]]
        r = x["r"]
        metrics = (f"مدت {fa(f'{r[chr(100)+chr(117)+chr(114)+chr(97)+chr(116)+chr(105)+chr(111)+chr(110)+chr(95)+chr(115)]:.2f}')} ثانیه · "
                   f"F0 میانه <b>{fa(f'{r[chr(102)+chr(48)+chr(95)+chr(109)+chr(101)+chr(100)+chr(105)+chr(97)+chr(110)]:.1f}')}</b> هرتز · "
                   f"IQR {fa(f'{x[chr(105)+chr(113)+chr(114)]:.1f}')} · "
                   f"مرکز طیفی {fa(round(r['spectral_centroid_hz']))} · "
                   f"هجا/ث {fa(f'{r[chr(115)+chr(121)+chr(108)+chr(108)+chr(97)+chr(98)+chr(108)+chr(101)+chr(115)+chr(95)+chr(112)+chr(101)+chr(114)+chr(95)+chr(115)+chr(101)+chr(99)]:.2f}')} · "
                   f"شباهت <b>{fa(f'{x[chr(115)+chr(105)+chr(109)]:.3f}')}</b>")
        table.append(
            f'      <tr class="{cls}"><td class="n">#{fa(x["num"])}</td><td>{x["role"]}</td>'
            f'<td>{x["stage"]}</td><td class="num">{fa(f"{r[chr(100)+chr(117)+chr(114)+chr(97)+chr(116)+chr(105)+chr(111)+chr(110)+chr(95)+chr(115)]:.1f}")}</td>'
            f'<td class="num">{fa(f"{r[chr(102)+chr(48)+chr(95)+chr(109)+chr(101)+chr(100)+chr(105)+chr(97)+chr(110)]:.1f}")}</td>'
            f'<td class="num">{fa(f"{x[chr(105)+chr(113)+chr(114)]:.1f}")}</td>'
            f'<td class="num">{fa(f"{x[chr(115)+chr(105)+chr(109)]:.3f}")}</td>'
            f'<td class="s {cls}">{label}</td></tr>')
        cards.append(f'''  <article class="card {cls}">
    <div class="num">#{fa(x["num"])}</div>
    <div class="body">
      <div class="top">
        <span class="st {cls}">{label}</span>
        <span class="role">{x["role"]}</span>
        <span class="stage">{x["stage"]}</span>
      </div>
      <p class="metrics">{metrics}</p>
      <audio controls preload="none" src="{datauri(x["path"])}"></audio>
      <p class="dl"><a href="{raw_link(x["path"])}" target="_blank" rel="noopener">فایل خام در گیت‌هاب ↗</a></p>
      <p class="note">{html.escape(x["note"])}</p>
      <p class="path"><code>{html.escape(x["path"])}</code> · {fa(f"{x[chr(115)+chr(105)+chr(122)+chr(101)]/1024:.0f}")} کیلوبایت · MD5 {x[chr(109)+chr(100)+chr(53)][:8]}…{x[chr(109)+chr(100)+chr(53)][-6:]}</p>
    </div>
  </article>''')

    ref_cards = "\n".join(
        f'''    <div class="ref">
      <h3>{name}</h3>
      <p class="note">{meta}</p>
      <audio controls preload="none" src="{datauri(path)}"></audio>
    </div>''' for name, path, meta in REFS)

    doc = f'''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>کاتالوگ شماره‌دار نمونه‌های صدا</title>
<style>
  :root{{--bg:#0d1412;--card:#151f1b;--line:#26362e;--ink:#eef5f0;--muted:#9db3a8;
        --ok:#4ec9a0;--al:#8fa7c7;--rj:#e06c8b}}
  *{{box-sizing:border-box}}
  body{{margin:0;padding:28px 16px 64px;font-family:"Vazirmatn","Segoe UI",Tahoma,sans-serif;
       background:radial-gradient(1200px 560px at 12% -10%,#19342a 0%,var(--bg) 62%);color:var(--ink)}}
  .wrap{{max-width:980px;margin:0 auto}}
  h1{{font-size:1.55rem;margin:0 0 8px}}
  .sub{{color:var(--muted);font-size:.92rem;line-height:1.95;margin:0 0 18px}}
  .final{{background:rgba(78,201,160,.08);border:1px solid rgba(78,201,160,.35);border-radius:14px;
         padding:12px 16px;font-size:.88rem;line-height:2;margin-bottom:20px}}
  .final b{{color:#7ee0bb}}
  .legend{{display:flex;gap:14px;flex-wrap:wrap;font-size:.78rem;color:var(--muted);margin-bottom:22px}}
  .legend span{{display:inline-flex;align-items:center;gap:6px}}
  .dot{{width:9px;height:9px;border-radius:50%;display:inline-block}}
  h2.sec{{font-size:1.05rem;margin:26px 0 12px;padding-bottom:8px;border-bottom:1px solid var(--line);color:#cfe3d8}}
  table{{width:100%;border-collapse:collapse;font-size:.83rem;background:rgba(255,255,255,.02);
        border:1px solid var(--line);border-radius:12px;overflow:hidden}}
  th,td{{border-bottom:1px solid var(--line);padding:8px;text-align:right}}
  th{{color:var(--muted);font-weight:500;font-size:.75rem;background:rgba(255,255,255,.03)}}
  td.num{{direction:ltr;text-align:left;font-variant-numeric:tabular-nums}}
  td.n{{font-weight:700;color:#fff;direction:ltr;text-align:center;width:44px}}
  tr:last-child td{{border-bottom:none}}
  tr.ok td{{background:rgba(78,201,160,.09)}}
  td.s{{font-size:.76rem}}
  td.ok{{color:var(--ok)}} td.al{{color:var(--al)}} td.rj{{color:var(--rj)}}
  .card{{display:flex;gap:14px;background:linear-gradient(180deg,rgba(255,255,255,.035),rgba(255,255,255,.01)),var(--card);
        border:1px solid var(--line);border-radius:16px;padding:14px;margin-bottom:12px}}
  .card.ok{{border-color:rgba(78,201,160,.6);box-shadow:0 0 0 1px rgba(78,201,160,.2) inset}}
  .num{{font-size:1.5rem;font-weight:800;color:#fff;min-width:62px;text-align:center;
        background:rgba(255,255,255,.05);border-radius:12px;padding:8px 4px;height:fit-content;
        direction:ltr;border:1px solid var(--line)}}
  .body{{flex:1;min-width:0}}
  .top{{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:6px}}
  .st{{font-size:.72rem;padding:2px 9px;border-radius:999px;border:1px solid}}
  .st.ok{{color:var(--ok);border-color:rgba(78,201,160,.5);background:rgba(78,201,160,.1)}}
  .st.al{{color:var(--al);border-color:rgba(143,167,199,.45);background:rgba(143,167,199,.08)}}
  .st.rj{{color:var(--rj);border-color:rgba(224,108,139,.42);background:rgba(224,108,139,.07)}}
  .role{{font-size:.78rem;color:#dfeee7}}
  .stage{{font-size:.74rem;color:var(--muted)}}
  .metrics{{color:var(--muted);font-size:.78rem;line-height:1.95;margin:0 0 8px}}
  .metrics b{{color:#eaf6f0}}
  audio{{width:100%}}
  .dl{{font-size:.72rem;margin:6px 0 0}}
  .dl a{{color:#7fb9a4;text-decoration:none;border-bottom:1px dotted rgba(127,185,164,.5)}}
  .note{{font-size:.78rem;color:#b9cbc1;line-height:1.9;margin:8px 0 0}}
  .path{{font-size:.7rem;color:#7f948a;margin:6px 0 0;line-height:1.8;word-break:break-all}}
  code{{background:rgba(255,255,255,.06);padding:1px 5px;border-radius:5px;direction:ltr;display:inline-block;font-size:.72rem}}
  .refs{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
  @media(max-width:700px){{.refs{{grid-template-columns:1fr}}}}
  .ref{{background:rgba(255,255,255,.025);border:1px solid var(--line);border-radius:14px;padding:14px}}
  .ref h3{{font-size:.9rem;margin:0 0 6px}}
  footer{{color:var(--muted);font-size:.77rem;line-height:2;margin-top:26px;border-top:1px solid var(--line);padding-top:14px}}
</style>
</head>
<body>
<div class="wrap">
  <h1>کاتالوگ شماره‌دار نمونه‌های صدا</h1>
  <p class="sub">همهٔ نمونه‌های ساخته‌شده با شمارهٔ ثابت. صداها داخل خودِ این فایل جاسازی شده‌اند؛
  نیازی به اینترنت یا سرور نیست.</p>

  <div class="final">
    <b>انتخاب نهایی:</b> زن → <b>#۳</b> (F0 ۲۱۹٫۲) · مرد → <b>#۱۰</b> (F0 ۱۶۳٫۳) ·
    نمونه‌های طولانی هم با همین دو صدا: <b>#۱۱</b> و <b>#۱۳</b>. بقیهٔ نمونه‌ها رد شده‌اند.
  </div>

  <div class="legend">
    <span><i class="dot" style="background:var(--ok)"></i> تأییدشده</span>
    <span><i class="dot" style="background:var(--al)"></i> بایگانی</span>
    <span><i class="dot" style="background:var(--rj)"></i> رد شده</span>
    <span>· «شباهت» نسبت به مرجع هم‌جنس سنجیده شده</span>
  </div>

  <h2 class="sec">جدول سریع</h2>
  <table>
    <thead>
      <tr><th>شماره</th><th>صدا</th><th>مرحله</th><th>مدت (ث)</th><th>F0 میانه</th><th>IQR</th><th>شباهت</th><th>وضعیت</th></tr>
    </thead>
    <tbody>
{chr(10).join(table)}
    </tbody>
  </table>

  <h2 class="sec">همهٔ نمونه‌ها با پخش‌کننده</h2>
{chr(10).join(cards)}

  <h2 class="sec">مرجع‌ها (منتقل‌شده از گفتگوی قبلی — ساختهٔ من نیستند)</h2>
  <div class="refs">
{ref_cards}
  </div>

  <footer>
    {fa(len(rows))} نمونهٔ ساخته‌شده + ۲ مرجع منتقل‌شده. فایل‌های تأییدشده در <code>approved/</code> بایگانی شده‌اند؛
    ثبت رسمی در <code>approved/approved.json</code>. ساخت مجدد این صفحه:
    <code>python voice-samples/build_catalog.py</code>
  </footer>
</div>
</body>
</html>
'''
    open(OUT, "w", encoding="utf-8").write(doc)
    print(f"wrote {OUT} ({len(doc)/1024/1024:.2f} MB), {len(rows)} samples")
    for x in rows:
        print(f"#{x['num']:>2} {x['role']:4} {x['stage']:22} {x['status']:9} "
              f"f0 {x['r']['f0_median']:6.1f} iqr {x['iqr']:6.1f} sim {x['sim']:.3f}")


if __name__ == "__main__":
    main()
