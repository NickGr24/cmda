// Language Switcher Module
const LanguageSwitcher = (function() {
    let currentLanguage = localStorage.getItem('selectedLanguage') || 'ro';
    let translations = {};

    // Load translation files
    async function loadTranslations() {
        try {
            const languages = ['ro', 'en', 'ru'];
            for (const lang of languages) {
                const response = await fetch(`assets/js/translations/${lang}.json`);
                translations[lang] = await response.json();
            }
        } catch (error) {
            console.error('Error loading translations:', error);
        }
    }

    // Update page content with translations
    function updatePageContent(lang) {
        const translation = translations[lang];
        if (!translation) return;

        // Update navigation
        document.querySelectorAll('[data-translate]').forEach(element => {
            const keys = element.getAttribute('data-translate').split('.');
            let value = translation;
            
            for (const key of keys) {
                value = value[key];
                if (!value) break;
            }
            
            if (value) {
                if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                    element.placeholder = value;
                } else {
                    element.textContent = value;
                }
            }
        });

        // Update document title
        if (document.querySelector('title')) {
            const pageTitle = document.querySelector('title').getAttribute('data-title-key');
            if (pageTitle && translation[pageTitle]) {
                document.title = translation[pageTitle];
            }
        }

        // Update HTML lang attribute
        document.documentElement.lang = lang === 'ru' ? 'ru' : lang === 'en' ? 'en' : 'ro';
    }

    // Initialize language switcher
    function init() {
        // Load translations on page load
        loadTranslations().then(() => {
            // Add language switcher to header if not exists
            if (!document.querySelector('.language-switcher')) {
                addLanguageSwitcher();
            }
            
            // Apply saved language
            updatePageContent(currentLanguage);
            updateLanguageSelector();
        });
    }

    // Add language switcher to header
    function addLanguageSwitcher() {
        const navMenu = document.querySelector('.nav-menu');
        if (!navMenu) return;

        const languageSwitcher = document.createElement('div');
        languageSwitcher.className = 'language-switcher';
        languageSwitcher.innerHTML = `
            <select class="lang-selector" id="languageSelector">
                <option value="ro">Română</option>
                <option value="en">English</option>
                <option value="ru">Русский</option>
            </select>
        `;

        navMenu.appendChild(languageSwitcher);

        // Add event listener for selector
        const selector = languageSwitcher.querySelector('#languageSelector');
        selector.addEventListener('change', (e) => {
            switchLanguage(e.target.value);
        });

        // Set initial value
        selector.value = currentLanguage;
    }

    // Switch language
    function switchLanguage(lang) {
        currentLanguage = lang;
        localStorage.setItem('selectedLanguage', lang);
        updatePageContent(lang);
        updateLanguageSelector();
    }

    // Update language selector
    function updateLanguageSelector() {
        const selector = document.querySelector('#languageSelector');
        if (selector) {
            selector.value = currentLanguage;
        }
    }

    // Public API
    return {
        init: init,
        switchLanguage: switchLanguage,
        getCurrentLanguage: () => currentLanguage
    };
})();

// Initialize on DOM content loaded
document.addEventListener('DOMContentLoaded', function() {
    LanguageSwitcher.init();
});