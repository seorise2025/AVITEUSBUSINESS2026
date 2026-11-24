"""Shared page shell: head (SEO, social, structured data), header, footer, sticky bar, cookie banner."""
import json
from html import escape

SITE = "https://www.aviteusbusiness.co.uk"
PHONE = "020 4628 8209"
PHONE_TEL = "tel:02046288209"
WA_NUMBER = "447570359908"
WA_DISPLAY = "+44 7570 359908"
EMAIL = "info@aviteusbusiness.co.uk"
ADDRESS = "Alpha House, 296 Kenton Road, Harrow HA3 8DD"
REG_OFFICE = "296 Kenton Road, Harrow HA3 8DD"
COMPANY_NO = "16694378"
CH_URL = "https://find-and-update.company-information.service.gov.uk/company/16694378"

WA_MESSAGES = {
    "general": "Hi Aviteus, I have a question about your services.",
    "bookkeeping": "Hi Aviteus, I have a question about bookkeeping.",
    "payroll": "Hi Aviteus, I have a question about payroll.",
    "vat": "Hi Aviteus, I have a question about VAT or year-end tax.",
}

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
PULSE = '<svg class="av-pulse" viewBox="0 0 160 24" aria-hidden="true" focusable="false"><path d="M0 12 H70 L76 4 L84 22 L92 2 L98 12 H150"/><circle cx="154" cy="12" r="4"/></svg>'


def wa(service="general"):
    from urllib.parse import quote
    return f"https://wa.me/{WA_NUMBER}?text={quote(WA_MESSAGES[service])}"


def book_btn(placement, label="Book a 20-minute review", cls="av-btn av-btn--ember"):
    return f'<a class="{cls}" href="/contact" data-book data-placement="{placement}">{label} {ARROW}</a>'


def wa_btn(placement, service="general", cls="av-btn av-btn--outline"):
    return f'<a class="{cls}" href="{wa(service)}" target="_blank" rel="noopener" data-placement="{placement}">Chat on WhatsApp</a>'


def org_ld():
    """The business entity, shared by every page's structured data."""
    return {
        "@type": ["AccountingService", "LocalBusiness"],
        "@id": f"{SITE}/#business",
        "name": "Aviteus Business Solutions",
        "legalName": "Aviteus Business Solutions Ltd",
        "url": f"{SITE}/",
        "logo": f"{SITE}/assets/img/aviteus-business-logo.png",
        "image": f"{SITE}/assets/img/og-default.png",
        "description": "Monthly bookkeeping, payroll and VAT for UK owner-managed businesses. A written scope, one named manager, and a short report on what is done and due.",
        "telephone": "+44 20 4628 8209",
        "email": EMAIL,
        "foundingDate": "2025-09-04",
        "identifier": {"@type": "PropertyValue", "propertyID": "Companies House company number", "value": COMPANY_NO},
        "address": {"@type": "PostalAddress", "streetAddress": "Alpha House, 296 Kenton Road", "addressLocality": "Harrow", "postalCode": "HA3 8DD", "addressCountry": "GB"},
        "areaServed": {"@type": "Country", "name": "United Kingdom"},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "17:00"}],
        "knowsAbout": ["Bookkeeping", "Management accounts", "Payroll", "Workplace pensions", "Real Time Information (RTI)", "VAT returns", "Making Tax Digital", "Year-end accounts", "Corporation tax", "Company tax return (CT600)", "Self Assessment", "Tax planning", "Business advisory", "Virtual CFO", "Business valuation", "Fundraising support", "Audit support", "Company formation", "Xero", "Sage", "QuickBooks", "FreeAgent"],
        "founder": {"@type": "Person", "@id": f"{SITE}/about-us#vikas-pandey", "name": "Vikas Pandey", "jobTitle": "CEO", "sameAs": ["https://www.linkedin.com/in/vikas-pandey-aviteus/"]},
    }


def website_ld():
    return {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "Aviteus Business Solutions", "inLanguage": "en-GB", "publisher": {"@id": f"{SITE}/#business"}}


