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
console.log('words',r.length,'late/early >0.05s:',bad.length); bad.forEach(x=>console.log(x[0],x[1],'spoken',x[2].toFixed(2),'shown',x[3].toFixed(2),'diff',(x[3]-x[2]).toFixed(2)));
if(errs.length) console.log('ERR',errs); await br.close();})();
