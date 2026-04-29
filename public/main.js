/* MENU SHOW Y HIDDEN */
const navMenu = document.getElementById('nav-menu'),
    navToggle = document.getElementById('nav-toggle'),
    navClose = document.getElementById('nav-close')

/* MENU SHOW */
if (navToggle) {
    navToggle.addEventListener('click', () => {
        navMenu.classList.add('show-menu')
    })
}

/* MENU HIDDEN */
if (navClose) {
    navClose.addEventListener('click', () => {
        navMenu.classList.remove('show-menu')
    })
}

/* REMOVE MENU MOBILE */
const navLink = document.querySelectorAll('.nav-link')

function linkAction() {
    const navMenu = document.getElementById('nav-menu')
    // When we click on each nav__link, we remove the show-menu class
    navMenu.classList.remove('show-menu')
}
navLink.forEach(n => n.addEventListener('click', linkAction))

/* CHANGE BACKGROUND HEADER */
function scrollHeader() {
    const header = document.getElementById('header')
    // When the scroll is greater than 50 viewport height, add the scroll-header class to the header tag
    if (this.scrollY >= 50) {
        document.querySelector('.header').classList.add('scroll-header');
    } else {
        document.querySelector('.header').classList.remove('scroll-header');
    }
}
window.addEventListener('scroll', scrollHeader)

/* SCROLL SECTIONS ACTIVE LINK */
const sections = document.querySelectorAll('section[id]')

function scrollActive() {
    const scrollY = window.pageYOffset

    sections.forEach(current => {
        const sectionHeight = current.offsetHeight,
            sectionTop = current.offsetTop - 58,
            sectionId = current.getAttribute('id')

        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            document.querySelector('.nav-menu a[href*=' + sectionId + ']').classList.add('active')
        } else {
            document.querySelector('.nav-menu a[href*=' + sectionId + ']').classList.remove('active')
        }
    })
}
window.addEventListener('scroll', scrollActive)

/* DYNAMIC AOS ASSIGNMENT & INIT */
document.querySelectorAll('.section-header, .service-card, .glassmorphism-card, .about-card, .client-item, .metric-item, .hero-title, .hero-description').forEach((el, index) => {
    if (!el.hasAttribute('data-aos')) {
        el.setAttribute('data-aos', 'fade-up');
        // Add staggered delays for grids
        if (el.classList.contains('service-card') || el.classList.contains('glassmorphism-card') || el.classList.contains('client-item')) {
            el.setAttribute('data-aos-delay', (index % 3) * 100);
        }
    }
});

// Initialize AOS
if (typeof AOS !== 'undefined') {
    AOS.init({
        duration: 800,
        once: true,
        offset: 50
    });
}

/* ASSISTANT MODAL LOGIC */
function openAssistant() {
    document.getElementById('assistantModal').classList.add('active');
    document.getElementById('step1').style.display = 'block';
    document.getElementById('step2').style.display = 'none';
}

function closeAssistant() {
    document.getElementById('assistantModal').classList.remove('active');
}

function showResult(type) {
    document.getElementById('step1').style.display = 'none';
    document.getElementById('step2').style.display = 'block';
    
    const title = document.getElementById('resultTitle');
    const text = document.getElementById('resultText');
    
    if (type === 'hidrocarburos') {
        title.innerHTML = '<ion-icon name="water-outline"></ion-icon> Línea Blanca (Hidrofóbica)';
        text.innerText = 'Recomendamos Paños ABP y Barreras Blancas. Absorben aceites e hidrocarburos repeliendo el agua. Ideal para derrames en suelo o agua.';
    } else if (type === 'quimicos') {
        title.innerHTML = '<ion-icon name="warning-outline"></ion-icon> Línea Química (Amarilla)';
        text.innerText = 'Recomendamos Paños Químicos Amarillos y Cordones. Tratados para soportar ácidos, bases y fluidos agresivos sin degradarse.';
    } else if (type === 'universales') {
        title.innerHTML = '<ion-icon name="layers-outline"></ion-icon> Línea Universal (Gris/Mineral)';
        text.innerText = 'Recomendamos Mantas ABM, Absorbente Mineral o Paños Grises. Solución versátil para refrigerantes, agua y uso general.';
    }
}

function resetAssistant() {
    document.getElementById('step1').style.display = 'block';
    document.getElementById('step2').style.display = 'none';
}

/* TABS LOGIC */
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));
        
        btn.classList.add('active');
        const target = document.getElementById(btn.dataset.target);
        if (target) target.classList.add('active');
    });
});
