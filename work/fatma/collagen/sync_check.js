// every word (captions, devices, list) must appear on its spoken time: |shown - spoken| <= 0.05 s
const {chromium}=require('/opt/node-tools/node_modules/playwright');
(async()=>{const br=await chromium.launch();const p=await br.newPage({viewport:{width:1080,height:1920}});const errs=[];p.on('pageerror',e=>errs.push(String(e)));
await p.goto('file://'+process.argv[2]);await p.evaluate(()=>document.fonts.ready);await p.evaluate(()=>seek(1));
const r=await p.evaluate(()=>{const o=[];const pre=3/25;
 blocks.forEach(B=>B.c.forEach(w=>o.push(['cap',w.w,w.t,w.ta+pre])));
 (D.devices||[]).forEach(d=>{ const ws=[]; const walk=x=>{ if(Array.isArray(x)) x.forEach(walk); else if(x&&typeof x=='object'){ if('w' in x) ws.push(x); else Object.values(x).forEach(walk);} }; walk(d.items||d.lines||d.sections);
   ws.forEach(w=>o.push([d.type,w.w,(w.t0??w.t),w.t])); });
 return o;});
const bad=r.filter(x=>Math.abs(x[3]-x[2])>0.05);
const wide=await p.evaluate(()=>blocks.map(B=>[B.c.map(o=>o.w).join(' '),Math.round(Math.max(...[...B.el.querySelectorAll('.row')].map(row=>{const k=[...row.children].map(c=>c.getBoundingClientRect());return Math.max(...k.map(x=>x.right))-Math.min(...k.map(x=>x.left));})))]).filter(x=>x[1]>640));
const shortB=await p.evaluate(()=>{const pre=3/25,o=[];blocks.forEach(B=>{const L=B.c[B.c.length-1];const v=Math.min(B.leave,D.END.start)-L.ta;if(v<0.8)o.push(['caption',B.c.map(x=>x.w).join(' '),+v.toFixed(2)]);});
 (D.devices||[]).forEach(d=>{let ws=[];const walk=x=>{if(Array.isArray(x))x.forEach(walk);else if(x&&typeof x=='object'){if('w' in x)ws.push(x);else Object.values(x).forEach(walk);}};walk(d.items||d.lines);
  if(d.type=='counter'){ d.items.forEach((it,i)=>{const nx=i+1<d.items.length?d.items[i+1].t-pre:d.end;const lw=Math.max(...it.words.map(w=>w.t))-pre;if(nx-lw<0.8)o.push(['counter',it.words.map(w=>w.w).join(' '),+(nx-lw).toFixed(2)]);}); }
  else { const lw=Math.max(...ws.map(w=>w.t))-pre; if(d.end-lw<0.8)o.push([d.type,ws.map(w=>w.w).slice(-3).join(' '),+(d.end-lw).toFixed(2)]); } });return o;});
console.log('last words shown < 0.8 s:',shortB.length); shortB.forEach(x=>console.log('  ',x.join(' | ')));
console.log('rows wider than 640px:',wide.length); wide.forEach(x=>console.log('  ',x[1],x[0]));
console.log('words',r.length,'late/early >0.05s:',bad.length); bad.forEach(x=>console.log(x[0],x[1],'spoken',x[2].toFixed(2),'shown',x[3].toFixed(2),'diff',(x[3]-x[2]).toFixed(2)));
if(errs.length) console.log('ERR',errs); await br.close();})();
