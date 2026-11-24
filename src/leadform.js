/* Multi-step lead form. Validates each step, scores lead quality (hidden), posts to the enquiry endpoint.
   Every state from strategy pack section 13 is kept: submitting, accepted, field errors, failure, rate limit. */
(function () {
  'use strict';
  var form = document.getElementById('lead-form');
  if (!form) return;
  var ENDPOINT = '/api/enquiries';
  var PHONE = '020 4628 8209';
  var WA = '447570359908';
  var steps = Array.prototype.slice.call(form.querySelectorAll('.lf-step'));
  var card = form.closest('.lf-card') || document;
  var bar = card.querySelector('.lf-bar span');
  var count = card.querySelector('.lf-count');
  var back = form.querySelector('[data-lf-back]');
  var next = form.querySelector('[data-lf-next]');
  var send = form.querySelector('[data-lf-send]');
  var summary = document.getElementById('lf-summary');
  var status = document.getElementById('lf-status');
  var loadedAt = Date.now();
  var submissionId = (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : String(loadedAt) + Math.random().toString(16).slice(2);
  var current = 0;
  window.dataLayer = window.dataLayer || [];

  function val(name) { var el = form.elements[name]; if (!el) return ''; if (el.length !== undefined && el.tagName !== 'SELECT') { for (var i = 0; i < el.length; i++) if (el[i].checked) return el[i].value; return ''; } return (el.value || '').trim(); }
  function vals(name) { return Array.prototype.filter.call(form.querySelectorAll('input[name="' + name + '"]'), function (b) { return b.checked; }).map(function (b) { return b.value; }); }

  // Phone becomes required only when a call or WhatsApp reply is chosen.
  function syncPhone() {
    var m = val('reply_method');
    var need = m === 'phone' || m === 'whatsapp';
    var lab = form.querySelector('label[for="lf-phone"]');
    if (lab) lab.textContent = need ? 'Phone or WhatsApp number' : 'Phone number (optional)';
    form.elements.phone.required = need;
  }
  form.addEventListener('change', function (e) { if (e.target.name === 'reply_method') syncPhone(); });
  syncPhone();

  var RULES = [
    function () { return vals('services').length ? {} : { services: 'Please choose at least one. Pick "Not sure yet" if you are unsure.' }; },
    function () {
      var e = {};
      if (!val('business_type')) e.business_type = 'Please choose the type of business.';
      if (!val('staff')) e.staff = 'Please choose how many people work in the business.';
      if (!val('turnover')) e.turnover = 'Please choose a range, or "Prefer not to say".';
      return e;
    },
    function () {
      var e = {};
      if (!val('books_status')) e.books_status = 'Please tell us how up to date your books are.';
      var m = val('message');
      if (!m) e.message = 'Please tell us a little about what you need.';
      else if (m.length < 10) e.message = 'Please add a few more words so we can prepare.';
      return e;
    },
    function () {
      var e = {};
      if (!val('start')) e.start = 'Please choose when you would like to start.';
      if (!val('decision')) e.decision = 'Please choose one.';
      return e;
    },
    function () {
      var e = {};
      var n = val('name'); if (n.length < 2) e.name = 'Please enter your name.';
      var em = val('email');
      if (!em) e.email = 'Please enter your email address.';
      else if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(em)) e.email = 'Please check your email address. It should look like name@company.co.uk.';
      var ph = val('phone');
      if (form.elements.phone.required && !ph) e.phone = 'Please add a number we can call or message.';
      else if (ph && !(/^[+()\d\s-]{7,20}$/.test(ph) && ph.replace(/\D/g, '').length >= 7)) e.phone = 'Please check the number.';
      return e;
    }
  ];
  var LABELS = { services: 'Services', business_type: 'Type of business', staff: 'People in the business', turnover: 'Yearly turnover', books_status: 'State of your books', message: 'What you want to change', start: 'Start date', decision: 'Decision maker', name: 'Full name', email: 'Email', phone: 'Phone' };

  function clearErrors() { form.querySelectorAll('.has-error').forEach(function (el) { el.classList.remove('has-error'); }); form.querySelectorAll('.err').forEach(function (el) { el.textContent = ''; }); }
  function showErrors(errs) {
    clearErrors();
    var keys = Object.keys(errs);
    keys.forEach(function (k) {
      var wrap = document.getElementById('lf-' + k + '-wrap'); var err = document.getElementById('lf-' + k + '-err');
      if (wrap) wrap.classList.add('has-error'); if (err) err.textContent = errs[k];
    });
    if (!keys.length) { summary.classList.remove('is-shown'); return true; }
    summary.querySelector('h2').textContent = keys.length === 1 ? 'There is 1 problem with your enquiry' : 'There are ' + keys.length + ' problems with your enquiry';
    var ul = summary.querySelector('ul'); ul.innerHTML = '';
    keys.forEach(function (k) { var li = document.createElement('li'); var a = document.createElement('a'); a.href = '#lf-' + k + '-wrap'; a.textContent = LABELS[k] + ': ' + errs[k]; li.appendChild(a); ul.appendChild(li); });
    summary.classList.add('is-shown'); summary.focus();
    return false;
  }

  function show(i) {
    current = i;
    steps.forEach(function (s, k) { s.hidden = k !== i; });
    bar.style.width = Math.round((i + 1) * 100 / steps.length) + '%';
    count.textContent = 'Step ' + (i + 1) + ' of ' + steps.length + ': ' + steps[i].getAttribute('data-title');
    back.hidden = i === 0;
    next.hidden = i === steps.length - 1;
    send.hidden = i !== steps.length - 1;
    window.dataLayer.push({ event: 'lead_form_step', step: i + 1, page_type: document.body.getAttribute('data-page') || 'other' });
  }
  next.addEventListener('click', function () {
    if (!showErrors(RULES[current]())) return;
    show(current + 1);
    var first = steps[current].querySelector('input, select, textarea'); if (first) first.focus({ preventScroll: true });
    form.scrollIntoView({ block: 'start', behavior: 'smooth' });
  });
  back.addEventListener('click', function () { clearErrors(); summary.classList.remove('is-shown'); show(current - 1); });

  // Hidden lead quality score: timing, authority, size, urgency and effort. Sent to the CRM, never shown.
  function score() {
    var s = 0;
    s += { two_weeks: 3, month: 2, quarter: 1, researching: 0 }[val('start')] || 0;
    s += { yes: 2, shared: 1, other: 0 }[val('decision')] || 0;
    s += { solo: 1, '2_9': 2, '10_49': 3, '50_plus': 2 }[val('staff')] || 0;
    s += { under_90k: 1, '90k_250k': 2, '250k_1m': 3, '1m_5m': 3, over_5m: 2, undisclosed: 1 }[val('turnover')] || 0;
    if (vals('services').length >= 2) s += 1;
    if (val('books_status') === 'behind_1_3' || val('books_status') === 'behind_3_plus') s += 1;
    var dl = vals('deadlines'); if (dl.length && dl.indexOf('none') === -1 && dl.indexOf('not_sure') === -1) s += 1;
    if (val('message').length >= 60) s += 1;
    if (val('phone')) s += 1;
    if (val('budget') && val('budget') !== 'not_sure') s += 1;
    return { score: s, tier: s >= 11 ? 'hot' : (s >= 7 ? 'warm' : 'nurture') };
  }

  function attribution() {
    var q = new URLSearchParams(location.search), first;
    try { first = sessionStorage.getItem('av_first') || location.pathname; } catch (e) { first = location.pathname; }
    return { page_url: location.href.split('#')[0], page_title: document.title, referrer: document.referrer || 'direct/unknown', utm_source: q.get('utm_source') || 'direct/unknown', utm_medium: q.get('utm_medium') || 'direct/unknown', utm_campaign: q.get('utm_campaign') || 'direct/unknown', utm_term: q.get('utm_term') || 'direct/unknown', utm_content: q.get('utm_content') || 'direct/unknown', gclid: q.get('gclid') || 'direct/unknown', first_landing: first, form_version: '2' };
  }

  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function wa() { return 'https://wa.me/' + WA + '?text=' + encodeURIComponent('Hi Aviteus, I have a question about your services.'); }
  function showStatus(kind, ref) {
    var first = val('name').split(/\s+/)[0] || '';
    var method = { email: 'email', phone: 'phone', whatsapp: 'WhatsApp' }[val('reply_method') || 'email'];
    var html;
    if (kind === 'ok') html = '<h2 tabindex="-1">Thanks, ' + esc(first) + '. We have your enquiry.</h2><p>Your reference is <b class="av-num">' + esc(ref || '') + '</b>. We will reply by ' + method + ', using the details you gave. If it is urgent, call <a class="tlink" href="tel:02046288209">' + PHONE + '</a>, Monday to Friday, 9am to 5pm.</p><div class="actions"><a class="av-btn av-btn--outline" href="' + wa() + '" target="_blank" rel="noopener">Chat on WhatsApp</a></div>';
    else if (kind === 'rate') html = '<h2 tabindex="-1">Please wait a minute</h2><p>You have sent several enquiries in a short time. Please wait a minute and try again, or message us on WhatsApp.</p><div class="actions"><a class="av-btn av-btn--outline" href="' + wa() + '" target="_blank" rel="noopener">Chat on WhatsApp</a></div>';
    else html = '<h2 tabindex="-1">We could not send your enquiry just now</h2><p>Your details are still here. Please try again, or message us on WhatsApp.</p><div class="actions"><button type="button" class="av-btn av-btn--ember" data-retry>Try again</button><a class="av-btn av-btn--outline" href="' + wa() + '" target="_blank" rel="noopener">Chat on WhatsApp</a></div>';
    status.innerHTML = html; status.classList.add('is-shown');
    if (kind === 'ok') form.hidden = true;
    status.querySelector('h2').focus();
  }
  status.addEventListener('click', function (e) { if (e.target.closest('[data-retry]')) { status.classList.remove('is-shown'); send.focus(); } });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (current !== steps.length - 1) { next.click(); return; }
    status.classList.remove('is-shown');
    if (!showErrors(RULES[current]())) return;
    var data = { services: vals('services'), deadlines: vals('deadlines') };
    ['business_type', 'staff', 'turnover', 'vat_registered', 'industry', 'books_now', 'software', 'books_status', 'message', 'start', 'decision', 'budget', 'source', 'name', 'email', 'company', 'phone', 'reply_method', 'best_time', 'website'].forEach(function (k) { data[k] = val(k); });
    data.newsletter = !!form.elements.newsletter.checked;
    var sc = score(); data.lead_score = sc.score; data.lead_tier = sc.tier;
    data.submission_id = submissionId; data.elapsed_ms = Date.now() - loadedAt;
    var a = attribution(); Object.keys(a).forEach(function (k) { data[k] = a[k]; });
    form.setAttribute('aria-busy', 'true'); send.disabled = true; send.textContent = 'Sending...';
    var done = function () { form.setAttribute('aria-busy', 'false'); send.disabled = false; send.textContent = 'Send enquiry'; };
    fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { status: r.status, body: j }; }); })
      .then(function (res) {
        done();
        if (res.status === 201 || (res.status === 200 && res.body.reference)) {
          showStatus('ok', res.body.reference);
          window.dataLayer.push({ event: 'generate_lead', form_id: 'lead_form', service: data.services.join('|'), reply_method: data.reply_method, lead_tier: data.lead_tier, page_type: document.body.getAttribute('data-page') || 'other' });
        } else if (res.status === 422 && res.body.errors) { showErrors(res.body.errors); }
        else if (res.status === 429) { showStatus('rate'); window.dataLayer.push({ event: 'form_error', error_type: 'rate_limited' }); }
        else { showStatus('fail'); window.dataLayer.push({ event: 'form_error', error_type: 'server_' + res.status }); }
      })
      .catch(function () { done(); showStatus('fail'); window.dataLayer.push({ event: 'form_error', error_type: 'network' }); });
  });

  show(0);
  // Arriving from a "Book a review" link with #review: bring the form into view.
  if (location.hash === '#review') setTimeout(function () { form.scrollIntoView({ block: 'start' }); }, 50);
})();
