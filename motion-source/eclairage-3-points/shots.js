// Usage: node shots.js scene.html outdir t1 t2 ...
const { chromium } = require('playwright');const fs=require('fs');
(async()=>{const [,,html,dir,...ts]=process.argv;fs.mkdirSync(dir,{recursive:true});
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
 const p=await b.newPage({viewport:{width:1080,height:1920}});p.on('pageerror',e=>console.log('ERR',e.message));p.on('console',m=>console.log('LOG',m.text()));
 await p.goto('file://'+require('path').resolve(html));await p.evaluate(()=>document.fonts.ready);
 for(const t of ts){await p.evaluate(t=>window.render(t),+t);await p.screenshot({path:`${dir}/t${(+t).toFixed(2).padStart(6,'0')}.jpg`,type:'jpeg',quality:85});}
 await b.close();})();
