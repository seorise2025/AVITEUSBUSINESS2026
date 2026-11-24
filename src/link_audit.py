"""Internal link audit: contextual links only (header, footer, breadcrumbs and the sticky bar excluded)."""
import os, re, sys
from collections import defaultdict
SITE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")
PAGES = {"index.html": "/", "services.html": "/services", "services/bookkeeping.html": "/services/bookkeeping", "services/payroll.html": "/services/payroll",
         "services/vat-tax.html": "/services/vat-tax", "services/self-assessment.html": "/services/self-assessment",
         "services/business-advisory.html": "/services/business-advisory", "services/company-formation.html": "/services/company-formation",
         "services/accounting-software.html": "/services/accounting-software", "services/virtual-cfo.html": "/services/virtual-cfo", "tools.html": "/tools", "tools/vat-threshold-checker.html": "/tools/vat-threshold-checker", "tools/switching-checklist.html": "/tools/switching-checklist", "about-us.html": "/about-us", "contact.html": "/contact", "deadline-finder.html": "/deadline-finder", "blog.html": "/blog"}
import sys as _s; _s.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from posts import POSTS
for _p in POSTS: PAGES[f"blog/{_p['slug']}.html"] = f"/blog/{_p['slug']}"
inbound = defaultdict(set); outbound = {}
for f, url in PAGES.items():
    html = open(os.path.join(SITE, f)).read()
    main = re.search(r'<main id="main">(.*)</main>', html, re.S).group(1)
    main = re.sub(r'<nav class="crumbs".*?</nav>', "", main, flags=re.S)
    links = set(h.split("#")[0] or url for h in re.findall(r'''href=["'](/[^"']*)["']''', main))
    links.discard(url)
    outbound[url] = sorted(l for l in links if l in PAGES.values())
    for l in outbound[url]: inbound[l].add(url)
print(f"{'page':26} {'in':>3} {'out':>3}  links out to")
for url in PAGES.values():
    print(f"{url:26} {len(inbound[url]):>3} {len(outbound[url]):>3}  {', '.join(outbound[url])}")
