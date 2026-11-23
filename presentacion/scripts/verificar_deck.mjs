import assert from 'node:assert/strict';
import { mkdir, mkdtemp, readFile, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const path = name => fileURLToPath(new URL('../' + name, import.meta.url));
const shots = await mkdtemp(join(tmpdir(), 'inferencia-deck-'));
const url = new URL('../index.html', import.meta.url);
const script = await readFile(path('guion.md'), 'utf8');
const browser = await chromium.launch();
try {
  const page = await browser.newPage({ offline: true, viewport: { width: 1440, height: 900 } });
  const errors = [];
  const remote = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('request', request => {
    if (/^https?:/.test(request.url())) remote.push(request.url());
  });
  const ready = async () => {
    await page.waitForFunction(() => window.Reveal?.isReady());
    await page.evaluate(async () => {
      await window.deckReady;
      await document.fonts.ready;
      await Promise.all([...document.images].map(image => image.decode()));
    });
  };
  await page.goto(url.href);
  await ready();
  const slides = await page.evaluate(() => Reveal.getSlides().map(s => ({
    id: s.id, seconds: Number(s.dataset.timing),
    speech: s.querySelector('aside p:nth-child(2)').textContent,
    transition: s.querySelector('aside p:nth-child(3)').textContent.replace('Transición. ', '')
  })));
  const duration = slides.reduce((sum, slide) => sum + slide.seconds, 0);
  assert.equal(duration, 480);
  for (const { id, speech, transition } of slides) {
    assert.ok(script.includes(speech) && script.includes(transition), id);
  }
  const equations = await page.locator('[data-tex]').count();
  assert.ok(equations > 0);
  assert.equal(await page.locator('[data-tex] .katex').count(), equations);
  for (const [i, slide] of slides.entries()) {
    await page.evaluate(i => Reveal.slide(i), i);
    await page.evaluate(() => document.fonts.ready);
    const surface = page.locator('section.present .slide-surface');
    const clipped = await surface.evaluate(surface => {
      const frame = surface.getBoundingClientRect();
      return [...surface.querySelectorAll('header, p, img, figcaption, .equation, td, th, a')]
        .filter(el => {
          const box = el.getBoundingClientRect();
          return box.right > frame.right + 1 || box.bottom > frame.bottom + 1;
        }).map(el => el.tagName + ' ' + el.textContent.slice(0, 38));
    });
    assert.deepEqual(clipped, [], slide.id);
    await surface.screenshot({ path: join(shots, `${String(i + 1).padStart(2, '0')}-${slide.id}.png`) });
  }
  assert.ok(await page.evaluate(() =>
    [...document.fonts].some(font => font.family.includes('KaTeX_') && font.status === 'loaded')
  ));
  await page.evaluate(i => Reveal.slide(i), slides.findIndex(slide => slide.id === 'conclusion'));
  await page.locator('section.present a[href="#/respaldos"]').click();
  assert.equal(await page.evaluate(() => Reveal.getCurrentSlide().id), 'respaldos');
  await page.locator('section.present a[href="#/conclusion"]').click();
  assert.equal(await page.evaluate(() => Reveal.getCurrentSlide().id), 'conclusion');

  url.searchParams.set('print-pdf', '');
  await page.goto(url.href);
  await ready();
  await page.waitForFunction(count => document.querySelectorAll('.pdf-page').length === count, slides.length);
  await page.pdf({ path: path('presentacion.pdf'), printBackground: true, preferCSSPageSize: true });
  assert.deepEqual(errors, []);
  assert.deepEqual(remote, []);
  const report = {
    prueba: 'Archivo local en Chromium, red desactivada, 1440 × 900',
    principales: slides.filter(s => s.seconds).length,
    respaldos: slides.filter(s => !s.seconds).length,
    segundos: duration,
    ecuaciones_katex: equations,
    notas_y_transiciones_cotejadas: slides.length,
    paginas_impresas: slides.length,
    solicitudes_externas: remote.length,
    errores: errors.length
  };
  await mkdir(path('verificacion'), { recursive: true });
  await writeFile(path('verificacion/resultado.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report));
  console.log('Capturas de revisión: ' + shots);
} finally {
  await browser.close();
}
