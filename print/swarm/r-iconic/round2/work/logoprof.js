const { chromium } = require('playwright');
const fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--disable-lcd-text']});const p=await b.newPage({viewport:{width:1125,height:675}});
let s=fs.readFileSync('/home/user/claude/print/swarm/assets/logo-linea.svg','utf8');s=s.slice(s.indexOf('<svg'));
s=s.replace(/viewBox="[^"]*"/,'viewBox="20.66 8.68 2177.58 302.63"').replace('<svg','<svg preserveAspectRatio="xMinYMin meet" style="position:absolute;left:75px;top:464.5px;width:975px;height:135.5px"');
await p.setContent('<body style="margin:0;background:#000">'+s.replace(/#F2F0E9/g,'#fff')+'</body>');
await p.screenshot({path:'logo-only.png'});await b.close();})();
