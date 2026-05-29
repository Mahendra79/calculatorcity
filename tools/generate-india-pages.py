from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDIA_DIR = ROOT / "india"
DOMAIN = "https://calculatorcity.in"


COMMON_JS = r"""
function formatIndianNumber(n) {
  if (isNaN(n)) return '0';
  let s = Math.abs(n).toFixed(2);
  let [int, dec] = s.split('.');
  let lastThree = int.slice(-3);
  let rest = int.slice(0, -3);
  if (rest) lastThree = rest.replace(/\B(?=(\d{2})+(?!\d))/g, ',') + ',' + lastThree;
  return (n < 0 ? '-' : '') + '₹' + lastThree + '.' + dec;
}
function formatPlainNumber(n, digits = 2) {
  const number = Number(n);
  if (!Number.isFinite(number)) return '0';
  return number.toLocaleString('en-IN', { maximumFractionDigits: digits });
}
function getPreferredNumberLocale() {
  const language = navigator.language || 'en-US';
  const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
  if (/(^|-)IN\b/i.test(language) || timeZone === 'Asia/Kolkata' || timeZone === 'Asia/Calcutta') return 'en-IN';
  return language;
}
function usesIndianNumberSystem() {
  return getPreferredNumberLocale() === 'en-IN';
}
function parseFormattedNumber(raw) {
  const cleaned = String(raw || '').replace(/[^\d.-]/g, '');
  const normalized = cleaned.replace(/(?!^)-/g, '').replace(/^(-?)\./, '$10.').replace(/(\..*)\./g, '$1');
  const number = Number(normalized);
  return Number.isFinite(number) ? number : 0;
}
function formatShortIndian(n) {
  const number = Number(n) || 0;
  const abs = Math.abs(number);
  if (usesIndianNumberSystem()) {
    if (abs >= 10000000) return `${formatPlainNumber(number / 10000000, 2)} Cr`;
    if (abs >= 100000) return `${formatPlainNumber(number / 100000, 2)} L`;
    return formatPlainNumber(number, 0);
  }
  const formatter = new Intl.NumberFormat(getPreferredNumberLocale(), { maximumFractionDigits: 2 });
  if (abs >= 1000000000) return `${formatter.format(number / 1000000000)} B`;
  if (abs >= 1000000) return `${formatter.format(number / 1000000)} M`;
  if (abs >= 1000) return `${formatter.format(number / 1000)} K`;
  return formatter.format(number);
}
function value(id) {
  const el = document.getElementById(id);
  return el ? parseFormattedNumber(el.value) : 0;
}
function text(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}
function html(id, value) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = value;
}
function clamp(number, min, max) {
  return Math.min(Math.max(Number(number) || 0, min), max);
}
function syncRange(rangeId, inputId, callback) {
  const range = document.getElementById(rangeId);
  const input = document.getElementById(inputId);
  if (!range || !input) return;
  range.addEventListener('input', () => {
    input.value = range.value;
    if (typeof updateRangeInput === 'function') updateRangeInput(range);
    callback();
  });
  input.addEventListener('input', () => {
    range.value = clamp(value(inputId), range.min || 0, range.max || value(inputId));
    if (typeof updateRangeInput === 'function') updateRangeInput(range);
    callback();
  });
}
function bindCalculator(callback) {
  const button = document.getElementById('calculate');
  if (button) button.addEventListener('click', callback);
  document.querySelectorAll('.calc-widget input, .calc-widget select').forEach((el) => {
    el.addEventListener('input', callback);
    el.addEventListener('change', callback);
  });
  window.addEventListener('load', callback);
}
function drawChart(canvasId, type, labels, datasets, options = {}) {
  if (typeof Chart === 'undefined') return;
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  window.indiaCharts = window.indiaCharts || {};
  if (window.indiaCharts[canvasId]) window.indiaCharts[canvasId].destroy();
  window.indiaCharts[canvasId] = new Chart(canvas, {
    type,
    data: { labels, datasets },
    options: Object.assign({
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: true } }
    }, options)
  });
}
function slabTax(income, slabs) {
  let tax = 0;
  for (const slab of slabs) {
    const lower = slab[0], upper = slab[1], rate = slab[2];
    if (income > lower) tax += (Math.min(income, upper) - lower) * rate;
  }
  return Math.max(0, tax);
}
function emiAmount(principal, annualRate, months) {
  if (principal <= 0 || months <= 0) return 0;
  const r = annualRate / 100 / 12;
  if (r === 0) return principal / months;
  return principal * r * Math.pow(1 + r, months) / (Math.pow(1 + r, months) - 1);
}
function amortizationRows(principal, annualRate, months) {
  const r = annualRate / 100 / 12;
  const emi = emiAmount(principal, annualRate, months);
  let balance = principal;
  const rows = [];
  for (let year = 1; year <= Math.ceil(months / 12); year++) {
    const opening = balance;
    let principalPaid = 0, interestPaid = 0;
    for (let m = 0; m < 12 && (year - 1) * 12 + m < months; m++) {
      const interest = balance * r;
      const principalPart = Math.min(emi - interest, balance);
      interestPaid += interest;
      principalPaid += principalPart;
      balance = Math.max(0, balance - principalPart);
    }
    rows.push({ year, opening, principalPaid, interestPaid, closing: balance });
  }
  return rows;
}
"""


def table(headers: list[str], rows: list[list[str]]) -> str:
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'<table class="reference-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def faq_html(items: list[tuple[str, str]]) -> str:
    blocks = []
    for question, answer in items:
        blocks.append(
            f'<div class="faq-item"><h3 class="faq-question">{question}</h3>'
            f'<div class="faq-answer"><p>{answer}</p></div></div>'
        )
    return "\n".join(blocks)


def ordered(items: list[str]) -> str:
    return '<ol class="how-to-steps">' + "".join(f"<li>{item}</li>" for item in items) + "</ol>"


def notes(items: list[str]) -> str:
    return '<ul class="summary-list">' + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def india_decision_section(page: dict) -> str:
    topic = page["h1"]
    return f"""<section class="content-section"><h2>Using this result in India</h2>
      <p>This {topic} is designed as a planning and audit tool, not as a substitute for the original Indian document that controls the transaction. For tax pages, that controlling document may be the Income-tax Act, Finance Act, Form 16, Form 26AS, AIS, challan, or employer declaration. For loan and investment pages, it may be the bank sanction letter, mutual fund scheme document, policy statement, EPFO passbook, NPS statement, or small-savings notification. For state-level pages, it may be a state transport, registration, electricity, or revenue department order. Use the calculator to understand scale, direction, and line-item logic before you rely on the official document.</p>
      <p>Indian financial decisions are sensitive to timing. A rate that is correct for FY 2024-25 may not be correct for FY 2025-26. A monthly salary figure may not include bonus, arrears, reimbursements, or employer contributions. A property or vehicle quote may include charges that are negotiable, optional, or state-specific. A bank rate may be floating and linked to an external benchmark. Re-run the calculator when any input changes, and compare at least three scenarios: conservative, expected, and high-cost or low-return.</p>
      <p>When the output is a large rupee amount, read it in both exact Indian notation and practical language. ₹10,00,000 is 10 lakhs, ₹1,00,00,000 is 1 crore, and small percentage changes can move the result by many lakhs on long tenures or high-value purchases. Keep screenshots or downloaded statements from the official portal, preserve invoices and receipts, and reconcile calculator output with the final bill, return, or statement before making a payment, filing a return, or signing a contract.</p>
      <p>If you share the result with a family member, accountant, lender, employer, dealer, or broker, share the inputs too. Most disagreements come from different assumptions, not from the arithmetic.</p>
    </section>"""


def header() -> str:
    return """<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="header-inner">
    <a class="logo" href="../index.html">⌗ Calculatorcity</a>
    <nav class="main-nav" aria-label="Main navigation">
      <a href="../index.html#math">Math</a>
      <a href="../index.html#finance">Finance</a>
      <a href="../index.html#unit">Unit</a>
      <a href="../index.html#health">Health</a>
      <a href="../index.html#datetime">Date &amp; Time</a>
      <a href="../index.html#science">Science</a>
      <a class="nav-india" href="../index.html#india">India</a>
    </nav>
    <div class="header-search">
      <label class="sr-only" for="header-search">Search calculators</label>
      <input id="header-search" class="search-input" type="search" data-search-input>
    </div>
    <button class="mobile-menu-btn" type="button" aria-label="Open menu" aria-expanded="false" data-mobile-menu-btn>☰</button>
  </div>
  <nav class="mobile-nav" aria-label="Mobile navigation" data-mobile-nav>
    <a href="../index.html#math">Math</a>
    <a href="../index.html#finance">Finance</a>
    <a href="../index.html#unit">Unit Converter</a>
    <a href="../index.html#health">Health &amp; Fitness</a>
    <a href="../index.html#datetime">Date &amp; Time</a>
    <a href="../index.html#science">Science &amp; Other</a>
    <a href="../index.html#india">🇮🇳 India</a>
  </nav>
</header>"""


def footer() -> str:
    return """<hr class="footer-separator" aria-hidden="true">
<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-main">
      <nav class="footer-categories" aria-labelledby="footer-categories-heading">
        <h3 id="footer-categories-heading" class="footer-links-label">CATEGORIES</h3>
        <div class="footer-category-pills">
        <a href="../index.html#math"><i class="ti ti-math" aria-hidden="true"></i><span>Math Calculators</span></a>
        <a href="../index.html#finance"><i class="ti ti-coin-rupee" aria-hidden="true"></i><span>Finance Calculators</span></a>
        <a href="../index.html#unit"><i class="ti ti-ruler" aria-hidden="true"></i><span>Unit Converters</span></a>
        <a href="../index.html#health"><i class="ti ti-heartbeat" aria-hidden="true"></i><span>Health &amp; Fitness</span></a>
        <a href="../index.html#datetime"><i class="ti ti-calendar" aria-hidden="true"></i><span>Date &amp; Time</span></a>
        <a href="../index.html#science"><i class="ti ti-flask" aria-hidden="true"></i><span>Science &amp; Other</span></a>
        <a href="../index.html#india"><i class="ti ti-map-pin" aria-hidden="true"></i><span>India Calculators</span></a>
        </div>
      </nav>
      <nav class="footer-popular" aria-labelledby="footer-popular-heading">
        <h3 id="footer-popular-heading" class="footer-links-label">POPULAR CALCULATORS</h3>
        <div class="footer-popular-links">
        <a href="../maths/percentage-calculator.html">Percentage</a>
        <a href="../india/gst-calculator.html">GST</a>
        <a href="../india/income-tax-calculator.html">Income Tax</a>
        <a href="../india/home-loan-emi-calculator.html">Home Loan EMI</a>
        <a href="../india/sip-calculator.html">SIP</a>
        <a href="../india/fd-calculator.html">FD</a>
        <a href="../health-fitness/bmi-calculator.html">BMI</a>
        <a href="../date-time/age-calculator.html">Age</a>
        <a href="../finance/currency-converter.html">Currency</a>
        <a href="../india/gold-price-calculator.html">Gold Price</a>
        <a href="../finance/loan-emi-calculator.html">Loan EMI</a>
        <a href="../finance/compound-interest-calculator.html">Compound Interest</a>
        <a href="../india/ctc-salary-calculator.html">CTC Salary</a>
        <a href="../india/pf-epf-calculator.html">EPF / PF</a>
        <a href="../india/ppf-calculator.html">PPF</a>
        <a href="../india/hra-exemption-calculator.html">HRA Exemption</a>
        <a href="../india/tds-calculator.html">TDS</a>
        <a href="../finance/discount-calculator.html">Discount</a>
        <a href="../india/cgpa-to-percentage-calculator.html">CGPA to %</a>
        <a href="../india/stamp-duty/index.html">Stamp Duty</a>
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
        <a href="../company/about-us.html">About Us</a>
        <a href="../company/blogs.html">Blog</a>
        <a href="../company/contact-us.html">Contact Us</a>
        <a href="../company/help.html">Help</a>
        <a href="../company/privacy-policy.html">Privacy Policy</a>
        <a href="../company/terms-and-conditions.html">Terms &amp; Conditions</a>
        </nav>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Calculatorcity. All calculations run locally in your browser.</span>
      <span class="footer-disclaimer">For education and planning only. Results are estimates — not financial, tax, legal, or medical advice. Verify with a qualified expert.</span>
    </div>
  </div>
</footer>"""


RELATED = [
    ("GST Calculator", "gst-calculator.html"),
    ("Income Tax", "income-tax-calculator.html"),
    ("Home Loan EMI", "home-loan-emi-calculator.html"),
    ("SIP Calculator", "sip-calculator.html"),
    ("FD Calculator", "fd-calculator.html"),
    ("CTC Salary", "ctc-salary-calculator.html"),
    ("EPF / PF", "pf-epf-calculator.html"),
    ("HRA Exemption", "hra-exemption-calculator.html"),
    ("PPF Calculator", "ppf-calculator.html"),
    ("TDS Calculator", "tds-calculator.html"),
]


def sidebar(current_file: str) -> str:
    links = [item for item in RELATED if item[1] != current_file][:7]
    items = "".join(f'<li><a href="../india/{href}">{name}</a></li>' for name, href in links)
    return f"""<aside class="calc-sidebar">
  <div class="card sidebar-card"><h3>Related Indian calculators</h3><ul>{items}</ul></div>
</aside>"""


def scripts(page: dict) -> str:
    chart = '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>\n' if page.get("chart", True) else ""
    return f"""{chart}<script src="../assets/js/main.js"></script>
<script>
{COMMON_JS}
{page["script"]}
</script>"""


def schemas(page: dict) -> str:
    webapp = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": page["h1"],
        "url": f"{DOMAIN}/india/{page['file']}",
        "description": page["meta"],
        "applicationCategory": "CalculatorApplication",
        "operatingSystem": "Any",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "INR"},
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{DOMAIN}/"},
            {"@type": "ListItem", "position": 2, "name": "India Calculators", "item": f"{DOMAIN}/#india"},
            {"@type": "ListItem", "position": 3, "name": page["h1"], "item": f"{DOMAIN}/india/{page['file']}"},
        ],
    }
    return (
        '<script type="application/ld+json">'
        + json.dumps(webapp, ensure_ascii=False)
        + '</script>\n  <script type="application/ld+json">'
        + json.dumps(breadcrumb, ensure_ascii=False)
        + "</script>"
    )


