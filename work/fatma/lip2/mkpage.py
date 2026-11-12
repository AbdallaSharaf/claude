import json
d=json.load(open("data.json"))
h=open("/home/user/claude/.claude/skills/montage/templates/reel_overlay.html").read().replace(">MARWA<",">FATMA<").replace(">MAGDY<",">TOURKY<").replace("NM,300,150,{})","NM,D.nameY-ly,D.nameY-ly,{})")
rep=[("(t>D.insert.start+0.45 && t<D.insert.end)","(t>(D.insert.hide??D.insert.start+0.45) && t<D.insert.end)"),
 ("c[0].t<D.insert.end-0.6","c[0].t<(D.insert.drop_to??D.insert.end-0.6)"),
 ('<path id="mask" fill="#2E1A0D"','<path id="mask" fill="#B4525E"'),('<circle id="ering" fill="none" stroke="#F0C98A"','<circle id="ering" fill="none" stroke="#F7EDE2"'),('<circle id="edot" fill="#F0C98A"','<circle id="edot" fill="#F7EDE2"'),
 # next block comes in on time; the last word keeps at least minHold (pauses give it more)
 ("B.leave=Math.min(Math.max(B.nxt-pre, last.ta+0.8), last.e+1.6, hard);","B.leave=Math.min(Math.max(B.nxt-pre, last.ta+(D.minHold??0.8)), last.e+1.6, hard);"),
 # a block whose widest row is wider than her body gets a smaller font (whole block, min 44)
 ("function seek(t){\n","function fitBlocks(){ blocks.forEach(B=>{ const rs=[...B.el.querySelectorAll('.row')]; const mw=Math.max(...rs.map(r=>{ const k=[...r.children].map(c=>c.getBoundingClientRect()); return Math.max(...k.map(x=>x.right))-Math.min(...k.map(x=>x.left)); })); B.mw=mw; if(mw>620){ const fs=Math.max(44,54*620/mw); B.el.querySelectorAll('.w').forEach(s=>s.style.fontSize=fs.toFixed(1)+'px'); B.fs=fs; } }); }\nlet FIT=false;\nfunction seek(t){ if(!FIT){ FIT=true; fitBlocks(); }\n")]
for a,b in rep:
    assert a in h,a[:40]; h=h.replace(a,b)
