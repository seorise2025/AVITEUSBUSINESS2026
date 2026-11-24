/* Free tools: VAT registration checker and switching checklist. Runs in the browser; sends nothing. */
(function () {
  'use strict';
  var doc = document;
  var gbp = function (n) { return '£' + Math.round(n).toLocaleString('en-GB'); };
  var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var LONG = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  window.dataLayer = window.dataLayer || [];

  // ---------------- VAT registration checker ----------------
  var vat = doc.getElementById('vat-form');
  if (vat) {
    var THRESHOLD = +vat.getAttribute('data-threshold');            // set in src/data.json, checked by the reviewer
    var grid = doc.getElementById('vat-months');
    var out = doc.getElementById('vat-result');
    var now = new Date();
    var months = [];                                                  // last 12 complete months, oldest first
    for (var i = 12; i >= 1; i--) { var d = new Date(now.getFullYear(), now.getMonth() - i, 1); months.push(d); }
    grid.innerHTML = months.map(function (d, k) {
      var id = 'vm-' + k;
      return '<div class="field"><label for="' + id + '">' + MONTHS[d.getMonth()] + ' ' + d.getFullYear() + '</label>' +
        '<input class="av-input av-num" id="' + id + '" inputmode="decimal" autocomplete="off" placeholder="0"></div>';
    }).join('');
    var inputs = grid.querySelectorAll('input');
    var num = function (v) { v = String(v || '').replace(/[£,\s]/g, ''); var n = parseFloat(v); return isFinite(n) && n > 0 ? n : 0; };

    doc.getElementById('vat-fill').addEventListener('click', function () {
      var first = inputs[0].value; inputs.forEach(function (el) { el.value = first; }); calc();
    });

    function calc() {
      var vals = Array.prototype.map.call(inputs, function (el) { return num(el.value); });
      var next30 = num(vat.elements.next30.value);
      var total = vals.reduce(function (a, b) { return a + b; }, 0);
      var filled = vals.filter(function (v) { return v > 0; }).length;
      if (!filled && !next30) { out.innerHTML = '<p class="results-empty">Enter your monthly VAT-taxable turnover to see where you stand.</p>'; return; }
      var recent = vals.slice(-3); var avg = recent.reduce(function (a, b) { return a + b; }, 0) / 3;
      var status, title, body;
      if (next30 > THRESHOLD) {
        status = 'over'; title = 'Register now';
        body = 'You expect ' + gbp(next30) + ' of taxable turnover in the next 30 days alone, which is over the ' + gbp(THRESHOLD) + ' threshold. You must register by the end of that 30-day period.';
      } else if (total > THRESHOLD) {
        status = 'over'; title = 'You are over the threshold';
        body = 'Your rolling 12-month taxable turnover is ' + gbp(total) + ', over the ' + gbp(THRESHOLD) + ' threshold. You must register within 30 days of the end of the month you went over. Late registration can mean paying VAT you never charged.';
      } else {
        var head = THRESHOLD - total;
        // Project forward: each new month at your recent 3-month average, the oldest month drops off.
        var roll = vals.slice(), cross = null;
        for (var m = 1; m <= 24 && avg > 0; m++) {
          roll.shift(); roll.push(avg);
          if (roll.reduce(function (a, b) { return a + b; }, 0) > THRESHOLD) { cross = m; break; }
        }
        if (cross) {
          var cd = new Date(now.getFullYear(), now.getMonth() + cross - 1, 1);
          status = cross <= 3 ? 'near' : 'watch';
          title = cross <= 3 ? 'Close to the threshold' : 'Under, but heading towards it';
          body = 'Your rolling 12-month total is ' + gbp(total) + ', so you have ' + gbp(head) + ' of headroom. At your recent average of ' + gbp(avg) + ' a month, you would go over around <b>' + LONG[cd.getMonth()] + ' ' + cd.getFullYear() + '</b>.';
        } else {
          status = 'under'; title = 'Under the threshold';
          body = 'Your rolling 12-month total is ' + gbp(total) + ', with ' + gbp(head) + ' of headroom. At your recent average, you would stay under. Check again each month: the total rolls forward.';
        }
      }
      var icon = { over: '!', near: '!', watch: '↗', under: '✓' }[status];
      out.innerHTML = '<div class="verdict verdict--' + status + '" role="status"><span class="verdict-icon" aria-hidden="true">' + icon + '</span><div><p class="verdict-title">' + title + '</p><p>' + body + '</p></div></div>' +
        '<table class="facts-table mt-5"><tr><th scope="row">Rolling 12-month total</th><td>' + gbp(total) + '</td></tr><tr><th scope="row">Registration threshold used</th><td>' + gbp(THRESHOLD) + '</td></tr><tr><th scope="row">Recent monthly average</th><td>' + gbp(avg) + '</td></tr></table>';
      window.dataLayer.push({ event: 'vat_checker_used', page_type: 'tool', result: status });
    }
    vat.addEventListener('input', calc);
    vat.addEventListener('submit', function (e) { e.preventDefault(); calc(); });
    calc();
  }

  // ---------------- Switching checklist ----------------
  var list = doc.getElementById('switch-list');
  if (list) {
    var KEY = 'av_switch_v1';
    var boxes = list.querySelectorAll('input[type="checkbox"]');
    var bar = doc.getElementById('switch-progress');
    var label = doc.getElementById('switch-count');
    var saved = {};
    try { saved = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { saved = {}; }
    boxes.forEach(function (b) { b.checked = !!saved[b.id]; });
    function update(save) {
      var done = Array.prototype.filter.call(boxes, function (b) { return b.checked; }).length;
      bar.style.width = Math.round(done * 100 / boxes.length) + '%';
      bar.parentNode.setAttribute('aria-valuenow', String(done));
      label.textContent = done + ' of ' + boxes.length + ' done';
      if (save) {
        var s = {}; boxes.forEach(function (b) { if (b.checked) s[b.id] = 1; });
        try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) {}
      }
    }
    list.addEventListener('change', function () { update(true); window.dataLayer.push({ event: 'switch_checklist_tick', page_type: 'tool' }); });
    doc.getElementById('switch-reset').addEventListener('click', function () { boxes.forEach(function (b) { b.checked = false; }); update(true); });
    var copyBtn = doc.getElementById('switch-copy');
    copyBtn.addEventListener('click', function () {
      var text = Array.prototype.map.call(list.querySelectorAll('.check-item'), function (li) {
        var b = li.querySelector('input'); return (b.checked ? '[x] ' : '[ ] ') + li.querySelector('.ci-text b').textContent;
      }).join('\n');
      var done = function () { copyBtn.textContent = 'Copied'; setTimeout(function () { copyBtn.textContent = 'Copy the checklist'; }, 2000); };
      try { navigator.clipboard.writeText(text).then(done, function () {}); } catch (e) {}
    });
    update(false);
  }
})();
