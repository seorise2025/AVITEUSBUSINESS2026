/* Aviteus website script. No framework, no third-party code until consent. */
(function () {
  'use strict';

  // ---- Settings. Edit these, not the code below. ----
  var CONFIG = {
    gtmId: '',                       // e.g. 'GTM-XXXXXXX'. Empty = no analytics loaded at all.
    enquiryEndpoint: '/api/enquiries',
    turnstileSiteKey: '',            // Cloudflare Turnstile site key, when the backend exists.
    phone: '020 4628 8209',
    whatsapp: '447570359908'
  };

  var doc = document;
  var body = doc.body;
  var pageType = body.getAttribute('data-page') || 'other';
  window.dataLayer = window.dataLayer || [];

  // ---------- Consent and analytics (UK PECR: reject is as easy as accept) ----------
  function readConsent() { try { return localStorage.getItem('av_consent'); } catch (e) { return null; } }
  function saveConsent(v) { try { localStorage.setItem('av_consent', v); } catch (e) {} }
  function gtag() { window.dataLayer.push(arguments); }
  gtag('consent', 'default', { analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', wait_for_update: 500 });

  function loadGtm() {
    if (!CONFIG.gtmId || window.__avGtm) return;
    window.__avGtm = true;
    window.dataLayer.push({ 'gtm.start': Date.now(), event: 'gtm.js' });
    var s = doc.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtm.js?id=' + encodeURIComponent(CONFIG.gtmId);
    doc.head.appendChild(s);
  }
  function applyConsent(v) {
    if (v === 'granted') {
      gtag('consent', 'update', { analytics_storage: 'granted' }); loadGtm();
      try { if (!sessionStorage.getItem('av_first')) sessionStorage.setItem('av_first', location.pathname); } catch (e) {}
    }
  }

  var banner = doc.getElementById('cookie');
  var consent = readConsent();
  if (consent) { applyConsent(consent); }
  else if (banner) { banner.hidden = false; }
  if (banner) {
    banner.addEventListener('click', function (e) {
      var b = e.target.closest('[data-consent]');
      if (!b) return;
      var v = b.getAttribute('data-consent');
      saveConsent(v); applyConsent(v);
      banner.hidden = true;
      updateBar();
    });
  }
  doc.addEventListener('click', function (e) {
    var t = e.target.closest('[data-cookie-settings]');
    if (t && banner) { e.preventDefault(); banner.hidden = false; }
  });

  // ---------- Event tracking (never sends personal data) ----------
  function track(name, params) {
    var p = params || {};
    p.event = name;
    p.page_type = pageType;
    window.dataLayer.push(p);
  }
  doc.addEventListener('click', function (e) {
    var a = e.target.closest('a, button');
    if (!a) return;
    var placement = a.getAttribute('data-placement') || 'unknown';
    var href = a.getAttribute('href') || '';
    if (href.indexOf('wa.me/') > -1) track('whatsapp_click', { placement: placement, service: body.getAttribute('data-service') || 'general' });
    else if (href.indexOf('tel:') === 0) track('phone_click', { placement: placement });
    else if (a.hasAttribute('data-book')) track('book_review_click', { placement: placement });
  });

  // ---------- Header: services menu and mobile menu ----------
  // Services panel: one state, shown with the hidden attribute. Click toggles; Escape, outside click and leaving close it.
  var subBtn = doc.querySelector('.menu-btn');
  var mega = doc.getElementById('mega-services');
  var hasSub = doc.querySelector('.has-sub');
  if (subBtn && mega && hasSub) {
    var hoverTimer = null;
    var canHover = window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    var setOpen = function (open) {
      subBtn.setAttribute('aria-expanded', String(open));
      mega.hidden = !open;
      body.classList.toggle('mega-open', open);
    };
    setOpen(false);
    subBtn.addEventListener('click', function () { clearTimeout(hoverTimer); setOpen(mega.hidden); });
    if (canHover) {
      hasSub.addEventListener('mouseenter', function () { clearTimeout(hoverTimer); hoverTimer = setTimeout(function () { setOpen(true); }, 120); });
      hasSub.addEventListener('mouseleave', function () { clearTimeout(hoverTimer); hoverTimer = setTimeout(function () { setOpen(false); }, 250); });
    }
    doc.addEventListener('click', function (e) { if (!e.target.closest('.has-sub')) setOpen(false); });
    doc.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !mega.hidden) { setOpen(false); subBtn.focus(); } });
    hasSub.addEventListener('focusout', function (e) { if (e.relatedTarget && !hasSub.contains(e.relatedTarget)) setOpen(false); });
    mega.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
  }
  var navBtn = doc.querySelector('.nav-toggle');
  var mobileNav = doc.getElementById('mobile-nav');
  if (navBtn && mobileNav) {
    navBtn.addEventListener('click', function () {
      var open = navBtn.getAttribute('aria-expanded') === 'true';
      navBtn.setAttribute('aria-expanded', String(!open));
      navBtn.setAttribute('aria-label', open ? 'Open menu' : 'Close menu');
      mobileNav.classList.toggle('is-open', !open);
      body.classList.toggle('nav-open', !open);
    });
  }

  // ---------- Sticky mobile bar ----------
  var bar = doc.getElementById('sticky-bar');
  var formOnScreen = false;
  var keyboardOpen = false;
  function updateBar() {
    if (!bar) return;
    var noChoice = banner && !banner.hidden;
    bar.hidden = noChoice || formOnScreen || keyboardOpen;
  }
  if (bar) {
    body.classList.add('has-sticky');
    var watched = doc.querySelectorAll('form.form, .finder form');
    if ('IntersectionObserver' in window && watched.length) {
      var io = new IntersectionObserver(function (entries) {
        formOnScreen = entries.some(function (en) { return en.isIntersecting; });
        updateBar();
      });
      watched.forEach(function (f) { io.observe(f); });
    }
    doc.addEventListener('focusin', function (e) { if (e.target.matches('input, textarea, select')) { keyboardOpen = true; updateBar(); } });
    doc.addEventListener('focusout', function () { keyboardOpen = false; updateBar(); });
    updateBar();
  }

  // ---------- "Book a review" scrolls to the lead form when the page has one ----------
  var leadCard = doc.getElementById('review');
  if (leadCard && doc.getElementById('lead-form')) {
    doc.addEventListener('click', function (e) {
      var a = e.target.closest('a[data-book]');
      if (!a || a.closest('#review')) return;
      e.preventDefault();
      leadCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
      var first = leadCard.querySelector('input'); if (first) setTimeout(function () { first.focus({ preventScroll: true }); }, 400);
    });
  }

  // ---------- WhatsApp widget ----------
  var waBox = doc.getElementById('wa-widget');
  if (waBox) {
    var fab = doc.getElementById('wa-fab'), panel = doc.getElementById('wa-panel'), hint = doc.getElementById('wa-hint');
    var leadForm = doc.getElementById('lead-form'), leadVisible = false;
    var openPanel = function (open) { panel.hidden = !open; fab.setAttribute('aria-expanded', String(open)); if (open) { hint.hidden = true; track('whatsapp_widget_open', { placement: 'widget' }); } };
    var showWidget = function () {
      var noChoice = banner && !banner.hidden;
      waBox.hidden = !!noChoice;
      waBox.classList.toggle('wa-dim', leadVisible);
    };
    fab.addEventListener('click', function () { openPanel(panel.hidden); });
    waBox.addEventListener('click', function (e) {
      if (e.target.closest('[data-wa-close]')) { openPanel(false); fab.focus(); }
      if (e.target.closest('[data-wa-hint-close]')) { hint.hidden = true; }
    });
    doc.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) { openPanel(false); fab.focus(); } });
    if (leadForm && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (en) { leadVisible = en.some(function (x) { return x.isIntersecting; }); if (leadVisible) { openPanel(false); hint.hidden = true; } showWidget(); }).observe(leadForm);
    }
    if (banner) banner.addEventListener('click', function () { setTimeout(showWidget, 0); });
    showWidget();
    // A gentle greeting, once per visit, after 20 seconds. Never while the lead form is on screen.
    var seen = false; try { seen = sessionStorage.getItem('av_wa_hint') === '1'; } catch (e) {}
    if (!seen) setTimeout(function () {
      if (waBox.hidden || leadVisible || !panel.hidden) return;
      hint.hidden = false; try { sessionStorage.setItem('av_wa_hint', '1'); } catch (e) {}
    }, 20000);
  }
})();