def breadcrumb_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": f"{SITE}{u}"} for i, (n, u) in enumerate(items)]}


def faq_ld(faqs):
    import re
    def plain(s):
        return re.sub(r"<[^>]+>", "", s)
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in faqs]}


def faq_html(faqs, first_open=True):
    out = ['<div class="faq-list">']
    for i, (q, a) in enumerate(faqs):
        op = " open" if (i == 0 and first_open) else ""
        out.append(f'<details{op}><summary>{q}</summary><div class="answer"><p>{a}</p></div></details>')
    out.append("</div>")
    return "\n".join(out)


def crumbs_html(items):
    lis = []
    for i, (n, u) in enumerate(items):
        if i == len(items) - 1:
            lis.append(f'<li><span aria-current="page">{n}</span></li>')
        else:
            lis.append(f'<li><a href="{u}">{n}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(lis)}</ol></nav>'


def logo_img(width, height, cls="", eager=False):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture><source srcset="/assets/img/aviteus-business-logo.webp" type="image/webp">'
            f'<img src="/assets/img/aviteus-business-logo.png" alt="Aviteus Business Solutions" width="{width}" height="{height}" {load} class="{cls}"></picture>')


# One source for every service: the header panel, the phone menu, the footer and the Services page all read this.
# The seven services match the live site's Services page. Labels reuse the deck's or the live site's own wording.
SERVICE_MAP = [
    {"key": "bookkeeping", "group": "Monthly accounting", "name": "Bookkeeping and management accounts", "url": "/services/bookkeeping",
     "line": "Books reconciled every month, plus a short management pack.",
     "items": [("Monthly bookkeeping", "/services/bookkeeping"), ("Bank and card reconciliation", "/services/bookkeeping#monthly"),
               ("Monthly management accounts pack", "/services/bookkeeping#monthly"), ("Catch-up bookkeeping", "/services/bookkeeping#catch-up")]},
    {"key": "payroll", "group": "Monthly accounting", "name": "Payroll and pensions", "url": "/services/payroll",
     "line": "Staff paid on the right day. RTI and auto enrolment handled.",
     "items": [("Monthly payroll and payslips", "/services/payroll#payroll-month"), ("RTI submissions to HMRC", "/services/payroll#handle"),
               ("Workplace pensions and auto enrolment", "/services/payroll#handle"), ("Moving payroll part way through the year", "/services/payroll#switch")]},
    {"key": "vat", "group": "Tax", "name": "VAT and year-end tax", "url": "/services/vat-tax",
     "line": "VAT, year-end accounts, corporation tax, tax planning and audit support.",
     "items": [("VAT returns under Making Tax Digital", "/services/vat-tax#file"), ("Year-end accounts and corporation tax", "/services/vat-tax#deadlines"),
               ("Tax planning", "/services/vat-tax#tax-planning"), ("Audit support", "/services/vat-tax#audit-support")]},
    {"key": "self-assessment", "group": "Tax", "name": "Self Assessment tax returns", "url": "/services/self-assessment",
     "line": "Personal tax returns, filed before 31 January.",
     "items": [("Registering for Self Assessment", "/services/self-assessment#included"), ("Preparing and filing your return", "/services/self-assessment#included"),
               ("Payments on account explained", "/services/self-assessment#dates"), ("Key Self Assessment dates", "/services/self-assessment#dates")]},
    {"key": "advisory", "group": "Growth and advice", "name": "Business advisory", "url": "/services/business-advisory",
     "line": "Forecasts, budgets, pricing, valuations and fundraising support.",
     "items": [("Cash flow forecasts and budgets", "/services/business-advisory#included"), ("Pricing and cost reviews", "/services/business-advisory#included"),
               ("Business valuation", "/services/business-advisory#included"), ("Fundraising support", "/services/business-advisory#included")]},
    {"key": "virtual-cfo", "group": "Growth and advice", "name": "Virtual CFO", "url": "/services/virtual-cfo",
     "line": "A part-time finance director for growing businesses.",
     "items": [("Monthly finance review", "/services/virtual-cfo#included"), ("Financial management and KPIs", "/services/virtual-cfo#included"),
               ("Strategic financial planning", "/services/virtual-cfo#included"), ("Lender and investor support", "/services/virtual-cfo#included")]},
    {"key": "formation", "group": "Company and software", "name": "Company formation and compliance", "url": "/services/company-formation",
     "line": "Company set-up, HMRC registrations and Companies House filings.",
     "items": [("Limited company set-up", "/services/company-formation#included"), ("HMRC registrations", "/services/company-formation#included"),
               ("Confirmation statement and Companies House filings", "/services/company-formation#included"), ("Company secretarial tasks", "/services/company-formation#included")]},
    {"key": "software", "group": "Company and software", "name": "Accounting software set-up and training", "url": "/services/accounting-software",
     "line": "Xero, QuickBooks, Sage and FreeAgent: set-up, clean-up and training.",
     "items": [("Choosing the right software", "/services/accounting-software#included"), ("Set-up and moving your records", "/services/accounting-software#included"),
               ("Cleaning up an existing file", "/services/accounting-software#included"), ("Training for you and your team", "/services/accounting-software#included")]},
]
SERVICE_GROUPS = ["Monthly accounting", "Tax", "Growth and advice", "Company and software"]
ALSO_AVAILABLE = [("Catch-up bookkeeping", "/services/bookkeeping#catch-up")]


