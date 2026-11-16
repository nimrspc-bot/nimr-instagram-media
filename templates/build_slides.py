import re, subprocess, os
D = "/home/claude/ig"
V2 = "/home/claude/v2"
FONTS = "/home/claude/fonts/node_modules/@fontsource"

def ff(fam, pkg, subsets, weights):
    out = ""
    for s, rng in subsets:
        for w in weights:
            out += f'@font-face{{font-family:"{fam}";src:url("file://{FONTS}/{pkg}/files/{pkg}-{s}-{w}-normal.woff");font-weight:{w};unicode-range:{rng};}}\n'
    return out
FONT = ff("Cairo","cairo",[("arabic","U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFF,U+200C-200F"),("latin","U+0000-00FF,U+2000-206F")],[400,600,700,800]) + \
       ff("Mont","montserrat",[("latin","U+0000-00FF,U+2000-206F")],[400,500,600,700,800])

CSS = FONT + f'''
*{{box-sizing:border-box;margin:0}}
html,body{{width:1080px;height:1350px;overflow:hidden}}
body{{font-family:"Cairo";color:#0a2350;position:relative;
  background:url("file://{V2}/pat_light.svg") 0 0/120px 120px, radial-gradient(120% 80% at 80% 0%,#d9ecff 0%,#f4f9ff 55%,#fff 100%)}}
.top{{position:absolute;top:56px;left:64px;right:64px;display:flex;justify-content:space-between;align-items:center}}
.top img{{height:140px}}
.tag{{background:#0a2350;color:#fff;font:800 30px "Cairo";padding:10px 30px;border-radius:40px;display:flex;align-items:center;gap:14px}}
.tag b{{font:800 30px "Mont";color:#f6c453}}
.n{{font-family:"Mont";font-weight:700;unicode-bidi:isolate}}
.foot{{position:absolute;left:0;right:0;bottom:0;height:120px;background:linear-gradient(90deg,#0a2350,#124a9c 70%,#1a6fc4);
  display:flex;align-items:center;justify-content:space-between;padding:0 64px;color:#fff}}
.foot:before{{content:"";position:absolute;left:0;right:0;top:0;height:7px;background:linear-gradient(90deg,#e3a72f,#f6d27c,#e3a72f)}}
.foot .ph{{font:800 44px "Mont";letter-spacing:1px;display:flex;align-items:center;gap:16px}}
.foot .ph svg{{width:44px;height:44px;color:#f6c453}}
.foot .sl{{font:700 28px "Cairo";color:#dbe8fa}}
.flag{{display:inline-flex;flex-direction:column;width:14px;height:34px;border-radius:3px;overflow:hidden;margin-inline-start:14px;box-shadow:0 0 0 2px rgba(255,255,255,.6)}}
.flag i{{flex:1}}.flag i:nth-child(1){{background:#fff}}.flag i:nth-child(2){{background:#db161b}}.flag i:nth-child(3){{background:#008000}}
.page{{position:absolute;top:220px;left:64px;right:64px;bottom:150px;display:flex;flex-direction:column}}
.hl{{color:#1667c4}}
.dots{{position:absolute;bottom:150px;left:0;right:0;display:flex;justify-content:center;gap:12px}}
.dots i{{width:14px;height:14px;border-radius:7px;background:#c9daef}}.dots i.on{{width:44px;background:#e3a72f}}
.card{{background:#fff;border:2px solid #dfe9f5;border-radius:36px;padding:44px 52px;box-shadow:0 14px 40px rgba(10,35,80,.08)}}
.lbl{{display:flex;align-items:center;gap:16px;font:800 44px "Cairo";color:#0a2350;margin-bottom:18px}}
.lbl svg{{width:46px;height:46px;color:#1677d6}}
.en{{font:500 30px/1.5 "Mont";color:#5a6f8c;direction:ltr;text-align:left}}
.en b{{color:#1667c4}}
.swipe{{position:absolute;bottom:150px;left:64px;font:700 30px "Cairo";color:#1677d6;display:flex;align-items:center;gap:10px}}
'''

PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3h4l2 5-3 2a12 12 0 0 0 6 6l2-3 5 2v4a2 2 0 0 1-2 2A18 18 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>'
I = {
 "bulb": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/>',
 "pen": '<path d="M4 20h4L19 9l-4-4L4 16z"/>',
 "book": '<path d="M4 4h6a3 3 0 0 1 2 1 3 3 0 0 1 2-1h6v15h-6a2 2 0 0 0-2 2 2 2 0 0 0-2-2H4z"/><path d="M12 5v16"/>',
 "star": '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
 "warn": '<path d="M12 3 2 20h20z"/><path d="M12 10v4M12 17v.1"/>',
 "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4M8 13v-2M11 13V9M14 13v-3"/>',
 "box": '<path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/>',
}
def ic(n, sw=2): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{I[n]}</svg>'

def shell(body, i, total, swipe=True, tag=True):
    dots = "".join(f'<i class="{"on" if j==i else ""}"></i>' for j in range(total))
    t = '<div class="tag">مصطلح الأسبوع <b>01</b></div>' if tag else '<span></span>'
    sw = '<div class="swipe">اسحب ←</div>' if swipe else ''
    return f'''<!doctype html><html dir="rtl"><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="top">{t}<img src="file:///home/claude/logo.png"></div>
{body}
<div class="dots" dir="ltr">{dots}</div>{sw}
<div class="foot"><div class="ph" dir="ltr">{PHONE}91474750</div><div class="sl">معك في كل خطوة.. نحو مستقبل أكثر أماناً<span class="flag"><i></i><i></i><i></i></span></div></div>
</body></html>'''

