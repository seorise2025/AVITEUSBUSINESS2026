"""Page content. Public copy is taken word for word from the Website Copy Deck (24 Nov 2026).
Blocks that wait on approval or proof read from data.json and stay hidden until filled."""
from html import escape
from layout import (SERVICE_MAP, ALSO_AVAILABLE, INDUSTRIES, REG_OFFICE, SITE, PHONE, PHONE_TEL, WA_DISPLAY, EMAIL, ADDRESS, COMPANY_NO, CH_URL, ARROW, PULSE,
                    book_btn, wa_btn, wa, faq_html, faq_ld, breadcrumb_ld, crumbs_html, page)


def close_band(h2, text, service="general", placement="close"):
    return f'''<section class="av-night close-band" aria-labelledby="close-h">
  <div class="wrap inner">
    <div><h2 id="close-h">{h2}</h2><p>{text}</p></div>
    <div class="close-actions">{book_btn(placement)}{wa_btn(placement + "_whatsapp", service, "av-btn av-btn--ghost")}</div>
  </div>
</section>'''


def related(links):
    items = "".join(f'<li><a class="tlink" href="{u}">{t}</a></li>' for t, u in links)
    return f'<nav class="mt-6" aria-label="Related pages"><ul class="choices" style="list-style:none;padding:0;gap:var(--space-5)">{items}</ul></nav>'


def team_block(data, heading, intro_link=False):
    people = [p for p in data.get("team", []) if p.get("consent") and p.get("name") and p.get("role")]
    if not people:
        return ""
    cards = []
    for p in people:
        initials = "".join(w[0] for w in p["name"].split()[:2]).upper()
        photo = f'<img src="{escape(p["photo"])}" alt="{escape(p["name"])}, {escape(p["role"])} at Aviteus Business Solutions" width="96" height="96" loading="lazy">' if p.get("photo") else f'<span class="initials" aria-hidden="true">{initials}</span>'
        cred = " · ".join(x for x in [p.get("qualification"), (p.get("body", "") + (" membership " + p["membership_number"] if p.get("membership_number") else "")).strip()] if x)
        li = f'<a class="tlink" href="{escape(p["linkedin"])}" target="_blank" rel="noopener">LinkedIn</a>' if p.get("linkedin") else ""
        cards.append(f'<article class="person">{photo}<h3>{escape(p["name"])}</h3><p class="small">{escape(p["role"])}</p><p class="cred">{escape(cred)}</p><p>{escape(p.get("summary", ""))}</p>{li}</article>')
    more = '<p class="mt-6"><a class="tlink" href="/about-us">Meet the team →</a></p>' if intro_link else ""
    return f'<section class="section" aria-labelledby="team-h"><div class="wrap"><div class="head"><h2 id="team-h">{heading}</h2></div><div class="team">{"".join(cards)}</div>{more}</div></section>'


def _png_size(src):
    import os, struct
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "img-" + src.rsplit("/", 1)[-1])
    with open(f, "rb") as fh:
        head = fh.read(24)
    return struct.unpack(">II", head[16:24])


def software_strip(data):
    """Deck: "Software we work in" strip. Names show as plain text until each vendor's partner terms are confirmed.
    Add an approved logo file path in data.json software_logos to swap a name for its official logo."""
    logos = data.get("software_logos", {})
    items = []
    for name in ["Xero", "Sage", "FreeAgent", "Hubdoc"]:
        src = logos.get(name)
        if src:
            w, h = _png_size(src)
            badge = w / h < 1.3                 # round marks (Xero, Hubdoc) need more height to read at the same visual size
            hh = 48 if badge else 32
            items.append(f'<li class="sw"><img class="{"badge" if badge else "mark"}" src="{escape(src)}" alt="{name} logo" width="{round(w * hh / h)}" height="{hh}" loading="lazy"></li>')
        else:
            items.append(f'<li class="sw sw--text">{name}</li>')
    return f'''<section class="section section--alt" id="software" aria-labelledby="sw-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="sw-h">Already on Xero, Sage, FreeAgent or Hubdoc? We start from your file.</h2></div>
    <div>
      <p class="sw-label">Software we work in</p>
      <ul class="sw-row" aria-label="Software we work in">{"".join(items)}</ul>
      <p class="lead mt-6">We work inside the software you already use, so nothing has to be rebuilt. Still on spreadsheets? We will set you up on the right one and move your records across.</p>
      <p class="mt-5"><a class="av-link" href="/services/bookkeeping">See how monthly bookkeeping works {ARROW}</a></p>
    </div>
  </div>
</section>'''


# ---------------------------------------------------------------- Home
def home(data):
    faqs = [
        ("How much will it cost?", "A fixed monthly fee, agreed in writing before we start. It depends on how many transactions you have, how many people you pay, and whether you are VAT registered. You will have the figure after your <a class='ilink' href='/contact'>review</a>."),
        ("Can I keep my current accountant for the year-end?", "Yes. Some owners use us for the monthly work and keep their current firm for the annual accounts. The scope will say who does what."),
        ("Which software do you work in?", "Xero, QuickBooks, Sage and FreeAgent. If you are on spreadsheets, we can <a class='ilink' href='/services/accounting-software'>set you up and move your records across</a>."),
        ("Do I need to be near Harrow?", "No. We work with businesses across the UK by video, phone and email. Our office in Harrow is there if you would rather meet in person."),
        ("How does switching work?", "We write to your current accountant for professional clearance, collect your records, and get authority to talk to HMRC for you. We time it around your next <a class='ilink' href='/services/payroll'>payroll</a> and <a class='ilink' href='/deadline-finder'>VAT dates</a> so nothing is missed."),
    ]
    facts = ["Aviteus Business Solutions Ltd", f'<a href="{CH_URL}" target="_blank" rel="noopener">Company number {COMPANY_NO}</a>', "Registered in England and Wales", f"Registered office: {REG_OFFICE}"]
    if data.get("aml_supervisor"): facts.append(escape(data["aml_supervisor"]))
    if data.get("pi_insurer"): facts.append(escape(data["pi_insurer"]))
    body = f'''
<section class="hero" aria-labelledby="h1">
  <div class="wrap hero-grid">
    <div>
      <p class="av-eyebrow">Bookkeeping · Payroll · VAT · Management accounts for UK businesses</p>
      <h1 id="h1">Know what's done. Know what's due. Every month.</h1>
      <p class="lead">We run the monthly finance work for UK owner-managed businesses. You get a written scope, one named manager, and a short report each month that shows what we finished and what is coming up next. No surprises in January.</p>
      <div class="hero-actions">{book_btn("hero")}<a class="tlink" href="#what-we-do">See what we do →</a></div>
      <p class="hero-note">Free. 20 minutes. By video or phone.</p>
      <p class="hero-cred">ICAEW, ACCA and CIMA qualified accountants · UK-wide service · Company no. 16694378</p>
    </div>
    <aside class="dd" aria-label="Sample Done and due report">
      <p class="dd-label">SAMPLE REPORT · Fictional company Sample Trading Ltd · November</p>
      <h3>Done this month</h3>
      <ul class="dd-done">
        <li>Bank accounts reconciled to 30 November</li>
        <li>41 supplier bills and 18 sales invoices posted</li>
        <li>Payroll run for 9 staff, paid on 28 November</li>
        <li>Pension contributions sent to the provider</li>
      </ul>
      <h3>Due next</h3>
      <ul>
        <li><span>VAT return, September to November quarter</span><span class="due">7 January</span></li>
        <li><span>Corporation tax payment, year to 31 March</span><span class="due">1 January</span></li>
      </ul>
      <h3>Waiting on you</h3>
      <ul>
        <li><span>3 receipts for card spending</span><span class="due">by 5 December</span></li>
      </ul>
      <p class="dd-more"><a class="tlink" href="/deadline-finder">Find your own dates →</a></p>
    </aside>
  </div>
</section>

<section class="section section--alt" aria-labelledby="familiar-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="familiar-h">Most owners call an accountant when something has already gone wrong</h2></div>
    <div>
      <ul class="lines">
        <li><a class='ilink' href='/services/bookkeeping'>The books are three months behind</a> and the <a class='ilink' href='/services/vat-tax'>VAT return is due in two weeks</a>.</li>
        <li><a class='ilink' href='/services/payroll'>Payroll only runs because you chase timesheets</a> on the 24th of every month.</li>
        <li>Your accountant appears once a year, with the accounts and an invoice, and you still don't know if you made money in March.</li>
      </ul>
      <p class="mt-6 lead">If any of that is you, the fix is not a better spreadsheet. It is someone doing the work every month, and telling you plainly where you stand.</p>
    </div>
  </div>
</section>

<section class="section" id="what-we-do" aria-labelledby="what-h">
  <div class="wrap">
    <div class="head"><h2 id="what-h">Three jobs, done properly, every month</h2>{PULSE}</div>
    <div class="rows">
      <div class="row"><h3>Bookkeeping and management accounts</h3><p>Your bank reconciled to the last day of the month. Bills and sales posted. A short pack showing profit, cash and what changed.</p><a class="av-link" href="/services/bookkeeping">Bookkeeping and management accounts {ARROW}</a></div>
      <div class="row"><h3>Payroll and pensions</h3><p>Staff paid on the right day. Payslips sent. RTI filed with HMRC. Pension contributions handled.</p><a class="av-link" href="/services/payroll">Payroll and pensions {ARROW}</a></div>
      <div class="row"><h3>VAT and year-end tax</h3><p>VAT returns under Making Tax Digital. Year-end accounts. Corporation tax. Your part flagged weeks ahead, not days.</p><a class="av-link" href="/services/vat-tax">VAT and year-end tax {ARROW}</a></div>
    </div>
    <p class="mt-5"><a class="tlink" href="/services">See all services and what we don't do →</a></p>
  </div>
</section>

<section class="section" aria-labelledby="how-h">
  <div class="wrap">
    <div class="head"><h2 id="how-h">From first call to first report in four steps</h2></div>
    <ol class="steps">
      <li><b>Review.</b> A free 20-minute call. We look at what is behind, what is due, and whether we are the right fit. Sometimes we are not, and we will say so.</li>
      <li><b>Scope.</b> We send a written scope: what we do, what you do, when, and the fixed monthly fee. Nothing starts until you agree it.</li>
      <li><b>Switch.</b> If you have an accountant now, we contact them for professional clearance and plan the move around your next <a class='ilink' href='/services/payroll'>payroll run</a> and <a class='ilink' href='/services/vat-tax'>VAT date</a>. You send one email.</li>
      <li><b>Monthly.</b> We do the work and send your "Done and due" report. You read it in two minutes.</li>
    </ol>
    <div class="mt-7">{book_btn("after_process")}</div>
  </div>
</section>
{software_strip(data)}

<section class="section" aria-labelledby="new-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="new-h">We're new. Here's why that works in your favour.</h2></div>
    <div>
      <p class="lead">Aviteus Business Solutions was set up in Harrow in September 2025. We will not pretend to have hundreds of clients. What we can offer is what bigger firms struggle to: senior people on your work, time to learn your business, and every reason to keep you.</p>
      <ul class="ticks mt-6">
        <li><b>A written scope before you pay.</b> You see exactly what is included and what is not.</li>
        <li><b>One named manager.</b> The same person every month, by email, phone or WhatsApp.</li>
        <li><b>A report you can read in two minutes.</b> What we finished, what is due, what we need from you.</li>
      </ul>
    </div>
  </div>
</section>
{team_block(data, "The people who will do your work", intro_link=True)}
<section class="section section--alt" aria-labelledby="roots-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="roots-h">Started by the team behind Aviteus Healthcare</h2></div>
    <div><p class="lead"><a class='ilink' href='/about-us'>Aviteus began in healthcare staffing</a>, supplying care and nursing staff across the UK. In that world a late payroll means a carer does not get paid on Friday. We brought the same standard to accounting: get the dull things right, on time, every time.</p>
    <p class="mt-5"><a class="tlink" href="/about-us#founder">Meet Vikas Pandey, our founder and CEO →</a></p></div>
  </div>
</section>

<section class="section section--alt" aria-labelledby="tools-h">
  <div class="wrap">
    <div class="head"><p class="av-eyebrow">Free · No sign-up</p><h2 id="tools-h">Free tools for UK business owners</h2></div>
    <div class="tool-grid">{"".join(f'<article class="tool-card"><h3><a href="{u}">{t}</a></h3><p>{d}</p><a class="av-link" href="{u}">{c} {ARROW}</a></article>' for u, t, d, c in TOOLS)}</div>
    <p class="mt-6"><a class="tlink" href="/tools">All free tools →</a></p>
  </div>
</section>

<section class="section" aria-labelledby="faq-h">
  <div class="wrap">
    <p class="facts" aria-label="Company details">{"<span>·</span>".join(f"<span>{f}</span>" for f in facts)}</p>
    <div class="split mt-8">
      <div class="head" style="margin:0"><h2 id="faq-h">Questions owners ask first</h2></div>
      {faq_html(faqs)}
    </div>
  </div>
</section>
{close_band("Bring one problem. Leave with a plan.", "Twenty minutes is enough to tell you what is behind, what is due next, and whether we can help. If we can't, we'll tell you who might.")}
'''
    return page(path="/", title="Bookkeeping, Payroll and VAT for UK Businesses | Aviteus",
                description="Monthly bookkeeping, payroll and VAT for UK owner-managed businesses. A written scope, one named manager, and a short report on what is done and due.",
                h_active="home", body_html=body, ld=[{"@type": "WebPage", "@id": f"{SITE}/#webpage", "url": f"{SITE}/", "name": "Know what's done. Know what's due. Every month.", "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": f"{SITE}/#business"}, "inLanguage": "en-GB"}, faq_ld(faqs)],
                data=data, page_type="home")


def service_ld(name, path, desc, service_type):
    return {"@type": "Service", "@id": f"{SITE}{path}#service", "name": name, "serviceType": service_type, "description": desc, "url": f"{SITE}{path}",
            "provider": {"@id": f"{SITE}/#business"}, "areaServed": {"@type": "Country", "name": "United Kingdom"}, "audience": {"@type": "BusinessAudience", "audienceType": "UK owner-managed businesses"}}


