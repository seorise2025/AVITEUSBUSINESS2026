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
    if (v === 'granted') { gtag('consent', 'update', { analytics_storage: 'granted' }); loadGtm(); }
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
  var subBtn = doc.querySelector('.menu-btn');
  if (subBtn) {
    subBtn.addEventListener('click', function () {
      var open = subBtn.getAttribute('aria-expanded') === 'true';
      subBtn.setAttribute('aria-expanded', String(!open));
    });
    doc.addEventListener('click', function (e) {
      if (!e.target.closest('.has-sub')) subBtn.setAttribute('aria-expanded', 'false');
    });
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { subBtn.setAttribute('aria-expanded', 'false'); }
    });
  }
  var navBtn = doc.querySelector('.nav-toggle');
  var mobileNav = doc.getElementById('mobile-nav');
  if (navBtn && mobileNav) {
    navBtn.addEventListener('click', function () {
      var open = navBtn.getAttribute('aria-expanded') === 'true';
      navBtn.setAttribute('aria-expanded', String(!open));
      navBtn.setAttribute('aria-label', open ? 'Open menu' : 'Close menu');
      mobileNav.classList.toggle('is-open', !open);
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

  // ---------- Enquiry form (strategy pack, section 13) ----------
  var form = doc.getElementById('enquiry-form');
  if (!form) return;

  var loadedAt = Date.now();
  var submissionId = (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : String(loadedAt) + Math.random().toString(16).slice(2);
  var summary = doc.getElementById('err-summary');
  var status = doc.getElementById('form-status');
  var submitBtn = form.querySelector('[type="submit"]');
  var phoneField = doc.getElementById('f-phone-wrap');

  // Attribution. Missing values become direct/unknown and never block a submit.
  (function attribution() {
    var q = new URLSearchParams(location.search);
    var first;
    try { first = sessionStorage.getItem('av_first'); if (!first) { first = location.pathname; sessionStorage.setItem('av_first', first); } } catch (e) { first = location.pathname; }
    var vals = {
      page_url: location.href.split('#')[0], page_title: doc.title, referrer: doc.referrer || 'direct/unknown',
      utm_source: q.get('utm_source'), utm_medium: q.get('utm_medium'), utm_campaign: q.get('utm_campaign'),
      utm_term: q.get('utm_term'), utm_content: q.get('utm_content'), gclid: q.get('gclid'),
      first_landing: first, form_version: form.getAttribute('data-version') || '1'
    };
    Object.keys(vals).forEach(function (k) {
      var i = doc.createElement('input'); i.type = 'hidden'; i.name = k; i.value = vals[k] || 'direct/unknown'; form.appendChild(i);
    });
  })();

  // Phone is shown and required only for Phone call or WhatsApp.
  function syncPhone() {
    var m = form.querySelector('input[name="reply_method"]:checked');
    var need = m && m.value !== 'email';
    phoneField.hidden = !need;
    phoneField.querySelector('input').required = !!need;
  }
  form.addEventListener('change', function (e) { if (e.target.name === 'reply_method') syncPhone(); });
  syncPhone();

  var rules = {
    name: function (v) { v = v.trim(); return v.length < 2 || v.length > 100 ? 'Please enter your name.' : ''; },
    email: function (v) { v = v.trim(); if (!v) return 'Please enter your email address.'; return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) ? '' : 'Please check your email address. It should look like name@company.co.uk.'; },
    service: function (v) { return v ? '' : "Please choose one. Pick 'not sure yet' if you are unsure."; },
    message: function (v) { v = v.trim(); if (!v) return 'Please tell us a little about what you need.'; return v.length < 10 ? 'Please add a few more words so we can prepare.' : (v.length > 2000 ? 'Please keep your message under 2,000 characters.' : ''); },
    phone: function (v) { if (phoneField.hidden) return ''; v = v.trim(); if (!v) return 'Please add a number we can call or message.'; return /^[+()\d\s-]{7,20}$/.test(v) && v.replace(/\D/g, '').length >= 7 ? '' : 'Please check the number.'; }
  };
  var labels = { name: 'Full name', email: 'Email', service: 'Which service is this about?', message: 'What would you like help with?', phone: 'Phone or WhatsApp number' };

  function setError(name, msg) {
    var el = form.elements[name];
    var wrap = doc.getElementById('f-' + name + '-wrap');
    var err = doc.getElementById('f-' + name + '-err');
    if (!wrap || !err) return;
    wrap.classList.toggle('has-error', !!msg);
    err.textContent = msg;
    if (el && el.setAttribute) el.setAttribute('aria-invalid', msg ? 'true' : 'false');
  }
  function validate() {
    var errors = [];
    Object.keys(rules).forEach(function (k) {
      var el = form.elements[k];
      var msg = rules[k](el ? el.value : '');
      setError(k, msg);
      if (msg) errors.push({ name: k, msg: msg });
    });
    return errors;
  }
  function showSummary(errors) {
    if (!errors.length) { summary.classList.remove('is-shown'); return; }
    summary.querySelector('h2').textContent = errors.length === 1 ? 'There is 1 problem with your enquiry' : 'There are ' + errors.length + ' problems with your enquiry';
    var ul = summary.querySelector('ul'); ul.innerHTML = '';
    errors.forEach(function (er) {
      var li = doc.createElement('li'); var a = doc.createElement('a');
      a.href = '#f-' + er.name; a.textContent = labels[er.name] + ': ' + er.msg; li.appendChild(a); ul.appendChild(li);
    });
    summary.classList.add('is-shown');
    summary.focus();
  }
  Object.keys(rules).forEach(function (k) {
    var el = form.elements[k];
    if (el) el.addEventListener('blur', function () { if (el.value) setError(k, rules[k](el.value)); });
  });

  function waLink() { return 'https://wa.me/' + CONFIG.whatsapp + '?text=' + encodeURIComponent('Hi Aviteus, I have a question about your services.'); }
  function showStatus(kind, data) {
    var first = (form.elements.name.value.trim().split(/\s+/)[0]) || '';
    var method = { email: 'email', phone: 'phone', whatsapp: 'WhatsApp' }[(form.querySelector('input[name="reply_method"]:checked') || {}).value || 'email'];
    var html;
    if (kind === 'ok') {
      html = '<h2 tabindex="-1">Thanks, ' + esc(first) + '. We have your enquiry.</h2>' +
        '<p>Your reference is <b class="av-num">' + esc(data.reference || '') + '</b>. We will reply by ' + method + ', using the details you gave. If it is urgent, call <a class="tlink" href="tel:02046288209" data-placement="form_success">' + CONFIG.phone + '</a>, Monday to Friday, 9am to 5pm.</p>' +
        '<div class="actions"><a class="av-btn av-btn--outline" href="' + waLink() + '" target="_blank" rel="noopener" data-placement="form_success">Chat on WhatsApp</a></div>';
    } else if (kind === 'rate') {
      html = '<h2 tabindex="-1">Please wait a minute</h2><p>You have sent several enquiries in a short time. Please wait a minute and try again, or message us on WhatsApp.</p>' +
        '<div class="actions"><a class="av-btn av-btn--outline" href="' + waLink() + '" target="_blank" rel="noopener" data-placement="form_error">Chat on WhatsApp</a></div>';
    } else {
      html = '<h2 tabindex="-1">We could not send your enquiry just now</h2><p>Your details are still here. Please try again, or message us on WhatsApp.</p>' +
        '<div class="actions"><button type="button" class="av-btn av-btn--ember" data-retry>Try again</button><a class="av-btn av-btn--outline" href="' + waLink() + '" target="_blank" rel="noopener" data-placement="form_error">Chat on WhatsApp</a></div>';
    }
    status.innerHTML = html;
    status.classList.add('is-shown');
    if (kind === 'ok') form.hidden = true;
    status.querySelector('h2').focus();
  }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  status.addEventListener('click', function (e) { if (e.target.closest('[data-retry]')) { status.classList.remove('is-shown'); submitBtn.focus(); } });

  function busy(on) {
    form.setAttribute('aria-busy', on ? 'true' : 'false');
    submitBtn.disabled = on;
    submitBtn.textContent = on ? 'Sending...' : 'Send enquiry';
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    status.classList.remove('is-shown');
    var errors = validate();
    showSummary(errors);
    if (errors.length) return;
    var data = {};
    new FormData(form).forEach(function (v, k) { data[k] = typeof v === 'string' ? v.trim() : v; });
    data.submission_id = submissionId;
    data.elapsed_ms = Date.now() - loadedAt;
    data.newsletter = !!form.elements.newsletter.checked;
    busy(true);
    fetch(CONFIG.enquiryEndpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { status: r.status, body: j }; }); })
      .then(function (res) {
        busy(false);
        if (res.status === 201 || (res.status === 200 && res.body.reference)) {
          showStatus('ok', res.body);
          var m = form.querySelector('input[name="reply_method"]:checked');
          track('generate_lead', { form_id: 'enquiry', service: data.service, reply_method: m ? m.value : 'email' });
        } else if (res.status === 422 && res.body.errors) {
          var list = Object.keys(res.body.errors).map(function (k) { setError(k, res.body.errors[k]); return { name: k, msg: res.body.errors[k] }; });
          showSummary(list);
        } else if (res.status === 429) {
          showStatus('rate'); track('form_error', { error_type: 'rate_limited' });
        } else {
          showStatus('fail'); track('form_error', { error_type: 'server_' + res.status });
        }
      })
      .catch(function () { busy(false); showStatus('fail'); track('form_error', { error_type: 'network' }); });
  });
})();
