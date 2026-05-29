from __future__ import annotations

import html
import re
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://calculatorcity.in"
OLD_DOMAIN = "https://" + "your" + "domain.com"
OLD_AD_LABEL = "Ad" + " slot"
UPDATED = "May 15, 2026"


CATEGORIES = [
    ("Math Calculators", "#math"),
    ("Finance Calculators", "#finance"),
    ("Unit Converters", "#unit"),
    ("Health & Fitness", "#health"),
    ("Date & Time", "#datetime"),
    ("Science & Other", "#science"),
    ("India Calculators", "#india"),
]

POPULAR = [
    ("Percentage", "maths/percentage-calculator.html"),
    ("GST", "india/gst-calculator.html"),
    ("Income Tax", "india/income-tax-calculator.html"),
    ("Home Loan EMI", "india/home-loan-emi-calculator.html"),
    ("SIP", "india/sip-calculator.html"),
    ("FD", "india/fd-calculator.html"),
    ("BMI", "health-fitness/bmi-calculator.html"),
    ("Age", "date-time/age-calculator.html"),
    ("Loan EMI", "finance/loan-emi-calculator.html"),
    ("Compound Interest", "finance/compound-interest-calculator.html"),
    ("CTC Salary", "india/ctc-salary-calculator.html"),
    ("EPF / PF", "india/pf-epf-calculator.html"),
    ("PPF", "india/ppf-calculator.html"),
    ("HRA Exemption", "india/hra-exemption-calculator.html"),
    ("TDS", "india/tds-calculator.html"),
    ("Discount", "finance/discount-calculator.html"),
    ("Currency", "finance/currency-converter.html"),
    ("CGPA to Percentage", "india/cgpa-to-percentage-calculator.html"),
    ("Gold Price", "india/gold-price-calculator.html"),
    ("Stamp Duty", "india/stamp-duty/index.html"),
]

COMPANY = [
    ("About Us", "company/about-us.html"),
    ("Privacy Policy", "company/privacy-policy.html"),
    ("Terms & Conditions", "company/terms-and-conditions.html"),
    ("Blogs", "company/blogs.html"),
    ("Contact Us", "company/contact-us.html"),
    ("Help", "company/help.html"),
]


def rel(page: Path, target: str) -> str:
    if target.startswith("#"):
        return f"index.html{target}" if page.parent == ROOT else f"../index.html{target}"
    if page.parent == ROOT / "company" and target.startswith("company/"):
        return target.removeprefix("company/")
    prefix = "" if page.parent == ROOT else "../"
    return prefix + target


def absolute(path: str) -> str:
    return DOMAIN + ("/" if path == "index.html" else f"/{path}")


def nav_for(page: Path) -> str:
    prefix = "" if page.parent == ROOT else "../"
    index = f"{prefix}index.html"
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="header-inner">
    <a class="logo" href="{index}">Calculatorcity</a>
    <nav class="main-nav" aria-label="Main navigation">
      <a href="{index}#math">Math</a>
      <a href="{index}#finance">Finance</a>
      <a href="{index}#unit">Unit</a>
      <a href="{index}#health">Health</a>
      <a href="{index}#datetime">Date &amp; Time</a>
      <a href="{index}#science">Science</a>
      <a class="nav-india" href="{index}#india">India</a>
    </nav>
    <div class="header-search">
      <label class="sr-only" for="header-search">Search calculators</label>
      <input id="header-search" class="search-input" type="search" data-search-input>
    </div>
    <button class="mobile-menu-btn" type="button" aria-label="Open menu" aria-expanded="false" data-mobile-menu-btn>☰</button>
  </div>
  <nav class="mobile-nav" aria-label="Mobile navigation" data-mobile-nav>
    <a href="{index}#math">Math</a>
    <a href="{index}#finance">Finance</a>
    <a href="{index}#unit">Unit Converter</a>
    <a href="{index}#health">Health &amp; Fitness</a>
    <a href="{index}#datetime">Date &amp; Time</a>
    <a href="{index}#science">Science &amp; Other</a>
    <a href="{index}#india">India</a>
  </nav>
</header>"""


def footer_for(page: Path) -> str:
    categories = [
        ("ti-math", "Math Calculators", "index.html#math"),
        ("ti-coin-rupee", "Finance Calculators", "index.html#finance"),
        ("ti-ruler", "Unit Converters", "index.html#unit"),
        ("ti-heartbeat", "Health & Fitness", "index.html#health"),
        ("ti-calendar", "Date & Time", "index.html#datetime"),
        ("ti-flask", "Science & Other", "index.html#science"),
        ("ti-map-pin", "India Calculators", "index.html#india"),
    ]
    popular = [
        ("Percentage", "maths/percentage-calculator.html"),
        ("GST", "india/gst-calculator.html"),
        ("Income Tax", "india/income-tax-calculator.html"),
        ("Home Loan EMI", "india/home-loan-emi-calculator.html"),
        ("SIP", "india/sip-calculator.html"),
        ("FD", "india/fd-calculator.html"),
        ("BMI", "health-fitness/bmi-calculator.html"),
        ("Age", "date-time/age-calculator.html"),
        ("Currency", "finance/currency-converter.html"),
        ("Gold Price", "india/gold-price-calculator.html"),
        ("Loan EMI", "finance/loan-emi-calculator.html"),
        ("Compound Interest", "finance/compound-interest-calculator.html"),
        ("CTC Salary", "india/ctc-salary-calculator.html"),
        ("EPF / PF", "india/pf-epf-calculator.html"),
        ("PPF", "india/ppf-calculator.html"),
        ("HRA Exemption", "india/hra-exemption-calculator.html"),
        ("TDS", "india/tds-calculator.html"),
        ("Discount", "finance/discount-calculator.html"),
        ("CGPA to %", "india/cgpa-to-percentage-calculator.html"),
        ("Stamp Duty", "india/stamp-duty/index.html"),
    ]
    company = [
        ("About Us", "company/about-us.html"),
        ("Blog", "company/blogs.html"),
        ("Contact Us", "company/contact-us.html"),
        ("Help", "company/help.html"),
        ("Privacy Policy", "company/privacy-policy.html"),
        ("Terms & Conditions", "company/terms-and-conditions.html"),
    ]
    category_links = "\n".join(
        f'        <a href="{rel(page, href)}"><i class="ti {icon}" aria-hidden="true"></i><span>{html.escape(label)}</span></a>'
        for icon, label, href in categories
    )
    popular_links = "\n".join(
        f'        <a href="{rel(page, href)}">{html.escape(label)}</a>' for label, href in popular
    )
    company_links = "\n".join(
        f'        <a href="{rel(page, href)}">{html.escape(label)}</a>' for label, href in company
    )
    return f"""<hr class="footer-separator" aria-hidden="true">
