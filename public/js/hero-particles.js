/* =============================================
   ABSORB PAD — Interactive Fluid Particles (Three.js)
   Premium 3D hero animation with mouse-reactive
   particle system simulating fluid molecules.
   ============================================= */

(function () {
  'use strict';

  const canvas = document.getElementById('hero-particles');
  if (!canvas || typeof THREE === 'undefined') return;

  const heroSection = canvas.closest('.hero');
  if (!heroSection) return;

  // ---- CONFIGURATION ----
  const PARTICLE_COUNT = 800;
  const PARTICLE_SIZE = 2.5;
  const SPREAD = 60;
  const MOUSE_RADIUS = 12;
  const MOUSE_FORCE = 0.08;
  const RETURN_SPEED = 0.015;
  const FLOW_SPEED = 0.0004;
  const COLOR_TEAL = new THREE.Color(0x2E8B98);
  const COLOR_YELLOW = new THREE.Color(0xF9D423);
  const COLOR_WHITE = new THREE.Color(0xE0F7FA);

  // ---- SCENE SETUP ----
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, 1, 0.1, 200);
  camera.position.z = 50;

  const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    alpha: true,
    antialias: true,
    powerPreference: 'high-performance'
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setClearColor(0x000000, 0);

  // ---- PARTICLE SYSTEM ----
  const geometry = new THREE.BufferGeometry();
  const positions = new Float32Array(PARTICLE_COUNT * 3);
  const colors = new Float32Array(PARTICLE_COUNT * 3);
  const sizes = new Float32Array(PARTICLE_COUNT);
  const velocities = new Float32Array(PARTICLE_COUNT * 3);
  const origPositions = new Float32Array(PARTICLE_COUNT * 3);

  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const i3 = i * 3;

    // Distribute in a fluid-like ellipsoid
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    const r = SPREAD * Math.cbrt(Math.random());

    positions[i3] = r * Math.sin(phi) * Math.cos(theta) * 1.4;
    positions[i3 + 1] = r * Math.sin(phi) * Math.sin(theta) * 0.6;
    positions[i3 + 2] = r * Math.cos(phi) * 0.8;

    origPositions[i3] = positions[i3];
    origPositions[i3 + 1] = positions[i3 + 1];
    origPositions[i3 + 2] = positions[i3 + 2];

    velocities[i3] = 0;
    velocities[i3 + 1] = 0;
    velocities[i3 + 2] = 0;

    // Color gradient: teal -> yellow -> white
    const t = Math.random();
    const color = new THREE.Color();
    if (t < 0.5) {
      color.lerpColors(COLOR_TEAL, COLOR_YELLOW, t * 2);
    } else {
      color.lerpColors(COLOR_YELLOW, COLOR_WHITE, (t - 0.5) * 2);
    }
    colors[i3] = color.r;
    colors[i3 + 1] = color.g;
    colors[i3 + 2] = color.b;

    sizes[i] = PARTICLE_SIZE * (0.5 + Math.random() * 1.0);
  }

  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

  // ---- SHADER MATERIAL ----
  const material = new THREE.ShaderMaterial({
    vertexShader: `
      attribute float size;
      varying vec3 vColor;
      varying float vAlpha;
      void main() {
        vColor = color;
        vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
        float dist = length(mvPosition.xyz);
        vAlpha = clamp(1.0 - dist / 80.0, 0.15, 0.85);
        gl_PointSize = size * (45.0 / -mvPosition.z);
        gl_Position = projectionMatrix * mvPosition;
      }
    `,
    fragmentShader: `
      varying vec3 vColor;
      varying float vAlpha;
      void main() {
        float d = length(gl_PointCoord - vec2(0.5));
        if (d > 0.5) discard;
        float glow = smoothstep(0.5, 0.0, d);
        gl_FragColor = vec4(vColor, vAlpha * glow);
      }
    `,
    transparent: true,
    depthWrite: false,
    vertexColors: true,
    blending: THREE.AdditiveBlending
  });

  const particles = new THREE.Points(geometry, material);
  scene.add(particles);

  // ---- AMBIENT GLOW (subtle central light) ----
  const glowGeo = new THREE.SphereGeometry(8, 32, 32);
  const glowMat = new THREE.MeshBasicMaterial({
    color: 0x2E8B98,
    transparent: true,
    opacity: 0.04
  });
  const glow = new THREE.Mesh(glowGeo, glowMat);
  scene.add(glow);

  // ---- MOUSE TRACKING ----
  const mouse = { x: 9999, y: 9999 };
  const mouse3D = new THREE.Vector3(9999, 9999, 0);

  heroSection.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    mouse3D.set(mouse.x * SPREAD * 1.2, mouse.y * SPREAD * 0.5, 0);
  });

  heroSection.addEventListener('mouseleave', () => {
    mouse3D.set(9999, 9999, 0);
  });

  // ---- RESIZE ----
  function resize() {
    const rect = heroSection.getBoundingClientRect();
    renderer.setSize(rect.width, rect.height, false);
    camera.aspect = rect.width / rect.height;
    camera.updateProjectionMatrix();
  }
  resize();
  window.addEventListener('resize', resize);

  // ---- ANIMATION LOOP ----
  let time = 0;
  let rafId;
  const posAttr = geometry.getAttribute('position');

  function animate() {
    rafId = requestAnimationFrame(animate);
    time += FLOW_SPEED;

    for (let i = 0; i < PARTICLE_COUNT; i++) {
      const i3 = i * 3;

      // Organic flow motion
      const flowX = Math.sin(time * 30 + origPositions[i3 + 1] * 0.1) * 0.03;
      const flowY = Math.cos(time * 25 + origPositions[i3] * 0.08) * 0.02;

      // Mouse repulsion
      const dx = positions[i3] - mouse3D.x;
      const dy = positions[i3 + 1] - mouse3D.y;
      const dist = Math.sqrt(dx * dx + dy * dy);

      if (dist < MOUSE_RADIUS && dist > 0.01) {
        const force = (MOUSE_RADIUS - dist) / MOUSE_RADIUS * MOUSE_FORCE;
        velocities[i3] += (dx / dist) * force;
        velocities[i3 + 1] += (dy / dist) * force;
      }

      // Return to origin
      velocities[i3] += (origPositions[i3] - positions[i3]) * RETURN_SPEED;
      velocities[i3 + 1] += (origPositions[i3 + 1] - positions[i3 + 1]) * RETURN_SPEED;
      velocities[i3 + 2] += (origPositions[i3 + 2] - positions[i3 + 2]) * RETURN_SPEED;

      // Damping
      velocities[i3] *= 0.92;
      velocities[i3 + 1] *= 0.92;
      velocities[i3 + 2] *= 0.92;

      // Apply
      positions[i3] += velocities[i3] + flowX;
      positions[i3 + 1] += velocities[i3 + 1] + flowY;
      positions[i3 + 2] += velocities[i3 + 2];
    }

    posAttr.needsUpdate = true;

    // Slow rotation
    particles.rotation.y = Math.sin(time * 8) * 0.08;
    particles.rotation.x = Math.cos(time * 5) * 0.03;

    // Glow pulse
    glow.material.opacity = 0.03 + Math.sin(time * 40) * 0.015;
    glow.scale.setScalar(1 + Math.sin(time * 20) * 0.1);

    renderer.render(scene, camera);
  }

  // ---- VISIBILITY OPTIMIZATION ----
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        if (!rafId) animate();
      } else {
        if (rafId) {
          cancelAnimationFrame(rafId);
          rafId = null;
        }
      }
    });
  }, { threshold: 0.1 });

  observer.observe(heroSection);

  // Start animation
  animate();
})();
