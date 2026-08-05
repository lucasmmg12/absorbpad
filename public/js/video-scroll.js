/**
 * Absorbpad - Interactive Video Scroll Scrubber
 * Hardware-accelerated video scrubbing synced with window scroll position.
 * Controls video playback of Miner_tightening_bolt_on_truck_202608051255.mp4
 * and reveals corresponding Absorbpad products with hotspots & animations.
 */

export class VideoScrollScrubber {
  constructor(options = {}) {
    this.wrapper = document.querySelector(options.wrapper || '.video-scroll-wrapper');
    this.stickyBox = document.querySelector(options.stickyBox || '.sticky-video-box');
    this.canvas = document.querySelector(options.canvas || '#videoScrollCanvas');
    this.video = document.querySelector(options.video || '#scrollVideo');
    this.hudPhase = document.querySelector(options.hudPhase || '#videoHudPhase');
    this.hudTitle = document.querySelector(options.hudTitle || '#videoHudTitle');
    this.progressFill = document.querySelector(options.progressFill || '#videoProgressFill');
    this.cardsContainer = document.querySelector(options.cardsContainer || '#videoCardsContainer');
    this.hotspotsContainer = document.querySelector(options.hotspotsContainer || '#videoHotspotsContainer');
    
    if (!this.wrapper || !this.canvas || !this.video) {
      console.warn('VideoScrollScrubber: Required DOM elements not found.');
      return;
    }

    this.ctx = this.canvas.getContext('2d');
    this.duration = 10.0; // 10 seconds
    this.targetProgress = 0;
    this.currentProgress = 0;
    this.currentFrameTime = 0;
    this.isLoaded = false;

    // Timeline phases definition
    this.phases = [
      {
        id: 'yacimiento',
        startTime: 0.0,
        endTime: 2.5,
        badge: 'FASE 01 | YACIMIENTO MINERO',
        title: 'Protección Integral en Infraestructura Minera',
        description: 'Soluciones de contención masiva para yacimientos a gran escala y logística pesada.',
        hotspot: { x: 50, y: 75, label: 'Pallets de Contención & Cordones ABC' },
        products: [
          {
            name: 'Barreras y Cordones ABC',
            desc: 'Delimitación y contención de derrames sobre tierra o agua con microfibra Meltblown.',
            link: 'producto-abc.html',
            image: 'public/assets/Cordones.webp',
            badge: 'Contención'
          },
          {
            name: 'Pallets de Contención Pasiva',
            desc: 'Estructuras de polietileno homologadas para almacenamiento seguro de tambores e IBCs.',
            link: 'producto-pallets.html',
            image: 'public/assets/palet contencion.webp',
            badge: 'Infraestructura'
          }
        ]
      },
      {
        id: 'terreno',
        startTime: 2.5,
        endTime: 5.0,
        badge: 'FASE 02 | MANTENIMIENTO EN TERRENO',
        title: 'Absorción y Respuesta Rápida Bajo Vehículos Pesados',
        description: 'Mantas impermeables de suelo y kits portátiles desplegados directamente en zona de operación.',
        hotspot: { x: 40, y: 82, label: 'Mantas ABM / Paños Absorbentes' },
        products: [
          {
            name: 'Mantas Absorbentes ABM',
            desc: 'Protección de suelos de alta resistencia con base impermeable para equipos de minería.',
            link: 'producto-abm.html',
            image: 'public/assets/manta abosrbente.webp',
            badge: 'Absorción'
          },
          {
            name: 'Kits Antiderrame Yacimiento',
            desc: 'Equipamiento de respuesta inmediata listo para operar en camionetas y maquinaria pesada.',
            link: 'producto-kits.html',
            image: 'public/assets/kit-product.webp',
            badge: 'Respuesta Rápida'
          },
          {
            name: 'Desengrasante Bio Terpenos',
            desc: 'Limpieza ecológica de superficies libre de solventes clorados.',
            link: 'producto-desengrasante.html',
            image: 'public/assets/Bidon.webp',
            badge: 'Bio-Eco'
          }
        ]
      },
      {
        id: 'mecanica',
        startTime: 5.0,
        endTime: 7.5,
        badge: 'FASE 03 | HERRAMIENTAS Y ALTO TORQUE',
        title: 'Mantenimiento de Maquinaria Pesada y Limpieza Técnica',
        description: 'Herramientas neumáticas e inalámbricas para exigencia extrema en taller y campo.',
        hotspot: { x: 42, y: 55, label: 'Herramientas TOTAL 2026' },
        products: [
          {
            name: 'Herramientas Industriales TOTAL',
            desc: 'Llaves de impacto, herramientas a batería y equipamiento pesado 2026.',
            link: 'productos-total.html',
            image: 'public/assets/images.webp',
            badge: 'NUEVO 2026'
          },
          {
            name: 'Limpiamanos Fast Orange',
            desc: 'Fórmula cítrica con piedra pómez y aloe para remover grasa pesada sin agredir la piel.',
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
        badge: 'FASE 04 | FIJACIÓN QUÍMICA Y CRÍTICA',
        title: 'Traba Anaeróbica SILOC Serie Roja para Bulones de Alto Estrés',
        description: 'Fijador químico anaeróbico que previene el aflojamiento por vibración en camiones de gran porte.',
        hotspot: { x: 69, y: 49, label: 'Traba Anaeróbica Serie Roja SILOC', activeColor: '#FF2A4B' },
        products: [
          {
            name: 'Trabas Anaeróbicas SILOC (Roja)',
            desc: 'Traba química de alta resistencia para bulones y roscas en maquinaria pesada.',
            link: 'productos-anaerobicos.html',
            image: 'pdf_images/p04_img1.jpeg',
            badge: 'Alta Resistencia'
          },
          {
            name: 'Cianoacrilatos Instantáneos CIANO',
            desc: 'Adhesivos de curado veloz para unión estructural de goma, metal y plástico.',
            link: 'productos-cianoacrilatos.html',
            image: 'productos-cianoacrilatos.html',
            image: 'pdf_images/p13_img1.jpeg',
            badge: 'Instantáneo'
          },
          {
            name: 'Selladores SILOC Siliconas & Poliuretano',
            desc: 'Sellado elástico y estanqueidad técnica para juntas industriales.',
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
    this.resizeCanvas();
    window.addEventListener('resize', () => this.resizeCanvas());

    // Prepare Video
    this.video.currentTime = 0;
    this.video.pause();

    this.video.addEventListener('loadeddata', () => {
      this.isLoaded = true;
      this.renderFrame(0);
    });

    if (this.video.readyState >= 2) {
      this.isLoaded = true;
      this.renderFrame(0);
    }

    // Bind Phase Nav Buttons if present
    const phaseBtns = document.querySelectorAll('.phase-step-btn');
    phaseBtns.forEach((btn, idx) => {
      btn.addEventListener('click', () => {
        this.scrollToPhase(idx);
      });
    });

    // Start Animation Loop
    this.loop();
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
    if (this.isLoaded) {
      this.renderFrame(this.currentFrameTime);
    }
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
    
    // Smooth lerp for liquid 60fps scrubbing
    this.currentProgress += (this.targetProgress - this.currentProgress) * 0.18;
    this.currentFrameTime = this.currentProgress * this.duration;

    if (this.isLoaded && Math.abs(this.video.currentTime - this.currentFrameTime) > 0.03) {
      this.video.currentTime = this.currentFrameTime;
    }

    this.renderFrame(this.currentFrameTime);
    this.updateHUD(this.currentProgress, this.currentFrameTime);

    requestAnimationFrame(() => this.loop());
  }

  renderFrame(time) {
    if (!this.ctx || !this.video || !this.canvasWidth || !this.canvasHeight) return;

    this.ctx.clearRect(0, 0, this.canvasWidth, this.canvasHeight);

    const videoRatio = 1280 / 720;
    const canvasRatio = this.canvasWidth / this.canvasHeight;
    let drawW, drawH, drawX, drawY;

    if (canvasRatio > videoRatio) {
      drawW = this.canvasWidth;
      drawH = this.canvasWidth / videoRatio;
      drawX = 0;
      drawY = (this.canvasHeight - drawH) / 2;
    } else {
      drawH = this.canvasHeight;
      drawW = this.canvasHeight * videoRatio;
      drawX = (this.canvasWidth - drawW) / 2;
      drawY = 0;
    }

    this.ctx.drawImage(this.video, drawX, drawY, drawW, drawH);
  }

  updateHUD(progress, time) {
    if (this.progressFill) {
      this.progressFill.style.width = `${(progress * 100).toFixed(1)}%`;
    }

    let currentPhaseIdx = 0;
    for (let i = 0; i < this.phases.length; i++) {
      if (time >= this.phases[i].startTime && time <= this.phases[i].endTime) {
        currentPhaseIdx = i;
        break;
      }
    }

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
      <div class="video-product-card glass-panel">
        <div class="card-badge">${prod.badge}</div>
        <div class="card-img-wrap">
          <img src="${prod.image}" alt="${prod.name}" class="card-img">
        </div>
        <div class="card-content">
          <h4 class="card-title">${prod.name}</h4>
          <p class="card-desc">${prod.desc}</p>
          <a href="${prod.link}" class="card-btn btn-sm btn-primary">
            Ver Ficha Técnica <ion-icon name="arrow-forward-outline"></ion-icon>
          </a>
        </div>
      </div>
    `).join('');
  }
}

// Auto-initialize on load
document.addEventListener('DOMContentLoaded', () => {
  if (document.querySelector('.video-scroll-wrapper')) {
    window.videoScrubber = new VideoScrollScrubber();
  }
});
