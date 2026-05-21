const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = path.resolve(__dirname, "..");
const OUT_DIR = path.join(ROOT, "india", "stamp-duty");
const DATA_FILE = path.join(ROOT, "assets", "js", "stamp-duty-data.js");
const DOMAIN = "https://calculatorcity.in";

function loadData() {
  const context = { window: {} };
  vm.runInNewContext(fs.readFileSync(DATA_FILE, "utf8"), context, { filename: DATA_FILE });
  return {
    data: context.window.stampDutyData,
    order: context.window.stampDutyStateOrder
  };
}

function escapeHTML(value) {
  return String(value == null ? "" : value).replace(/[&<>"']/g, char => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  }[char]));
}

function stripHTML(value) {
  return String(value || "").replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
}

function percent(value, decimals) {
  const number = Number(value) || 0;
  const places = decimals == null ? (Number.isInteger(number) ? 0 : 2) : decimals;
  return number.toFixed(places).replace(/\.?0+$/, "") + "%";
}

function stateUrl(slug) {
  return `${slug}.html`;
}

function stateTotal(state, gender = "male") {
  return (state.stampDuty[gender] || state.stampDuty.male || 0) +
    (state.registrationCharges[gender] || state.registrationCharges.male || 0) +
    (state.transferDuty || 0);
}

function faqSchema(items) {
  return {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": (items || []).map(item => ({
      "@type": "Question",
      "name": item.q,
      "acceptedAnswer": {
        "@type": "Answer",
        "text": stripHTML(item.a)
      }
    }))
  };
}

const defaultFaq = [
  {
    q: "What is stamp duty on property in India?",
    a: "Stamp duty is a state government tax on property transactions. Rates vary from 3% to 8.25% depending on the state. It is charged on the higher of the actual transaction value or the government-declared circle rate. Registration charges are additional fees for officially recording the property transfer."
  },
  {
    q: "Which state has lowest stamp duty in India?",
    a: "Telangana has one of the lowest effective totals at approximately 6% (4% stamp duty + 0.5% registration + 1.5% transfer duty). Goa has a low stamp duty of 3.5%, although its registration charge is higher."
  },
  {
    q: "Which state has highest stamp duty in India?",
    a: "Tamil Nadu has the highest total in this calculator at 11% (7% stamp duty + 4% registration). Kerala, Assam, Madhya Pradesh and Chhattisgarh are also among the higher-cost states."
  },
  {
    q: "Do women get lower stamp duty?",
    a: "Yes. Several states and UTs offer lower stamp duty for women buyers, including Delhi, Haryana, Punjab, Maharashtra, Uttar Pradesh, Rajasthan, Odisha, Himachal Pradesh, Uttarakhand, Jammu & Kashmir, Chandigarh and Ladakh."
  },
  {
    q: "What is circle rate and how does it affect stamp duty?",
    a: "Circle rate is the minimum property value set by the government for a locality. Stamp duty is usually calculated on the higher of circle rate and transaction value, so a low agreement price does not always reduce duty."
  },
  {
    q: "Is stamp duty included in home loan?",
    a: "Usually no. Buyers commonly need to pay stamp duty and registration charges from their own funds, so the upfront budget should include these costs in addition to down payment and other charges."
  }
];

function header() {
  return `<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="header-inner">
    <a class="logo" href="../../index.html">⌗ Calculatorcity</a>
    <nav class="main-nav" aria-label="Main navigation">
      <a href="../../index.html#math">Math</a>
      <a href="../../index.html#finance">Finance</a>
      <a href="../../index.html#unit">Unit</a>
      <a href="../../index.html#health">Health</a>
      <a href="../../index.html#datetime">Date &amp; Time</a>
      <a href="../../index.html#science">Science</a>
      <a class="nav-india" href="../../index.html#india">India</a>
    </nav>
    <div class="header-search">
      <label class="sr-only" for="header-search">Search calculators</label>
      <input id="header-search" class="search-input" type="search" data-search-input>
    </div>
    <button class="mobile-menu-btn" type="button" aria-label="Open menu" aria-expanded="false" data-mobile-menu-btn>☰</button>
  </div>
  <nav class="mobile-nav" aria-label="Mobile navigation" data-mobile-nav>
    <a href="../../index.html#math">Math</a>
    <a href="../../index.html#finance">Finance</a>
    <a href="../../index.html#unit">Unit Converter</a>
    <a href="../../index.html#health">Health &amp; Fitness</a>
    <a href="../../index.html#datetime">Date &amp; Time</a>
    <a href="../../index.html#science">Science &amp; Other</a>
    <a href="../../index.html#india">India</a>
  </nav>
</header>`;
}