# ---------------------------------------------------------------- Bookkeeping
def bookkeeping(data):
    faqs = [
        ("How much does bookkeeping cost for a small business?", "It depends on volume, not on a price list. A business with 80 transactions a month and one bank account costs less than one with 600 transactions and four accounts. We fix the monthly fee in writing after a 20-minute review, so you know the figure before you commit."),
        ("What is the difference between bookkeeping and management accounts?", "Bookkeeping is recording and matching every transaction. Management accounts are the short report built from those records: profit, cash and what changed. Good management accounts need up-to-date books first."),
        ("Will I still have access to my own books?", "Yes, always. The software stays in your name. We work inside it as your adviser, and you can remove our access at any time."),
        ("Do you need my paperwork in a particular format?", "No. Photos of receipts, forwarded emails and PDFs all work. We will show you the quickest route for your business."),
        ("Can you take over from my current bookkeeper part way through the year?", "Yes. We pick up from the last reconciled month and check the opening balances before posting anything new."),
    ]
    pack_day = data.get("management_pack_day")
    pack_when = f"By {escape(str(pack_day))} of the following month" if pack_day else ""
    sample_link = '<a class="tlink" href="#sample">See a sample monthly pack ↓</a>' if data.get("sample_pack_ready") else ""
    sample = ""
    if data.get("sample_pack_ready"):
        sample = '''<section class="section" id="sample" aria-labelledby="sample-h"><div class="wrap read"><h2 id="sample-h">See what a monthly pack looks like</h2><p class="mt-4">This is a sample for a fictional company, Sample Trading Ltd. Your pack will use your own figures and the same simple layout: three pages, no jargon, and notes that tell you why the numbers moved.</p></div></section>'''
    crumbs = [("Home", "/"), ("Services", "/services"), ("Bookkeeping", "/services/bookkeeping")]
    body = f'''
<section class="hero hero--simple" aria-labelledby="h1">
  <div class="wrap read">
    {crumbs_html(crumbs)}
    <h1 id="h1">Bookkeeping and management accounts, done every month</h1>
    <p class="lead">Your bank reconciled to the last day of the month. Every bill and sale posted. A short pack that shows profit, cash and what changed, in plain English. All on a fixed fee you agree in writing before we start.</p>
    <div class="hero-actions">{book_btn("hero")}{sample_link}</div>
  </div>
</section>

<section class="section section--alt" aria-labelledby="answer-h">
  <div class="wrap read">
    <h2 id="answer-h">What outsourced bookkeeping means with Aviteus</h2>
    <p class="mt-4 lead">Outsourced bookkeeping means a qualified team outside your business keeps your accounting records up to date for you. With Aviteus, that happens every month, in your own software, to a written scope. You keep full access to your books at all times. We do the posting, matching and checking. You send us what only you have: receipts, a few answers, and approval of anything unusual.</p>
  </div>
</section>

<section class="section" id="monthly" aria-labelledby="get-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="get-h">What lands in your inbox each month</h2></div>
    <ul class="ticks">
      <li><b>Reconciled bank and card accounts.</b> Every line matched to a bill, a sale or a receipt, to the last day of the month.</li>
      <li><b>Bills and sales posted.</b> Supplier bills, sales invoices and credit notes recorded and coded correctly for <a class='ilink' href='/services/vat-tax'>VAT</a>.</li>
      <li><b>A list of what is missing.</b> Short and specific: "3 card payments need receipts", not "please send paperwork".</li>
      <li><b>Your monthly management pack.</b> Profit and loss for the month and year to date, balance sheet, cash position, and one page of notes on what moved and why.</li>
      <li><b>Your "Done and due" report.</b> What we finished, what is due next, and what we need from you, with dates.</li>
    </ul>
  </div>
</section>

<section class="section section--alt" id="scope" aria-labelledby="scope-h">
  <div class="wrap">
    <div class="head"><h2 id="scope-h">Who does what, and when</h2></div>
    <table class="table table--stack">
      <thead><tr><th scope="col">Task</th><th scope="col">We do</th><th scope="col">You do</th><th scope="col">When</th></tr></thead>
      <tbody>
        <tr><td>Bank feeds and card accounts</td><td data-label="We do">Reconcile every line</td><td data-label="You do">Keep the bank feed connected</td><td data-label="When" class="when">Monthly</td></tr>
        <tr><td>Supplier bills</td><td data-label="We do">Post and code them</td><td data-label="You do">Forward bills, or snap them in the app</td><td data-label="When" class="when">As they arrive</td></tr>
        <tr><td>Sales invoices</td><td data-label="We do">Post and match payments</td><td data-label="You do">Raise invoices, or let us know who owes what</td><td data-label="When" class="when">As issued</td></tr>
        <tr><td>Receipts and queries</td><td data-label="We do">Send one clear list</td><td data-label="You do">Answer it</td><td data-label="When" class="when">Once a month</td></tr>
        <tr><td>Management pack</td><td data-label="We do">Prepare and explain it</td><td data-label="You do">Read it, ask anything</td><td{' data-label="When"' if pack_when else ''} class="when">{pack_when}</td></tr>
        <tr><td>Year-end</td><td data-label="We do">Hand clean books to your accountant, or to <a class='ilink' href='/services/vat-tax'>our year-end team</a></td><td data-label="You do">Approve the accounts</td><td data-label="When" class="when">Once a year</td></tr>
      </tbody>
    </table>
    <p class="note mt-4">The table in your scope will be specific to your business. This is the starting point.</p>
    {related([("We can run payroll from the same books", "/services/payroll"), ("VAT returns and Making Tax Digital", "/services/vat-tax"), ("Who will do the work", "/about-us"), ("Business advisory: forecasts and budgets", "/services/business-advisory"), ("Virtual CFO", "/services/virtual-cfo"), ("All services", "/services"), ("Blog: bookkeeping vs management accounts", "/blog/bookkeeping-vs-management-accounts"), ("Blog: catch up your books", "/blog/catch-up-bookkeeping")])}
    <div class="mt-7">{book_btn("after_scope")}</div>
  </div>
</section>
{sample}
<section class="section" id="catch-up" aria-labelledby="behind-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="behind-h">Books three months behind? Start with a catch-up.</h2></div>
    <p class="lead">Most new clients are behind when they call. That is normal. We bring the records up to date first, as a separate, fixed-price piece of work, then move you onto the monthly routine. You will know the catch-up fee and how long it will take before we start.</p>
  </div>
</section>

<section class="section section--alt" id="software" aria-labelledby="soft-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="soft-h">Your software, or we will set it up</h2></div>
    <p class="lead">We work in Xero, QuickBooks, Sage and FreeAgent. If your records live in spreadsheets or a shoebox, we will <a class='ilink' href='/services/accounting-software'>set up the software</a>, connect your bank, and show you the two or three things you need to do each month. Nothing more.</p>
  </div>
</section>

<section class="section" aria-labelledby="suits-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="suits-h">Who this is for, and who it isn't</h2></div>
    <div>
      <p class="lead">This suits you if you run a UK business with regular sales, supplier bills and a few staff, and you want to see your numbers every month without doing the posting yourself.</p>
      <div class="quiet mt-6"><p>It may not suit you if you have fewer than 20 transactions a month and no staff. Good software and a quarterly check might be enough. We will tell you that on the call.</p></div>
    </div>
  </div>
</section>

<section class="section section--alt" aria-labelledby="fee-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="fee-h">How the fee works</h2></div>
    <p class="lead">One fixed monthly fee, agreed in writing before any work starts. It is based on how many transactions you have, how many bank and card accounts we reconcile, and whether you need management accounts. Catch-up work and software set-up are quoted separately, so you can see each cost on its own.</p>
  </div>
</section>

<section class="section" aria-labelledby="faq-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="faq-h">Bookkeeping questions</h2></div>
    {faq_html(faqs)}
  </div>
</section>
{close_band("Find out where your books really stand", "In 20 minutes we will tell you how far behind you are, what it will take to catch up, and what a monthly fee would look like.", "bookkeeping")}
'''
    return page(path="/services/bookkeeping", title="Outsourced Bookkeeping and Management Accounts UK | Aviteus",
                description="Monthly bookkeeping for UK businesses: bank reconciled, bills and sales posted, and a short management pack. Written scope, fixed fee, one manager.",
                h_active="bookkeeping", body_html=body, service="bookkeeping", page_type="service",
                ld=[service_ld("Bookkeeping and management accounts", "/services/bookkeeping", "Monthly outsourced bookkeeping and management accounts for UK owner-managed businesses, in your own software, to a written scope and a fixed monthly fee.", "Bookkeeping"), breadcrumb_ld(crumbs), faq_ld(faqs)], data=data)


# ---------------------------------------------------------------- Contact
def contact(data):
    services = ["Bookkeeping and management accounts", "Payroll and pensions", "VAT and year-end tax", "Switching from my current accountant", "Something else, or not sure yet"]
    opts = "".join(f'<option value="{escape(s)}">{escape(s)}</option>' for s in services)
    body = f'''
<section class="hero" aria-labelledby="h1">
  <div class="wrap contact-grid">
    <div class="c-intro">
      <h1 id="h1">Book your free 20-minute review</h1>
      <p class="lead">Bring one problem. Books behind, payroll that eats your month, a VAT deadline you are worried about. We will look at it with you and give you a straight answer.</p>
    </div>

    <div class="c-form">
      <div class="form-card">
        <div class="err-summary" id="err-summary" tabindex="-1" role="alert"><h2>There is 1 problem with your enquiry</h2><ul></ul></div>
        <div class="form-status" id="form-status" role="status" aria-live="polite"></div>
        <form class="form" id="enquiry-form" novalidate data-version="1" aria-labelledby="form-h">
          <div><h2 id="form-h">Tell us what you need help with</h2><p class="small mt-4">Share a little about your business and what you need, so we can prepare for your review.</p></div>
          <div class="field" id="f-name-wrap"><label for="f-name">Full name</label><input class="av-input" id="f-name" name="name" autocomplete="name" required maxlength="100" aria-describedby="f-name-err"><p class="err" id="f-name-err"></p></div>
          <div class="field" id="f-email-wrap"><label for="f-email">Email</label><input class="av-input" id="f-email" name="email" type="email" autocomplete="email" required aria-describedby="f-email-err"><p class="err" id="f-email-err"></p></div>
          <div class="field"><label for="f-company">Company or website (optional)</label><input class="av-input" id="f-company" name="company" autocomplete="organization" maxlength="200"></div>
          <div class="field" id="f-service-wrap"><label for="f-service">Which service is this about?</label><select class="av-input" id="f-service" name="service" required aria-describedby="f-service-err"><option value="">Choose one</option>{opts}</select><p class="hint">Compare them first: <a class='ilink' href='/services'>see all services</a>.</p><p class="err" id="f-service-err"></p></div>
          <div class="field" id="f-message-wrap"><label for="f-message">What would you like help with?</label><p class="hint" id="f-message-hint">For example: our books are three months behind, or we want to move payroll before the new tax year.</p><textarea class="av-input" id="f-message" name="message" rows="5" required maxlength="2000" aria-describedby="f-message-hint f-message-err"></textarea><p class="err" id="f-message-err"></p></div>
          <fieldset class="field"><legend>How should we reply?</legend><div class="choices">
            <label class="choice"><input type="radio" name="reply_method" value="email" checked><span>Email</span></label>
            <label class="choice"><input type="radio" name="reply_method" value="phone"><span>Phone call</span></label>
            <label class="choice"><input type="radio" name="reply_method" value="whatsapp"><span>WhatsApp</span></label>
          </div></fieldset>
          <div class="field" id="f-phone-wrap" hidden><label for="f-phone">Phone or WhatsApp number</label><p class="hint" id="f-phone-hint">Include the country code if it is not a UK number.</p><input class="av-input" id="f-phone" name="phone" type="tel" autocomplete="tel" aria-describedby="f-phone-hint f-phone-err"><p class="err" id="f-phone-err"></p></div>
          <label class="check"><input type="checkbox" name="newsletter" value="yes"><span>Send me occasional emails about UK tax deadlines and changes. You can unsubscribe at any time.</span></label>
          <div class="hp" aria-hidden="true"><label for="f-website">Leave this empty</label><input id="f-website" name="website" tabindex="-1" autocomplete="off"></div>
          <div class="cf-turnstile" data-sitekey=""></div>
          <p class="privacy">We use these details only to reply to your enquiry. Read our <a class="tlink" href="/privacy-policy">privacy notice</a>.</p>
          <button class="av-btn av-btn--ember" type="submit">Send enquiry</button>
          <p class="send-note">Free. No obligation. We reply within one business day.</p>
          <p class="small">Prefer to message? <a class="tlink" href="{wa()}" target="_blank" rel="noopener" data-placement="under_form">Chat on WhatsApp</a></p>
        </form>
      </div>
    </div>

    <div class="c-rest">
      <h2>What happens in the 20 minutes</h2>
      <ol class="steps steps--v mt-5">
        <li><b>We listen.</b> You tell us what is going on and what is bothering you most.</li>
        <li><b>We look.</b> If you can, share your software screen or last VAT return. If not, we work from what you tell us.</li>
        <li><b>We tell you three things:</b> what is behind, what is due next, and whether Aviteus is the right fit.</li>
      </ol>
      <h2 class="mt-7">What you leave with</h2>
      <p class="mt-4">A clear next step, even if it is not us. If we are a fit, we send a short written note with the scope and fixed monthly fee to consider. No pressure, no chasing.</p>
      <h2 class="mt-7">Useful to have ready (not essential)</h2>
      <ul class="ticks mt-5">
        <li>Your accounting software login, or your last set of accounts</li>
        <li>Your <a class='ilink' href='/deadline-finder'>VAT and payroll dates</a>, if you know them</li>
        <li>The name of your current accountant, if you have one</li>
      </ul>
      <p class="mt-6"><a class="tlink" href="/about-us#founder">Meet our founder first</a></p>
    </div>
  </div>
</section>

<section class="section section--alt" aria-labelledby="reach-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="reach-h">Other ways to reach us</h2></div>
    <div>
      <table class="facts-table">
        <tr><th scope="row">Phone</th><td><a class="tlink" href="{PHONE_TEL}" data-placement="contact_table">{PHONE}</a> · Monday to Friday, 9am to 5pm · Saturday by appointment · Sunday closed</td></tr>
        <tr><th scope="row">WhatsApp</th><td>{WA_DISPLAY} · <a class="tlink" href="{wa()}" target="_blank" rel="noopener" data-placement="contact_table">Chat on WhatsApp</a></td></tr>
        <tr><th scope="row">Email</th><td><a class="tlink" href="mailto:{EMAIL}">{EMAIL}</a></td></tr>
        <tr><th scope="row">Office</th><td>{ADDRESS}. Meetings online or in person, by appointment · <a class="tlink" href="https://www.google.com/maps/search/?api=1&amp;query=Alpha+House+296+Kenton+Road+Harrow+HA3+8DD" target="_blank" rel="noopener">Open in Google Maps</a></td></tr>
      </table>
      <p class="mt-5">We respond within one business day and can meet online or in person. UK-wide coverage using secure cloud systems: you do not need to be near Harrow.</p>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="before-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="before-h">Before you book</h2></div>
    {faq_html([("Is the review really free?", "Yes. It is 20 minutes, and there is nothing to sign."), ("Will you try to sell me something?", "We will tell you whether we can help. If we can, you get a written scope and fee to think about in your own time."), ("Can I talk to you without my current accountant knowing?", "Yes. We only contact them if you decide to switch and ask us to.")])}
  </div>
</section>
'''
    css = '''<style>
.contact-grid { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); grid-template-areas: "intro form" "rest form"; grid-template-rows: auto 1fr; gap: var(--space-6) var(--space-8); align-items: start; }
.c-intro { grid-area: intro; } .c-form { grid-area: form; position: sticky; top: 100px; } .c-rest { grid-area: rest; }
.c-rest h2 { font-size: 26px; line-height: 32px; }
@media (max-width: 960px) { .contact-grid { grid-template-columns: 1fr; grid-template-areas: "intro" "form" "rest"; } .c-form { position: static; } }
.steps--v { grid-template-columns: 1fr; gap: var(--space-5); }
.steps--v::before { left: 19px; right: auto; top: 0; bottom: 0; width: 1px; height: auto; }
.steps--v li { padding-left: 64px; } .steps--v li::before { position: absolute; left: 0; top: 0; margin: 0; }
.steps--v b { display: inline; font-family: var(--font-text); font-size: inherit; }
</style>'''
    return page(path="/contact", title="Book a Free 20-Minute Review | Aviteus Business Solutions",
                description="Tell us what you need help with. In 20 minutes we will show you what is behind, what is due next, and whether Aviteus is the right fit.",
                h_active="contact", body_html=css + body, sticky=False, page_type="contact",
                ld=[{"@type": "ContactPage", "url": f"{SITE}/contact", "name": "Book your free 20-minute review", "about": {"@id": f"{SITE}/#business"}, "inLanguage": "en-GB"}, breadcrumb_ld([("Home", "/"), ("Book a review", "/contact")])], data=data)