<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-main">
      <nav class="footer-categories" aria-labelledby="footer-categories-heading">
        <h3 id="footer-categories-heading" class="footer-links-label">CATEGORIES</h3>
        <div class="footer-category-pills">
{category_links}
        </div>
      </nav>
      <nav class="footer-popular" aria-labelledby="footer-popular-heading">
        <h3 id="footer-popular-heading" class="footer-links-label">POPULAR CALCULATORS</h3>
        <div class="footer-popular-links">
{popular_links}
        </div>
      </nav>
      <div class="footer-brand-company">
        <div class="footer-brand">
          <span class="footer-brand-name">Calculatorcity</span>
          <p class="footer-tagline">Free calculators running locally in your browser.</p>
          <span class="footer-local-badge"><i class="ti ti-device-desktop" aria-hidden="true"></i><span>No data sent</span></span>
        </div>
        <hr class="footer-company-divider" aria-hidden="true">
        <nav class="footer-company-links" aria-labelledby="footer-company-heading">
          <h3 id="footer-company-heading" class="footer-links-label">COMPANY</h3>
{company_links}
        </nav>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Calculatorcity. All calculations run locally in your browser.</span>
      <span class="footer-disclaimer">For education and planning only. Results are estimates — not financial, tax, legal, or medical advice. Verify with a qualified expert.</span>
    </div>
  </div>
</footer>"""


def page_head(title: str, description: str, path: str, page_type: str = "WebPage") -> str:
    prefix = "" if (ROOT / path).parent == ROOT else "../"
    schema = {
        "@context": "https://schema.org",
        "@type": page_type,
        "name": title.replace(" | Calculatorcity", ""),
        "url": absolute(path),
        "description": description,
        "publisher": {"@type": "Organization", "name": "Calculatorcity", "url": DOMAIN},
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": title.replace(" | Calculatorcity", ""), "item": absolute(path)},
        ],
    }
    import json

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="canonical" href="{absolute(path)}">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:type" content="website">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="/assets/icons/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}assets/css/base.css">
  <link rel="stylesheet" href="{prefix}assets/css/layout.css">
  <link rel="stylesheet" href="{prefix}assets/css/components.css">
  <link rel="stylesheet" href="{prefix}assets/css/calculator.css">
  <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(breadcrumb, ensure_ascii=False)}</script>
</head>"""


def section(title: str, paragraphs: list[str]) -> str:
    body = "\n".join(f"        <p>{p}</p>" for p in paragraphs)
    return f"""      <section class="content-section">
        <h2>{title}</h2>
{body}
      </section>"""