function footer() {
  return `<hr class="footer-separator" aria-hidden="true">
<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-main">
      <nav class="footer-categories" aria-labelledby="footer-categories-heading">
        <h3 id="footer-categories-heading" class="footer-links-label">CATEGORIES</h3>
        <div class="footer-category-pills">
          <a href="../../index.html#math"><i class="ti ti-math" aria-hidden="true"></i><span>Math Calculators</span></a>
          <a href="../../index.html#finance"><i class="ti ti-coin-rupee" aria-hidden="true"></i><span>Finance Calculators</span></a>
          <a href="../../index.html#unit"><i class="ti ti-ruler" aria-hidden="true"></i><span>Unit Converters</span></a>
          <a href="../../index.html#health"><i class="ti ti-heartbeat" aria-hidden="true"></i><span>Health &amp; Fitness</span></a>
          <a href="../../index.html#datetime"><i class="ti ti-calendar" aria-hidden="true"></i><span>Date &amp; Time</span></a>
          <a href="../../index.html#science"><i class="ti ti-flask" aria-hidden="true"></i><span>Science &amp; Other</span></a>
          <a href="../../index.html#india"><i class="ti ti-map-pin" aria-hidden="true"></i><span>India Calculators</span></a>
        </div>
      </nav>
      <nav class="footer-popular" aria-labelledby="footer-popular-heading">
        <h3 id="footer-popular-heading" class="footer-links-label">POPULAR CALCULATORS</h3>
        <div class="footer-popular-links">
          <a href="../../maths/percentage-calculator.html">Percentage</a>
          <a href="../../india/gst-calculator.html">GST</a>
          <a href="../../india/income-tax-calculator.html">Income Tax</a>
          <a href="../../india/home-loan-emi-calculator.html">Home Loan EMI</a>
          <a href="../../india/sip-calculator.html">SIP</a>
          <a href="../../india/fd-calculator.html">FD</a>
          <a href="../../health-fitness/bmi-calculator.html">BMI</a>
          <a href="../../date-time/age-calculator.html">Age</a>
          <a href="../../finance/currency-converter.html">Currency</a>
          <a href="../../india/gold-price-calculator.html">Gold Price</a>
          <a href="../../finance/loan-emi-calculator.html">Loan EMI</a>
          <a href="../../finance/compound-interest-calculator.html">Compound Interest</a>
          <a href="../../india/ctc-salary-calculator.html">CTC Salary</a>
          <a href="../../india/pf-epf-calculator.html">EPF / PF</a>
          <a href="../../india/ppf-calculator.html">PPF</a>
          <a href="../../india/hra-exemption-calculator.html">HRA Exemption</a>
          <a href="../../india/tds-calculator.html">TDS</a>
          <a href="../../finance/discount-calculator.html">Discount</a>
          <a href="../../india/cgpa-to-percentage-calculator.html">CGPA to %</a>
          <a href="../../india/stamp-duty/index.html">Stamp Duty India</a>
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
          <a href="../../company/about-us.html">About Us</a>
          <a href="../../company/blogs.html">Blog</a>
          <a href="../../company/contact-us.html">Contact Us</a>
          <a href="../../company/help.html">Help</a>
          <a href="../../company/privacy-policy.html">Privacy Policy</a>
          <a href="../../company/terms-and-conditions.html">Terms &amp; Conditions</a>
        </nav>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Calculatorcity. All calculations run locally in your browser.</span>
      <span class="footer-disclaimer">For education and planning only. Results are estimates — not financial, tax, legal, or medical advice. Verify with a qualified expert.</span>
    </div>
  </div>
</footer>`;
}

