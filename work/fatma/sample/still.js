const {chromium}=require('/opt/node-tools/node_modules/playwright');
(async()=>{ const br=await chromium.launch(); const p=await br.newPage({viewport:{width:1080,height:1920}});
 for(const v of ['A','B','C']){ await p.goto('file://'+process.cwd()+'/page_'+v+'.html'); await p.evaluate(()=>document.fonts.ready);
  for(const t of [3.7,5.9]){ await p.evaluate(t=>seek(t),t); await p.locator('#st').screenshot({path:`o_${v}_${t}.png`,omitBackground:true}); } }
 await br.close(); })();
