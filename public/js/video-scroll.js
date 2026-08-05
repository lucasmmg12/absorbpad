/**
 * Absorbpad - Minimalist Cinematic Video Scroll Scrubber
 * 60 FPS Apple-Grade Fullscreen Frame Sequence Scrubber
 * Renders pure fullscreen video with dynamic floating typography and pulsing hotspots.
 * NO static boxes, NO dark container cards.
 */

export class VideoScrollScrubber {
  constructor(options = {}) {
    this.wrapper = document.querySelector(options.wrapper || '.video-scroll-wrapper');
    this.stickyBox = document.querySelector(options.stickyBox || '.sticky-video-box');
    this.canvas = document.querySelector(options.canvas || '#videoScrollCanvas');
    this.video = document.querySelector(options.video || '#scrollVideo');
    this.hudPhase = document.querySelector(options.hudPhase || '#videoHudPhase');
    this.hudTitle = document.querySelector(options.hudTitle || '#videoHudTitle');
    this.hotspotsContainer = document.querySelector(options.hotspotsContainer || '#videoHotspotsContainer');

    if (!this.wrapper || !this.canvas) {
      console.warn('VideoScrollScrubber: Required DOM elements not found.');
      return;
    }

    this.ctx = this.canvas.getContext('2d');
    this.totalFrameCount = 120; // 120 extracted frames
    this.frameImages = [];
    this.loadedFramesCount = 0;
    this.targetProgress = 0;
    this.currentProgress = 0;
    this.duration = 10.0;

    // Minimalist Timeline Phases (Pure Hotspots & Typography Captions)
    this.phases = [
      {
        id: 'yacimiento',
        startTime: 0.0,
        endTime: 2.5,
        badge: 'FASE 01 | YACIMIENTO MINERO',
        title: 'Protección & Contención Pasiva en Yacimientos',
        hotspot: {
          x: 50,
          y: 72,
          label: 'Pallets de Contención & Cordones ABC',
          link: 'producto-abc.html',
          badge: 'Contención'
        }
      },
      {
        id: 'terreno',
        startTime: 2.5,
        endTime: 5.0,
        badge: 'FASE 02 | MANTENIMIENTO EN TERRENO',
        title: 'Mantas Absorbentes ABM & Kits Antiderrame',
        hotspot: {
          x: 42,
          y: 80,
          label: 'Mantas ABM / Paños Absorbentes',
          link: 'producto-abm.html',
          badge: 'Absorción Suelo'
        }
      },
      {
        id: 'mecanica',
        startTime: 5.0,
        endTime: 7.5,
        badge: 'FASE 03 | HERRAMIENTAS Y ALTO TORQUE',
        title: 'Herramientas TOTAL 2026 & Limpiamanos',
        hotspot: {
          x: 44,
          y: 54,
          label: 'Llave de Impacto TOTAL 2026',
          link: 'productos-total.html',
          badge: 'Alto Torque'
        }
      },
      {
        id: 'fijacion',
        startTime: 7.5,
        endTime: 10.0,
        badge: 'FASE 04 | FIJACIÓN QUÍMICA Y ROSCAS',
        title: 'Traba Anaeróbica SILOC Serie Roja (Alta Resistencia)',
        hotspot: {
          x: 68,
          y: 48,
          label: 'Traba Anaeróbica SILOC Serie Roja',
          link: 'productos-anaerobicos.html',
          badge: 'Fijación Roscas',
          activeColor: '#FF2A4B'
        }
      }
    ];

    this.activePhaseIndex = -1;
    this.init();
  }

  init() {
    this.preloadFrames();
    this.resizeCanvas();
    window.addEventListener('resize', () => this.resizeCanvas());

    // Start 60fps Loop
    this.loop();
  }

  preloadFrames() {
    for (let i = 0; i < this.totalFrameCount; i++) {
      const img = new Image();
      const numStr = String(i).padStart(3, '0');
      img.src = `assets/video_frames/frame_${numStr}.jpg`;
      img.onerror = () => {
        if (!img.src.includes('public/')) {
          img.src = `public/assets/video_frames/frame_${numStr}.jpg`;
        }
      };
      img.onload = () => {
        this.loadedFramesCount++;
      };
      this.frameImages.push(img);
    }
  }