LIST_JS = r"""
<style>
@font-face{font-family:G7;src:url(../fonts/Geist700.woff2)}
@font-face{font-family:P7;src:url(../fonts/IBMPA700.ttf)}
[id^=lc]{position:absolute;box-sizing:border-box;background:rgba(250,242,236,.80);border:1.5px solid rgba(255,248,242,.9);box-shadow:0 1px 0 rgba(255,250,246,.9) inset,0 2px 6px rgba(70,20,28,.10),0 24px 60px rgba(50,14,20,.22);border-radius:40px;overflow:hidden}
.lr{position:absolute;right:36px;display:flex;align-items:center;gap:22px;direction:rtl;white-space:nowrap}
.lr .ar{font:700 42px/1.2 P7;color:#3A1219}
.lr .en{font:700 42px/1.2 G7;color:#B4525E;letter-spacing:-.01em}
.cb{width:48px;height:48px;border-radius:14px;box-sizing:border-box;border:3px solid rgba(180,82,94,.45);display:flex;align-items:center;justify-content:center;flex:none}
</style>
<div style="position:absolute;left:-2000px;top:0;font:700 42px P7">أ</div><div style="position:absolute;left:-2000px;top:0;font:700 42px G7">A</div>
<script>
(D.devices||[]).filter(d=>d.type=='list').forEach(function(L){
 const st=document.getElementById('st'); const card=document.createElement('div'); card.id='lc'+L.start; st.appendChild(card);
 const LAT=/[A-Za-z]/, W0=780, HEAD=110, RH=86, PADB=26;
 const head=document.createElement('div'); head.className='lr'; head.style.top='28px';
 if(L.num) head.innerHTML=`<div style="width:58px;height:58px;border-radius:29px;background:#B4525E;color:#FAF2EC;font:700 34px/58px P7;text-align:center;flex:none">${L.num}</div>`;
 card.appendChild(head);
 const hw=L.lines[0].map(o=>{ const sp=document.createElement('span'); sp.className=LAT.test(o.w)?'en':'ar'; sp.textContent=o.w; if(o.g) sp.style.color='#B4525E'; head.appendChild(sp); return {el:sp,t:o.t}; });
 const div=document.createElement('div'); div.style.cssText='position:absolute;left:30px;right:30px;top:104px;height:1.5px;background:rgba(58,18,25,.10)'; card.appendChild(div);
 const rows=L.lines.slice(1).map((ln,i)=>{ const r=document.createElement('div'); r.className='lr'; r.style.top=(HEAD+12+i*RH)+'px';
   const hdr=!!ln[0].hdr; const cb=document.createElement('div'); cb.className='cb'; if(hdr){ cb.style.visibility='hidden'; cb.style.width='0px'; cb.style.border='none'; } cb.innerHTML='<svg width="30" height="30" viewBox="0 0 30 30"><path d="M7 16 L13 22 L24 9" stroke="#FAF2EC" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'; r.appendChild(cb);
   const ws=ln.map(o=>{ const sp=document.createElement('span'); sp.className=LAT.test(o.w)?'en':'ar'; sp.textContent=o.w; if(hdr) sp.style.color='#B4525E'; r.appendChild(sp); return {el:sp,t:o.t}; });
   card.appendChild(r); return {r,cb,ck:cb.querySelector('path'),ws,t:ln[0].t}; });
 const HK=[[0,HEAD+PADB-14]].concat(rows.map((R,i)=>[R.t-pre-0.18,HEAD+12+(i+1)*RH+PADB-12]));
 const trk=(K,t,Ts)=>{ let v=K[0][1]; for(let i=1;i<K.length;i++) v+=(K[i][1]-K[i-1][1])*spr(t-K[i][0],Ts); return v; };
 const rise=(o,t)=>{ const a=cl(spr(t-(o.t-pre),.28),0,1); o.el.style.transform=`translateY(${((1-a)*22).toFixed(1)}px)`; o.el.style.opacity=a.toFixed(3); };
 let W0f=null;
 const _seek=window.seek;
 window.seek=function(t){ _seek(t);
   const on=t>L.start-0.05 && t<L.end+0.5; card.style.visibility=on?'visible':'hidden'; if(!on) return;
   if(W0f===null){ W0f=Math.max(head.scrollWidth,...rows.map(R=>R.r.scrollWidth))+72; }
   const g=spr(t-L.start,.34), ex=spx(t-L.end,.24);
   const w=(160+(W0f-160)*g)*(1-ex*0.6), h=trk(HK,t,.36)*(0.4+0.6*g)*(1-ex*0.6);
   card.style.left=(540-w/2).toFixed(1)+'px'; card.style.top=(L.top+(1-g)*30).toFixed(1)+'px'; card.style.width=w.toFixed(1)+'px'; card.style.height=h.toFixed(1)+'px'; card.style.opacity=(1-ex).toFixed(3);
   hw.forEach(o=>rise(o,t)); if(L.num) head.firstChild.style.transform=`scale(${cl(spr(t-L.start-0.05,.3),0,1).toFixed(3)})`;
   rows.forEach(R=>{ const a=cl(spr(t-(R.t-pre),.28),0,1); R.cb.style.opacity=a; R.cb.style.transform=`scale(${(0.6+0.4*a).toFixed(3)})`;
     const f=cl(spr(t-(R.t-pre+0.25),.25),0,1); R.cb.style.background=`rgba(180,82,94,${(0.9*f).toFixed(3)})`; R.cb.style.borderColor=`rgba(180,82,94,${(0.45+0.5*f).toFixed(3)})`;
     const L2=R.ck.getTotalLength(); R.ck.style.strokeDasharray=`${(L2*f).toFixed(1)} ${L2+1}`; R.ws.forEach(o=>rise(o,t)); }); };
});
</script>"""
h=h.replace("</body>",LIST_JS+"</body>")
open("page.html","w").write(h.replace("DATA",json.dumps(d,ensure_ascii=False)))