# ---------------------------------------------------------------- Payroll
def payroll(data):
    faqs = [
        ("How much does outsourced payroll cost for a small business?", "It depends mainly on how many people you pay and how often you run payroll. We agree a fixed monthly fee in writing after a 20-minute review, so you know the cost before you start."),
        ("What is RTI?", "Real Time Information is how employers report pay, tax and National Insurance to HMRC. A report must be sent on or before each payday. We send it for you."),
        ("Do you pay my staff, or do I?", "You do, from your own bank account. We prepare the payment file and tell you the totals. Your money never passes through us."),
        ("What if I send changes after the cut-off?", "Tell us anyway. We will do our best to include them. If it is too late, we will add them to the next run and tell you exactly what that means for the employee."),
        ("Do you handle workplace pensions?", "Yes. We assess each employee, enrol those who qualify, send contributions to your pension provider and handle re-enrolment every three years."),
    ]
    cut = data.get("payroll_cutoff_day")
    cut_txt = escape(str(cut)) if cut else "Cut-off day"
    crumbs = [("Home", "/"), ("Services", "/services"), ("Payroll", "/services/payroll")]
    you, us = '<span class="who who--you">You</span>', '<span class="who who--us">Aviteus</span>'
    body = f'''
<section class="hero hero--simple" aria-labelledby="h1">
  <div class="wrap read">
    {crumbs_html(crumbs)}
    <h1 id="h1">Payroll for small businesses, run on time every month</h1>
    <p class="lead">You send the changes. We do the rest. Staff paid on the right day, payslips in their inbox, HMRC told on time, pension contributions sent. You stop being the payroll department.</p>
    <div class="hero-actions">{book_btn("hero")}<a class="tlink" href="#payroll-month">See how a payroll month works ↓</a></div>
  </div>
</section>

<section class="section section--alt" aria-labelledby="answer-h">
  <div class="wrap read">
    <h2 id="answer-h">What a managed payroll service includes</h2>
    <p class="mt-4 lead">A managed payroll service means a person runs your payroll for you, start to finish. With Aviteus that covers calculating pay, tax and National Insurance, sending payslips, reporting each pay run to HMRC through Real Time Information (RTI), and handling workplace pension contributions. You approve the figures before anyone is paid.</p>
  </div>
</section>

<section class="section" id="payroll-month" aria-labelledby="month-h">
  <div class="wrap">
    <div class="head"><h2 id="month-h">One payroll month, start to finish</h2></div>
    <table class="table table--stack">
      <thead><tr><th scope="col">When</th><th scope="col">What happens</th><th scope="col">Who</th></tr></thead>
      <tbody>
        <tr><td class="when">{cut_txt}</td><td data-label="What happens">You send starters, leavers, hours, overtime, bonuses and sickness. One message, one form</td><td data-label="Who">{you}</td></tr>
        <tr><td class="when">Next working day</td><td data-label="What happens">We calculate pay, tax, NI, pensions and statutory pay, and send you a summary to approve</td><td data-label="Who">{us}</td></tr>
        <tr><td class="when">You approve</td><td data-label="What happens">One reply: "approved", or the changes you want</td><td data-label="Who">{you}</td></tr>
        <tr><td class="when">Before payday</td><td data-label="What happens">Payslips go to staff. The pay run is reported to HMRC through RTI</td><td data-label="Who">{us}</td></tr>
        <tr><td class="when">Payday</td><td data-label="What happens">You pay staff from your bank, using the file we prepare</td><td data-label="Who">{you}</td></tr>
        <tr><td class="when date">By the 22nd of the next month</td><td data-label="What happens">You pay PAYE and NI to HMRC. We tell you the exact amount</td><td data-label="Who"><span class="who who--you">You, with our reminder</span></td></tr>
      </tbody>
    </table>
    <p class="lead mt-5">The same routine every month. No guessing, no last-minute calls.</p>
    {related([("Monthly bookkeeping", "/services/bookkeeping"), ("Who will run your payroll", "/about-us"), ("VAT and year-end tax", "/services/vat-tax"), ("Find your payroll dates", "/deadline-finder"), ("Directors' Self Assessment", "/services/self-assessment"), ("Payroll for healthcare and care", "/industries#healthcare"), ("All services", "/services"), ("Blog: the employer payroll checklist", "/blog/small-business-payroll-checklist")])}
    <div class="mt-7">{book_btn("after_table")}</div>
  </div>
</section>

<section class="section section--alt" id="handle" aria-labelledby="cover-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="cover-h">What we handle</h2></div>
    <ul class="ticks">
      <li><b>Weekly, fortnightly, four-weekly or monthly pay runs</b></li>
      <li><b>Payslips</b> sent securely to each employee</li>
      <li><b>RTI submissions</b> to HMRC for every pay run</li>
      <li><b>Starters and leavers</b>, including P45s</li>
      <li><b>Statutory pay:</b> sick pay, maternity, paternity and shared parental pay</li>
      <li><b>Workplace pensions:</b> assessing staff, enrolling them, sending contributions, and re-enrolment every three years</li>
      <li><b>Year-end:</b> <a class='ilink' href='/deadline-finder'>P60s for staff by 31 May, P11D benefit forms by 6 July</a> where needed</li>
      <li><b>Directors' payroll</b>, including salary set at a <a class='ilink' href='/services/vat-tax'>tax-efficient level</a> agreed with you</li>
    </ul>
  </div>
</section>

<section class="section" id="switch" aria-labelledby="switch-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="switch-h">Moving payroll part way through the year</h2></div>
    <p class="lead">You can move payroll to us at any point in the tax year. We need your PAYE reference, your Accounts Office reference, and the year-to-date figures for each employee from your current provider. We check those figures, run a parallel month if you want one, and take over from the next pay run. Your staff should notice nothing except the new payslip layout.</p>
  </div>
</section>

<section class="section section--alt" aria-labelledby="suits-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="suits-h">Who this is for, and who it isn't</h2></div>
    <div>
      <p class="lead">This suits you if you pay between 2 and 50 people and you are tired of being the person who chases timesheets and fixes tax codes.</p>
      <div class="quiet mt-6"><p>If you pay one director a fixed salary and nothing else changes, payroll software may be enough on its own. We will say so.</p></div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="fee-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="fee-h">How the fee works</h2></div>
    <p class="lead">A fixed monthly fee based on how many people you pay and how often. Pension administration is included. Year-end forms are included. Anything unusual, such as a large redundancy round, is quoted before we start it.</p>
  </div>
</section>

<section class="section section--alt" aria-labelledby="faq-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="faq-h">Payroll questions</h2></div>
    {faq_html(faqs)}
  </div>
</section>
{close_band("Get your 24th of the month back", "Twenty minutes is enough to see how your payroll runs today and what would change with us.", "payroll")}
'''
    return page(path="/services/payroll", title="Payroll Services for Small Businesses UK | Aviteus",
                description="Managed payroll for UK small businesses. Staff paid on time, payslips sent, RTI filed with HMRC and pensions handled, to a fixed monthly routine.",
                h_active="payroll", body_html=body, service="payroll", page_type="service",
                ld=[service_ld("Payroll and pensions", "/services/payroll", "Managed payroll for UK small businesses: pay, tax and National Insurance calculated, payslips sent, RTI filed with HMRC and workplace pensions handled.", "Payroll"), breadcrumb_ld(crumbs), faq_ld(faqs)], data=data)


# ---------------------------------------------------------------- VAT and tax
def vat(data):
    faqs = [
        ("When is my VAT return due?", "One calendar month and seven days after the end of your VAT period. For a quarter ending 30 November, both the return and the payment are due by 7 January."),
        ("When do I have to register for VAT?", "When your VAT-taxable turnover goes over the registration threshold in any rolling 12 months, or you expect it to in the next 30 days. We check your turnover each month, so you hear about it early."),
        ("Can you take over my VAT returns mid-year?", "Yes. We start from your next VAT period and check the last return filed before we submit anything."),
        ("Do you deal with HMRC for me?", "Yes, once you authorise us as your agent. HMRC letters and calls about your VAT or corporation tax come to us, and we tell you what they mean."),
        ("I'm a sole trader. Does Making Tax Digital for Income Tax affect me?", "It might. It started in April 2026 for sole traders and landlords above an income threshold, and the threshold falls in later years. Bring your figures to a review and we will tell you if and when it applies."),
    ]
    crumbs = [("Home", "/"), ("Services", "/services"), ("VAT and tax", "/services/vat-tax")]
    body = f'''
<section class="hero hero--simple" aria-labelledby="h1">
  <div class="wrap read">
    {crumbs_html(crumbs)}
    <h1 id="h1">VAT, year-end accounts and corporation tax, with no last-minute panic</h1>
    <p class="lead">HMRC deadlines do not move. So we plan backwards from them. You will know every date that applies to your business, what we need from you, and when, usually weeks before it matters.</p>
    <div class="hero-actions">{book_btn("hero")}<a class="tlink" href="#deadlines">See the deadlines ↓</a></div>
  </div>
</section>

<section class="section section--alt" id="file" aria-labelledby="answer-h">
  <div class="wrap read">
    <h2 id="answer-h">What we file for you</h2>
    <p class="mt-4 lead">We prepare and submit VAT returns through Making Tax Digital software, prepare your year-end accounts, file them with Companies House, and prepare and file your company tax return (CT600) with HMRC. We also tell you how much corporation tax to pay and by when. You review and approve everything before it is sent.</p>
  </div>
</section>

<section class="section" id="deadlines" aria-labelledby="dl-h">
  <div class="wrap">
    <div class="head"><h2 id="dl-h">The deadlines that apply to most UK limited companies</h2></div>
    <table class="table table--stack">
      <thead><tr><th scope="col">What</th><th scope="col">Deadline</th><th scope="col">What we need from you</th></tr></thead>
      <tbody>
        <tr><td>VAT return and payment</td><td data-label="Deadline" class="date">1 month and 7 days after the end of each VAT period</td><td data-label="What we need from you">Sales and purchase records for the period. If we do your books, nothing extra</td></tr>
        <tr><td>Annual accounts to Companies House</td><td data-label="Deadline" class="date">9 months after your company's year end</td><td data-label="What we need from you">Answers to our year-end questions and your approval</td></tr>
        <tr><td>Corporation tax payment</td><td data-label="Deadline" class="date">9 months and 1 day after your year end</td><td data-label="What we need from you">Approval of the tax figure. You pay HMRC directly</td></tr>
        <tr><td>Company tax return (CT600) to HMRC</td><td data-label="Deadline" class="date">12 months after your year end</td><td data-label="What we need from you">Approval of the return</td></tr>
        <tr><td>Confirmation statement</td><td data-label="Deadline" class="date">Once a year, within 14 days of your review date</td><td data-label="What we need from you">Confirmation that company details have not changed</td></tr>
      </tbody>
    </table>
    <p class="callout mt-5">Note the order. Corporation tax is <b>paid</b> three months before the return is <b>due</b>. Many owners find that out the hard way.</p>
    {related([("Find your own dates with the free deadline finder", "/deadline-finder"), ("Monthly bookkeeping", "/services/bookkeeping"), ("Payroll", "/services/payroll"), ("Who will do the work", "/about-us"), ("Self Assessment tax returns", "/services/self-assessment"), ("Company formation and compliance", "/services/company-formation"), ("Construction and CIS", "/industries#construction"), ("Virtual CFO", "/services/virtual-cfo"), ("All services", "/services"), ("Blog: VAT and Making Tax Digital", "/blog/vat-returns-making-tax-digital"), ("Blog: limited company deadlines", "/blog/limited-company-deadlines-uk")])}
    <div class="mt-7">{book_btn("after_table")}</div>
  </div>
</section>

<section class="section section--alt" aria-labelledby="plan-h">
  <div class="wrap">
    <div class="head"><h2 id="plan-h">How we stay ahead of the dates</h2></div>
    <ol class="steps">
      <li><b>On day one</b> we put <a class='ilink' href='/deadline-finder'>every deadline for your company into one calendar</a>, and you get a copy.</li>
      <li><b>Each month</b> your "Done and due" report shows the next two deadlines and anything we need from you.</li>
      <li><b>Before each VAT return</b> we send the draft figures for approval, with any unusual items explained in a sentence.</li>
      <li><b>At year-end</b> we send one list of questions, not a drip of emails, and a draft tax figure early enough for you to plan the payment.</li>
    </ol>
  </div>
</section>

<section class="section" id="tax-planning" aria-labelledby="tp-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="tp-h">Tax planning</h2></div>
    <div><p class="lead">We file on time, reduce errors and plan legally to lower what you owe. That means using the reliefs and allowances your business is entitled to, timing big purchases sensibly, and setting directors' pay at a tax-efficient level agreed with you. Planning happens before the year end, not after it.</p>
    <p class="mt-4">Directors' own tax is covered too: see <a class='ilink' href='/services/self-assessment'>Self Assessment tax returns</a>.</p></div>
  </div>
</section>

<section class="section section--alt" id="audit-support" aria-labelledby="as-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="as-h">Audit support</h2></div>
    <p class="lead">If your company needs an audit, or HMRC opens an enquiry, we prepare the records, answer the questions and support you through it. Statutory audits themselves are carried out by a registered audit firm, and we work alongside them.</p>
  </div>
</section>

<section class="section" id="mtd" aria-labelledby="mtd-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="mtd-h">Making Tax Digital, in plain terms</h2></div>
    <p class="lead">Every VAT-registered business must keep digital records and submit VAT returns through compatible software. If you still use spreadsheets, we can connect them through approved bridging software, or <a class='ilink' href='/services/accounting-software'>move you to Xero, QuickBooks, Sage or FreeAgent</a>. Sole traders and landlords now face a similar rule for income tax, phased in by income level from April 2026.</p>
  </div>
</section>

<section class="section section--alt" aria-labelledby="suits-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="suits-h">Who this is for</h2></div>
    <p class="lead">UK limited companies that are VAT registered, or close to the registration threshold, and want returns and year-end handled by the same team that <a class='ilink' href='/services/bookkeeping'>sees their books each month</a>. If you want year-end only and do your own books, we can do that too. Tell us on the call.</p>
  </div>
</section>

<section class="section" aria-labelledby="faq-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="faq-h">VAT and tax questions</h2></div>
    {faq_html(faqs)}
  </div>
</section>
{close_band("Leave one call knowing your next three deadlines", "Book a 20-minute review and we will list the dates that apply to your business, and what you need to do before each one.", "vat")}
'''
    return page(path="/services/vat-tax", title="VAT Returns, Year-End Accounts and Corporation Tax | Aviteus",
                description="VAT returns under Making Tax Digital, year-end accounts and corporation tax for UK companies. Every deadline in one place, with your part flagged early.",
                h_active="vat", body_html=body, service="vat", page_type="service",
                ld=[service_ld("VAT and year-end tax", "/services/vat-tax", "VAT returns under Making Tax Digital, year-end accounts filed with Companies House, and corporation tax returns (CT600) for UK limited companies.", "Tax preparation"), breadcrumb_ld(crumbs), faq_ld(faqs)], data=data)