def header(active):
    def cur(k):
        return ' aria-current="page"' if active == k else ""
    chev = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
    svc_active = active in [s["key"] for s in SERVICE_MAP] + ["services"]
    cols = []
    for g in SERVICE_GROUPS:
        svcs = "".join(f'''<li><a class="mega-svc" href="{s["url"]}"{cur(s["key"])}><b>{s["name"]}</b><span>{s["line"]}</span></a></li>'''
                       for s in SERVICE_MAP if s["group"] == g)
        cols.append(f'<div class="mega-col"><p class="mega-group">{g}</p><ul>{svcs}</ul></div>')
    also = "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in ALSO_AVAILABLE)
    m_groups = "".join(
        f'''<li class="m-group"><span class="m-glabel">{g}</span><ul>{"".join(f'<li><a href="{s["url"]}">{s["name"]}</a></li>' for s in SERVICE_MAP if s["group"] == g)}</ul></li>'''
        for g in SERVICE_GROUPS)
    return f'''<header class="site-header">
  <div class="wrap">
    <a class="av-logo" href="/" aria-label="Aviteus Business Solutions home">{logo_img(168, 74, eager=True)}</a>
    <ul class="menu">
      <li class="has-sub">
        <button class="menu-btn{" is-current" if svc_active else ""}" type="button" aria-expanded="false" aria-controls="mega-services">Services {chev}</button>
        <div class="mega" id="mega-services" hidden>
          <div class="wrap">
            <div class="mega-grid">
              {"".join(cols)}
            </div>
            <div class="mega-strip">
              <p><span class="mega-strip-label">Who we help</span> <a href="/services#who-we-help">Owner-managed businesses in any sector, across the UK</a></p>
              <p><span class="mega-strip-label">Free tools</span> <a href="/deadline-finder"{cur("finder")}>Deadline finder</a> <a href="/tools/vat-threshold-checker">VAT checker</a> <a href="/tools/switching-checklist">Switching checklist</a></p>
            </div>
            <div class="mega-foot">
              <a class="av-link" href="/services"{cur("services")}>All services, side by side {ARROW}</a>
              <span class="mega-cta"><span>Not sure which you need?</span> <a class="av-btn av-btn--ember av-btn--small" href="/contact" data-book data-placement="mega_menu">Book a 20-minute review</a></span>
            </div>
          </div>
        </div>
      </li>
      <li><a href="/tools"{cur("tools")}>Free tools</a></li>
      <li><a href="/about-us"{cur("about")}>About us</a></li>
      <li><a href="/blog"{cur("blog")}>Blog</a></li>
      <li><a class="header-phone" href="{PHONE_TEL}" data-placement="header">{PHONE}</a></li>
    </ul>
    <a class="av-btn av-btn--ember av-btn--small header-cta" href="/contact" data-book data-placement="header">Book a review</a>
    <button class="av-menu-toggle nav-toggle" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h10M4 17h16"/></svg></button>
  </div>
  <nav class="mobile-nav wrap" id="mobile-nav" aria-label="Main">
    <p class="m-label">Our services</p>
    <ul class="m-services">
      {m_groups}
    </ul>
    <ul class="m-main">
      <li><a href="/services">All services</a></li>
      <li><a href="/about-us">About us</a></li>
      <li><a href="/tools">Free tools</a></li>
      <li><a href="/blog">Blog</a></li>
      <li><a href="{PHONE_TEL}" data-placement="mobile_menu">Call {PHONE}</a></li>
    </ul>
  </nav>
</header>'''


