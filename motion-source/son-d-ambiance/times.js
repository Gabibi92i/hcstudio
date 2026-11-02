const { chromium } = require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'});const p=await b.newPage();
await p.goto('file://'+require('path').resolve('scene.html'));const T=await p.evaluate(()=>window.TIMES);fs.writeFileSync('times.json',JSON.stringify(T,null,1));await b.close();console.log(T);})();
