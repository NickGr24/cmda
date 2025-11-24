document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (mobileMenuToggle && navMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            this.classList.toggle('active');
            navMenu.classList.toggle('active');
            
            // Prevent body scroll when menu is active
            document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
        });
        
        document.addEventListener('click', function(e) {
            if (!mobileMenuToggle.contains(e.target) && !navMenu.contains(e.target)) {
                mobileMenuToggle.classList.remove('active');
                navMenu.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }
    
    const navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                mobileMenuToggle.classList.remove('active');
                navMenu.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });
    
    const currentPath = window.location.pathname;
    navLinks.forEach(link => {
        const linkPath = new URL(link.href).pathname;
        if (linkPath === currentPath || 
            (currentPath === '/' && linkPath.endsWith('index.html')) ||
            (currentPath.endsWith('index.html') && linkPath === '/')) {
            link.classList.add('active');
        }
    });
    
    const contactForm = document.getElementById('contact-form');
    const formMessage = document.getElementById('form-message');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = value;
            });
            
            const nameField = this.querySelector('#name');
            const emailField = this.querySelector('#email');
            const messageField = this.querySelector('#message');
            
            let isValid = true;
            const errors = [];
            
            if (!nameField.value.trim()) {
                errors.push('Numele este obligatoriu');
                nameField.classList.add('error');
                isValid = false;
            } else {
                nameField.classList.remove('error');
            }
            
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailField.value.trim() || !emailRegex.test(emailField.value)) {
                errors.push('Email-ul este invalid');
                emailField.classList.add('error');
                isValid = false;
            } else {
                emailField.classList.remove('error');
            }
            
            if (!messageField.value.trim() || messageField.value.trim().length < 10) {
                errors.push('Mesajul trebuie să aibă cel puțin 10 caractere');
                messageField.classList.add('error');
                isValid = false;
            } else {
                messageField.classList.remove('error');
            }
            
            if (isValid) {
                console.log('Date formular:', data);
                
                this.style.display = 'none';
                formMessage.style.display = 'block';
                
                setTimeout(() => {
                    this.reset();
                    this.style.display = 'block';
                    formMessage.style.display = 'none';
                }, 5000);
            } else {
                alert('Te rugăm să completezi toate câmpurile obligatorii:\n\n' + errors.join('\n'));
            }
        });
    }
    
    const header = document.querySelector('.site-header');
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            header.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
        } else {
            header.style.boxShadow = '0 1px 2px 0 rgb(0 0 0 / 0.05)';
        }
        
        lastScroll = currentScroll;
    });
    
    const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
    smoothScrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href !== '#0') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    const headerHeight = header.offsetHeight;
                    const targetPosition = target.offsetTop - headerHeight - 20;
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
    
    document.querySelectorAll('input, textarea').forEach(field => {
        field.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        field.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
            if (this.value) {
                this.parentElement.classList.add('filled');
            } else {
                this.parentElement.classList.remove('filled');
            }
        });
    });
});

console.log('%cCMDA - Centrul Municipal pentru Dezvoltarea Antreprenoriatului', 'color: #1e40af; font-size: 16px; font-weight: bold;');
console.log('%cWebsite dezvoltat pentru susținerea antreprenorilor din Chișinău', 'color: #6b7280; font-size: 14px;');

// Counting animation for numbers
function animateCounter(element) {
    const target = parseFloat(element.getAttribute('data-count'));
    const hasDecimal = element.hasAttribute('data-decimal');
    const decimalPlaces = hasDecimal ? parseInt(element.getAttribute('data-decimal')) : 0;
    const duration = 2000; // 2 seconds
    const start = 0;
    const increment = target / (duration / 16);
    let current = 0;
    
    const formatNumber = (num) => {
        // Handle decimal numbers
        if (decimalPlaces > 0) {
            return num.toFixed(decimalPlaces).replace('.', ',');
        }
        // Format large numbers with space as thousand separator
        if (num >= 1000) {
            return Math.floor(num).toLocaleString('ro-RO').replace(/,/g, ' ');
        }
        return Math.floor(num).toString();
    };
    
    const updateCounter = () => {
        current += increment;
        if (current < target) {
            element.textContent = formatNumber(current);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = formatNumber(target);
        }
    };
    
    updateCounter();
}

// Initialize counter animations when elements come into view
document.addEventListener('DOMContentLoaded', function() {
    const counters = document.querySelectorAll('[data-count]');
    
    if (counters.length > 0) {
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1
        };
        
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                    entry.target.classList.add('counted');
                    animateCounter(entry.target);
                }
            });
        }, observerOptions);
        
        counters.forEach(counter => {
            counterObserver.observe(counter);
        });
    }
});