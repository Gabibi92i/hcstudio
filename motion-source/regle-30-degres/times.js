// Usage: node times.js scene.html > times.json  (exporte window.TIMES : source unique du calage son/image)
const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'});const p=await b.newPage();
 await p.goto('file://'+require('path').resolve(process.argv[2]));console.log(JSON.stringify(await p.evaluate(()=>window.TIMES),null,1));await b.close();})();