PAGES = {
    "company/about-us.html": {
        "title": "About Us | Calculatorcity",
        "description": "Learn about Calculatorcity, our calculator quality standards, privacy-first design, Indian calculator focus, and how we keep everyday calculations clear and useful.",
        "h1": "About Calculatorcity",
        "intro": "Calculatorcity is a free calculator website built for people who want fast answers without confusing forms, outdated formulas, or unnecessary signups. The site covers worldwide calculators for math, finance, units, health, time, and science, plus a deep India section for rupee-based tax, salary, investment, property, and utility calculations.",
        "sections": [
            ("Why Calculatorcity exists", [
                "Most people use calculators at moments when they need clarity quickly: comparing loan offers, checking an exam percentage, converting a measurement, estimating tax, or planning a monthly investment. A calculator page should respect that moment. It should ask only for the values that matter, label every input clearly, show the result in a readable way, and explain the formula without turning the page into a textbook. Calculatorcity exists because many online calculators still feel cluttered, slow, or written for search engines rather than real people.",
                "Our goal is to make calculation pages that are easy to trust. That means the result is not the only useful part of the page. A good calculator also shows supporting values, examples, reference tables, and notes about when a formula should be treated as an estimate. When a user changes an input, the page should respond predictably and should not hide the assumptions behind the answer. This is especially important for financial, tax, and health topics, where a small misunderstanding can change a decision.",
            ]),
            ("What we build", [
                "Calculatorcity currently includes eighty calculator tools across seven practical groups. Math pages cover everyday arithmetic and school needs such as percentages, fractions, averages, ratios, square roots, exponents, probability, and quadratic equations. Finance pages cover interest, EMI, mortgage, discounts, inflation, ROI, currency conversion, tips, and break-even analysis. Unit pages convert length, weight, temperature, speed, area, volume, data storage, energy, pressure, and number systems. Health and date tools help with BMI, calories, age, time zones, working days, and other common tasks.",
                "The India calculator section is a major part of the site because Indian users often need rules and formatting that global calculators ignore. Rupee amounts should use the Indian number system, not the million and billion style by default. Tax, salary, GST, PPF, EPF, NPS, SIP, FD, gratuity, stamp duty, on-road price, AP electricity bills, and gold jewellery calculations all need local context. Calculatorcity pages include Indian symbols, lakhs and crores, state-specific tables where useful, and practical notes that help users understand the result.",
            ]),
            ("How we approach accuracy", [
                "Accuracy starts with the formula. Every calculator is written around a specific rule, equation, or standard method. For example, EMI uses the standard amortization formula, SIP uses the future value of a monthly investment, GST uses taxable value and tax-rate arithmetic, and age uses calendar dates rather than a rough number of days divided by 365. A page is not considered complete until the formula is visible in plain language and the result can be checked with a worked example.",
                "Accuracy also depends on context. Some formulas are exact, such as unit conversion or percentage change. Some are estimates, such as calorie needs or body fat percentage. Some are rule-based but change with government notifications, bank policy, state rules, or employer practice. Calculatorcity tries to separate these cases clearly. Where a rule can change, the page explains the assumption and asks users to verify final decisions with the official source, employer, bank, doctor, tax adviser, or government portal that applies to their situation.",
            ]),
            ("Privacy-first calculation", [
                "Most calculator inputs are personal. Salary, tax, loan amount, body weight, rent, investment contribution, property value, and date of birth can reveal sensitive details. Calculatorcity is designed so calculations run locally in the browser. The normal calculator experience does not require an account and does not send typed calculator values to our server for processing. This keeps the site fast and reduces unnecessary data exposure.",
                "Search boxes and calculator inputs are built for convenience, not profiling. The website may use standard hosting logs, security tools, analytics, or advertising systems in the future, but the calculator logic itself is client-side. The privacy policy explains this in more detail. The short version is simple: use the tools freely, avoid entering information you would not want on a shared screen, and review official documents before acting on a result that affects money, tax, health, employment, or legal rights.",
            ]),
            ("Design standards", [
                "A calculator page should feel calm, not crowded. We use consistent layouts, readable typography, clear labels, large result cards, and responsive controls that work on mobile and desktop. Inputs use sensible defaults and ranges where a slider improves speed. Result values are formatted for their audience, so Indian pages show rupees, commas in the Indian system, and practical language like lakhs and crores when numbers become large.",
                "We also avoid making the homepage a marketing wall. The first job of the site is to help users reach the right calculator. The homepage lists categories, all calculator pages, Indian tools, and popular calculators. The footer now carries the same idea: all categories are visible, the twenty most popular calculators are one click away, and company pages are grouped clearly. Navigation should reduce effort, not create another puzzle.",
            ]),
            ("How users should read results", [
                "Every result should be read with its inputs. If a SIP calculator says a future value could reach a certain amount, the return assumption matters. If a home loan EMI looks affordable, the tenure, interest rate, processing fee, insurance, and income stability still matter. If a tax calculator compares regimes, the result depends on salary structure, deductions, exemptions, surcharge, cess, and rules for the financial year selected on the page. A number without context can be misleading.",
                "Calculatorcity therefore encourages scenario checking. Try a conservative input, an expected input, and a high-cost or low-return input. Compare the direction and size of change. For important decisions, export or write down the inputs before discussing the result with a family member, accountant, lender, doctor, employer, or adviser. The most useful calculator result is one that helps you ask better questions before signing, filing, investing, borrowing, or changing a plan.",
            ]),
            ("How we improve the site", [
                "Calculator pages are living tools. They need updates when rules change, when users report unclear wording, when mobile layouts can be improved, or when a formula needs a better explanation. We review pages for broken links, visible unfinished text, formatting problems, result overflow, and basic accessibility. We also look for practical gaps: missing state data, unclear labels, no worked example, or a result that needs a better comparison chart.",
                "Feedback is welcome, especially when it includes the page URL, the inputs used, the result shown, and the expected result. That information makes a report actionable. For India-specific rules, a link to the official notification, government page, bank circular, or regulator source is especially helpful. We prefer to fix the root issue rather than add vague disclaimers, because users deserve pages that are both useful and honest about their limits.",
            ]),
            ("Our promise", [
                "Calculatorcity will stay focused on practical, free, browser-based calculators. We will not turn simple tools into account-gated workflows. We will not hide basic formulas. We will keep improving readability, mobile behavior, Indian number formatting, and link quality. When a topic requires professional judgement, the page will say so plainly instead of pretending that one calculation can replace a qualified adviser.",
                "The site is built for everyday users: students, parents, employees, freelancers, small business owners, investors, home buyers, teachers, and anyone who needs a quick, clear calculation. If a page helps you understand a number faster and with fewer doubts, it is doing its job. That is the standard we use when adding new calculators and improving the existing ones.",
            ]),
        ],
    },
    "company/privacy-policy.html": {
        "title": "Privacy Policy | Calculatorcity",
        "description": "Read the Calculatorcity privacy policy, including how calculator inputs are handled, what data may be collected, cookies, analytics, advertising, and user choices.",
        "h1": "Privacy Policy",
        "intro": "This privacy policy explains how Calculatorcity handles information when you use our calculator website. We write it in plain language because privacy should be understandable. The key point is that calculator results are generated in your browser, and you do not need to create an account to use the tools.",
        "sections": [
            ("Information you enter into calculators", [
                "Calculatorcity calculators are designed to run locally in your browser. When you type salary, rent, investment amount, loan amount, weight, date of birth, units, marks, or any other calculator value, the page uses JavaScript in your browser to produce the result. The normal calculator workflow does not require those values to be submitted to a Calculatorcity account or saved in a profile. You can refresh the page, change the inputs, and calculate again without signing in.",
                "This local design is important because calculator values can be sensitive. A tax page may reveal income. A health page may reveal body measurements. A loan page may reveal planned borrowing. A property page may reveal purchase value. We encourage users to treat calculator inputs with the same care they would use on any shared computer or public screen. If you are using a device that is not yours, close the tab when finished and avoid saving form values in the browser.",
            ]),
            ("Information collected automatically", [
                "Like most websites, Calculatorcity may receive basic technical information when a page loads. This can include IP address, browser type, device type, pages visited, referring page, approximate location derived from network information, and the time of the request. Hosting providers and security systems use this information to deliver the site, monitor uptime, prevent abuse, diagnose errors, and understand whether pages are loading correctly.",
                "Automatic information is not the same as calculator input. Server logs may show that a browser visited the GST calculator page, but they are not intended to store the amount you typed into the GST amount field. If future features require data submission, such as a contact form or saved report, the page should make that action clear before you send information. We do not want users to guess whether a calculation is private.",
            ]),
            ("Cookies, analytics, and advertising", [
                "Calculatorcity may use cookies or similar technologies for essential site operation, analytics, security, preferences, and advertising. Analytics helps answer practical questions such as which pages are used most, which devices have layout issues, and whether search helps people find calculators. Advertising, if enabled, may use third-party scripts that follow their own policies and may set cookies to measure performance, prevent fraud, or personalize ads according to their settings.",
                "You can control cookies through your browser settings. Blocking some cookies should not stop the basic calculators from working, because the formulas run in the page. Some optional features, advertising, embedded services, or analytics may behave differently if cookies are blocked. We recommend reviewing the privacy controls in your browser, especially if you use shared devices, workplace devices, or school devices.",
            ]),
            ("Search and navigation behavior", [
                "The site includes search boxes to help you find calculators quickly. Search suggestions are built from the calculator index available in the site files. The search feature is intended for navigation, not for collecting personal information. Avoid typing private information into the search box; use calculator inputs only for calculation values. If analytics is enabled in the future, aggregate search behavior may help us improve labels, keywords, and category organization.",
                "Navigation data can also show which pages need improvement. For example, if many users search for EMI and then leave a global loan page to use the India home loan page, that is a signal that local wording and rupee formatting matter. We use that kind of pattern to improve the site structure. The goal is better usability, not building personal profiles around individual calculator use.",
            ]),
            ("Contact messages", [
                "If you contact Calculatorcity, you may provide your name, email address, page URL, message, screenshots, or details about a calculation issue. We use that information to understand the request and respond. For a bug report, the most useful details are the exact page, inputs, expected result, actual result, device, and browser. Do not send sensitive documents, tax IDs, medical records, bank statements, or passwords through ordinary email.",
                "Contact messages may be stored in an email inbox, helpdesk, or similar communication tool. We keep them only as long as reasonably needed for support, record keeping, security, or legal purposes. If you ask us to delete a support conversation, we will consider the request according to applicable rules and practical obligations. We may keep minimal records if needed to prevent abuse or document that a request was handled.",
            ]),
            ("Third-party services", [
                "Some pages may use third-party libraries or services to render charts, fonts, analytics, ads, security checks, or hosted assets. For example, charts can be displayed with a browser library, fonts may be served by a font provider, and future advertising may come from an ad network. These services may receive technical information when their files load. Their handling of information is governed by their own privacy policies.",
                "We try to keep third-party use practical and limited. A calculator should not depend on unnecessary trackers to perform arithmetic. Where a library is used, it should improve the user experience, such as making a chart clearer or typography more readable. If a third-party service fails to load, the calculator should still provide the core result whenever possible.",
            ]),
            ("Children and students", [
                "Calculatorcity includes educational tools that students may use, such as percentage, fraction, CGPA, GPA, grade, probability, and unit conversion calculators. The site is not designed to knowingly collect personal information from children. Students should avoid entering private personal details into optional text fields, and parents or teachers should supervise internet use according to their own rules.",
                "Educational calculators are meant to explain methods, not help users avoid learning. Many pages show formulas and worked examples so students can understand how the answer is produced. If a school or parent has rules about calculator use during homework or exams, those rules should be followed. Privacy and academic honesty both depend on using tools in the right context.",
            ]),
            ("Security and retention", [
                "No website can promise perfect security, but Calculatorcity is designed to reduce risk by avoiding unnecessary accounts and keeping calculations local where possible. We use ordinary security practices for a static website, such as limiting what data is collected, keeping dependencies purposeful, and monitoring for broken or suspicious behavior. Users should also protect themselves by keeping browsers updated and avoiding sensitive calculations on untrusted devices.",
                "Server logs, analytics records, advertising records, and support messages may have different retention periods depending on the service involved and the reason for keeping them. We aim to keep information only as long as it is useful for operation, security, support, compliance, or improvement. Aggregated statistics that do not identify a person may be kept longer because they help us understand site quality over time.",
            ]),
            ("Your choices", [
                "You can choose not to use a calculator, clear form fields, block cookies, use browser privacy settings, disable JavaScript, or contact us with privacy questions. Disabling JavaScript will stop most calculators because the formulas run in the browser. If you need maximum privacy for a sensitive calculation, use a trusted personal device, close other tabs, avoid screen sharing, and do not send the result through unencrypted channels unless you are comfortable doing so.",
                "You may also ask questions about information you intentionally sent to us, such as contact messages. Include enough detail for us to identify the message without sending extra sensitive data. We may need to verify the request before acting on it. Privacy rights vary by location, but our practical approach is to answer clearly and avoid keeping information that has no useful purpose.",
            ]),
            ("Changes to this policy", [
                f"This policy may be updated as the website changes. The latest update date is {UPDATED}. If we add new features that materially change how information is handled, the policy should be updated to explain those changes. Continued use of the site after an update means the current version applies to your use.",
                "For urgent legal, tax, medical, or financial decisions, privacy is only one part of responsible use. You should also verify formulas, rates, and rules with official sources. Calculatorcity helps with calculation and explanation, but the final decision and the decision context remain yours.",
            ]),
        ],
    },
    "company/terms-and-conditions.html": {
        "title": "Terms & Conditions | Calculatorcity",
        "description": "Read the Calculatorcity terms and conditions for using free online calculators, including acceptable use, disclaimers, intellectual property, and limitations.",
        "h1": "Terms & Conditions",
        "intro": "These terms explain the rules for using Calculatorcity. By using the website, you agree to use the calculators responsibly, understand that results are educational estimates unless clearly stated otherwise, and verify important decisions with the official source or a qualified professional.",
        "sections": [
            ("Use of the website", [
                "Calculatorcity provides free online calculators and explanatory content for general education, planning, comparison, and convenience. You may use the site to calculate percentages, interest, EMI, tax estimates, unit conversions, health estimates, date differences, and other everyday values. The tools are designed for normal personal, educational, and business planning use. You do not need an account for ordinary calculator access.",
                "You agree not to misuse the site. Misuse includes attempting to attack, scrape aggressively, overload, reverse engineer for harmful purposes, inject malicious code, bypass security controls, remove attribution from copied content, or use calculator results in a way that harms others. Reasonable personal use, classroom use, internal business use, and sharing links to useful pages are welcome.",
            ]),
            ("Calculator results are not professional advice", [
                "Calculator results can be useful, but they are not a substitute for professional advice. Financial calculators do not replace a financial planner, lender, auditor, or chartered accountant. Tax calculators do not replace the Income-tax Act, GST rules, government portals, employer payroll systems, or professional tax advice. Health calculators do not replace a doctor, dietitian, or medical diagnosis. Legal or eligibility calculations do not replace the official notification, contract, or law that controls the situation.",
                "Some calculations are exact arithmetic, while others are estimates. Unit conversions and percentage formulas are generally deterministic. Calorie needs, body fat, sleep needs, investment returns, future market values, loan affordability, and tax comparisons depend on assumptions. Before acting on an important result, check the inputs, formula, date, rule year, and official source. You are responsible for deciding whether a calculator result is suitable for your specific situation.",
            ]),
            ("India-specific calculators", [
                "The India section includes calculators for GST, income tax, EMI, SIP, FD, salary, EPF, PPF, NPS, gratuity, HRA, TDS, stamp duty, on-road vehicle price, AP electricity bills, gold jewellery value, CGPA conversion, Sukanya Samriddhi, and advance tax. These pages use Indian formatting and practical local assumptions. They are built to help users understand rupee amounts, lakhs, crores, deductions, slabs, charges, and examples more clearly.",
                "Indian rules can change by financial year, notification, state, bank, employer, discom, university, or department. A state transport rate, stamp duty concession, small-savings interest rate, tax slab, surcharge rule, professional tax amount, or electricity tariff can change after a page is published. Treat India-specific results as planning aids and verify final payments, filings, registrations, or claims with the official portal, professional adviser, or department responsible for the decision.",
            ]),
            ("User responsibilities", [
                "You are responsible for entering accurate inputs. A calculator cannot know whether the salary entered is gross salary or basic salary unless the label says so. It cannot know whether a date is a cutoff date, invoice date, due date, or birth date unless you choose the right field. It cannot know whether a bank offer includes insurance, processing fees, penalties, or floating-rate changes unless those details are entered or considered separately.",
                "You are also responsible for reviewing outputs before using them. Check whether the value is rounded, whether tax is included or excluded, whether a number is monthly or yearly, whether the currency is correct, and whether an assumption is realistic. If a result looks too high, too low, or surprising, compare it with a manual estimate and review the formula section on the page. Reporting suspected errors helps improve the site for everyone.",
            ]),
            ("Content ownership and permitted use", [
                "The website design, text, page structure, calculator logic, tables, and original explanations are owned by Calculatorcity or used with permission where applicable. You may link to pages, quote short excerpts with attribution, and use results for personal, educational, or internal planning. You may not copy large parts of the site, republish pages as your own, remove branding, or create a competing mirror without permission.",
                "Calculator formulas that are standard mathematical or legal concepts are not owned by Calculatorcity. What is protected is the expression, layout, code implementation, explanations, and compilation of content. If you want to reference a calculator in a class, article, spreadsheet, or support document, linking to the page is the simplest and clearest approach.",
            ]),
            ("Availability and changes", [
                "Calculatorcity aims to keep pages available and working, but we do not guarantee uninterrupted access. Static websites can still be affected by hosting issues, network problems, browser bugs, third-party library outages, or maintenance. We may update, add, remove, rename, or reorganize calculators and company pages as the site improves. Links may change if a better structure is needed, though we try to avoid unnecessary disruption.",
                "We may also change formulas, examples, tables, design, or explanations when we find a better method or when rules change. A result from an older version of a page may differ from a result generated later if inputs, assumptions, rates, or rules changed. For important records, save the result together with the date, inputs, and source documents used at the time.",
            ]),
            ("Third-party links and services", [
                "The website may refer to external services, official portals, chart libraries, font providers, analytics systems, advertising networks, or sources of further information. External sites are controlled by their own operators, not by Calculatorcity. We are not responsible for their content, availability, privacy practices, pricing, advice, or transactions. Use external links with normal caution and verify that the page is official before entering sensitive information.",
                "If advertising appears on the site, ad content may be selected by third-party systems. An advertisement is not an endorsement of the advertiser, product, or claim. Users should apply the same judgement to ads that they would use anywhere else on the internet, especially for financial products, loans, investments, medical services, education programs, and government-related services.",
            ]),
            ("Limitation of liability", [
                "To the maximum extent allowed by law, Calculatorcity is provided on an as-is and as-available basis. We do not promise that every result will be error-free, complete, current, or suitable for every use case. We are not liable for losses arising from reliance on calculator results, content, delays, interruptions, external links, ads, or user input mistakes. This limitation applies even if a result affects money, tax, health, eligibility, employment, travel, education, or legal timing.",
                "Some jurisdictions do not allow certain limitations, so parts of this section may not apply to every user. The practical rule remains the same: use Calculatorcity as a helpful calculation and learning tool, then verify important decisions with the controlling source. A transparent calculator can reduce arithmetic mistakes, but it cannot take responsibility for the real-world decision that follows.",
            ]),
            ("Contact and updates", [
                f"These terms were last updated on {UPDATED}. We may update them when the site changes, when new features are added, or when wording can be made clearer. Continued use of the site after updates means the current terms apply. If you do not agree with the terms, you should stop using the website.",
                "Questions, corrections, and bug reports are welcome through the Contact Us page. Useful reports include the page URL, exact inputs, expected result, actual result, browser, device, and a link to any official source that supports the correction. Clear reports help us improve the calculator rather than guessing at the issue.",
            ]),
        ],
    },
    "company/blogs.html": {
        "title": "Blogs | Calculatorcity",
        "description": "Read practical Calculatorcity guides about calculators, personal finance, Indian tax tools, unit conversion, health estimates, and using results responsibly.",
        "h1": "Calculatorcity Blogs",
        "intro": "The Calculatorcity blog is a practical reading hub for people who want to understand calculator results, not just copy the final number. These guides explain how to use calculators thoughtfully, compare scenarios, and avoid common mistakes in finance, tax, health, education, and everyday math.",
        "sections": [
            ("How to choose the right calculator", [
                "The fastest way to get a useful result is to choose the page that matches the real question. If you want to know a monthly loan payment, use an EMI calculator, not a simple interest calculator. If you want to know how much a monthly investment may grow, use SIP, not FD. If you want a tax comparison for India, use the India income tax page, not a global percentage page. Matching the calculator to the question prevents most mistakes before any number is entered.",
                "Read the input labels before typing. A field labelled annual rate expects a yearly percentage, while a field labelled monthly contribution expects one month of investment. A salary calculator may need annual CTC, but HRA exemption needs monthly basic salary, HRA received, and rent paid. If the calculator has a mode switch, such as add GST versus remove GST, set the mode first. Correct input structure matters as much as the formula.",
            ]),
            ("Why scenario comparison matters", [
                "One calculator result is useful, but three results are often more useful. A conservative scenario shows what happens if returns are lower, rates are higher, or expenses increase. An expected scenario uses the most realistic assumption available today. An optimistic scenario shows the upside, but should not be treated as guaranteed. This habit is powerful for SIP, NPS, PPF, EMI, mortgage, inflation, break-even, and retirement planning.",
                "Scenario comparison also helps with negotiation. If a car dealer quotes a high on-road price, changing insurance, handling charges, or state tax assumptions shows which part of the quote matters. If a lender offers a lower EMI by extending tenure, comparing total interest reveals the hidden cost. If a salary offer looks attractive as CTC, a take-home calculator shows the effect of PF, professional tax, TDS, and allowances. Good decisions come from seeing the tradeoff, not just the headline.",
            ]),
            ("Using Indian finance calculators well", [
                "Indian calculators need Indian formatting and rule context. A result of 10000000 is harder to read than ₹1,00,00,000, and the practical meaning is one crore. Salary, tax, investment, GST, EPF, PPF, NPS, and property calculations often involve thresholds in lakhs, crores, or statutory limits. Calculatorcity pages use rupees, Indian grouping, and relevant tables so that users do not have to mentally translate global number formats.",
                "Rules still need verification. Income tax slabs can change by financial year. PPF, SSY, and EPF rates are notified periodically. Stamp duty and road tax vary by state. Electricity tariffs depend on category, slab, and discom. University CGPA rules differ. Treat calculators as a clean workspace for understanding the calculation, then confirm the final rule on the official portal, employer document, bank letter, or government notification before making a payment or filing a return.",
            ]),
            ("Personal finance calculators are planning tools", [
                "A finance calculator can show scale, direction, and sensitivity. It cannot guarantee future returns or remove risk. SIP and NPS pages assume an expected annual return, but markets do not move in a straight line. FD and PPF calculators are more stable, but rates can change and taxes may affect the final result. EMI calculators use the entered rate and tenure, but floating rates, prepayments, fees, insurance, and penalties can change the actual cost.",
                "The best way to use a finance calculator is to ask practical questions. Can I afford the EMI if income drops for two months? What happens if the interest rate rises by one percent? How much more interest do I pay by choosing twenty-five years instead of fifteen? How much SIP is needed for a one crore goal at different return assumptions? The calculator becomes valuable when it helps you test decisions before money moves.",
            ]),
            ("Health calculators need careful interpretation", [
                "Health calculators are useful for orientation, not diagnosis. BMI, calorie, body fat, water intake, heart-rate zones, protein intake, sleep, pregnancy dates, and steps-to-calories estimates depend on formulas and assumptions. Two people with the same BMI can have different muscle mass, health history, age, and goals. A calorie estimate can be a starting point, but real progress depends on tracking, consistency, sleep, stress, medical conditions, and professional guidance when needed.",
                "Use health calculators to prepare better questions. If a calorie target seems extreme, ask why. If heart-rate zones feel too hard or too easy, check resting heart rate, medication, training history, and device accuracy. If pregnancy dates are involved, follow your clinician’s advice and scan dates. Calculatorcity explains formulas so users know what the number means and where its limits begin.",
            ]),
            ("Education calculators and honest learning", [
                "Math and education calculators can save time, but they are most useful when they teach the method. A percentage calculator should make it clear that part divided by whole times one hundred gives the percentage. A fraction calculator should show simplification. CGPA and GPA pages should identify the conversion rule, because universities and boards do not always use the same multiplier. Grade calculators should separate achieved marks, weights, and required final exam scores.",
                "Students should follow their school or college rules for calculator use. A tool can help check homework, understand formulas, and catch arithmetic mistakes, but it should not replace learning the concept. Teachers and parents can use calculator pages as examples because formulas, tables, and worked examples make the result easier to discuss. A transparent calculator supports learning better than a black-box answer.",
            ]),
            ("Unit conversion mistakes to avoid", [
                "Unit conversion looks simple until the wrong unit is used in a real project. Length, area, volume, pressure, energy, speed, data storage, and temperature all have contexts where a small mistake can become expensive. Area conversion is especially easy to misread because square units grow differently from linear units. Temperature conversion has offsets, so Celsius and Fahrenheit cannot be converted with only a multiplier. Data storage can use decimal or binary meanings depending on context.",
                "When converting units, write down the original value, original unit, target unit, and reason for the conversion. If the value will be used in engineering, medicine, construction, travel, shipping, or pricing, verify the result with the relevant professional standard. Calculatorcity gives quick conversions and reference tables, but the surrounding context still matters.",
            ]),
            ("What makes a calculator trustworthy", [
                "A trustworthy calculator has clear labels, visible formulas, realistic examples, readable results, useful reference tables, and honest limitations. It should not hide important assumptions or force users through unnecessary steps. It should work on mobile, prevent obvious layout breakage, and keep large numbers readable. It should avoid fake precision by rounding results to a practical level. It should also link users to related calculators when the next question is obvious.",
                "Trust also comes from maintenance. Broken links, input hint labels, outdated rates, unreadable result cards, and generic content reduce confidence. Calculatorcity’s production checklist includes link audits, HTTP checks, syntax checks, footer consistency, mobile-friendly layout, and removal of visible unfinished text. A calculator site earns trust by being boring in the right ways: stable, clear, fast, and predictable.",
            ]),
            ("Future blog topics", [
                "Future Calculatorcity guides will cover how to compare new and old Indian tax regimes, how to read an EMI amortization table, how inflation affects long-term goals, how to estimate a realistic SIP target, how to avoid mistakes in CTC to in-hand salary calculations, and how to use stamp duty and on-road price calculators before negotiating a purchase. We will also add guides for students, teachers, and small business owners.",
                "The blog will stay connected to the calculators. Each article should help users understand a tool better or use a result more responsibly. We are not trying to publish vague financial or health advice. The aim is practical explanation: what the calculator asks, what the result means, what assumptions matter, and when to verify with an official source or professional.",
            ]),
        ],
    },
    "company/contact-us.html": {
        "title": "Contact Us | Calculatorcity",
        "description": "Contact Calculatorcity for calculator feedback, bug reports, correction requests, content suggestions, partnerships, and general support questions.",
        "h1": "Contact Us",
        "intro": "Have a question, correction, or suggestion for Calculatorcity? Use this page to understand the best way to contact us and what details make a report useful. Clear feedback helps us fix calculator issues faster and improve the site for everyone.",
        "sections": [
            ("Best way to reach us", [
                "For general questions, corrections, and feedback, email us at contact@calculatorcity.in. A useful message explains what page you were using, what you expected, what happened instead, and whether the issue is about formula accuracy, wording, layout, links, mobile behavior, or missing content. If the issue is India-specific, include the official source or notification if you have one. That helps us verify the rule rather than guessing.",
                "Please do not send sensitive documents such as tax returns, bank statements, medical reports, passwords, Aadhaar numbers, PAN images, salary slips, or private contracts. Calculator issues can usually be reported with sample inputs instead of real personal data. For example, you can say that a ₹10,00,000 input at 18% GST produced an unexpected result without sharing an actual invoice.",
            ]),
            ("Bug reports", [
                "Bug reports are most helpful when they are specific. Include the page URL, browser name, device type, screen size if relevant, input values, selected options, result shown, and result expected. If a button does not respond, mention whether other calculators work. If a chart is blank, mention whether the result cards still calculate. If a result card overflows, include the exact large number entered. These details help separate formula bugs from layout bugs.",
                "A strong bug report might say: On the SIP calculator, I entered monthly SIP ₹5,00,000, expected return 20%, period 40 years, and the large result value overflowed the card on desktop. That report is actionable because it includes the calculator, input values, symptom, and device context. Vague reports such as the calculator is wrong are harder to fix because we have to recreate the missing details.",
            ]),
            ("Formula corrections", [
                "Formula corrections are welcome, especially for tax, state, banking, education, and utility topics. Please include the exact rule source when possible. For Indian tax pages, useful sources include Finance Act changes, Income Tax Department pages, GST notifications, EPFO updates, PFRDA notes, or official small-savings rate notifications. For state pages, government department pages or official circulars are better than screenshots from third-party websites.",
                "We review corrections carefully because changing a calculator affects many users. Sometimes two sources appear to disagree because they apply to different years, categories, states, income types, consumer classes, or edge cases. In those situations, we may update wording to make the assumption clearer rather than changing the formula for everyone. The goal is correctness plus transparency.",
            ]),
            ("Content suggestions", [
                "If you want a new calculator, describe the problem it should solve and the formula or rule it should use. A good suggestion includes example inputs, expected outputs, units, common edge cases, and a note about who would use it. For example, a good request for an India page might include a state, rule year, official rate table, and a sample calculation. A good request for a science page might include the equation, unit conversions, and common classroom examples.",
                "We prioritize calculators that many people need, have clear formulas, and can be explained responsibly in a static browser page. We are especially interested in tools that reduce confusion around Indian personal finance, tax, salary, property, vehicle, education, utility, and investment decisions. We also improve existing pages when a better table, FAQ, chart, or worked example would help more than a new page.",
            ]),
            ("Partnership and media questions", [
                "Calculatorcity is a calculator and educational utility site. If you want to reference a calculator in an article, classroom resource, help document, or internal workflow, you can link directly to the relevant page. If you want broader collaboration, content correction, attribution, or permission for larger reuse, contact us with the purpose, pages involved, expected audience, and publication format.",
                "We do not endorse products simply because they relate to a calculator. Financial, loan, tax, education, health, insurance, investment, and property topics require user trust. Any partnership request should be transparent about the organization, offer, compensation, and user impact. Calculatorcity’s first obligation is to keep calculator pages clear and useful.",
            ]),
            ("Support expectations", [
                "Calculatorcity is a free website, so support is practical rather than instant. We aim to prioritize issues that affect calculation accuracy, broken pages, navigation, accessibility, mobile layout, visible unfinished text, and official rule updates. General questions may take longer, especially if they require research or if the issue is better handled by a professional adviser.",
                "We cannot provide personal financial planning, tax filing, legal advice, medical diagnosis, or official eligibility decisions by email. We can clarify how a calculator works, review a potential bug, improve wording, or consider a correction. If your decision has legal, tax, medical, or financial consequences, use the calculator as preparation and then speak with the appropriate professional or official source.",
            ]),
            ("Accessibility feedback", [
                "Accessibility matters because calculator pages are often used under pressure. If a label is unclear, a button is hard to tap, a contrast level is weak, a result does not announce properly, or keyboard navigation fails, tell us the page and device. We try to use semantic HTML, visible labels, readable tables, responsive layouts, and predictable controls, but real feedback catches issues that automated checks can miss.",
                "Mobile feedback is especially useful. Many users calculate EMI, GST, salary, CGPA, and unit conversions on phones. A page that looks fine on desktop can still have crowded controls, long result values, or tables that need horizontal scrolling on smaller screens. Screenshots are helpful if they avoid personal information.",
            ]),
            ("Privacy when contacting us", [
                "Contact messages are different from calculator inputs. Calculator inputs normally run locally in your browser, but an email you send is intentionally transmitted. Keep messages focused on the issue and use sample data when possible. If we need more information, we will ask for the minimum practical detail. We do not need your full identity to fix most calculator bugs.",
                "If you send a correction request, we may keep the message while reviewing and updating the page. If you later want a support message deleted, contact us from the same email address and describe the request. Some minimal records may remain if needed for security, abuse prevention, or legal compliance, but we aim to avoid unnecessary storage.",
            ]),
            ("Quick contact checklist", [
                "Before sending a message, check whether the calculator page already has a formula section, FAQ, important notes, or reference table that answers the question. If the issue remains, include the page URL, exact inputs, selected mode, actual result, expected result, device, browser, and source for corrections. This checklist may feel detailed, but it saves time and helps us fix the right thing.",
                "Thank you for helping improve Calculatorcity. A calculator website becomes stronger when users report real problems from real use: a confusing label, an outdated rule, a broken link, a result that needs better formatting, or a missing example. Those details help turn a basic tool into a reliable public resource.",
            ]),
        ],
        "extra": '<div class="contact-actions"><a class="calc-btn" href="mailto:contact@calculatorcity.in">Email Calculatorcity</a></div>',
    },
    "company/help.html": {
        "title": "Help | Calculatorcity",
        "description": "Get help using Calculatorcity calculators, search, inputs, result cards, Indian number formatting, mobile layout, privacy, and troubleshooting.",
        "h1": "Help Center",
        "intro": "This help page explains how to use Calculatorcity efficiently, how to read calculator results, and what to do if something looks wrong. Most tools are simple, but a few careful habits make the results easier to trust.",
        "sections": [
            ("Finding the right calculator", [
                "Use the homepage categories, header navigation, footer categories, or search box to find a calculator. Categories group tools by the type of question: math, finance, unit converters, health and fitness, date and time, science and other, and India calculators. If you are working with rupee values, Indian tax, salary, GST, EPF, PPF, NPS, stamp duty, or state-specific charges, start with the India category because those pages use local assumptions and Indian number formatting.",
                "The search box understands calculator names and common keywords. Typing GST, EMI, SIP, BMI, age, percentage, FD, PPF, or income tax should show relevant tools. Search is for navigation only. Do not type private financial, health, or identity information into the search box. Use the calculator input fields for values and keep sensitive documents outside the website unless you are deliberately contacting support.",
            ]),
            ("Entering values correctly", [
                "Read every label before entering values. A field may ask for monthly amount, annual amount, principal, rate, tenure, rent paid, basic salary, total income, or units consumed. These are not interchangeable. If a calculator has a toggle such as years versus months, rupees versus percent, add GST versus remove GST, or metro versus non-metro, set the toggle before relying on the result. The calculator can only apply the formula to the inputs it receives.",
                "For money fields, use digits with or without commas. India pages display rupee values and use Indian grouping such as ₹1,00,000 and ₹1,00,00,000. Large results may also be easier to think about as lakhs and crores. Non-India formatting can use thousands, millions, and billions depending on the browser locale. If a field rejects a symbol, enter only the number. The output will usually apply the correct display format.",
            ]),
            ("Understanding result cards", [
                "Result cards separate the main answer from supporting values. For example, an EMI page may show monthly EMI, total interest, total payment, and processing fee. A GST page may show taxable base, GST, CGST, SGST, and invoice total. A tax page may show taxable income, tax before cess, cess, total tax, and monthly TDS. Read all cards before deciding what the answer means.",
                "Large numbers are formatted to stay readable and stay inside their result cards. If a result wraps onto two lines, that is intentional; it is better than letting a long number overflow into another part of the page. When comparing results, focus on both the exact number and the direction of change. A small interest-rate or return assumption can move long-term results by lakhs or crores.",
            ]),
            ("Using charts and tables", [
                "Many calculators include charts, tables, or visual scales. Charts are there to make patterns visible: invested amount versus returns, principal versus interest, balance falling over time, or cost components in a vehicle price. Tables provide reference values, common examples, slabs, rates, or conversions. They should support the main result rather than distract from it.",
                "If a chart does not load because a browser extension blocks scripts or a third-party library fails, the result cards should still be the primary source. Refresh the page, try another browser, or disable aggressive content blocking for the site if you want the chart. Tables can be scrolled horizontally on small screens where needed.",
            ]),
            ("Checking accuracy", [
                "To check a result, start with a rough mental estimate. Ten percent of 1,000 is 100. A five-year monthly SIP has sixty contributions. A twelve-month loan has twelve payments. A date difference across one week should be seven days. These quick checks catch decimal mistakes, wrong units, reversed dates, and incorrect modes. Then read the formula section for the exact method.",
                "For rule-based pages, confirm the effective year or state. Income tax, GST, stamp duty, electricity tariff, professional tax, small-savings interest, EPF interest, vehicle tax, and university conversion rules can change. Calculatorcity aims to keep content useful, but official portals and notifications control final decisions. If you find an outdated rule, contact us with the source.",
            ]),
            ("Troubleshooting common issues", [
                "If a calculator does not respond, make sure JavaScript is enabled. Calculatorcity calculators run in the browser, so disabling JavaScript will stop most tools. If a result looks blank, check that required fields are filled and that the value is within the allowed range. If a slider appears stuck, try typing the value directly into the input beside it. If a date result seems wrong, check whether the date is in the expected format and whether the page asks for today, a due date, a birth date, or a cutoff date.",
                "If the page layout looks broken, refresh the page and try another browser. Very old browsers may not support newer layout or chart features. Browser extensions that block scripts, fonts, or styles can also affect appearance. On mobile, rotate the device or scroll tables horizontally if a reference table has many columns.",
            ]),
            ("Privacy basics", [
                "Most calculator inputs are processed locally in your browser. You do not need an account, and the ordinary calculator workflow does not require sending your salary, investment amount, body weight, loan value, or date of birth to a server. Still, you should use common sense. Do not calculate sensitive values on a public screen, shared device, or recorded video call if you are not comfortable with others seeing them.",
                "Contact messages are different because email or support requests are intentionally transmitted. Use sample data when reporting bugs. For example, you can describe a GST calculation with a sample ₹1,00,000 amount rather than sending an actual invoice. Review the Privacy Policy for more detail.",
            ]),
            ("When to ask a professional", [
                "Ask a professional when a result affects tax filing, legal rights, medical care, investment suitability, loan commitments, property purchase, employment decisions, or official eligibility. A calculator can show the arithmetic, but it cannot know every personal fact or local rule. A chartered accountant, lawyer, doctor, lender, government office, employer, university, or certified adviser may be needed for final confirmation.",
                "This is not a weakness of calculators. It is the boundary between calculation and judgement. Calculatorcity helps you prepare better questions, compare scenarios, and catch mistakes before a conversation with a professional. The final decision should come from the authority that controls the matter.",
            ]),
            ("Mobile and accessibility tips", [
                "Calculatorcity is designed for mobile and desktop. On phones, use the search box, quick links, and category sections to move quickly. Tap labels carefully, use numeric keyboards where available, and scroll result sections fully before leaving the page. If a table is wide, swipe sideways inside the table area. If text appears too small because of browser zoom settings, increase the browser text size.",
                "Keyboard users can tab through links, inputs, and buttons. Screen-reader users should benefit from labels, headings, and aria-live result regions on calculator widgets. If any page is hard to use with assistive technology, contact us with the page, device, browser, and specific problem. Accessibility feedback is treated as a product-quality issue, not a nice-to-have.",
            ]),
            ("Getting more from Calculatorcity", [
                "Use related calculator links when one question leads to another. A home buyer may use home loan EMI, stamp duty, on-road price for a vehicle, and income tax in the same planning session. A student may use percentage, CGPA, grade, and average. A fitness user may use BMI, calorie, protein intake, water intake, and heart-rate zones together. The footer popular links are designed to keep high-demand tools one click away.",
                "For important planning, write down the inputs, result, page name, and date. This makes it easier to compare later or explain the calculation to someone else. A saved result without inputs is hard to audit. A saved result with inputs becomes a useful record of the assumption you used at that time.",
            ]),
        ],
    },
}


