// Usage: node frames.js scene.html dir fps from to  (rend les images [from,to) en JPEG)
const { chromium } = require('playwright');const fs=require('fs');
(async()=>{const [,,html,dir,fps,a,b]=process.argv;fs.mkdirSync(dir,{recursive:true});
 const br=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
 const p=await br.newPage({viewport:{width:1080,height:1920}});p.on('pageerror',e=>console.log('ERR',e.message));
 await p.goto('file://'+require('path').resolve(html));await p.evaluate(()=>document.fonts.ready);
 for(let i=+a;i<+b;i++){await p.evaluate(t=>window.render(t),i/fps);await p.screenshot({path:`${dir}/${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:96});}
 await br.close();console.log('done',a,b);})();
