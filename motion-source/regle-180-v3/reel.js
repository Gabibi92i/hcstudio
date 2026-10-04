// Usage: node reel.js <scene.html> <out.mp4> <seconds> [fps]
const { chromium } = require('playwright');
const { execSync } = require('child_process');
const fs = require('fs');
(async()=>{
  const [,, html, out, secs, fpsArg] = process.argv;
  const fps = +(fpsArg||30), n = Math.round(+secs*fps);
  const dir = out + '.frames'; fs.rmSync(dir,{recursive:true,force:true}); fs.mkdirSync(dir);
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p = await b.newPage({viewport:{width:1080,height:1920}});
  await p.goto('file://' + require('path').resolve(html)); await p.evaluate(()=>document.fonts.ready); p.on('pageerror',e=>console.log('ERR',e.message));
  for (let i=0;i<n;i++){
    await p.evaluate(t=>window.render(t), i/fps);
    await p.screenshot({path:`${dir}/${String(i).padStart(5,'0')}.jpg`, type:'jpeg', quality:96});
  }
  await b.close();
  execSync(`ffmpeg -loglevel error -y -framerate ${fps} -i ${dir}/%05d.jpg -c:v libx264 -pix_fmt yuv420p -profile:v high -preset slow -crf 14 -x264-params aq-mode=3 -movflags +faststart ${out}`);
  fs.rmSync(dir,{recursive:true,force:true});
  console.log('ok', out, n, 'frames');
})();