STANDARD_COMPANY_GUIDE = section("How to use this page", [
    "Read company pages the same way you would read a calculator result: start with the purpose, then check the details that apply to your situation. The About page explains why the site exists and how we think about quality. The Privacy Policy explains what happens to information during normal use. The Terms page explains the boundary between a helpful calculation and professional advice. The Blog page gives practical learning guides. Contact and Help explain how to get support and report issues clearly.",
    "If you are reviewing Calculatorcity for production use, school use, workplace sharing, or a family recommendation, look for three things. First, calculator inputs should be labelled clearly enough that a user knows what to type. Second, pages should explain formulas and limitations instead of presenting a number without context. Third, navigation should make important tools easy to find without hiding legal, privacy, help, or contact information. These pages are written to support that level of review.",
    "For important decisions, keep the calculator page, inputs, and company guidance together. A result is strongest when the user understands both the arithmetic and the responsibility for applying it. Calculatorcity can make calculations faster and clearer, but official rules, professional judgement, and personal circumstances still matter. When in doubt, use the site to prepare better questions, then verify the final answer with the authority that controls the decision.",
])


def company_page(path: str, data: dict) -> str:
    blocks = [section(title, paragraphs) for title, paragraphs in data["sections"]]
    extra = data.get("extra", "")
    page = ROOT / path
    prefix = "" if page.parent == ROOT else "../"
    return f"""{page_head(data["title"], data["description"], path)}
<body>
  {nav_for(page)}
  <main id="main" class="page-container company-page">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="{prefix}index.html">Home</a><span>{data["h1"]}</span></nav>
    <section class="company-hero">
      <span class="badge">Company</span>
      <h1>{data["h1"]}</h1>
      <p>{data["intro"]}</p>
      {extra}
    </section>
{chr(10).join(blocks)}
{STANDARD_COMPANY_GUIDE}
  </main>
  {footer_for(page)}
  <script src="{prefix}assets/js/main.js"></script>
</body>
</html>
"""


