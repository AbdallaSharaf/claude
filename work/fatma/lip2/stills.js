const {chromium}=require('/opt/node-tools/node_modules/playwright');
(async()=>{ const br=await chromium.launch(); const p=await br.newPage({viewport:{width:1080,height:1920}}); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('file://'+process.cwd()+'/page.html'); await p.evaluate(()=>document.fonts.ready);
 for(const t of process.argv.slice(2)){ await p.evaluate(t=>seek(+t),t); await p.locator('#st').screenshot({path:`so_${t}.png`,omitBackground:true}); }
 console.log(errs); await br.close(); })();