def render_page(page: dict) -> str:
    extra_sections = "\n".join(
        f'<section class="content-section"><h2>{title}</h2>{body}</section>'
        for title, body in page.get("sections", [])
    )
    badge_extra = ' <span class="badge badge-india">🏛️ Andhra Pradesh</span>' if page["file"] == "ap-electricity-bill-calculator.html" else ""
    reference = table(page["reference_headers"], page["reference_rows"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{page["title"]}</title>
  <meta name="description" content="{page["meta"]}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="canonical" href="{DOMAIN}/india/{page['file']}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/base.css">
  <link rel="stylesheet" href="../assets/css/layout.css">
  <link rel="stylesheet" href="../assets/css/components.css">
  <link rel="stylesheet" href="../assets/css/calculator.css">
  {schemas(page)}
</head>
<body class="india-page">
{header()}
<main id="main" class="page-container two-col-layout">
  <article class="calc-main">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="../index.html">Home</a><span><a href="../index.html#india">India Calculators</a></span><span>{page["h1"]}</span></nav>
    <p><span class="badge badge-india">🇮🇳 India</span>{badge_extra}</p>
    <h1>{page["h1"]}</h1>
    <p>{page["intro"]}</p>
    {page["widget"]}
    <section class="content-section"><h2>How to use</h2>{ordered(page["how_to"])}</section>
    <section class="content-section"><h2>Formula</h2><div class="formula-box">{page["formula_box"]}</div>{page["formula_text"]}</section>
    <section class="content-section"><h2>Worked example</h2><div class="example-box">{page["example"]}</div></section>
    <section class="content-section"><h2>{page["reference_title"]}</h2>{reference}</section>
    {extra_sections}
    {india_decision_section(page)}
    <section class="content-section"><h2>FAQ</h2>{faq_html(page["faqs"])}</section>
    <section class="content-section"><h2>Important notes for India</h2>{notes(page["notes"])}</section>
  </article>
  {sidebar(page["file"])}
</main>
{footer()}
{scripts(page)}
</body>
</html>
"""


PAGES: list[dict] = []


PAGES.append({
    "file": "gst-calculator.html",
    "title": "GST Calculator — Add or Remove GST Online Free | Calculatorcity",
    "meta": "Free GST calculator for India. Add or remove GST at 5%, 12%, 18% or 28% slab. Get CGST, SGST breakdown instantly. No signup needed.",
    "h1": "GST Calculator",
    "intro": "The GST calculator helps Indian businesses, freelancers, and shoppers calculate Goods and Services Tax on invoices, quotations, and retail prices. Enter an amount in rupees, choose a GST slab, and add or remove tax instantly. The result splits CGST and SGST for intra-state transactions, shows the taxable base, and keeps every rupee value in the Indian numbering system used on bills and accounting records.",
    "widget": """<section class="calc-widget">
      <div class="field-grid">
        <div class="calc-input-group"><label for="gst-amount">Amount (₹)</label><div class="input-prefix"><span>₹</span><input id="gst-amount" type="number" inputmode="decimal" value="50000"></div></div>
        <div class="calc-input-group"><label for="gst-rate">GST slab</label><select id="gst-rate"><option value="0">0%</option><option value="5">5%</option><option value="12">12%</option><option value="18" selected>18%</option><option value="28">28%</option></select></div>
      </div>
      <div class="toggle-buttons" role="group" aria-label="GST mode"><button class="toggle-btn active" type="button" data-mode="add">Add GST</button><button class="toggle-btn" type="button" data-mode="remove">Remove GST</button></div>
      <button class="calc-btn" id="calculate" type="button">Calculate GST</button>
      <div class="calc-result show"><div class="result-grid"><div class="result-card"><span class="result-value" id="base-amount">₹0.00</span><span class="result-label">Taxable base</span></div><div class="result-card"><span class="result-value" id="gst-amount-out">₹0.00</span><span class="result-label">Total GST</span></div><div class="result-card"><span class="result-value" id="cgst">₹0.00</span><span class="result-label">CGST</span></div><div class="result-card"><span class="result-value" id="sgst">₹0.00</span><span class="result-label">SGST</span></div><div class="result-card highlight"><span class="result-value" id="total-amount">₹0.00</span><span class="result-label">Invoice total</span></div></div><div class="chart-container"><canvas id="calc-chart"></canvas></div></div>
    </section>""",
    "how_to": [
        "Enter the amount in rupees exactly as it appears on your invoice, quotation, or price tag.",
        "Choose the GST slab that applies to the goods or services: 0%, 5%, 12%, 18%, or 28%.",
        "Select Add GST when your entered amount is before tax, or Remove GST when your amount already includes GST.",
        "Click Calculate GST to see taxable value, total GST, CGST, SGST, and invoice total.",
        "Use the chart to check the proportion of base price and tax before preparing the final bill.",
    ],
    "formula_box": "Add GST: GST = Amount × Rate / 100<br>Remove GST: Base = Inclusive Amount / (1 + Rate / 100)<br>CGST = SGST = Total GST / 2",
    "formula_text": "<p>GST is a percentage of the taxable value. When the listed price is exclusive of tax, the tax amount is calculated by multiplying the base value by the slab rate and dividing by 100. The invoice value is then the base plus GST. When the listed price is inclusive of tax, the tax must be extracted by dividing the total by one plus the slab rate as a decimal. This avoids the common mistake of subtracting 18% directly from an inclusive price.</p><p>For most intra-state supplies, GST is split equally into CGST and SGST. For inter-state supplies, the same total rate generally appears as IGST instead. The calculator focuses on the arithmetic and invoice split; product classification, place of supply, exemptions, reverse charge, and input tax credit eligibility must be confirmed against GST law and your tax advisor.</p>",
    "example": "<p>A consultant quotes ₹50,000 before GST for a service taxable at 18%.</p><p>GST = ₹50,000 × 18 / 100 = ₹9,000. CGST is ₹4,500 and SGST is ₹4,500.</p><p><strong>Invoice total = ₹59,000.</strong></p>",
    "reference_title": "GST slab reference",
    "reference_headers": ["Goods or service", "Typical GST rate"],
    "reference_rows": [["Fresh milk and unpacked food grains", "0%"], ["Books and newspapers", "0%"], ["Domestic transport", "5%"], ["Essential medicines", "5% or 12%"], ["Packaged food items", "5% or 12%"], ["Hotel rooms", "12% or 18%"], ["Software and IT services", "18%"], ["Insurance services", "18%"], ["Mobile phones", "18%"], ["Air conditioners", "28%"], ["Automobiles", "28% plus cess where applicable"], ["Tobacco products", "28% plus compensation cess"]],
    "sections": [("GST calculation tips for Indian invoices", "<p>Indian invoices normally show taxable value, CGST, SGST, or IGST separately. If a vendor gives only the final amount, use the Remove GST mode to find the taxable value before recording purchase cost or reconciling input tax credit. If you are quoting a customer, use Add GST mode so the buyer can see the base service fee and the tax separately.</p><p>Small differences of a few paise can appear because accounting software rounds each line item while a quick calculator rounds the final total. For high-value invoices, calculate GST line by line in your billing system and use this page as an independent reasonableness check.</p>")],
    "faqs": [("What is GST in India?", "GST is Goods and Services Tax, an indirect tax on the supply of many goods and services in India. Registered businesses collect it from buyers and deposit it with the government after adjusting eligible input tax credit."), ("What are the common GST slabs?", "The common GST slabs are 0%, 5%, 12%, 18%, and 28%. Some goods also carry compensation cess or special rates, so the exact rate depends on classification."), ("What is CGST and SGST?", "CGST is Central GST and SGST is State GST. In most intra-state sales the GST amount is split equally between them. Inter-state sales generally use IGST instead."), ("Can I remove GST from an inclusive price?", "Yes. Divide the inclusive price by one plus the GST rate as a decimal to get the taxable base. The difference between total and base is GST."), ("Does this calculator handle input tax credit?", "No. It calculates invoice tax. Input tax credit depends on GST registration, invoice validity, return filing, supplier compliance, and blocked-credit rules.")],
    "notes": ["GST rates can change through GST Council notifications, so verify unusual goods or services before issuing a tax invoice.", "CGST and SGST split applies to intra-state supplies; IGST usually applies when supplier and place of supply are in different states.", "Composition dealers, exempt suppliers, reverse-charge transactions, and e-commerce collections can have special treatment.", "For accounting, preserve the supplier GSTIN, invoice number, place of supply, and HSN/SAC details along with the calculated tax."],
    "script": """let gstMode = 'add';
document.querySelectorAll('[data-mode]').forEach((btn) => btn.addEventListener('click', () => {
  gstMode = btn.dataset.mode;
  document.querySelectorAll('[data-mode]').forEach((item) => item.classList.toggle('active', item === btn));
  calculate();
}));
function calculate() {
  const amount = value('gst-amount');
  const rate = value('gst-rate');
  let base = amount, gst = amount * rate / 100, total = amount + gst;
  if (gstMode === 'remove') {
    total = amount;
    base = rate === 0 ? amount : amount / (1 + rate / 100);
    gst = total - base;
  }
  text('base-amount', formatIndianNumber(base));
  text('gst-amount-out', formatIndianNumber(gst));
  text('cgst', formatIndianNumber(gst / 2));
  text('sgst', formatIndianNumber(gst / 2));
  text('total-amount', formatIndianNumber(total));
  drawChart('calc-chart', 'pie', ['Taxable base', 'GST'], [{ data: [base, gst], backgroundColor: ['#2563eb', '#f97316'] }]);
}
bindCalculator(calculate);""",
})


PAGES.append({
    "file": "income-tax-calculator.html",
    "title": "Income Tax Calculator India 2024-25 — New vs Old Regime | Calculatorcity",
    "meta": "Free income tax calculator for India FY 2024-25. Compare new regime vs old regime. Calculate exact tax liability with all deductions. Supports all income slabs.",
    "h1": "Income Tax Calculator India (FY 2024-25)",
    "intro": "This income tax calculator for India estimates FY 2024-25 tax under the new and old regimes for salaried taxpayers. Enter salary, HRA details, deductions, home loan interest, professional tax, and other eligible reductions to compare taxable income side by side. It applies Indian slab logic, 4% health and education cess, rebate rules, and monthly TDS estimates in rupees using Indian number formatting.",
    "widget": """<section class="calc-widget">
      <div class="section-label">Step 1: Income inputs</div>
      <div class="field-grid">
        <div class="calc-input-group"><label for="gross-income">Gross salary / total income (₹)</label><div class="input-prefix"><span>₹</span><input id="gross-income" type="number" value="1200000"></div></div>
        <div class="calc-input-group"><label for="hra-received">HRA received annually (₹)</label><div class="input-prefix"><span>₹</span><input id="hra-received" type="number" value="240000"></div></div>
        <div class="calc-input-group"><label for="basic-da">Basic salary + DA annually (₹)</label><div class="input-prefix"><span>₹</span><input id="basic-da" type="number" value="600000"></div></div>
        <div class="calc-input-group"><label for="rent-paid">Rent paid annually (₹)</label><div class="input-prefix"><span>₹</span><input id="rent-paid" type="number" value="300000"></div></div>
        <div class="calc-input-group"><label for="city-type">HRA city type</label><select id="city-type"><option value="metro">Metro</option><option value="non-metro" selected>Non-metro</option></select></div>
        <div class="calc-input-group"><label for="standard-deduction">Old regime standard deduction (₹)</label><div class="input-prefix"><span>₹</span><input id="standard-deduction" type="number" value="50000"></div><span class="hint">New regime uses ₹75,000 for FY 2024-25 salary income.</span></div>
        <div class="calc-input-group"><label for="professional-tax">Professional tax (₹)</label><div class="input-prefix"><span>₹</span><input id="professional-tax" type="number" value="2400"></div></div>
        <div class="calc-input-group"><label for="deduction-80c">Section 80C investments (₹)</label><div class="input-prefix"><span>₹</span><input id="deduction-80c" type="number" value="150000"></div><span class="hint">Capped at ₹1,50,000 in old regime.</span></div>
        <div class="calc-input-group"><label for="deduction-80d">Section 80D health insurance (₹)</label><div class="input-prefix"><span>₹</span><input id="deduction-80d" type="number" value="25000"></div></div>
        <div class="calc-input-group"><label for="home-loan-interest">Home loan interest Section 24(b) (₹)</label><div class="input-prefix"><span>₹</span><input id="home-loan-interest" type="number" value="180000"></div><span class="hint">Self-occupied cap generally ₹2,00,000 in old regime.</span></div>
        <div class="calc-input-group"><label for="other-deductions">Other old-regime deductions (₹)</label><div class="input-prefix"><span>₹</span><input id="other-deductions" type="number" value="50000"></div></div>
      </div>
      <div class="section-label">Step 2: Regime selection</div>
      <div class="toggle-buttons" style="grid-template-columns:repeat(3,1fr)" role="group" aria-label="Tax regime"><button class="toggle-btn regime-btn active" type="button" data-regime="compare">Compare Both</button><button class="toggle-btn regime-btn" type="button" data-regime="new">New Regime</button><button class="toggle-btn regime-btn" type="button" data-regime="old">Old Regime</button></div>
      <button class="calc-btn" id="calculate" type="button">Calculate income tax</button>
      <div class="calc-result show"><div class="result-grid"><div class="result-card" id="new-card"><span class="result-value" id="new-tax">₹0.00</span><span class="result-label">New regime net tax</span><span id="new-badge"></span></div><div class="result-card" id="old-card"><span class="result-value" id="old-tax">₹0.00</span><span class="result-label">Old regime net tax</span><span id="old-badge"></span></div><div class="result-card"><span class="result-value" id="new-taxable">₹0.00</span><span class="result-label">New taxable income</span></div><div class="result-card"><span class="result-value" id="old-taxable">₹0.00</span><span class="result-label">Old taxable income</span></div><div class="result-card"><span class="result-value" id="cess-out">₹0.00</span><span class="result-label">Cess included at 4%</span></div><div class="result-card"><span class="result-value" id="monthly-tds">₹0.00</span><span class="result-label">Lower monthly TDS</span></div></div><div class="mini-note" id="tax-note"></div><div class="chart-container"><canvas id="calc-chart"></canvas></div></div>
    </section>""",
    "how_to": ["Enter annual gross salary or total taxable income before deductions.", "Fill HRA, rent, basic salary, and city details if you want automatic HRA exemption under the old regime.", "Add old-regime deductions such as 80C, 80D, professional tax, and home loan interest.", "Choose New Regime, Old Regime, or Compare Both to focus the output.", "Review taxable income, cess, net tax, monthly TDS, and the green badge showing the lower-tax regime."],
    "formula_box": "Tax = slab-wise income tax − eligible rebate<br>Net tax payable = Tax + 4% health and education cess<br>Monthly TDS = Net tax payable / 12",
    "formula_text": "<p>Income tax is calculated slab by slab. Each slab taxes only the portion of income that falls inside that band, not the entire income at the highest rate. For FY 2024-25, the new regime for most individual salaried taxpayers has lower slab rates and a salary standard deduction of ₹75,000, but it does not allow common deductions such as HRA exemption, 80C, 80D, or self-occupied home loan interest. The old regime keeps those deductions but uses higher slab rates after ₹5,00,000.</p><p>This calculator first computes taxable income separately for each regime. It then applies rebate logic, adds health and education cess at 4%, and divides the final yearly tax by 12 for a monthly TDS planning number. It does not calculate surcharge for very high incomes, marginal relief beyond standard rebate handling, capital gains special rates, or business-income restrictions on switching regimes.</p>",
    "example": "<p>Assume gross salary of ₹12,00,000, 80C investments of ₹1,50,000, 80D premium of ₹25,000, rent of ₹3,00,000, and basic salary of ₹6,00,000.</p><p>The old regime may reduce taxable income through HRA and deductions, while the new regime mainly uses the ₹75,000 standard deduction.</p><p><strong>The calculator compares both and shows the lower annual tax and monthly TDS.</strong></p>",
    "reference_title": "Section 80C investments and limits",
    "reference_headers": ["Investment or payment", "Typical 80C treatment"],
    "reference_rows": [["Employee Provident Fund", "Included within ₹1,50,000 limit"], ["Public Provident Fund", "Included within ₹1,50,000 limit"], ["ELSS mutual funds", "Included; 3-year lock-in"], ["Life insurance premium", "Included subject to policy rules"], ["Principal repayment on home loan", "Included for eligible house property"], ["Sukanya Samriddhi Yojana", "Included within ₹1,50,000 limit"], ["National Savings Certificate", "Included within ₹1,50,000 limit"], ["5-year tax saver FD", "Included; interest taxable"], ["Tuition fees for children", "Included for eligible full-time education"], ["Senior Citizens Savings Scheme", "Included within ₹1,50,000 limit"]],
    "sections": [("New regime vs old regime", "<p>The new regime is the default regime for many individual taxpayers, but salaried taxpayers without business income can generally choose the old regime while filing the return. The better choice depends on deduction depth. A taxpayer with high HRA exemption, full 80C, health insurance, home loan interest, and professional tax may still prefer the old regime. A taxpayer with fewer deductions often pays less in the new regime because slabs are lower and the rebate limit is higher.</p><p>Use this page as a planning estimate before declaring investments to your employer. Your Form 16, AIS, capital gains, bank interest, and other income can change the final return calculation.</p>")],
    "faqs": [("What is the new tax regime?", "The new regime is the default personal tax system with lower slab rates and fewer deductions. For FY 2024-25 it allows salary standard deduction but generally excludes HRA, 80C, 80D, and self-occupied home loan interest deductions."), ("Which regime is better for me?", "The old regime is usually better when eligible deductions and exemptions are large. The new regime is often better when you do not claim much beyond standard deduction. The calculator compares both."), ("What is standard deduction?", "Standard deduction is a flat reduction from salary income. For FY 2024-25, the calculator uses ₹75,000 for the new regime and lets you edit the old-regime standard deduction field."), ("What is Section 80C?", "Section 80C covers common investments and payments such as EPF, PPF, ELSS, life insurance premium, home loan principal, and tuition fees up to ₹1,50,000 in the old regime."), ("How is cess calculated?", "Health and education cess is 4% of income tax after rebate and before final payable tax. If income tax after rebate is zero, cess is also zero.")],
    "notes": ["FY 2024-25 corresponds to Assessment Year 2025-26; tax filing forms and employer TDS declarations should use the correct AY.", "The calculator uses the FY 2024-25 new-regime slabs notified after the 2024 Budget, including the ₹3,00,001 to ₹7,00,000 slab at 5%.", "Surcharge, marginal relief for high income, special capital gains rates, agricultural income aggregation, and business-income regime restrictions need separate review.", "HRA exemption is available only when rent is actually paid and conditions under Section 10(13A) are met."],
    "script": """let selectedRegime = 'compare';
const newSlabs = [[0,300000,0],[300000,700000,0.05],[700000,1000000,0.10],[1000000,1200000,0.15],[1200000,1500000,0.20],[1500000,Infinity,0.30]];
const oldSlabs = [[0,250000,0],[250000,500000,0.05],[500000,1000000,0.20],[1000000,Infinity,0.30]];
document.querySelectorAll('.regime-btn').forEach((btn) => btn.addEventListener('click', () => {
  selectedRegime = btn.dataset.regime;
  document.querySelectorAll('.regime-btn').forEach((item) => item.classList.toggle('active', item === btn));
  calculate();
}));
function taxWithRebate(taxable, slabs, regime) {
  let tax = slabTax(taxable, slabs);
  if (regime === 'new' && taxable <= 700000) tax = 0;
  if (regime === 'old' && taxable <= 500000) tax = 0;
  return tax;
}
function calculateHra() {
  const hra = value('hra-received');
  const basic = value('basic-da');
  const rent = value('rent-paid');
  if (hra <= 0 || basic <= 0 || rent <= 0) return 0;
  const cityFactor = document.getElementById('city-type').value === 'metro' ? 0.5 : 0.4;
  return Math.max(0, Math.min(hra, basic * cityFactor, rent - basic * 0.10));
}
function calculate() {
  const gross = value('gross-income');
  const hraExemption = calculateHra();
  const oldDeductions = Math.min(value('standard-deduction'), 50000) + value('professional-tax') + Math.min(value('deduction-80c'), 150000) + value('deduction-80d') + Math.min(value('home-loan-interest'), 200000) + value('other-deductions') + hraExemption;
  const oldTaxable = Math.max(0, gross - oldDeductions);
  const newTaxable = Math.max(0, gross - 75000);
  const oldBaseTax = taxWithRebate(oldTaxable, oldSlabs, 'old');
  const newBaseTax = taxWithRebate(newTaxable, newSlabs, 'new');
  const oldTotal = oldBaseTax * 1.04;
  const newTotal = newBaseTax * 1.04;
  const better = newTotal <= oldTotal ? 'new' : 'old';
  text('new-tax', formatIndianNumber(newTotal));
  text('old-tax', formatIndianNumber(oldTotal));
  text('new-taxable', formatIndianNumber(newTaxable));
  text('old-taxable', formatIndianNumber(oldTaxable));
  text('cess-out', `${formatIndianNumber((better === 'new' ? newBaseTax : oldBaseTax) * 0.04)} on lower-tax option`);
  text('monthly-tds', formatIndianNumber(Math.min(newTotal, oldTotal) / 12));
  html('new-badge', better === 'new' ? '<span class="better-badge">Better for you</span>' : '');
  html('old-badge', better === 'old' ? '<span class="better-badge">Better for you</span>' : '');
  document.getElementById('new-card').classList.toggle('highlight', better === 'new');
  document.getElementById('old-card').classList.toggle('highlight', better === 'old');
  text('tax-note', `Estimated HRA exemption used in old regime: ${formatIndianNumber(hraExemption)}. Lower-tax option shown for ${selectedRegime === 'compare' ? 'comparison' : selectedRegime + ' regime view'}.`);
  drawChart('calc-chart', 'bar', ['New regime', 'Old regime'], [{ label: 'Net tax payable', data: [newTotal, oldTotal], backgroundColor: ['#f97316', '#2563eb'] }], { indexAxis: 'y' });
}
bindCalculator(calculate);""",
})


PAGES.append({
    "file": "home-loan-emi-calculator.html",
    "title": "Home Loan EMI Calculator — Monthly EMI & Total Interest | Calculatorcity",
    "meta": "Free home loan EMI calculator India. Calculate monthly EMI, total interest, and amortization schedule. Supports all loan amounts and tenures.",
    "h1": "Home Loan EMI Calculator",
    "intro": "The home loan EMI calculator estimates monthly instalments for Indian housing loans, including total interest, total repayment, processing fee, and year-wise balance reduction. Use it for apartment purchases, resale property, plot-plus-construction loans, or balance-transfer comparisons. The calculator supports rupee loan amounts from lakhs to crores, flexible tenures in years or months, and an amortization schedule that shows how principal repayment accelerates over time.",
    "widget": """<section class="calc-widget">
      <div class="field-grid">
        <div class="calc-input-group"><label for="loan-range">Loan amount slider (₹)</label><div class="dual-control"><input id="loan-range" type="range" min="100000" max="50000000" step="100000" value="5000000"><div class="input-prefix"><span>₹</span><input id="loan-amount" type="number" value="5000000"></div></div></div>
        <div class="calc-input-group"><label for="rate-range">Interest rate (%)</label><div class="dual-control"><input id="rate-range" type="range" min="6" max="20" step="0.05" value="8.5"><input id="interest-rate" type="number" step="0.05" value="8.5"></div></div>
        <div class="calc-input-group"><label for="tenure-range">Loan tenure</label><div class="dual-control"><input id="tenure-range" type="range" min="1" max="30" step="1" value="20"><input id="tenure" type="number" value="20"></div></div>
        <div class="calc-input-group"><label for="tenure-unit">Tenure unit</label><select id="tenure-unit"><option value="years" selected>Years</option><option value="months">Months</option></select></div>
        <div class="calc-input-group"><label for="processing-fee">Processing fee (%)</label><input id="processing-fee" type="number" step="0.05" value="0.5"></div>
      </div>
      <button class="calc-btn" id="calculate" type="button">Calculate EMI</button>
      <div class="calc-result show"><div class="result-grid"><div class="result-card highlight"><span class="result-value" id="emi">₹0.00</span><span class="result-label">Monthly EMI</span></div><div class="result-card"><span class="result-value" id="total-interest">₹0.00</span><span class="result-label">Total interest payable</span></div><div class="result-card"><span class="result-value" id="total-payment">₹0.00</span><span class="result-label">Total amount payable</span></div><div class="result-card"><span class="result-value" id="fee-out">₹0.00</span><span class="result-label">Processing fee</span></div><div class="result-card"><span class="result-value" id="effective-rate">0%</span><span class="result-label">Approx. effective annual cost</span></div></div><div class="field-grid"><div class="chart-container"><canvas id="emi-pie"></canvas></div><div class="chart-container"><canvas id="balance-line"></canvas></div></div><div id="amortization" class="amortization-table"></div><button class="btn btn-secondary" type="button" id="toggle-amortization">Show all years</button></div>
    </section>""",
    "how_to": ["Enter the home loan amount you expect the bank or housing finance company to disburse.", "Set the annual floating or fixed interest rate quoted by the lender.", "Choose tenure in years or months and include processing fee if you want a fuller cost estimate.", "Click Calculate EMI to view EMI, total interest, total repayment, fee, and effective cost.", "Read the amortization table to see opening balance, principal paid, interest paid, and closing balance year by year."],
    "formula_box": "EMI = P × r × (1 + r)<sup>n</sup> / ((1 + r)<sup>n</sup> − 1)<br>P = principal, r = monthly interest rate, n = months",
    "formula_text": "<p>Home loan EMI is based on the standard amortizing loan formula. The annual interest rate is divided by 12 and by 100 to get the monthly decimal rate. The tenure is converted into months. The formula produces one fixed instalment that covers that month’s interest and repays part of the principal. In early years, the outstanding principal is high, so a larger share of each EMI goes toward interest. Later, more of the same EMI reduces principal.</p><p>If the interest rate is zero, the EMI is simply principal divided by months. Real Indian home loans can change because floating rates reset, lenders alter the remaining tenure, borrowers prepay principal, or fees are charged separately. This calculator treats the rate and EMI as constant so that the base repayment structure is easy to audit before comparing bank offers.</p>",
    "example": "<p>For a ₹50,00,000 home loan at 8.5% for 20 years, the monthly rate is 8.5 / 12 / 100 and tenure is 240 months.</p><p>The EMI is about ₹43,391. Total payment is about ₹1,04,13,840 and total interest is about ₹54,13,840.</p><p><strong>A 0.5% processing fee adds about ₹25,000 upfront.</strong></p>",
    "reference_title": "EMI for ₹50L home loan at common rates",
    "reference_headers": ["Rate", "10 years", "15 years", "20 years", "25 years"],
    "reference_rows": [["7.5%", "₹59,351", "₹46,351", "₹40,280", "₹36,950"], ["8.0%", "₹60,663", "₹47,782", "₹41,822", "₹38,591"], ["8.5%", "₹61,993", "₹49,237", "₹43,391", "₹40,261"], ["9.0%", "₹63,338", "₹50,713", "₹44,986", "₹41,960"], ["9.5%", "₹64,700", "₹52,211", "₹46,607", "₹43,687"], ["10.0%", "₹66,075", "₹53,730", "₹48,251", "₹45,435"], ["10.5%", "₹67,464", "₹55,269", "₹49,919", "₹47,207"], ["11.0%", "₹68,856", "₹56,824", "₹51,610", "₹48,991"]],
    "sections": [("Home loan prepayment context", "<p>Prepayment can reduce total interest sharply because it cuts outstanding principal early. Indian lenders may offer part-prepayment without penalty on floating-rate individual home loans, but fixed-rate loans, non-individual borrowers, or special products can have conditions. If you expect bonuses, RSU vesting, or rental income, compare a shorter tenure with a longer tenure plus planned prepayments.</p><p>Also compare the processing fee, legal fee, valuation charge, insurance bundling, reset frequency, spread over repo or benchmark rate, and foreclosure rules. A slightly lower EMI is not always better if total interest and fees are much higher.</p>")],
    "faqs": [("How is home loan EMI calculated?", "EMI is calculated using principal, monthly interest rate, and number of monthly instalments. The formula keeps the EMI fixed while the interest and principal split changes each month."), ("What is prepayment?", "Prepayment is an extra amount paid toward the outstanding loan principal. It usually reduces total interest and can reduce either tenure or EMI depending on the lender’s option."), ("What is the maximum home loan tenure?", "Many Indian lenders offer home loan tenures up to 30 years, subject to age, retirement, income, property type, and credit policy."), ("How does interest rate affect EMI?", "A higher rate increases EMI and total interest. Long tenures magnify the impact because interest is charged over more months."), ("What documents are needed for a home loan?", "Common documents include identity proof, address proof, PAN, income proof, bank statements, property papers, sale agreement, and title documents.")],
    "notes": ["Floating-rate home loan EMIs can change when the external benchmark or lender spread changes.", "Section 24(b) interest deduction and principal repayment deduction under 80C are old-regime tax concepts and have eligibility conditions.", "Stamp duty, registration, legal charges, interiors, maintenance deposits, and GST on under-construction property are not part of bank EMI.", "For RERA projects, verify project registration, title, approvals, and possession timelines before committing funds."],
    "script": """let showAllAmortization = false;
syncRange('loan-range', 'loan-amount', calculate);
syncRange('rate-range', 'interest-rate', calculate);
syncRange('tenure-range', 'tenure', calculate);
document.getElementById('toggle-amortization').addEventListener('click', () => { showAllAmortization = !showAllAmortization; calculate(); });
function calculate() {
  const principal = value('loan-amount');
  const annualRate = value('interest-rate');
  const unit = document.getElementById('tenure-unit').value;
  let months = Math.max(1, value('tenure'));
  if (unit === 'years') months *= 12;
  const emi = emiAmount(principal, annualRate, months);
  const total = emi * months;
  const interest = Math.max(0, total - principal);
  const fee = principal * value('processing-fee') / 100;
  text('emi', formatIndianNumber(emi));
  text('total-interest', formatIndianNumber(interest));
  text('total-payment', formatIndianNumber(total));
  text('fee-out', formatIndianNumber(fee));
  text('effective-rate', `${formatPlainNumber(annualRate + (fee / principal / Math.max(1, months / 12)) * 100, 2)}%`);
  drawChart('emi-pie', 'pie', ['Principal', 'Total interest'], [{ data: [principal, interest], backgroundColor: ['#2563eb', '#f97316'] }]);
  const rows = amortizationRows(principal, annualRate, months);
  drawChart('balance-line', 'line', rows.map((r) => `Year ${r.year}`), [{ label: 'Outstanding balance', data: rows.map((r) => r.closing), borderColor: '#f97316', backgroundColor: '#fff7ed', fill: true, tension: 0.25 }]);
  const visible = showAllAmortization ? rows : rows.filter((r, i) => i === 0 || i === rows.length - 1);
  html('amortization', '<table class="reference-table"><thead><tr><th>Year</th><th>Opening Balance</th><th>Principal Paid</th><th>Interest Paid</th><th>Closing Balance</th></tr></thead><tbody>' + visible.map((r) => `<tr><td>Year ${r.year}</td><td>${formatIndianNumber(r.opening)}</td><td>${formatIndianNumber(r.principalPaid)}</td><td>${formatIndianNumber(r.interestPaid)}</td><td>${formatIndianNumber(r.closing)}</td></tr>`).join('') + '</tbody></table>');
  text('toggle-amortization', showAllAmortization ? 'Show first and last year' : 'Show all years');
}
bindCalculator(calculate);""",
})


PAGES.append({
    "file": "sip-calculator.html",
    "title": "SIP Calculator — Mutual Fund Returns Calculator | Calculatorcity",
    "meta": "Free SIP calculator to estimate mutual fund returns. Calculate wealth growth for monthly SIP investments. Shows invested amount vs estimated returns over time.",
    "h1": "SIP Calculator (Systematic Investment Plan)",
    "intro": "The SIP calculator estimates the future value of monthly mutual fund investments in India. Enter your monthly SIP, expected annual return, and investment period to see invested amount, estimated gain, maturity value, and absolute return. The stacked chart separates your contributions from market returns year by year, making it easier to understand compounding, long-term discipline, and the journey from lakhs to crores.",
    "widget": """<section class="calc-widget">
      <div class="field-grid">
        <div class="calc-input-group"><label for="sip-range">Monthly SIP amount (₹)</label><div class="dual-control"><input id="sip-range" type="range" min="500" max="500000" step="500" value="10000"><div class="input-prefix"><span>₹</span><input id="sip-amount" type="number" value="10000"></div></div></div>
        <div class="calc-input-group"><label for="return-range">Expected annual return (%)</label><div class="dual-control"><input id="return-range" type="range" min="8" max="20" step="0.1" value="12"><input id="return-rate" type="number" step="0.1" value="12"></div></div>
        <div class="calc-input-group"><label for="years-range">Investment period (years)</label><div class="dual-control"><input id="years-range" type="range" min="1" max="40" step="1" value="15"><input id="years" type="number" value="15"></div></div>
        <div class="calc-input-group"><label for="breakdown">Breakdown</label><select id="breakdown"><option value="year" selected>Year-wise</option><option value="month">Month-wise summary</option></select></div>
      </div>
      <button class="calc-btn" id="calculate" type="button">Calculate SIP returns</button>
      <div class="calc-result show"><div class="result-grid"><div class="result-card"><span class="result-value" id="invested">₹0.00</span><span class="result-label">Invested amount</span></div><div class="result-card"><span class="result-value" id="gain">₹0.00</span><span class="result-label">Estimated returns</span></div><div class="result-card highlight"><span class="result-value" id="future-value">₹0.00</span><span class="result-label">Total value</span></div><div class="result-card"><span class="result-value" id="absolute-return">0%</span><span class="result-label">Absolute return</span></div></div><div class="chart-container"><canvas id="calc-chart"></canvas></div><div id="sip-table" class="amortization-table"></div></div>
    </section>""",
    "how_to": ["Enter the amount you plan to invest every month through SIP.", "Choose an expected annual return; use conservative assumptions for planning and higher figures only for scenario testing.", "Set the number of years you will keep investing.", "Select Calculate SIP returns to see invested amount, gain, maturity value, and return percentage.", "Use the year-wise table and chart to see how compounding becomes stronger in later years."],
    "formula_box": "FV = P × {[(1 + r)<sup>n</sup> − 1] / r} × (1 + r)<br>P = monthly SIP, r = monthly return, n = number of months",
    "formula_text": "<p>SIP future value assumes that the same amount is invested at the start or end of each monthly period and grows at a constant monthly rate. The annual expected return is divided by 12 and converted to a decimal. The formula adds the compounded value of every monthly instalment. Early instalments remain invested longer, so they contribute more to the final corpus than later instalments.</p><p>Actual mutual fund returns are market-linked and never move in a straight line. Equity SIPs can show negative returns over short periods, while long holding periods may reduce but not remove volatility. The calculator is best used for goal planning: retirement, children’s education, house down payment, or wealth targets such as ₹1 crore. It does not include expense ratio changes, exit load, capital gains tax, STT, or changes in SIP amount.</p>",
    "example": "<p>A monthly SIP of ₹10,000 for 15 years at an assumed 12% annual return invests ₹18,00,000.</p><p>The estimated maturity value is about ₹50,45,760, so the wealth gain is about ₹32,45,760.</p><p><strong>The same SIP continued longer can move the goal from lakhs toward crores because later years compound a larger base.</strong></p>",
    "reference_title": "Monthly SIP needed for wealth targets at 12%",
    "reference_headers": ["Target corpus", "10 years", "15 years", "20 years", "25 years"],
    "reference_rows": [["₹25L", "₹10,861", "₹4,954", "₹2,527", "₹1,322"], ["₹50L", "₹21,722", "₹9,908", "₹5,054", "₹2,644"], ["₹1Cr", "₹43,444", "₹19,816", "₹10,109", "₹5,288"], ["₹2Cr", "₹86,888", "₹39,632", "₹20,218", "₹10,576"], ["₹5Cr", "₹2,17,220", "₹99,080", "₹50,545", "₹26,440"], ["₹10L", "₹4,344", "₹1,982", "₹1,011", "₹529"], ["₹75L", "₹32,583", "₹14,862", "₹7,582", "₹3,966"], ["₹3Cr", "₹1,30,332", "₹59,448", "₹30,327", "₹15,864"]],
    "sections": [("What is SIP?", "<p>A Systematic Investment Plan is a method of investing a fixed amount in a mutual fund at regular intervals, usually monthly. It helps investors automate discipline and buy more units when prices are low and fewer units when prices are high. SIP is not a separate product; it is an investment route into mutual fund schemes such as equity funds, hybrid funds, debt funds, and index funds.</p>"), ("SIP vs lump sum", table(["Point", "SIP", "Lump sum"], [["Cash flow", "Monthly investment from salary", "One-time investment"], ["Market timing", "Reduces timing risk through averaging", "Entry valuation matters more"], ["Best suited for", "Regular income earners", "Investors with idle corpus"], ["Volatility comfort", "Usually easier emotionally", "Can fluctuate sharply from day one"], ["Goal planning", "Useful for long goals", "Useful when money is already available"], ["Tax", "Each instalment has its own holding period", "One purchase date for holding period"], ["Discipline", "Automatic habit", "Requires allocation decision"], ["Common use", "Salary-based investing", "Bonus, inheritance, asset sale proceeds"]])), ("Benefits of starting early", "<p>If two investors target retirement wealth with a ₹5,000 monthly SIP at 12%, starting at age 25 for 35 years can create a corpus many times larger than starting at age 35 for 25 years. The difference is not only the extra ₹6,00,000 invested over 10 years; it is the additional decade of compounding on every early instalment. In India, starting early also leaves more time to handle bear markets without disturbing long-term goals.</p>")],
    "faqs": [("What is SIP?", "SIP is a systematic way to invest a fixed amount in a mutual fund at regular intervals, usually every month."), ("Is SIP safe?", "SIP reduces timing risk but does not remove market risk. Safety depends on the mutual fund category, portfolio, time horizon, and investor behavior."), ("How much SIP to become crorepati?", "At 12% annual return, a ₹10,109 monthly SIP for 20 years or about ₹19,816 for 15 years can target ₹1 crore before taxes and charges."), ("Can I stop SIP midway?", "Yes, most SIP mandates can be paused or stopped, but the process and timeline depend on the AMC, platform, and bank mandate."), ("What is XIRR in SIP?", "XIRR is the annualized return for investments made on different dates. It is useful for SIPs because every instalment has a different investment date.")],
    "notes": ["Mutual fund investments are subject to market risk; expected return is only an assumption.", "Equity fund gains are taxed based on holding period and current capital gains rules, which can change.", "Each SIP instalment has its own purchase date for exit load and capital gains holding period.", "Use direct plans, expense ratios, asset allocation, and goal horizon while choosing schemes, not only past returns."],
    "script": """syncRange('sip-range', 'sip-amount', calculate);
syncRange('return-range', 'return-rate', calculate);
syncRange('years-range', 'years', calculate);
function calculate() {
  const p = value('sip-amount');
  const annual = value('return-rate');
  const years = Math.max(1, value('years'));
  const months = years * 12;
  const r = annual / 100 / 12;
  const fv = r === 0 ? p * months : p * ((Math.pow(1 + r, months) - 1) / r) * (1 + r);
  const invested = p * months;
  const gain = Math.max(0, fv - invested);
  text('invested', formatIndianNumber(invested));
  text('gain', formatIndianNumber(gain));
  text('future-value', `${formatIndianNumber(fv)} (${formatShortIndian(fv)})`);
  text('absolute-return', `${formatPlainNumber((gain / Math.max(1, invested)) * 100, 1)}%`);
  const labels = [], investedData = [], gainData = [];
  let tableRows = '';
  for (let y = 1; y <= years; y++) {
    const m = y * 12;
    const valueAtYear = r === 0 ? p * m : p * ((Math.pow(1 + r, m) - 1) / r) * (1 + r);
    const investedAtYear = p * m;
    labels.push(`Year ${y}`);
    investedData.push(investedAtYear);
    gainData.push(Math.max(0, valueAtYear - investedAtYear));
    tableRows += `<tr><td>Year ${y}</td><td>${formatIndianNumber(investedAtYear)}</td><td>${formatIndianNumber(Math.max(0, valueAtYear - investedAtYear))}</td><td>${formatIndianNumber(valueAtYear)}</td></tr>`;
  }
  drawChart('calc-chart', 'bar', labels, [{ label: 'Invested amount', data: investedData, backgroundColor: '#2563eb' }, { label: 'Estimated returns', data: gainData, backgroundColor: '#16a34a' }], { scales: { x: { stacked: true }, y: { stacked: true } } });
  html('sip-table', '<table class="reference-table"><thead><tr><th>Year</th><th>Invested</th><th>Returns</th><th>Total value</th></tr></thead><tbody>' + tableRows + '</tbody></table>');
}
bindCalculator(calculate);""",
})


PAGES.append({
    "file": "fd-calculator.html",
    "title": "FD Calculator — Fixed Deposit Maturity Amount | Calculatorcity",
    "meta": "Free FD calculator India. Calculate fixed deposit maturity amount and interest earned. Compare simple and compound interest. Supports quarterly compounding.",
    "h1": "Fixed Deposit (FD) Calculator",
    "intro": "The FD calculator estimates fixed deposit maturity amount, interest earned, post-TDS interest, and effective annual yield for Indian bank deposits. Enter principal, interest rate, tenure, compounding frequency, and TDS preference to compare cumulative and simple-interest outcomes. The chart compares FD growth with an assumed 6% inflation line so you can judge both nominal safety and real purchasing power over the deposit period.",
    "widget": """<section class="calc-widget">
      <div class="field-grid">
        <div class="calc-input-group"><label for="principal">Principal amount (₹)</label><div class="input-prefix"><span>₹</span><input id="principal" type="number" value="500000"></div></div>
        <div class="calc-input-group"><label for="fd-rate">Annual interest rate (%)</label><input id="fd-rate" type="number" step="0.05" value="7.25"></div>
        <div class="calc-input-group"><label for="years">Tenure years</label><input id="years" type="number" value="3"></div>
        <div class="calc-input-group"><label for="months">Tenure months</label><input id="months" type="number" value="0"></div>
        <div class="calc-input-group"><label for="compounding">Interest compounding</label><select id="compounding"><option value="4" selected>Quarterly</option><option value="12">Monthly</option><option value="2">Half-yearly</option><option value="1">Annually</option><option value="0">Simple interest</option></select></div>
        <div class="calc-input-group"><label for="tds">Tax deducted at source</label><select id="tds"><option value="yes" selected>Yes, 10% TDS if applicable</option><option value="no">No / Form 15G or 15H</option></select></div>
      </div>
      <button class="calc-btn" id="calculate" type="button">Calculate FD maturity</button>
      <div class="calc-result show"><div class="result-grid"><div class="result-card highlight"><span class="result-value" id="maturity">₹0.00</span><span class="result-label">Maturity amount</span></div><div class="result-card"><span class="result-value" id="interest">₹0.00</span><span class="result-label">Total interest</span></div><div class="result-card"><span class="result-value" id="post-tds">₹0.00</span><span class="result-label">Post-TDS interest</span></div><div class="result-card"><span class="result-value" id="yield">0%</span><span class="result-label">Effective annual yield</span></div></div><div class="chart-container"><canvas id="calc-chart"></canvas></div></div>
    </section>""",
    "how_to": ["Enter the deposit amount you plan to place in the FD.", "Type the annual FD interest rate quoted by the bank or NBFC.", "Enter tenure using years and months together.", "Choose quarterly compounding for most Indian cumulative bank FDs, or simple interest for payout-style comparison.", "Select whether TDS should be estimated and review maturity amount, interest, post-TDS interest, and yield."],
    "formula_box": "Compound FD: A = P × (1 + r/m)<sup>m×t</sup><br>Simple FD: Interest = P × r × t<br>Effective yield = (A / P)<sup>1/t</sup> − 1",
    "formula_text": "<p>For a cumulative fixed deposit, interest is added back to the deposit at the chosen compounding frequency. Quarterly compounding is common for Indian bank FDs, so the annual rate is divided by four and applied for each completed quarter-equivalent period. Monthly, half-yearly, and annual compounding follow the same structure with different compounding counts. Simple interest does not add interest back to principal and is useful for comparing payout deposits.</p><p>The calculator estimates TDS at 10% when total interest crosses the common non-senior threshold of ₹40,000 in a financial year. TDS is not the final tax. FD interest is added to income and taxed at the slab rate, so a person in the 20% or 30% slab may owe additional tax after TDS, while a person below taxable income may submit Form 15G or 15H if eligible.</p>",
    "example": "<p>A ₹5,00,000 FD at 7.25% for 3 years with quarterly compounding grows to about ₹6,20,160.</p><p>Total interest is about ₹1,20,160. If 10% TDS applies, tax deducted is about ₹12,016 and post-TDS interest received is about ₹1,08,144.</p><p><strong>The interest still has to be reported in the income tax return.</strong></p>",
    "reference_title": "Indicative FD rates at major Indian banks",
    "reference_headers": ["Bank", "General public", "Senior citizen", "Notes"],
    "reference_rows": [["SBI", "6.50% to 7.25%", "Usually +0.50%", "Tenure dependent"], ["HDFC Bank", "6.60% to 7.35%", "Usually +0.50%", "Indicative retail range"], ["ICICI Bank", "6.60% to 7.25%", "Usually +0.50%", "Tenure dependent"], ["Axis Bank", "6.70% to 7.30%", "Usually +0.50%", "Promotional tenures vary"], ["Kotak Mahindra Bank", "6.50% to 7.40%", "Usually +0.50%", "Indicative only"], ["Bank of Baroda", "6.50% to 7.25%", "Usually +0.50%", "Public sector bank"], ["Canara Bank", "6.40% to 7.25%", "Usually +0.50%", "Tenure dependent"], ["Punjab National Bank", "6.40% to 7.25%", "Usually +0.50%", "Check current card rate"]],
    "sections": [("Senior citizen FD rates", "<p>Senior citizens generally receive an extra 0.50% per year on many bank FD tenures. Some banks also offer special senior or super-senior products with different rates and conditions. The extra rate improves maturity value, but interest remains taxable unless a specific exemption applies.</p>"), ("Tax and premature withdrawal", "<p>FD interest is taxed under income from other sources at your slab rate. Banks deduct TDS when interest crosses threshold rules, but TDS does not settle the final liability. Premature withdrawal can reduce the applicable rate and may attract a penalty, often 0.50% to 1.00%. Compare liquidity needs before locking money for long tenures.</p>")],
    "faqs": [("How is FD interest calculated?", "Cumulative FD interest is usually compounded quarterly in India. The rate is applied periodically and added to principal until maturity."), ("Is FD interest taxable?", "Yes. FD interest is added to your income and taxed at your slab rate, even when the bank has already deducted TDS."), ("What is TDS on FD?", "TDS is tax deducted by the bank when interest crosses threshold limits. For many resident individuals it is 10% if PAN is available."), ("What is cumulative vs non-cumulative FD?", "Cumulative FDs pay principal plus compounded interest at maturity. Non-cumulative FDs pay interest monthly, quarterly, half-yearly, or annually."), ("Is FD safe?", "Bank FDs are relatively low-risk, and deposits are insured by DICGC up to the applicable limit per depositor per bank, but interest-rate and inflation risk remain.")],
    "notes": ["FD rate cards change often; verify the rate on the bank website before booking.", "Senior citizen thresholds and TDS rules can differ from non-senior depositors.", "TDS is not final tax; report FD interest in your income tax return.", "Premature withdrawal may reduce the contracted rate and add a penalty."],
    "script": """function calculate() {
  const p = value('principal');
  const rate = value('fd-rate') / 100;
  const years = value('years') + value('months') / 12;
  const comp = Number(document.getElementById('compounding').value);
  let amount = p;
  if (comp === 0) amount = p + p * rate * years;
  else amount = p * Math.pow(1 + rate / comp, comp * years);
  const interest = Math.max(0, amount - p);
  const tdsApplicable = document.getElementById('tds').value === 'yes' && interest > 40000;
  const tdsAmount = tdsApplicable ? interest * 0.10 : 0;
  const postTdsInterest = interest - tdsAmount;
  const yieldRate = years > 0 && p > 0 ? (Math.pow(amount / p, 1 / years) - 1) * 100 : 0;
  text('maturity', formatIndianNumber(amount));
  text('interest', formatIndianNumber(interest));
  text('post-tds', formatIndianNumber(postTdsInterest));
  text('yield', `${formatPlainNumber(yieldRate, 2)}%`);
  const labels = [], fd = [], inflation = [];
  for (let y = 0; y <= Math.ceil(years); y++) {
    labels.push(`Year ${y}`);
    const t = Math.min(y, years);
    fd.push(comp === 0 ? p + p * rate * t : p * Math.pow(1 + rate / Math.max(1, comp), Math.max(1, comp) * t));
    inflation.push(p * Math.pow(1.06, t));
  }
  drawChart('calc-chart', 'line', labels, [{ label: 'FD value', data: fd, borderColor: '#f97316', backgroundColor: '#fff7ed', fill: true }, { label: '6% inflation line', data: inflation, borderColor: '#64748b', backgroundColor: '#f1f5f9', fill: false }]);
}
bindCalculator(calculate);""",
})


PAGES.append({
    "file": "ctc-salary-calculator.html",
    "title": "CTC to In-Hand Salary Calculator India | Calculatorcity",
    "meta": "Free CTC to in-hand salary calculator India. Convert your annual CTC to monthly take-home salary with complete breakup of PF, HRA, basic, and deductions.",
    "h1": "CTC to In-Hand Salary Calculator",
    "intro": "The CTC to in-hand salary calculator converts an Indian annual compensation package into an estimated monthly take-home salary. Enter annual CTC, city type, rent, professional tax state, voluntary PF, and extra deductions to see a salary slip style breakup. It estimates basic pay, HRA, special allowance, LTA, employee PF, professional tax, income tax TDS, and the final net salary credited to your bank account.",
    "chart": False,
    "widget": """<section class="calc-widget">
      <div class="field-grid">
        <div class="calc-input-group"><label for="ctc">Annual CTC (₹)</label><div class="input-prefix"><span>₹</span><input id="ctc" type="number" value="1200000"></div></div>
        <div class="calc-input-group"><label for="city-type">City type</label><select id="city-type"><option value="metro" selected>Metro</option><option value="non-metro">Non-metro</option></select></div>
        <div class="calc-input-group"><label for="rent">Rent paid monthly (₹)</label><div class="input-prefix"><span>₹</span><input id="rent" type="number" value="25000"></div></div>
        <div class="calc-input-group"><label for="pt-state">Professional tax state</label><select id="pt-state"><option value="200">Andhra Pradesh - ₹200/month</option><option value="200" selected>Karnataka - ₹200/month</option><option value="200">Maharashtra - ₹200/month approx.</option><option value="208">Telangana - ₹208/month approx.</option><option value="0">Delhi / no PT state - ₹0</option></select></div>
        <div class="calc-input-group"><label for="additional">Additional deductions monthly (₹)</label><div class="input-prefix"><span>₹</span><input id="additional" type="number" value="0"></div></div>
        <div class="calc-input-group"><label for="vpf">VPF monthly (₹)</label><div class="input-prefix"><span>₹</span><input id="vpf" type="number" value="0"></div></div>
      </div>
      <button class="calc-btn" id="calculate" type="button">Calculate in-hand salary</button>
      <div class="calc-result show"><div class="result-grid"><div class="result-card highlight"><span class="result-value" id="net-monthly">₹0.00</span><span class="result-label">Net take-home salary</span></div><div class="result-card"><span class="result-value" id="gross-monthly">₹0.00</span><span class="result-label">Gross monthly salary</span></div><div class="result-card"><span class="result-value" id="deductions">₹0.00</span><span class="result-label">Monthly deductions</span></div><div class="result-card"><span class="result-value" id="tds">₹0.00</span><span class="result-label">Estimated income tax TDS</span></div></div><div class="visual-panel"><div id="salary-slip" class="svg-slip"></div></div></div>
    </section>""",
    "how_to": ["Enter the annual CTC mentioned in the offer letter.", "Choose metro or non-metro because HRA is usually structured differently.", "Enter monthly rent, professional tax state, VPF, and any other recurring deductions.", "Click Calculate in-hand salary to generate the salary slip breakup.", "Review earnings, statutory deductions, tax estimate, and net monthly salary before comparing offers."],
    "formula_box": "Basic = 40% of CTC<br>HRA = 50% of basic in metro, 40% in non-metro<br>Net salary = Gross monthly earnings − employee PF − professional tax − TDS − other deductions",
    "formula_text": "<p>CTC is not the same as in-hand salary. Cost to Company can include employer PF, gratuity accrual, insurance premium, variable bonus, joining bonus, meal benefits, and other components that may not be paid monthly. This calculator uses a common Indian salary structure: basic salary at 40% of CTC, HRA based on city type, a small LTA component, and special allowance as the balancing figure. It then estimates employee PF at 12% of basic with a practical monthly cap shown in the calculator.</p><p>Income tax TDS is estimated using a simplified new-regime calculation for salary planning. Actual take-home can differ if your employer uses a different salary structure, variable pay is paid quarterly or annually, old-regime declarations are accepted, NPS employer contribution is included, or reimbursements require bills. Treat the output as an offer-comparison estimate, not a payroll guarantee.</p>",
    "example": "<p>For a ₹12,00,000 annual CTC, basic salary is estimated at ₹4,80,000 per year and metro HRA at ₹2,40,000 per year.</p><p>After employee PF of up to ₹1,800 per month, professional tax, and estimated TDS, monthly in-hand salary may be around ₹83,000 to ₹89,000 depending on deductions.</p><p><strong>The payslip visual shows how ₹1 lakh monthly CTC becomes a lower bank credit.</strong></p>",
    "reference_title": "CTC vs estimated monthly take-home",
    "reference_headers": ["Annual CTC", "Approx. monthly CTC", "Estimated in-hand", "Common observation"],
    "reference_rows": [["₹3L", "₹25,000", "₹22,000 - ₹24,000", "Low or no TDS"], ["₹5L", "₹41,667", "₹36,000 - ₹39,000", "PF and PT matter"], ["₹8L", "₹66,667", "₹58,000 - ₹62,000", "Tax starts affecting take-home"], ["₹10L", "₹83,333", "₹71,000 - ₹77,000", "Structure differences visible"], ["₹15L", "₹1,25,000", "₹1,02,000 - ₹1,12,000", "TDS becomes material"], ["₹20L", "₹1,66,667", "₹1,32,000 - ₹1,47,000", "Check variable pay"], ["₹25L", "₹2,08,333", "₹1,62,000 - ₹1,82,000", "NPS and reimbursements matter"], ["₹30L", "₹2,50,000", "₹1,92,000 - ₹2,16,000", "Surcharge not usually relevant yet"]],
    "sections": [("Reading an Indian salary slip", "<p>A salary slip usually separates earnings and deductions. Earnings can include basic, HRA, special allowance, LTA, conveyance, and reimbursements. Deductions can include employee PF, professional tax, income tax TDS, VPF, insurance, canteen recovery, loan recovery, or loss-of-pay adjustment. The net pay is what reaches the bank account.</p><p>When comparing two offers, check fixed pay separately from variable bonus, joining bonus clawback, stock vesting, employer PF, gratuity, and insurance. Two offers with the same CTC can produce different monthly cash flow.</p>")],
    "faqs": [("What is CTC?", "CTC means Cost to Company. It is the total annual cost an employer associates with your compensation, not necessarily the cash paid every month."), ("Why is in-hand salary lower than CTC?", "In-hand salary is lower because CTC can include employer benefits, PF, gratuity, tax deductions, professional tax, and variable pay."), ("What is basic salary?", "Basic salary is the core salary component. Many benefits and deductions such as HRA, PF, and gratuity are linked to basic pay."), ("How is PF calculated?", "Employee PF is generally 12% of basic salary, often with wage-cap practices depending on employer policy and statutory coverage."), ("Does rent paid change in-hand salary?", "Rent paid does not directly change monthly payroll unless old-regime HRA declarations are used for TDS. This calculator uses rent for context but estimates TDS simply.")],
    "notes": ["Professional tax rates are state-specific and may vary by salary slab and month.", "Employer PF, gratuity, insurance, and variable pay can be included in CTC but not monthly take-home.", "The calculator estimates TDS; final tax depends on chosen regime, declarations, Form 16, AIS, and other income.", "Offer letters may use different basic/HRA percentages, so compare with the actual salary annexure."],
    "script": """const slabs = [[0,300000,0],[300000,700000,0.05],[700000,1000000,0.10],[1000000,1200000,0.15],[1200000,1500000,0.20],[1500000,Infinity,0.30]];
function estimateTax(annualGross) {
  const taxable = Math.max(0, annualGross - 75000);
  let tax = taxable <= 700000 ? 0 : slabTax(taxable, slabs);
  return tax * 1.04;
}
function calculate() {
  const ctc = value('ctc');
  const monthlyCtc = ctc / 12;
  const basicAnnual = ctc * 0.40;
  const basicMonthly = basicAnnual / 12;
  const hraAnnual = basicAnnual * (document.getElementById('city-type').value === 'metro' ? 0.50 : 0.40);
  const hraMonthly = hraAnnual / 12;
  const ltaMonthly = ctc * 0.05 / 12;
  const employeePf = Math.min(basicMonthly * 0.12, 1800) + value('vpf');
  const professionalTax = Number(document.getElementById('pt-state').value) || 0;
  const annualTax = estimateTax(ctc);
  const monthlyTds = annualTax / 12;
  const specialMonthly = Math.max(0, monthlyCtc - basicMonthly - hraMonthly - ltaMonthly);
  const additional = value('additional');
  const totalDeductions = employeePf + professionalTax + monthlyTds + additional;
  const net = Math.max(0, monthlyCtc - totalDeductions);
  text('net-monthly', formatIndianNumber(net));
  text('gross-monthly', formatIndianNumber(monthlyCtc));
  text('deductions', formatIndianNumber(totalDeductions));
  text('tds', formatIndianNumber(monthlyTds));
  html('salary-slip', `<svg viewBox="0 0 760 420" role="img" aria-label="Salary slip breakup" style="width:100%;height:auto"><rect width="760" height="420" rx="8" fill="#fff"/><rect x="24" y="24" width="712" height="56" rx="6" fill="#fff7ed" stroke="#fdba74"/><text x="44" y="59" font-size="24" font-weight="700" fill="#0f172a">Monthly Salary Slip Estimate</text><text x="560" y="59" font-size="18" font-weight="700" fill="#f97316">${formatIndianNumber(net)}</text><text x="44" y="112" font-size="18" font-weight="700" fill="#166534">Earnings</text><text x="400" y="112" font-size="18" font-weight="700" fill="#dc2626">Deductions</text>${rowSvg(44,145,'Basic salary',basicMonthly)}${rowSvg(44,185,'HRA',hraMonthly)}${rowSvg(44,225,'Special allowance',specialMonthly)}${rowSvg(44,265,'LTA',ltaMonthly)}${rowSvg(400,145,'Employee PF',employeePf)}${rowSvg(400,185,'Professional tax',professionalTax)}${rowSvg(400,225,'Income tax TDS',monthlyTds)}${rowSvg(400,265,'Other deductions',additional)}<line x1="44" y1="322" x2="716" y2="322" stroke="#e2e8f0"/><text x="44" y="360" font-size="20" font-weight="700" fill="#0f172a">Net take-home salary</text><text x="560" y="360" font-size="22" font-weight="800" fill="#f97316">${formatIndianNumber(net)}</text></svg>`);
}
function rowSvg(x, y, label, amount) {
  return `<text x="${x}" y="${y}" font-size="15" fill="#475569">${label}</text><text x="${x + 210}" y="${y}" font-size="15" font-weight="700" fill="#0f172a">${formatIndianNumber(amount)}</text>`;
}
bindCalculator(calculate);""",
})


PAGES.append({
    "file": "pf-epf-calculator.html",
    "title": "PF Calculator — EPF Maturity Amount Calculator | Calculatorcity",
    "meta": "Free EPF/PF calculator India. Calculate your Employee Provident Fund balance at retirement. Shows month-wise contributions and interest accumulated.",
    "h1": "EPF / PF Calculator (Employee Provident Fund)",
    "intro": "The EPF calculator projects your provident fund corpus at retirement using monthly employee contribution, employer EPF contribution, EPS diversion, salary increments, current balance, and declared interest rate. It is built for Indian salaried employees who want to estimate long-term retirement savings in rupees. The year-wise chart shows how fresh contributions and annual compounding can turn monthly PF deductions into a large retirement balance.",
    "widget": """<section class="calc-widget">
      <div class="field-grid">
        <div class="calc-input-group"><label for="current-age">Current age</label><input id="current-age" type="number" value="30"></div>
        <div class="calc-input-group"><label for="retirement-age">Retirement age</label><input id="retirement-age" type="number" value="58"></div>
        <div class="calc-input-group"><label for="basic-salary">Monthly basic salary + DA (₹)</label><div class="input-prefix"><span>₹</span><input id="basic-salary" type="number" value="50000"></div></div>
        <div class="calc-input-group"><label for="current-balance">Current EPF balance (₹)</label><div class="input-prefix"><span>₹</span><input id="current-balance" type="number" value="200000"></div></div>
        <div class="calc-input-group"><label for="increment">Expected annual salary increment (%)</label><input id="increment" type="number" step="0.1" value="6"></div>
        <div class="calc-input-group"><label for="epf-rate">EPF interest rate (%)</label><input id="epf-rate" type="number" step="0.05" value="8.25"><span class="hint">Editable; EPFO rates are declared yearly.</span></div>
      </div>
      <button class="calc-btn" id="calculate" type="button">Calculate EPF corpus</button>
      <div class="calc-result show"><div class="result-grid"><div class="result-card"><span class="result-value" id="employee-contribution">₹0.00</span><span class="result-label">Monthly employee contribution</span></div><div class="result-card"><span class="result-value" id="employer-contribution">₹0.00</span><span class="result-label">Monthly employer EPF contribution</span></div><div class="result-card"><span class="result-value" id="eps-contribution">₹0.00</span><span class="result-label">Monthly EPS contribution</span></div><div class="result-card highlight"><span class="result-value" id="corpus">₹0.00</span><span class="result-label">EPF corpus at retirement</span></div><div class="result-card"><span class="result-value" id="pension">₹0.00</span><span class="result-label">Estimated EPS pension/month</span></div></div><div class="chart-container"><canvas id="calc-chart"></canvas></div></div>
    </section>""",
    "how_to": ["Enter your current age and expected retirement age.", "Enter monthly basic salary plus dearness allowance, not full CTC.", "Add current EPF balance from passbook if available.", "Enter expected annual increment and EPF interest rate.", "Calculate to see monthly PF split, projected corpus, EPS pension estimate, and year-wise growth."],
    "formula_box": "Employee EPF = 12% of Basic + DA<br>Employer EPS = 8.33% of pensionable salary, commonly capped at ₹15,000<br>Employer EPF = Employer 12% share − EPS diversion",
    "formula_text": "<p>EPF contributions are usually linked to basic salary plus dearness allowance. The employee contribution is 12%. The employer also contributes 12%, but a portion is diverted to the Employee Pension Scheme. For many members, EPS is calculated at 8.33% of pensionable salary capped at ₹15,000 per month, so the maximum EPS diversion is about ₹1,250 per month. The remaining employer share goes to EPF.</p><p>The calculator adds monthly employee and employer EPF contributions to the current balance, grows salary yearly by the increment assumption, and applies annual EPF interest to the accumulating balance. EPS pension is estimated with a simplified pensionable salary × service / 70 method. Actual EPS depends on service history, wage ceiling, higher pension options, scheme rules, and EPFO records, so use the pension number only as a rough guide.</p>",
    "example": "<p>A 30-year-old employee with ₹50,000 basic salary and ₹2,00,000 current EPF balance contributes ₹6,000 monthly as employee EPF.</p><p>With EPS capped at ₹1,250, employer EPF contribution is about ₹4,750 per month. At 8.25% interest and 6% salary growth, the retirement corpus can cross ₹1 crore.</p><p><strong>The exact result depends heavily on future increments and declared EPF rates.</strong></p>",
    "reference_title": "EPF interest rates for recent years",
    "reference_headers": ["Financial year", "EPF interest rate", "Context"],
    "reference_rows": [["2015-16", "8.80%", "Higher-rate period"], ["2016-17", "8.65%", "Declared by EPFO"], ["2017-18", "8.55%", "Declared by EPFO"], ["2018-19", "8.65%", "Declared by EPFO"], ["2019-20", "8.50%", "Declared by EPFO"], ["2020-21", "8.50%", "Declared by EPFO"], ["2021-22", "8.10%", "Lower-rate year"], ["2022-23", "8.15%", "Declared by EPFO"], ["2023-24", "8.25%", "Declared by EPFO"], ["2024-25", "8.25%", "Retained as per EPFO recommendation/approval cycle"]],
    "sections": [("EPF vs EPS", "<p>EPF is the provident fund balance that earns declared interest and is visible in the member passbook. EPS is the pension scheme portion funded from the employer contribution. EPS does not grow like an individual investment account in the passbook; it supports monthly pension eligibility under scheme rules. This distinction explains why the entire employer contribution does not appear as EPF balance.</p>"), ("Withdrawal and tax basics", "<p>EPF withdrawals are generally tax-favorable after five years of continuous service, but early withdrawal, unemployment withdrawal, transfer gaps, and employer contributions above specified limits can create tax consequences. UAN linking, KYC, Aadhaar, PAN, and bank verification are important for online claims and transfers.</p>")],
    "faqs": [("What is EPF?", "EPF is Employee Provident Fund, a retirement savings scheme for eligible salaried employees in India."), ("How much does employer contribute to PF?", "The employer contributes 12% of basic plus DA, but part of it is diverted to EPS and the balance goes to EPF."), ("Can I withdraw PF before retirement?", "Partial or full withdrawal is allowed in specified situations such as unemployment, housing, illness, marriage, and retirement, subject to EPFO rules."), ("Is PF interest taxable?", "For most employees, EPF interest is tax-favorable within prescribed limits, but excess employee contribution and some early withdrawals can be taxable."), ("How to check PF balance?", "You can check EPF balance through the EPFO member passbook portal, UMANG app, SMS, or missed-call facility if UAN and KYC are active.")],
    "notes": ["EPF interest rate is declared for each financial year and may be credited after approval and processing.", "EPS contribution is commonly capped using pensionable salary rules; higher-pension cases require separate treatment.", "Keep UAN, Aadhaar, PAN, and bank KYC updated to avoid transfer and withdrawal delays.", "Transfer old member IDs after changing jobs so service continuity and balance tracking remain clean."],
    "script": """function calculate() {
  const currentAge = value('current-age');
  const retirementAge = value('retirement-age');
  let basic = value('basic-salary');
  let balance = value('current-balance');
  const increment = value('increment') / 100;
  const rate = value('epf-rate') / 100;
  const years = Math.max(0, retirementAge - currentAge);
  const labels = [], balances = [];
  let lastEmployee = 0, lastEmployer = 0, lastEps = 0;
  for (let y = 1; y <= years; y++) {
    for (let m = 0; m < 12; m++) {
      const employee = basic * 0.12;
      const eps = Math.min(basic, 15000) * 0.0833;
      const employer = Math.max(0, basic * 0.12 - eps);
      balance += employee + employer;
      lastEmployee = employee; lastEmployer = employer; lastEps = eps;
    }
    balance *= (1 + rate);
    labels.push(`Age ${currentAge + y}`);
    balances.push(balance);
    basic *= (1 + increment);
  }
  const service = years;
  const pension = Math.min(basic, 15000) * service / 70;
  text('employee-contribution', formatIndianNumber(lastEmployee || value('basic-salary') * 0.12));
  text('employer-contribution', formatIndianNumber(lastEmployer || Math.max(0, value('basic-salary') * 0.12 - Math.min(value('basic-salary'), 15000) * 0.0833)));
  text('eps-contribution', formatIndianNumber(lastEps || Math.min(value('basic-salary'), 15000) * 0.0833));
  text('corpus', `${formatIndianNumber(balance)} (${formatShortIndian(balance)})`);
  text('pension', formatIndianNumber(pension));
  drawChart('calc-chart', 'bar', labels, [{ label: 'EPF balance', data: balances, backgroundColor: '#f97316' }]);
}
bindCalculator(calculate);""",
})


PAGES.append({
    "file": "on-road-price-calculator.html",
    "title": "On-Road Price Calculator India — Car On-Road Price | Calculatorcity",
    "meta": "Calculate on-road price of any car in India. Add ex-showroom price, get RTO charges, insurance, TCS and other costs state-wise. Free car price calculator.",
    "h1": "Car On-Road Price Calculator India",
    "intro": "The car on-road price calculator estimates the final amount payable for buying a vehicle in India after adding state registration tax, road tax, insurance, FASTag, handling charges, and TCS on high-value cars. Enter the ex-showroom price, state, fuel type, and vehicle category to build a transparent cost breakup. It is especially useful when comparing dealer quotes across Delhi, Maharashtra, Karnataka, Andhra Pradesh, Telangana, and other states.",
    "widget": """<section class="calc-widget">
      <div class="field-grid">
        <div class="calc-input-group"><label for="ex-showroom">Ex-showroom price (₹)</label><div class="input-prefix"><span>₹</span><input id="ex-showroom" type="number" value="1000000"></div></div>
        <div class="calc-input-group"><label for="state">State / UT</label><select id="state"></select></div>
        <div class="calc-input-group"><label for="fuel">Vehicle type</label><select id="fuel"><option value="petrol">Petrol</option><option value="diesel">Diesel</option><option value="cng">CNG</option><option value="electric">Electric</option></select></div>
        <div class="calc-input-group"><label for="category">Category</label><select id="category"><option value="new" selected>New car</option><option value="used">Used car</option></select></div>
        <div class="calc-input-group"><label for="seating">Seating</label><select id="seating"><option value="normal" selected>Up to 10 seater</option><option value="large">More than 10 seater</option></select></div>
        <div class="calc-input-group"><label for="insurance-rate">Insurance estimate (%)</label><input id="insurance-rate" type="number" step="0.1" value="2.5"></div>
      </div>
      <button class="calc-btn" id="calculate" type="button">Calculate on-road price</button>
      <div class="calc-result show"><div class="result-grid"><div class="result-card"><span class="result-value" id="road-tax">₹0.00</span><span class="result-label">Registration / road tax</span></div><div class="result-card"><span class="result-value" id="insurance">₹0.00</span><span class="result-label">Insurance estimate</span></div><div class="result-card"><span class="result-value" id="tcs">₹0.00</span><span class="result-label">TCS if applicable</span></div><div class="result-card highlight"><span class="result-value" id="on-road">₹0.00</span><span class="result-label">Total on-road price</span></div></div><div class="chart-container"><canvas id="calc-chart"></canvas></div><div id="breakup" class="amortization-table"></div></div>
    </section>""",
    "how_to": ["Enter the car’s ex-showroom price before registration and insurance.", "Select the state or union territory where the car will be registered.", "Choose fuel type because many states charge different road tax for petrol, diesel, CNG, and electric cars.", "Adjust insurance rate if your dealer quote is higher or lower.", "Calculate and compare the full on-road breakup with dealer quotations before booking."],
    "formula_box": "On-road price = Ex-showroom price + road tax + registration charges + insurance + FASTag + handling + TCS",
    "formula_text": "<p>On-road price is the amount a buyer usually pays to drive the car out of the showroom. The largest addition is state road tax or registration charge, calculated as a percentage of ex-showroom value. The percentage varies by state, vehicle cost, fuel type, seating capacity, and sometimes buyer category. Insurance is estimated as a percentage of insured declared value, while FASTag and handling charges are flat estimates.</p><p>For cars above ₹10,00,000, dealers generally collect tax collected at source at 1% under income tax provisions. TCS is not an extra cost in the same way as road tax because it can appear as tax credit in Form 26AS/AIS, but it affects cash outflow at purchase. Electric vehicles may get lower registration tax in some states, but concessions change frequently, so verify state notifications before payment.</p>",
    "example": "<p>A petrol car with ex-showroom price of ₹10,00,000 registered in Andhra Pradesh at an approximate 12% road tax has road tax of ₹1,20,000.</p><p>With insurance of ₹25,000, FASTag of ₹500, handling of ₹10,000, and no TCS threshold issue beyond normal rules, on-road price is about ₹11,55,500.</p><p><strong>Dealer quotes should be checked line by line against this breakup.</strong></p>",
    "reference_title": "Popular car on-road comparison",
    "reference_headers": ["Model", "Approx. ex-showroom", "Delhi on-road", "Mumbai on-road"],
    "reference_rows": [["Maruti Swift", "₹7,00,000", "₹7.65L", "₹8.05L"], ["Hyundai i20", "₹8,50,000", "₹9.30L", "₹9.85L"], ["Tata Nexon", "₹10,00,000", "₹11.00L", "₹11.70L"], ["Maruti Brezza", "₹9,50,000", "₹10.40L", "₹11.05L"], ["Hyundai Creta", "₹13,00,000", "₹14.45L", "₹15.25L"], ["Mahindra XUV700", "₹17,00,000", "₹18.95L", "₹20.00L"], ["Tata Punch EV", "₹11,00,000", "₹11.60L", "₹12.05L"], ["Toyota Innova Hycross", "₹20,00,000", "₹22.35L", "₹23.70L"]],
    "sections": [("State-wise RTO differences", "<p>Indian on-road prices vary sharply by state. Maharashtra and Karnataka can be materially higher than Delhi or Gujarat for many private cars, while Andhra Pradesh and Telangana often use higher slabs for diesel vehicles. Electric vehicles may receive concessions, but some states revise EV benefits as adoption increases. Always compare quotes based on the registration state, not where the dealer is located.</p>")],
    "faqs": [("What is ex-showroom price?", "Ex-showroom price is the manufacturer/dealer price before road tax, registration, insurance, FASTag, accessories, and other on-road costs."), ("Why is on-road price different by state?", "Road tax and registration charges are state subjects and vary by vehicle price, fuel type, seating capacity, and local rules."), ("What is TCS on car purchase?", "TCS is tax collected at source, generally 1% on cars above ₹10,00,000, and can be claimed as tax credit by the buyer."), ("Is insurance included in on-road price?", "Dealer on-road quotes usually include first-year comprehensive insurance, but you can compare and buy insurance separately where allowed."), ("Are handling charges legal?", "Handling or logistics charges are often disputed. Ask the dealer for an itemized invoice and check local transport department guidance.")],
    "notes": ["RTO rates in this calculator are approximate planning rates; final tax is determined by the registering authority.", "Andhra Pradesh and Telangana buyers should pay close attention to petrol vs diesel rates because the difference can be significant.", "TCS collected by the dealer should appear in tax credit statements if PAN is correctly captured.", "Dealer accessories, extended warranty, RSA, insurance add-ons, and hypothecation charges can change the final invoice."],
    "script": """const rtoRates = {
  'Andhra Pradesh': { petrol: 12, diesel: 14, cng: 12, electric: 1 }, 'Telangana': { petrol: 12, diesel: 14, cng: 12, electric: 1 }, 'Delhi': { petrol: 4, diesel: 5, cng: 4, electric: 0 }, 'Maharashtra': { petrol: 11, diesel: 13, cng: 11, electric: 1 }, 'Karnataka': { petrol: 13, diesel: 14, cng: 13, electric: 0 }, 'Tamil Nadu': { petrol: 10, diesel: 10, cng: 10, electric: 0 }, 'Gujarat': { petrol: 6, diesel: 6, cng: 6, electric: 0 }, 'Rajasthan': { petrol: 6, diesel: 6, cng: 6, electric: 0 }, 'Kerala': { petrol: 11, diesel: 13, cng: 11, electric: 5 }, 'Uttar Pradesh': { petrol: 8, diesel: 8, cng: 8, electric: 0 }, 'Haryana': { petrol: 6, diesel: 8, cng: 6, electric: 0 }, 'Punjab': { petrol: 8, diesel: 8, cng: 8, electric: 1 }, 'West Bengal': { petrol: 6, diesel: 7, cng: 6, electric: 0 }, 'Madhya Pradesh': { petrol: 8, diesel: 10, cng: 8, electric: 1 }, 'Bihar': { petrol: 8, diesel: 10, cng: 8, electric: 1 }, 'Odisha': { petrol: 6, diesel: 8, cng: 6, electric: 1 }, 'Assam': { petrol: 7, diesel: 8, cng: 7, electric: 1 }, 'Jharkhand': { petrol: 6, diesel: 8, cng: 6, electric: 1 }, 'Chhattisgarh': { petrol: 7, diesel: 8, cng: 7, electric: 1 }, 'Uttarakhand': { petrol: 8, diesel: 8, cng: 8, electric: 0 }, 'Himachal Pradesh': { petrol: 6, diesel: 7, cng: 6, electric: 0 }, 'Goa': { petrol: 9, diesel: 9, cng: 9, electric: 0 }, 'Jammu and Kashmir': { petrol: 9, diesel: 9, cng: 9, electric: 1 }, 'Chandigarh': { petrol: 6, diesel: 6, cng: 6, electric: 0 }, 'Puducherry': { petrol: 8, diesel: 8, cng: 8, electric: 0 }, 'Other States / UTs': { petrol: 8, diesel: 9, cng: 8, electric: 1 }
};
const stateSelect = document.getElementById('state');
Object.keys(rtoRates).forEach((state) => stateSelect.add(new Option(state, state)));
stateSelect.value = 'Andhra Pradesh';
function calculate() {
  const price = value('ex-showroom');
  const state = stateSelect.value;
  const fuel = document.getElementById('fuel').value;
  let rate = rtoRates[state][fuel] || rtoRates[state].petrol;
  if (document.getElementById('category').value === 'used') rate *= 0.55;
  if (document.getElementById('seating').value === 'large') rate += 2;
  const roadTax = price * rate / 100;
  const insurance = price * value('insurance-rate') / 100;
  const fastag = 500;
  const handling = price > 1500000 ? 15000 : 10000;
  const tcs = price > 1000000 ? price * 0.01 : 0;
  const total = price + roadTax + insurance + fastag + handling + tcs;
  text('road-tax', formatIndianNumber(roadTax));
  text('insurance', formatIndianNumber(insurance));
  text('tcs', formatIndianNumber(tcs));
  text('on-road', `${formatIndianNumber(total)} (${formatShortIndian(total)})`);
  html('breakup', '<table class="reference-table"><tbody>' + [['Ex-showroom', price], ['Registration / road tax', roadTax], ['Insurance', insurance], ['FASTag', fastag], ['Handling / logistics', handling], ['TCS', tcs], ['Total on-road price', total]].map(([l,v]) => `<tr><th>${l}</th><td>${formatIndianNumber(v)}</td></tr>`).join('') + '</tbody></table>');
  drawChart('calc-chart', 'bar', ['On-road breakup'], [{ label: 'Ex-showroom', data: [price], backgroundColor: '#2563eb' }, { label: 'Road tax', data: [roadTax], backgroundColor: '#f97316' }, { label: 'Insurance', data: [insurance], backgroundColor: '#16a34a' }, { label: 'Other', data: [fastag + handling + tcs], backgroundColor: '#64748b' }], { indexAxis: 'y', scales: { x: { stacked: true }, y: { stacked: true } } });
}
bindCalculator(calculate);""",
})


PAGES.append({
    "file": "gratuity-calculator.html",
    "title": "Gratuity Calculator India — Gratuity Amount Formula | Calculatorcity",
    "meta": "Free gratuity calculator India. Calculate your gratuity amount based on salary and years of service. Follows Payment of Gratuity Act 1972.",
    "h1": "Gratuity Calculator",
    "intro": "The gratuity calculator estimates the lump sum payable to an employee in India based on last drawn basic salary plus dearness allowance and completed years of service. It follows the common Payment of Gratuity Act formula for covered organisations and flags the five-year eligibility rule. The result also shows the private-sector tax-exempt limit and taxable gratuity where the payout crosses the exemption threshold.",
    "widget": """<section class="calc-widget">
      <div class="field-grid">
        <div class="calc-input-group"><label for="salary">Last drawn monthly salary (basic + DA) (₹)</label><div class="input-prefix"><span>₹</span><input id="salary" type="number" value="80000"></div></div>
        <div class="calc-input-group"><label for="years">Years of service</label><input id="years" type="number" step="0.1" value="8"></div>
        <div class="calc-input-group"><label for="org-type">Type of organization</label><select id="org-type"><option value="covered" selected>Covered under Gratuity Act</option><option value="not-covered">Not covered</option></select></div>
      </div>
      <button class="calc-btn" id="calculate" type="button">Calculate gratuity</button>
      <div class="calc-result show"><div class="result-grid"><div class="result-card highlight"><span class="result-value" id="gratuity">₹0.00</span><span class="result-label">Gratuity amount</span></div><div class="result-card"><span class="result-value" id="exempt">₹0.00</span><span class="result-label">Tax-exempt portion</span></div><div class="result-card"><span class="result-value" id="taxable">₹0.00</span><span class="result-label">Taxable gratuity</span></div><div class="result-card"><span class="result-value" id="eligibility">Eligible</span><span class="result-label">Eligibility status</span></div></div><div class="chart-container"><canvas id="calc-chart"></canvas></div></div>
    </section>""",
    "how_to": ["Enter your last drawn monthly basic salary plus dearness allowance.", "Enter completed years of continuous service with the employer.", "Select whether the employer is covered under the Payment of Gratuity Act.", "Calculate to see gratuity amount, exemption, taxable portion, and eligibility message.", "Use the reference table to compare how service length changes the payout."],
    "formula_box": "Covered employer: Gratuity = Monthly salary × 15 × Years of service / 26<br>Not covered: Gratuity = Monthly salary × 15 × Years of service / 30",
    "formula_text": "<p>For establishments covered by the Payment of Gratuity Act, gratuity is calculated as 15 days of wages for every completed year of service or part exceeding six months. The formula divides by 26 because the Act treats monthly wages as 26 working days. Salary for this purpose generally means last drawn basic salary plus dearness allowance. If the organisation is not covered, a common calculation uses half-month salary based on a 30-day month.</p><p>Eligibility usually requires at least five years of continuous service, except in cases such as death or disablement where the five-year condition may not apply. For private-sector employees, tax exemption is generally limited to the least of actual gratuity received, eligible formula amount, and the notified monetary cap. This calculator uses ₹20,00,000 as the private-sector exemption cap for planning.</p>",
    "example": "<p>An employee with last drawn basic plus DA of ₹80,000 and 8 years of service in a covered organisation gets gratuity of ₹80,000 × 15 × 8 / 26.</p><p>The estimated gratuity is ₹3,69,230.77.</p><p><strong>Because this is below ₹20,00,000, the entire amount is generally tax-exempt for many private-sector cases.</strong></p>",
    "reference_title": "Gratuity amounts by salary and service",
    "reference_headers": ["Monthly salary", "5 years", "10 years", "15 years", "20 years"],
    "reference_rows": [["₹30,000", "₹86,538", "₹1,73,077", "₹2,59,615", "₹3,46,154"], ["₹50,000", "₹1,44,231", "₹2,88,462", "₹4,32,692", "₹5,76,923"], ["₹75,000", "₹2,16,346", "₹4,32,692", "₹6,49,038", "₹8,65,385"], ["₹1,00,000", "₹2,88,462", "₹5,76,923", "₹8,65,385", "₹11,53,846"], ["₹1,50,000", "₹4,32,692", "₹8,65,385", "₹12,98,077", "₹17,30,769"], ["₹2,00,000", "₹5,76,923", "₹11,53,846", "₹17,30,769", "₹23,07,692"], ["₹2,50,000", "₹7,21,154", "₹14,42,308", "₹21,63,462", "₹28,84,615"], ["₹3,00,000", "₹8,65,385", "₹17,30,769", "₹25,96,154", "₹34,61,538"]],
    "sections": [("Who is eligible?", "<p>Employees in covered establishments generally become eligible after five years of continuous service. Service above six months in the final year is commonly rounded up for gratuity calculation. The five-year condition does not apply in death or disablement cases. Contractors, consultants, gig workers, and employees outside covered establishments may have different contractual treatment.</p>"), ("When is gratuity paid?", "<p>Gratuity is usually paid when employment ends because of resignation, retirement, superannuation, death, or disablement. Employers are expected to process eligible gratuity promptly after it becomes payable. Keep appointment letters, salary slips, and service records because last drawn salary and service period determine the amount.</p>")],
    "faqs": [("What is gratuity?", "Gratuity is a terminal benefit paid by an employer to an eligible employee for long service."), ("What is the minimum service period?", "The usual minimum is five years of continuous service, except for death or disablement cases."), ("Is gratuity taxable?", "It can be fully or partly exempt depending on employment type, actual amount, formula amount, and notified cap."), ("When is gratuity paid?", "It is paid when employment ends due to resignation, retirement, superannuation, death, or disablement."), ("What is the maximum gratuity amount?", "The statutory ceiling and tax exemption cap can differ by rule and notification; this calculator uses ₹20,00,000 for private-sector tax planning.")],
    "notes": ["The five-year rule has exceptions for death and disablement.", "Government employees have different tax treatment from private-sector employees.", "The formula uses basic salary plus DA, not full CTC or gross salary.", "Keep service records and final salary proof because they affect eligibility and calculation."],
    "script": """function calculate() {
  const salary = value('salary');
  const years = value('years');
  const covered = document.getElementById('org-type').value === 'covered';
  const eligible = years >= 5;
  const denominator = covered ? 26 : 30;
  const gratuity = eligible ? salary * 15 * Math.floor(years) / denominator : 0;
  const exempt = Math.min(gratuity, 2000000);
  const taxable = Math.max(0, gratuity - exempt);
  text('gratuity', formatIndianNumber(gratuity));
  text('exempt', formatIndianNumber(exempt));
  text('taxable', formatIndianNumber(taxable));
  text('eligibility', eligible ? 'Eligible' : 'Need 5 years');
  if (!eligible) text('eligibility', 'Minimum 5 years required');
  drawChart('calc-chart', 'bar', ['Gratuity breakup'], [{ label: 'Tax-exempt', data: [exempt], backgroundColor: '#16a34a' }, { label: 'Taxable', data: [taxable], backgroundColor: '#dc2626' }], { indexAxis: 'y', scales: { x: { stacked: true }, y: { stacked: true } } });
}
bindCalculator(calculate);""",
})


PAGES.append({
    "file": "cgpa-to-percentage-calculator.html",
    "title": "CGPA to Percentage Calculator — All Universities | Calculatorcity",
    "meta": "Convert CGPA to percentage for all Indian universities. Supports CBSE (×9.5), VTU, Anna University, JNTU, Mumbai University and custom multipliers.",
    "h1": "CGPA to Percentage Calculator",
    "intro": "The CGPA to percentage calculator converts Indian board and university grades into percentage using commonly accepted formulas for CBSE, VTU, Anna University, JNTU Hyderabad, Mumbai University, and custom multipliers. It also includes a reverse percentage-to-CGPA tool, letter grade, and class estimate. Use it for resumes, campus placements, government job forms, scholarship applications, and university admission documents where percentage is requested.",
    "widget": """<section class="calc-widget">
      <div class="field-grid">
        <div class="calc-input-group"><label for="cgpa">CGPA (0 to 10)</label><input id="cgpa" type="number" min="0" max="10" step="0.01" value="8.2"></div>
        <div class="calc-input-group"><label for="university">University / Board</label><select id="university"><option value="cbse">CBSE × 9.5</option><option value="vtu">VTU × 10</option><option value="anna">Anna University × 10</option><option value="jntu">JNTU Hyderabad × 10</option><option value="mumbai">Mumbai University × 7.1 + 11</option><option value="custom">Custom multiplier</option></select></div>
        <div class="calc-input-group"><label for="custom-multiplier">Custom multiplier</label><input id="custom-multiplier" type="number" step="0.1" value="10"></div>
        <div class="calc-input-group"><label for="percentage-input">Reverse: percentage to CGPA</label><input id="percentage-input" type="number" step="0.1" value="78"></div>
      </div>
      <button class="calc-btn" id="calculate" type="button">Convert CGPA</button>
      <div class="calc-result show"><div class="result-grid"><div class="result-card highlight"><span class="result-value" id="percentage">0%</span><span class="result-label">Percentage</span></div><div class="result-card"><span class="result-value" id="letter">A</span><span class="result-label">Letter grade</span></div><div class="result-card"><span class="result-value" id="class">First Class</span><span class="result-label">Class</span></div><div class="result-card"><span class="result-value" id="reverse">0</span><span class="result-label">Reverse CGPA</span></div></div><div class="chart-container"><canvas id="calc-chart"></canvas></div></div>
    </section>""",
    "how_to": ["Enter your CGPA exactly as shown on your marksheet.", "Select your board or university formula from the dropdown.", "Use custom multiplier only if your official transcript or university circular gives a different conversion rule.", "Optionally enter a percentage to convert it back to CGPA for comparison.", "Use the output for forms only after checking the official conversion certificate requirements."],
    "formula_box": "CBSE: Percentage = CGPA × 9.5<br>VTU/JNTU/Anna: Percentage = CGPA × 10<br>Mumbai University: Percentage = CGPA × 7.1 + 11",
    "formula_text": "<p>CGPA conversion is not universal in India. CBSE has commonly used CGPA multiplied by 9.5 for older 10-point grading. Several technical universities use CGPA multiplied by 10, while Mumbai University uses a linear formula of CGPA multiplied by 7.1 plus 11 for many cases. Some institutions issue their own formula or conversion certificate, and that official document should override any generic calculator.</p><p>The calculator applies the selected formula, then maps percentage to a broad letter grade and class category. These labels are only indicative because universities define distinction, first class, second class, and pass class differently. For government jobs, PSU recruitment, foreign applications, or credential evaluation, attach the university formula or transcript wherever possible instead of relying only on a self-calculated number.</p>",
    "example": "<p>A student with 8.2 CGPA applying for a campus role with a ₹6,00,000 annual package may need percentage on the application form.</p><p>Under CBSE-style conversion, 8.2 × 9.5 = 77.9%. Under VTU-style conversion, 8.2 × 10 = 82%.</p><p><strong>The right answer depends on the institution’s official formula.</strong></p>",
    "reference_title": "CGPA to percentage comparison",
    "reference_headers": ["CGPA", "CBSE ×9.5", "VTU ×10", "Mumbai formula"],
    "reference_rows": [["10.0", "95.0%", "100.0%", "82.0%"], ["9.5", "90.25%", "95.0%", "78.45%"], ["9.0", "85.5%", "90.0%", "74.9%"], ["8.5", "80.75%", "85.0%", "71.35%"], ["8.0", "76.0%", "80.0%", "67.8%"], ["7.5", "71.25%", "75.0%", "64.25%"], ["7.0", "66.5%", "70.0%", "60.7%"], ["6.5", "61.75%", "65.0%", "57.15%"], ["6.0", "57.0%", "60.0%", "53.6%"], ["5.0", "47.5%", "50.0%", "46.5%"]],
    "sections": [("What is CGPA?", "<p>CGPA means Cumulative Grade Point Average. It summarizes performance across subjects or semesters on a grade scale, often 10 points in India. SGPA is Semester Grade Point Average and covers one semester, while CGPA aggregates multiple semesters. Colleges may calculate credits, grade points, backlogs, and improvement exams differently, so the official transcript remains the source of truth.</p>"), ("Using conversion for applications", "<p>For job applications, enter the formula requested by the recruiter. If the form asks for percentage but your university gives only CGPA, use the official formula from the university website, marksheet back page, or controller of examinations. For government jobs, a conversion certificate may be required if the advertisement says so.</p>")],
    "faqs": [("What is CGPA?", "CGPA is Cumulative Grade Point Average, a weighted or average grade measure across subjects or semesters."), ("Is 8 CGPA a good score?", "In many Indian colleges, 8 CGPA is considered strong, but competitiveness depends on branch, college, grading strictness, and recruiter cutoff."), ("Which formula does CBSE use?", "CBSE commonly used CGPA multiplied by 9.5 for converting 10-point CGPA to percentage."), ("How to convert CGPA for government jobs?", "Use the formula officially prescribed by your board or university and keep proof ready if the recruitment body asks for it."), ("What is the difference between CGPA and percentage?", "CGPA is a grade-point average, while percentage expresses marks out of 100. Conversion depends on institution rules.")],
    "notes": ["Always prefer the formula printed on your marksheet or official university conversion certificate.", "Recruiters may reject self-converted percentages if the advertisement requires official proof.", "Different universities can assign different percentages to the same CGPA.", "Backlogs, grace marks, and credit weighting can affect official CGPA even when raw marks look similar."],
    "script": """function convert(cgpa, uni) {
  if (uni === 'cbse') return cgpa * 9.5;
  if (uni === 'mumbai') return cgpa * 7.1 + 11;
  if (uni === 'custom') return cgpa * value('custom-multiplier');
  return cgpa * 10;
}
function grade(p) { return p >= 85 ? 'A+' : p >= 75 ? 'A' : p >= 65 ? 'B+' : p >= 55 ? 'B' : p >= 45 ? 'C' : 'Needs review'; }
function className(p) { return p >= 75 ? 'Distinction' : p >= 60 ? 'First Class' : p >= 50 ? 'Second Class' : p >= 40 ? 'Pass Class' : 'Below pass'; }
function calculate() {
  const cgpa = clamp(value('cgpa'), 0, 10);
  const uni = document.getElementById('university').value;
  const p = Math.min(100, convert(cgpa, uni));
  text('percentage', `${formatPlainNumber(p, 2)}%`);
  text('letter', grade(p));
  text('class', className(p));
  const reverseBase = value('percentage-input');
  const reverse = uni === 'mumbai' ? (reverseBase - 11) / 7.1 : reverseBase / (uni === 'cbse' ? 9.5 : (uni === 'custom' ? value('custom-multiplier') : 10));
  text('reverse', formatPlainNumber(reverse, 2));
  drawChart('calc-chart', 'bar', ['CBSE', 'VTU/JNTU', 'Mumbai', 'Selected'], [{ label: 'Percentage for entered CGPA', data: [convert(cgpa,'cbse'), convert(cgpa,'vtu'), convert(cgpa,'mumbai'), p], backgroundColor: ['#2563eb', '#16a34a', '#64748b', '#f97316'] }]);
}
bindCalculator(calculate);""",
})


PAGES.append({
    "file": "hra-exemption-calculator.html",
    "title": "HRA Exemption Calculator — HRA Tax Exemption India | Calculatorcity",
    "meta": "Free HRA exemption calculator India. Find your House Rent Allowance tax exemption under Section 10(13A). Supports metro and non-metro cities.",
    "h1": "HRA Exemption Calculator (Section 10-13A)",
    "intro": "The HRA exemption calculator estimates tax-free House Rent Allowance for salaried employees in India under Section 10(13A). Enter monthly basic salary plus DA, HRA received, rent paid, and city type to see all three statutory conditions side by side. The calculator identifies the minimum value, annual exemption, and taxable HRA so you can submit accurate rent declarations to your employer.",
    "widget": """<section class="calc-widget">
      <div class="field-grid">
        <div class="calc-input-group"><label for="basic">Basic salary + DA per month (₹)</label><div class="input-prefix"><span>₹</span><input id="basic" type="number" value="50000"></div></div>
        <div class="calc-input-group"><label for="hra">HRA received per month (₹)</label><div class="input-prefix"><span>₹</span><input id="hra" type="number" value="25000"></div></div>
        <div class="calc-input-group"><label for="rent">Rent paid per month (₹)</label><div class="input-prefix"><span>₹</span><input id="rent" type="number" value="30000"></div></div>
        <div class="calc-input-group"><label for="city">City</label><select id="city"><option value="metro">Metro (Delhi/Mumbai/Kolkata/Chennai)</option><option value="non-metro" selected>Non-metro</option></select></div>
      </div>
      <button class="calc-btn" id="calculate" type="button">Calculate HRA exemption</button>
      <div class="calc-result show"><div class="result-grid"><div class="result-card"><span class="result-value" id="condition1">₹0.00</span><span class="result-label">Actual HRA received</span></div><div class="result-card"><span class="result-value" id="condition2">₹0.00</span><span class="result-label">40% / 50% of salary</span></div><div class="result-card"><span class="result-value" id="condition3">₹0.00</span><span class="result-label">Rent minus 10% salary</span></div><div class="result-card highlight"><span class="result-value" id="exemption">₹0.00</span><span class="result-label">Annual HRA exemption</span></div><div class="result-card"><span class="result-value" id="taxable">₹0.00</span><span class="result-label">Taxable HRA</span></div></div><div class="chart-container"><canvas id="calc-chart"></canvas></div></div>
    </section>""",
    "how_to": ["Enter monthly basic salary plus DA for the period you paid rent.", "Enter monthly HRA received from your employer.", "Enter actual rent paid per month.", "Choose metro only for Delhi, Mumbai, Kolkata, or Chennai; other cities are non-metro for HRA rules.", "Calculate and use the lowest of the three conditions as the monthly exemption."],
    "formula_box": "HRA exemption = minimum of:<br>1. Actual HRA received<br>2. 50% of salary in metro or 40% in non-metro<br>3. Rent paid − 10% of salary",
    "formula_text": "<p>HRA exemption under Section 10(13A) is based on three values for the period during which rented accommodation is occupied. Salary generally means basic salary plus dearness allowance to the extent it forms part of retirement benefits, and turnover-based commission where applicable. The exemption is the least of actual HRA received, 50% of salary for specified metro cities or 40% for other places, and rent paid in excess of 10% of salary.</p><p>If rent paid is less than or equal to 10% of salary, the third condition becomes zero and no HRA exemption is available. If you live in your own house or do not actually pay rent, HRA is taxable. Employers may require rent receipts, rental agreement, landlord PAN where annual rent exceeds ₹1,00,000, and proof of payment before allowing exemption in payroll TDS.</p>",
    "example": "<p>Basic plus DA is ₹50,000 per month, HRA is ₹25,000, and rent is ₹30,000 in a non-metro city.</p><p>Actual HRA is ₹25,000, 40% of salary is ₹20,000, and rent minus 10% of salary is ₹25,000. Monthly exemption is the minimum: ₹20,000.</p><p><strong>Annual HRA exemption is ₹2,40,000 and taxable HRA is ₹60,000.</strong></p>",
    "reference_title": "HRA examples for Indian salaries",
    "reference_headers": ["Monthly salary", "Monthly HRA", "Rent", "City", "Monthly exemption"],
    "reference_rows": [["₹30,000", "₹12,000", "₹10,000", "Non-metro", "₹7,000"], ["₹40,000", "₹20,000", "₹18,000", "Metro", "₹14,000"], ["₹50,000", "₹25,000", "₹30,000", "Non-metro", "₹20,000"], ["₹60,000", "₹30,000", "₹35,000", "Metro", "₹29,000"], ["₹80,000", "₹40,000", "₹45,000", "Non-metro", "₹32,000"], ["₹1,00,000", "₹50,000", "₹60,000", "Metro", "₹50,000"], ["₹1,20,000", "₹60,000", "₹70,000", "Non-metro", "₹48,000"], ["₹1,50,000", "₹75,000", "₹90,000", "Metro", "₹75,000"]],
    "sections": [("Documents for HRA claims", "<p>Employers commonly ask for rent receipts, lease agreement, landlord name, address, and PAN if annual rent exceeds ₹1,00,000. Bank transfer proof is useful when rent is large. If you pay rent to parents, keep a genuine agreement, payment trail, and their tax reporting aligned. Artificial rent claims can be questioned during assessment.</p>")],
    "faqs": [("Can I claim HRA in the new tax regime?", "HRA exemption is generally not available under the new regime for salaried individuals. It is an old-regime exemption."), ("Which cities count as metro for HRA?", "For HRA, metro typically means Delhi, Mumbai, Kolkata, and Chennai. Other cities are treated as non-metro."), ("Is landlord PAN required?", "Employers generally require landlord PAN if annual rent exceeds ₹1,00,000."), ("Can I claim HRA while paying rent to parents?", "It may be possible if the arrangement is genuine, rent is actually paid, and parents report rental income where applicable."), ("What if rent is less than 10% of salary?", "Then the rent-minus-10% condition is zero or negative, so HRA exemption is not available.")],
    "notes": ["HRA exemption is an old-regime benefit; it is generally not allowed in the new regime.", "Metro for HRA means Delhi, Mumbai, Kolkata, and Chennai, not every large Indian city.", "Maintain rent receipts, agreement, and payment proof, especially for high rent claims.", "Landlord PAN is commonly required by employers when annual rent paid exceeds ₹1,00,000."],
    "script": """function calculate() {
  const basic = value('basic');
  const hra = value('hra');
  const rent = value('rent');
  const cityFactor = document.getElementById('city').value === 'metro' ? 0.5 : 0.4;
  const c1 = hra;
  const c2 = basic * cityFactor;
  const c3 = Math.max(0, rent - basic * 0.10);
  const monthly = Math.min(c1, c2, c3);
  const annual = monthly * 12;
  const taxable = Math.max(0, hra * 12 - annual);
  text('condition1', formatIndianNumber(c1));
  text('condition2', formatIndianNumber(c2));
  text('condition3', formatIndianNumber(c3));
  text('exemption', formatIndianNumber(annual));
  text('taxable', formatIndianNumber(taxable));
  drawChart('calc-chart', 'bar', ['Actual HRA', '40/50% salary', 'Rent - 10% salary', 'Exemption'], [{ label: 'Monthly amount', data: [c1, c2, c3, monthly], backgroundColor: ['#2563eb', '#64748b', '#16a34a', '#f97316'] }]);
}
bindCalculator(calculate);""",
})


# Additional page definitions are intentionally compact: each follows the same production template above.
PAGES.extend([
{
    "file": "ppf-calculator.html",
    "title": "PPF Calculator — Public Provident Fund Maturity | Calculatorcity",
    "meta": "Free PPF calculator India. Calculate your Public Provident Fund maturity amount. Shows year-wise balance for 15-year PPF account.",
    "h1": "PPF Calculator (Public Provident Fund)",
    "intro": "The PPF calculator estimates maturity value for a 15-year Public Provident Fund account in India. Enter yearly investment, interest rate, and deposit timing to see total deposits, interest earned, maturity amount, and estimated 80C tax saving. The year-wise table shows opening balance, deposit, annual interest, and closing balance so you can understand how a safe government-backed savings account compounds over time.",
    "widget": """<section class="calc-widget"><div class="field-grid"><div class="calc-input-group"><label for="investment">Yearly investment amount (₹)</label><div class="input-prefix"><span>₹</span><input id="investment" type="number" min="500" max="150000" value="150000"></div></div><div class="calc-input-group"><label for="rate">PPF interest rate (%)</label><input id="rate" type="number" step="0.1" value="7.1"></div><div class="calc-input-group"><label for="timing">Investment timing</label><select id="timing"><option value="beginning" selected>Beginning of year</option><option value="end">End of year</option></select></div></div><button class="calc-btn" id="calculate" type="button">Calculate PPF maturity</button><div class="calc-result show"><div class="result-grid"><div class="result-card highlight"><span class="result-value" id="maturity">₹0.00</span><span class="result-label">Maturity amount at 15 years</span></div><div class="result-card"><span class="result-value" id="invested">₹0.00</span><span class="result-label">Total invested</span></div><div class="result-card"><span class="result-value" id="interest">₹0.00</span><span class="result-label">Interest earned</span></div><div class="result-card"><span class="result-value" id="tax-saving">₹0.00</span><span class="result-label">80C tax saved at 30%</span></div></div><div class="chart-container"><canvas id="calc-chart"></canvas></div><div id="year-table" class="amortization-table"></div></div></section>""",
    "how_to": ["Enter annual deposit between ₹500 and ₹1,50,000.", "Use the current PPF rate or edit it for scenario planning.", "Select whether deposits are made at the beginning or end of each year.", "Calculate maturity value, total deposits, interest, and indicative tax saving.", "Review all 15 yearly rows to understand compounding and lock-in behavior."],
    "formula_box": "Opening balance + deposit earns annual PPF interest when deposited at year beginning.<br>Closing balance = Opening balance + deposit + interest",
    "formula_text": "<p>PPF interest is notified by the Government of India and compounded annually. In practical account calculations, monthly balances and deposit dates can matter, but for planning a yearly calculator is easier to understand. If investment timing is set to beginning of year, the annual deposit is added before interest. If timing is end of year, interest is calculated on the opening balance and the deposit is added after interest.</p><p>The account has a 15-year lock-in, but loan and partial withdrawal facilities become available after specified years. PPF follows EEE tax treatment: eligible contribution can qualify for Section 80C under the old regime, interest is tax-free, and maturity proceeds are tax-free. The calculator caps yearly investment at ₹1,50,000 because that is the normal annual deposit ceiling.</p>",
    "example": "<p>Investing ₹1,50,000 every year for 15 years at 7.1% from the beginning of each year deposits ₹22,50,000.</p><p>The estimated maturity amount is about ₹42,58,000, with interest of about ₹20,08,000.</p><p><strong>At a 30% tax slab, the annual 80C benefit can be worth up to ₹45,000 if the old regime is used.</strong></p>",
    "reference_title": "PPF maturity estimates at 7.1%",
    "reference_headers": ["Yearly deposit", "Total deposit", "Approx. maturity", "Interest earned"],
    "reference_rows": [["₹500", "₹7,500", "₹14,194", "₹6,694"], ["₹12,000", "₹1,80,000", "₹3,40,650", "₹1,60,650"], ["₹24,000", "₹3,60,000", "₹6,81,300", "₹3,21,300"], ["₹50,000", "₹7,50,000", "₹14,19,375", "₹6,69,375"], ["₹75,000", "₹11,25,000", "₹21,29,063", "₹10,04,063"], ["₹1,00,000", "₹15,00,000", "₹28,38,750", "₹13,38,750"], ["₹1,25,000", "₹18,75,000", "₹35,48,438", "₹16,73,438"], ["₹1,50,000", "₹22,50,000", "₹42,58,125", "₹20,08,125"]],
    "sections": [("PPF rules and withdrawals", "<p>PPF has a 15-year lock-in. Loans are generally available during the early years and partial withdrawals from later years subject to limits. After maturity, the account can be extended in blocks. This makes PPF useful for conservative long-term goals but unsuitable for emergency money.</p>"), ("PPF vs FD", "<p>PPF interest is tax-free and government-backed, while FD interest is taxable at slab rates. FDs offer flexible tenures and liquidity but can lose post-tax appeal for higher-bracket taxpayers. PPF has annual contribution limits and lock-in but stronger tax treatment under the old regime.</p>")],
    "faqs": [("What is PPF?", "PPF is Public Provident Fund, a government-backed long-term savings scheme with tax benefits."), ("What is the current PPF interest rate?", "The rate is notified quarterly by the government; this calculator defaults to 7.1% and lets you edit it."), ("Can I withdraw PPF before 15 years?", "Partial withdrawals and loans are allowed only under specified rules after certain years."), ("Is PPF interest taxable?", "PPF interest is tax-free under current rules."), ("Can I open PPF for my child?", "A parent or guardian can open a PPF account for a minor, subject to combined contribution rules.")],
    "notes": ["PPF rates are revised by government notification and can change every quarter.", "The annual deposit limit is ₹1,50,000 across accounts where applicable.", "80C benefit matters only if you use the old tax regime and have available limit.", "Deposit timing affects actual interest; early financial-year deposits usually earn more."],
    "script": """function calculate(){const annual=clamp(value('investment'),500,150000);const rate=value('rate')/100;const beginning=document.getElementById('timing').value==='beginning';let balance=0,invested=0,rows='',labels=[],dep=[],intData=[];for(let y=1;y<=15;y++){const opening=balance;let interest;if(beginning){balance+=annual;invested+=annual;interest=balance*rate;balance+=interest;}else{interest=balance*rate;balance+=interest+annual;invested+=annual;}labels.push(`Year ${y}`);dep.push(invested);intData.push(balance-invested);rows+=`<tr><td>${y}</td><td>${formatIndianNumber(opening)}</td><td>${formatIndianNumber(annual)}</td><td>${formatIndianNumber(interest)}</td><td>${formatIndianNumber(balance)}</td></tr>`;}text('maturity',`${formatIndianNumber(balance)} (${formatShortIndian(balance)})`);text('invested',formatIndianNumber(invested));text('interest',formatIndianNumber(balance-invested));text('tax-saving',formatIndianNumber(Math.min(annual,150000)*0.30));html('year-table','<table class="reference-table"><thead><tr><th>Year</th><th>Opening Balance</th><th>Deposit</th><th>Interest</th><th>Closing Balance</th></tr></thead><tbody>'+rows+'</tbody></table>');drawChart('calc-chart','bar',labels,[{label:'Cumulative invested',data:dep,backgroundColor:'#2563eb'},{label:'Interest accumulated',data:intData,backgroundColor:'#16a34a'}],{scales:{x:{stacked:true},y:{stacked:true}}});}bindCalculator(calculate);""",
},
{
    "file": "stamp-duty/index.html",
    "title": "Stamp Duty Calculator India — Property Registration | Calculatorcity",
    "meta": "Calculate stamp duty and registration charges for property purchase in India. State-wise rates for all major states including Andhra Pradesh, Telangana, Maharashtra.",
    "h1": "Stamp Duty Calculator India",
    "intro": "The stamp duty calculator estimates property registration cost in India using state-wise stamp duty and registration charge assumptions. Enter property value, state, property type, buyer gender, and new or resale status to calculate stamp duty, registration fee, and total registration outflow. It helps homebuyers compare Andhra Pradesh, Telangana, Maharashtra, Delhi, Karnataka, Tamil Nadu, Gujarat, and other state costs before budgeting the full purchase amount.",
    "widget": """<section class="calc-widget"><div class="field-grid"><div class="calc-input-group"><label for="property-value">Property value (₹)</label><div class="input-prefix"><span>₹</span><input id="property-value" type="number" value="7500000"></div></div><div class="calc-input-group"><label for="state">State</label><select id="state"></select></div><div class="calc-input-group"><label for="property-type">Property type</label><select id="property-type"><option value="residential" selected>Residential</option><option value="commercial">Commercial</option><option value="agricultural">Agricultural land</option></select></div><div class="calc-input-group"><label for="gender">Gender of buyer</label><select id="gender"><option value="male">Male</option><option value="female">Female</option><option value="joint">Joint</option></select></div><div class="calc-input-group"><label for="new-resale">New property / Resale</label><select id="new-resale"><option value="new" selected>New property</option><option value="resale">Resale</option></select></div></div><button class="calc-btn" id="calculate" type="button">Calculate stamp duty</button><div class="calc-result show"><div class="result-grid"><div class="result-card"><span class="result-value" id="stamp">₹0.00</span><span class="result-label">Stamp duty</span></div><div class="result-card"><span class="result-value" id="registration">₹0.00</span><span class="result-label">Registration charges</span></div><div class="result-card highlight"><span class="result-value" id="total">₹0.00</span><span class="result-label">Total registration cost</span></div><div class="result-card"><span class="result-value" id="rate-note">0%</span><span class="result-label">Rate used</span></div></div><div class="chart-container"><canvas id="calc-chart"></canvas></div></div></section>""",
    "how_to": ["Enter agreement value or market value, whichever is higher for registration purposes.", "Select the state where the property will be registered.", "Choose residential, commercial, or agricultural land because rates can differ.", "Select buyer gender to apply common women-buyer concessions where included.", "Calculate stamp duty, registration fee, and total cost before arranging funds."],
    "formula_box": "Stamp duty = Property value × state stamp rate<br>Registration charge = Property value × state registration rate<br>Total cost = Stamp duty + registration charge",
    "formula_text": "<p>Stamp duty is a state levy on property transfer documents. It is generally calculated on the higher of agreement value and government guidance value, circle rate, ready reckoner value, or market value depending on the state. Registration charges are separate and typically range around 0.5% to 4%. Several states offer lower stamp duty for women buyers, joint ownership, affordable housing, or specific property categories.</p><p>This calculator uses planning rates for major states and applies simple adjustments for commercial and agricultural selections. Actual duty can change due to municipal surcharges, metro cess, local body tax, rural/urban classification, property use, buyer category, and notification date. For execution, always verify on the state registration department portal or with the sub-registrar before paying challans.</p>",
    "example": "<p>A residential property worth ₹75,00,000 in Andhra Pradesh at 5% stamp duty and 1.5% registration charge has stamp duty of ₹3,75,000 and registration charge of ₹1,12,500.</p><p><strong>Total registration cost is about ₹4,87,500 before any local surcharge or document charges.</strong></p>",
    "reference_title": "Stamp duty comparison across major states",
    "reference_headers": ["State", "Stamp duty", "Registration", "Women concession"],
    "reference_rows": [["Andhra Pradesh", "5%", "1.5%", "No broad standard concession"], ["Telangana", "4%", "0.5%", "Varies by property"], ["Maharashtra", "5%", "1%", "Often lower for women"], ["Karnataka", "5%", "1%", "Limited cases"], ["Delhi", "6%", "1%", "4% stamp for women"], ["Tamil Nadu", "7%", "4%", "No broad standard concession"], ["Gujarat", "4.9%", "1%", "Concessions vary"], ["Rajasthan", "6%", "1%", "Lower for women in many cases"], ["Uttar Pradesh", "7%", "1%", "Rebate for women up to limits"], ["West Bengal", "6%", "1%", "Urban/rural variation"]],
    "sections": [("Budgeting for property registration", "<p>Stamp duty is usually one of the largest upfront costs after down payment. Banks may not fund it fully, so buyers should keep separate liquidity for duty, registration, franking, legal verification, brokerage, society transfer, and moving costs. Under-budgeting registration cost can delay sale deed execution.</p>")],
    "faqs": [("What is stamp duty?", "Stamp duty is a state tax paid on legal documents that record property transfer."), ("Is registration charge separate?", "Yes. Registration charge is paid for registering the document with the state registration department."), ("Do women buyers get lower duty?", "Many states give concessions to women buyers, but rates and limits vary."), ("Which value is used for duty?", "States usually use the higher of agreement value and official guidance/circle/market value."), ("Can stamp duty be paid online?", "Most states provide e-stamp or online challan facilities, but process varies.")],
    "notes": ["Andhra Pradesh commonly uses 5% stamp duty plus 1.5% registration for many property transfers.", "State rates change through notifications; verify before executing the sale deed.", "Circle value or market value can override the agreement value for duty calculation.", "Local surcharges, transfer duty, mutation fees, and document writer charges are not fully modeled here."],
    "script": """const rates={'Andhra Pradesh':[5,1.5,5],'Telangana':[4,0.5,4],'Maharashtra':[5,1,3],'Karnataka':[5,1,5],'Delhi':[6,1,4],'Tamil Nadu':[7,4,7],'Gujarat':[4.9,1,4.9],'Rajasthan':[6,1,5],'Uttar Pradesh':[7,1,6],'West Bengal':[6,1,6],'Kerala':[8,2,8],'Haryana':[7,1,5],'Punjab':[6,1,5],'Madhya Pradesh':[7.5,3,7.5],'Bihar':[6,2,5.7],'Odisha':[5,2,4],'Assam':[6,1,5],'Goa':[4,3,4],'Other States / UTs':[6,1,5]};const st=document.getElementById('state');Object.keys(rates).forEach(s=>st.add(new Option(s,s)));st.value='Andhra Pradesh';function calculate(){const v=value('property-value');let [stampRate,regRate,womenRate]=rates[st.value];if(document.getElementById('gender').value==='female')stampRate=womenRate;if(document.getElementById('gender').value==='joint')stampRate=(stampRate+womenRate)/2;if(document.getElementById('property-type').value==='commercial')stampRate+=1;if(document.getElementById('property-type').value==='agricultural')stampRate=Math.max(1,stampRate-1);const stamp=v*stampRate/100,reg=v*regRate/100,total=stamp+reg;text('stamp',formatIndianNumber(stamp));text('registration',formatIndianNumber(reg));text('total',formatIndianNumber(total));text('rate-note',`${formatPlainNumber(stampRate,2)}% + ${formatPlainNumber(regRate,2)}%`);drawChart('calc-chart','pie',['Stamp duty','Registration charge'],[{data:[stamp,reg],backgroundColor:['#f97316','#2563eb']}]);}bindCalculator(calculate);""",
},
{
    "file": "car-loan-emi-calculator.html",
    "title": "Car Loan EMI Calculator India — Auto Loan EMI | Calculatorcity",
    "meta": "Free car loan EMI calculator India. Calculate monthly car loan EMI with down payment, interest rate and tenure. Get full amortization schedule.",
    "h1": "Car Loan EMI Calculator",
    "intro": "The car loan EMI calculator estimates monthly auto loan payments in India after accounting for down payment, interest rate, and tenure. Enter car price or loan amount, choose down payment as rupees or percentage, and select a tenure from 12 to 84 months. The output shows loan amount, EMI, total interest, total payment, and a year-wise amortization schedule for comparing bank and dealer finance offers.",
    "widget": """<section class="calc-widget"><div class="field-grid"><div class="calc-input-group"><label for="car-price">Car price / loan basis (₹)</label><div class="input-prefix"><span>₹</span><input id="car-price" type="number" value="1000000"></div></div><div class="calc-input-group"><label for="down-payment">Down payment</label><input id="down-payment" type="number" value="200000"></div><div class="calc-input-group"><label for="down-mode">Down payment mode</label><select id="down-mode"><option value="amount" selected>₹ amount</option><option value="percent">% of car price</option></select></div><div class="calc-input-group"><label for="rate">Annual interest rate (%)</label><input id="rate" type="number" step="0.1" value="9"></div><div class="calc-input-group"><label for="tenure">Loan tenure (months)</label><select id="tenure"><option>12</option><option>24</option><option>36</option><option>48</option><option selected>60</option><option>72</option><option>84</option></select></div></div><button class="calc-btn" id="calculate" type="button">Calculate car loan EMI</button><div class="calc-result show"><div class="result-grid"><div class="result-card"><span class="result-value" id="loan">₹0.00</span><span class="result-label">Loan amount after down payment</span></div><div class="result-card highlight"><span class="result-value" id="emi">₹0.00</span><span class="result-label">Monthly EMI</span></div><div class="result-card"><span class="result-value" id="interest">₹0.00</span><span class="result-label">Total interest</span></div><div class="result-card"><span class="result-value" id="payment">₹0.00</span><span class="result-label">Total payment</span></div><div class="result-card"><span class="result-value" id="down-percent">0%</span><span class="result-label">Down payment %</span></div></div><div class="chart-container"><canvas id="calc-chart"></canvas></div><div id="amortization" class="amortization-table"></div></div></section>""",
    "how_to": ["Enter the car price or loan basis amount.", "Enter down payment as rupees or select percentage mode.", "Set annual car loan interest rate from your bank or dealer quote.", "Choose tenure in months.", "Calculate EMI and review total interest plus year-wise repayment."],
    "formula_box": "Loan amount = Car price − down payment<br>EMI = P × r × (1 + r)<sup>n</sup> / ((1 + r)<sup>n</sup> − 1)",
    "formula_text": "<p>A car loan is an amortizing loan similar to other retail loans. The principal is the financed amount after down payment. The annual rate is converted to a monthly rate and applied across the selected number of monthly instalments. Each EMI includes interest on the outstanding balance plus a principal component. Early EMIs contain more interest because the balance is higher.</p><p>Indian car loans often include processing fee, hypothecation, documentation charges, bundled insurance, extended warranty, and dealer discounts. This calculator focuses on EMI and interest. When comparing offers, check the final on-road price, down payment, flat vs reducing rate wording, foreclosure charges, late-payment fees, and whether accessories or insurance are being financed into the loan.</p>",
    "example": "<p>For a ₹10,00,000 car with ₹2,00,000 down payment, the loan amount is ₹8,00,000.</p><p>At 9% for 60 months, EMI is about ₹16,607 and total interest is about ₹1,96,420.</p><p><strong>Total paid to the lender is about ₹9,96,420 excluding processing fee.</strong></p>",
    "reference_title": "EMI comparison at 9% for 60 months",
    "reference_headers": ["Car price", "20% down payment", "Loan amount", "Approx. EMI"],
    "reference_rows": [["₹5L", "₹1L", "₹4L", "₹8,303"], ["₹8L", "₹1.6L", "₹6.4L", "₹13,285"], ["₹10L", "₹2L", "₹8L", "₹16,607"], ["₹12L", "₹2.4L", "₹9.6L", "₹19,928"], ["₹15L", "₹3L", "₹12L", "₹24,910"], ["₹20L", "₹4L", "₹16L", "₹33,214"], ["₹25L", "₹5L", "₹20L", "₹41,517"], ["₹30L", "₹6L", "₹24L", "₹49,821"]],
    "sections": [("Down payment strategy", "<p>A higher down payment lowers EMI and total interest, but it also uses liquid savings. For Indian buyers, a practical approach is to avoid stretching EMI beyond comfortable monthly cash flow after fuel, parking, maintenance, insurance renewal, and annual service costs.</p>")],
    "faqs": [("What is a good car loan tenure?", "Many borrowers choose 3 to 5 years. Longer tenure lowers EMI but increases total interest."), ("Is 100% car finance available?", "Some lenders may finance high percentages for eligible borrowers, but margin requirements vary."), ("Can I prepay a car loan?", "Yes, subject to lender foreclosure or part-payment rules and charges."), ("What interest rate is normal for car loans?", "Rates often fall around 7% to 12% depending on lender, borrower profile, vehicle, and market conditions."), ("Does down payment reduce EMI?", "Yes. A larger down payment reduces financed principal and therefore EMI and interest.")],
    "notes": ["Check whether the quoted rate is reducing-balance EMI rate, not a flat rate.", "Dealer finance can bundle insurance or accessories; compare with bank approval separately.", "Hypothecation removal after loan closure requires RTO and lender documentation.", "Used-car loan rates are often higher and tenure may be shorter than new-car loans."],
    "script": """function calculate(){const price=value('car-price');let down=value('down-payment');if(document.getElementById('down-mode').value==='percent')down=price*down/100;down=Math.min(price,down);const loan=Math.max(0,price-down);const months=Number(document.getElementById('tenure').value);const rate=value('rate');const emi=emiAmount(loan,rate,months);const payment=emi*months;const interest=Math.max(0,payment-loan);text('loan',formatIndianNumber(loan));text('emi',formatIndianNumber(emi));text('interest',formatIndianNumber(interest));text('payment',formatIndianNumber(payment));text('down-percent',`${formatPlainNumber(price?down/price*100:0,1)}%`);drawChart('calc-chart','pie',['Down payment','Principal financed','Total interest'],[{data:[down,loan,interest],backgroundColor:['#16a34a','#2563eb','#f97316']}]);const rows=amortizationRows(loan,rate,months);html('amortization','<table class="reference-table"><thead><tr><th>Year</th><th>Opening Balance</th><th>Principal Paid</th><th>Interest Paid</th><th>Closing Balance</th></tr></thead><tbody>'+rows.map(r=>`<tr><td>Year ${r.year}</td><td>${formatIndianNumber(r.opening)}</td><td>${formatIndianNumber(r.principalPaid)}</td><td>${formatIndianNumber(r.interestPaid)}</td><td>${formatIndianNumber(r.closing)}</td></tr>`).join('')+'</tbody></table>');}bindCalculator(calculate);""",
},
{
    "file": "ap-electricity-bill-calculator.html",
    "title": "AP Electricity Bill Calculator — APSPDCL & APEPDCL | Calculatorcity",
    "meta": "Calculate Andhra Pradesh electricity bill online. Supports APSPDCL and APEPDCL tariff slabs for domestic consumers. Free and accurate AP electricity bill calculator.",
    "h1": "Andhra Pradesh Electricity Bill Calculator",
    "intro": "The AP electricity bill calculator estimates monthly power bills for Andhra Pradesh consumers served by APSPDCL and APEPDCL. Enter discom, category, connected load, units consumed, and fuel adjustment charge to calculate fixed charges, slab-wise energy charges, electricity duty, and total bill. The domestic tariff uses APERC-style telescopic slabs and keeps a clear disclaimer because official tariff orders and FPPCA adjustments can change.",
    "widget": """<section class="calc-widget"><div class="field-grid"><div class="calc-input-group"><label for="discom">Discom</label><select id="discom"><option>APSPDCL (South)</option><option>APEPDCL (North/East)</option></select></div><div class="calc-input-group"><label for="category">Consumer category</label><select id="category"><option value="domestic" selected>Domestic</option><option value="commercial">Commercial</option><option value="agricultural">Agricultural</option><option value="industrial">Industrial</option></select></div><div class="calc-input-group"><label for="units">Units consumed (kWh)</label><input id="units" type="number" value="180"></div><div class="calc-input-group"><label for="load">Connected load (kW)</label><input id="load" type="number" step="0.5" value="3"></div><div class="calc-input-group"><label for="fppca">Fuel adjustment / FPPCA (₹ per unit)</label><input id="fppca" type="number" step="0.01" value="0"></div></div><button class="calc-btn" id="calculate" type="button">Calculate AP electricity bill</button><div class="calc-result show"><div class="result-grid"><div class="result-card"><span class="result-value" id="fixed">₹0.00</span><span class="result-label">Fixed charges</span></div><div class="result-card"><span class="result-value" id="energy">₹0.00</span><span class="result-label">Energy charges</span></div><div class="result-card"><span class="result-value" id="duty">₹0.00</span><span class="result-label">Electricity duty</span></div><div class="result-card highlight"><span class="result-value" id="total">₹0.00</span><span class="result-label">Total bill amount</span></div></div><div class="chart-container"><canvas id="calc-chart"></canvas></div><div id="slab-breakup" class="amortization-table"></div></div></section>""",
    "how_to": ["Select APSPDCL or APEPDCL based on your service area.", "Choose domestic, commercial, agricultural, or industrial category.", "Enter monthly units consumed from your meter reading or bill.", "Enter connected load and any FPPCA shown in the latest bill if applicable.", "Calculate fixed charge, energy charge by slab, duty, and estimated total bill."],
    "formula_box": "Total bill = fixed charge + slab-wise energy charges + FPPCA + electricity duty<br>Domestic slabs are telescopic, so each block of units is charged at its own rate.",
    "formula_text": "<p>Andhra Pradesh domestic billing uses telescopic slabs for LT domestic consumers. This means the first block of units is charged at the first slab rate, the next block at the next slab rate, and so on. Fixed charge is calculated using connected load in kW. Electricity duty and fuel/power purchase cost adjustment can be added as separate line items depending on the tariff order and monthly adjustment.</p><p>The calculator uses the commonly cited APERC domestic slab structure of 0-30 units at ₹1.90, 31-75 at ₹3.00, 76-125 at ₹4.50, 126-225 at ₹6.00, 226-400 at ₹8.75, and above 400 at ₹9.75. Agricultural, commercial, and industrial modes use simplified planning rates. For official billing, check the latest tariff order and your discom bill because subsidies, arrears, true-up, and FPPCA can alter the final amount.</p>",
    "example": "<p>A domestic consumer in Vijayawada using 180 units with 3 kW load pays fixed charges of about ₹30.</p><p>Energy charge is calculated across slabs up to 180 units, then electricity duty and FPPCA are added.</p><p><strong>The calculator shows each slab so the consumer can compare it with the APSPDCL or APEPDCL bill.</strong></p>",
    "reference_title": "AP domestic tariff slabs used",
    "reference_headers": ["Monthly units", "Rate per unit", "Billing method"],
    "reference_rows": [["0-30", "₹1.90", "Telescopic"], ["31-75", "₹3.00", "Telescopic"], ["76-125", "₹4.50", "Telescopic"], ["126-225", "₹6.00", "Telescopic"], ["226-400", "₹8.75", "Telescopic"], [">400", "₹9.75", "Telescopic"], ["Fixed charge", "₹10/kW/month", "Domestic estimate"], ["Electricity duty", "₹0.06/unit", "Planning estimate"]],
    "sections": [("Reading your AP electricity meter", "<p>Read the current kWh number and subtract the previous bill reading to estimate units. Smart meters and online portals can show consumption history. If the bill is estimated, reconcile it when actual reading is captured. LT supply is common for homes and small shops, while HT supply applies to larger contracted demand consumers.</p>"), ("Reducing AP electricity bill", "<p>High-slab units are expensive. Efficient fans, inverter ACs, correct thermostat settings, LED lighting, solar water heating, and shifting heavy daytime use where practical can reduce monthly units. Consumers above 500 units should check whether smart-meter time-of-day options or rooftop solar net metering are relevant under current rules.</p>")],
    "faqs": [("How is APSPDCL bill calculated?", "It combines fixed charges, slab-wise energy charges, duty, FPPCA or adjustments, arrears, and subsidies where applicable."), ("What are current AP electricity slab rates?", "This page uses APERC-style domestic slabs starting at ₹1.90/unit and going up to ₹9.75/unit; verify latest official tariff order."), ("How to pay APSPDCL bill online?", "You can pay through the official discom website, app, authorized payment partners, or supported UPI/banking channels."), ("What is the difference between APSPDCL and APEPDCL?", "APSPDCL serves southern/central areas, while APEPDCL serves northern and eastern coastal districts."), ("How to apply for new connection in AP?", "Apply through the relevant discom portal or customer service center with identity, address, ownership/occupancy proof, load requirement, and fees.")],
    "notes": ["AP tariff rates are governed by APERC orders; verify the latest PDF before relying on a bill estimate.", "FPPCA, true-up charges, arrears, subsidies, and meter rent can change the actual bill.", "Domestic tariff is telescopic; commercial and industrial categories use different rates.", "BPL, agriculture, rooftop solar, and government subsidy cases may not match a standard estimate."],
    "script": """const domestic=[[30,1.90],[75,3.00],[125,4.50],[225,6.00],[400,8.75],[Infinity,9.75]];function slab(units,slabs){let prev=0,total=0,rows='';for(const [limit,rate] of slabs){if(units>prev){const used=Math.min(units,limit)-prev;const charge=used*rate;total+=charge;rows+=`<tr><td>${prev+1}-${limit===Infinity?'Above':limit}</td><td>${formatPlainNumber(used,0)}</td><td>₹${rate.toFixed(2)}</td><td>${formatIndianNumber(charge)}</td></tr>`;prev=limit;}}return{total,rows};}function calculate(){const units=value('units'),load=value('load'),cat=document.getElementById('category').value;let fixed=load*10,energy=0,rows='';if(cat==='domestic'){const s=slab(units,domestic);energy=s.total;rows=s.rows;}else if(cat==='commercial'){fixed=load*75;const s=slab(units,[[50,5.40],[100,7.65],[300,9.05],[500,9.60],[Infinity,10.15]]);energy=s.total;rows=s.rows;}else if(cat==='industrial'){fixed=load*80;energy=units*7.80;rows=`<tr><td>All units</td><td>${units}</td><td>₹7.80</td><td>${formatIndianNumber(energy)}</td></tr>`;}else{fixed=0;energy=units*0;rows=`<tr><td>Agricultural subsidy category</td><td>${units}</td><td>Varies</td><td>${formatIndianNumber(0)}</td></tr>`;}const fppca=units*value('fppca');const duty=units*0.06;const total=fixed+energy+fppca+duty;text('fixed',formatIndianNumber(fixed));text('energy',formatIndianNumber(energy));text('duty',formatIndianNumber(duty));text('total',formatIndianNumber(total));html('slab-breakup','<table class="reference-table"><thead><tr><th>Slab</th><th>Units</th><th>Rate</th><th>Charge</th></tr></thead><tbody>'+rows+`<tr><th>FPPCA</th><td>${units}</td><td>${formatIndianNumber(value('fppca'))}/unit</td><td>${formatIndianNumber(fppca)}</td></tr></tbody></table>`);drawChart('calc-chart','pie',['Fixed','Energy','FPPCA','Duty'],[{data:[fixed,energy,fppca,duty],backgroundColor:['#64748b','#f97316','#2563eb','#16a34a']}]);}bindCalculator(calculate);""",
},
{
    "file": "tds-calculator.html",
    "title": "TDS Calculator India — Tax Deducted at Source | Calculatorcity",
    "meta": "Free TDS calculator India. Calculate TDS on salary, rent, professional fees, and contracts. Shows TDS rates under all major sections.",
    "h1": "TDS Calculator India",
    "intro": "The TDS calculator estimates tax deducted at source in India for salary, rent, professional fees, contractor payments, FD interest, commission, and property purchase. Select payment type, amount, PAN availability, and recipient type where relevant to see TDS rate, section number, TDS amount, and net payment. It includes important thresholds and current rate notes for common FY 2024-25 and later compliance use cases.",
    "widget": """<section class="calc-widget"><div class="field-grid"><div class="calc-input-group"><label for="payment-type">Payment type</label><select id="payment-type"><option value="salary">Salary - Section 192</option><option value="rent">Rent above threshold - Section 194IB</option><option value="professional">Professional fees - Section 194J</option><option value="contractor">Contractor payment - Section 194C</option><option value="fd">Interest on FD - Section 194A</option><option value="commission">Commission - Section 194H</option><option value="property">Property purchase - Section 194IA</option></select></div><div class="calc-input-group"><label for="amount">Payment amount (₹)</label><div class="input-prefix"><span>₹</span><input id="amount" type="number" value="100000"></div></div><div class="calc-input-group"><label for="pan">PAN</label><select id="pan"><option value="yes" selected>Available</option><option value="no">Not available</option></select></div><div class="calc-input-group"><label for="recipient">Contractor recipient type</label><select id="recipient"><option value="individual">Individual / HUF</option><option value="company">Company / others</option></select></div></div><button class="calc-btn" id="calculate" type="button">Calculate TDS</button><div class="calc-result show"><div class="result-grid"><div class="result-card"><span class="result-value" id="section">-</span><span class="result-label">Section number</span></div><div class="result-card"><span class="result-value" id="rate">0%</span><span class="result-label">TDS rate used</span></div><div class="result-card highlight"><span class="result-value" id="tds">₹0.00</span><span class="result-label">TDS amount</span></div><div class="result-card"><span class="result-value" id="net">₹0.00</span><span class="result-label">Net payment after TDS</span></div></div><div class="chart-container"><canvas id="calc-chart"></canvas></div><p class="mini-note" id="tds-note"></p></div></section>""",
    "how_to": ["Select the payment category and Income-tax section.", "Enter gross payment amount in rupees.", "Choose whether valid PAN is available.", "For contractor payments, select individual/HUF or company/other recipient.", "Calculate TDS amount and net payable amount before accounting entry or payment."],
    "formula_box": "TDS = Payment amount × TDS rate<br>Net payment = Payment amount − TDS<br>No PAN: higher of applicable rate, rate in force, or 20% in many cases",
    "formula_text": "<p>TDS is deducted at the time of credit or payment depending on the section. Each section has its own rate, threshold, deductor category, and timing rule. For example, professional fees under Section 194J commonly use 10%, contractor payments under Section 194C use 1% for individual/HUF and 2% for others, and property purchase under Section 194IA uses 1% when consideration crosses ₹50,00,000.</p><p>If PAN is not furnished, Section 206AA can require deduction at a higher rate, commonly 20%, subject to section-specific limits. Salary TDS under Section 192 is not a flat rate; it is based on estimated annual tax after deductions and regime selection. This calculator uses simplified current-rate assumptions for planning and should be cross-checked with the Income-tax Act, rules, and latest Finance Act changes before filing returns.</p>",
    "example": "<p>A company pays professional fees of ₹1,00,000 to a resident consultant with PAN.</p><p>Section 194J TDS at 10% is ₹10,000, so net payment is ₹90,000.</p><p><strong>If PAN is not available, the calculator applies 20% and TDS becomes ₹20,000.</strong></p>",
    "reference_title": "Major TDS sections, rates, and thresholds",
    "reference_headers": ["Section", "Payment", "Rate", "Common threshold"],
    "reference_rows": [["192", "Salary", "Slab based", "Taxable salary"], ["194IB", "Rent by individual/HUF", "2% current; 5% before change", "Above ₹50,000/month"], ["194J", "Professional fees", "10%", "₹50,000/year"], ["194C", "Contractor", "1% / 2%", "₹30,000 single or ₹1,00,000 aggregate"], ["194A", "Bank interest", "10%", "₹40,000 non-senior"], ["194H", "Commission", "5%", "₹15,000/year"], ["194IA", "Property purchase", "1%", "₹50,00,000"], ["194M", "Payments by individual/HUF", "2%", "₹50,00,000 aggregate"]],
    "sections": [("TDS compliance context", "<p>Deductors must deposit TDS on time, file TDS returns, and issue certificates such as Form 16, Form 16A, or Form 16B. Deductees should verify credits in Form 26AS and AIS. Mismatched PAN, wrong section, delayed deposit, or incorrect challan details can create credit issues during ITR filing.</p>")],
    "faqs": [("What is TDS?", "TDS is tax deducted at source from specified payments and deposited with the government by the deductor."), ("Is TDS final tax?", "No. It is a tax credit. Final tax depends on total income and return calculation."), ("What happens if PAN is not available?", "A higher rate, often 20%, may apply under Section 206AA."), ("Is TDS deducted on rent?", "Yes, if rent crosses applicable thresholds and conditions under 194I or 194IB apply."), ("How do I claim TDS credit?", "Report income and claim TDS credit in the income tax return using Form 26AS/AIS and TDS certificates.")],
    "notes": ["Section 194IB rate was reduced from 5% to 2% with effect from 1 October 2024; check payment period.", "No-PAN higher deduction can apply under Section 206AA.", "Thresholds and rates can change through Finance Acts, so verify for the exact financial year.", "TDS credit depends on correct PAN, TAN, challan, return filing, and statement matching."],
    "script": """const slabNew=[[0,300000,0],[300000,700000,0.05],[700000,1000000,0.10],[1000000,1200000,0.15],[1200000,1500000,0.20],[1500000,Infinity,0.30]];function data(){const t=document.getElementById('payment-type').value;const rec=document.getElementById('recipient').value;if(t==='salary')return['192','Slab based',0,'Estimated annual salary tax divided by payment cycle'];if(t==='rent')return['194IB','2%',0.02,'Current 194IB rate; older 5% may apply before 1 Oct 2024'];if(t==='professional')return['194J','10%',0.10,'Professional fees'];if(t==='contractor')return['194C',rec==='individual'?'1%':'2%',rec==='individual'?0.01:0.02,'Contractor payment'];if(t==='fd')return['194A','10%',0.10,'FD interest threshold applies'];if(t==='commission')return['194H','5%',0.05,'Commission or brokerage'];return['194IA','1%',0.01,'Property above ₹50 lakh'];}function calculate(){const amount=value('amount');let [sec,label,rate,note]=data();if(sec==='192'){const taxable=Math.max(0,amount-75000);rate=taxable<=700000?0:slabTax(taxable,slabNew)*1.04/Math.max(1,amount);label=`${formatPlainNumber(rate*100,2)}% effective`;}if(document.getElementById('pan').value==='no')rate=Math.max(rate,0.20);const tds=amount*rate;const net=amount-tds;text('section',sec);text('rate',`${formatPlainNumber(rate*100,2)}%`);text('tds',formatIndianNumber(tds));text('net',formatIndianNumber(net));text('tds-note',note);drawChart('calc-chart','pie',['Net payment','TDS'],[{data:[net,tds],backgroundColor:['#16a34a','#f97316']}]);}bindCalculator(calculate);""",
},
{
    "file": "nps-calculator.html",
    "title": "NPS Calculator — National Pension Scheme Returns | Calculatorcity",
    "meta": "Free NPS calculator India. Calculate National Pension Scheme corpus and monthly pension at retirement. Shows expected annuity and lump sum.",
    "h1": "NPS Calculator (National Pension Scheme)",
    "intro": "The NPS calculator estimates retirement corpus and monthly pension from National Pension System contributions in India. Enter current age, retirement age, monthly contribution, expected return, annuity rate, and annuity purchase percentage to see total corpus, compulsory annuity amount, lump sum withdrawal, and monthly pension. It helps compare NPS with EPF, PPF, and mutual fund SIPs for long-term retirement planning.",
    "widget": """<section class="calc-widget"><div class="field-grid"><div class="calc-input-group"><label for="age">Current age</label><input id="age" type="number" value="30"></div><div class="calc-input-group"><label for="retirement">Retirement age</label><input id="retirement" type="number" value="60"></div><div class="calc-input-group"><label for="contribution">Monthly NPS contribution (₹)</label><div class="input-prefix"><span>₹</span><input id="contribution" type="number" value="10000"></div></div><div class="calc-input-group"><label for="return">Expected annual return (%)</label><input id="return" type="number" step="0.1" value="10"></div><div class="calc-input-group"><label for="annuity-rate">Annuity rate (%)</label><input id="annuity-rate" type="number" step="0.1" value="6"></div><div class="calc-input-group"><label for="annuity-percent">Annuity purchase (%)</label><input id="annuity-percent" type="number" value="40"></div></div><button class="calc-btn" id="calculate" type="button">Calculate NPS corpus</button><div class="calc-result show"><div class="result-grid"><div class="result-card highlight"><span class="result-value" id="corpus">₹0.00</span><span class="result-label">Corpus at retirement</span></div><div class="result-card"><span class="result-value" id="annuity">₹0.00</span><span class="result-label">Amount for annuity</span></div><div class="result-card"><span class="result-value" id="lump">₹0.00</span><span class="result-label">Lump sum withdrawal</span></div><div class="result-card"><span class="result-value" id="pension">₹0.00</span><span class="result-label">Monthly pension</span></div></div><div class="chart-container"><canvas id="calc-chart"></canvas></div></div></section>""",
    "how_to": ["Enter current age and planned retirement age.", "Enter monthly NPS contribution.", "Set expected annual return based on asset allocation assumptions.", "Set annuity rate and annuity purchase percentage.", "Calculate retirement corpus, lump sum, annuity purchase amount, and monthly pension."],
    "formula_box": "NPS corpus = monthly contribution future value<br>Annuity amount = corpus × annuity percentage<br>Monthly pension = annuity amount × annuity rate / 12",
    "formula_text": "<p>NPS accumulation works like a market-linked monthly investment. Contributions are invested into pension fund schemes based on chosen asset allocation, and returns compound until retirement. The calculator converts annual return to a monthly rate and compounds every monthly contribution to retirement age. It then splits the final corpus into annuity purchase and lump sum withdrawal based on the selected annuity percentage.</p><p>At normal exit, many NPS subscribers must use at least 40% of accumulated corpus to buy an annuity, while the remaining amount can be withdrawn as lump sum subject to prevailing rules. The annuity rate is not guaranteed by NPS during accumulation; it depends on annuity providers and product options at retirement. Pension received from annuity is generally taxable in the year of receipt.</p>",
    "example": "<p>A 30-year-old investing ₹10,000 per month until age 60 at 10% expected return can build a corpus of about ₹2.28 crore.</p><p>If 40% is used for annuity at 6%, monthly pension is about ₹45,600 and lump sum is about ₹1.37 crore.</p><p><strong>Changing return or annuity rate materially changes the pension estimate.</strong></p>",
    "reference_title": "NPS monthly contribution scenarios at 10%",
    "reference_headers": ["Monthly contribution", "20 years", "25 years", "30 years", "35 years"],
    "reference_rows": [["₹2,000", "₹15.3L", "₹26.8L", "₹45.6L", "₹75.9L"], ["₹5,000", "₹38.3L", "₹67.0L", "₹1.14Cr", "₹1.90Cr"], ["₹10,000", "₹76.6L", "₹1.34Cr", "₹2.28Cr", "₹3.79Cr"], ["₹15,000", "₹1.15Cr", "₹2.01Cr", "₹3.42Cr", "₹5.69Cr"], ["₹20,000", "₹1.53Cr", "₹2.68Cr", "₹4.56Cr", "₹7.59Cr"], ["₹25,000", "₹1.91Cr", "₹3.35Cr", "₹5.70Cr", "₹9.49Cr"], ["₹30,000", "₹2.30Cr", "₹4.02Cr", "₹6.84Cr", "₹11.38Cr"], ["₹50,000", "₹3.83Cr", "₹6.70Cr", "₹11.40Cr", "₹18.97Cr"]],
    "sections": [("Tier 1 vs Tier 2", "<p>NPS Tier 1 is the retirement account with tax benefits and withdrawal restrictions. Tier 2 is more flexible and works like an optional investment account, but tax benefits are limited to specified cases. Most retirement planning discussions focus on Tier 1 because of the lock-in and tax structure.</p>"), ("NPS tax benefits", "<p>Employee contribution may qualify under Section 80CCD within 80C limits, and Section 80CCD(1B) provides an additional old-regime deduction up to ₹50,000. Employer contribution has separate treatment. New-regime rules differ, so verify your regime before assuming tax savings.</p>")],
    "faqs": [("What is NPS?", "NPS is the National Pension System, a regulated retirement savings framework in India."), ("What is the tax benefit on NPS?", "Old-regime taxpayers may use 80CCD deductions, including an additional ₹50,000 under 80CCD(1B)."), ("When can I withdraw NPS?", "Normal exit is at retirement age, with partial and premature withdrawal rules subject to PFRDA regulations."), ("What is annuity in NPS?", "An annuity is a pension product bought with part of the corpus to provide periodic pension."), ("Is NPS safe?", "NPS is regulated, but returns are market-linked and depend on asset allocation and pension fund performance.")],
    "notes": ["NPS rules on annuity percentage and exit can be updated by PFRDA; verify before retirement decisions.", "Monthly pension depends on annuity rates available at retirement, not only NPS returns.", "Section 80CCD benefits depend on tax regime and contribution type.", "Equity allocation, age, and active/auto choice affect return volatility."],
    "script": """function calculate(){const years=Math.max(0,value('retirement')-value('age'));const p=value('contribution'),r=value('return')/100/12,n=years*12;const corpus=r===0?p*n:p*((Math.pow(1+r,n)-1)/r)*(1+r);const annPct=Math.max(40,value('annuity-percent'))/100;const ann=corpus*annPct,lump=corpus-ann,pension=ann*value('annuity-rate')/100/12;text('corpus',`${formatIndianNumber(corpus)} (${formatShortIndian(corpus)})`);text('annuity',formatIndianNumber(ann));text('lump',formatIndianNumber(lump));text('pension',formatIndianNumber(pension));let labels=[],corp=[],pens=[];for(let y=1;y<=years;y++){const m=y*12;const c=r===0?p*m:p*((Math.pow(1+r,m)-1)/r)*(1+r);labels.push(`Year ${y}`);corp.push(c);pens.push(c*annPct*value('annuity-rate')/100/12);}drawChart('calc-chart','bar',labels,[{label:'Corpus',data:corp,backgroundColor:'#f97316'},{label:'Expected monthly pension',data:pens,backgroundColor:'#2563eb'}]);}bindCalculator(calculate);""",
},
{
    "file": "gold-price-calculator.html",
    "title": "Gold Price Calculator India — 24K, 22K, 18K Gold Value | Calculatorcity",
    "meta": "Calculate gold value in India. Enter weight in grams or tola, select purity (24K, 22K, 18K, 14K). Get gold price with making charges and GST.",
    "h1": "Gold Price Calculator India",
    "intro": "The gold price calculator estimates jewellery value in India using weight, purity, live market rate entered by the user, making charges, and GST. Enter grams or tola, choose 24K, 22K, 18K, or 14K, and add making charge percentage to calculate pure gold value, making charges, GST on gold and making, and total jewellery price. It is useful before visiting jewellers or comparing BIS-hallmarked quotes.",
    "widget": """<section class="calc-widget"><div class="field-grid"><div class="calc-input-group"><label for="weight">Weight</label><input id="weight" type="number" step="0.01" value="10"></div><div class="calc-input-group"><label for="unit">Weight unit</label><select id="unit"><option value="gram" selected>Grams</option><option value="tola">Tola (11.664 g)</option></select></div><div class="calc-input-group"><label for="purity">Gold purity</label><select id="purity"><option value="1">24K (99.9%)</option><option value="0.916" selected>22K (91.6%)</option><option value="0.75">18K (75%)</option><option value="0.583">14K (58.3%)</option></select></div><div class="calc-input-group"><label for="rate">24K gold price per gram (₹)</label><div class="input-prefix"><span>₹</span><input id="rate" type="number" value="7200"></div><span class="hint">Enter today's rate from MCX, jeweller, or trusted market source.</span></div><div class="calc-input-group"><label for="making">Making charges (%)</label><input id="making" type="number" value="15"></div></div><button class="calc-btn" id="calculate" type="button">Calculate gold value</button><div class="calc-result show"><div class="result-grid"><div class="result-card"><span class="result-value" id="gold-value">₹0.00</span><span class="result-label">Pure gold value</span></div><div class="result-card"><span class="result-value" id="making-out">₹0.00</span><span class="result-label">Making charges</span></div><div class="result-card"><span class="result-value" id="gst">₹0.00</span><span class="result-label">GST amount</span></div><div class="result-card highlight"><span class="result-value" id="total">₹0.00</span><span class="result-label">Total jewellery price</span></div></div><div class="chart-container"><canvas id="calc-chart"></canvas></div></div></section>""",
    "how_to": ["Enter jewellery weight in grams or tola.", "Choose purity based on hallmark or jeweller quote.", "Enter current 24K gold price per gram manually.", "Add making charge percentage quoted by the jeweller.", "Calculate gold value, making charge, GST, and total price before purchase."],
    "formula_box": "Gold value = weight in grams × 24K price × purity factor<br>Making charge = gold value × making %<br>GST = 3% on gold value + 5% on making charge",
    "formula_text": "<p>Indian jewellery is usually sold in 22K or 18K purity, not pure 24K, because pure gold is soft. The calculator treats the entered rate as a 24K per-gram reference and multiplies it by the purity factor. For 22K 916 gold, the factor is 0.916. Making charges are then applied as a percentage of the gold value. GST is estimated at 3% on gold value and 5% on making charges as commonly applied to jewellery invoices.</p><p>Actual bills can differ because jewellers use their own daily board rate, wastage, fixed making charges per gram, stone charges, hallmarking charges, discounts, exchange deductions, and rounding. For studded jewellery, only gold weight should be used for metal value; stones and diamonds should be valued separately. Always ask for a breakup showing net weight, purity, rate, making, GST, and hallmark details.</p>",
    "example": "<p>For 10 grams of 22K gold at a 24K rate of ₹7,200 per gram, gold value is ₹65,952.</p><p>At 15% making charge, making is ₹9,892.80. GST is 3% on gold plus 5% on making.</p><p><strong>Total jewellery price is about ₹78,318 before rounding.</strong></p>",
    "reference_title": "Gold purity and fineness",
    "reference_headers": ["Karat", "Purity", "Fineness mark"],
    "reference_rows": [["24K", "99.9%", "999"], ["23K", "95.8%", "958"], ["22K", "91.6%", "916"], ["21K", "87.5%", "875"], ["20K", "83.3%", "833"], ["18K", "75.0%", "750"], ["14K", "58.3%", "585"], ["9K", "37.5%", "375"]],
    "sections": [("Weight conversions", table(["Unit", "Equivalent"], [["1 tola", "11.664 grams"], ["1 sovereign", "8 grams"], ["1 ounce", "31.1035 grams"], ["10 grams", "0.857 tola"], ["100 grams", "8.573 tola"], ["1 kilogram", "1,000 grams"], ["1 gram", "1,000 milligrams"], ["1 carat for gemstones", "0.2 grams, not gold purity"]])), ("BIS hallmarking", "<p>BIS hallmarking helps buyers verify purity. A 916 hallmark means 22K gold with 91.6% gold content. Check the HUID, jeweller identification, purity mark, and invoice details. Hallmarking does not control making charges, so price comparison is still necessary.</p>")],
    "faqs": [("What is 916 gold?", "916 gold means 22K gold with about 91.6% pure gold content."), ("What is the difference between 22K and 24K gold?", "24K is nearly pure gold, while 22K contains alloy metals for strength and is common for jewellery."), ("How is gold purity measured?", "Purity is measured in karats or fineness, such as 999 for 24K and 916 for 22K."), ("What is BIS hallmark?", "BIS hallmark is a certification mark indicating tested purity and traceability details."), ("Why does jewellery have making charges?", "Making charges cover design, labour, wastage, craftsmanship, and retailer margin.")],
    "notes": ["Static websites cannot fetch live gold rates; enter today’s rate manually before calculating.", "Ask whether making charge is percentage-based or fixed per gram.", "GST treatment can differ for exchange, repair, stones, and old-gold purchase cases.", "BIS hallmark and invoice breakup are essential for resale and purity confidence."],
    "script": """function calculate(){const grams=value('weight')*(document.getElementById('unit').value==='tola'?11.664:1);const purity=Number(document.getElementById('purity').value);const gold=grams*value('rate')*purity;const making=gold*value('making')/100;const gst=gold*0.03+making*0.05;const total=gold+making+gst;text('gold-value',formatIndianNumber(gold));text('making-out',formatIndianNumber(making));text('gst',formatIndianNumber(gst));text('total',formatIndianNumber(total));drawChart('calc-chart','pie',['Gold value','Making','GST'],[{data:[gold,making,gst],backgroundColor:['#f59e0b','#f97316','#2563eb']}]);}bindCalculator(calculate);""",
},
{
    "file": "sukanya-samriddhi-calculator.html",
    "title": "Sukanya Samriddhi Yojana Calculator — SSY Maturity | Calculatorcity",
    "meta": "Free Sukanya Samriddhi Yojana calculator. Calculate SSY maturity amount for your daughter. Shows year-wise balance and interest for the full tenure.",
    "h1": "Sukanya Samriddhi Yojana (SSY) Calculator",
    "intro": "The Sukanya Samriddhi Yojana calculator estimates maturity value for a girl child’s SSY account in India. Enter daughter’s age, annual investment, and SSY interest rate to calculate deposit tenure, total amount deposited, interest earned, and maturity amount when the account completes 21 years from opening. The year-wise growth chart helps parents plan education, marriage, and long-term savings with government-backed tax benefits.",
    "widget": """<section class="calc-widget"><div class="field-grid"><div class="calc-input-group"><label for="age">Daughter's current age</label><input id="age" type="number" min="0" max="10" value="3"></div><div class="calc-input-group"><label for="investment">Annual investment amount (₹)</label><div class="input-prefix"><span>₹</span><input id="investment" type="number" min="250" max="150000" value="100000"></div></div><div class="calc-input-group"><label for="rate">SSY interest rate (%)</label><input id="rate" type="number" step="0.1" value="8.2"></div></div><button class="calc-btn" id="calculate" type="button">Calculate SSY maturity</button><div class="calc-result show"><div class="result-grid"><div class="result-card"><span class="result-value" id="deposit-years">15</span><span class="result-label">Deposit years</span></div><div class="result-card"><span class="result-value" id="deposited">₹0.00</span><span class="result-label">Total deposited</span></div><div class="result-card"><span class="result-value" id="interest">₹0.00</span><span class="result-label">Interest earned</span></div><div class="result-card highlight"><span class="result-value" id="maturity">₹0.00</span><span class="result-label">Maturity amount</span></div></div><div class="chart-container"><canvas id="calc-chart"></canvas></div><div id="year-table" class="amortization-table"></div></div></section>""",
    "how_to": ["Enter your daughter’s current age from 0 to 10.", "Enter yearly SSY deposit between ₹250 and ₹1,50,000.", "Use the current SSY interest rate or edit it for planning.", "Calculate maturity value at 21 years from account opening.", "Review the year-wise table showing deposit, interest, and closing balance."],
    "formula_box": "Balance grows annually at the SSY rate.<br>Deposits are made for 15 years and the account earns interest until maturity at 21 years from opening.",
    "formula_text": "<p>SSY deposits are made for 15 years, while the account matures after 21 years from opening. Interest is notified by the government and compounded annually. The calculator assumes one annual deposit at the beginning of each deposit year, then applies annual interest. After the 15-year deposit period ends, no further deposits are added, but the balance continues to earn interest until maturity.</p><p>The scheme is designed for girl children and an account can generally be opened until age 10. Deposits qualify for Section 80C under the old tax regime, and the scheme has EEE treatment: eligible investment deduction, tax-free interest, and tax-free maturity under current rules. Actual interest can change quarterly, so long-term projections should be reviewed every year.</p>",
    "example": "<p>If a parent invests ₹1,00,000 every year for 15 years at 8.2%, total deposits are ₹15,00,000.</p><p>The account continues earning interest until 21 years from opening and can mature around ₹46,00,000 depending on timing assumptions.</p><p><strong>The exact number changes if the government revises SSY rates.</strong></p>",
    "reference_title": "SSY annual deposit maturity estimates at 8.2%",
    "reference_headers": ["Annual deposit", "Total deposit", "Approx. maturity", "Interest"],
    "reference_rows": [["₹250", "₹3,750", "₹11,505", "₹7,755"], ["₹12,000", "₹1,80,000", "₹5,52,240", "₹3,72,240"], ["₹24,000", "₹3,60,000", "₹11,04,480", "₹7,44,480"], ["₹50,000", "₹7,50,000", "₹23,01,000", "₹15,51,000"], ["₹75,000", "₹11,25,000", "₹34,51,500", "₹23,26,500"], ["₹1,00,000", "₹15,00,000", "₹46,02,000", "₹31,02,000"], ["₹1,25,000", "₹18,75,000", "₹57,52,500", "₹38,77,500"], ["₹1,50,000", "₹22,50,000", "₹69,03,000", "₹46,53,000"]],
    "sections": [("SSY rules", "<p>The minimum annual deposit is ₹250 and maximum is ₹1,50,000. Partial withdrawal is allowed for higher education after the girl turns 18 or passes specified education milestones, subject to limits. The account can be opened for up to two daughters, with special allowance for twins or triplets as per scheme rules.</p>")],
    "faqs": [("What is Sukanya Samriddhi Yojana?", "SSY is a government-backed small savings scheme for girl children."), ("What is the current SSY interest rate?", "The calculator defaults to 8.2%, but the government can revise rates periodically."), ("When can I withdraw from SSY?", "Partial withdrawal is allowed for education after 18 under conditions; full maturity is 21 years from opening."), ("Is SSY better than PPF?", "SSY usually has a higher rate and girl-child purpose, while PPF is more flexible for any eligible individual."), ("Can NRI open SSY account?", "SSY is generally for resident Indian girl children; NRI eligibility has restrictions and should be verified.")],
    "notes": ["SSY interest rates are government-notified and can change every quarter.", "The account can generally be opened only until the girl child turns 10.", "Deposits above ₹1,50,000 in a financial year are not allowed for normal benefit calculation.", "Tax benefits depend on old-regime 80C usage and current scheme rules."],
    "script": """function calculate(){const age=clamp(value('age'),0,10);const annual=clamp(value('investment'),250,150000);const rate=value('rate')/100;const totalYears=21;let balance=0,deposit=0,rows='',labels=[],dep=[],intData=[];for(let y=1;y<=totalYears;y++){const opening=balance;let d=y<=15?annual:0;balance+=d;deposit+=d;const interest=balance*rate;balance+=interest;labels.push(`Age ${age+y}`);dep.push(deposit);intData.push(balance-deposit);rows+=`<tr><td>${y}</td><td>${formatIndianNumber(d)}</td><td>${formatIndianNumber(interest)}</td><td>${formatIndianNumber(balance)}</td></tr>`;}text('deposit-years','15 years');text('deposited',formatIndianNumber(deposit));text('interest',formatIndianNumber(balance-deposit));text('maturity',`${formatIndianNumber(balance)} (${formatShortIndian(balance)})`);html('year-table','<table class="reference-table"><thead><tr><th>Year</th><th>Deposit</th><th>Interest</th><th>Closing Balance</th></tr></thead><tbody>'+rows+'</tbody></table>');drawChart('calc-chart','bar',labels,[{label:'Deposited',data:dep,backgroundColor:'#2563eb'},{label:'Interest',data:intData,backgroundColor:'#16a34a'}],{scales:{x:{stacked:true},y:{stacked:true}}});}bindCalculator(calculate);""",
},
{
    "file": "advance-tax-calculator.html",
    "title": "Advance Tax Calculator India — Due Dates & Amounts | Calculatorcity",
    "meta": "Calculate advance tax installments for FY 2024-25. Find quarterly advance tax amounts and due dates. For salaried, self-employed and businesspersons.",
    "h1": "Advance Tax Calculator India",
    "intro": "The advance tax calculator estimates quarterly tax instalments for Indian taxpayers based on estimated yearly income, taxpayer type, TDS already deducted, and tax already paid. It calculates total tax liability, net advance tax payable, due-date percentages for June, September, December, and March, and whether interest risk under Sections 234B or 234C may apply. It is useful for salaried taxpayers with extra income, freelancers, professionals, and businesses.",
    "widget": """<section class="calc-widget"><div class="field-grid"><div class="calc-input-group"><label for="income">Total estimated income for the year (₹)</label><div class="input-prefix"><span>₹</span><input id="income" type="number" value="1500000"></div></div><div class="calc-input-group"><label for="type">Type</label><select id="type"><option value="salaried">Salaried</option><option value="self">Self-employed</option><option value="business">Business</option><option value="senior">Senior citizen, no business income</option></select></div><div class="calc-input-group"><label for="tds">TDS already deducted (₹)</label><div class="input-prefix"><span>₹</span><input id="tds" type="number" value="50000"></div></div><div class="calc-input-group"><label for="paid">Tax already paid (₹)</label><div class="input-prefix"><span>₹</span><input id="paid" type="number" value="0"></div></div></div><button class="calc-btn" id="calculate" type="button">Calculate advance tax</button><div class="calc-result show"><div class="result-grid"><div class="result-card"><span class="result-value" id="liability">₹0.00</span><span class="result-label">Total tax liability</span></div><div class="result-card highlight"><span class="result-value" id="payable">₹0.00</span><span class="result-label">Advance tax payable after TDS</span></div><div class="result-card"><span class="result-value" id="interest-risk">No</span><span class="result-label">234B / 234C interest risk</span></div></div><div class="chart-container"><canvas id="calc-chart"></canvas></div><div id="installments" class="amortization-table"></div></div></section>""",
    "how_to": ["Enter estimated total income for the financial year.", "Choose taxpayer type, including senior citizen with no business income if applicable.", "Enter TDS already deducted and any advance/self-assessment tax already paid.", "Calculate total tax and net advance tax payable.", "Use the instalment table to plan payments by June 15, September 15, December 15, and March 15."],
    "formula_box": "Advance tax payable = estimated annual tax − TDS already deducted<br>Installments: 15%, 45%, 75%, 100% of total advance tax by due dates",
    "formula_text": "<p>Advance tax is pay-as-you-earn tax paid during the financial year when estimated tax liability after TDS is ₹10,000 or more. For most taxpayers, cumulative payment targets are 15% by 15 June, 45% by 15 September, 75% by 15 December, and 100% by 15 March. The calculator first estimates tax using a simplified new-regime individual slab model, subtracts TDS, and then allocates the balance to instalments.</p><p>Senior citizens who do not have income from business or profession are generally not required to pay advance tax. Presumptive taxation cases can have different payment timing. If advance tax is not paid or is paid short, interest under Sections 234B and 234C can apply, commonly at 1% per month or part month depending on default type and period. Use exact income estimates before each due date.</p>",
    "example": "<p>A freelancer estimates annual income of ₹15,00,000 and TDS of ₹50,000.</p><p>If total tax is about ₹1,45,600, advance tax payable after TDS is about ₹95,600.</p><p><strong>The cumulative targets are 15%, 45%, 75%, and 100% by the four due dates.</strong></p>",
    "reference_title": "Advance tax due dates for FY 2024-25",
    "reference_headers": ["Due date", "Cumulative tax payable", "Who it applies to"],
    "reference_rows": [["15 June 2024", "15%", "Most advance tax payers"], ["15 September 2024", "45%", "Most advance tax payers"], ["15 December 2024", "75%", "Most advance tax payers"], ["15 March 2025", "100%", "Most advance tax payers"], ["15 March 2025", "100%", "Eligible presumptive taxpayers"], ["Threshold", "₹10,000", "Advance tax required if payable tax crosses this"], ["Interest 234B", "1% per month", "Default in advance tax"], ["Interest 234C", "1% / 3% periods", "Deferment of instalments"]],
    "sections": [("Who needs to pay advance tax?", "<p>Salaried people may still need advance tax when they have rent, capital gains, interest, freelance income, or business income not fully covered by TDS. Self-employed professionals and business owners commonly pay advance tax because no employer deducts monthly TDS from profits. Estimate income before each due date and update the next instalment if income changes.</p>")],
    "faqs": [("What is advance tax?", "Advance tax is income tax paid during the financial year instead of waiting until return filing."), ("Who is required to pay advance tax?", "Taxpayers with estimated tax payable of ₹10,000 or more after TDS generally need to pay, subject to exemptions."), ("What is the penalty for not paying advance tax?", "Interest under Sections 234B and 234C can apply for non-payment or deferment."), ("What are the advance tax due dates?", "The main due dates are June 15, September 15, December 15, and March 15."), ("How is advance tax different from TDS?", "TDS is deducted by payer; advance tax is paid directly by the taxpayer based on estimated income.")],
    "notes": ["Advance tax applies when tax payable after TDS is ₹10,000 or more.", "Senior citizens without business or professional income are generally exempt from advance tax.", "Income from capital gains can arise unpredictably; pay the next instalment after the gain if needed.", "Use the correct assessment year and challan details while paying online."],
    "script": """const slabs=[[0,300000,0],[300000,700000,0.05],[700000,1000000,0.10],[1000000,1200000,0.15],[1200000,1500000,0.20],[1500000,Infinity,0.30]];function calculate(){const income=value('income');const type=document.getElementById('type').value;const taxable=Math.max(0,income-(type==='salaried'?75000:0));let tax=taxable<=700000?0:slabTax(taxable,slabs)*1.04;if(type==='senior')tax=0;const payable=Math.max(0,tax-value('tds'));const paid=value('paid');const risk=payable>=10000&&paid<payable*0.9?'Possible':'Low';text('liability',formatIndianNumber(tax));text('payable',formatIndianNumber(payable));text('interest-risk',risk);const dues=[['15 Jun',0.15],['15 Sep',0.45],['15 Dec',0.75],['15 Mar',1.00]];html('installments','<table class="reference-table"><thead><tr><th>Due date</th><th>Cumulative target</th><th>Cumulative amount</th><th>Installment amount</th></tr></thead><tbody>'+dues.map((d,i)=>{const prev=i?dues[i-1][1]*payable:0;const cum=d[1]*payable;return `<tr><td>${d[0]}</td><td>${formatPlainNumber(d[1]*100,0)}%</td><td>${formatIndianNumber(cum)}</td><td>${formatIndianNumber(Math.max(0,cum-prev))}</td></tr>`}).join('')+'</tbody></table>');drawChart('calc-chart','bar',dues.map(d=>d[0]),[{label:'Cumulative advance tax',data:dues.map(d=>d[1]*payable),backgroundColor:'#f97316'}]);}bindCalculator(calculate);""",
}
])


