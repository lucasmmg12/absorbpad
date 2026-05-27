/* =============================================
   ABSORB PAD — Hero Morphing Text Rotator
   Cycles through industrial phrases with a
   blur-dissolve transition effect.
   ============================================= */

(function () {
  'use strict';

  const el = document.getElementById('heroMorph');
  if (!el) return;

  const phrases = [
    'Eficiencia Máxima',
    'Absorción Inmediata',
    'Protección Total',
    'Respuesta Rápida',
    'Control Absoluto',
    'Sellado Perfecto',
    'Cero Derrames',
    'Máxima Seguridad',
  ];

  let current = 0;
  const DISPLAY_TIME = 3000;  // Time each phrase is visible (ms)
  const MORPH_TIME = 600;     // Must match CSS transition duration

  function morphTo(index) {
    // Phase 1: Blur out current text
    el.classList.add('morph-out');

    setTimeout(() => {
      // Phase 2: Swap text while invisible
      el.textContent = phrases[index];
      el.classList.remove('morph-out');
      el.classList.add('morph-in');

      // Phase 3: Force reflow then fade in
      void el.offsetWidth;
      el.classList.remove('morph-in');
    }, MORPH_TIME);
  }

  function cycle() {
    current = (current + 1) % phrases.length;
    morphTo(current);
  }

  // Start cycling after initial display
  setInterval(cycle, DISPLAY_TIME + MORPH_TIME);
})();