def footer(data):
    linkedin = f'<li><a href="{escape(data["linkedin_company_url"])}" target="_blank" rel="noopener">LinkedIn</a></li>' if data.get("linkedin_company_url") else ""
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <span class="av-logo av-logo--plate">{logo_img(150, 66)}</span>
        <p class="mt-4">Aviteus Business Solutions. Monthly bookkeeping, payroll and VAT for UK owner-managed businesses.</p>
      </div>
      <div>
        <h2>Services</h2>
        <ul>
          {"".join(f'<li><a href="{s["url"]}">{s["name"]}</a></li>' for s in SERVICE_MAP)}
          <li><a href="/services">All services</a></li>
        </ul>
      </div>
      <div>
        <h2>Company</h2>
        <ul>
          <li><a href="/about-us">About us</a></li>
          <li><a href="/services#who-we-help">Who we work with</a></li>
          <li><a href="/tools">Free tools</a></li>
          <li><a href="/deadline-finder">UK deadline finder</a></li>
          <li><a href="/tools/vat-threshold-checker">VAT registration checker</a></li>
          <li><a href="/tools/switching-checklist">Switching checklist</a></li>
          <li><a href="/blog">Blog</a></li>
          <li><a href="/contact" data-book data-placement="footer">Book a review</a></li>
          {linkedin}
        </ul>
      </div>
      <div>
        <h2>Contact</h2>
        <ul>
          <li><a class="num" href="{PHONE_TEL}" data-placement="footer">{PHONE}</a></li>
          <li><a href="{wa()}" target="_blank" rel="noopener" data-placement="footer">WhatsApp <span class="num">{WA_DISPLAY}</span></a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{ADDRESS}</li>
          <li>Monday to Friday, 9am to 5pm. Saturday by appointment. Sunday closed.</li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <p>&copy; 2026 Aviteus Business Solutions Ltd. Registered in England and Wales, company number {COMPANY_NO}. Registered office: {REG_OFFICE}.</p>
      <nav aria-label="Legal"><a href="/privacy-policy">Privacy notice</a><a href="/terms-and-conditions">Terms and conditions</a><a href="/cookies">Cookies</a><a href="#" data-cookie-settings>Cookie settings</a></nav>
    </div>
  </div>
</footer>'''


def sticky_bar(service):
    return f'''<div class="sticky-bar" id="sticky-bar" hidden>
  <a class="av-btn av-btn--ember" href="/contact" data-book data-placement="sticky_bar">Book a review</a>
  <a class="av-btn av-btn--outline" href="{wa(service)}" target="_blank" rel="noopener" data-placement="sticky_bar">Chat on WhatsApp</a>