def write_pages() -> None:
    INDIA_DIR.mkdir(exist_ok=True)
    for page in PAGES:
        (INDIA_DIR / page["file"]).write_text(render_page(page), encoding="utf-8")


def update_search_index() -> None:
    category_map = {
        "maths": "Math",
        "finance": "Finance",
        "unit-converter": "Unit Converter",
        "health-fitness": "Health & Fitness",
        "date-time": "Date & Time",
        "science-other": "Science & Other",
        "india": "India",
    }
    entries = []
    for path in sorted(ROOT.glob("*/*.html")):
        rel = path.relative_to(ROOT).as_posix()
        folder = rel.split("/")[0]
        if folder not in category_map:
            continue
        content = path.read_text(encoding="utf-8")
        h1_match = re.search(r"<h1>(.*?)</h1>", content, re.S)
        title_match = re.search(r"<title>(.*?)</title>", content, re.S)
        raw_name = h1_match.group(1) if h1_match else title_match.group(1)
        name = re.sub(r"<.*?>", "", raw_name).replace("&amp;", "&").strip()
        keywords = re.sub(r"[^a-z0-9 ]+", " ", name.lower())
        if folder == "india":
            keywords += " india rupee tax investment loan gst salary"
        entries.append({
            "name": name,
            "url": f"/{rel}",
            "category": category_map[folder],
            "keywords": keywords,
        })
    js_path = ROOT / "assets" / "js" / "main.js"
    js = js_path.read_text(encoding="utf-8")
    replacement = "const calculators = " + json.dumps(entries, ensure_ascii=False, indent=2) + ";"
    js = re.sub(r"const calculators = \[.*?\];", replacement, js, count=1, flags=re.S)
    js_path.write_text(js, encoding="utf-8")


def update_sitemap() -> None:
    urls = [""]
    for path in sorted(ROOT.glob("*/*.html")):
        urls.append(path.relative_to(ROOT).as_posix())
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        loc = f"{DOMAIN}/" if url == "" else f"{DOMAIN}/{url}"
        priority = "1.0" if url == "" else "0.8"
        body.append(f"  <url><loc>{loc}</loc><changefreq>monthly</changefreq><priority>{priority}</priority></url>")
    body.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(body) + "\n", encoding="utf-8")


if __name__ == "__main__":
    write_pages()
    update_search_index()
    update_sitemap()
    print(f"Generated {len(PAGES)} India pages and refreshed search index/sitemap.")


