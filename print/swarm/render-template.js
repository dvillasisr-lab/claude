const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:1500}});
await p.goto('file://'+process.cwd()+'/cards.html');await p.waitForTimeout(500);
for(const id of ['front','back']) await p.locator('#'+id).screenshot({path:`card-${id}.png`});
const q=await b.newPage();await q.goto('file://'+process.cwd()+'/cards.html#print');await q.waitForTimeout(500);
await q.pdf({path:'cards.pdf',width:'3.75in',height:'2.25in',printBackground:true,pageRanges:'1-2'});await b.close()})();
