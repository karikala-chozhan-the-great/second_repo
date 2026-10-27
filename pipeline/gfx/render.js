// node render.js scene.html out.(mp4|mov) durationSec [--alpha] [--data '{"json":..}']
// The page must define window.setT(t) (seconds) that sets the whole visual state deterministically.
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs'), path = require('path');
(async () => {
  const [scene, out, dur] = process.argv.slice(2, 5);
  const alpha = process.argv.includes('--alpha');
  const di = process.argv.indexOf('--data');
  const data = di > 0 ? process.argv[di + 1] : '{}';
  const FPS = 30, W = 1920, H = 1080, total = Math.round(parseFloat(dur) * FPS);
  const fz = (JSON.parse(data).freeze !== undefined) ? Math.min(total, Math.round(JSON.parse(data).freeze * FPS) + 1) : total;
  const n = fz;
  const args = ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-'];
  if (alpha) args.push('-c:v', 'qtrle', '-pix_fmt', 'argb'); else args.push('-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'fast');
  if (fz < total) args.push('-vf', `tpad=stop_mode=clone:stop_duration=${((total - fz) / FPS).toFixed(3)}`);
  args.push(out);
  const ff = spawn('ffmpeg', args, { stdio: ['pipe', 'inherit', 'inherit'] });
  const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  await page.addInitScript(d => { window.__DATA = JSON.parse(d); }, data);
  await page.goto('file://' + path.resolve(scene));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForFunction(() => window.__ready !== false);
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => window.setT(t), i / FPS);
    const buf = await page.screenshot({ type: 'png', omitBackground: alpha });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