function inlineStyles({ stateColor = "#f97316", stateLight = "#fff7ed", stateBorder = "#fed7aa" } = {}) {
  return `/* ─── Page transition — prevents flicker between state pages ─── */
body {
  opacity: 0;
  transition: opacity 0.18s ease;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
body.page-loaded { opacity: 1; }
.page-exit {
  opacity: 0 !important;
  transition: opacity 0.15s ease !important;
}

:root {
  --stamp-primary: ${stateColor};
  --stamp-primary-dark: #ea580c;
  --stamp-primary-light: ${stateLight};
  --stamp-primary-border: ${stateBorder};
  --state-color: ${stateColor};
  --state-light: ${stateLight};
  --state-border: ${stateBorder};
  --cheap-color: #16a34a;
  --expensive-color: #dc2626;
  --women-color: #ec4899;
  --font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  --widget-radius: 16px;
  --card-radius: 12px;
  --btn-radius: 10px;
  --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.stamp-page {
  --primary: var(--stamp-primary);
  --primary-dark: var(--stamp-primary-dark);
  --primary-light: var(--state-light);
  font-family: var(--font-body);
  background: #f8fafc;
  overflow-x: hidden;
}
.stamp-page input,
.stamp-page select,
.stamp-page button {
  font-family: var(--font-body);
}
.stamp-hero {
  background:
    radial-gradient(circle at top left, var(--state-light), transparent 32rem),
    linear-gradient(135deg, var(--state-light) 0%, #ffffff 100%);
  border-bottom: 1px solid var(--state-border);
  padding: 2rem 0 1.5rem;
}
.stamp-hero .breadcrumb {
  margin-bottom: 1rem;
}
.hero-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.hero-content > div:last-child {
  min-width: 0;
}
.hero-icon {
  width: 3rem;
  height: 3rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: #fff;
  border: 1px solid var(--state-border);
  color: var(--state-color);
  font-size: 1.7rem;
  box-shadow: 0 4px 16px rgba(15,23,42,0.08);
}
.hero-h1 {
  margin: 0;
  font-size: clamp(1.45rem, 4vw, 2.1rem);
  font-weight: 700;
  color: #0f172a;
  line-height: 1.18;
  letter-spacing: 0;
  overflow-wrap: anywhere;
}
.hero-subtitle {
  font-size: 0.95rem;
  color: #64748b;
  margin-top: 0.4rem;
  max-width: 52rem;
}
.state-selector-wrap {
  background: white;
  border: 1.5px solid var(--state-border);
  border-radius: var(--widget-radius);
  padding: 1rem 1.25rem;
  box-shadow: 0 4px 16px rgba(15,23,42,0.08);
}
.state-label,
.input-label {
  display: block;
  font-size: 0.8rem;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.6rem;
}
.state-label {
  display: flex;
  align-items: center;
  gap: 6px;
}
.state-select-wrapper {
  position: relative;
}
.state-select {
  width: 100%;
  min-height: 3.25rem;
  padding: 0.875rem 3rem 0.875rem 1rem;
  font-size: 1.05rem;
  font-weight: 600;
  color: #0f172a;
  background: white;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
  transition: var(--transition);
}
.state-select:focus {
  outline: none;
  border-color: var(--state-color);
  box-shadow: 0 0 0 3px var(--state-light);
}
.select-arrow {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
  pointer-events: none;
}
.calc-section {
  padding: 1.5rem 0;
  background: #f8fafc;
}
.calc-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 280px;
  gap: 1.5rem;
  align-items: start;
}
.calc-main-col {
  min-width: 0;
}
.calc-widget-box {
  background: white;
  border: 1.5px solid var(--state-border);
  border-radius: var(--widget-radius);
  padding: 1.5rem;
  box-shadow: 0 4px 24px rgba(15,23,42,0.06);
}
.state-info-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  border: 1.5px solid var(--state-color);
  border-radius: var(--card-radius);
  padding: 0.875rem 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 10px;
}
.state-info-left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}
.state-info-left > div {
  min-width: 0;
}
.state-flag-big {
  font-size: 1.5rem;
}
.state-info-name {
  font-size: 1rem;
  font-weight: 700;
}
.state-info-sub {
  font-size: 0.8rem;
  color: #64748b;
  margin-top: 1px;
  overflow-wrap: anywhere;
}
.badge {
  display: inline-block;
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
  margin-left: 6px;
  background: #f1f5f9;
  color: #475569;
}
.badge-women {
  background: #fdf2f8;
  color: #9d174d;
}
.badge-transfer {
  background: #fef3c7;
  color: #92400e;
}
.gender-row,
.prop-type-row,
.urban-rural-row,
.calc-input-group {
  margin-bottom: 1.25rem;
}
.gender-tabs {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(6.75rem, 1fr));
  gap: 8px;
}
.prop-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.gender-tab,
.prop-tab {
  border: 1.5px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #475569;
  background: white;
  cursor: pointer;
  transition: var(--transition);
  text-align: center;
}
.gender-tab {
  min-width: 0;
  padding: 0.625rem;
}
.prop-tab {
  padding: 0.5rem 1rem;
}
.gender-tab:hover,
.prop-tab:hover {
  border-color: var(--state-color);
}
.gender-tab.active,
.prop-tab.active {
  background: var(--state-color);
  border-color: var(--state-color);
  color: white;
}
.gender-tab.women-tab.active {
  background: var(--women-color);
  border-color: var(--women-color);
}
.women-discount-badge {
  display: none;
  align-items: center;
  gap: 8px;
  background: #fdf2f8;
  border: 1px solid #fbcfe8;
  border-radius: 8px;
  padding: 0.6rem 0.875rem;
  font-size: 0.875rem;
  color: #9d174d;
  margin-bottom: 1rem;
}
.women-discount-badge.show {
  display: flex;
}
.toggle-row {
  display: flex;
  align-items: center;
  gap: 12px;
}
.toggle-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #334155;
}
.toggle-switch {
  position: relative;
  width: 44px;
  height: 24px;
  flex-shrink: 0;
}
.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}
.toggle-slider {
  position: absolute;
  inset: 0;
  background: #cbd5e1;
  border-radius: 24px;
  cursor: pointer;
  transition: background 0.2s;
}
.toggle-slider::before {
  content: '';
  position: absolute;
  width: 18px;
  height: 18px;
  left: 3px;
  top: 3px;
  background: white;
  border-radius: 50%;
  transition: transform 0.2s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}
.toggle-switch input:checked + .toggle-slider {
  background: var(--state-color);
}
.toggle-switch input:checked + .toggle-slider::before {
  transform: translateX(20px);
}
.amount-input-wrap {
  position: relative;
  display: grid;
  gap: 0.45rem;
  margin-bottom: 0.75rem;
}
.calc-input-group .amount-input {
  width: 100%;
  min-width: 0;
  padding: 1rem 1rem 1rem 2.75rem;
  font-size: clamp(1.35rem, 7vw, 1.75rem);
  font-weight: 500;
  font-family: var(--font-mono);
  color: #0f172a;
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  transition: var(--transition);
}
.calc-input-group .amount-input:focus {
  outline: none;
  border-color: var(--state-color);
  background: white;
  box-shadow: 0 0 0 3px var(--state-light);
}
.rupee-prefix {
  position: absolute;
  left: 1rem;
  top: 2rem;
  transform: translateY(-50%);
  font-size: 1.15rem;
  line-height: 1;
  font-weight: 700;
  color: #64748b;
  font-family: var(--font-body);
  pointer-events: none;
}
.amount-badge {
  position: static;
  transform: none;
  justify-self: start;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 0.72rem;
  font-weight: 700;
  color: #94a3b8;
  background: #f1f5f9;
  padding: 2px 8px;
  border-radius: 6px;
}
.amount-helper {
  min-height: 1.2rem;
  font-size: 0.8rem;
  color: #64748b;
  margin-bottom: 0.75rem;
  font-family: var(--font-mono);
}
.calc-error {
  padding: 0.65rem 0.8rem;
  margin-bottom: 0.875rem;
  border-radius: 8px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
  font-size: 0.85rem;
  font-weight: 600;
}
.calc-btn-main {
  width: 100%;
  padding: 1rem;
  background: var(--state-color);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1.05rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: var(--transition);
}
.calc-btn-main:hover {
  filter: brightness(1.05);
}
.calc-btn-main:active {
  transform: scale(0.99);
}
.results-box {
  margin-top: 1.5rem;
  animation: fadeUp 0.3s ease;
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.result-total {
  background: linear-gradient(135deg, var(--state-color), #0f172a);
  color: white;
  border-radius: var(--card-radius);
  padding: 1.5rem;
  text-align: center;
  margin-bottom: 1rem;
  box-shadow: 0 8px 24px rgba(249,115,22,0.2);
}
.result-total-label {
  font-size: 0.8rem;
  font-weight: 700;
  opacity: 0.85;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.result-total-value {
  font-size: clamp(2rem, 9vw, 2.75rem);
  font-weight: 700;
  font-family: var(--font-mono);
  line-height: 1.1;
  margin: 0.25rem 0;
  overflow-wrap: anywhere;
}
.result-total-meta {
  font-size: 0.85rem;
  opacity: 0.8;
}
.women-savings-banner {
  display: none;
  background: #fdf2f8;
  border: 1px solid #fbcfe8;
  border-radius: 8px;
  padding: 0.875rem 1rem;
  margin-bottom: 1rem;
  font-size: 0.875rem;
  color: #9d174d;
  text-align: center;
}
.women-savings-banner.show {
  display: block;
}
.breakdown-section,
.state-compare-section,
.tips-section {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: var(--card-radius);
  padding: 1.25rem;
  margin-bottom: 1rem;
}
.section-title {
  font-size: 0.8rem;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.75rem;
}
.breakdown-table,
.rates-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}
.breakdown-table th,
.rates-table th {
  text-align: left;
  padding: 7px 10px;
  background: #f8fafc;
  color: #64748b;
  font-weight: 700;
  font-size: 0.75rem;
  text-transform: uppercase;
  border-bottom: 1px solid #e2e8f0;
}
.breakdown-table td,
.rates-table td {
  padding: 8px 10px;
  border-bottom: 1px solid #f1f5f9;
  color: #334155;
  vertical-align: top;
}
.breakdown-table td:last-child {
  text-align: right;
  font-family: var(--font-mono);
  font-weight: 600;
}
.breakdown-table tfoot td {
  font-weight: 700;
  border-top: 2px solid #e2e8f0;
  background: #f8fafc;
}
.breakdown-table tfoot tr:not(.total-row) td {
  font-size: 0.8rem;
  color: #64748b;
}
.compare-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 8px;
  margin-top: 0.75rem;
}
.compare-item {
  display: block;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 8px 10px;
  cursor: pointer;
  transition: var(--transition);
  font-size: 0.8rem;
  text-decoration: none;
}
.compare-item:hover {
  border-color: var(--tile-color, var(--state-color));
  background: var(--tile-light, var(--state-light));
  text-decoration: none;
}
.compare-item-name {
  font-weight: 700;
  color: #334155;
  font-size: 0.75rem;
}
.compare-item-total {
  font-family: var(--font-mono);
  font-weight: 700;
  color: #0f172a;
  font-size: 0.875rem;
  margin-top: 2px;
}
.compare-item-rate {
  font-size: 0.7rem;
  color: #94a3b8;
  margin-top: 1px;
}
.compare-item.cheaper .compare-item-total {
  color: var(--cheap-color);
}
.compare-item.expensive .compare-item-total {
  color: var(--expensive-color);
}
.all-states-section {
  padding: 2.5rem 0;
  background: white;
  border-top: 1px solid #e2e8f0;
}
.states-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 8px;
}
.state-tile {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 4.6rem;
  padding: 0.875rem 0.75rem;
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  cursor: pointer;
  transition: var(--transition);
  text-align: center;
  gap: 3px;
  text-decoration: none;
}
.state-tile:hover {
  border-color: var(--tile-color, var(--state-color));
  background: var(--tile-light, var(--state-light));
  transform: translateY(-1px);
  text-decoration: none;
}
.state-tile.active-state {
  border-color: var(--state-color);
  background: var(--state-color);
}
.state-tile-name {
  font-size: 0.8rem;
  font-weight: 700;
  color: #334155;
}
.state-tile.active-state .state-tile-name {
  color: white;
}
.state-tile-rate {
  font-size: 0.7rem;
  color: #94a3b8;
}
.state-tile.active-state .state-tile-rate {
  color: rgba(255,255,255,0.8);
}
.content-area {
  padding: 2rem 0;
  background: #f8fafc;
}
.content-section {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: var(--card-radius);
  padding: 1.5rem;
  margin-bottom: 1.25rem;
}
.content-section h2 {
  font-size: 1.1rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 0.875rem;
}
.content-section p {
  font-size: 0.92rem;
  color: #475569;
  line-height: 1.75;
  margin-bottom: 0.75rem;
}
.content-section p:last-child {
  margin-bottom: 0;
}
.tariff-summary {
  background: var(--state-light);
  border: 1px solid var(--state-border);
  border-radius: var(--card-radius);
  padding: 1rem;
  margin-bottom: 1.25rem;
}
.tariff-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
  gap: 8px;
}
.tariff-item {
  text-align: center;
}
.tariff-val {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--stamp-primary);
  font-family: var(--font-mono);
}
.tariff-women {
  color: var(--women-color);
}
.tariff-transfer {
  color: #d97706;
}
.tariff-lbl {
  font-size: 0.7rem;
  color: #64748b;
  margin-top: 2px;
}
.rate-note {
  font-size: 0.82rem !important;
  color: #64748b !important;
  margin-top: 0.75rem;
}
.women-rate-row td {
  background: #fdf2f8;
  color: #9d174d;
  font-size: 0.82rem;
  font-weight: 700;
}
.faq-list {
  display: block;
}
.faq-item {
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  margin-bottom: 0.8rem;
  background: var(--bg);
  overflow: hidden;
}
.faq-item:last-child {
  margin-bottom: 0;
}
.faq-q-btn {
  width: 100%;
  text-align: left;
  padding: 1rem 1.15rem;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text);
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  line-height: 1.45;
  transition: background 0.2s ease;
}
.faq-q-btn:hover,
.faq-q-btn[aria-expanded="true"] {
  background: var(--primary-light);
}
.faq-chevron {
  width: 1.35rem;
  height: 1.35rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: #fff;
  color: var(--primary);
  font-size: 0.8rem;
  font-weight: 700;
  flex-shrink: 0;
  transition: transform 0.2s;
}
.faq-q-btn[aria-expanded="true"] .faq-chevron {
  transform: rotate(180deg);
}
.faq-answer {
  padding: 0 1.15rem 1rem;
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.75;
  display: none;
}
.faq-answer.open {
  display: block;
}
.calc-sidebar-col {
  position: sticky;
  top: 80px;
}
.sidebar-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: var(--card-radius);
  padding: 1rem;
  margin-bottom: 1rem;
}
.sidebar-card-title {
  font-size: 0.8rem;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.75rem;
}
.quick-fact {
  padding: 5px 8px;
  background: #f8fafc;
  border-radius: 6px;
  font-size: 0.8rem;
  color: #475569;
  margin-bottom: 4px;
}
.fact-women {
  color: #9d174d;
}
.quick-fact-total {
  border-top: 1px solid #e2e8f0;
  padding-top: 6px;
  margin-top: 4px;
}
.tip-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 8px 10px;
  background: #f8fafc;
  border-radius: 8px;
  font-size: 0.85rem;
  color: #334155;
  line-height: 1.5;
  margin-bottom: 6px;
}
.tip-icon {
  font-size: 1rem;
  flex-shrink: 0;
}
.ad-slot {
  min-height: 90px;
  border: 1px dashed #cbd5e1;
  border-radius: 10px;
  background: #f8fafc;
}
.ad-slot-horizontal {
  margin-bottom: 1.25rem;
}
@media (max-width: 900px) {
  .calc-layout {
    grid-template-columns: 1fr;
  }
  .calc-sidebar-col {
    display: none;
  }
}
@media (max-width: 640px) {
  .stamp-hero {
    padding-top: 1.25rem;
  }
  .hero-content {
    align-items: flex-start;
  }
  .calc-widget-box,
  .content-section,
  .breakdown-section,
  .state-compare-section,
  .tips-section {
    padding: 1rem;
  }
  .states-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }
  .gender-tabs {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .gender-tab {
    min-width: 0;
  }
  .amount-badge {
    display: inline-block;
    max-width: 100%;
  }
  .breakdown-table,
  .rates-table {
    font-size: 0.8rem;
  }
  .breakdown-table th,
  .breakdown-table td,
  .rates-table th,
  .rates-table td {
    padding: 7px 6px;
  }
}`;
}

