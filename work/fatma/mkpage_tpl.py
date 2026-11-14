import json
d=json.load(open("data.json"))
h=open("/home/user/claude/.claude/skills/montage/templates/reel_overlay.html").read().replace(">MARWA<",">FATMA<").replace(">MAGDY<",">TOURKY<").replace("NM,300,150,{})","NM,D.nameY-ly,D.nameY-ly,{})")
rep=[("(t>D.insert.start+0.45 && t<D.insert.end)","(t>(D.insert.hide??D.insert.start+0.45) && t<D.insert.end)"),
 ("c[0].t<D.insert.end-0.6","c[0].t<(D.insert.drop_to??D.insert.end-0.6)"),
 ('<path id="mask" fill="#2E1A0D"','<path id="mask" fill="#B4525E"'),('<circle id="ering" fill="none" stroke="#F0C98A"','<circle id="ering" fill="none" stroke="#F7EDE2"'),('<circle id="edot" fill="#F0C98A"','<circle id="edot" fill="#F7EDE2"'),
 # next block comes in on time; the last word keeps at least minHold (pauses give it more)
 ("B.leave=Math.min(Math.max(B.nxt-pre, last.ta+0.8), last.e+1.6, hard);","B.leave=Math.min(Math.max(B.nxt-pre, last.ta+(D.minHold??0.8)), hard);"),
 # a block whose widest row is wider than her body gets a smaller font (whole block, min 44)
 (".m{overflow:hidden;padding:12px 6px 28px;display:inline-block}",".m{overflow:hidden;padding:16px 26px 30px;margin:0 -20px;display:inline-block}"),
 ("function seek(t){\n","function fitBlocks(){ blocks.forEach(B=>{ const rs=[...B.el.querySelectorAll('.row')]; const mw=Math.max(...rs.map(r=>{ const k=[...r.children].map(c=>c.getBoundingClientRect()); return Math.max(...k.map(x=>x.right))-Math.min(...k.map(x=>x.left)); })); B.mw=mw; if(mw>620){ const fs=Math.max(44,54*620/mw); B.el.querySelectorAll('.w').forEach(s=>s.style.fontSize=fs.toFixed(1)+'px'); B.fs=fs; } }); }\nlet FIT=false;\nfunction seek(t){ if(!FIT){ FIT=true; fitBlocks(); }\n")]
for a,b in rep:
    assert a in h,a[:40]; h=h.replace(a,b)
