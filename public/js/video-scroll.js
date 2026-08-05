/**
 * Absorbpad - Interactive Video Scroll Scrubber
 * 60 FPS Apple-Grade Fullscreen Frame Sequence Scrubber & Interactive Embedded Narrative
 * Controls playback of Miner_tightening_bolt_on_truck_202608051255 video frames
 * and embeds synchronized text, interactive product tags, and hotspots.
 */

export class VideoScrollScrubber {
  constructor(options = {}) {
    this.wrapper = document.querySelector(options.wrapper || '.video-scroll-wrapper');
    this.stickyBox = document.querySelector(options.stickyBox || '.sticky-video-box');
    this.canvas = document.querySelector(options.canvas || '#videoScrollCanvas');
    this.video = document.querySelector(options.video || '#scrollVideo');
    this.hudPhase = document.querySelector(options.hudPhase || '#videoHudPhase');
    this.hudTitle = document.querySelector(options.hudTitle || '#videoHudTitle');
    this.hudDesc = document.querySelector(options.hudDesc || '#videoHudDesc');
    this.progressFill = document.querySelector(options.progressFill || '#videoProgressFill');
    this.cardsContainer = document.querySelector(options.cardsContainer || '#videoCardsContainer');
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

    // Timeline phases definition with exact products & embedded text
    this.phases = [
      {
        id: 'yacimiento',
        startTime: 0.0,
        endTime: 2.5,
        badge: 'FASE 01 | YACIMIENTO MINERO',
        title: 'Protección Integral en Yacimientos',
        description: 'Delimitación y contención pasiva para yacimientos a gran escala y logística de minería pesada.',
        hotspot: { x: 50, y: 72, label: 'Pallets de Contención & Cordones ABC' },
        products: [
          {
            name: 'Barreras y Cordones ABC',
            desc: 'Microfibra Meltblown de alta absorción para delimitar derrames sobre tierra o agua.',
            link: 'producto-abc.html',
            image: 'assets/Cordones.webp',
            badge: 'Contención'
          },
          {
            name: 'Pallets de Contención Pasiva',
            desc: 'Estructuras homologadas para almacenamiento seguro de tambores e IBCs.',
            link: 'producto-pallets.html',
            image: 'assets/palet contencion.webp',
            badge: 'Infraestructura'
          }
        ]
      },
      {
        id: 'terreno',
        startTime: 2.5,
        endTime: 5.0,
        badge: 'FASE 02 | MANTENIMIENTO EN TERRENO',
        title: 'Absorción y Respuesta Rápida',
        description: 'Mantas impermeables de suelo y kits portátiles desplegados bajo camionetas y camiones mineros.',
        hotspot: { x: 42, y: 80, label: 'Mantas ABM & Paños Absorbentes' },
        products: [
          {
            name: 'Mantas Absorbentes ABM',
            desc: 'Protección de suelo con base impermeable para equipos de perforación y acarreo.',
            link: 'producto-abm.html',
            image: 'assets/manta abosrbente.webp',
            badge: 'Absorción Suelo'
          },
          {
            name: 'Kits Antiderrame Yacimiento',
            desc: 'Respuesta inmediata en flota vehicular y estaciones de bombeo.',
            link: 'producto-kits.html',
            image: 'assets/kit-product.webp',
            badge: 'Respuesta Rápida'
          },
          {
            name: 'Desengrasante Bio Terpenos',
            desc: 'Limpieza ecológica de motores y chasis libre de solventes clorados.',
            link: 'producto-desengrasante.html',
            image: 'assets/Bidon.webp',
            badge: 'Bio-Eco'
          }
        ]
      },
      {
        id: 'mecanica',
        startTime: 5.0,
        endTime: 7.5,
        badge: 'FASE 03 | ALTO TORQUE Y HERRAMIENTAS',
        title: 'Mantenimiento de Maquinaria Pesada',
        description: 'Herramientas a batería y neumáticas para ajuste de llantas en camiones Caterpillar/Komatsu.',
        hotspot: { x: 44, y: 54, label: 'Herramientas TOTAL 2026' },
        products: [
          {
            name: 'Herramientas Industriales TOTAL',
            desc: 'Llaves de impacto a batería y equipamiento pesado 2026.',
            link: 'productos-total.html',
            image: 'assets/images.webp',
            badge: 'NUEVO 2026'
          },
          {
            name: 'Limpiamanos Fast Orange',
            desc: 'Fórmula cítrica biodegradable con piedra pómez para remover grasa pesada.',
            link: 'productos-limpiamanos.html',
            image: 'pdf_images/p37_img1.jpeg',
            badge: 'Higiene Industrial'
          }
        ]
      },
      {
        id: 'fijacion',
        startTime: 7.5,
        endTime: 10.0,
        badge: 'FASE 04 | FIJACIÓN QUÍMICA Y TRABA DE ROSCAS',
        title: 'Traba Anaeróbica SILOC Serie Roja',
        description: 'Fijador químico anaeróbico de máxima resistencia que bloquea aflojamientos por vibración en bulones de ruedas.',
        hotspot: { x: 68, y: 48, label: 'Traba Anaeróbica SILOC Serie Roja', activeColor: '#FF2A4B' },
        products: [
          {
            name: 'Trabas Anaeróbicas SILOC (Roja)',
            desc: 'Traba química de alta resistencia para roscas y bulones sometidos a extrema vibración.',
            link: 'productos-anaerobicos.html',
            image: 'pdf_images/p04_img1.jpeg',
            badge: 'Alta Resistencia'
          },
          {
            name: 'Cianoacrilatos CIANO 2000',
            desc: 'Adhesivos instantáneos de rápida velocidad para caucho, metal y plásticos.',
            link: 'productos-cianoacrilatos.html',
            image: 'pdf_images/p13_img1.jpeg',
            badge: 'Instantáneo'
          },
          {
            name: 'Selladores SILOC Silicona / PU',
            desc: 'Estanqueidad técnica y sellado de alto desempeño para juntas.',
            link: 'productos-selladores.html',
            image: 'pdf_images/p16_img1.jpeg',
            badge: 'Estanqueidad'
          }
        ]
      }
    ];

    this.activePhaseIndex = -1;
    this.init();
  }