function ratesTable(state) {
  if (!state) return "";
  const propNames = {
    residential: "🏠 Residential",
    commercial: "🏢 Commercial",
    agricultural: "🌾 Agricultural"
  };
  let html = `<table class="rates-table"><thead><tr><th>Property type</th><th>Stamp duty</th><th>Registration</th>`;
  if (state.transferDuty > 0) html += `<th>Transfer duty</th>`;
  html += `<th>Total</th></tr></thead><tbody>`;
  Object.entries(state.propertyTypes).forEach(([type, rates]) => {
    const stamp = rates.stamp || rates.male || state.stampDuty.male;
    const reg = rates.reg || state.registrationCharges.male;
    const total = stamp + reg + (state.transferDuty || 0);
    html += `<tr><td>${escapeHTML(propNames[type] || type)}</td><td>${percent(stamp)}</td><td>${percent(reg)}</td>`;
    if (state.transferDuty > 0) html += `<td>${percent(state.transferDuty)}</td>`;
    html += `<td style="font-weight:600;">${percent(total, 2)}</td></tr>`;
  });
  if (state.hasWomenDiscount) {
    html += `<tr class="women-rate-row"><td colspan="5">💝 Women buyers get ${percent(state.womenDiscount)} discount on stamp duty in ${escapeHTML(state.name)}</td></tr>`;
  }
  html += `</tbody></table>`;
  if (state.notes) html += `<p class="rate-note">📌 ${escapeHTML(state.notes)}</p>`;
  return html;
}

