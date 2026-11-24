"""Shared page shell: head (SEO, social, structured data), header, footer, sticky bar, cookie banner."""
import json
from html import escape

SITE = "https://www.aviteusbusiness.co.uk"
PHONE = "020 4628 8209"
PHONE_TEL = "tel:02046288209"
WA_NUMBER = "447570359908"
WA_DISPLAY = "+44 7570 359908"
EMAIL = "info@aviteusbusiness.co.uk"
ADDRESS = "296 Kenton Road, Harrow HA3 8DD"
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
        "address": {"@type": "PostalAddress", "streetAddress": "296 Kenton Road", "addressLocality": "Harrow", "postalCode": "HA3 8DD", "addressCountry": "GB"},
        "areaServed": {"@type": "Country", "name": "United Kingdom"},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "17:00"}],
        "knowsAbout": ["Bookkeeping", "Management accounts", "Payroll", "Workplace pensions", "Real Time Information (RTI)", "VAT returns", "Making Tax Digital", "Year-end accounts", "Corporation tax", "Company tax return (CT600)"],
        "founder": {"@type": "Person", "name": "Vikas Pandey"},
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


def header(active):
    def cur(k):
        return ' aria-current="page"' if active == k else ""
    chev = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
    return f'''<header class="site-header">
  <div class="wrap">
    <a class="av-logo" href="/" aria-label="Aviteus Business Solutions home">{logo_img(168, 74, eager=True)}</a>
    <ul class="menu">
      <li class="has-sub">
        <button class="menu-btn" type="button" aria-expanded="false" aria-controls="submenu-services">Services {chev}</button>
        <ul class="submenu" id="submenu-services">
          <li><a href="/services/bookkeeping"{cur("bookkeeping")}>Bookkeeping and management accounts</a></li>
          <li><a href="/services/payroll"{cur("payroll")}>Payroll and pensions</a></li>
          <li><a href="/services/vat-tax"{cur("vat")}>VAT and year-end tax</a></li>
          <li><a href="/services"{cur("services")}>All services</a></li>
          <li><a href="/deadline-finder"{cur("finder")}>Free UK deadline finder</a></li>
        </ul>
      </li>
      <li><a href="/about-us"{cur("about")}>About us</a></li>
      <li><a class="header-phone" href="{PHONE_TEL}" data-placement="header">Call {PHONE}</a></li>
    </ul>
    <a class="av-btn av-btn--ember av-btn--small header-cta" href="/contact" data-book data-placement="header">Book a review</a>
    <button class="av-menu-toggle nav-toggle" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h10M4 17h16"/></svg></button>
  </div>
  <nav class="mobile-nav wrap" id="mobile-nav" aria-label="Main">
    <ul>
      <li><a href="/services">Services</a></li>
      <li class="sub"><a href="/services/bookkeeping">Bookkeeping and management accounts</a></li>
      <li class="sub"><a href="/services/payroll">Payroll and pensions</a></li>
      <li class="sub"><a href="/services/vat-tax">VAT and year-end tax</a></li>
      <li><a href="/about-us">About us</a></li>
      <li><a href="/deadline-finder">Free UK deadline finder</a></li>
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
          <li><a href="/services/bookkeeping">Bookkeeping and management accounts</a></li>
          <li><a href="/services/payroll">Payroll and pensions</a></li>
          <li><a href="/services/vat-tax">VAT and year-end tax</a></li>
          <li><a href="/deadline-finder">Free UK deadline finder</a></li>
        </ul>
      </div>
      <div>
        <h2>Company</h2>
        <ul>
          <li><a href="/about-us">About us</a></li>
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
          <li>Monday to Friday, 9am to 5pm. Saturday by appointment.</li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <p>&copy; 2026 Aviteus Business Solutions Ltd. Registered in England and Wales, company number {COMPANY_NO}. Registered office: {ADDRESS}.</p>
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


def page(*, path, title, description, h_active, body_html, ld, data, page_type, service="general",
         sticky=True, noindex=False, extra_js="", og_title=None, og_desc=None):
    canonical = f"{SITE}{path}"
    graph = [org_ld(), website_ld()] + ld
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
{COOKIE}
<script src="/assets/site.js" defer></script>
{extra_js}
</body>
</html>
'''
