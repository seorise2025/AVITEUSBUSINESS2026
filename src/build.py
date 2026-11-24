"""Builds the static site into ../site. Run: python3 src/build.py
Every page is full HTML from the server: no JavaScript is needed to read any content."""
import json, os, re, shutil, sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
DS = os.path.join(ROOT, "design-system")
OUT = os.path.join(ROOT, "site")
sys.path.insert(0, SRC)
import pages  # noqa: E402
from layout import SITE  # noqa: E402

data = json.load(open(os.path.join(SRC, "data.json")))
TODAY = date.today().isoformat()

if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, "assets", "img"))

# ---------- Assets ----------
shutil.copytree(os.path.join(DS, "fonts"), os.path.join(OUT, "assets", "fonts"))
tokens = open(os.path.join(DS, "tokens.css")).read().replace("url('fonts/", "url('/assets/fonts/")
bundle = open(os.path.join(DS, "components", "bundle.css")).read()
site_css = open(os.path.join(SRC, "site.css")).read()
css = "\n".join([tokens, bundle, site_css])
css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)          # strip comments
css = re.sub(r"\n\s*\n+", "\n", css)
open(os.path.join(OUT, "assets", "site.css"), "w").write(css)
shutil.copy(os.path.join(SRC, "site.js"), os.path.join(OUT, "assets", "site.js"))
shutil.copy(os.path.join(SRC, "finder.js"), os.path.join(OUT, "assets", "finder.js"))
for f in os.listdir(os.path.join(SRC, "static")):
    shutil.copy(os.path.join(SRC, "static", f), os.path.join(OUT, f if not f.startswith("img-") else os.path.join("assets", "img", f[4:])))

# ---------- Pages ----------
ROUTES = [
    ("index.html", pages.home, "/", "1.0", "weekly"),
    ("services/bookkeeping.html", pages.bookkeeping, "/services/bookkeeping", "0.9", "monthly"),
    ("services/payroll.html", pages.payroll, "/services/payroll", "0.9", "monthly"),
    ("services/vat-tax.html", pages.vat, "/services/vat-tax", "0.9", "monthly"),
    ("contact.html", pages.contact, "/contact", "0.8", "monthly"),
    ("about-us.html", pages.about, "/about-us", "0.7", "monthly"),
    ("services.html", pages.services, "/services", "0.6", "monthly"),
    ("deadline-finder.html", pages.finder, "/deadline-finder", "0.8", "monthly"),
    ("404.html", pages.notfound, None, None, None),
]
for fn, func, url, _, _ in ROUTES:
    p = os.path.join(OUT, fn)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(func(data))

# ---------- Crawl and host files ----------
urls = "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority></url>\n" for _, _, u, pr, cf in ROUTES if u)
open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')

open(os.path.join(OUT, "robots.txt"), "w").write(f"""User-agent: *
Allow: /
Disallow: /api/

Sitemap: {SITE}/sitemap.xml
""")

# Netlify and Cloudflare Pages both read these two files.
open(os.path.join(OUT, "_redirects"), "w").write("""/contactus        /contact  301
/contactus/       /contact  301
/contactus.html   /contact  301
/index.html       /         301
""")
open(os.path.join(OUT, "_headers"), "w").write("""/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()
  X-Frame-Options: DENY
  Strict-Transport-Security: max-age=31536000; includeSubDomains

/assets/*
  Cache-Control: public, max-age=2592000

/assets/fonts/*
  Cache-Control: public, max-age=31536000, immutable
""")

print("Built", len(ROUTES), "pages into", OUT)