function indexRatesTable(data, order) {
  const rows = order.map(slug => {
    const state = data[slug];
    const women = state.hasWomenDiscount ? percent(state.stampDuty.female) : "No broad discount";
    return `<tr><td><a data-state-link data-href="${stateUrl(slug)}" href="${stateUrl(slug)}">${escapeHTML(state.name)}</a></td><td>${percent(state.stampDuty.male)}</td><td>${women}</td><td>${percent(state.registrationCharges.male)}</td><td style="font-weight:600;">${percent(stateTotal(state), 2)}</td></tr>`;
  }).join("");
  return `<table class="rates-table"><thead><tr><th>State / UT</th><th>Men stamp</th><th>Women stamp</th><th>Registration</th><th>Total</th></tr></thead><tbody>${rows}</tbody></table>`;
}

function faqHtml(items) {
  return (items || []).map((item, index) => `<div class="faq-item">
            <button class="faq-q-btn" type="button" aria-expanded="false" aria-controls="faq-a-${index}">
              ${escapeHTML(item.q)} <span class="faq-chevron">▾</span>
            </button>
            <div class="faq-answer" id="faq-a-${index}">${escapeHTML(item.a)}</div>
          </div>`).join("\n");
}

function tariffSummary(state) {
  if (!state) return "";
  return `<div class="tariff-item"><div class="tariff-val">${percent(state.stampDuty.male)}</div><div class="tariff-lbl">Stamp duty (men)</div></div>
          ${state.hasWomenDiscount ? `<div class="tariff-item"><div class="tariff-val tariff-women">${percent(state.stampDuty.female)}</div><div class="tariff-lbl">Stamp duty (women)</div></div>` : ""}
          <div class="tariff-item"><div class="tariff-val">${percent(state.registrationCharges.male)}</div><div class="tariff-lbl">Registration</div></div>
          ${state.transferDuty > 0 ? `<div class="tariff-item"><div class="tariff-val tariff-transfer">${percent(state.transferDuty)}</div><div class="tariff-lbl">Transfer duty</div></div>` : ""}
          <div class="tariff-item"><div class="tariff-val">${percent(stateTotal(state), 2)}</div><div class="tariff-lbl">Total (men)</div></div>`;
}

