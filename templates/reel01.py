import subprocess, os, sys
sys.path.insert(0, "/home/claude/ig")
D = "/home/claude/ig/reel01"; os.makedirs(D, exist_ok=True)
V2 = "/home/claude/v2"
from build_slides import FONT  # reuse fonts (module re-renders slides; harmless)

CSS = FONT + f'''
*{{box-sizing:border-box;margin:0}}
html,body{{width:1080px;height:1920px;overflow:hidden}}
body{{font-family:"Cairo";color:#0a2350;text-align:center;position:relative;
 background:url("file://{V2}/pat_light.svg") 0 0/130px 130px,radial-gradient(120% 70% at 80% 0%,#d9ecff 0%,#f4f9ff 55%,#fff 100%)}}
body.dark{{color:#fff;background:url("file://{V2}/pat_dark.svg") 0 0/130px 130px,linear-gradient(165deg,#081a3d 0%,#0e3a80 55%,#1663b8 100%)}}
.logo{{position:absolute;top:110px;left:0;right:0;text-align:center}}.logo img{{height:150px}}
.mid{{position:absolute;top:330px;bottom:330px;left:70px;right:70px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:50px}}
.pill{{background:#0a2350;color:#fff;font:800 46px "Cairo";padding:14px 44px;border-radius:60px}}
.dark .pill{{background:#e3a72f;color:#0a2350}}
.q{{font:800 96px/1.45 "Cairo"}}
.card{{background:#fff;border:3px solid #dfe9f5;border-radius:48px;padding:60px 56px;box-shadow:0 20px 60px rgba(10,35,80,.1);width:100%}}
.opts{{display:flex;gap:40px;width:100%}}
.opt{{flex:1;border-radius:40px;padding:40px 0;font:800 72px "Cairo";border:4px solid #c9daef;background:#fff;color:#7a8ca5}}
.opt.on{{background:#0e9f6e;border-color:#0e9f6e;color:#fff;box-shadow:0 18px 40px rgba(14,159,110,.35)}}
.opt.off{{opacity:.35}}
.cd{{width:230px;height:260px;border-radius:115px 115px 36px 36px;background:linear-gradient(160deg,#0a2350,#1f8be0);color:#fff;
  font:800 150px/260px "Mont";box-shadow:0 0 0 12px #fff,0 0 0 17px #e3a72f}}
.ans{{font:700 54px/1.6 "Cairo";color:#3a5070}}.ans b{{color:#1667c4}}
.num{{font:800 40px "Mont";color:#e3a72f}}
.foot{{position:absolute;left:0;right:0;bottom:0;height:200px;background:linear-gradient(90deg,#0a2350,#124a9c 70%,#1a6fc4);
 display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;gap:6px}}
.foot:before{{content:"";position:absolute;left:0;right:0;top:0;height:8px;background:linear-gradient(90deg,#e3a72f,#f6d27c,#e3a72f)}}
.foot b{{font:800 64px "Mont";letter-spacing:2px}}.foot span{{font:700 34px "Cairo";color:#dbe8fa}}
'''
def page(body, dark=False, logo="/home/claude/logo.png"):
    return f'''<!doctype html><html dir="rtl"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body class="{'dark' if dark else ''}"><div class="logo"><img src="file://{logo}"></div><div class="mid">{body}</div>
<div class="foot"><b dir="ltr">91474750</b><span>نمر العالمية .. معك في كل خطوة</span></div></body></html>'''

Q = [("بضاعة اشتريتها من مورد <span style='color:#1667c4'>بالأجل</span>", "دائن", "تُسجَّل ضمن <b>الذمم الدائنة</b> لأنها مبلغ عليك."),
     ("عميل اشترى منك <span style='color:#1667c4'>بالأجل</span>", "مدين", "تُسجَّل ضمن <b>الذمم المدينة</b> لأنها مبلغ لك."),
     ("رواتب ديسمبر <span style='color:#1667c4'>لم تُدفع بعد</span>", "دائن", "<b>مصروف مستحق</b>: التزام على الشركة حتى يُدفع.")]