# ---------------------------------------------------------------- About
def founder_block(data):
    f = data.get("founder") or {}
    if not f.get("name"):
        return ""
    if f.get("photo"):
        portrait = f'<img class="founder-photo" src="{escape(f["photo"])}" alt="{escape(f["name"])}, {escape(f.get("role", ""))}" width="200" height="200" loading="lazy">'
    else:
        portrait = '<span class="founder-photo founder-initials" aria-hidden="true">VP</span>'
    li = f'<a class="tlink" href="{escape(f["linkedin"])}" target="_blank" rel="noopener">View Vikas on LinkedIn</a>' if f.get("linkedin") else ""
    return f'''<section class="section founder" id="founder" aria-labelledby="founder-h">
  <div class="wrap founder-grid">
    <div class="founder-card">
      {portrait}
      <div><p class="founder-name">{escape(f["name"])}</p><p class="founder-role">{escape(f.get("role", ""))}</p></div>
      {li}
    </div>
    <div class="founder-letter">
      <p class="av-eyebrow">About the founder and CEO</p>
      <h2 id="founder-h" class="mt-4">Meet Vikas Pandey</h2>
      <p class="lead mt-5">Handing over your books, payroll or client work takes trust. I don’t expect you to hand over everything on day one. I’d rather start with one clearly defined piece of work and give you the chance to see how we deliver.</p>
      <p>I lead Aviteus Business Solutions from Harrow, London. We help UK businesses with bookkeeping, payroll, VAT, year-end accounts and tax. We also give accountancy practices extra capacity for recurring work such as bookkeeping and reconciliations, so their teams have more time to advise clients.</p>
      <p>I also lead <a class="ilink" href="https://www.aviteushealthcare.co.uk" target="_blank" rel="noopener">Aviteus Healthcare</a>, a separate UK healthcare staffing business established in 2021. Working with care providers has shaped how I lead: get the details right, raise issues early and follow through on what you’ve agreed. Those are the same standards I expect at Aviteus Business Solutions.</p>
      <p>Before we start, we’ll agree on what we’ll handle, what it will cost and when you can expect it back. You can then judge us on the work itself and how we communicate along the way. If it works for your business, we can take on more. If you only need help with that one task, that’s fine too.</p>
      <p class="founder-sign">Vikas Pandey</p>
      <div class="mt-6">{book_btn("founder", "Discuss your accounting needs")}</div>
    </div>
  </div>
</section>'''


# The deck's line names the team, so it shows only once team members are added in data.json.
ABOUT_INTRO_TEAM = "You are about to trust someone with your bank feeds, your payroll and your tax. You should know who they are. Here they are, with the details you can check."
ABOUT_INTRO_NO_TEAM = "You are about to trust someone with your bank feeds, your payroll and your tax. You should be able to check who we are. Here is our story, how we work, and the company details you can verify yourself."


def _has_team(data):
    return any(p.get("consent") and p.get("name") and p.get("role") for p in data.get("team", []))


ABOUT_FAQS = [  # reworked from the live About page FAQ
    ("What services does Aviteus Business Solutions provide?", "Bookkeeping and management accounts, payroll and pensions, VAT returns, year-end accounts and corporation tax, tax planning, Self Assessment, business advisory, Virtual CFO, audit support, company formation and accounting software set-up. We also have specialist knowledge of <a class='ilink' href='/industries'>healthcare, construction and e-commerce</a>."),
    ("Do you support Making Tax Digital?", "Yes. We use cloud accounting software such as Xero, QuickBooks and Sage, so your business meets HMRC's digital rules for VAT and other tax submissions."),
    ("How quickly do you respond to queries?", "Each client has a dedicated account manager. We respond within one business day, and urgent matters come first."),
    ("What makes Aviteus different from other accountants?", "A qualified team (ICAEW, ACCA and CIMA), modern cloud tools and fixed fees agreed in writing. We give advice before problems arrive, not just compliance after them, and we build long-term working relationships around your goals."),
    ("Can you help with starting and growing a business?", "Yes. We support businesses at every stage: <a class='ilink' href='/services/company-formation'>company formation</a> and set-up, growth planning, <a class='ilink' href='/services/business-advisory'>business valuation and fundraising support</a>, cash flow management and strategic financial planning."),
]


def about(data):
    facts = [("Company", "Aviteus Business Solutions Ltd"),
             ("Company number", f'<a class="tlink" href="{CH_URL}" target="_blank" rel="noopener">{COMPANY_NO}</a>, registered in England and Wales'),
             ("Registered office", REG_OFFICE), ("Office", ADDRESS)]
    if data.get("aml_supervisor"): facts.append(("Anti-money laundering supervisor", escape(data["aml_supervisor"])))
    if data.get("pi_insurer"): facts.append(("Professional indemnity insurance", escape(data["pi_insurer"])))
    facts.append(("Sister company", "Aviteus Healthcare Ltd"))
    rows = "".join(f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in facts)
    where = ""
    opt = data.get("where_work_is_done")
    if opt in ("A", "B"):
        where = f'<section class="section section--alt" aria-labelledby="where-h"><div class="wrap split"><div class="head" style="margin:0"><h2 id="where-h">Where your work is done</h2></div><p class="lead">{escape(data["where_work_is_done_options"][opt])}</p></div></section>'
    body = f'''
<section class="hero hero--simple" aria-labelledby="h1">
  <div class="wrap read">
    <h1 id="h1">The people who will keep your books</h1>
    <p class="lead">{ABOUT_INTRO_TEAM if _has_team(data) else ABOUT_INTRO_NO_TEAM}</p>
  </div>
</section>

{founder_block(data)}
<section class="section section--alt" aria-labelledby="story-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="story-h">Why Aviteus exists</h2></div>
    <div>
      <p class="lead">Vikas Pandey started <a class="tlink" href="https://www.aviteushealthcare.co.uk" target="_blank" rel="noopener">Aviteus Healthcare</a> to supply care and nursing staff across the UK. Running that business taught him a simple lesson about money: when payroll is late, real people do not get paid, and when the books are behind, the owner makes decisions blind.</p>
      <p class="lead">Aviteus Business Solutions was set up in Harrow in September 2025 to give other owner-managed businesses what he needed himself. <a class='ilink' href='/services/bookkeeping'>Books that are current</a>. <a class='ilink' href='/services/payroll'>Payroll that runs on the same day every month</a>. <a class='ilink' href='/services/vat-tax'>Deadlines known well in advance</a>. And one person to ask.</p>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="new-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="new-h">Yes, we're a new firm</h2></div>
    <div>
      <p class="lead">We do not have a wall of reviews yet, and we will not invent one. Here is what being new means in practice:</p>
      <ul class="ticks mt-6">
        <li>Your work gets senior attention, not a junior working from a checklist.</li>
        <li>Each client matters to us, so we will work hard to keep you.</li>
        <li>We set up every process recently, around today's software and <a class='ilink' href='/services/vat-tax'>Making Tax Digital</a>, not around habits from 1998.</li>
      </ul>
    </div>
  </div>
</section>
{team_block(data, "Meet the team")}
<section class="section section--alt" aria-labelledby="how-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="how-h">How we work with you</h2></div>
    <ul class="ticks">
      <li><b>Everything in writing first.</b> <a class='ilink' href='/services/bookkeeping#scope'>A scope that lists what we do, what you do</a>, and the fixed fee, before any work starts.</li>
      <li><b>One named manager.</b> You will not be passed around. If your manager is away, you will be told who is covering.</li>
      <li><b>A monthly report you can read in two minutes.</b> What we finished, what is due next, what we need from you.</li>
      <li><b>Your software, your data.</b> Your accounting software stays in your name, and you can remove our access at any time.</li>
    </ul>
  </div>
</section>

<section class="section" id="credentials" aria-labelledby="cred-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="cred-h">Team and credentials</h2></div>
    <div>
      <p class="lead">Our accountants hold ICAEW, ACCA and CIMA qualifications. We work across <a class='ilink' href='/services/accounting-software'>Xero, Sage, QuickBooks and FreeAgent</a>, and we support migrations and training.</p>
      <p class="lead">We learn your goals, tidy the data, set the right processes and keep you ahead of HMRC dates. You get simple dashboards, monthly insights and early notes on risks and opportunities.</p>
    </div>
  </div>
</section>

<section class="section section--alt" id="values" aria-labelledby="values-h">
  <div class="wrap">
    <div class="head"><h2 id="values-h">What guides us</h2></div>
    <ul class="values">
      <li><b>Integrity</b><span>Honest advice and strict confidentiality.</span></li>
      <li><b>Accuracy</b><span>Precise books, compliant filings and audit-ready records.</span></li>
      <li><b>Commitment</b><span>We own deadlines and outcomes.</span></li>
      <li><b>Innovation</b><span>Secure cloud tools with real-time access.</span></li>
      <li><b>Partnership</b><span>We work with you as part of your team.</span></li>
    </ul>
  </div>
</section>
{where}
<section class="section" aria-labelledby="check-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="check-h">Details you can check</h2></div>
    <div><table class="facts-table">{rows}</table>
    {related([(s["name"], s["url"]) for s in SERVICE_MAP] + [("All services", "/services")])}</div>
  </div>
</section>

<section class="section" aria-labelledby="afaq-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="afaq-h">Common questions about our services</h2></div>
    {faq_html(ABOUT_FAQS)}
  </div>
</section>
{close_band("Talk to the person who would actually do your work", "Book a 20-minute review. You will speak to someone from the team above, not a sales desk.")}
'''
    people = [{"@type": "Person", "name": p["name"], "jobTitle": p["role"], "worksFor": {"@id": f"{SITE}/#business"}, **({"sameAs": [p["linkedin"]]} if p.get("linkedin") else {})}
              for p in data.get("team", []) if p.get("consent") and p.get("name")]
    return page(path="/about-us", title="About Aviteus Business Solutions | The Team in Harrow",
                description="Meet Aviteus Business Solutions: ICAEW, ACCA and CIMA qualified accountants in Harrow, our values, how we work, and company details you can check.",
                h_active="about", body_html=body, page_type="about",
                ld=[{"@type": "AboutPage", "url": f"{SITE}/about-us", "name": "The people who will keep your books", "about": {"@id": f"{SITE}/#business"}, "inLanguage": "en-GB"}, faq_ld(ABOUT_FAQS),
                    {"@type": "Person", "@id": f"{SITE}/about-us#vikas-pandey", "name": "Vikas Pandey", "jobTitle": "CEO", "worksFor": {"@id": f"{SITE}/#business"}, "url": f"{SITE}/about-us#founder", "sameAs": ["https://www.linkedin.com/in/vikas-pandey-aviteus/"]},
                    {"@type": "Organization", "@id": f"{SITE}/#org", "name": "Aviteus Business Solutions Ltd", "url": f"{SITE}/", "founder": {"@id": f"{SITE}/about-us#vikas-pandey"}, "foundingDate": "2025-09-04", "foundingLocation": "Harrow, United Kingdom",
                     "sameAs": [CH_URL]} | ({"employee": people} if people else {}),
                    breadcrumb_ld([("Home", "/"), ("About us", "/about-us")])], data=data)


# ---------------------------------------------------------------- Services hub
def _incl(key):
    s = next(x for x in SERVICE_MAP if x["key"] == key)
    items = "".join(f'<li><a class="ilink" href="{u}">{t}</a></li>' for t, u in s["items"])
    return f'<p class="incl-label mt-5">Includes</p><ul class="incl">{items}</ul>'


HUB_ORDER = ["bookkeeping", "payroll", "vat", "self-assessment", "advisory", "virtual-cfo", "formation", "software"]
HUB_TEXT = {  # "for" and "you get" lines. The first three are the copy deck's own words; the rest follow the live site.
    "bookkeeping": ("owners whose books are behind, or who want to see profit and cash every month.", "reconciled bank accounts, bills and sales posted, a three-page monthly pack.", "See how bookkeeping works"),
    "advisory": ("owners planning a hire, a price change, a sale or a funding round.", "forecasts, budgets, pricing and cost reviews, business valuation and fundraising support.", "See how business advisory works"),
    "virtual-cfo": ("growing businesses that want a finance director without the full-time cost.", "monthly finance reviews, cash flow management, strategic planning and investor support.", "See how Virtual CFO works"),
    "payroll": ("businesses paying 2 to 50 people who want payroll off their desk.", "staff paid on the right day, payslips, RTI filed, workplace pensions handled.", "See how payroll works"),
    "vat": ("VAT-registered companies that want every deadline known and met.", "VAT returns under Making Tax Digital, year-end accounts, corporation tax, tax planning and audit support.", "See VAT and tax deadlines"),
    "self-assessment": ("directors, landlords and the self-employed who file a personal tax return.", "your return prepared from your figures and filed before 31 January.", "See how Self Assessment works"),
    "formation": ("anyone starting a limited company, or moving from sole trader to limited.", "limited company set-up, HMRC registrations, Companies House filings and company secretarial tasks.", "See how company formation works"),
    "software": ("businesses on spreadsheets, starting out, or with a software file nobody trusts.", "Xero, QuickBooks, Sage or FreeAgent set up, cleaned up and taught to your team.", "See how software set-up works"),
}


def _svc(key):
    return next(x for x in SERVICE_MAP if x["key"] == key)


def _hub_row(key):
    s = _svc(key)
    f, g, link = HUB_TEXT[key]
    return (f'\n      <div class="row" id="svc-{key}"><h3><a href="{s["url"]}" style="color:inherit;text-decoration:none">{s["name"]}</a></h3>'
            f'<div class="row-meta"><p><b>For</b> {f}</p><p class="mt-4"><b>You get:</b> {g}</p>{_incl(key)}</div>'
            f'<a class="av-link" href="{s["url"]}">{link} {ARROW}</a></div>')


def services(data):
    body = f'''
<section class="hero hero--simple" aria-labelledby="h1">
  <div class="wrap read">
    {crumbs_html([("Home", "/"), ("Services", "/services")])}
    <h1 id="h1">What we do, and what we don't</h1>
    <p class="lead">Eight services for UK SMEs and startups, from monthly books and tax to advice, a Virtual CFO and company set-up. Most clients use two or three together, because they all run off the same set of books.</p>
    <nav class="jump mt-6" aria-label="Jump to a service">
      {"".join(f'<a href="#svc-{k}">{_svc(k)["name"]}</a>' for k in HUB_ORDER)}<a href="/industries">Industries we work with</a><a href="#dont-h">What we don't do</a>
    </nav>
  </div>
</section>

<section class="section" style="padding-top:0" aria-label="Our three services">
  <div class="wrap">
    <div class="rows">{"".join(_hub_row(k) for k in HUB_ORDER)}
    </div>
  </div>
</section>

<section class="section section--alt" id="also" aria-labelledby="also-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="also-h">Also available, as part of a monthly service</h2></div>
    <ul class="ticks">
      <li><b>Company set-up:</b> <a class='ilink' href='/services/company-formation'>forming a limited company and registering it with HMRC</a>.</li>
      <li><b>Software set-up and clean-up:</b> <a class='ilink' href='/services/accounting-software'>moving you onto Xero, QuickBooks, Sage or FreeAgent</a>, or tidying a file that has got out of hand.</li>
      <li><b>Catch-up bookkeeping:</b> <a class='ilink' href='/services/bookkeeping#catch-up'>bringing old records up to date</a> before monthly work starts.</li>
    </ul>
  </div>
</section>

<section class="section" aria-labelledby="dont-h">
  <div class="wrap">
    <div class="quiet read"><h2 id="dont-h">What we don't do</h2><p class="mt-4">We do not carry out statutory audits: those need a registered audit firm. If your company needs one, we will point you to a firm and support you through it, as part of our audit support. Saying no to work we are not set up for is how we keep the work we do take on to a high standard.</p></div>
  </div>
</section>

<section class="section" style="padding-top:0" aria-labelledby="unsure-h">
  <div class="wrap read">
    <h2 id="unsure-h"><a class="ilink" href="/contact" style="text-decoration-color:transparent">Not sure which you need?</a></h2>
    <p class="mt-4 lead">Most people aren't. Tell us what is going wrong and we will tell you which service fixes it, in 20 minutes.</p>
    <div class="mt-6">{book_btn("unsure")}</div>
  </div>
</section>
'''
    items = [(_svc(k)["name"], _svc(k)["url"]) for k in HUB_ORDER]
    return page(path="/services", title="Accounting Services for UK Businesses | Aviteus",
                description="Bookkeeping, payroll, VAT and tax planning, Self Assessment, business advisory, Virtual CFO, company formation and software set-up for UK SMEs.",
                h_active="services", body_html=body, page_type="hub",
                ld=[{"@type": "ItemList", "name": "Aviteus services", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "url": f"{SITE}{u}"} for i, (n, u) in enumerate(items)]},
                    breadcrumb_ld([("Home", "/"), ("Services", "/services")])], data=data)


