import assert from 'node:assert/strict';
import { chromium } from 'playwright';

const browser = await chromium.launch();
try {
  const page = await browser.newPage({ offline: true });
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto(new URL('../index.html', import.meta.url).href);
  await page.waitForFunction(() => window.Reveal?.isReady());
  await page.evaluate(() => window.deckReady);
  await page.keyboard.press('ArrowRight');
  assert.equal(await page.evaluate(() => Reveal.getCurrentSlide().id), 'datos');
  await page.keyboard.press('ArrowLeft');
  assert.equal(await page.evaluate(() => Reveal.getCurrentSlide().id), 'pregunta');
  assert.deepEqual(errors, []);
  console.log('Carga sin conexión. Las flechas avanzan y regresan.');
} finally {
  await browser.close();
}
