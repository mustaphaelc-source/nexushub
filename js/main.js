/* ============================================
   NEXUSHUB - MAIN JAVASCRIPT
   Interactions, Animations, Language Switching
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {

    // ==================== LOADER ====================
    const loader = document.getElementById('loader');
    window.addEventListener('load', () => {
        setTimeout(() => loader.classList.add('hidden'), 500);
    });

    // ==================== LANGUAGE SYSTEM ====================
    let currentLang = localStorage.getItem('nexushub-lang') || 'en';
    const html = document.documentElement;
    const langSwitch = document.getElementById('langSwitch');
    const langCurrent = langSwitch.querySelector('.lang-current');
    const langAlt = langSwitch.querySelector('.lang-alt');

    function setLanguage(lang) {
        currentLang = lang;
        localStorage.setItem('nexushub-lang', lang);

        // Set direction
        html.lang = lang;
        html.dir = lang === 'ar' ? 'rtl' : 'ltr';

        // Update switcher text
        langCurrent.textContent = lang === 'ar' ? 'عربي' : 'EN';
        langAlt.textContent = lang === 'ar' ? 'EN' : 'عربي';

        // Update all translatable elements
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (translations[lang] && translations[lang][key]) {
                el.textContent = translations[lang][key];
            }
        });

        // Update placeholders
        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.getAttribute('data-i18n-placeholder');
            if (translations[lang] && translations[lang][key]) {
                el.placeholder = translations[lang][key];
            }
        });

        // Update select options
        document.querySelectorAll('select option[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (translations[lang] && translations[lang][key]) {
                el.textContent = translations[lang][key];
            }
        });

        // Re-trigger animations
        animateCounters();
    }

    langSwitch.addEventListener('click', () => {
        setLanguage(currentLang === 'en' ? 'ar' : 'en');
    });

    // Initialize language
    setLanguage(currentLang);

    // ==================== NAVBAR SCROLL ====================
    const navbar = document.getElementById('navbar');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        lastScroll = currentScroll;
    });

    // ==================== MOBILE MENU ====================
    const mobileToggle = document.getElementById('mobileToggle');
    const navLinks = document.getElementById('navLinks');

    mobileToggle.addEventListener('click', () => {
        mobileToggle.classList.toggle('active');
        navLinks.classList.toggle('active');
    });

    // Close mobile menu on link click
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            mobileToggle.classList.remove('active');
            navLinks.classList.remove('active');
        });
    });

    // ==================== SMOOTH SCROLL & ACTIVE LINK ====================
    const sections = document.querySelectorAll('section[id]');
    const navItems = document.querySelectorAll('.nav-link');

    function updateActiveLink() {
        const scrollPos = window.scrollY + 100;

        sections.forEach(section => {
            const top = section.offsetTop;
            const height = section.offsetHeight;
            const id = section.getAttribute('id');

            if (scrollPos >= top && scrollPos < top + height) {
                navItems.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + id) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }

    window.addEventListener('scroll', updateActiveLink);

    // ==================== ANIMATED COUNTERS ====================
    function animateCounters() {
        const counters = document.querySelectorAll('.stat-number');

        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-count'));
            const duration = 2000;
            const increment = target / (duration / 16);
            let current = 0;

            const updateCounter = () => {
                current += increment;
                if (current < target) {
                    counter.textContent = Math.floor(current).toLocaleString();
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.textContent = target.toLocaleString();
                }
            };

            updateCounter();
        });
    }

    // Trigger counters on load
    setTimeout(animateCounters, 1000);

    // ==================== SCROLL REVEAL ====================
    const revealElements = document.querySelectorAll('.feature-card, .blog-card, .product-card, .deal-card, .pricing-card');

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                revealObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    revealElements.forEach((el, index) => {
        el.classList.add('reveal');
        el.style.transitionDelay = `${index * 0.1}s`;
        revealObserver.observe(el);
    });

    // ==================== BACK TO TOP ====================
    const backToTop = document.getElementById('backToTop');

    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 500) {
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
        }
    });

    backToTop.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // ==================== NEWSLETTER FORM ====================
    const newsletterForm = document.getElementById('newsletterForm');

    newsletterForm.addEventListener('submit', function(e) {
        // Formspree handles the actual submission
        // This is for UX feedback
        const btn = this.querySelector('button[type="submit"]');
        const originalText = btn.innerHTML;

        btn.innerHTML = '<span>✓ Subscribed!</span>';
        btn.style.background = 'linear-gradient(135deg, #22c55e, #16a34a)';

        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.style.background = '';
        }, 3000);
    });

    // ==================== AFFILIATE LINK TRACKING ====================
    document.querySelectorAll('a[href*="YOUR_AFF_ID"], a[href*="YOUR_AFFILIATE"]').forEach(link => {
        link.addEventListener('click', function(e) {
            // Replace YOUR_AFF_ID with actual IDs before going live
            if (this.href.includes('YOUR_AFF_ID')) {
                e.preventDefault();
                alert('⚠️ Replace YOUR_AFF_ID with your actual affiliate ID in the HTML before launching!');
            }
        });
    });

    // ==================== ADSENSE WARNING ====================
    if (document.querySelector('ins.adsbygoogle')) {
        const adSlots = document.querySelectorAll('ins.adsbygoogle');
        adSlots.forEach(slot => {
            if (slot.getAttribute('data-ad-client') === 'ca-pub-YOUR_PUBLISHER_ID') {
                // Not live yet - show placeholder styling
                slot.style.minHeight = '90px';
                slot.style.background = 'rgba(255,255,255,0.02)';
                slot.style.border = '1px dashed rgba(255,255,255,0.1)';
                slot.style.display = 'flex';
                slot.style.alignItems = 'center';
                slot.style.justifyContent = 'center';
                slot.style.color = 'var(--text-muted)';
                slot.style.fontSize = '0.8rem';
                slot.innerHTML = '<span>📢 AdSense Placeholder - Replace with your Publisher ID</span>';
            }
        });
    }

    // ==================== PARALLAX ORBS ====================
    const orbs = document.querySelectorAll('.orb');

    document.addEventListener('mousemove', (e) => {
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;

        orbs.forEach((orb, index) => {
            const speed = (index + 1) * 20;
            const xOffset = (0.5 - x) * speed;
            const yOffset = (0.5 - y) * speed;
            orb.style.transform = `translate(${xOffset}px, ${yOffset}px)`;
        });
    });

    // ==================== PRODUCT CARD HOVER EFFECT ====================
    document.querySelectorAll('.product-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.zIndex = '10';
        });
        card.addEventListener('mouseleave', function() {
            this.style.zIndex = '1';
        });
    });

    // ==================== CONSOLE BRANDING ====================
    console.log('%c◈ NexusHub', 'font-size: 24px; font-weight: bold; background: linear-gradient(135deg, #00d4aa, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;');
    console.log('%cBuilt for digital empire builders.', 'font-size: 12px; color: #6b6b7b;');

});