  init() {
    this.preloadFrames();
    this.resizeCanvas();
    window.addEventListener('resize', () => this.resizeCanvas());

    // Bind Phase Nav Buttons
    const phaseBtns = document.querySelectorAll('.phase-step-btn');
    phaseBtns.forEach((btn, idx) => {
      btn.addEventListener('click', () => {
        this.scrollToPhase(idx);
      });
    });

    // Start 60fps Loop
    this.loop();
  }

  preloadFrames() {
    for (let i = 0; i < this.totalFrameCount; i++) {
      const img = new Image();
      const numStr = String(i).padStart(3, '0');
      // Relative path works in both dev server and production
      img.src = `assets/video_frames/frame_${numStr}.jpg`;
      img.onerror = () => {
        // Fallback path attempt if required
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

  scrollToPhase(index) {
    if (!this.wrapper) return;
    const phase = this.phases[index];
    if (!phase) return;
    
    const wrapperRect = this.wrapper.getBoundingClientRect();
    const absoluteTop = window.pageYOffset + wrapperRect.top;
    const scrollableDistance = this.wrapper.offsetHeight - window.innerHeight;
    
    const targetTime = (phase.startTime + phase.endTime) / 2;
    const progressRatio = targetTime / this.duration;
    
    const scrollToY = absoluteTop + (progressRatio * scrollableDistance);
    window.scrollTo({ top: scrollToY, behavior: 'smooth' });
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

    // Clear canvas
    this.ctx.clearRect(0, 0, this.canvasWidth, this.canvasHeight);

    // Draw frame to canvas if loaded
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
      // Fallback to video element
      const currentTime = this.currentProgress * this.duration;
      if (Math.abs(this.video.currentTime - currentTime) > 0.05) {
        this.video.currentTime = currentTime;
      }
      this.ctx.drawImage(this.video, 0, 0, this.canvasWidth, this.canvasHeight);
    }

    this.updateHUD(this.currentProgress);
  }

  updateHUD(progress) {
    if (this.progressFill) {
      this.progressFill.style.width = `${(progress * 100).toFixed(1)}%`;
    }

    const time = progress * this.duration;
    let currentPhaseIdx = 0;
    for (let i = 0; i < this.phases.length; i++) {
      if (time >= this.phases[i].startTime && time <= this.phases[i].endTime) {
        currentPhaseIdx = i;
        break;
      }
    }

    // Update active nav buttons
    const phaseBtns = document.querySelectorAll('.phase-step-btn');
    phaseBtns.forEach((btn, idx) => {
      if (idx === currentPhaseIdx) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    if (currentPhaseIdx !== this.activePhaseIndex) {
      this.activePhaseIndex = currentPhaseIdx;
      const phase = this.phases[currentPhaseIdx];

      if (this.hudPhase && this.hudTitle) {
        this.hudPhase.textContent = phase.badge;
        this.hudTitle.textContent = phase.title;
        if (this.hudDesc) this.hudDesc.textContent = phase.description;
      }

      this.renderHotspot(phase.hotspot);
      this.renderCards(phase.products);
    }
  }

  renderHotspot(hotspot) {
    if (!this.hotspotsContainer || !hotspot) return;

    const activeColor = hotspot.activeColor || '#F9D423';
    this.hotspotsContainer.innerHTML = `
      <div class="video-hotspot-pin" style="left: ${hotspot.x}%; top: ${hotspot.y}%;">
        <div class="pulse-ring" style="border-color: ${activeColor};"></div>
        <div class="center-dot" style="background-color: ${activeColor};"></div>
        <div class="hotspot-tooltip">
          <span class="tooltip-badge">PRODUCTO EN ACCIÓN</span>
          <span class="tooltip-title">${hotspot.label}</span>
        </div>
      </div>
    `;
  }

  renderCards(products) {
    if (!this.cardsContainer || !products) return;

    this.cardsContainer.innerHTML = products.map(prod => `
      <a href="${prod.link}" class="embedded-product-chip">
        <div class="chip-img-wrap">
          <img src="${prod.image}" alt="${prod.name}" class="chip-img" onerror="if(!this.src.includes('pdf_images/')){this.src='pdf_images/p04_img1.jpeg';}">
        </div>
        <div class="chip-info">
          <span class="chip-badge">${prod.badge}</span>
          <h4 class="chip-title">${prod.name}</h4>
          <p class="chip-desc">${prod.desc}</p>
        </div>
        <div class="chip-arrow">
          <ion-icon name="arrow-forward-outline"></ion-icon>
        </div>
      </a>
    `).join('');
  }
}

// Auto-initialize on load
document.addEventListener('DOMContentLoaded', () => {
  if (document.querySelector('.video-scroll-wrapper')) {
    window.videoScrubber = new VideoScrollScrubber();
  }
});