</div>'''


COOKIE = '''<div class="cookie" id="cookie" role="region" aria-label="Cookie choice" hidden>
  <p>We use essential cookies to run this site. With your permission, we also use analytics cookies to see which pages help people. We do not use advertising cookies.</p>
  <div class="actions">
    <button class="av-btn av-btn--ember" type="button" data-consent="granted">Accept analytics</button>
    <button class="av-btn av-btn--ember" type="button" data-consent="denied">Reject analytics</button>
  </div>
  <p class="mt-4 small"><a href="/cookies">Cookie details</a></p>
</div>'''


# ---------------------------------------------------------------- Lead form (multi-step, qualifies the lead)
LF_SERVICES = [(s["key"], s["name"]) for s in SERVICE_MAP] + [("switching", "Switching from my current accountant"), ("practice", "Extra capacity for my accountancy practice"), ("not_sure", "Not sure yet")]


def _chips(name, options, kind="radio", checked=()):
    return '<div class="choices">' + "".join(
        f'<label class="choice"><input type="{kind}" name="{name}" value="{v}"{" checked" if v in checked else ""}><span>{t}</span></label>' for v, t in options) + "</div>"


def _group(name, legend, body, hint="", required=True):
    opt = "" if required else ' <span class="opt">(optional)</span>'
    h = f'<p class="hint">{hint}</p>' if hint else ""
    return f'<fieldset class="field" id="lf-{name}-wrap"><legend>{legend}{opt}</legend>{h}{body}<p class="err" id="lf-{name}-err"></p></fieldset>'


def _select(name, label, options, required=False):
    opt = "" if required else ' <span class="opt">(optional)</span>'
    ops = '<option value="">Choose one</option>' + "".join(f'<option value="{v}">{t}</option>' for v, t in options)
    return f'<div class="field" id="lf-{name}-wrap"><label for="lf-{name}">{label}{opt}</label><select class="av-input" id="lf-{name}" name="{name}">{ops}</select><p class="err" id="lf-{name}-err"></p></div>'


def lead_form(preselect=(), title="Tell us what you need help with", intro="Five short steps, most of them one tap. It helps us prepare, so your free 20-minute review is useful from the first minute."):
    s1 = _group("services", "What do you need help with?", _chips("services", LF_SERVICES, "checkbox", preselect), "Choose all that apply.")
    s2 = (_group("business_type", "What type of business is it?", _chips("business_type", [("limited", "Limited company"), ("sole_trader", "Sole trader"), ("partnership", "Partnership or LLP"), ("not_set_up", "Not set up yet"), ("practice", "Accountancy practice")]))
          + _group("staff", "How many people work in the business, including you?", _chips("staff", [("solo", "Just me"), ("2_9", "2 to 9"), ("10_49", "10 to 49"), ("50_plus", "50 or more")]))
          + _group("turnover", "Roughly what is your yearly turnover?", _chips("turnover", [("under_90k", "Under £90,000"), ("90k_250k", "£90,000 to £250,000"), ("250k_1m", "£250,000 to £1 million"), ("1m_5m", "£1 million to £5 million"), ("over_5m", "Over £5 million"), ("undisclosed", "Prefer not to say")]))
          + _group("vat_registered", "Are you VAT registered?", _chips("vat_registered", [("yes", "Yes"), ("no", "No"), ("not_sure", "Not sure")]), required=False)
          + _select("industry", "Which industry are you in?", [("charity", "Charity or not for profit"), ("construction", "Construction and trades"), ("creative", "Creative and media"), ("ecommerce", "E-commerce"), ("healthcare", "Healthcare and care"), ("hospitality", "Hospitality"), ("manufacturing", "Manufacturing"), ("professional", "Professional services"), ("property", "Property and lettings"), ("retail", "Retail"), ("technology", "Technology"), ("transport", "Transport and logistics"), ("other", "Something else")]))
    s3 = (_group("books_now", "Who keeps your books today?", _chips("books_now", [("accountant", "An accountant or bookkeeper"), ("self_software", "Me, in accounting software"), ("spreadsheets", "Spreadsheets"), ("paper", "Paper or a shoebox"), ("not_started", "Not started yet")]), required=False)
          + _select("software", "Which software, if any?", [("xero", "Xero"), ("quickbooks", "QuickBooks"), ("sage", "Sage"), ("freeagent", "FreeAgent"), ("other", "Something else"), ("none", "None")])
          + _group("books_status", "How up to date are your books?", _chips("books_status", [("up_to_date", "Up to date"), ("behind_1_3", "1 to 3 months behind"), ("behind_3_plus", "More than 3 months behind"), ("not_sure", "Not sure")]))
          + _group("deadlines", "Any deadlines in the next 60 days?", _chips("deadlines", [("vat", "A VAT return"), ("accounts", "Year-end accounts"), ("corp_tax", "Corporation tax payment"), ("sa", "Self Assessment"), ("payroll", "Payroll year-end"), ("none", "None that I know of"), ("not_sure", "Not sure")], "checkbox"), "Choose all that apply.", required=False)
          + '<div class="field" id="lf-message-wrap"><label for="lf-message">What would you like to change?</label><p class="hint" id="lf-message-hint">In a sentence or two. For example: our books are three months behind, or we want to move payroll before the new tax year.</p><textarea class="av-input" id="lf-message" name="message" rows="4" maxlength="2000" aria-describedby="lf-message-hint lf-message-err"></textarea><p class="err" id="lf-message-err"></p></div>')
    s4 = (_group("start", "When would you like to start?", _chips("start", [("two_weeks", "Within 2 weeks"), ("month", "Within a month"), ("quarter", "In 1 to 3 months"), ("researching", "Just researching for now")]))
          + _group("decision", "Who makes the decision?", _chips("decision", [("yes", "I do"), ("shared", "I decide with a partner or director"), ("other", "I am gathering information for someone else")]))
          + _group("budget", "Do you have a rough monthly budget in mind?", _chips("budget", [("under_150", "Under £150"), ("150_300", "£150 to £300"), ("300_600", "£300 to £600"), ("600_plus", "Over £600"), ("not_sure", "Not sure yet")]), "It helps us suggest the right scope. It is not a quote.", required=False)
          + _select("source", "How did you hear about us?", [("google", "Google search"), ("linkedin", "LinkedIn"), ("referral", "A referral"), ("directory", "A software or adviser directory"), ("ai", "An AI assistant, such as ChatGPT"), ("other", "Something else")]))
    s5 = (f'''<div class="field" id="lf-name-wrap"><label for="lf-name">Full name</label><input class="av-input" id="lf-name" name="name" autocomplete="name" maxlength="100"><p class="err" id="lf-name-err"></p></div>
