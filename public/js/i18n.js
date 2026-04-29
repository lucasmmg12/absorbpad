// 1. Define translation logic immediately in global scope
(function () {
    console.log('[AbsorbPad] i18n script initializing...');

    // --- SAFEGUARDS ---
    // Safe LocalStorage wrapper
    function safeGetStorage(key, defaultValue) {
        try {
            return localStorage.getItem(key) || defaultValue;
        } catch (e) {
            console.warn('[AbsorbPad] localStorage access denied or failed:', e);
            return defaultValue;
        }
    }

    function safeSetStorage(key, value) {
        try {
            localStorage.setItem(key, value);
        } catch (e) {
            console.warn('[AbsorbPad] localStorage write failed:', e);
        }
    }

    // Default language is Spanish
    let currentLang = safeGetStorage('absorbpad_lang', 'es');
    console.log('[AbsorbPad] Initial language set to:', currentLang);

    // Helper to get nested value
    function getNestedTranslation(lang, key) {
        // USE WINDOW.TRANSLATIONS EXPLICITLY
        if (typeof window.translations === 'undefined') {
            console.error('[AbsorbPad] window.translations is undefined! Ensure translations.js loaded.');
            return null;
        }
        const keys = key.split('.');
        let value = window.translations[lang];
        for (const k of keys) {
            if (value && value[k]) {
                value = value[k];
            } else {
                return null;
            }
        }
        return value;
    }

    // Main update function
    function updateContent(lang) {
        console.log(`[AbsorbPad] Attempting update to: ${lang}`);

        if (typeof window.translations === 'undefined') {
            console.error('[AbsorbPad] CRITICAL: window.translations missing.');
            return;
        }

        if (!window.translations[lang]) {
            console.warn(`[AbsorbPad] Language ${lang} not supported.`);
            return;
        }

        currentLang = lang;
        safeSetStorage('absorbpad_lang', lang);

        // Update all elements with data-i18n attribute
        const elements = document.querySelectorAll('[data-i18n]');
        let updatedCount = 0;

        elements.forEach(element => {
            const key = element.getAttribute('data-i18n');
            const value = getNestedTranslation(lang, key);

            if (value) {
                if (value.includes('<')) {
                    element.innerHTML = value;
                } else {
                    element.innerText = value;
                }
                updatedCount++;
            } else {
                console.warn(`[AbsorbPad] Missing key: ${key} (${lang})`);
            }
        });
        console.log(`[AbsorbPad] Updated ${updatedCount} elements.`);

        // Update active state of language buttons
        const buttons = document.querySelectorAll('.lang-btn');
        buttons.forEach(btn => {
            const btnLang = btn.getAttribute('data-lang');
            if (btnLang === lang) {
                btn.classList.add('active');
                btn.style.fontWeight = 'bold';
                btn.style.opacity = '1';
                btn.style.borderBottom = '1px solid currentColor';
            } else {
                btn.classList.remove('active');
                btn.style.fontWeight = 'normal';
                btn.style.opacity = '0.7';
                btn.style.borderBottom = 'none';
            }
        });

        document.documentElement.lang = lang;
        console.log(`[AbsorbPad] Language success: ${lang}`);
    }

    // Expose function globally immediately
    window.setLanguage = updateContent;

    // EVENT DELEGATION
    document.addEventListener('click', function (event) {
        let target = event.target;
        while (target && target !== document) {
            if (target.matches && target.matches('.lang-btn')) {
                const lang = target.getAttribute('data-lang');
                console.log('[AbsorbPad] Clicked lang:', lang);
                event.preventDefault();
                event.stopPropagation(); // Stop bubbling just in case
                if (lang) {
                    updateContent(lang);
                }
                return;
            }
            target = target.parentNode;
        }
    });

    // Initialize content when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            updateContent(currentLang);
        });
    } else {
        updateContent(currentLang);
    }

    // VISUAL CONFIRMATION FOR DEBUGGING (Temporary)
    // console.log('[AbsorbPad] Script fully loaded');
})();