KARAOKE_JS = r"""
<style>
@font-face{font-family:G7;src:url(../fonts/Geist700.woff2)}
.w.kw{display:inline-grid}
.w.kw>span{grid-area:1/1;text-align:center;transform-origin:50% 70%}
.w.kw>.kb{font-family:A8;color:#F0C98A}
#ttl{position:absolute;left:0;width:1080px;display:flex;justify-content:center;pointer-events:none}
#ttl svg{position:static}
</style>
<script>
(function(){
 // whole line in at once; the word she is saying takes the "تكبير" style
 const KW=[]; blocks.forEach(B=>B.c.forEach(o=>{ if(o.k===undefined) return; const s=o.el; const tx=s.textContent; s.textContent='';
   s.classList.add('kw'); const n=document.createElement('span'); n.textContent=tx; const b=document.createElement('span'); b.className='kb'; b.textContent=tx; s.appendChild(n); s.appendChild(b); KW.push({o,B,n,b}); }));
 // Lip Filler title: glass pill with a lips icon (option 2)
 const TT=D.title; let tt=null;
 if(TT){ tt=document.createElement('div'); tt.id='ttl'; tt.innerHTML=`<div id="ttp" style="display:flex;align-items:center;gap:22px;padding:14px 40px 14px 16px;border-radius:60px;background:rgba(250,242,236,.82);border:1.5px solid rgba(255,248,242,.9);box-shadow:0 1px 0 rgba(255,250,246,.9) inset,0 20px 50px rgba(50,14,20,.25)"><div style="width:84px;height:84px;border-radius:42px;background:#B4525E;display:flex;align-items:center;justify-content:center">${TT.svg}</div><div style="font:66px/1 ${/[A-Za-z]/.test(TT.text)?'G7':'P7'};color:#3A1219;letter-spacing:-.01em;white-space:nowrap">${TT.text}</div></div>`; document.getElementById('L').appendChild(tt); }
 const _seek=window.seek;
 window.seek=function(t){ _seek(t);
   KW.forEach(x=>{ const ws=x.B.c.filter(q=>q.k!==undefined); const i=ws.indexOf(x.o); const nx=i+1<ws.length?ws[i+1].k-pre:1e9;
     const on=cl(spr(t-(x.o.k-pre),.16),0,1)*(1-cl(spr(t-nx,.16),0,1));
     x.b.style.opacity=on.toFixed(3); x.n.style.opacity=(1-on).toFixed(3); const sc=(1+0.10*on).toFixed(3); x.b.style.transform=`scale(${sc})`; x.n.style.transform=`scale(${sc})`; });
   if(tt){ const first=blocks[TT.block||0]; const vis=t>TT.t-pre-0.02 && t<first.leave+0.4; tt.style.visibility=vis?'visible':'hidden';
     if(vis){ const a=cl(spr(t-(TT.t-pre),.32),0,1), xo=spx(t-first.leave,.2); const p=document.getElementById('ttp');
       tt.style.top=(-118)+'px'; p.style.transform=`translateY(${((1-a)*40-xo*20).toFixed(1)}px) scale(${(0.9+0.1*a).toFixed(3)})`; p.style.opacity=(a*(1-xo)).toFixed(3); } } };
})();
</script>"""
HOOK_JS = r"""
<style>
#hk{position:absolute;left:0;width:1080px;display:flex;flex-direction:column;align-items:center;pointer-events:none}
#hk .hr{display:flex;gap:26px;direction:rtl}
#hk .hm{overflow:hidden;padding:18px 24px 34px;display:inline-block}
#hk .hw{display:inline-block;font:116px/1.15 A8;color:#F6EAD6;text-shadow:0 4px 14px rgba(74,42,20,.6),0 1px 2px rgba(74,42,20,.45);transform-origin:50% 80%}
#hk .hw.g{color:#F0C98A}
#hk .tl{height:5px;border-radius:3px;background:#F0C98A;box-shadow:0 2px 6px rgba(74,42,20,.5);margin-top:-14px}
</style>
<script>
(function(){ const HK=D.hook; if(!HK) return;
 const box=document.createElement('div'); box.id='hk'; const row=document.createElement('div'); row.className='hr'; box.appendChild(row);
 const ws=HK.words.map((o,i)=>{ const m=document.createElement('span'); m.className='hm'; const s=document.createElement('span'); s.className='hw'+(i==1?' g':''); s.textContent=o.w; m.appendChild(s); row.appendChild(m); return {el:s,t:o.t}; });
 const tl=document.createElement('div'); tl.className='tl'; box.appendChild(tl); document.getElementById('L').appendChild(box);
 let W=null;
 const _seek=window.seek;
 window.seek=function(t){ _seek(t);
   const vis=t>HK.words[0].t-pre-0.02 && t<HK.end+0.5; box.style.visibility=vis?'visible':'hidden'; if(!vis) return;
   if(W===null) W=row.getBoundingClientRect().width-48;
   box.style.top='-330px'; const xo=spx(t-HK.end,.22);
   ws.forEach((o,i)=>{ const a=spr(t-(o.t-pre),.34); const k=cl(a,0,1.2);
     o.el.style.transform=`translateY(${((1-k)*150-xo*150).toFixed(1)}px) scale(${(1.12-0.12*cl(a,0,1)).toFixed(3)})`; o.el.style.opacity=(a>0.001&&xo<.999)?1:0; });
   // one-second timer: the gold line runs right to left for exactly one second from the first word
   const u=cl((t-(HK.words[0].t-pre))/1.0,0,1), e=1-Math.pow(1-u,2);
   tl.style.width=(W*e).toFixed(1)+'px'; tl.style.marginLeft=(W*(1-e)).toFixed(1)+'px'; tl.style.opacity=(1-xo).toFixed(3); };
})();
</script>"""
LIST_JS = r"""
<style>
@font-face{font-family:P7;src:url(../fonts/IBMPA700.ttf)}
.lc{position:absolute;box-sizing:border-box;background:rgba(250,242,236,.82);border:1.5px solid rgba(255,248,242,.9);box-shadow:0 1px 0 rgba(255,250,246,.9) inset,0 2px 6px rgba(70,20,28,.10),0 24px 60px rgba(50,14,20,.22);border-radius:44px;overflow:hidden}
.lt{position:absolute;left:0;right:0;text-align:center;direction:rtl;font:700 54px/1.2 P7;color:#B4525E;white-space:nowrap}
.lr{position:absolute;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:26px;direction:rtl}
.lr .tx{font:700 46px/1.2 P7;color:#3A1219;white-space:nowrap;text-align:center}
.cb{position:relative;width:52px;height:52px;border-radius:15px;flex:none;box-shadow:inset 0 0 0 3px rgba(180,82,94,.45)}
.cb svg{position:absolute;left:0;top:0}
</style>
<div style="position:absolute;left:-2000px;top:0;font:700 46px P7">أ</div>
<script>
(D.devices||[]).filter(d=>d.type=='list').forEach(function(L){
 const st=document.getElementById('st'), card=document.createElement('div'); card.className='lc'; st.appendChild(card);
 const PADX=70, TOPP=34, TH=74, DIVG=34, RH=92, BOT=40;
 const title=document.createElement('div'); title.className='lt'; title.style.top=TOPP+'px'; card.appendChild(title);
 const tws=L.lines[0].map(o=>{ const sp=document.createElement('span'); sp.textContent=o.w; sp.style.display='inline-block'; sp.style.margin='0 7px'; title.appendChild(sp); return {el:sp,t:o.t}; });
 const div=document.createElement('div'); div.style.cssText='position:absolute;left:40px;right:40px;height:2px;border-radius:1px;background:rgba(180,82,94,.28)'; div.style.top=(TOPP+TH+DIVG/2)+'px'; card.appendChild(div);
 const rows=L.lines.slice(1).map((ln,i)=>{ const r=document.createElement('div'); r.className='lr'; r.style.top=(TOPP+TH+DIVG+i*RH)+'px';
   const cb=document.createElement('div'); cb.className='cb'; cb.innerHTML='<svg width="52" height="52" viewBox="0 0 52 52"><path d="M16 27 L23 34 L36 19" stroke="#FAF2EC" stroke-width="4.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'; r.appendChild(cb);
   const tx=document.createElement('div'); tx.className='tx'; r.appendChild(tx);
   const ws=ln.map(o=>{ const sp=document.createElement('span'); sp.textContent=o.w; sp.style.display='inline-block'; sp.style.margin='0 7px'; tx.appendChild(sp); return {el:sp,t:o.t}; });
   card.appendChild(r); return {r,cb,ck:cb.querySelector('path'),tx,ws,t:ln[0].t}; });
 // every row the same width: Arabic stretched with kashida
 const NOJ='اأإآدذرزوؤةىء';
 function kas(sp,add){ const s0=sp.textContent, w0=sp.getBoundingClientRect().width;
   // one natural spot per word: the joining point closest to the middle, never between lam and alef
   const pos=[]; for(let i=0;i<s0.length-1;i++){ const c=s0[i],n=s0[i+1]; if(/[ء-ي]/.test(c)&&/[ء-ي]/.test(n)&&!NOJ.includes(c)&&!(c=='ل'&&'اأإآ'.includes(n))&&!(i==1&&s0[0]=='ا'&&c=='ل')) pos.push(i+1); }
   if(!pos.length) return; const mid=s0.length/2; const k=pos.sort((a,b)=>Math.abs(a-mid)-Math.abs(b-mid))[0];
   let n=0; while(n<40){ sp.textContent=s0.slice(0,k)+'ـ'.repeat(n+1)+s0.slice(k); if(sp.getBoundingClientRect().width>w0+add+2){ sp.textContent=s0.slice(0,k)+'ـ'.repeat(n)+s0.slice(k); break; } n++; } }
 let LAY=null;
 function lay(){ const W=rows.map(R=>R.tx.getBoundingClientRect().width), T=Math.max(...W);
   rows.forEach((R,i)=>{ if(W[i]<0.72*T) return; let left=T-W[i]; const sp=[...R.ws].map(o=>o.el).sort((a,b)=>b.textContent.length-a.textContent.length);
     sp.forEach((x,j)=>{ if(left<4) return; const w0=x.getBoundingClientRect().width; kas(x,left/(sp.length-j)); left-=x.getBoundingClientRect().width-w0; }); });
   const rowW=52+26+Math.max(...rows.map(R=>R.tx.getBoundingClientRect().width));
   LAY={W:Math.max(rowW,title.scrollWidth)+2*PADX, H:TOPP+TH+DIVG+rows.length*RH+BOT-20};
   rows.forEach(R=>{ R.r.style.justifyContent='flex-start'; R.r.style.boxSizing='border-box'; R.r.style.paddingRight=((LAY.W-rowW)/2).toFixed(1)+'px'; }); }
 const HK=[[0,TOPP+TH+BOT]].concat(rows.map((R,i)=>[R.t-pre-0.18,TOPP+TH+DIVG+(i+1)*RH+BOT-20]));
 const trk=(K,t,Ts)=>{ let v=K[0][1]; for(let i=1;i<K.length;i++) v+=(K[i][1]-K[i-1][1])*spr(t-K[i][0],Ts); return v; };
 const rise=(o,t)=>{ const a=cl(spr(t-(o.t-pre),.28),0,1); o.el.style.transform=`translateY(${((1-a)*22).toFixed(1)}px)`; o.el.style.opacity=a.toFixed(3); };
 const _seek=window.seek;
 window.seek=function(t){ _seek(t);
   const on=t>L.start-0.05 && t<L.end+0.5; card.style.visibility=on?'visible':'hidden'; if(!on) return;
   if(!LAY) lay();
   const g=spr(t-L.start,.34), ex=spx(t-L.end,.24);
   const w=(200+(LAY.W-200)*g)*(1-ex*0.6), h=trk(HK,t,.36)*(0.4+0.6*g)*(1-ex*0.6);
   card.style.left=(540-w/2).toFixed(1)+'px'; card.style.top=(L.top+(1-g)*30).toFixed(1)+'px'; card.style.width=w.toFixed(1)+'px'; card.style.height=h.toFixed(1)+'px'; card.style.opacity=(1-ex).toFixed(3);
   tws.forEach(o=>rise(o,t)); div.style.transform=`scaleX(${cl(spr(t-L.start-0.1,.3),0,1).toFixed(3)})`;
   rows.forEach(R=>{ const a=cl(spr(t-(R.t-pre),.28),0,1); R.cb.style.opacity=a; R.cb.style.transform=`scale(${(0.6+0.4*a).toFixed(3)})`;
     const f=cl(spr(t-(R.t-pre+0.25),.25),0,1); R.cb.style.background=`rgba(180,82,94,${(0.92*f).toFixed(3)})`;
     const L2=R.ck.getTotalLength(); R.ck.style.strokeDasharray=`${(L2*f).toFixed(1)} ${L2+1}`; R.ws.forEach(o=>rise(o,t)); }); };
});
</script>"""
h=h.replace("</body>",HOOK_JS+KARAOKE_JS+LIST_JS+"</body>")
open("page.html","w").write(h.replace("DATA",json.dumps(d,ensure_ascii=False)))
