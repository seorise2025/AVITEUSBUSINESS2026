"""Blog posts. Each post supports one service page and one keyword cluster from the strategy pack.
Every post stays noindex, out of the sitemap and marked as a draft until its slug is listed in
data.json "approved_posts" (the strategy pack requires a named accounting reviewer for tax content)."""

L = lambda href, text: f"<a class='ilink' href='{href}'>{text}</a>"

POSTS = [
# ------------------------------------------------------------------------------------------------
{
"slug": "how-to-change-accountant-uk",
"category": "Switching",
"title": "How to change accountant in the UK: a step-by-step guide",
"seo_title": "How to Change Accountant in the UK, Step by Step | Aviteus",
"description": "You can change accountant at any time of year. The steps, what to ask for, how professional clearance works, and how to time the move safely.",
"date": "2026-11-24",
"summary": "You can switch at any time of year. Your new accountant does most of the work. Your part is one email, a few approvals, and good timing.",
"in_short": "You can change accountant at any time of year. Your new accountant does most of the work: they ask your old firm for professional clearance, collect your records and get authority to deal with HMRC for you. Your part is usually one email and a few approvals. The real risk is timing, so plan the move around your next payroll run and VAT return.",
"services": [("Bookkeeping and management accounts", "/services/bookkeeping"), ("Payroll and pensions", "/services/payroll")],
"sections": [
("Before you start: read your engagement letter", f"""
<p>Your current accountant should have given you an engagement letter. It sets out the notice period and how fees are settled when you leave. Check two things:</p>
<ul><li><b>Notice period.</b> Many firms ask for 30 days. Some ask for less.</li>
<li><b>Fees owed.</b> Clear any unpaid invoices, or agree how they will be paid. Unpaid fees are the most common reason a handover slows down.</li></ul>
<p>You do not need a reason to leave. You also do not need your current firm's permission.</p>"""),
("Step 1: Agree the new scope in writing", f"""
<p>Before you tell anyone, get a written scope from the new firm. It should say what they will do, what you will do, when, and the fixed fee. Our {L('/services/bookkeeping#scope', 'scope table for monthly bookkeeping')} shows what that looks like.</p>
<p>Ask the new firm one question: <b>which date will you take over from?</b> A clean answer is "from the start of your next VAT quarter" or "from your next pay run".</p>"""),
("Step 2: Tell your current accountant", """
<p>A short email is enough. Keep it polite and factual:</p>
<div class="quiet"><p>Hello [name],</p><p>We have decided to move our accounting work to another firm from [date]. They will be in touch for professional clearance and the handover. Please let me know if any fees are outstanding.</p><p>Thank you for your help.</p></div>"""),
("Step 3: Professional clearance", """
<p>Your new accountant writes to your old one to ask if there is any professional reason they should not take on the work. This is called professional clearance. Accountants who belong to a professional body, such as ICAEW or ACCA, follow this step as part of their ethics rules.</p>
<p>The same letter asks for the information needed to carry on the work, such as the last accounts and tax returns, and any open matters with HMRC.</p>"""),
("Step 4: Authority to talk to HMRC", f"""
<p>Your new accountant asks HMRC to become your agent for each tax they will handle: corporation tax, VAT, PAYE and Self Assessment. You then approve each request. Until this is done, HMRC will not discuss your affairs with them.</p>
<p>Tip: approve these quickly. A missing authority is the usual reason a {L('/services/vat-tax', 'VAT return')} or payroll submission is held up during a switch.</p>"""),
("Step 5: Hand over records and access", """
<table class="table table--stack"><thead><tr><th scope="col">Item</th><th scope="col">Why it matters</th></tr></thead><tbody>
<tr><td>Last year's accounts and tax returns</td><td data-label="Why it matters">The opening figures for this year</td></tr>
<tr><td>Accounting software access</td><td data-label="Why it matters">Make sure the subscription is in your company's name, not the old firm's</td></tr>
<tr><td>VAT returns filed this year</td><td data-label="Why it matters">So the next return starts from the right place</td></tr>
<tr><td>Payroll year-to-date figures</td><td data-label="Why it matters">Needed for every employee if payroll moves mid-year</td></tr>
<tr><td>References: UTR, VAT number, PAYE and Accounts Office references</td><td data-label="Why it matters">The new firm needs these to set up HMRC authority</td></tr>
<tr><td>Companies House authentication code</td><td data-label="Why it matters">Needed to file accounts and the confirmation statement online</td></tr>
</tbody></table>"""),
("When is the best time to switch?", f"""
<p>Any time works, but some moments are easier:</p>
<ul><li><b>Just after a VAT return is filed.</b> The new firm starts with a clean quarter.</li>
<li><b>Just after a pay run.</b> Payroll moves from the next run, with no gap. Our payroll page explains {L('/services/payroll', 'how moving payroll part way through the year works')}.</li>
<li><b>Not in the last weeks before a big deadline.</b> If your accounts or tax return are due within a month, let the old firm finish that one.</li></ul>
<p>Not sure which dates are close for you? The {L('/deadline-finder', 'free deadline finder')} lists them in order.</p>"""),
],
"faqs": [
("Do I need to tell HMRC that I have changed accountant?", "Not directly. Your new accountant sends HMRC the requests to act for you, and you approve them. That is enough for HMRC."),
("Can I change accountant part way through the year?", "Yes. There is no fixed time to switch. The new firm picks up from the last month that was completed and checks the opening figures first."),
("Will I lose my accounting records?", "No, as long as the accounting software is in your company's name. If the old firm holds the subscription, ask them to transfer it to you before you leave."),
("How long does a switch take?", "Usually a few weeks, most of it waiting for clearance and HMRC approvals. Planning around your next payroll and VAT dates means nothing is missed while that happens."),
],
},
# ------------------------------------------------------------------------------------------------
{
"slug": "limited-company-deadlines-uk",
"category": "Deadlines",
"title": "UK limited company deadlines: the dates every director should know",
"seo_title": "UK Limited Company Deadlines for Directors | Aviteus",
"description": "Accounts, corporation tax, CT600, VAT, PAYE and confirmation statement deadlines for UK limited companies, with examples and late penalties.",
"date": "2026-11-24",
"summary": "Accounts, corporation tax, CT600, VAT, payroll and the confirmation statement. Every date, with a worked example and what happens if you miss it.",
"in_short": "Most dates follow from your company's year end. Accounts go to Companies House 9 months after it. Corporation tax is paid 9 months and 1 day after it. The company tax return (CT600) is due 12 months after it. VAT is due 1 month and 7 days after each VAT period, and PAYE by the 22nd of each month.",
"services": [("VAT and year-end tax", "/services/vat-tax"), ("Payroll and pensions", "/services/payroll")],
"sections": [
("The main dates, with a 31 March year end", """
<table class="table table--stack"><thead><tr><th scope="col">What</th><th scope="col">Rule</th><th scope="col">Year end 31 March 2026</th></tr></thead><tbody>
<tr><td>Annual accounts to Companies House</td><td data-label="Rule">9 months after year end</td><td data-label="Year end 31 March 2026" class="date">31 December 2026</td></tr>
<tr><td>Corporation tax payment</td><td data-label="Rule">9 months and 1 day after year end</td><td data-label="Year end 31 March 2026" class="date">1 January 2027</td></tr>
<tr><td>Company tax return (CT600)</td><td data-label="Rule">12 months after year end</td><td data-label="Year end 31 March 2026" class="date">31 March 2027</td></tr>
</tbody></table>
<p class="mt-5">Notice the order. You pay corporation tax three months before the return is due. That catches many owners out, because the bill arrives before the paperwork.</p>"""),
("Your first accounts are different", f"""
<p>A new company's first accounts are due 21 months after the date it was set up. If you are setting one up now, see {L('/services/company-formation', 'company formation and compliance')}. After that, the 9-month rule applies. If your company is new, check this date first, as it is easy to miss.</p>"""),
("Dates that repeat through the year", f"""
<table class="table table--stack"><thead><tr><th scope="col">What</th><th scope="col">When</th></tr></thead><tbody>
<tr><td>VAT return and payment</td><td data-label="When" class="date">1 month and 7 days after each VAT period ends</td></tr>
<tr><td>PAYE and National Insurance</td><td data-label="When" class="date">22nd of each month if you pay electronically</td></tr>
<tr><td>Payroll report to HMRC (RTI)</td><td data-label="When" class="date">On or before each payday</td></tr>
<tr><td>Confirmation statement</td><td data-label="When" class="date">At least once a year, within 14 days of your review date</td></tr>
</tbody></table>
<p class="mt-5">More on each: {L('/services/vat-tax', 'VAT returns and year-end')} and {L('/services/payroll', 'running payroll')}.</p>"""),
("Yearly payroll dates", """
<ul><li><b>31 May:</b> give every employee their P60 for the tax year that ended on 5 April.</li>
<li><b>6 July:</b> send P11D and P11D(b) forms for benefits in kind, where you have any.</li></ul>"""),
("Directors' own tax", f"""
<ul><li><b>31 January:</b> Self Assessment return and any tax due for the tax year that ended the previous April, plus a first payment on account if one applies.</li>
<li><b>31 July:</b> second payment on account, if one applies.</li></ul>
<p>We prepare and file directors' returns: see {L('/services/self-assessment', 'Self Assessment tax returns')}.</p>"""),
("What happens if you miss a date", """
<ul><li><b>Accounts filed late at Companies House:</b> an automatic penalty that grows with time, from £150 for up to a month late to £1,500 for over six months. It doubles if you are late two years running.</li>
<li><b>CT600 filed late:</b> a £100 penalty, and another £100 if it is three months late. More follows after that.</li>
<li><b>Corporation tax paid late:</b> HMRC charges interest from the day after the due date.</li>
<li><b>VAT returns filed late:</b> each late return adds a penalty point. Reach the limit and a penalty follows.</li></ul>
<p>If a date falls on a weekend or bank holiday, make sure payment reaches HMRC by the working day before.</p>"""),
("See your own dates", f"""
<p>Your dates depend on your year end, your VAT quarters and whether you run payroll. The {L('/deadline-finder', 'free UK deadline finder')} works them out and lists the next 12 months in order.</p>"""),
],
"faqs": [
("When is corporation tax due for a small company?", "9 months and 1 day after the end of the accounting period. With a 31 March year end, that is 1 January."),
("When are company accounts due at Companies House?", "9 months after the year end for a private limited company, after its first accounts. First accounts are due 21 months after the company was set up."),
("Is the corporation tax return due at the same time as the payment?", "No. The return (CT600) is due 12 months after the year end, three months after the payment."),
],
},
# ------------------------------------------------------------------------------------------------
{
"slug": "bookkeeping-vs-management-accounts",
"category": "Bookkeeping",
"title": "Bookkeeping vs management accounts: what is the difference?",
"seo_title": "Bookkeeping vs Management Accounts: The Difference | Aviteus",
"description": "Bookkeeping records every transaction. Management accounts turn those records into a short monthly report. What each covers and when you need both.",
"date": "2026-11-24",
"summary": "Bookkeeping records every transaction. Management accounts turn those records into a short report you can act on. Here is when you need each.",
"in_short": "Bookkeeping is recording and matching every transaction. Management accounts are the short monthly report built from those records: profit, cash and what changed. Statutory accounts are the yearly accounts the law requires. You need up-to-date books before management accounts are worth reading.",
"services": [("Bookkeeping and management accounts", "/services/bookkeeping")],
"sections": [
("Three kinds of accounts, side by side", """
<table class="table table--stack"><thead><tr><th scope="col"></th><th scope="col">Bookkeeping</th><th scope="col">Management accounts</th><th scope="col">Statutory accounts</th></tr></thead><tbody>
<tr><td>What it is</td><td data-label="Bookkeeping">Recording and matching every sale, bill and bank line</td><td data-label="Management accounts">A short report on profit, cash and what changed</td><td data-label="Statutory accounts">The yearly accounts the law requires</td></tr>
<tr><td>How often</td><td data-label="Bookkeeping">All the time, closed each month</td><td data-label="Management accounts">Monthly or quarterly</td><td data-label="Statutory accounts">Once a year</td></tr>
<tr><td>Who it is for</td><td data-label="Bookkeeping">Everything else depends on it</td><td data-label="Management accounts">You, your managers, your lender</td><td data-label="Statutory accounts">Companies House and HMRC</td></tr>
<tr><td>Required by law?</td><td data-label="Bookkeeping">Yes, you must keep records</td><td data-label="Management accounts">No</td><td data-label="Statutory accounts">Yes</td></tr>
</tbody></table>"""),
("What bookkeeping covers", """
<ul><li>Every bank and card line matched to a bill, a sale or a receipt.</li>
<li>Supplier bills and sales invoices recorded and coded for VAT.</li>
<li>A list of what is missing, such as receipts for card payments.</li>
<li>The month closed, so the figures stop moving.</li></ul>
<p>Good bookkeeping is invisible. You notice it only when it is missing, usually a week before a VAT return.</p>"""),
("What management accounts contain", """
<ul><li><b>Profit and loss</b> for the month and the year to date.</li>
<li><b>Balance sheet:</b> what the business owns and owes.</li>
<li><b>Cash position</b> and what is coming in and going out.</li>
<li><b>Notes in plain English</b> on what moved and why. This is the part most owners actually read.</li></ul>"""),
("When management accounts are worth it", f"""
<p>You probably need them if any of these is true:</p>
<ul><li>You employ staff and want to know if you can afford the next hire.</li>
<li>You borrow money, or plan to. Lenders often ask for recent management accounts, and a {L('/services/business-advisory', 'forecast')} helps too.</li>
<li>Your margins move from month to month and you do not know why.</li>
<li>You only find out if you made money when the yearly accounts arrive.</li></ul>
<p>If you have very few transactions and no staff, good software and a quarterly check may be enough.</p>"""),
("What good management accounts look like", f"""
<p>Short, on time and readable. Three pages is plenty. They should arrive at the same point each month, and the notes should answer "why" in a sentence or two. See {L('/services/bookkeeping', 'how our monthly bookkeeping and management pack work')}.</p>"""),
],
"faqs": [
("Can I have management accounts without a bookkeeper?", "Only if your books are up to date. Management accounts are built from your records, so if the records are behind, the report will be wrong."),
("Are management accounts the same as year-end accounts?", "No. Year-end (statutory) accounts are a legal filing made once a year. Management accounts are for running the business and are not filed anywhere."),
("How often should I get management accounts?", "Monthly suits most growing businesses. Quarterly can work if your figures do not change much from month to month."),
],
},
# ------------------------------------------------------------------------------------------------
{
"slug": "small-business-payroll-checklist",
"category": "Payroll",
"title": "Running payroll for a small business: the employer checklist",
"seo_title": "Small Business Payroll Checklist for UK Employers | Aviteus",
"description": "What a UK employer must do before the first payday, every pay run, every month and every year: RTI, PAYE, payslips, workplace pensions, P60 and P11D.",
"date": "2026-11-24",
"summary": "What a UK employer must do before the first payday, on every pay run, each month and each year. RTI, PAYE, pensions, P60 and P11D in one list.",
"in_short": "Each pay run, you calculate pay, tax and National Insurance, report it to HMRC through RTI on or before payday, and give staff payslips. Each month, you pay PAYE to HMRC by the 22nd if you pay electronically. Each year, staff get a P60 by 31 May and any P11D forms go in by 6 July. Workplace pension duties run alongside all of it.",
"services": [("Payroll and pensions", "/services/payroll")],
"sections": [
("Before your first payday", """
<ul><li><b>Register as an employer with HMRC.</b> You can do this up to 2 months before you first pay anyone. You get a PAYE reference and an Accounts Office reference.</li>
<li><b>Check each person's right to work in the UK</b> before they start.</li>
<li><b>Get employers' liability insurance.</b> Most employers must have it from the first day.</li>
<li><b>Set up workplace pension duties.</b> Your duties start from the first day you employ someone. You must confirm what you have done to The Pensions Regulator (the declaration of compliance).</li></ul>"""),
("Every pay run", """
<ul><li>Collect changes: starters, leavers, hours, overtime, bonuses and sickness.</li>
<li>Calculate pay, tax, National Insurance, pension and any statutory pay.</li>
<li>Send a Full Payment Submission (FPS) to HMRC <b>on or before payday</b>. This is Real Time Information, or RTI.</li>
<li>Give every employee a payslip.</li>
<li>Pay your staff.</li></ul>"""),
("Every month", f"""
<table class="table table--stack"><thead><tr><th scope="col">Task</th><th scope="col">Deadline</th></tr></thead><tbody>
<tr><td>Pay PAYE and National Insurance to HMRC</td><td data-label="Deadline" class="date">22nd of the month if paying electronically (19th by post)</td></tr>
<tr><td>Employer Payment Summary (EPS), if you need one</td><td data-label="Deadline" class="date">19th of the month</td></tr>
<tr><td>Pension contributions to your provider</td><td data-label="Deadline" class="date">By the date your provider and the rules set</td></tr>
</tbody></table>
<p class="mt-5">Small employers often pay HMRC quarterly instead of monthly. Check with HMRC whether you qualify before you change.</p>"""),
("Every year", f"""
<ul><li><b>Last payday of the tax year:</b> mark that pay run's FPS as the final one for the year.</li>
<li><b>By 31 May:</b> give every employee their P60.</li>
<li><b>By 6 July:</b> send P11D and P11D(b) forms if you provided benefits in kind.</li>
<li><b>Every three years:</b> re-enrol staff into your workplace pension and confirm it to The Pensions Regulator.</li></ul>
<p>The {L('/deadline-finder', 'deadline finder')} lists your next payroll dates in order.</p>"""),
("Common payroll mistakes", """
<ul><li><b>Late RTI.</b> The report must reach HMRC on or before payday, not after.</li>
<li><b>Wrong tax codes</b> left unchanged after HMRC sends an update.</li>
<li><b>Forgetting a leaver's P45,</b> or paying someone after they have left without reporting it.</li>
<li><b>Missing pension deadlines,</b> which The Pensions Regulator can fine for.</li></ul>"""),
("Doing it yourself, or handing it over", f"""
<p>If you pay one director a fixed salary and nothing changes, payroll software may be all you need. Once you have staff with hours, sickness and starters, a person running it to a fixed monthly routine saves you the chase. See {L('/services/payroll', 'how our managed payroll month works')}.</p>"""),
],
"faqs": [
("When must RTI be sent to HMRC?", "On or before each payday. Each pay run needs its own Full Payment Submission."),
("When is PAYE due?", "By the 22nd of the month if you pay electronically, for the tax month that ended on the 5th. By post, it is the 19th."),
("When do employees get their P60?", "By 31 May, for the tax year that ended on 5 April."),
],
},
# ------------------------------------------------------------------------------------------------
{
"slug": "vat-returns-making-tax-digital",
"category": "VAT",
"title": "VAT returns and Making Tax Digital: a plain guide for small businesses",
"seo_title": "VAT Returns and Making Tax Digital, Explained | Aviteus",
"description": "When VAT returns are due, what Making Tax Digital requires, which records to keep and what happens if you file late. A plain guide for UK small businesses.",
"date": "2026-11-24",
"summary": "When VAT returns are due, what Making Tax Digital means in practice, which records to keep, and how late filing penalties work.",
"in_short": "A VAT return and its payment are due 1 calendar month and 7 days after the end of each VAT period. Every VAT-registered business must keep digital records and file through software that works with Making Tax Digital. Keep your VAT records for at least 6 years.",
"services": [("VAT and year-end tax", "/services/vat-tax"), ("Bookkeeping and management accounts", "/services/bookkeeping")],
"sections": [
("When your VAT return is due", """
<p>Most businesses file every three months. The return and the payment are both due 1 calendar month and 7 days after the period ends.</p>
<table class="table table--stack"><thead><tr><th scope="col">Quarter ends</th><th scope="col">Return and payment due</th></tr></thead><tbody>
<tr><td>31 March</td><td data-label="Return and payment due" class="date">7 May</td></tr>
<tr><td>30 June</td><td data-label="Return and payment due" class="date">7 August</td></tr>
<tr><td>30 September</td><td data-label="Return and payment due" class="date">7 November</td></tr>
<tr><td>31 December</td><td data-label="Return and payment due" class="date">7 February</td></tr>
</tbody></table>
<p class="mt-5">If you pay by Direct Debit, HMRC collects the payment a few working days after the due date.</p>"""),
("What Making Tax Digital means for VAT", f"""
<p>Every VAT-registered business must:</p>
<ul><li>Keep its VAT records digitally.</li>
<li>Submit returns through software that works with Making Tax Digital.</li>
<li>Keep digital links between its records and the return. Copying figures by hand between systems is not allowed.</li></ul>
<p>If you still use spreadsheets, bridging software can link them to HMRC. Most businesses find it simpler to move to {L('/services/accounting-software', 'Xero, QuickBooks, Sage or FreeAgent')}.</p>"""),
("When you must register for VAT", """
<p>You must register when your VAT-taxable turnover goes over the registration threshold in any rolling 12 months, or when you expect it to in the next 30 days alone. Check the current threshold on GOV.UK, as it can change. Watching your turnover each month is the easiest way to avoid registering late.</p>"""),
("Records to keep", """
<ul><li>Sales and purchase invoices.</li>
<li>Records of VAT you charged and VAT you paid.</li>
<li>Any adjustments, such as credit notes.</li></ul>
<p>Keep them for at least 6 years.</p>"""),
("What happens if you file or pay late", """
<ul><li><b>Late returns:</b> each late return adds a penalty point. Once you reach the limit for your filing frequency, a penalty follows, and so does every late return after it.</li>
<li><b>Late payments:</b> penalties and interest start soon after the due date and grow the longer it is unpaid.</li></ul>
<p>Filing a few days early every quarter is the simplest way to avoid both.</p>"""),
("Let someone else watch the dates", f"""
<p>We prepare the return from your books, send you the draft figures to approve, and file before the deadline. See {L('/services/vat-tax', 'how our VAT and year-end service works')}, or use the {L('/deadline-finder', 'deadline finder')} to see your next VAT dates.</p>"""),
],
"faqs": [
("When is my VAT return due?", "One calendar month and seven days after the end of your VAT period. For a quarter ending 31 March, it is 7 May."),
("Do I have to use Making Tax Digital software?", "Yes, if you are VAT registered. Returns must go through compatible software, with digital links between your records and the return."),
("How long do I keep VAT records?", "At least 6 years."),
],
},
# ------------------------------------------------------------------------------------------------
{
"slug": "catch-up-bookkeeping",
"category": "Bookkeeping",
"title": "Books behind? How to catch up your bookkeeping before a deadline",
"seo_title": "Catch-Up Bookkeeping: Getting Your Books Current | Aviteus",
"description": "Months behind on your books with a VAT return coming? A step-by-step plan to catch up, what to gather first, and how to stay current after.",
"date": "2026-11-24",
"summary": "Months behind with a VAT return coming? Start with the deadline, gather statements, work oldest month first, then switch to a monthly routine.",
"in_short": "Start with your next deadline, then work backwards. Download every bank and card statement for the missing months, reconcile the oldest month first, and keep a single list of what is missing. Once you are current, close each month within a few weeks of its end so it never builds up again.",
"services": [("Bookkeeping and management accounts", "/services/bookkeeping")],
"sections": [
("Step 1: Find your next deadline", f"""
<p>Your catch-up has a finish line. It is usually your next VAT return or your company's year end. The {L('/deadline-finder', 'deadline finder')} shows which comes first. Work to that date, not to "when we get round to it".</p>"""),
("Step 2: Gather what you need", """
<ul><li>Every bank and card statement for the missing months, downloaded as files. Bank feeds often reach back only a few months, so do not rely on them alone.</li>
<li>Sales invoices you issued.</li>
<li>Supplier bills and receipts, including photos and email copies.</li>
<li>Loan, lease and finance agreements.</li>
<li>Your last filed VAT return and last year's accounts, to check the opening figures.</li></ul>"""),
("Step 3: Work oldest month first", """
<p>Reconcile one month at a time, starting with the oldest. Match every bank line to a sale, a bill or a receipt, then close the month before you start the next. Working in order means each month's closing balance proves the next month's opening balance.</p>"""),
("Step 4: Keep one list of what is missing", """
<p>Do not chase receipts one by one. Keep a single list, such as "card payment, £84.20, 3 March, no receipt", and deal with it in one sitting. Some items will never be found. Those need a sensible decision, not more searching.</p>"""),
("Step 5: Check VAT before you file", f"""
<p>Before the next {L('/services/vat-tax', 'VAT return')}, check that every bill and sale has the right VAT treatment. Catch-up work is where VAT errors hide, because bills get posted in a rush.</p>"""),
("Step 6: Stay current", f"""
<p>Once the books are up to date, close each month within a few weeks of its end. A monthly routine takes far less time than a catch-up, and it gives you figures you can act on. See {L('/services/bookkeeping#catch-up', 'how we handle catch-up work')} and then the {L('/services/bookkeeping', 'monthly routine that follows')}.</p>"""),
],
"faqs": [
("How long does catch-up bookkeeping take?", "It depends on how many months are missing and how many transactions each month has. A business with a few months of light activity can be current in days. A year of heavy activity takes longer."),
("Can I catch up my books myself?", "Yes, if you have the time and the records. The work is steady rather than hard. Most owners hand it over because the deadline is close and the records are scattered."),
("What if I cannot find some receipts?", "Keep a list and make a reasonable decision on each item. Your accountant can tell you how to treat missing receipts for VAT and tax."),
],
},
]