# ---------------------------------------------------------------- 404
def notfound(data):
    body = f'''
<section class="section notfound" aria-labelledby="h1">
  <div class="wrap read">
    <h1 id="h1">This page isn't here</h1>
    <p class="lead mt-4">The link may be old, or the address mistyped. Here is where most people are heading:</p>
    <ul class="lines mt-6">
      <li><a href="/services/bookkeeping">Bookkeeping and management accounts</a></li>
      <li><a href="/services/payroll">Payroll and pensions</a></li>
      <li><a href="/services/vat-tax">VAT and year-end tax</a></li>
      <li><a href="/contact" data-book data-placement="404">Book a 20-minute review</a></li>
    </ul>
  </div>
</section>'''
    return page(path="/404", title="Page not found | Aviteus Business Solutions", description="This page isn't here. Find bookkeeping, payroll and VAT services, or book a 20-minute review.",
                h_active="", body_html=body, page_type="404", noindex=True, ld=[], data=data)


# ---------------------------------------------------------------- Deadline finder (lead magnet, new copy: reviewer to confirm)
def finder(data):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    ye_opts = '<option value="">No limited company</option>' + "".join(f'<option value="{i}"{" selected" if i == 2 else ""}>Last day of {m}</option>' for i, m in enumerate(months))
    faqs = [
        ("When is corporation tax due for a limited company?", "For most small companies, 9 months and 1 day after the end of the accounting period. With a year end of 31 March, the payment is due on 1 January. The company tax return (CT600) is due later, 12 months after the year end."),
        ("When do I file my company accounts at Companies House?", "9 months after your company's year end, for a private limited company after its first accounts. With a year end of 31 March, the deadline is 31 December."),
        ("When is PAYE due each month?", "If you pay HMRC electronically, PAYE and National Insurance are due by the 22nd of the month, for the tax month that ended on the 5th."),
        ("Does this tool store my details?", "No. The dates are worked out in your browser. Nothing you choose is saved or sent to us."),
    ]
    crumbs = [("Home", "/"), ("Free deadline finder", "/deadline-finder")]
    def link_rule(a):
        target = "/services/payroll" if any(k in a for k in ("PAYE", "P60", "P11D")) else ("/services/vat-tax" if not a.startswith(("Self", "Second")) else "/contact")
        return f'<a class="ilink" href="{target}">{a}</a>'
    rules = [
        ("VAT return and payment", "1 month and 7 days after the end of each VAT period", "Quarter ending 30 November: due 7 January"),
        ("Annual accounts to Companies House", "9 months after your year end", "Year end 31 March: due 31 December"),
        ("Corporation tax payment", "9 months and 1 day after your year end", "Year end 31 March: due 1 January"),
        ("Company tax return (CT600)", "12 months after your year end", "Year end 31 March: due 31 March the next year"),
        ("PAYE and National Insurance", "22nd of each month, paying electronically", "Tax month ending 5 June: due 22 June"),
        ("P60s to employees", "31 May each year", "For the tax year that ended on 5 April"),
        ("P11D and P11D(b) forms", "6 July each year", "Benefits in kind for the tax year that ended on 5 April"),
        ("Self Assessment return and tax", "31 January after the tax year ends", "2025/26 tax year: due 31 January 2027"),
        ("Second payment on account", "31 July", "2026/27 tax year: due 31 July 2027"),
    ]
    rule_rows = "".join(f'<tr><td>{link_rule(a)}</td><td data-label="Deadline" class="date">{b}</td><td data-label="Example">{c}</td></tr>' for a, b, c in rules)
    body = f'''
<section class="hero hero--simple" aria-labelledby="h1">
  <div class="wrap read">
    {crumbs_html(crumbs)}
    <p class="av-eyebrow">Free tool · No sign-up</p>
    <h1 id="h1" class="mt-4">Find your next UK tax deadlines</h1>
    <p class="lead">Pick your company's year end, your VAT quarters and whether you run payroll. You will see every date for the next 12 months, in date order. Nothing you enter is stored or sent.</p>
  </div>
</section>

<section class="section" style="padding-top:0" aria-label="Deadline finder">
  <div class="wrap finder">
    <form class="form-card form" id="finder-form" aria-labelledby="finder-h">
      <h2 id="finder-h">Your business</h2>
      <div class="field"><label for="d-ye">Your company's year end</label><select class="av-input" id="d-ye" name="year_end">{ye_opts}</select><p class="hint">Not the last day of a month? Your dates move by the same number of days.</p></div>
      <div class="field"><label for="d-vat">Your VAT returns</label><select class="av-input" id="d-vat" name="vat">
        <option value="none">Not VAT registered</option>
        <option value="2" selected>Quarters end Mar, Jun, Sep, Dec</option>
        <option value="0">Quarters end Jan, Apr, Jul, Oct</option>
        <option value="1">Quarters end Feb, May, Aug, Nov</option>
        <option value="monthly">Monthly returns</option></select></div>
      <label class="check"><input type="checkbox" name="payroll" checked><span>We run payroll for staff or directors</span></label>
      <label class="check"><input type="checkbox" name="sa"><span>I file a personal Self Assessment tax return</span></label>
      <button class="av-btn av-btn--ember" type="submit">Show my dates</button>
    </form>
    <div>
      <h2 class="sr-only">Your dates for the next 12 months</h2>
      <div class="results" id="finder-results" role="list" aria-live="polite"><noscript><p>This tool needs JavaScript. The rules it uses are listed below.</p></noscript></div>
      <div class="mt-5" style="display:flex;flex-wrap:wrap;gap:var(--space-3);align-items:center">
        <button class="av-btn av-btn--outline" type="button" id="finder-ics" hidden>Add these dates to my calendar</button>
        <span class="small" id="finder-ics-note">Each calendar entry has a reminder 14 days before.</span>
      </div>
      <div class="callout mt-6">
        <h2 style="font-size:24px;line-height:30px">Want someone to watch these dates for you?</h2>
        <p class="mt-4">Book a 20-minute review. We will check which dates apply to your business, and what you need to do before each one.</p>
        <div class="close-actions mt-5">{book_btn("finder")}{wa_btn("finder_whatsapp", "vat")}</div>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt" aria-labelledby="rules-h">
  <div class="wrap">
    <div class="head"><h2 id="rules-h">How these dates are worked out</h2><p class="lead">These are the standard rules for most UK limited companies and their directors.</p></div>
    <table class="table table--stack">
      <thead><tr><th scope="col">What</th><th scope="col">Deadline</th><th scope="col">Example</th></tr></thead>
      <tbody>{rule_rows}</tbody>
    </table>
    <div class="quiet mt-6"><h3>When these rules do not fit</h3><p class="mt-4">Your first accounts after setting up a company have a different deadline. Large companies pay corporation tax in instalments. If a payment date falls on a weekend or bank holiday, make sure the money reaches HMRC by the working day before. Always check your own dates on GOV.UK or with your accountant.</p></div>
    {related([("VAT and year-end tax", "/services/vat-tax"), ("Payroll and pensions", "/services/payroll"), ("Monthly bookkeeping", "/services/bookkeeping"), ("Self Assessment tax returns", "/services/self-assessment"), ("VAT registration checker", "/tools/vat-threshold-checker"), ("All free tools", "/tools"), ("All services", "/services"), ("Blog: limited company deadlines", "/blog/limited-company-deadlines-uk")])}
  </div>
</section>

<section class="section" aria-labelledby="faq-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="faq-h">Deadline questions</h2></div>
    {faq_html(faqs)}
  </div>
</section>
{close_band("Leave one call knowing your next three deadlines", "Book a 20-minute review and we will list the dates that apply to your business, and what you need to do before each one.", "vat")}
'''
    return page(path="/deadline-finder", title="UK Tax Deadline Finder for Limited Companies | Aviteus",
                description="Free tool. Enter your year end and VAT quarters to see your next corporation tax, VAT, payroll and Self Assessment dates. Save them to your calendar.",
                h_active="finder", body_html=body, page_type="tool", service="vat",
                extra_js='<script src="/assets/finder.js" defer></script>',
                og_title="Free UK tax deadline finder · Aviteus Business Solutions",
                og_desc="See your next corporation tax, VAT, payroll and Self Assessment dates in one list, and save them to your calendar.",
                ld=[{"@type": "WebApplication", "name": "UK tax deadline finder", "url": f"{SITE}/deadline-finder", "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
                     "offers": {"@type": "Offer", "price": "0", "priceCurrency": "GBP"}, "provider": {"@id": f"{SITE}/#business"}, "inLanguage": "en-GB",
                     "description": "Enter your year end, VAT quarters and payroll status to see your next UK tax and filing deadlines."},
                    breadcrumb_ld(crumbs), faq_ld(faqs)], data=data)


# ---------------------------------------------------------------- Legal pages
def _legal(path, title, desc, h1, crumb, body_inner, data, noindex=False, draft=None):
    banner = f'<div class="callout mt-6" role="note"><b>Draft for adviser review.</b> {draft}</div>' if draft else ""
    body = f'''
<section class="hero hero--simple" aria-labelledby="h1">
  <div class="wrap read">
    {crumbs_html([("Home", "/"), (crumb, path)])}
    <h1 id="h1">{h1}</h1>
    {banner}
  </div>
</section>
<section class="section legal-copy" style="padding-top:0">
  <div class="wrap read">
{body_inner}
  </div>
</section>'''
    return page(path=path, title=title, description=desc, h_active="", body_html=body, page_type="legal", noindex=noindex,
                ld=[breadcrumb_ld([("Home", "/"), (crumb, path)])], data=data)


def terms(data):
    # Word for word from the live site (read 24 Nov 2026). The strategy pack keeps these unchanged until Vikas reviews them.
    s = [
        ("1. Introduction", "<p>Welcome to Aviteus Business Solutions. These Terms and Conditions govern your use of our website and services. By accessing our website or engaging our services, you agree to be bound by these terms. If you do not agree with any part of these terms, please do not use our website or services.</p>"),
        ("2. Our Services", "<p>Aviteus Business Solutions provides professional accounting, tax planning, business advisory, and related financial services to businesses and individuals. The scope of services will be defined in individual engagement letters or service agreements.</p><ul><li>All services are subject to availability and acceptance by Aviteus Business Solutions</li><li>Service fees and payment terms will be outlined in your engagement letter</li><li>We reserve the right to refuse service to any client at our discretion</li></ul>"),
        ("3. Client Responsibilities", "<p>As our client, you agree to:</p><ul><li>Provide accurate, complete, and timely information required for our services</li><li>Respond promptly to our requests for information or clarification</li><li>Maintain proper records and documentation as required by law</li><li>Pay all fees in accordance with agreed payment terms</li><li>Inform us immediately of any changes to your circumstances that may affect our services</li></ul>"),
        ("4. Confidentiality", "<p>We are committed to protecting the confidentiality of your information. All client information will be kept confidential and will only be disclosed where required by law or with your express permission. We maintain professional standards in accordance with relevant accounting bodies and data protection legislation.</p>"),
        ("5. Limitation of Liability", "<p>While we strive to provide accurate and professional services, Aviteus Business Solutions shall not be liable for:</p><ul><li>Any losses arising from incomplete or inaccurate information provided by the client</li><li>Losses resulting from circumstances beyond our reasonable control</li><li>Indirect or consequential losses, unless caused by our negligence</li><li>Decisions made by clients based on advice that was not formally documented</li></ul><p>Our liability is limited to the fees paid for the specific service in question, except in cases of proven negligence or breach of professional duty.</p>"),
        ("6. Intellectual Property", "<p>All content on this website, including text, graphics, logos, and software, is the property of Aviteus Business Solutions and is protected by intellectual property laws. You may not reproduce, distribute, or use any content without our prior written permission.</p>"),
        ("7. Termination of Services", "<p>Either party may terminate services with written notice as specified in the engagement letter. Upon termination, you remain responsible for payment of all fees for services rendered. We will return your records and documents upon settlement of outstanding fees.</p>"),
        ("8. Professional Standards", "<p>Aviteus Business Solutions operates in accordance with professional standards set by relevant accounting and regulatory bodies. We maintain professional indemnity insurance and adhere to continuing professional development requirements.</p>"),
        ("9. Complaints Procedure", "<p>If you have a complaint about our services, please contact us in writing at info@aviteusbusiness.co.uk. We will acknowledge your complaint within 5 business days and provide a full response within 28 days.</p>"),
        ("10. Changes to Terms", "<p>We reserve the right to modify these Terms and Conditions at any time. Changes will be posted on this page with an updated revision date. Your continued use of our services after changes are posted constitutes acceptance of the modified terms.</p>"),
        ("11. Governing Law", "<p>These Terms and Conditions are governed by the laws of England and Wales. Any disputes arising from these terms or our services will be subject to the exclusive jurisdiction of the courts of England and Wales.</p>"),
        ("12. Contact Information", "<p>If you have any questions about these Terms and Conditions, please contact us:</p><p><b>Aviteus Business Solutions</b><br>Alpha House, 296 Kenton Rd, Harrow HA3 8DD, United Kingdom<br>Email: info@aviteusbusiness.co.uk<br>Phone: 020 4628 8209</p>"),
    ]
    inner = "".join(f"<h2>{h}</h2>{b}" for h, b in s) + "<p><b>Last Updated: November 6, 2025</b></p>"
    return _legal("/terms-and-conditions", "Terms and Conditions | Aviteus Business Solutions",
                  "The terms and conditions for using the Aviteus Business Solutions website and services, including confidentiality, liability, complaints and governing law.",
                  "Terms &amp; Conditions", "Terms and conditions", inner, data)