function pageHtml({ slug, state, data, order }) {
  const isState = Boolean(state);
  const title = isState ? state.seo.title : "India Stamp Duty Calculator 2025 — All States Property Registration | Calculatorcity";
  const description = isState ? state.seo.description : "Calculate stamp duty and registration charges for property purchase in India. Compare all Indian states and UTs with women discounts, transfer duty and registration charges.";
  const canonicalPath = isState ? `/india/stamp-duty/${slug}.html` : "/india/stamp-duty/";
  const h1 = isState ? state.seo.h1 : "Stamp Duty Calculator India";
  const subtitle = isState ? state.seo.subtitle : "Calculate property stamp duty and registration charges for any Indian state instantly.";
  const faqItems = isState ? state.content.faq : defaultFaq;
  const stateColor = "#f97316";
  const stateLight = "#fff7ed";
  const stateBorder = "#fed7aa";
  const schema = faqSchema(faqItems);
  const webappSchema = {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": h1,
    "url": DOMAIN + canonicalPath,
    "description": description,
    "applicationCategory": "CalculatorApplication",
    "operatingSystem": "Any",
    "offers": { "@type": "Offer", "price": "0", "priceCurrency": "INR" }
  };
  const breadcrumbSchema = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/" },
      { "@type": "ListItem", "position": 2, "name": "India Calculators", "item": DOMAIN + "/#india" },
      { "@type": "ListItem", "position": 3, "name": h1, "item": DOMAIN + canonicalPath }
    ]
  };

  const howTitle = isState ? `How is stamp duty calculated in ${state.name}?` : "How is stamp duty calculated in India?";
  const howText = isState ? state.content.howItWorks : `<p>Stamp duty is a state-level tax charged on property transactions in India. Every state sets its own stamp duty rates, which typically range from 3% to 8.25% of the property value. Registration charges are additional fees paid to the state government to officially record the property transfer.</p>
          <p>Stamp duty is calculated on the higher of: (1) the actual transaction value, or (2) the government-declared circle rate (also called guideline value, ready reckoner rate, jantri, collector rate or fair value depending on the state).</p>
          <p>Select your state above to open the dedicated calculator with exact rates, women discounts, transfer duty and state-specific registration guidance.</p>`;

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title id="page-title">${escapeHTML(title)}</title>
  <meta name="description" id="page-meta" content="${escapeHTML(description)}">
  <link rel="icon" href="/assets/icons/favicon.svg" type="image/svg+xml">
  <link rel="canonical" id="page-canonical" href="${DOMAIN + canonicalPath}">
  <meta property="og:title" id="og-title" content="${escapeHTML(title)}">
  <meta property="og:description" id="og-description" content="${escapeHTML(description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" id="og-url" content="${DOMAIN + canonicalPath}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../assets/css/base.css">
  <link rel="stylesheet" href="../../assets/css/layout.css">
  <link rel="stylesheet" href="../../assets/css/components.css">
  <link rel="stylesheet" href="../../assets/css/calculator.css">
  <script type="application/ld+json">${JSON.stringify(webappSchema)}</script>
  <script type="application/ld+json">${JSON.stringify(breadcrumbSchema)}</script>
  <script type="application/ld+json" id="schema-faq">${JSON.stringify(schema, null, 2)}</script>
  <style>
