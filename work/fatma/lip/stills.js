const {chromium}=require('/opt/node-tools/node_modules/playwright');
(async()=>{ const br=await chromium.launch(); const p=await br.newPage({viewport:{width:1080,height:1920}}); const q=await br.newPage({viewport:{width:1080,height:1920}});
 await p.goto('file://'+process.cwd()+'/page.html'); await q.goto('file://'+process.cwd()+'/ins.html'); await p.evaluate(()=>document.fonts.ready); await q.evaluate(()=>document.fonts.ready);
 const ts=process.argv.slice(2);
 for(const t of ts){ await p.evaluate(t=>seek(+t),t); await p.locator('#st').screenshot({path:`st_o_${t}.png`,omitBackground:true});
   await q.evaluate(t=>seek(+t),t); await q.locator('#st').screenshot({path:`st_i_${t}.png`,omitBackground:true}); }
 await br.close(); })();