def privacy(data):
    todo = lambda t: f'<span class="todo">To confirm: {t}</span>'
    inner = f'''
<h2>Who we are</h2>
<p>Aviteus Business Solutions Ltd is the data controller for personal data collected through this website. Company number {COMPANY_NO}, registered in England and Wales. Registered office: {ADDRESS}.</p>
<p>Questions about your data: email {EMAIL} or call {PHONE}.</p>

<h2>What we collect</h2>
<ul>
<li><b>When you send an enquiry:</b> your full name, email, company or website (if you give it), the service you ask about, your message, how you want us to reply, and your phone or WhatsApp number if you choose a call or WhatsApp.</li>
<li><b>About the visit that led to your enquiry:</b> the page you sent it from, the website that sent you here, and any campaign tags in the link you clicked.</li>
<li><b>If you tick the email box:</b> your email address, to send occasional emails about UK tax deadlines and changes.</li>
<li><b>If you accept analytics cookies:</b> how pages are used, through Google Analytics. See our <a class="tlink" href="/cookies">cookie details</a>.</li>
<li><b>If you message us on WhatsApp:</b> your number and the messages you send.</li>
</ul>
<p>The deadline finder works in your browser. Nothing you choose in it is saved or sent to us.</p>

<h2>Why we use it, and our lawful basis</h2>
<ul>
<li>To reply to your enquiry and prepare your review. {todo("lawful basis, for example steps taken at your request before a contract, or legitimate interests")}</li>
<li>To send occasional emails, only if you tick the box. Lawful basis: your consent. You can withdraw it at any time.</li>
<li>To see which pages help people, only if you accept analytics cookies. Lawful basis: your consent.</li>
</ul>

<h2>Who we share it with</h2>
<p>{todo("the final list of processors and the agreements with each. The strategy pack names: Zoho CRM, the email service that sends enquiry notifications, SEO Rise (website support and lead notifications), Google Analytics, Cloudflare Turnstile spam checks, and WhatsApp (Meta) for chats.")}</p>
<p>We do not sell your data.</p>

<h2>Where your data is handled</h2>
<p>{todo("whether any processing happens outside the UK, for example by team members in India, and the safeguards used.")}</p>

<h2>How long we keep it</h2>
<p>{todo("how long enquiries that do not become clients are kept, and how long client records are kept.")}</p>

<h2>Your rights</h2>
<p>You can ask to see the personal data we hold about you, to correct it, to delete it, to limit how we use it, to object to how we use it, or to receive a copy in a common format. Where we rely on your consent, you can withdraw it at any time. To use any of these rights, email {EMAIL}.</p>
<p>If you are unhappy with how we handle your data, you can complain to the Information Commissioner's Office at ico.org.uk or on 0303 123 1113.</p>

<h2>Changes to this notice</h2>
<p>{todo("the date this notice is approved and published.")}</p>
'''
    return _legal("/privacy-policy", "Privacy Notice | Aviteus Business Solutions",
                  "How Aviteus Business Solutions collects and uses personal data from its website enquiry form, emails and analytics, and the rights you have.",
                  "Privacy notice", "Privacy notice", inner, data, noindex=True,
                  draft="This notice has not been approved yet. Aviteus's adviser must check and complete it before the website goes live. Items marked \"To confirm\" need an answer from Aviteus.")


def cookies(data):
    inner = '''
<p class="lead">We use essential cookies to run this site. With your permission, we also use analytics cookies to see which pages help people. We do not use advertising cookies.</p>

<h2>Before you choose</h2>
<p>Nothing is set for analytics until you choose. Your choice itself is saved in your browser so we do not ask again on every page.</p>
<table class="facts-table">
<tr><th scope="row">av_consent</th><td>Remembers whether you accepted or rejected analytics. Saved in your browser's local storage until you clear it.</td></tr>
</table>

<h2>If you accept analytics</h2>
<table class="facts-table">
<tr><th scope="row">_ga</th><td>Google Analytics. Tells visits apart. Expires after 2 years.</td></tr>
<tr><th scope="row">_ga_ followed by an ID</th><td>Google Analytics. Keeps track of a visit. Expires after 2 years.</td></tr>
<tr><th scope="row">av_first</th><td>The first page you visited, so an enquiry shows which page helped. Saved in your browser for this visit only.</td></tr>
</table>

<h2>Spam protection on the enquiry form</h2>
<p><span class="todo">To confirm: once the enquiry form goes live, Cloudflare Turnstile checks that a real person is sending it. List what it stores here.</span></p>

<h2>Change your choice</h2>
<p>Use <a class="tlink" href="#" data-cookie-settings>Cookie settings</a> at any time, or at the bottom of every page.</p>
'''
    return _legal("/cookies", "Cookie Details | Aviteus Business Solutions",
                  "Which cookies and browser storage the Aviteus Business Solutions website uses, why, for how long, and how to change your choice at any time.",
                  "Cookie details", "Cookies", inner, data, noindex=True,
                  draft="This page describes exactly what the website does today. Aviteus's adviser must approve it before the website goes live.")


# ---------------------------------------------------------------- Blog
from posts import POSTS
from datetime import date as _date


def _when(iso):
    d = _date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


def _minutes(post):
    import re as _re
    text = _re.sub(r"<[^>]+>", " ", " ".join(b for _, b in post["sections"]) + post["in_short"] + " ".join(q + a for q, a in post["faqs"]))
    return max(2, round(len(text.split()) / 220))


def _approved(data, post):
    return post["slug"] in data.get("approved_posts", [])