S = []
# 1 cover
S.append(shell(f'''
<div class="page" style="align-items:center;justify-content:center;text-align:center">
  <div style="width:250px;height:280px;border-radius:125px 125px 40px 40px;background:linear-gradient(160deg,#0a2350,#1f8be0);
     display:flex;align-items:center;justify-content:center;color:#fff;box-shadow:0 0 0 12px #fff,0 0 0 16px #e3a72f,0 30px 60px rgba(10,35,80,.25)">
     <div style="width:140px;height:140px">{ic("box",1.6)}</div></div>
  <div style="font:800 104px/1.25 'Cairo';margin-top:70px">الذمم الدائنة<br><span class="hl">التجارية</span></div>
  <div style="font:800 54px 'Mont';color:#12284a;margin-top:10px;direction:ltr">Trade Payables</div>
  <div style="width:200px;height:10px;border-radius:6px;background:linear-gradient(90deg,#e3a72f,#1677d6);margin:36px auto"></div>
  <div style="font:700 38px/1.6 'Cairo';color:#3a5070">أول مصطلح في سلسلة<br>«المصطلحات المحاسبية الأساسية»</div>
</div>''', 0, 5))
# 2 meaning
S.append(shell(f'''
<div class="page" style="justify-content:center;gap:40px">
  <div class="card">
    <div class="lbl">{ic("bulb")}المعنى</div>
    <p style="font:700 50px/1.75 'Cairo'">المبالغ <span class="hl">المستحقة على الشركة للموردين</span> مقابل بضائع أو خدمات اشترتها <span class="hl">بالأجل</span>.</p>
    <p style="font:600 38px/1.7 'Cairo';color:#3a5070;margin-top:20px">التزام قصير الأجل يُسدَّد عادةً خلال 30 إلى 90 يوماً.</p>
  </div>
  <div class="card" style="padding:34px 52px">
    <p class="en">Money the business <b>owes to its suppliers</b> for goods or services bought on credit.</p>
  </div>
  <div style="text-align:center;font:800 40px 'Cairo';color:#0a2350">يظهر في الميزانية ضمن: <span class="hl">الالتزامات المتداولة</span></div>
</div>''', 1, 5))
# 3 example + entry
rows = [("من ح/ المخزون","5,000",""),("إلى ح/ الذمم الدائنة","","5,000"),("عند السداد: من ح/ الذمم الدائنة","5,000",""),("إلى ح/ النقدية","","5,000")]
tr = "".join(f'<tr><td style="padding:16px 10px;border-bottom:2px solid #edf2f8">{a}</td><td class="n" style="text-align:center;color:#0e7e7a">{d}</td><td class="n" style="text-align:center;color:#1667c4">{c}</td></tr>' for a,d,c in rows)
S.append(shell(f'''
<div class="page" style="justify-content:center;gap:36px">
  <div class="card">
    <div class="lbl">{ic("pen")}مثال</div>
    <p style="font:700 46px/1.7 'Cairo'">اشترت الشركة بضاعة بقيمة <bdi><span class="n hl">5,000</span> ر.ع.</bdi> <span class="hl">بالأجل</span> من أحد الموردين.</p>
  </div>
  <div class="card" style="padding:36px 44px">
    <div class="lbl" style="font-size:40px">{ic("book")}القيد المحاسبي</div>
    <table style="width:100%;border-collapse:collapse;font:700 34px 'Cairo'">
      <tr style="font:700 26px 'Cairo';color:#7a8ca5"><td style="padding-bottom:10px;border-bottom:4px solid #e3a72f">الحساب</td><td style="text-align:center;border-bottom:4px solid #e3a72f">مدين (ر.ع.)</td><td style="text-align:center;border-bottom:4px solid #e3a72f">دائن (ر.ع.)</td></tr>
      {tr}
    </table>
  </div>
</div>''', 2, 5))
# 4 remember + mistake
S.append(shell(f'''
<div class="page" style="justify-content:center;gap:40px">
  <div class="card" style="background:#fff6e3;border-color:#f3dca6">
    <div class="lbl">{ic("star")}تذكّر</div>
    <p style="font:800 64px/1.5 'Cairo'">الذمم الدائنة = <span style="color:#b27508">ندفع لاحقاً</span></p>
    <p class="en" style="margin-top:8px">Payables = <b style="color:#b27508">we pay later</b>.</p>
  </div>
  <div class="card" style="background:#fdeeed;border-color:#f4c9c5">
    <div class="lbl" style="color:#0a2350">{ic("warn").replace('currentColor','#d64545')}خطأ شائع</div>
    <p style="font:700 46px/1.7 'Cairo'">الخلط بينها وبين الذمم المدينة؛ فالدائنة هي <span style="color:#c43a3a">ما عليك</span> أنت، والمدينة هي ما لك عند غيرك.</p>
  </div>
</div>''', 3, 5))
# 5 tip + CTA
S.append(shell(f'''
<div class="page" style="justify-content:center;gap:40px">
  <div class="card" style="background:url('file://{V2}/pat_dark.svg') 0 0/110px 110px,linear-gradient(135deg,#0a2350,#124a9c);border:none;color:#fff">
    <div class="lbl" style="color:#fff">{ic("search").replace('currentColor','#f6c453')}نصيحة المدقق</div>
    <p style="font:700 52px/1.65 'Cairo'">طابِق كشف حساب كل مورد مع دفاترك <span style="color:#f6c453">شهرياً</span>.</p>
    <p style="font:500 28px 'Cairo';color:#9fc2ea;margin-top:20px">فريق التدقيق في نمر العالمية</p>
  </div>
  <div style="text-align:center">
    <div style="font:800 46px/1.6 'Cairo'">احفظ المنشور 🔖 وتابعنا<br>مصطلح جديد كل أسبوع</div>
    <div style="font:700 34px 'Cairo';color:#3a5070;margin-top:16px">لاستشارتك المحاسبية والضريبية تواصل معنا</div>
  </div>
</div>''', 4, 5, swipe=False))

os.makedirs(f"{D}/out", exist_ok=True)
for i, h in enumerate(S, 1):
    p = f"{D}/s{i}.html"; open(p, "w").write(h)
    subprocess.run(["google-chrome","--headless=new","--no-sandbox","--disable-gpu","--hide-scrollbars","--allow-file-access-from-files",
                    "--force-device-scale-factor=1","--window-size=1080,1350",f"--screenshot={D}/out/s{i}.png",f"file://{p}"],capture_output=True)
from PIL import Image
for i in range(1, len(S)+1):
    Image.open(f"{D}/out/s{i}.png").convert("RGB").save(f"{D}/out/term01_slide{i}.jpg", quality=92)
print("ok")
