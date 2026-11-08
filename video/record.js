// Record the replay animation and render slides to PNG. Usage: node video/record.js
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'video', 'build'); fs.mkdirSync(OUT, { recursive: true });
const script = JSON.parse(fs.readFileSync(path.join(ROOT, 'video', 'script.json')));
const GAP = 0.5;
const BLOBS = {
  '/_blob/df432f8d4717ac826d3d3b8fba080b60': 'results/figures/fig1_reid_auc.png',
  '/_blob/2e4d58fc7a22889c05f42977cd30dede': 'results/figures/fig7_coord_vs_agree.png',
  '/_blob/5b14c95b07534518cc7b5c4a66ecc3ed': 'results/figures/fig6_robustness.png',
};
(async () => {
  const browser = await chromium.launch();
  // 1) slides -> PNG
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  for (const s of script.filter(s => s.kind === 'slide')) {
    let html = fs.readFileSync(path.join(ROOT, 'slides', 'project', 'slides', s.id + '.html'), 'utf8');
    for (const [k, v] of Object.entries(BLOBS)) html = html.split(k).join('file://' + path.join(ROOT, v));
    html = html.replace(/<aside>[\s\S]*?<\/aside>/, '');
    const doc = `<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400..700&family=Inter:wght@400;600&family=Space+Mono:wght@400;700&display=swap">
<style>html,body{margin:0;width:1920px;height:1080px;overflow:hidden}section{position:relative;box-sizing:border-box;width:1920px;height:1080px}
h1,h2,h3,p,ul,table{margin:0} table{border-collapse:collapse} th,td{padding:14px 18px;border-bottom:2px solid #2A4157;text-align:left}</style>
</head><body>${html}</body></html>`;
    const f = path.join(OUT, `slide_${s.id}.html`); fs.writeFileSync(f, doc);
    await page.goto('file://' + f); await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(OUT, `slide_${s.id}.png`) });
    console.log('slide', s.id);
  }
  await page.close();
  // 2) replay -> webm
  const demo = script.filter(s => s.kind === 'demo').map(s => (s.dur + GAP).toFixed(2));
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, recordVideo: { dir: OUT, size: { width: 1920, height: 1080 } } });
  const t0 = Date.now();
  const rp = await ctx.newPage();
  await rp.goto('file://' + path.join(ROOT, 'video', 'replay.html') + '?phases=' + demo.join(','));
  await rp.waitForFunction(() => window.__done === true, null, { timeout: 120000, polling: 500 });
  const started = await rp.evaluate(() => window.__started);
  const vid = await rp.video().path();
  await ctx.close(); await browser.close();
  fs.renameSync(vid, path.join(OUT, 'replay.webm'));
  fs.writeFileSync(path.join(OUT, 'replay_offset.txt'), String((started - t0) / 1000));
  console.log('replay recorded; animation starts at', (started - t0) / 1000, 's; phases', demo.join(','));
})();