def blog_index(data):
    rows = []
    for post in POSTS:
        rows.append(f'''<article class="post-row">
  <p class="post-meta"><span class="post-cat">{post["category"]}</span> · <time datetime="{post["date"]}">{_when(post["date"])}</time> · {_minutes(post)} min read</p>
  <h2><a href="/blog/{post["slug"]}">{post["title"]}</a></h2>
  <p>{post["summary"]}</p>
  <a class="av-link" href="/blog/{post["slug"]}" aria-label="Read: {escape(post["title"])}">Read the guide {ARROW}</a>
</article>''')
    any_ok = any(_approved(data, p) for p in POSTS)
    body = f'''
<section class="hero hero--simple" aria-labelledby="h1">
  <div class="wrap read">
    {crumbs_html([("Home", "/"), ("Blog", "/blog")])}
    <p class="av-eyebrow">Blog</p>
    <h1 id="h1" class="mt-4">Plain answers on UK bookkeeping, payroll and tax</h1>
    <p class="lead">Short guides for owners of UK businesses. Each one answers a question we hear on review calls, with the dates and steps that matter.</p>
  </div>
</section>
<section class="section" style="padding-top:0" aria-label="Posts">
  <div class="wrap">
    <div class="post-list">{"".join(rows)}</div>
    <div class="callout mt-8"><h2 style="font-size:24px;line-height:30px">Rather someone handled it?</h2><p class="mt-4">Book a 20-minute review and we will tell you what is behind, what is due next, and whether we can help.</p><div class="close-actions mt-5">{book_btn("blog_index")}</div></div>
  </div>
</section>'''
    items = [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/blog/{p['slug']}", "name": p["title"]} for i, p in enumerate(POSTS)]
    return page(path="/blog", title="Blog: UK Bookkeeping, Payroll and Tax Guides | Aviteus",
                description="Plain guides for UK business owners on bookkeeping, payroll, VAT, Making Tax Digital, company deadlines and switching accountant.",
                h_active="blog", body_html=body, page_type="blog", noindex=not any_ok,
                ld=[{"@type": "Blog", "@id": f"{SITE}/blog#blog", "name": "Aviteus Business Solutions blog", "url": f"{SITE}/blog", "publisher": {"@id": f"{SITE}/#business"}, "inLanguage": "en-GB"},
                    {"@type": "ItemList", "itemListElement": items}, breadcrumb_ld([("Home", "/"), ("Blog", "/blog")])], data=data)


def blog_post(data, post):
    import re as _re
    ok = _approved(data, post)
    ids = [_re.sub(r"[^a-z0-9]+", "-", h.lower()).strip("-")[:48] for h, _ in post["sections"]]
    toc = "".join(f'<li><a class="ilink" href="#{i}">{h}</a></li>' for (h, _), i in zip(post["sections"], ids))
    secs = "".join(f'<section class="post-sec" aria-labelledby="{i}"><h2 id="{i}">{h}</h2>{b}</section>' for (h, b), i in zip(post["sections"], ids))
    others = [p for p in POSTS if p["slug"] != post["slug"]]
    same = [p for p in others if p["category"] == post["category"]]
    more = (same + [p for p in others if p not in same])[:3]
    more_html = "".join(f'<li><a class="tlink" href="/blog/{p["slug"]}">{p["title"]}</a></li>' for p in more)
    svc_html = "".join(f'<li><a class="tlink" href="{u}">{t}</a></li>' for t, u in post["services"])
    draft = "" if ok else '<div class="callout mt-5" role="note"><b>Draft: awaiting accounting review.</b> This guide is not yet signed off by a named reviewer, so search engines are asked not to list it.</div>'
    url = f"/blog/{post['slug']}"
    crumbs = [("Home", "/"), ("Blog", "/blog"), (post["category"], url)]
    body = f'''
<article>
<section class="hero hero--simple" aria-labelledby="h1">
  <div class="wrap read">
    {crumbs_html(crumbs)}
    <p class="av-eyebrow">{post["category"]}</p>
    <h1 id="h1" class="mt-4">{post["title"]}</h1>
    <p class="post-meta mt-5">Aviteus Business Solutions · Updated <time datetime="{post["date"]}">{_when(post["date"])}</time> · {_minutes(post)} min read</p>
    {draft}
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap post-grid">
    <aside class="post-side" aria-label="On this page">
      <p class="sw-label">On this page</p>
      <ol class="toc">{toc}<li><a class="ilink" href="#faq-h">Questions</a></li></ol>
      <div class="post-cta"><p><b>Need a hand?</b> Book a free 20-minute review.</p>{book_btn("post_side", "Book a review", "av-btn av-btn--ember av-btn--small")}</div>
    </aside>
    <div class="post-body">
      <div class="in-short"><p class="sw-label">In short</p><p>{post["in_short"]}</p></div>
      {secs}
      <section class="post-sec" aria-labelledby="faq-h"><h2 id="faq-h">Questions</h2>{faq_html(post["faqs"], first_open=False)}</section>
      <nav class="post-links" aria-label="Related">
        <div><p class="sw-label">Related services</p><ul>{svc_html}</ul></div>
        <div><p class="sw-label">More from the blog</p><ul>{more_html}<li><a class="av-link" href="/blog">All posts {ARROW}</a></li></ul></div>
      </nav>
    </div>
  </div>
</section>
</article>
{close_band("Bring one problem. Leave with a plan.", "Twenty minutes is enough to tell you what is behind, what is due next, and whether we can help. If we can't, we'll tell you who might.")}'''
    ld = {"@type": "BlogPosting", "@id": f"{SITE}{url}#post", "headline": post["title"], "description": post["description"], "datePublished": post["date"], "dateModified": post["date"],
          "inLanguage": "en-GB", "mainEntityOfPage": f"{SITE}{url}", "image": f"{SITE}/assets/img/og-default.png", "articleSection": post["category"],
          "author": {"@id": f"{SITE}/#business"}, "publisher": {"@id": f"{SITE}/#business"}, "isPartOf": {"@id": f"{SITE}/blog#blog"},
          "about": [{"@id": f"{SITE}{u}#service"} for _, u in post["services"]]}
    return page(path=url, title=post["seo_title"], description=post["description"], h_active="blog", body_html=body, page_type="post",
                noindex=not ok, og_title=post["title"], og_desc=post["description"],
                ld=[ld, breadcrumb_ld(crumbs), faq_ld(post["faqs"])], data=data)


# ---------------------------------------------------------------- Services added from the live site (not in the copy deck: Vikas to approve)
def _svc_page(data, spec):
    you, us = '<span class="who who--you">You</span>', '<span class="who who--us">Aviteus</span>'
    crumbs = [("Home", "/"), ("Services", "/services"), (spec["crumb"], spec["path"])]
    incl = "".join(f"<li><b>{a}</b> {b}</li>" for a, b in spec["included"])
    rows = "".join(f'<tr><td>{t}</td><td data-label="We do">{w}</td><td data-label="You do">{y}</td></tr>' for t, w, y in spec["scope"])
    extra = spec.get("extra", "")
    body = f'''
<section class="hero hero--simple" aria-labelledby="h1">
  <div class="wrap read">
    {crumbs_html(crumbs)}
    <h1 id="h1">{spec["h1"]}</h1>
    <p class="lead">{spec["lead"]}</p>
    <div class="hero-actions">{book_btn("hero")}<a class="tlink" href="#included">{spec["jump"]} ↓</a></div>
  </div>
</section>

<section class="section section--alt" aria-labelledby="answer-h">
  <div class="wrap read">
    <h2 id="answer-h">{spec["answer_h"]}</h2>
    <p class="mt-4 lead">{spec["answer"]}</p>
  </div>
</section>

<section class="section" id="included" aria-labelledby="inc-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="inc-h">What is included</h2></div>
    <ul class="ticks">{incl}</ul>
  </div>
</section>

<section class="section section--alt" id="scope" aria-labelledby="scope-h">
  <div class="wrap">
    <div class="head"><h2 id="scope-h">Who does what</h2></div>
    <table class="table table--stack">
      <thead><tr><th scope="col">Task</th><th scope="col">We do</th><th scope="col">You do</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <p class="note mt-4">The table in your scope will be specific to your business. This is the starting point.</p>
    {related(spec["related"] + [("All services", "/services")])}
    <div class="mt-7">{book_btn("after_scope")}</div>
  </div>
</section>
{extra}
<section class="section" aria-labelledby="suits-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="suits-h">Who this is for, and who it isn't</h2></div>
    <div><p class="lead">{spec["suits"]}</p><div class="quiet mt-6"><p>{spec["not"]}</p></div></div>
  </div>
</section>

<section class="section section--alt" aria-labelledby="fee-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="fee-h">How the fee works</h2></div>
    <p class="lead">{spec["fee"]}</p>
  </div>
</section>

<section class="section" aria-labelledby="faq-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="faq-h">{spec["faq_h"]}</h2></div>
    {faq_html(spec["faqs"])}
  </div>
</section>
{close_band(spec["close_h"], spec["close_p"])}
'''
    return page(path=spec["path"], title=spec["title"], description=spec["desc"], h_active=spec["key"], body_html=body, page_type="service",
                ld=[service_ld(spec["schema_name"], spec["path"], spec["desc"], spec["service_type"]), breadcrumb_ld(crumbs), faq_ld(spec["faqs"])], data=data)


def advisory(data):
    return _svc_page(data, {
        "key": "advisory", "path": "/services/business-advisory", "crumb": "Business advisory",
        "title": "Business Advisory, Valuation and Fundraising | Aviteus",
        "desc": "Business advisory for UK SMEs: forecasts, budgets, pricing and cost reviews, business valuation, fundraising support and growth planning. Fixed fee.",
        "schema_name": "Business advisory", "service_type": "Business advisory",
        "h1": "Business advisory: forecasts, valuations and funding, in plain numbers",
        "lead": "Know what next quarter looks like before it arrives. We build forecasts and budgets from your own books, review your prices and costs, value your business and support you when you raise funds. On a fee agreed in writing before we start.",
        "jump": "See what is included",
        "answer_h": "What business advisory means with Aviteus",
        "answer": "Business advisory means using your figures to make decisions, not just to file returns. With Aviteus it starts from up-to-date books, so every forecast rests on real numbers. You get a forecast you can update, a budget to measure against, and a short list of actions that protect cash and support growth.",
        "included": [("Cash flow forecasts.", "What comes in and goes out over the coming months, built from your books and your plans."),
                     ("Budgets.", "Targets for the year, compared with your actual figures each month."),
                     ("Pricing reviews.", "The margin on each product or service, so you can see which ones pay their way."),
                     ("Cost controls.", "Where the money goes: suppliers, subscriptions and the costs that crept up."),
                     ("Business valuation.", "What your business is worth, for a sale, a new shareholder or planning ahead."),
                     ("Fundraising support.", "Business plans, forecasts and investor or lender packs, with support through their questions."),
                     ("Growth planning.", "Strategic financial planning for start-up, expansion and the next stage of the business.")],
        "scope": [("Cash flow forecast", "Build it from your books and update it each month or quarter", "Tell us about plans: hires, big purchases, new contracts"),
                  ("Budget", "Set it with you and compare it with your actual figures", "Agree the targets"),
                  ("Pricing review", "Work out the margin on each product or service", "Share your price list and supplier costs"),
                  ("Valuation", "Value the business from its accounts, profits and prospects", "Share plans and any offers received"),
                  ("Fundraising", "Prepare the business plan, forecasts and investor pack", "Meet investors or lenders and choose the offer")],
        "related": [("Virtual CFO", "/services/virtual-cfo"), ("Monthly bookkeeping", "/services/bookkeeping"), ("Company formation", "/services/company-formation"), ("Bookkeeping vs management accounts", "/blog/bookkeeping-vs-management-accounts")],
        "suits": "This suits you if you run a growing UK business and want to see the next few months before they happen: before a hire, a big purchase, a price change or a loan.",
        "not": "If your books are behind, we start with a catch-up, because advice built on old figures is guesswork. For ongoing senior support every month, see our Virtual CFO service.",
        "fee": "A fixed fee for a one-off piece of work, such as a pricing review or a funding pack. Or a fixed monthly fee if you want your forecast and budget kept up to date alongside your bookkeeping. Agreed in writing before any work starts.",
        "faq_h": "Business advisory questions",
        "faqs": [("Do I need monthly bookkeeping first?", "You need up-to-date books. If ours is the team keeping them, the forecast stays current every month. If your books are behind, we catch them up first."),
                 ("Can you help us raise funds or get a bank loan?", "Yes. We prepare the business plan, forecasts and figures lenders and investors ask for, and support you through their questions and checks."),
                 ("Can you value my business?", "Yes. We value the business from its accounts, profits and prospects, whether for a sale, a new shareholder or planning ahead."),
                 ("How often should a forecast be updated?", "Monthly suits most growing businesses. Quarterly can work if your figures do not change much."),
                 ("What is the difference between a forecast and a budget?", "A budget is the target you set for the year. A forecast is your best view of what will actually happen, updated as things change.")],
        "close_h": "See the next few months before they happen",
        "close_p": "In 20 minutes we will look at where your figures stand and what a forecast or budget would show you.",
    })


def formation(data):
    return _svc_page(data, {
        "key": "formation", "path": "/services/company-formation", "crumb": "Company formation",
        "title": "Company Formation and Compliance in the UK | Aviteus",
        "desc": "Limited company set-up, HMRC registrations, Companies House filings and company secretarial tasks, done in the right order with your first dates set.",
        "schema_name": "Company formation and compliance", "service_type": "Company formation",
        "h1": "Company formation and compliance, set up right from day one",
        "lead": "Limited company set-up, HMRC registrations, Companies House filings and company secretarial tasks. Done in the right order, so your first tax, VAT and payroll dates are known before they arrive.",
        "jump": "See what is included",
        "answer_h": "What company formation and compliance cover",
        "answer": "Company formation means registering a limited company at Companies House. Compliance means keeping it in good standing after that: the yearly confirmation statement, changes to directors and shareholders, and the records the law asks you to keep. We do both, and put every date in your \"Done and due\" report.",
        "included": [("Limited company set-up.", "Registering the company at Companies House, with directors, shareholders and the registered office address checked first."),
                     ("HMRC registrations.", "Corporation tax, and VAT and PAYE when you need them."),
                     ("Companies House filings.", "The confirmation statement each year, and changes to directors, shareholders and addresses."),
                     ("Company secretarial tasks.", "Keeping the company's registers and minutes of key decisions up to date."),
                     ("Your first dates.", "First accounts, first corporation tax payment and first confirmation statement, in one calendar.")],
        "scope": [("Before set-up", "Check the name, directors, shareholders and business activity", "Decide who the directors and shareholders are"),
                  ("Set-up", "Register the company at Companies House", "Approve the details before we file"),
                  ("HMRC registrations", "Register for corporation tax, and VAT and PAYE if needed", "Answer a few questions about the business"),
                  ("Each year", "File the confirmation statement and keep the registers current", "Tell us about any changes")],
        "related": [("Your first company deadlines", "/blog/limited-company-deadlines-uk"), ("VAT and year-end tax", "/services/vat-tax"), ("Payroll and pensions", "/services/payroll"), ("Accounting software set-up", "/services/accounting-software"), ("Self Assessment for directors", "/services/self-assessment")],
        "suits": "This suits you if you are starting a new limited company, or moving from sole trader to limited company and want the set-up done once and done properly.",
        "not": "Whether a limited company is right for you depends on your profit and your plans. If it is not the right move yet, we will say so on the call.",
        "fee": "A fixed fee for the set-up and registrations. Yearly compliance, such as the confirmation statement, is included when you use one of our monthly services. Agreed in writing before any work starts.",
        "faq_h": "Company formation questions",
        "faqs": [("How long does it take to set up a limited company?", "Online applications to Companies House are often registered within a day, once the details are ready. Most of the time goes into deciding the details first."),
                 ("When are my first accounts due?", "A new company's first accounts are due 21 months after the date it was set up. After that, accounts are due 9 months after each year end."),
                 ("Do you file the confirmation statement?", "Yes. We check the company's details with you each year and file it within 14 days of the review date."),
                 ("Do I need to register for VAT straight away?", "Only if your VAT-taxable turnover goes over the registration threshold, or you expect it to. Some businesses register early by choice. We go through this when we set up the company.")],
        "close_h": "Start your company with the dates already set",
        "close_p": "In 20 minutes we will go through the set-up, the registrations you need and your first deadlines.",
    })


def software(data):
    return _svc_page(data, {
        "key": "software", "path": "/services/accounting-software", "crumb": "Accounting software",
        "title": "Xero, QuickBooks, Sage and FreeAgent Set-Up | Aviteus",
        "desc": "Accounting software set-up, clean-up and training for UK businesses. Xero, QuickBooks, Sage and FreeAgent, with your records moved across and checked.",
        "schema_name": "Accounting software set-up and training", "service_type": "Accounting software set-up",
        "h1": "Accounting software set-up, clean-up and training",
        "lead": "Xero, QuickBooks, Sage or FreeAgent. We help you choose, set it up, move your records across and show your team the few things they need to do each month.",
        "jump": "See what is included",
        "answer_h": "What accounting software set-up means with Aviteus",
        "answer": "The right software turns bookkeeping from a monthly chore into a routine that runs itself. We set it up around how your business works: bank feeds connected, VAT set correctly, invoices ready to send. Your subscription stays in your company's name, and you keep full access at all times.",
        "included": [("Choosing the right software.", "Xero, QuickBooks, Sage or FreeAgent, matched to your size, your sector and how you work."),
                     ("Set-up.", "Chart of accounts, VAT settings, bank feeds and invoice templates."),
                     ("Moving your records.", "From spreadsheets or another package, with opening balances checked before anything new is posted."),
                     ("Clean-up.", "A file that has got out of hand: unmatched bank lines, duplicates and wrong VAT codes put right."),
                     ("Training.", "For you and your team: the two or three things to do each month, and nothing more."),
                     ("Connected apps.", "Receipt capture apps such as Hubdoc, so bills and receipts reach your books without paper.")],
        "scope": [("Choosing software", "Recommend the best fit and explain why", "Make the final choice"),
                  ("Set-up", "Build the accounts, VAT settings and invoice templates", "Connect your bank feeds with us"),
                  ("Moving records", "Bring across balances and history, then check them", "Share access to your old system"),
                  ("Training", "Show your team the monthly routine", "Join one short session")],
        "related": [("Monthly bookkeeping", "/services/bookkeeping"), ("E-commerce accounting", "/industries#ecommerce"), ("VAT returns and Making Tax Digital", "/blog/vat-returns-making-tax-digital"), ("Catch-up bookkeeping", "/blog/catch-up-bookkeeping")],
        "suits": "This suits you if you are still on spreadsheets, starting out, or stuck with a software file nobody trusts any more.",
        "not": "If your current software works and your books are up to date, you may not need this at all. We will say so on the call.",
        "fee": "A fixed fee for set-up, moving records or a clean-up, quoted before we start. Training is included with set-up. If you then use our monthly bookkeeping, the software becomes part of that routine.",
        "faq_h": "Accounting software questions",
        "faqs": [("Which accounting software is best for a small business?", "It depends on your size, your sector and who will use it. Xero, QuickBooks, Sage and FreeAgent all work for UK businesses. We recommend one after a short review."),
                 ("Can you move my old records into new software?", "Yes. We bring across opening balances and, where needed, past transactions, then check the figures before anything new is posted."),
                 ("Do I need Making Tax Digital software?", "If you are VAT registered, yes. Your VAT returns must be filed through compatible software, and all four packages we use are compatible."),
                 ("Who owns the software subscription?", "You do. The subscription stays in your company's name, and you can remove our access at any time.")],
        "close_h": "Get software your whole team can use",
        "close_p": "In 20 minutes we will look at how you keep records today and which software would fit.",
    })


def self_assessment(data):
    dates = """<section class="section" id="dates" aria-labelledby="dates-h">
  <div class="wrap">
    <div class="head"><h2 id="dates-h">The Self Assessment dates</h2></div>
    <table class="table table--stack">
      <thead><tr><th scope="col">What</th><th scope="col">Deadline</th></tr></thead>
      <tbody>
        <tr><td>Register for Self Assessment, if you are new to it</td><td data-label="Deadline" class="date">5 October after the tax year ends</td></tr>
        <tr><td>Paper tax return</td><td data-label="Deadline" class="date">31 October after the tax year ends</td></tr>
        <tr><td>Online tax return and tax due</td><td data-label="Deadline" class="date">31 January after the tax year ends</td></tr>
        <tr><td>First payment on account, if one applies</td><td data-label="Deadline" class="date">31 January</td></tr>
        <tr><td>Second payment on account, if one applies</td><td data-label="Deadline" class="date">31 July</td></tr>
      </tbody>
    </table>
    <p class="callout mt-5">Payments on account are advance payments towards next year's bill. They often catch people out in their second year, when the first return and the first advance payment fall due on the same day.</p>
  </div>
</section>"""
    return _svc_page(data, {
        "key": "self-assessment", "path": "/services/self-assessment", "crumb": "Self Assessment",
        "title": "Self Assessment Tax Returns for Directors | Aviteus",
        "desc": "Self Assessment tax returns for company directors, landlords and the self-employed. Prepared from your figures, filed before 31 January, no surprises.",
        "schema_name": "Self Assessment tax returns", "service_type": "Tax preparation",
        "h1": "Self Assessment tax returns, filed before 31 January",
        "lead": "Your personal tax return, prepared from your figures and filed on time. You see the tax figure early, so the 31 January payment is never a surprise.",
        "jump": "See what is included",
        "answer_h": "Who needs a Self Assessment tax return",
        "answer": "You usually need to file a Self Assessment tax return if you are self-employed, earn rental income, or have income that tax has not already been taken from, such as dividends above your allowance. HMRC can also ask you to file. Check GOV.UK, or ask us on a review call.",
        "included": [("Registering for Self Assessment,", "if you are new to it."),
                     ("Gathering your income:", "salary, dividends, rental income and self-employment."),
                     ("Working out your tax,", "and any payments on account, with the figure sent to you early."),
                     ("Filing your return online", "before 31 January, after you approve it."),
                     ("Reminders", "for the 31 January and 31 July payments.")],
        "scope": [("Your income", "Ask for the figures we need, in one list", "Send payslips, dividend vouchers and rental figures"),
                  ("The return", "Prepare it and explain the tax figure", "Check it and approve it"),
                  ("Filing", "File it online with HMRC", "Pay the tax by the due date"),
                  ("Next year", "Remind you about payments on account", "Keep records as the year goes")],
        "related": [("Company deadlines for directors", "/blog/limited-company-deadlines-uk"), ("Find your dates with the deadline finder", "/deadline-finder"), ("VAT and year-end tax", "/services/vat-tax"), ("Payroll and pensions", "/services/payroll")],
        "extra": dates,
        "suits": "This suits company directors who take dividends, landlords, and self-employed people who want their return done properly and early, not in the last week of January.",
        "not": "If your only income is a salary taxed through PAYE, you may not need to file at all. We will tell you on the call.",
        "fee": "A fixed fee for each tax return, based on how many income sources you have. Agreed in writing before any work starts.",
        "faq_h": "Self Assessment questions",
        "faqs": [("When is the Self Assessment deadline?", "31 January after the end of the tax year, for online returns and for paying the tax. Paper returns are due earlier, on 31 October."),
                 ("What are payments on account?", "Advance payments towards next year's tax bill, due on 31 January and 31 July. Whether they apply depends on your last bill."),
                 ("What happens if I file late?", "HMRC charges a £100 penalty straight away for a late return, with more if it stays late. Interest is also charged on tax paid late."),
                 ("Does Making Tax Digital for Income Tax affect me?", "It might, if you are self-employed or a landlord above an income threshold. Bring your figures to a review and we will tell you if and when it applies.")],
        "close_h": "Get your return done before the January rush",
        "close_p": "In 20 minutes we will go through your income sources and what your return will need.",
    })


def virtual_cfo(data):
    return _svc_page(data, {
        "key": "virtual-cfo", "path": "/services/virtual-cfo", "crumb": "Virtual CFO",
        "title": "Virtual CFO Services for UK SMEs and Startups | Aviteus",
        "desc": "A part-time finance director for growing UK businesses: monthly finance reviews, cash flow management, strategic planning and lender and investor support.",
        "schema_name": "Virtual CFO", "service_type": "Virtual CFO",
        "h1": "Virtual CFO: a finance director for your business, without the full-time cost",
        "lead": "Senior finance support every month. Your figures reviewed with you, cash planned ahead, and clear advice before big decisions. Part-time, on a fixed monthly fee.",
        "jump": "See what is included",
        "answer_h": "What a Virtual CFO does",
        "answer": "A Virtual CFO is a part-time finance director. With Aviteus, that means a qualified, senior person who reviews your figures with you each month, plans cash and growth, and sits beside you for the big decisions: hiring, pricing, borrowing or raising funds.",
        "included": [("Monthly finance review.", "Your management accounts walked through with you, with the three things that need attention."),
                     ("Financial management.", "Margins, overheads, working capital and the KPIs that show how the business is doing."),
                     ("Cash flow management.", "A rolling cash forecast, so you see a shortfall weeks before it arrives."),
                     ("Strategic financial planning.", "An annual plan and budget, and the numbers behind each growth option."),
                     ("Lender and investor support.", "Business plans, forecasts and the figures lenders and investors ask for, with support through their questions.")],
        "scope": [("Monthly review", "Prepare the pack and walk you through it", "Join one call a month"),
                  ("Cash forecast", "Keep it up to date and flag risks early", "Share plans: hires, contracts, big purchases"),
                  ("Big decisions", "Model the options and give a clear recommendation", "Make the decision"),
                  ("Lenders and investors", "Prepare the figures and join meetings where useful", "Lead the relationship")],
        "related": [("Business advisory", "/services/business-advisory"), ("Monthly bookkeeping", "/services/bookkeeping"), ("Bookkeeping vs management accounts", "/blog/bookkeeping-vs-management-accounts")],
        "suits": "This suits you if your business has outgrown basic bookkeeping and you want senior finance input every month, without hiring a full-time finance director.",
        "not": "If you only need your books kept and your returns filed, our monthly bookkeeping and VAT services will be enough. We will say so on the call.",
        "fee": "A fixed monthly fee, based on how much time you need each month. Agreed in writing before any work starts, and reviewed with you as the business grows.",
        "faq_h": "Virtual CFO questions",
        "faqs": [("What is the difference between a Virtual CFO and an accountant?", "An accountant keeps your records and files your returns. A Virtual CFO uses those figures to plan ahead and advise on decisions. Many clients use both, from the same team."),
                 ("How often will we meet?", "Usually once a month, with more contact around big decisions, year end or a funding round."),
                 ("Can a Virtual CFO help us raise money?", "Yes. We prepare the business plan, forecasts and investor or lender pack, and support you through their questions and checks."),
                 ("Do we need monthly bookkeeping as well?", "You need up-to-date books. If ours is the team keeping them, your Virtual CFO works from current figures every month.")],
        "close_h": "Get a finance director in your corner",
        "close_p": "In 20 minutes we will look at where your business is heading and how much finance support would help.",
    })


INDUSTRY_TEXT = [
    ("healthcare", "Healthcare and care",
     "Our roots are in healthcare staffing, through Aviteus Healthcare. We know the payroll pressure of shift work and agency staff, and the cash flow of long contract payment terms.",
     [("Payroll for shift and agency staff,", "with changing hours, rates and holiday pay."),
      ("Cash flow planning", "for contracts that pay weeks after the work is done."),
      ("VAT checks", "for health and care services, where some income can be exempt.")],
     [("Payroll and pensions", "/services/payroll"), ("Bookkeeping and management accounts", "/services/bookkeeping")]),
    ("construction", "Construction",
     "Construction businesses deal with the Construction Industry Scheme (CIS), stage payments, retentions and tight margins on every job.",
     [("CIS deductions and monthly returns,", "for contractors and subcontractors."),
      ("Job costing,", "so you see the margin on each contract, not just the year."),
      ("VAT on construction services,", "including the domestic reverse charge.")],
     [("VAT and year-end tax", "/services/vat-tax"), ("Payroll and pensions", "/services/payroll")]),
    ("ecommerce", "E-commerce",
     "Online sellers deal with many sales channels, many fees and VAT on sales to customers in other countries.",
     [("Reconciling sales channels:", "Amazon, Shopify, eBay and payment providers, matched to your bank."),
      ("Stock and cost of sales,", "so profit per product is real, not a guess."),
      ("VAT on online and overseas sales,", "set up correctly in your software.")],
     [("Accounting software set-up", "/services/accounting-software"), ("VAT and year-end tax", "/services/vat-tax")]),
]


def industries(data):
    crumbs = [("Home", "/"), ("Industries", "/industries")]
    secs = []
    for i, (slug, name, intro, items, links) in enumerate(INDUSTRY_TEXT):
        alt = " section--alt" if i % 2 == 0 else ""
        lis = "".join(f"<li><b>{a}</b> {b}</li>" for a, b in items)
        secs.append(f'''<section class="section{alt}" id="{slug}" aria-labelledby="{slug}-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="{slug}-h">{name}</h2></div>
    <div><p class="lead">{intro}</p><ul class="ticks mt-6">{lis}</ul>{related(links + [("All services", "/services")])}</div>
  </div>
</section>''')
    body = f'''
<section class="hero hero--simple" aria-labelledby="h1">
  <div class="wrap read">
    {crumbs_html(crumbs)}
    <h1 id="h1">Industries we work with</h1>
    <p class="lead">We serve SMEs and startups across the UK. Three sectors get specialist attention: healthcare and care, construction, and e-commerce.</p>
    <nav class="jump mt-6" aria-label="Jump to an industry">{"".join(f'<a href="#{s}">{n}</a>' for s, n, *_ in INDUSTRY_TEXT)}</nav>
  </div>
</section>
{"".join(secs)}
{close_band("Talk to someone who knows your sector", "Book a 20-minute review and we will look at the questions your industry raises for your books, payroll and tax.")}'''
    return page(path="/industries", title="Healthcare, Construction and E-commerce Accounting | Aviteus",
                description="Accounting, payroll and tax for UK healthcare and care providers, construction businesses and online sellers, from a team with roots in healthcare.",
                h_active="industries", body_html=body, page_type="industries",
                ld=[{"@type": "CollectionPage", "url": f"{SITE}/industries", "name": "Industries we work with", "about": {"@id": f"{SITE}/#business"}, "inLanguage": "en-GB"},
                    breadcrumb_ld(crumbs)], data=data)


# ---------------------------------------------------------------- Free tools (new copy: reviewer to confirm the VAT rules and threshold)
TOOLS = [
    ("/deadline-finder", "UK deadline finder", "Your next VAT, corporation tax, Companies House, payroll and Self Assessment dates, in date order, for the next 12 months.", "Find my dates"),
    ("/tools/vat-threshold-checker", "VAT registration checker", "Enter your monthly taxable turnover. See your rolling 12-month total, your headroom, and when you would go over the threshold.", "Check my turnover"),
    ("/tools/switching-checklist", "Switching accountant checklist", "Every step of changing accountant, in order. Tick them off as you go: your progress is saved in your browser.", "Open the checklist"),
]


def tools_hub(data):
    cards = "".join(f'''<article class="tool-card">
  <h2><a href="{u}">{t}</a></h2><p>{d}</p><a class="av-link" href="{u}">{c} {ARROW}</a>
</article>''' for u, t, d, c in TOOLS)
    body = f'''
<section class="hero hero--simple" aria-labelledby="h1">
  <div class="wrap read">
    {crumbs_html([("Home", "/"), ("Free tools", "/tools")])}
    <p class="av-eyebrow">Free · No sign-up</p>
    <h1 id="h1" class="mt-4">Free tools for UK business owners</h1>
    <p class="lead">Three quick tools for the questions owners ask us most. They work in your browser, and nothing you enter is stored or sent.</p>
  </div>
</section>
<section class="section" style="padding-top:0" aria-label="Tools">
  <div class="wrap"><div class="tool-grid">{cards}</div></div>
</section>
{close_band("Want a person to check your figures?", "Book a free 20-minute review. We will look at your dates, your turnover and your books with you, and tell you what needs doing.")}'''
    items = [{"@type": "ListItem", "position": i + 1, "name": t, "url": f"{SITE}{u}"} for i, (u, t, d, c) in enumerate(TOOLS)]
    return page(path="/tools", title="Free Tools for UK Business Owners | Aviteus",
                description="Free tools for UK business owners: a tax deadline finder, a VAT registration checker and a switching accountant checklist. No sign-up needed.",
                h_active="tools", body_html=body, page_type="tools",
                ld=[{"@type": "ItemList", "name": "Free tools", "itemListElement": items}, breadcrumb_ld([("Home", "/"), ("Free tools", "/tools")])], data=data)


def vat_checker(data):
    th = int(data.get("vat_threshold", 90000))
    crumbs = [("Home", "/"), ("Free tools", "/tools"), ("VAT registration checker", "/tools/vat-threshold-checker")]
    faqs = [
        ("When do I have to register for VAT?", f"When your VAT-taxable turnover for the last 12 months goes over the registration threshold (£{th:,} in this tool), or when you expect to go over it in the next 30 days alone."),
        ("How long do I have to register?", "If your rolling 12-month total goes over, register within 30 days of the end of the month you went over. If you expect to go over in the next 30 days alone, register by the end of that 30-day period."),
        ("What counts as VAT-taxable turnover?", "The total value of everything you sell that is not exempt from VAT. Exempt sales, such as some health, education and insurance services, do not count."),
        ("Can I register before I reach the threshold?", "Yes. Some businesses register voluntarily, for example to reclaim VAT on costs. Whether it suits you depends on who your customers are. We go through this on a review call."),
    ]
    body = f'''
<section class="hero hero--simple" aria-labelledby="h1">
  <div class="wrap read">
    {crumbs_html(crumbs)}
    <p class="av-eyebrow">Free tool · No sign-up</p>
    <h1 id="h1" class="mt-4">VAT registration checker</h1>
    <p class="lead">Enter your VAT-taxable turnover for each of the last 12 months. You will see your rolling total, how much headroom you have, and roughly when you would go over the threshold.</p>
  </div>
</section>
<section class="section" style="padding-top:0" aria-label="VAT registration checker">
  <div class="wrap finder">
    <form class="form-card form" id="vat-form" data-threshold="{th}" aria-labelledby="vat-h" novalidate>
      <div><h2 id="vat-h">Your taxable turnover</h2><p class="hint mt-4">Sales that are not exempt from VAT, before any VAT is added. Round figures are fine.</p></div>
      <div class="month-grid" id="vat-months"><noscript><p>This tool needs JavaScript. The rules are listed below.</p></noscript></div>
      <button class="av-btn av-btn--outline av-btn--small" type="button" id="vat-fill">Copy the first month to all months</button>
      <div class="field"><label for="vat-next30">Expected taxable turnover in the next 30 days alone (optional)</label><input class="av-input av-num" id="vat-next30" name="next30" inputmode="decimal" placeholder="0"></div>
    </form>
    <div>
      <div id="vat-result" aria-live="polite"></div>
      <div class="callout mt-6">
        <h2 style="font-size:24px;line-height:30px">Close to the threshold?</h2>
        <p class="mt-4">Book a 20-minute review. We will check your figures, tell you whether to register now or wait, and set up VAT in your software.</p>
        <div class="close-actions mt-5">{book_btn("vat_checker")}{wa_btn("vat_checker_whatsapp", "vat")}</div>
      </div>
      <p class="note mt-5">This tool uses a threshold of £{th:,}. Check the current figure on GOV.UK before you rely on the result.</p>
    </div>
  </div>
</section>
<section class="section section--alt" aria-labelledby="faq-h">
  <div class="wrap split">
    <div class="head" style="margin:0"><h2 id="faq-h">VAT registration questions</h2></div>
    <div>{faq_html(faqs)}{related([("VAT and year-end tax", "/services/vat-tax"), ("VAT returns and Making Tax Digital", "/blog/vat-returns-making-tax-digital"), ("UK deadline finder", "/deadline-finder"), ("All free tools", "/tools")])}</div>
  </div>
</section>
{close_band("Get VAT set up right first time", "In 20 minutes we will tell you when to register, which VAT scheme fits, and what changes in your software.", "vat")}'''
    return page(path="/tools/vat-threshold-checker", title="VAT Registration Threshold Checker UK | Aviteus",
                description="Free VAT registration checker. Enter 12 months of taxable turnover to see your rolling total, your headroom and when you would cross the threshold.",
                h_active="tools", body_html=body, page_type="tool", service="vat",
                extra_js='<script src="/assets/tools.js" defer></script>',
                ld=[{"@type": "WebApplication", "name": "VAT registration checker", "url": f"{SITE}/tools/vat-threshold-checker", "applicationCategory": "FinanceApplication", "operatingSystem": "Any",
                     "offers": {"@type": "Offer", "price": "0", "priceCurrency": "GBP"}, "provider": {"@id": f"{SITE}/#business"}, "inLanguage": "en-GB"},
                    breadcrumb_ld(crumbs), faq_ld(faqs)], data=data)


SWITCH_STEPS = [
    ("Before you switch", [
        ("s1", "Read your engagement letter", "Check the notice period and how fees are settled when you leave."),
        ("s2", "Clear or agree any unpaid fees", "Unpaid fees are the most common reason a handover slows down."),
        ("s3", "Get a written scope from the new firm", "What they do, what you do, when, and the fixed fee."),
        ("s4", "Agree the takeover date", "Ideally the start of your next VAT quarter or your next pay run."),
    ]),
    ("Telling people", [
        ("s5", "Email your current accountant", "A short, polite note with the date you are moving."),
        ("s6", "Let the new firm request professional clearance", "They write to your old firm. You do not need to do anything."),
    ]),
    ("Authority and access", [
        ("s7", "Approve the new firm as your HMRC agent", "For corporation tax, VAT, PAYE and Self Assessment, as each request arrives."),
        ("s8", "Move your accounting software into your company's name", "If the old firm holds the subscription, ask them to transfer it."),
        ("s9", "Find your Companies House authentication code", "Needed to file accounts and the confirmation statement."),
    ]),
    ("Records to hand over", [
        ("s10", "Last year's accounts and tax returns", "The opening figures for this year."),
        ("s11", "VAT returns filed this year", "So the next return starts from the right place."),
        ("s12", "Payroll year-to-date figures for each employee", "Needed if payroll moves part way through the year."),
        ("s13", "Your tax references", "UTR, VAT number, PAYE and Accounts Office references."),
    ]),
    ("After the switch", [
        ("s14", "Check the first monthly report", "Confirm the opening balances and your next deadlines are right."),
        ("s15", "Put your next three deadlines in your calendar", "Your new firm should give you these on day one."),
    ]),
]


def switching_checklist(data):
    crumbs = [("Home", "/"), ("Free tools", "/tools"), ("Switching checklist", "/tools/switching-checklist")]
    total = sum(len(items) for _, items in SWITCH_STEPS)
    groups = []
    for title, items in SWITCH_STEPS:
        lis = "".join(f'''<li class="check-item"><input type="checkbox" id="{i}"><label for="{i}" class="ci-text"><b>{a}</b><span>{b}</span></label></li>''' for i, a, b in items)
        groups.append(f'<fieldset class="check-group"><legend>{title}</legend><ul>{lis}</ul></fieldset>')
    body = f'''
<section class="hero hero--simple" aria-labelledby="h1">
  <div class="wrap read">
    {crumbs_html(crumbs)}
    <p class="av-eyebrow">Free tool · No sign-up</p>
    <h1 id="h1" class="mt-4">Switching accountant checklist</h1>
    <p class="lead">Every step of changing accountant, in the order you do them. Tick each one as you go. Your progress is saved in this browser only.</p>
  </div>
</section>
<section class="section" style="padding-top:0" aria-label="Checklist">
  <div class="wrap finder">
    <div>
      <div class="progress-wrap"><div class="progress" role="progressbar" aria-label="Checklist progress" aria-valuemin="0" aria-valuemax="{total}" aria-valuenow="0"><span id="switch-progress"></span></div><p class="small" id="switch-count">0 of {total} done</p></div>
      <div id="switch-list" class="mt-5">{"".join(groups)}</div>
      <div class="close-actions mt-6"><button class="av-btn av-btn--outline av-btn--small" type="button" id="switch-copy">Copy the checklist</button><button class="av-btn av-btn--small" type="button" id="switch-reset" style="background:transparent;color:var(--ink);box-shadow:inset 0 0 0 1px var(--line-strong)">Start again</button></div>
    </div>
    <div class="post-side" style="top:112px">
      <div class="callout">
        <h2 style="font-size:24px;line-height:30px">Would you rather we did it?</h2>
        <p class="mt-4">When you switch to Aviteus, we handle clearance, HMRC authority and the handover, timed around your next payroll run and VAT date. You send one email.</p>
        <div class="close-actions mt-5">{book_btn("switch_checklist")}</div>
      </div>
      <p class="note">Read the full guide: <a class="ilink" href="/blog/how-to-change-accountant-uk">How to change accountant in the UK</a>.</p>
    </div>
  </div>
</section>
{close_band("Switch without missing a deadline", "Book a 20-minute review and we will plan your move around your next payroll run and VAT date.")}'''
    return page(path="/tools/switching-checklist", title="Switching Accountant Checklist for UK Businesses | Aviteus",
                description="Free switching accountant checklist: every step from your engagement letter to HMRC authority and the records to hand over. Tick as you go.",
                h_active="tools", body_html=body, page_type="tool",
                extra_js='<script src="/assets/tools.js" defer></script>',
                ld=[{"@type": "HowTo", "name": "How to change accountant in the UK", "url": f"{SITE}/tools/switching-checklist", "inLanguage": "en-GB",
                     "step": [{"@type": "HowToStep", "name": a, "text": b} for _, items in SWITCH_STEPS for _, a, b in items]},
                    breadcrumb_ld(crumbs)], data=data)
