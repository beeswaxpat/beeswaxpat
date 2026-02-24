/* ============================================
   BEESWAX PAT — main.js
   Mobile menu · FAQ accordion · Sticky nav
   Email popup · Fade-in animations
   ============================================ */

(function () {
  'use strict';

  /* === STICKY NAV === */
  const nav = document.querySelector('.nav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.classList.toggle('scrolled', window.scrollY > 20);
    }, { passive: true });
  }

  /* === MOBILE MENU === */
  const hamburger = document.querySelector('.nav-hamburger');
  const mobileMenu = document.querySelector('.mobile-menu');
  const menuClose = document.querySelector('.mobile-menu-close');
  const mobileLinks = document.querySelectorAll('.mobile-menu a');

  function openMenu() {
    mobileMenu.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeMenu() {
    mobileMenu.classList.remove('open');
    document.body.style.overflow = '';
  }

  if (hamburger) hamburger.addEventListener('click', openMenu);
  if (menuClose) menuClose.addEventListener('click', closeMenu);
  mobileLinks.forEach(link => link.addEventListener('click', closeMenu));

  /* === FAQ ACCORDION === */
  const faqItems = document.querySelectorAll('.faq-item');

  faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    const answer = item.querySelector('.faq-answer');

    question.addEventListener('click', () => {
      const isOpen = item.classList.contains('open');

      // Close all others
      faqItems.forEach(other => {
        if (other !== item) {
          other.classList.remove('open');
          other.querySelector('.faq-answer').style.maxHeight = '0';
        }
      });

      // Toggle current
      if (isOpen) {
        item.classList.remove('open');
        answer.style.maxHeight = '0';
      } else {
        item.classList.add('open');
        answer.style.maxHeight = answer.scrollHeight + 'px';
      }
    });
  });

  /* === EMAIL POPUP === */
  const popup = document.querySelector('.popup-overlay');
  const popupClose = document.querySelector('.popup-close');
  const POPUP_KEY = 'beeswaxpat_popup_shown';

  function showPopup() {
    if (!popup) return;
    if (sessionStorage.getItem(POPUP_KEY)) return;
    popup.classList.add('show');
    sessionStorage.setItem(POPUP_KEY, '1');
  }

  function hidePopup() {
    if (!popup) return;
    popup.classList.remove('show');
  }

  if (popup) {
    // Delay: 8s desktop, 15s mobile
    const delay = window.innerWidth < 640 ? 15000 : 8000;
    setTimeout(showPopup, delay);

    // Close on overlay click
    popup.addEventListener('click', e => {
      if (e.target === popup) hidePopup();
    });

    // Close on Escape
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') hidePopup();
    });
  }

  if (popupClose) popupClose.addEventListener('click', hidePopup);

  /* === FADE-IN ON SCROLL === */
  const fadeEls = document.querySelectorAll('.fade-in');

  if ('IntersectionObserver' in window && fadeEls.length) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    fadeEls.forEach(el => observer.observe(el));
  } else {
    // Fallback: show all immediately
    fadeEls.forEach(el => el.classList.add('visible'));
  }

  /* === BUNDLE SELECTOR === */
  const bundleBtns = document.querySelectorAll('.bundle-btn');
  bundleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      bundleBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });

  /* === SMOOTH SCROLL for anchor links === */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', e => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        const offset = nav ? nav.offsetHeight + 16 : 80;
        window.scrollTo({
          top: target.getBoundingClientRect().top + window.scrollY - offset,
          behavior: 'smooth'
        });
      }
    });
  });

})();