<div class="field" id="lf-email-wrap"><label for="lf-email">Email</label><input class="av-input" id="lf-email" name="email" type="email" autocomplete="email"><p class="err" id="lf-email-err"></p></div>
<div class="field"><label for="lf-company">Company or website <span class="opt">(optional)</span></label><input class="av-input" id="lf-company" name="company" autocomplete="organization" maxlength="200"></div>'''
          + _group("reply_method", "How should we reply?", _chips("reply_method", [("email", "Email"), ("phone", "Phone call"), ("whatsapp", "WhatsApp")], checked=("email",)), required=False)
          + f'''<div class="field" id="lf-phone-wrap"><label for="lf-phone">Phone number (optional)</label><p class="hint">Include the country code if it is not a UK number.</p><input class="av-input" id="lf-phone" name="phone" type="tel" autocomplete="tel"><p class="err" id="lf-phone-err"></p></div>'''
          + _group("best_time", "Best time to call?", _chips("best_time", [("morning", "Morning"), ("afternoon", "Afternoon"), ("any", "Any time")]), required=False)
          + '''<label class="check"><input type="checkbox" name="newsletter" value="yes"><span>Send me occasional emails about UK tax deadlines and changes. You can unsubscribe at any time.</span></label>
<div class="hp" aria-hidden="true"><label for="lf-website">Leave this empty</label><input id="lf-website" name="website" tabindex="-1" autocomplete="off"></div>
<p class="privacy">We use these details only to reply to your enquiry. Read our <a class="tlink" href="/privacy-policy">privacy notice</a>.</p>''')
    steps = [("What you need", s1), ("Your business", s2), ("Where things stand", s3), ("Timing", s4), ("Your details", s5)]
    step_html = "".join(f'<div class="lf-step" data-title="{t}"{" hidden" if i else ""}>{b}</div>' for i, (t, b) in enumerate(steps))
    return f'''<div class="form-card lf-card" id="review">
  <div class="lf-head"><h2 id="lf-h">{title}</h2><p class="small mt-4">{intro}</p>
    <div class="lf-progress"><div class="lf-bar" aria-hidden="true"><span></span></div><p class="lf-count small" aria-live="polite">Step 1 of 5: What you need</p></div></div>
  <div class="err-summary" id="lf-summary" tabindex="-1" role="alert"><h2>There is 1 problem with your enquiry</h2><ul></ul></div>
  <div class="form-status" id="lf-status" role="status" aria-live="polite"></div>
  <form class="form lead-form" id="lead-form" novalidate aria-labelledby="lf-h">
    {step_html}
    <div class="lf-nav">
      <button class="av-btn av-btn--outline av-btn--small" type="button" data-lf-back hidden>Back</button>
      <button class="av-btn av-btn--ember" type="button" data-lf-next>Next {ARROW}</button>
      <button class="av-btn av-btn--ember" type="submit" data-lf-send hidden>Send enquiry</button>
    </div>
    <p class="send-note">Free. No obligation. We reply within one business day.</p>
    <p class="small">Prefer to message? <a class="tlink" href="{wa()}" target="_blank" rel="noopener" data-placement="under_form">Chat on WhatsApp</a></p>
  </form>