def add_favicon_link(text: str) -> str:
    if 'rel="icon"' in text:
        return text
    return text.replace(
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n  <link rel="icon" href="/assets/icons/favicon.svg" type="image/svg+xml">',
        1,
    )


def update_existing_html() -> None:
    for page in ROOT.rglob("*.html"):
        if page.relative_to(ROOT).as_posix() in PAGES:
            continue
        text = page.read_text(encoding="utf-8")
        text = text.replace(OLD_DOMAIN, DOMAIN)
        text = add_favicon_link(text)
        text, count = re.subn(r'(?:<hr class="footer-separator" aria-hidden="true">\s*)?<footer class="site-footer">.*?</footer>', footer_for(page), text, count=1, flags=re.S)
        if count != 1:
            raise RuntimeError(f"Footer replacement failed for {page}")
        page.write_text(text, encoding="utf-8", newline="")


def write_company_pages() -> None:
    (ROOT / "company").mkdir(exist_ok=True)
    for path, data in PAGES.items():
        (ROOT / path).write_text(company_page(path, data), encoding="utf-8", newline="")


def remove_legacy_company_pages() -> None:
    legacy = [
        "about-us.html",
        "privacy-policy.html",
        "terms-and-conditions.html",
        "blogs.html",
        "contact-us.html",
        "help.html",
    ]
    for name in legacy:
        path = ROOT / name
        if path.exists():
            path.unlink()


