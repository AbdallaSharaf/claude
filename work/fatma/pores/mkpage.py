import json
d=json.load(open("data.json"))
h=open("/home/user/claude/.claude/skills/montage/templates/reel_overlay.html").read().replace(">MARWA<",">FATMA<").replace(">MAGDY<",">TOURKY<").replace("NM,300,150,{})","NM,222,150,{})")
rep=[("(t>D.insert.start+0.45 && t<D.insert.end)","(t>(D.insert.hide??D.insert.start+0.45) && t<D.insert.end)"),
 ("c[0].t<D.insert.end-0.6","c[0].t<(D.insert.drop_to??D.insert.end-0.6)"),
 ('<path id="mask" fill="#2E1A0D"','<path id="mask" fill="#B4525E"'),('<circle id="ering" fill="none" stroke="#F0C98A"','<circle id="ering" fill="none" stroke="#F7EDE2"'),('<circle id="edot" fill="#F0C98A"','<circle id="edot" fill="#F7EDE2"'),
 # next block comes in on time; the last word keeps at least minHold (pauses give it more)
 ("B.leave=Math.min(Math.max(B.nxt-pre, last.ta+0.8), last.e+1.6, hard);","B.leave=Math.min(Math.max(B.nxt-pre, last.ta+(D.minHold??0.8)), last.e+1.6, hard);"),
 # a block whose widest row is wider than her body gets a smaller font (whole block, min 44)
 ("function seek(t){\n","function fitBlocks(){ blocks.forEach(B=>{ const rs=[...B.el.querySelectorAll('.row')]; const mw=Math.max(...rs.map(r=>{ const k=[...r.children].map(c=>c.getBoundingClientRect()); return Math.max(...k.map(x=>x.right))-Math.min(...k.map(x=>x.left)); })); B.mw=mw; if(mw>620){ const fs=Math.max(44,54*620/mw); B.el.querySelectorAll('.w').forEach(s=>s.style.fontSize=fs.toFixed(1)+'px'); B.fs=fs; } }); }\nlet FIT=false;\nfunction seek(t){ if(!FIT){ FIT=true; fitBlocks(); }\n")]
for a,b in rep:
    assert a in h,a[:40]; h=h.replace(a,b)
open("page.html","w").write(h.replace("DATA",json.dumps(d,ensure_ascii=False)))
