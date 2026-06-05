/* ============================================================
   Ruijian Petroleum — Main JavaScript
   Features: Navigation, Language Switcher, GeoIP, 
   Animations, Cookie Consent, Back to Top
   ============================================================ */

(function() {
  'use strict';

  // --- Configuration ---
  const CONFIG = {
    cookieConsentDuration: 365, // days
    langCookieName: 'ruijian_lang',
    cookieConsentName: 'ruijian_cookie_consent',
    scrollThreshold: 100,
    animationThreshold: 0.1,
  };

  // --- Language Configuration ---
  const LANGUAGES = {
    zh: { name: '中文', native: '中文', dir: 'ltr', flag: '🇨🇳' },
    en: { name: 'English', native: 'English', dir: 'ltr', flag: '🇬🇧' },
    ar: { name: 'العربية', native: 'العربية', dir: 'rtl', flag: '🇸🇦' },
    ru: { name: 'Русский', native: 'Русский', dir: 'ltr', flag: '🇷🇺' },
    es: { name: 'Español', native: 'Español', dir: 'ltr', flag: '🇪🇸' },
    fr: { name: 'Français', native: 'Français', dir: 'ltr', flag: '🇫🇷' },
  };

  // GeoIP language mapping (country code -> language)
  const GEO_MAP = {
    CN: 'zh', TW: 'zh', HK: 'zh', MO: 'zh',
    US: 'en', GB: 'en', CA: 'en', AU: 'en', IN: 'en', 
    SG: 'en', MY: 'en', PH: 'en', TH: 'en', VN: 'en',
    SA: 'ar', AE: 'ar', IQ: 'ar', KW: 'ar', QA: 'ar', 
    OM: 'ar', EG: 'ar', BH: 'ar', JO: 'ar', LY: 'ar',
    RU: 'ru', KZ: 'ru', UZ: 'ru', BY: 'ru', UA: 'ru',
    MX: 'es', VE: 'es', CO: 'es', AR: 'es', BR: 'es', 
    CL: 'es', PE: 'es', EC: 'es',
    FR: 'fr', DZ: 'fr', MA: 'fr', TN: 'fr', CI: 'fr', 
    SN: 'fr', CM: 'fr', BE: 'fr', CH: 'fr',
  };

  // --- State ---
  let currentLang = 'zh';
  let isMobileMenuOpen = false;

  // --- Utility Functions ---
  function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : null;
  }

  function setCookie(name, value, days) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = name + '=' + encodeURIComponent(value) + '; expires=' + expires + '; path=/; SameSite=Lax';
  }

  function getCurrentLang() {
    // Priority: URL path > Cookie > Browser > Default
    const pathMatch = window.location.pathname.match(/^\/(zh|en|ar|ru|es|fr)\//);
    if (pathMatch) return pathMatch[1];

    const cookieLang = getCookie(CONFIG.langCookieName);
    if (cookieLang && LANGUAGES[cookieLang]) return cookieLang;

    return 'zh';
  }

  function getBrowserLang() {
    try {
      const lang = navigator.language || navigator.userLanguage;
      if (!lang) return null;
      const code = lang.split('-')[0].toLowerCase();
      if (LANGUAGES[code]) return code;
      // Map partial matches
      if (code.startsWith('zh')) return 'zh';
    } catch (e) {}
    return null;
  }

  async function detectGeoIP() {
    try {
      // Try multiple free GeoIP services
      const services = [
        'https://ipapi.co/json/',
        'https://ip-api.com/json/',
        'https://api.ipify.org?format=json'
      ];
      
      const response = await fetch(services[0], { signal: AbortSignal.timeout(3000) });
      if (!response.ok) throw new Error('GeoIP failed');
      const data = await response.json();
      const countryCode = data.country_code || data.countryCode;
      if (countryCode && GEO_MAP[countryCode]) {
        return GEO_MAP[countryCode];
      }
    } catch (e) {
      // Fallback to browser language
      return getBrowserLang();
    }
    return null;
  }

  function redirectToLanguage(lang) {
    if (!LANGUAGES[lang]) lang = 'zh';
    setCookie(CONFIG.langCookieName, lang, CONFIG.cookieConsentDuration);
    
    const currentPath = window.location.pathname;
    // If already on a language path, replace it
    const newPath = currentPath.replace(/^\/(zh|en|ar|ru|es|fr)(\/|$)/, '/' + lang + '/');
    
    if (newPath !== currentPath) {
      window.location.href = newPath;
    }
  }

  // --- DOM Ready ---
  document.addEventListener('DOMContentLoaded', function() {
    // Detect current language
    currentLang = getCurrentLang();
    
    // Set lang and dir on html
    document.documentElement.lang = currentLang;
    document.documentElement.dir = LANGUAGES[currentLang]?.dir || 'ltr';
    document.body.classList.add('lang-' + currentLang);
    
    // If no language in URL, detect and redirect
    const pathHasLang = window.location.pathname.match(/^\/(zh|en|ar|ru|es|fr)\//);
    if (!pathHasLang && window.location.pathname !== '/') {
      // On the root index, try GeoIP
      detectGeoIP().then(detectedLang => {
        if (detectedLang && detectedLang !== 'zh') {
          redirectToLanguage(detectedLang);
        }
      });
    }

    initNavigation();
    initLanguageSwitcher();
    initScrollEffects();
    initAnimations();
    initCookieConsent();
    initBackToTop();
    initContactForm();
  });

  // --- Navigation ---
  function initNavigation() {
    const menuToggle = document.querySelector('.menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    
    if (menuToggle && mainNav) {
      menuToggle.addEventListener('click', function() {
        isMobileMenuOpen = !isMobileMenuOpen;
        mainNav.classList.toggle('mobile-open', isMobileMenuOpen);
        document.body.style.overflow = isMobileMenuOpen ? 'hidden' : '';
      });

      // Close menu on link click
      mainNav.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', function() {
          mainNav.classList.remove('mobile-open');
          isMobileMenuOpen = false;
          document.body.style.overflow = '';
        });
      });
    }

    // Highlight active nav item
    const currentPath = window.location.pathname;
    document.querySelectorAll('.main-nav a').forEach(link => {
      const href = link.getAttribute('href');
      if (href && currentPath.includes(href) && href !== '#') {
        link.classList.add('active');
      }
    });
  }

  // --- Language Switcher ---
  function initLanguageSwitcher() {
    // Update current language display
    const langBtn = document.querySelector('.lang-switcher-btn');
    if (langBtn) {
      const langInfo = LANGUAGES[currentLang];
      if (langInfo) {
        const nameSpan = langBtn.querySelector('.lang-name');
        if (nameSpan) nameSpan.textContent = langInfo.name;
      }
    }

    // Handle language clicks
    document.querySelectorAll('.lang-dropdown a').forEach(link => {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        const lang = this.dataset.lang;
        if (lang && lang !== currentLang) {
          redirectToLanguage(lang);
        }
      });
    });
  }

  // --- Scroll Effects ---
  function initScrollEffects() {
    const header = document.querySelector('.site-header');
    const backToTop = document.querySelector('.back-to-top');
    
    let ticking = false;
    window.addEventListener('scroll', function() {
      if (!ticking) {
        window.requestAnimationFrame(function() {
          const scrollY = window.scrollY || window.pageYOffset;
          
          if (header) {
            header.classList.toggle('scrolled', scrollY > 50);
          }
          
          if (backToTop) {
            backToTop.classList.toggle('visible', scrollY > 400);
          }
          
          ticking = false;
        });
        ticking = true;
      }
    });
  }

  // --- Scroll Animations ---
  function initAnimations() {
    const elements = document.querySelectorAll('.fade-in');
    
    if (!elements.length) return;
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: CONFIG.animationThreshold,
      rootMargin: '0px 0px -50px 0px'
    });

    elements.forEach(el => observer.observe(el));
  }

  // --- Cookie Consent ---
  function initCookieConsent() {
    const consent = document.querySelector('.cookie-consent');
    if (!consent) return;
    
    const saved = getCookie(CONFIG.cookieConsentName);
    if (saved === 'accepted') return;
    
    // Show after a short delay
    setTimeout(() => {
      consent.classList.add('show');
    }, 1000);

    const acceptBtn = consent.querySelector('.btn-primary');
    const declineBtn = consent.querySelector('.btn-outline');
    
    if (acceptBtn) {
      acceptBtn.addEventListener('click', function() {
        setCookie(CONFIG.cookieConsentName, 'accepted', CONFIG.cookieConsentDuration);
        consent.classList.remove('show');
        // Load GA or other tracking here
        loadAnalytics();
      });
    }
    
    if (declineBtn) {
      declineBtn.addEventListener('click', function() {
        setCookie(CONFIG.cookieConsentName, 'declined', CONFIG.cookieConsentDuration);
        consent.classList.remove('show');
      });
    }
  }

  // --- Google Analytics ---
  function loadAnalytics() {
    // GA4 placeholder - uncomment and add your measurement ID
    // const script = document.createElement('script');
    // script.src = 'https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX';
    // script.async = true;
    // document.head.appendChild(script);
    // 
    // window.dataLayer = window.dataLayer || [];
    // function gtag(){dataLayer.push(arguments);}
    // gtag('js', new Date());
    // gtag('config', 'G-XXXXXXXXXX', { anonymize_ip: true });
  }

  // --- Back to Top ---
  function initBackToTop() {
    const btn = document.querySelector('.back-to-top');
    if (!btn) return;
    
    btn.addEventListener('click', function() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // --- Contact Form ---
  function initContactForm() {
    const form = document.querySelector('.contact-form form');
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const submitBtn = form.querySelector('[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = form.dataset.sending || 'Sending...';
      }
      
      // Collect form data
      const formData = new FormData(form);
      
      // Use Formspree or Web3Forms
      const action = form.getAttribute('action');
      if (action && action.includes('formspree')) {
        fetch(action, {
          method: 'POST',
          body: formData,
          headers: { 'Accept': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
          if (data.ok) {
            form.innerHTML = '<div class="form-success" style="text-align:center;padding:40px;">' +
              '<div style="font-size:3rem;margin-bottom:16px;">✅</div>' +
              '<h3>' + (form.dataset.successTitle || 'Thank You!') + '</h3>' +
              '<p>' + (form.dataset.successMsg || 'We will get back to you shortly.') + '</p>' +
              '</div>';
          } else {
            throw new Error('Form submission failed');
          }
        })
        .catch(error => {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = form.dataset.submitText || 'Send Message';
          }
          alert('There was an error. Please try again or email us directly.');
        });
      } else {
        // Fallback: show success message
        form.innerHTML = '<div class="form-success" style="text-align:center;padding:40px;">' +
          '<div style="font-size:3rem;margin-bottom:16px;">✅</div>' +
          '<h3>' + (form.dataset.successTitle || 'Thank You!') + '</h3>' +
          '<p>' + (form.dataset.successMsg || 'We will get back to you shortly.') + '</p>' +
          '</div>';
      }
    });
  }


  // --- Scroll Counter Animation ---
  function initCounters() {
    const counters = document.querySelectorAll('.stat-number');
    if (!counters.length) return;
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const counter = entry.target;
          const text = counter.textContent.trim();
          // Extract number from text like "150<span>K</span>" or "15<span>万吨</span>"
          const numMatch = text.match(/(\d+[\.]?\d*)/);
          if (!numMatch) { observer.unobserve(counter); return; }
          
          const target = parseFloat(numMatch[1]);
          const suffix = text.replace(numMatch[1], '');
          const duration = 2000;
          const start = performance.now();
          
          function update(currentTime) {
            const elapsed = currentTime - start;
            const progress = Math.min(elapsed / duration, 1);
            // Ease out cubic
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = Math.round(target * eased);
            counter.innerHTML = current + '<span class="suffix">' + suffix + '</span>';
            if (progress < 1) {
              requestAnimationFrame(update);
            } else {
              counter.innerHTML = numMatch[1] + '<span class="suffix">' + suffix + '</span>';
            }
          }
          requestAnimationFrame(update);
          observer.unobserve(counter);
        }
      });
    }, { threshold: 0.5 });
    
    counters.forEach(c => observer.observe(c));
  }
  
  initCounters();
  highlightCurrentLang();

  // --- Fix Language Switcher Links ---
  // Auto-update language switcher hrefs to point to current page in other languages
  document.querySelectorAll('.lang-dropdown a[data-lang]').forEach(function(link) {
    var lang = link.getAttribute('data-lang');
    var currentPath = window.location.pathname;
    // Replace language prefix in path
    var newPath = currentPath.replace(/^\/[a-z]{2}(?:\/|$)/, '/' + lang + '/');
    if (newPath !== currentPath) {
      link.setAttribute('href', newPath);
    }
  });



  // --- Certification Carousel: Infinite Auto-Scroll ---
  function initCarousel() {
    const track = document.getElementById('certCarouselTrack');
    const dots = document.getElementById('certCarouselDots');
    if (!track) return;
    
    // Clone items for seamless loop
    const items = track.querySelectorAll('.cert-carousel-item');
    items.forEach(function(item) {
      var clone = item.cloneNode(true);
      track.appendChild(clone);
    });
    
    // Second clone set for truly infinite feel
    items.forEach(function(item) {
      var clone2 = item.cloneNode(true);
      track.appendChild(clone2);
    });
    
    var totalItems = track.querySelectorAll('.cert-carousel-item').length;
    var itemWidth = 220; // min-width + gap
    var gap = 30;
    var step = itemWidth + gap;
    var scrollSpeed = 0.8; // pixels per frame
    var pos = 0;
    var animId = null;
    var isPaused = false;
    
    function animate() {
      if (!isPaused) {
        pos -= scrollSpeed;
        // When scrolled past the first set, reset to middle
        if (pos < -(items.length * step)) {
          pos = 0;
        }
        track.style.transform = 'translateX(' + pos + 'px)';
      }
      animId = requestAnimationFrame(animate);
    }
    
    // Start animation
    animId = requestAnimationFrame(animate);
    
    // Pause on hover/touch
    var container = track.parentElement;
    container.addEventListener('mouseenter', function() { isPaused = true; });
    container.addEventListener('mouseleave', function() { isPaused = false; });
    container.addEventListener('touchstart', function() { isPaused = true; });
    container.addEventListener('touchend', function() { isPaused = false; });
    
    // Arrow navigation (temporary skip)
    window.moveCarousel = function(dir) {
      isPaused = true;
      pos -= dir * step * 2;
      setTimeout(function() { isPaused = false; }, 3000);
    };
    
    // Create dots (for reference only)
    if (dots) {
      var origCount = items.length;
      for (var i = 0; i < origCount; i++) {
        var dot = document.createElement('button');
        dot.className = 'cert-carousel-dot' + (i === 0 ? ' active' : '');
        (function(idx) {
          dot.onclick = function() {
            isPaused = true;
            var targetPos = -(idx * step);
            // Smooth jump
            var startPos = pos;
            var duration = 300;
            var startTime = performance.now();
            function ease(t) { return 1 - Math.pow(1 - t, 3); }
            function jumpAnim(now) {
              var elapsed = now - startTime;
              var progress = Math.min(elapsed / duration, 1);
              pos = startPos + (targetPos - startPos) * ease(progress);
              track.style.transform = 'translateX(' + pos + 'px)';
              if (progress < 1) requestAnimationFrame(jumpAnim);
              else setTimeout(function() { isPaused = false; }, 2000);
            }
            requestAnimationFrame(jumpAnim);
            
            dots.querySelectorAll('.cert-carousel-dot').forEach(function(d, di) {
              d.classList.toggle('active', di === idx);
            });
          };
        })(i);
        dots.appendChild(dot);
      }
    }
  }
  
  // Initialize on load
  if (document.getElementById('certCarousel')) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initCarousel);
    } else {
      initCarousel();
    }
  }


  // --- Language Switcher: Highlight current language ---
  function highlightCurrentLang() {
    var currentLang = document.documentElement.lang || 'zh';
    document.querySelectorAll('.lang-dropdown a[data-lang]').forEach(function(item) {
      var lang = item.getAttribute('data-lang');
      if (lang === currentLang) {
        item.classList.add('is-current');
        item.setAttribute('aria-current', 'true');
      } else {
        item.classList.remove('is-current');
        item.removeAttribute('aria-current');
      }
    });
  }
  highlightCurrentLang();

})();
