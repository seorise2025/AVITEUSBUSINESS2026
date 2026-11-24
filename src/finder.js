/* UK deadline finder. Rule-based, runs in the browser, stores nothing, sends no personal data. */
(function () {
  'use strict';
  var form = document.getElementById('finder-form');
  if (!form) return;
  var out = document.getElementById('finder-results');
  var icsBtn = document.getElementById('finder-ics');
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var SHORT = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
  var current = [];

  function d(y, m, day) { return new Date(Date.UTC(y, m, day)); }            // m is 0-based; overflow rolls over
  function monthEnd(y, m) { return d(y, m + 1, 0); }
  function fmt(dt) { return String(dt.getUTCDate()).padStart(2, '0') + ' ' + SHORT[dt.getUTCMonth()] + ' ' + dt.getUTCFullYear(); }
  function long(dt) { return dt.getUTCDate() + ' ' + MONTHS[dt.getUTCMonth()] + ' ' + dt.getUTCFullYear(); }
  function weekend(dt) { var w = dt.getUTCDay(); return w === 0 || w === 6; }

  function build(opts) {
    var now = new Date();
    var today = d(now.getFullYear(), now.getMonth(), now.getDate());
    var end = d(now.getFullYear() + 1, now.getMonth(), now.getDate());
    var list = [];
    function add(date, title, detail) { if (date >= today && date <= end) list.push({ date: date, title: title, detail: detail }); }
    var y0 = now.getFullYear() - 2;

    for (var y = y0; y <= y0 + 4; y++) {
      // Limited company dates, from a year end on the last day of the chosen month.
      if (opts.ye !== '') {
        var m = +opts.ye;
        var ye = monthEnd(y, m);
        var yeTxt = 'Year ended ' + long(ye);
        add(monthEnd(y, m + 9), 'Annual accounts to Companies House', yeTxt + '. Due 9 months after your year end.');
        add(d(y, m + 10, 1), 'Corporation tax payment', yeTxt + '. Due 9 months and 1 day after your year end.');
        add(monthEnd(y + 1, m), 'Company tax return (CT600)', yeTxt + '. Due 12 months after your year end.');
      }
      // VAT: return and payment due 1 month and 7 days after each period ends.
      if (opts.vat !== 'none') {
        for (var pm = 0; pm < 12; pm++) {
          var include = opts.vat === 'monthly' || (pm % 3) === +opts.vat;
          if (!include) continue;
          var pEnd = monthEnd(y, pm);
          var label = opts.vat === 'monthly' ? 'Month ended ' : 'Quarter ended ';
          add(d(y, pm + 2, 7), 'VAT return and payment', label + long(pEnd) + '.');
        }
      }
      // Payroll employer dates.
      if (opts.payroll) {
        add(d(y, 4, 31), 'P60s to every employee', 'For the tax year that ended on 5 April ' + y + '.');
        add(d(y, 6, 6), 'P11D and P11D(b) forms to HMRC', 'Benefits in kind for the tax year that ended on 5 April ' + y + '.');
      }
      // Personal Self Assessment.
      if (opts.sa) {
        add(d(y, 0, 31), 'Self Assessment return and tax due', 'Online return and balancing payment for ' + (y - 2) + '/' + String(y - 1).slice(2) + '. First payment on account for ' + (y - 1) + '/' + String(y).slice(2) + ', if one applies.');
        add(d(y, 6, 31), 'Second payment on account', 'For the ' + (y - 1) + '/' + String(y).slice(2) + ' tax year, if one applies.');
      }
    }
    // Monthly PAYE: show the next two only, so the list stays readable.
    if (opts.payroll) {
      var shown = 0;
      for (var k = 0; k < 3 && shown < 2; k++) {
        var p = d(now.getFullYear(), now.getMonth() + k, 22);
        if (p >= today) { list.push({ date: p, title: 'PAYE and National Insurance to HMRC', detail: 'Electronic payment for the tax month ending on the 5th. Due on the 22nd of every month.' }); shown++; }
      }
    }
    list.sort(function (a, b) { return a.date - b.date; });
    return { items: list, today: today };
  }

  function render(res) {
    current = res.items;
    out.innerHTML = '';
    if (!res.items.length) {
      out.innerHTML = '<p class="results-empty">Choose at least one option to see your dates.</p>';
      icsBtn.hidden = true;
      return;
    }
    res.items.forEach(function (it) {
      var days = Math.round((it.date - res.today) / 86400000);
      var row = document.createElement('div');
      row.className = 'result';
      row.setAttribute('role', 'listitem');
      row.innerHTML = '<span class="result-date">' + fmt(it.date) + '</span>' +
        '<span class="result-what"><b></b><span></span></span>' +
        '<span class="result-left">' + (days === 0 ? 'TODAY' : days + ' DAYS') + '</span>';
      row.querySelector('b').textContent = it.title;
      row.querySelector('.result-what span').textContent = it.detail + (weekend(it.date) ? ' Falls on a weekend: pay by the working day before.' : '');
      out.appendChild(row);
    });
    icsBtn.hidden = false;
  }

  function opts() {
    return {
      ye: form.elements.year_end.value,
      vat: form.elements.vat.value,
      payroll: form.elements.payroll.checked,
      sa: form.elements.sa.checked
    };
  }
  function run(e) {
    if (e) e.preventDefault();
    var o = opts();
    render(build(o));
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: 'deadline_finder_used', page_type: 'tool', vat: o.vat, payroll: o.payroll, self_assessment: o.sa, has_year_end: o.ye !== '' });
  }
  form.addEventListener('submit', run);
  form.addEventListener('change', function () { render(build(opts())); });

  icsBtn.addEventListener('click', function () {
    var stamp = new Date().toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
    var lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Aviteus Business Solutions//Deadline finder//EN', 'CALSCALE:GREGORIAN'];
    current.forEach(function (it, i) {
      var ds = it.date.toISOString().slice(0, 10).replace(/-/g, '');
      var next = new Date(it.date.getTime() + 86400000).toISOString().slice(0, 10).replace(/-/g, '');
      lines.push('BEGIN:VEVENT', 'UID:' + ds + '-' + i + '@aviteusbusiness.co.uk', 'DTSTAMP:' + stamp, 'DTSTART;VALUE=DATE:' + ds, 'DTEND;VALUE=DATE:' + next,
        'SUMMARY:' + it.title.replace(/[,;]/g, ' '), 'DESCRIPTION:' + it.detail.replace(/[,;]/g, ' ') + ' Check with your accountant or GOV.UK.',
        'BEGIN:VALARM', 'TRIGGER:-P14D', 'ACTION:DISPLAY', 'DESCRIPTION:' + it.title.replace(/[,;]/g, ' ') + ' in 14 days', 'END:VALARM', 'END:VEVENT');
    });
    lines.push('END:VCALENDAR');
    var blob = new Blob([lines.join('\r\n')], { type: 'text/calendar' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'uk-tax-deadlines.ics';
    document.body.appendChild(a); a.click(); a.remove();
    window.dataLayer.push({ event: 'deadline_calendar_download', page_type: 'tool', count: current.length });
  });

  render(build(opts()));
})();
