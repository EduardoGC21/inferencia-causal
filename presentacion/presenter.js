/* Small presentation shell; navigation, scaling and print layout use Reveal.js. */
const spanish = document.documentElement.lang.startsWith('es');
const words = spanish
  ? { overview: 'Índice', previous: 'Anterior', next: 'Siguiente', pdf: 'Exportar PDF', present: 'Presentar', save: 'Elige «Guardar como PDF», sin márgenes y con gráficos de fondo.', fullscreen: 'Abre el archivo HTML en una pestaña propia para usar pantalla completa.' }
  : { overview: 'Overview', previous: 'Previous', next: 'Next', pdf: 'Export PDF', present: 'Present', save: 'Choose “Save as PDF”, no margins, and background graphics.', fullscreen: 'Open the HTML file in its own tab to use fullscreen.' };
const embedded = window.self !== window.top;
document.documentElement.classList.toggle('embedded', embedded);
const stage = document.querySelector('.reveal');
const player = document.createElement('main');
player.id = 'presentation';
stage.before(player);
player.append(stage);
const toolbar = document.createElement('nav');
toolbar.className = 'deck-toolbar';
toolbar.setAttribute('aria-label', spanish ? 'Presentación' : 'Presentation');
toolbar.innerHTML = `<button data-action="overview">${words.overview}</button>
  <button data-action="previous" aria-label="${words.previous}">←</button>
  <span class="deck-counter" aria-live="polite"></span>
  <button data-action="next" aria-label="${words.next}">→</button>
  <span class="deck-spacer"></span>
  <button data-action="pdf">${words.pdf}</button>
  <button data-action="present" class="deck-present">${words.present} ⛶</button>`;
player.append(toolbar);
const status = document.createElement('p');
status.className = 'deck-status';
status.setAttribute('role', 'status');
player.after(status);
function fitWindow() {
  player.style.setProperty('--player-height', `${window.innerHeight}px`);
  if (window.Reveal?.isReady()) Reveal.layout();
}
fitWindow();
window.addEventListener('resize', fitWindow);
document.addEventListener('fullscreenchange', fitWindow);
if (!window.Reveal) {
  status.textContent = spanish ? 'No se pudo cargar Reveal.js. Revisa la conexión o usa una copia local del motor.' : 'Reveal.js could not load. Check the connection or use a local runtime copy.';
  toolbar.querySelectorAll('button').forEach(button => { button.disabled = true; });
} else {
  window.deckReady = Reveal.initialize({
    width: 1280, height: 720, margin: 0.025, minScale: 0.1, maxScale: 2,
    embedded: true, center: false, hash: true, controls: false, progress: false,
    transition: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'none' : 'fade',
    backgroundTransition: 'none', pdfSeparateFragments: false,
    ...window.deckOptions
  }).then(async () => {
    const previous = toolbar.querySelector('[data-action="previous"]');
    const next = toolbar.querySelector('[data-action="next"]');
    function updateCounter() {
      toolbar.querySelector('.deck-counter').textContent = `${Reveal.getSlidePastCount() + 1} / ${Reveal.getTotalSlides()}`;
      previous.disabled = Reveal.isFirstSlide();
      next.disabled = Reveal.isLastSlide();
    }
    updateCounter();
    Reveal.on('slidechanged', updateCounter);
    toolbar.querySelector('[data-action="overview"]').onclick = () => Reveal.toggleOverview();
    previous.onclick = () => Reveal.prev();
    next.onclick = () => Reveal.next();
    toolbar.querySelector('[data-action="present"]').onclick = async () => {
      try { await player.requestFullscreen(); }
      catch { status.textContent = words.fullscreen; }
    };
    toolbar.querySelector('[data-action="pdf"]').onclick = () => {
      const url = new URL(location.href);
      url.searchParams.set('print-pdf', '');
      url.searchParams.set('export-pdf', '');
      url.hash = '';
      window.open(url.href, '_blank', 'noopener');
    };
    if (new URLSearchParams(location.search).has('export-pdf')) {
      status.textContent = words.save;
      await document.fonts.ready;
      requestAnimationFrame(() => requestAnimationFrame(() => window.print()));
    }
  });
}
