"""Makes a preview copy of site/ that runs as a claude.ai artifact.
Run after build.py:  python3 src/build_artifact.py <output folder>
The live website (site/) is not changed. Differences in the preview copy:
- clean URLs become file names (/contact -> contact.html, /services/payroll -> services-payroll.html)
- the home page loses its <html>/<head>/<body> tags, because claude.ai wraps the main page itself
- the site keeps its light look even if the viewer's claude.ai is set to dark
- window.AV_ARTIFACT is set, so the deadline finder offers "Copy these dates" (downloads are blocked there)"""
import os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
OUT = sys.argv[1]

PAGES = {
    "/": "index.html", "/services": "services.html", "/services/bookkeeping": "services-bookkeeping.html",
    "/services/payroll": "services-payroll.html", "/services/vat-tax": "services-vat-tax.html",
    "/about-us": "about-us.html", "/contact": "contact.html", "/deadline-finder": "deadline-finder.html",
    "/terms-and-conditions": "terms-and-conditions.html", "/privacy-policy": "privacy-policy.html",
    "/cookies": "cookies.html", "/blog": "blog.html",
    "/services/self-assessment": "services-self-assessment.html", "/services/business-advisory": "services-business-advisory.html",
    "/services/company-formation": "services-company-formation.html", "/services/accounting-software": "services-accounting-software.html",
    "/services/virtual-cfo": "services-virtual-cfo.html", "/industries": "industries.html",
}
sys.path.insert(0, os.path.join(ROOT, "src"))
from posts import POSTS  # noqa: E402
for _p in POSTS:
    PAGES[f"/blog/{_p['slug']}"] = f"blog-{_p['slug']}.html"
SOURCES = {v: (k.strip("/") or "index") + ".html" for k, v in PAGES.items()}
SOURCES["index.html"] = "index.html"
SOURCES["404.html"] = "404.html"


def rewrite_url(u):
    if u.startswith("//") or not u.startswith("/"):
        return u
    path, _, frag = u.partition("#")
    frag = "#" + frag if frag else ""
    if path in PAGES:
        return PAGES[path] + frag
    return path.lstrip("/") + frag            # /assets/site.css -> assets/site.css


def convert(html, main):
    html = re.sub(r'((?:href|src|srcset)=")([^"]*)(")', lambda m: m.group(1) + rewrite_url(m.group(2)) + m.group(3), html)
    html = re.sub(r"((?:href|src|srcset)=')([^']*)(')", lambda m: m.group(1) + rewrite_url(m.group(2)) + m.group(3), html)
    html = re.sub(r'<link rel="(?:icon|apple-touch-icon)"[^>]*>\s*', "", html)
    html = html.replace('<script src="assets/site.js" defer></script>', '<script>window.AV_ARTIFACT = true;</script>\n<script src="assets/site.js" defer></script>')
    if main:
        body_attrs = re.search(r"<body([^>]*)>", html).group(1)
        page = re.search(r'data-page="([^"]*)"', body_attrs).group(1)
        service = re.search(r'data-service="([^"]*)"', body_attrs).group(1)
        html = re.sub(r"<title>.*?</title>", "<title>Aviteus Business Website</title>", html, count=1)
        html = re.sub(r"<!doctype html>\s*|<html[^>]*>\s*|</html>\s*|<head>\s*|</head>\s*|</body>\s*", "", html, flags=re.I)
        html = re.sub(r"<body[^>]*>", f'<script>document.body.className = "av"; document.body.dataset.page = "{page}"; document.body.dataset.service = "{service}";</script>', html, count=1)
        html = re.sub(r'<meta charset="utf-8">\s*<meta name="viewport"[^>]*>\s*', "", html)
    return html


if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
shutil.copytree(os.path.join(SITE, "assets"), os.path.join(OUT, "assets"))
css_path = os.path.join(OUT, "assets", "site.css")
css = open(css_path).read().replace("url('/assets/fonts/", "url('fonts/")
css = css.replace('[data-theme="dark"]', '[data-av-theme="dark"]')   # one deliberate light look in the preview
open(css_path, "w").write(css)

for out_name, src_name in SOURCES.items():
    src = os.path.join(SITE, src_name)
    html = open(src).read()
    open(os.path.join(OUT, out_name), "w").write(convert(html, out_name == "index.html"))

print("Preview copy written to", OUT)
print("Pages:", ", ".join(sorted(SOURCES)))