</div>'''


def lead_section(preselect=(), heading="Get your free 20-minute review", lead="Tell us a little about your business and we will come to the call prepared. You will leave knowing what is behind, what is due next, and whether we are the right fit.", alt=True):
    return f'''<section class="section{" section--alt" if alt else ""} lead-section" aria-labelledby="ls-h">
  <div class="wrap split">
    <div class="head" style="margin:0">
      <p class="av-eyebrow">Free · 20 minutes · No obligation</p>
      <h2 id="ls-h" class="mt-4">{heading}</h2>
      <p class="lead">{lead}</p>
      <ul class="ticks mt-6">
        <li><b>We listen.</b> You tell us what is going on.</li>
        <li><b>We look.</b> At your software or last return, if you can share it.</li>
        <li><b>We tell you three things:</b> what is behind, what is due next, and whether we can help.</li>
      </ul>
      <p class="small mt-6">Or call <a class="tlink" href="{PHONE_TEL}" data-placement="lead_section">{PHONE}</a>, Monday to Friday, 9am to 5pm.</p>
    </div>
    {lead_form(preselect)}
  </div>
</section>'''


WA_WIDGET = f'''<div class="wa-widget" id="wa-widget" hidden>
  <div class="wa-panel" id="wa-panel" role="dialog" aria-labelledby="wa-title" hidden>
    <div class="wa-top"><div><p class="wa-title" id="wa-title">Aviteus Business Solutions</p><p class="wa-sub">We reply within one business day</p></div><button class="wa-close" type="button" data-wa-close aria-label="Close WhatsApp chat">×</button></div>
    <div class="wa-body">
      <p class="wa-bubble">Hi, how can we help? Pick a topic and WhatsApp opens with your message ready to send.</p>
      <div class="wa-topics">
        <a class="wa-topic" href="{wa("bookkeeping")}" target="_blank" rel="noopener" data-placement="widget_bookkeeping">Bookkeeping</a>
        <a class="wa-topic" href="{wa("payroll")}" target="_blank" rel="noopener" data-placement="widget_payroll">Payroll</a>
        <a class="wa-topic" href="{wa("vat")}" target="_blank" rel="noopener" data-placement="widget_vat">VAT or year-end tax</a>
        <a class="wa-topic" href="{wa()}" target="_blank" rel="noopener" data-placement="widget_general">Something else</a>
      </div>
      <p class="wa-num">Or message <span class="av-num">{WA_DISPLAY}</span></p>
    </div>
  </div>
  <p class="wa-hint" id="wa-hint" hidden><span>Questions? Chat with us on WhatsApp.</span><button type="button" data-wa-hint-close aria-label="Dismiss">×</button></p>
  <button class="wa-fab" type="button" id="wa-fab" aria-expanded="false" aria-controls="wa-panel"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.4 8.4 0 1 1 21 11.5z"/><path d="M9 10h.01M12 10h.01M15 10h.01"/></svg><span>WhatsApp</span></button>