scenes = []  # (name, html, seconds, sound)
scenes.append(("hook", page('''<div class="pill">تحدّي المحاسبة ⏱️</div>
  <div class="q" style="font-size:150px;line-height:1.3">مدين<br>أم<br><span style="color:#f6c453">دائن؟</span></div>
  <div style="font:700 56px 'Cairo';color:#cfe0f7">3 أسئلة.. 3 ثوانٍ لكل سؤال</div>''', dark=True, logo=f"{V2}/logo_white.png"), 2.8, "whoosh"))
for i, (q, a, ex) in enumerate(Q, 1):
    base = lambda extra, state: page(f'''<div class="pill">السؤال {i} من 3</div>
      <div class="card"><div class="q">{q}</div></div>
      <div class="opts"><div class="opt {state[0]}">مدين</div><div class="opt {state[1]}">دائن</div></div>{extra}''')
    for n in (3, 2, 1):
        scenes.append((f"q{i}_{n}", base(f'<div class="cd">{n}</div>', ("", "")), 1.0, "tick"))
    st = ("on", "off") if a == "مدين" else ("off", "on")
    scenes.append((f"q{i}_a", base(f'<div class="ans">✅ الإجابة: <b>{a}</b><br>{ex}</div>', st), 2.6, "ding"))
scenes.append(("cta", page('''<div class="q" style="font-size:110px">كم إجابة<br><span style="color:#f6c453">صحيحة؟</span></div>
  <div style="font:700 60px/1.6 'Cairo'">اكتب نتيجتك في التعليقات 👇<br>وتابعنا لتحدٍّ جديد كل أسبوع</div>''', dark=True, logo=f"{V2}/logo_white.png"), 3.6, "ding"))

# render frames
for name, html, dur, snd in scenes:
    p = f"{D}/{name}.html"; open(p, "w").write(html)
    subprocess.run(["google-chrome","--headless=new","--no-sandbox","--disable-gpu","--hide-scrollbars","--allow-file-access-from-files",
        "--force-device-scale-factor=1","--window-size=1080,1920",f"--screenshot={D}/{name}.png",f"file://{p}"],capture_output=True)

# sounds (synthesised, no copyrighted audio)
S = {
 "tick": "aevalsrc='0.35*sin(2*PI*1200*t)*exp(-40*t)':d=0.15",
 "ding": "aevalsrc='0.3*(sin(2*PI*880*t)+0.6*sin(2*PI*1320*t))*exp(-5*t)':d=0.9",
 "whoosh": "anoisesrc=d=0.6:c=pink:a=0.25,afade=t=in:d=0.25,afade=t=out:st=0.3:d=0.3,lowpass=f=1800",
}
for k, v in S.items():
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","lavfi","-i",v,"-ar","44100","-ac","2",f"{D}/{k}.wav"])

# clips: subtle zoom + short fades, each with its sound
parts = []
for idx, (name, _, dur, snd) in enumerate(scenes):
    frames = int(dur * 30)
    zoom = "1+0.0006*on" if not name.startswith("q") or name.endswith("_a") else "1"
    fade = f",fade=t=in:st=0:d=0.12" if not name.endswith(("_2","_1")) else ""
    vf = f"scale=1188:2112,zoompan=z='{zoom}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps=30{fade},format=yuv420p"
    out = f"{D}/c{idx:02d}.mp4"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-loop","1","-i",f"{D}/{name}.png","-i",f"{D}/{snd}.wav",
        "-filter_complex",f"[0:v]{vf}[v];[1:a]apad=whole_dur={dur}[a]","-map","[v]","-map","[a]","-t",str(dur),
        "-c:v","libx264","-preset","veryfast","-crf","20","-r","30","-c:a","aac","-b:a","128k","-ar","44100",out])
    parts.append(out)
open(f"{D}/list.txt","w").write("".join(f"file '{p}'\n" for p in parts))
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",f"{D}/list.txt","-c:v","libx264","-preset","veryfast","-crf","20",
    "-pix_fmt","yuv420p","-c:a","aac","-b:a","128k","-movflags","+faststart","/home/claude/ig/out/reel01_debit_credit_quiz.mp4"])
# cover
subprocess.run(["cp", f"{D}/hook.png", "/home/claude/ig/out/reel01_cover.png"])
print("done")
