const {chromium}=require('/opt/node-tools/node_modules/playwright');
(async()=>{ const br=await chromium.launch(); const q=await br.newPage({viewport:{width:1080,height:1920}}); const errs=[]; q.on('pageerror',e=>errs.push(String(e)));
 await q.goto('file://'+process.cwd()+'/ins_ui_page.html'); await q.evaluate(()=>document.fonts.ready);
 for(const t of process.argv.slice(2)){ await q.evaluate(t=>seek(+t),t); await q.locator('#st').screenshot({path:`u_${t}.png`,omitBackground:true}); }
 console.log('errs',errs); await br.close(); })();