</div>'''


PAGE_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage")


def _page_node(path, title, description, ld, data, noindex):
    """Every page gets one WebPage node, tied to the site, the business and its breadcrumb (entity graph)."""
    url = f"{SITE}{path}"
    ld = [dict(n) for n in ld]
    crumbs = next((n for n in ld if n.get("@type") == "BreadcrumbList"), None)
    if crumbs is not None:
        crumbs["@id"] = f"{url}#breadcrumb"
    main = next((n for n in ld if n.get("@type") in ("Service", "BlogPosting", "WebApplication", "HowTo")), None)
    node = next((n for n in ld if n.get("@type") in PAGE_TYPES), None)
    if node is None:
        node = {"@type": "WebPage", "name": title}
        ld.insert(0, node)
    node.setdefault("@id", f"{url}#webpage")
    node.setdefault("url", url)
    node.setdefault("description", description)
    node.setdefault("isPartOf", {"@id": f"{SITE}/#website"})
    node.setdefault("about", {"@id": f"{SITE}/#business"})
    node.setdefault("publisher", {"@id": f"{SITE}/#business"})
    node.setdefault("inLanguage", "en-GB")
    if data.get("content_updated"):
        node.setdefault("dateModified", data["content_updated"])
    if crumbs is not None:
        node.setdefault("breadcrumb", {"@id": crumbs["@id"]})
    if main is not None and main.get("@id"):
        node.setdefault("mainEntity", {"@id": main["@id"]})
    return ld


def page(*, path, title, description, h_active, body_html, ld, data, page_type, service="general",
         sticky=True, noindex=False, extra_js="", og_title=None, og_desc=None):
    canonical = f"{SITE}{path}"
    graph = [org_ld(), website_ld()] + _page_node(path, title, description, ld, data, noindex)
    ld_json = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=None).replace("</", "<\\/")
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
    ogt = og_title or "Aviteus Business Solutions · Know what's done. Know what's due."
    ogd = og_desc or "Monthly bookkeeping, payroll and VAT for UK owner-managed businesses, with a written scope and one named manager."
    canon = "" if noindex else f'<link rel="canonical" href="{canonical}">'
    return f'''<!doctype html>
<html lang="en-GB" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<meta name="robots" content="{robots}">
{canon}
<meta name="theme-color" content="#0e1422">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Aviteus Business Solutions">
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="{escape(ogt)}">
<meta property="og:description" content="{escape(ogd)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/img/og-default.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Aviteus Business Solutions: monthly bookkeeping, payroll and VAT for UK businesses">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/BricolageGrotesque-Variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/InstrumentSans-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">{ld_json}</script>
</head>
<body class="av" data-page="{page_type}" data-service="{service}">
<a class="skip" href="#main">Skip to content</a>
{header(h_active)}
<main id="main">
{body_html}
</main>
{footer(data)}
{sticky_bar(service) if sticky else ""}
{WA_WIDGET}
{COOKIE}
<script src="/assets/site.js" defer></script>
{'<script src="/assets/leadform.js" defer></script>' if 'id="lead-form"' in body_html else ""}
{extra_js}
</body>
</html>
'''
