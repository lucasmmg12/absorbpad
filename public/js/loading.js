/* =============================================
   ABSORB PAD — Premium Loading Screen
   Animated progress bar + floating particles.
   Auto-dismiss after content loads.
   ============================================= */

(function () {
  'use strict';

  const screen = document.getElementById('loadingScreen');
  const bar = document.getElementById('loadingBar');
  const particlesContainer = document.getElementById('loadingParticles');
  if (!screen || !bar) return;

  // ---- Spawn floating particles ----
  if (particlesContainer) {
    for (let i = 0; i < 20; i++) {
      const p = document.createElement('div');
      p.className = 'loading-particle';
      p.style.left = Math.random() * 100 + '%';
      p.style.top = 40 + Math.random() * 50 + '%';
      p.style.animationDelay = Math.random() * 2 + 's';
      p.style.animationDuration = 1.5 + Math.random() * 2 + 's';
      // Mix teal and yellow particles
      if (Math.random() > 0.5) {
        p.style.background = '#2E8B98';
      }
      particlesContainer.appendChild(p);
    }
  }

  // ---- Simulated progress bar ----
  let progress = 0;
  const interval = setInterval(() => {
    // Accelerate near the end
    const increment = progress < 70 ? 2 + Math.random() * 3 : 0.5 + Math.random();
    progress = Math.min(progress + increment, 95);
    bar.style.width = progress + '%';
  }, 30);

  // ---- Dismiss on window load ----
  function dismiss() {
    clearInterval(interval);

    // Fill bar to 100%
    bar.style.width = '100%';

    // Wait a beat then fade out
    setTimeout(() => {
      screen.classList.add('fade-out');
      // Remove from DOM after transition
      setTimeout(() => {
        screen.remove();
      }, 900);
    }, 300);
  }

  // Trigger on window load or after max 3s safety timeout
  window.addEventListener('load', dismiss);
  setTimeout(dismiss, 3000);
})();
