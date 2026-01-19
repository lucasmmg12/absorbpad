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

/* REVEAL ON SCROLL (Simple Implementation) */
const observerOptions = {
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-up');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.animate-card').forEach(card => {
    observer.observe(card);
});

/* CHATBOT LOGIC */
const chatbotToggle = document.getElementById('chatbot-toggle');
const chatWindow = document.getElementById('chat-window');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const typingIndicator = document.getElementById('typing-indicator');

chatbotToggle.addEventListener('click', () => {
    chatWindow.classList.toggle('show');
    document.querySelector('.notification-badge').style.display = 'none';
});

const responses = {
    'Minería': "Entendido. Para el sector minero en San Juan, nos especializamos en soporte para operaciones de altura. Ofrecemos mantenimiento de plantas y protocolos de seguridad EHS específicos para yacimientos como Veladero.\n\n¿Desea que un consultor técnico dimensione su proyecto?",
    'Petróleo': "Excelente. En Petróleo & Gas, Absorb Pad gestiona logística crítica y mantenimiento de infraestructuras. Cumplimos con normativas internacionales de integridad para optimizar la cadena de valor.\n\n¿Necesita un presupuesto para servicios de campo?",
    'Salud': "La salud ocupacional es vital. Diseñamos puestos sanitarios modulares y servicios de soporte médico para campamentos industriales remotos con los más altos estándares provinciales.\n\n¿Le gustaría ver nuestro dossier de capacidades en salud?"
};

function addMessage(text, isBot = false) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(isBot ? 'bot-message' : 'user-message');
    messageDiv.innerText = text;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function handleOption(option) {
    addMessage(option, false);

    typingIndicator.style.display = 'block';

    setTimeout(() => {
        typingIndicator.style.display = 'none';
        addMessage(responses[option], true);

        // Add Lead Gen Form simulation after response
        setTimeout(() => {
            addMessage("Para enviarle más información técnica, por favor indíquenos su nombre y empresa.", true);
        }, 1000);
    }, 1500);
}

sendBtn.addEventListener('click', () => {
    const text = chatInput.value.trim();
    if (text) {
        addMessage(text, false);
        chatInput.value = '';

        typingIndicator.style.display = 'block';

        setTimeout(() => {
            typingIndicator.style.display = 'none';
            addMessage("He recibido su consulta. Analizando factibilidad técnica... En breve un consultor especializado de Absorb Pad se pondrá en contacto con usted.", true);
        }, 2000);
    }
});

chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendBtn.click();
});