${inlineStyles({ stateColor, stateLight, stateBorder })}
  </style>
  <noscript><style>body{opacity:1!important}</style></noscript>
</head>
<body class="india-page stamp-page">
${header()}
<main id="main" role="main">
  <section class="stamp-hero">
    <div class="page-container">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="../../index.html">Home</a>
        <span>›</span>
        <a href="../../index.html#india">India</a>
        <span>›</span>
        <span id="breadcrumb-current">${escapeHTML(h1)}</span>
      </nav>
      <div class="hero-content">
        <div class="hero-icon" aria-hidden="true">🏛️</div>
        <div>
          <h1 class="hero-h1" id="page-h1">${escapeHTML(h1)}</h1>
          <p class="hero-subtitle" id="page-subtitle">${escapeHTML(subtitle)}</p>
        </div>
      </div>
      <div class="state-selector-wrap">
        <label class="state-label" for="state-select">🗺️ Select your state or UT</label>
        <div class="state-select-wrapper">
          <select id="state-select" class="state-select" aria-label="Select state or union territory"></select>
          <span class="select-arrow" aria-hidden="true">▾</span>
        </div>
      </div>
    </div>
  </section>

  <section class="calc-section">
    <div class="page-container">
      <div class="calc-layout">
        <div class="calc-main-col">
          <div class="state-info-bar" id="state-info-bar" style="${isState ? "" : "display:none;"}">
            <div class="state-info-left">
              <span class="state-flag-big" id="state-flag">${isState ? state.flag : "🏛️"}</span>
              <div>
                <div class="state-info-name" id="state-info-name">${isState ? escapeHTML(state.name) : "Select a state"}</div>
                <div class="state-info-sub" id="state-info-sub">${isState ? `Stamp duty: ${percent(state.stampDuty.male)} • Registration: ${percent(state.registrationCharges.male)}${state.transferDuty ? ` • Transfer duty: ${percent(state.transferDuty)}` : ""}` : "Stamp duty rates"}</div>
              </div>
            </div>
            <div id="state-badges"></div>
          </div>

          <div class="calc-widget-box" id="calc-widget" style="${isState ? "" : "display:none;"}">
            <div class="gender-row">
              <label class="input-label">Buyer type</label>
              <div class="gender-tabs" id="gender-tabs">
                <button class="gender-tab active" data-gender="male" type="button">👨 Male</button>
                <button class="gender-tab women-tab" data-gender="female" type="button">👩 Female</button>
                <button class="gender-tab" data-gender="joint" type="button">👫 Joint</button>
              </div>
            </div>

            <div class="women-discount-badge${isState && state.hasWomenDiscount ? " show" : ""}" id="women-discount-badge">
              <span aria-hidden="true">💝</span>
              <span id="women-discount-text">${isState && state.hasWomenDiscount ? `Women buyers get ${percent(state.womenDiscount)} discount in ${escapeHTML(state.name)} — pay ${percent(state.stampDuty.female)} instead of ${percent(state.stampDuty.male)}` : ""}</span>
            </div>

            <div class="prop-type-row">
              <label class="input-label">Property type</label>
              <div class="prop-tabs" id="prop-tabs">
                <button class="prop-tab active" data-prop="residential" type="button">🏠 Residential</button>
                <button class="prop-tab" data-prop="commercial" type="button">🏢 Commercial</button>
                <button class="prop-tab" data-prop="agricultural" type="button">🌾 Agricultural</button>
              </div>
            </div>

            <div class="urban-rural-row" id="urban-rural-row" style="${isState && state.hasUrbanRural ? "" : "display:none;"}">
              <label class="input-label">Area type</label>
              <div class="toggle-row">
                <span class="toggle-label">Urban</span>
                <label class="toggle-switch">
                  <input type="checkbox" id="rural-toggle">
                  <span class="toggle-slider"></span>
                </label>
                <span class="toggle-label">Rural (lower rate)</span>
              </div>
            </div>

            <div class="calc-input-group">
              <label class="input-label" for="property-value">Property value (₹)</label>
              <div class="amount-input-wrap">
                <span class="rupee-prefix">₹</span>
                <input type="number" id="property-value" class="amount-input" placeholder="e.g. 5000000" min="0" step="100000" data-no-amount-format="true">
                <span class="amount-badge" id="amount-display">Enter value</span>
              </div>
              <p class="amount-helper" id="amount-in-words"></p>
            </div>

            <div class="calc-error" id="calc-error" hidden></div>

            <button class="calc-btn-main" id="calc-btn" type="button">
              <span aria-hidden="true">🏛️</span> Calculate Stamp Duty
            </button>
          </div>

          <div class="results-box" id="results-box" style="display:none;">
            <div class="result-total">
              <div class="result-total-label">Total Registration Cost</div>
              <div class="result-total-value" id="result-total">₹0</div>
              <div class="result-total-meta" id="result-meta">Stamp duty + Registration charges</div>
            </div>

            <div class="women-savings-banner" id="women-savings-banner">
              <span id="women-savings-text"></span>
            </div>

            <div class="breakdown-section">
              <div class="section-title">Cost breakdown</div>
              <table class="breakdown-table">
                <thead>
                  <tr>
                    <th>Component</th>
                    <th>Rate</th>
                    <th style="text-align:right">Amount</th>
                  </tr>
                </thead>
                <tbody id="breakdown-tbody"></tbody>
                <tfoot id="breakdown-tfoot"></tfoot>
              </table>
            </div>

            <div class="state-compare-section">
              <div class="section-title">💰 Same property — other states comparison</div>
              <p style="font-size:0.8rem;color:#64748b;margin-bottom:0;">Click any state to see its full calculator</p>
              <div class="compare-grid" id="compare-grid"></div>
            </div>

            <div class="tips-section" id="tips-section">
              <div class="section-title">💡 Tips to save on stamp duty</div>
              <div id="tips-list"></div>
            </div>
          </div>
        </div>

        <aside class="calc-sidebar-col">
          <div class="sidebar-card" id="rates-summary-card" style="${isState ? "" : "display:none;"}">
            <div class="sidebar-card-title">📋 Quick rates</div>
            <div id="rates-summary"></div>
          </div>
          <div class="sidebar-card">
            <div class="sidebar-card-title">💡 Did you know?</div>
            <div class="quick-fact">Stamp duty is calculated on circle rate or transaction value — whichever is higher</div>
            <div class="quick-fact">Women buyers save 1-2% in many Indian states and UTs</div>
            <div class="quick-fact">Tamil Nadu total: 11% (7% + 4%)</div>
            <div class="quick-fact">Telangana total: 6% (4% + 0.5% + 1.5%)</div>
            <div class="quick-fact">Registration is usually required within 4 months of execution</div>
          </div>
          <div class="ad-slot">
            <ins class="adsbygoogle" data-ad-slot="sidebar-stamp-ad"></ins>
          </div>
        </aside>
      </div>
    </div>
  </section>

  <section class="all-states-section">
    <div class="page-container">
      <h2 style="font-size:1.25rem;font-weight:700;margin-bottom:0.4rem;">Stamp duty calculator — all states &amp; UTs</h2>
      <p style="font-size:0.875rem;color:#64748b;margin-bottom:1.25rem;">Click any state to calculate stamp duty instantly</p>
      <div class="states-grid" id="states-grid"></div>
    </div>
  </section>

  <section class="content-area">
    <div class="page-container" style="max-width:860px;">
      <div class="tariff-summary" id="tariff-summary" style="${isState ? "" : "display:none;"}">
        <div class="section-title" style="margin-bottom:0.75rem;" id="tariff-summary-title">${isState ? `${escapeHTML(state.name)} stamp duty rates 2025` : "Current rates"}</div>
        <div class="tariff-grid" id="tariff-grid">${isState ? tariffSummary(state) : ""}</div>
      </div>

      <div class="content-section">
        <h2 id="content-h2-how">${escapeHTML(howTitle)}</h2>
        <div id="content-how-text">
          ${howText}
        </div>
      </div>

      <div class="content-section" id="content-state-section" style="${isState && state.content.stateSpecific ? "" : "display:none;"}">
        <div id="content-state-text">${isState ? state.content.stateSpecific : ""}</div>
      </div>

      <div class="content-section" id="content-rates-section">
        <h2 id="content-h2-rates">${isState ? `${escapeHTML(state.name)} stamp duty rates — all property types` : "Stamp duty rates comparison — all states &amp; UTs"}</h2>
        <div id="content-rates-table">${isState ? ratesTable(state) : indexRatesTable(data, order)}</div>
      </div>

      <div class="ad-slot ad-slot-horizontal">
        <ins class="adsbygoogle" data-ad-slot="content-stamp-ad"></ins>
      </div>

      <div class="content-section">
        <h2 id="content-h2-faq">${isState ? `${escapeHTML(state.name)} stamp duty — frequently asked questions` : "Frequently asked questions"}</h2>
        <div class="faq-list" id="faq-list">
          ${faqHtml(faqItems)}
        </div>
      </div>
    </div>
  </section>
</main>
${footer()}
<script>
  window.STAMP_DUTY_INITIAL_STATE = ${isState ? JSON.stringify(slug) : "null"};
</script>
<script src="../../assets/js/main.js" defer></script>
<script src="../../assets/js/stamp-duty-data.js" defer></script>
<script src="../../assets/js/stamp-duty.js" defer></script>
</body>
</html>
`;
}

function main() {
  const { data, order } = loadData();
  fs.mkdirSync(OUT_DIR, { recursive: true });
  fs.writeFileSync(path.join(OUT_DIR, "index.html"), pageHtml({ slug: null, state: null, data, order }), "utf8");
  order.forEach(slug => {
    const state = data[slug];
    if (!state) throw new Error(`Missing state data for ${slug}`);
    fs.writeFileSync(path.join(OUT_DIR, `${slug}.html`), pageHtml({ slug, state, data, order }), "utf8");
  });
  console.log(`Generated ${order.length + 1} stamp duty pages in ${path.relative(ROOT, OUT_DIR)}`);
}

main();