def update_generator() -> None:
    path = ROOT / "tools" / "generate-india-pages.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace(f'DOMAIN = "{OLD_DOMAIN}"', f'DOMAIN = "{DOMAIN}"')
    text = re.sub(
        r'def footer\(\) -> str:\n    return """.*?"""\n\n\nRELATED = \[',
        'def footer() -> str:\n    return """' + footer_for(ROOT / "india" / "sample.html").replace('"""', '\\"\\"\\"') + '"""\n\n\nRELATED = [',
        text,
        count=1,
        flags=re.S,
    )
    path.write_text(text, encoding="utf-8", newline="")


def write_sitemap() -> None:
    pages = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts)
    index = ROOT / "index.html"
    if index in pages:
        pages.remove(index)
        pages.insert(0, index)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for page in pages:
        rel_path = page.relative_to(ROOT).as_posix()
        loc = DOMAIN + ("/" if rel_path == "index.html" else f"/{rel_path}")
        priority = "1.0" if rel_path == "index.html" else ("0.6" if rel_path in PAGES else "0.8")
        lines.append(f"  <url><loc>{loc}</loc><changefreq>monthly</changefreq><priority>{priority}</priority></url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")
    ET.parse(ROOT / "sitemap.xml")


def write_robots() -> None:
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n",
        encoding="utf-8",
        newline="",
    )


def word_count(path: Path) -> int:
    text = re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", path.read_text(encoding="utf-8"), flags=re.S)
    return len(re.findall(r"[A-Za-z0-9₹%'-]+", text))


def main() -> None:
    remove_legacy_company_pages()
    update_existing_html()
    write_company_pages()
    update_generator()
    write_sitemap()
    write_robots()
    for path in PAGES:
        count = word_count(ROOT / path)
        if count < 1500:
            raise RuntimeError(f"{path} has only {count} words")
    print("Production polish complete")
    print("Company pages:", ", ".join(PAGES))


if __name__ == "__main__":
    main()


