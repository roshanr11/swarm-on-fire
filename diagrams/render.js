// Render diagrams/*.html to results/figures/diag_*.png. Usage: node diagrams/render.js
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 900 }, deviceScaleFactor: 2 });
  for (const n of ['design', 'pipeline']) {
    await p.goto('file://' + path.join(__dirname, n + '.html')); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    await (await p.$('.wrap')).screenshot({ path: path.join(__dirname, '..', 'results', 'figures', `diag_${n}.png`) });
    console.log('rendered', n);
  }
  await b.close();
})();