  resizeCanvas() {
    if (!this.canvas || !this.stickyBox) return;
    const rect = this.stickyBox.getBoundingClientRect();
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    this.canvas.width = rect.width * dpr;
    this.canvas.height = rect.height * dpr;
    this.ctx.scale(dpr, dpr);
    this.canvasWidth = rect.width;
    this.canvasHeight = rect.height;
    this.renderCurrentProgress();
  }

  calculateScrollProgress() {
    if (!this.wrapper) return 0;
    const rect = this.wrapper.getBoundingClientRect();
    const totalScroll = this.wrapper.offsetHeight - window.innerHeight;
    if (totalScroll <= 0) return 0;
    
    const currentScroll = -rect.top;
    let progress = currentScroll / totalScroll;
    return Math.max(0, Math.min(1, progress));
  }

  loop() {
    this.targetProgress = this.calculateScrollProgress();
    
    // Smooth lerp for liquid 60fps animation
    this.currentProgress += (this.targetProgress - this.currentProgress) * 0.22;
    
    this.renderCurrentProgress();
    requestAnimationFrame(() => this.loop());
  }

  renderCurrentProgress() {
    const frameIndex = Math.min(
      this.totalFrameCount - 1,
      Math.max(0, Math.floor(this.currentProgress * (this.totalFrameCount - 1)))
    );

    const frameImg = this.frameImages[frameIndex];

    this.ctx.clearRect(0, 0, this.canvasWidth, this.canvasHeight);

    if (frameImg && frameImg.complete && frameImg.naturalWidth > 0) {
      const imgRatio = frameImg.naturalWidth / frameImg.naturalHeight;
      const canvasRatio = this.canvasWidth / this.canvasHeight;
      let drawW, drawH, drawX, drawY;

      if (canvasRatio > imgRatio) {
        drawW = this.canvasWidth;
        drawH = this.canvasWidth / imgRatio;
        drawX = 0;
        drawY = (this.canvasHeight - drawH) / 2;
      } else {
        drawH = this.canvasHeight;
        drawW = this.canvasHeight * imgRatio;
        drawX = (this.canvasWidth - drawW) / 2;
        drawY = 0;
      }

      this.ctx.drawImage(frameImg, drawX, drawY, drawW, drawH);
    } else if (this.video && this.video.readyState >= 2) {
      const currentTime = this.currentProgress * this.duration;
      if (Math.abs(this.video.currentTime - currentTime) > 0.05) {
        this.video.currentTime = currentTime;
      }
      this.ctx.drawImage(this.video, 0, 0, this.canvasWidth, this.canvasHeight);
    }

    this.updateHUD(this.currentProgress);
  }

  updateHUD(progress) {
    const time = progress * this.duration;
    let currentPhaseIdx = 0;
    for (let i = 0; i < this.phases.length; i++) {
      if (time >= this.phases[i].startTime && time <= this.phases[i].endTime) {
        currentPhaseIdx = i;
        break;
      }
    }

    if (currentPhaseIdx !== this.activePhaseIndex) {
      this.activePhaseIndex = currentPhaseIdx;
      const phase = this.phases[currentPhaseIdx];

      if (this.hudPhase && this.hudTitle) {
        this.hudPhase.textContent = phase.badge;
        this.hudTitle.textContent = phase.title;
      }

      this.renderHotspot(phase.hotspot);
    }
  }

  renderHotspot(hotspot) {
    if (!this.hotspotsContainer || !hotspot) return;

    const activeColor = hotspot.activeColor || '#F9D423';
    this.hotspotsContainer.innerHTML = `
      <a href="${hotspot.link || '#'}" class="video-hotspot-pin" style="left: ${hotspot.x}%; top: ${hotspot.y}%;">
        <div class="pulse-ring" style="border-color: ${activeColor};"></div>
        <div class="center-dot" style="background-color: ${activeColor};"></div>
        <div class="hotspot-tooltip">
          <span class="tooltip-badge">${hotspot.badge || 'PRODUCTO EN ACCIÓN'}</span>
          <span class="tooltip-title">${hotspot.label} <ion-icon name="arrow-forward-outline"></ion-icon></span>
        </div>
      </a>
    `;
  }
}

// Auto-initialize on load
document.addEventListener('DOMContentLoaded', () => {
  if (document.querySelector('.video-scroll-wrapper')) {
    window.videoScrubber = new VideoScrollScrubber();
  }
});
