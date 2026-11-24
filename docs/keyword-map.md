# Keyword map

UK data, Ubersuggest, pulled 24 November 2026. Volumes are monthly estimates, not exact counts. Difficulty is SEO difficulty from 0 to 100 (lower is easier).

**Rule: one primary keyword per page.** No two pages chase the same term. Blog posts answer questions and link to the matching service page using that page's keyword as the link text.

## Service and core pages

| Page | Primary keyword | UK / month | Difficulty | Secondary and related terms | Where it is used |
|---|---|---|---|---|---|
| `/` Home | accountants for small business | 2,900 | 25 | small business accountant (1,900, KD 8), UK owner-managed businesses | Title, description, hero credentials line |
| `/services` | accounting services | 1,000 | 57 | accounting services for small businesses, any sector, who we work with | Title, description, "Who we work with" block |
| `/services/bookkeeping` | bookkeeping services | 1,900 | 9 | management accounts (1,900, KD 10), outsourced bookkeeping (390, KD 11), catch-up bookkeeping, bank reconciliation | Title, description, H1 |
| `/services/payroll` | payroll services | 1,900 | 16 | payroll services for small business (880, KD 36), RTI, auto enrolment, payslips, P60, P11D | Title, description, H1 |
| `/services/vat-tax` | VAT returns | 3,600 | 14 | limited company accountant (720, KD 30), VAT accountant (210), corporation tax, CT600, Making Tax Digital, year-end accounts | Title, description, H1 |
| `/services/self-assessment` | self assessment accountant | 880 | 15 | self assessment tax return accountant (260), 31 January deadline, directors, landlords | Title, description |
| `/services/business-advisory` | business advisory services | 260 | 33 | cash flow forecast, business valuation, fundraising, budgets | Title, description |
| `/services/virtual-cfo` | fractional CFO | 880 | 37 | virtual CFO (50, KD 21), part-time finance director | Title, description, new FAQ "Is a Virtual CFO the same as a fractional CFO?" |
| `/services/company-formation` | limited company formation | 1,000 | 43 | company formation (5,400, KD 34), HMRC registration, Companies House filings | Title, description |
| `/services/accounting-software` | Xero setup | 140 | 43 | QuickBooks, Sage, FreeAgent set-up, clean-up, training | Title |
| `/about-us` | accountants in Harrow | 390 | 34 | accountant Harrow (390, KD 32), ICAEW, ACCA, CIMA | Title, LocalBusiness schema address |
| `/contact` | (brand and action) | | | free 20-minute review | Title |

## Notes on the data

- **"Company formation" (5,400) is a trap.** Formation agents own that term. We target "limited company formation" and sell the accounting that follows.
- **"Fractional CFO" beats "virtual CFO" 880 to 50.** The page keeps the name "Virtual CFO" (it matches the live site) and uses "fractional CFO" in the title and an FAQ.
- **"VAT returns" is mostly people looking for how-to answers.** The service page targets it in the title. The blog guide "VAT returns and Making Tax Digital" catches the how-to searches and links back to the service page.
- **Self Assessment searches peak from November to January.** Publish and approve the Self Assessment content now, not in January.
- **"Accountants in Harrow" depends more on the Google Business Profile than on the website.** See "Off-site" below.

## Blog and tools (informational)

| Page | Question it answers | Links to |
|---|---|---|
| `/blog/bookkeeping-vs-management-accounts` | What is the difference? | Bookkeeping, Business advisory |
| `/blog/catch-up-bookkeeping` | How do I catch up my books? | Bookkeeping, VAT and year-end tax |
| `/blog/how-to-change-accountant-uk` | How do I change accountant? | Switching checklist, Bookkeeping, Payroll |
| `/blog/limited-company-deadlines-uk` | Which dates must a director know? | VAT and year-end tax, Company formation, Self Assessment |
| `/blog/small-business-payroll-checklist` | What must an employer do? | Payroll |
| `/blog/vat-returns-making-tax-digital` | When are VAT returns due and what is MTD? | VAT and year-end tax, Software |
| `/deadline-finder`, `/tools/*` | Free tools, no sign-up | Matching service pages and the lead form |

## 2026 techniques built in

1. **One entity graph.** Every page has a WebPage node tied by `@id` to the WebSite, the business (AccountingService and LocalBusiness), the founder (Person), its breadcrumb and its main topic (Service, BlogPosting). This helps Google and AI answer engines link the pages to one trusted business.
2. **Honest dates.** `dateModified` and sitemap `lastmod` come from `content_updated` in `data.json`. They change only when the copy changes, not on every build. Search engines ignore dates that move every day.
3. **Ready for AI answers.** Short answer paragraphs under each heading, FAQs with schema, `llms.txt`, and `robots.txt` that names the AI search crawlers and allows them.
4. **IndexNow.** The key file is built at `/<key>.txt`. After launch, send changed URLs to IndexNow so Bing, Copilot and others recrawl within hours.
5. **No sector limits.** The Industries page is gone and redirects to `/services#who-we-help`. The site now says "any sector" in the menu, the services page, an FAQ answer and `llms.txt`.
6. **Internal links.** Every indexable page has at least 4 contextual links in from other pages, on top of the menu and footer. The link text uses the target page's keyword. Run `python3 src/link_audit.py` after any edit.

## What the site cannot do on its own (owner actions)

- [ ] **Google Business Profile** for Alpha House, Harrow: category "Accountant", all 8 services, the same phone number and hours as the site. This is the main lever for "accountants in Harrow".
- [ ] **Reviews.** Ask each new client for a Google review after the first month. Reply to every one.
- [ ] **Named reviewer for blog posts** (a qualified accountant). Posts stay noindex until then. This is the biggest E-E-A-T gap.
- [ ] **Team data** in `data.json` with real names and memberships. Real people beat "our team".
- [ ] **Listings** with the same name, address and phone: Companies House (done), ICAEW or ACCA directories where eligible, Xero Advisor directory, Yell, Bing Places.
- [ ] **Search Console and Bing Webmaster Tools** on launch day. Submit the sitemap.
