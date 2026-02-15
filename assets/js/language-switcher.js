// Language Switcher Module
const LanguageSwitcher = (function() {
    let currentLanguage = localStorage.getItem('selectedLanguage') || 'ro';
    let translations = {};
    let isOpen = false;

    const languages = [
        { code: 'ro', label: 'Română' },
        { code: 'en', label: 'English' },
        { code: 'ru', label: 'Русский' }
    ];

    // Load translation files — current language first, others in background
    async function loadTranslations() {
        try {
            const response = await fetch(`assets/js/translations/${currentLanguage}.json`);
            translations[currentLanguage] = await response.json();
            const others = ['ro', 'en', 'ru'].filter(l => l !== currentLanguage);
            Promise.all(others.map(lang =>
                fetch(`assets/js/translations/${lang}.json`)
                    .then(r => r.json())
                    .then(data => { translations[lang] = data; })
            )).catch(err => console.error('Error loading other translations:', err));
        } catch (error) {
            console.error('Error loading translations:', error);
        }
    }

    // Update page content with translations
    function updatePageContent(lang) {
        const translation = translations[lang];
        if (!translation) return;

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

        if (document.querySelector('title')) {
            const pageTitle = document.querySelector('title').getAttribute('data-title-key');
            if (pageTitle && translation[pageTitle]) {
                document.title = translation[pageTitle];
            }
        }

        document.documentElement.lang = lang === 'ru' ? 'ru' : lang === 'en' ? 'en' : 'ro';
    }

    // Initialize language switcher
    function init() {
        loadTranslations().then(() => {
            if (!document.querySelector('.language-switcher')) {
                addLanguageSwitcher();
            }
            updatePageContent(currentLanguage);
        });
    }

    // Build the custom dropdown HTML
    function buildDropdownHTML() {
        const current = languages.find(l => l.code === currentLanguage) || languages[0];

        const optionsHTML = languages.map(lang => `
            <button class="lang-option${lang.code === currentLanguage ? ' lang-option--active' : ''}" data-lang="${lang.code}">
                <span class="lang-option-label">${lang.label}</span>
                <span class="lang-option-code">${lang.code.toUpperCase()}</span>
                ${lang.code === currentLanguage ? '<svg class="lang-option-check" width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2.5 7.5L5.5 10.5L11.5 3.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>' : ''}
            </button>
        `).join('');

        return `
            <button class="lang-trigger" aria-expanded="false" aria-haspopup="listbox">
                <svg class="lang-trigger-globe" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                </svg>
                <span class="lang-trigger-code">${current.code.toUpperCase()}</span>
                <svg class="lang-trigger-chevron" width="10" height="6" viewBox="0 0 10 6" fill="none">
                    <path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </button>
            <div class="lang-dropdown" role="listbox">
                <div class="lang-dropdown-inner">
                    ${optionsHTML}
                </div>
            </div>
        `;
    }

    // Add language switcher to header
    function addLanguageSwitcher() {
        const preHeaderRight = document.querySelector('.pre-header-right');
        if (!preHeaderRight) return;

        const languageSwitcher = document.createElement('div');
        languageSwitcher.className = 'language-switcher';
        languageSwitcher.innerHTML = buildDropdownHTML();

        preHeaderRight.appendChild(languageSwitcher);

        // Trigger button click
        const trigger = languageSwitcher.querySelector('.lang-trigger');
        trigger.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleDropdown(languageSwitcher);
        });

        // Option clicks
        languageSwitcher.querySelectorAll('.lang-option').forEach(option => {
            option.addEventListener('click', (e) => {
                e.stopPropagation();
                const lang = option.dataset.lang;
                switchLanguage(lang);
                closeDropdown(languageSwitcher);
                rebuildOptions(languageSwitcher);
            });
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!languageSwitcher.contains(e.target)) {
                closeDropdown(languageSwitcher);
            }
        });

        // Close on Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                closeDropdown(languageSwitcher);
            }
        });
    }

    function toggleDropdown(switcher) {
        if (isOpen) {
            closeDropdown(switcher);
        } else {
            openDropdown(switcher);
        }
    }

    function openDropdown(switcher) {
        isOpen = true;
        switcher.classList.add('lang-open');
        const trigger = switcher.querySelector('.lang-trigger');
        if (trigger) trigger.setAttribute('aria-expanded', 'true');
    }

    function closeDropdown(switcher) {
        isOpen = false;
        switcher.classList.remove('lang-open');
        const trigger = switcher.querySelector('.lang-trigger');
        if (trigger) trigger.setAttribute('aria-expanded', 'false');
    }

    function rebuildOptions(switcher) {
        const current = languages.find(l => l.code === currentLanguage) || languages[0];

        // Update trigger text
        const triggerCode = switcher.querySelector('.lang-trigger-code');
        if (triggerCode) triggerCode.textContent = current.code.toUpperCase();

        // Update options
        switcher.querySelectorAll('.lang-option').forEach(option => {
            const lang = option.dataset.lang;
            option.classList.toggle('lang-option--active', lang === currentLanguage);

            // Update checkmark
            const existingCheck = option.querySelector('.lang-option-check');
            if (lang === currentLanguage && !existingCheck) {
                option.insertAdjacentHTML('beforeend', '<svg class="lang-option-check" width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2.5 7.5L5.5 10.5L11.5 3.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>');
            } else if (lang !== currentLanguage && existingCheck) {
                existingCheck.remove();
            }
        });

        // Also update mobile language buttons if they exist
        document.querySelectorAll('.mobile-lang-btn').forEach(btn => {
            btn.classList.toggle('mobile-lang-btn--active', btn.dataset.lang === currentLanguage);
        });
    }

    // Switch language
    function switchLanguage(lang) {
        currentLanguage = lang;
        localStorage.setItem('selectedLanguage', lang);
        updatePageContent(lang);

        // Update all switcher instances
        document.querySelectorAll('.language-switcher').forEach(sw => {
            rebuildOptions(sw);
        });
    }

    // Public API
    return {
        init: init,
        switchLanguage: switchLanguage,
        getCurrentLanguage: () => currentLanguage,
        getLanguages: () => languages
    };
})();

// Initialize on DOM content loaded
document.addEventListener('DOMContentLoaded', function() {
    LanguageSwitcher.init();
});
