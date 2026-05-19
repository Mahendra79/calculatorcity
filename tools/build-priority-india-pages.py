from __future__ import annotations

import html
import importlib.util
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDIA = ROOT / "india"
DOMAIN = "https://calculatorcity.com"

spec = importlib.util.spec_from_file_location("production_polish", ROOT / "tools" / "production-polish.py")
production = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(production)


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


def sidebar(current: str) -> str:
    links = [item for item in RELATED if item[1] != current][:7]
    items = "".join(f'<li><a href="../india/{href}">{name}</a></li>' for name, href in links)
    return f"""<aside class="calc-sidebar">
  <div class="card sidebar-card"><h3>Related Indian calculators</h3><ul>{items}</ul></div>
  <div class="ad-slot" aria-label="Advertisement"></div>
</aside>"""


def faq_schema(items: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)},
            }
            for q, a in items
        ],
    }


def page(
    filename: str,
    title: str,
    meta: str,
    h1: str,
    intro: str,
    body: str,
    script: str,
    faqs: list[tuple[str, str]],
    chart: bool = False,
) -> str:
    path = f"india/{filename}"
    url = f"{DOMAIN}/{path}"
    webapp = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": h1,
        "url": url,
        "description": meta,
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
            {"@type": "ListItem", "position": 3, "name": h1, "item": url},
        ],
    }
    chart_tag = '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>\n' if chart else ""
    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(meta)}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="/assets/icons/favicon.svg" type="image/svg+xml">
  <link rel="canonical" href="{url}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/base.css">
  <link rel="stylesheet" href="../assets/css/layout.css">
  <link rel="stylesheet" href="../assets/css/components.css">
  <link rel="stylesheet" href="../assets/css/calculator.css">
  <script type="application/ld+json">{json.dumps(webapp, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(faq_schema(faqs), ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(breadcrumb, ensure_ascii=False)}</script>
</head>
<body class="india-page">
{production.nav_for(INDIA / filename)}
<main id="main" class="page-container two-col-layout">
  <article class="calc-main">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="../index.html">Home</a><span><a href="../index.html#india">India Calculators</a></span><span>{html.escape(h1)}</span></nav>
    <p><span class="badge badge-india">🇮🇳 India</span></p>
    <h1>{html.escape(h1)}</h1>
    <p>{intro}</p>
{body}
  </article>
  {sidebar(filename)}
</main>
{production.footer_for(INDIA / filename)}
{chart_tag}<script src="../assets/js/main.js"></script>
<script>
{script}
</script>
</body>
</html>
"""
    return "\n".join(line.rstrip() for line in html_doc.splitlines()) + "\n"


def table(headers: list[str], rows: list[list[str]]) -> str:
    h = "".join(f"<th>{x}</th>" for x in headers)
    r = "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
    return f'<table class="reference-table"><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table>'


def faq_html(items: list[tuple[str, str]]) -> str:
    return '<section class="content-section"><h2>FAQ</h2>' + "\n".join(
        f'<div class="faq-item"><h3 class="faq-question">{q}</h3><div class="faq-answer"><p>{a}</p></div></div>'
        for q, a in items
    ) + "</section>"


def how_to(items: list[str]) -> str:
    return '<ol class="how-to-steps">' + "".join(f"<li>{x}</li>" for x in items) + "</ol>"


COMMON_JS = """
function formatINR(n) {
  if (isNaN(n) || n === null) return '₹0';
  const num = Math.abs(Math.round(n));
  const s = num.toString();
  let result = '';
  if (s.length <= 3) {
    result = s;
  } else {
    result = s.slice(-3);
    let remaining = s.slice(0, -3);
    while (remaining.length > 2) {
      result = remaining.slice(-2) + ',' + result;
      remaining = remaining.slice(0, -2);
    }
    result = remaining + ',' + result;
  }
  return (n < 0 ? '-₹' : '₹') + result;
}
function formatLakhCrore(n) {
  if (n >= 10000000) return '₹' + (n/10000000).toFixed(2) + ' Crore';
  if (n >= 100000) return '₹' + (n/100000).toFixed(2) + ' Lakh';
  return formatINR(n);
}
function num(id) {
  const el = document.getElementById(id);
  return el ? Number(String(el.value || '').replace(/[^\\d.-]/g, '')) || 0 : 0;
}
function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}
function showResultCards(id, rows) {
  const box = document.getElementById(id);
  if (!box) return;
  box.innerHTML = '<div class="result-grid">' + rows.map((r, i) =>
    `<div class="result-card ${i === 0 ? 'highlight' : ''}"><span class="result-value">${r[1]}</span><span class="result-label">${r[0]}</span></div>`
  ).join('') + '</div>';
  box.classList.add('show');
}
function showError(message) {
  alert(message);
}
"""


car_data = {
    "Maruti Suzuki": {
        "Alto K10": {"STD": 349000, "LXi": 399000, "VXi": 449000, "VXi+": 499000, "VXi AGS": 529000},
        "Wagon R": {"LXi 1.0": 579000, "VXi 1.0": 629000, "ZXi 1.0": 699000, "LXi 1.2": 619000, "VXi 1.2": 679000, "ZXi 1.2": 749000, "ZXi+ 1.2": 809000, "ZXi Plus AGS": 849000},
        "Swift": {"LXi": 699000, "VXi": 779000, "ZXi": 889000, "ZXi+": 989000, "VXi AMT": 839000, "ZXi AMT": 939000},
        "Baleno": {"Sigma": 669000, "Delta": 749000, "Zeta": 849000, "Alpha": 989000, "Delta AMT": 799000, "Zeta AMT": 899000},
        "Brezza": {"LXi": 849000, "VXi": 1099000, "ZXi": 1299000, "ZXi+": 1449000, "ZXi+ Dual Tone": 1499000},
        "Ertiga": {"LXi": 849000, "VXi": 999000, "ZXi": 1149000, "ZXi+": 1299000, "ZXi+ AT": 1399000},
        "Grand Vitara": {"Sigma": 1069000, "Delta": 1199000, "Zeta": 1349000, "Alpha": 1699000, "Alpha Hybrid": 1949000},
    },
    "Hyundai": {
        "i20": {"Era 1.2 MT": 749000, "Magna 1.2 MT": 899000, "Sportz 1.2 MT": 1049000, "Asta 1.2 MT": 1149000, "Asta (O) 1.2 MT": 1249000, "Asta Turbo DCT": 1399000},
        "Creta": {"E 1.5 MT": 1099000, "EX 1.5 MT": 1199000, "S 1.5 MT": 1399000, "SX 1.5 MT": 1599000, "SX(O) 1.5 MT": 1799000, "SX(O) Turbo DCT": 1999000},
        "Venue": {"E MT": 799000, "S MT": 999000, "S+ MT": 1099000, "SX MT": 1249000, "SX(O) DCT": 1449000},
        "Verna": {"EX 1.5 MT": 1099000, "S 1.5 MT": 1299000, "S+ 1.5 MT": 1449000, "SX 1.5 MT": 1649000, "SX(O) 1.5 Turbo DCT": 1899000},
        "Alcazar": {"Prestige 1.5 MT": 1699000, "Platinum 1.5 MT": 1849000, "Signature 1.5 MT": 1999000},
    },
    "Tata": {
        "Punch": {"Pure MT": 599000, "Adventure MT": 729000, "Accomplished MT": 849000, "Creative AMT": 999000, "Pure EV": 999000, "Empowered+ EV": 1399000},
        "Nexon": {"Smart MT": 899000, "Pure MT": 999000, "Creative MT": 1249000, "Fearless MT": 1449000, "Creative+ EV": 1449000, "Fearless EV": 1849000},
        "Harrier": {"Smart MT": 1499000, "Pure MT": 1699000, "Creative MT": 1899000, "Fearless MT": 2099000, "Fearless Plus MT": 2499000},
        "Safari": {"Smart MT": 1599000, "Pure MT": 1799000, "Creative MT": 1999000, "Fearless MT": 2199000, "Fearless Plus Dark Edition": 2699000},
        "Altroz": {"XE MT": 649000, "XM MT": 749000, "XT MT": 879000, "XZ MT": 999000, "XZ+ MT": 1099000},
    },
    "Mahindra": {
        "Scorpio N": {"Z2 MT 4×2": 1349000, "Z4 MT 4×2": 1549000, "Z6 MT 4×2": 1999000, "Z8 MT 4×2": 2299000, "Z8 L AT 4×4": 2999000},
        "XUV 3XO": {"MX1": 799000, "MX2": 899000, "MX3": 999000, "AX3": 1099000, "AX5 L": 1299000, "AX7 L": 1499000},
        "XUV700": {"MX 5-seater MT": 1399000, "AX3 MT": 1599000, "AX5 MT": 1999000, "AX7 MT": 2399000, "AX7 L AT": 2699000},
        "Thar": {"LX 4-str Convertible MT": 1599000, "LX Hardtop MT 4×2": 1699000, "LX Hardtop MT 4×4": 1849000, "LX Hardtop AT 4×4": 1999000},
        "BE 6e": {"Pack One": 1899000, "Pack Two": 2199000, "Pack Three": 2499000},
    },
    "Toyota": {
        "Innova Crysta": {"GX MT 7-str": 1949000, "VX MT 7-str": 2249000, "ZX MT 7-str": 2649000, "ZX AT 7-str": 2899000},
        "Fortuner": {"Petrol MT": 3399000, "Diesel MT": 3599000, "Diesel AT": 3899000, "Legender AT": 4299000},
        "Hyryder": {"E MT": 1099000, "S MT": 1299000, "G MT": 1499000, "V MT": 1699000, "G Hybrid": 1899000, "V Hybrid": 2099000},
        "Glanza": {"E MT": 669000, "S MT": 749000, "G MT": 849000, "V AMT": 949000},
    },
    "Honda": {
        "Amaze": {"E MT": 799000, "S MT": 899000, "V MT": 999000, "VX MT": 1099000, "S CVT": 1049000, "VX CVT": 1199000},
        "City": {"V MT": 1149000, "VX MT": 1299000, "ZX MT": 1499000, "V CVT": 1299000, "VX CVT": 1449000, "ZX CVT": 1649000, "e:HEV V": 1949000, "e:HEV ZX": 2149000},
        "Elevate": {"V MT": 1099000, "VX MT": 1299000, "ZX MT": 1499000, "V CVT": 1249000, "VX CVT": 1449000, "ZX CVT": 1649000},
    },
    "Kia": {
        "Sonet": {"HTE MT": 799000, "HTK MT": 899000, "HTK+ MT": 1099000, "HTX MT": 1249000, "HTX+ DCT": 1449000, "GTX+ DCT": 1549000},
        "Seltos": {"HTE MT": 1099000, "HTK MT": 1249000, "HTK+ MT": 1399000, "HTX MT": 1599000, "HTX+ DCT": 1849000, "GTX+ DCT": 1999000},
        "Carens": {"Premium MT 6-str": 1099000, "Prestige MT": 1299000, "Prestige+ MT": 1449000, "Luxury DCT": 1699000},
    },
    "MG": {
        "Hector": {"Style MT": 1399000, "Shine MT": 1599000, "Select MT": 1799000, "Sharp MT": 1999000, "Savvy AT": 2099000},
        "Comet EV": {"Excite": 699000, "Exclusive": 799000, "Essence": 899000},
        "ZS EV": {"Excite": 1899000, "Exclusive": 2099000, "Essence": 2399000},
    },
    "Volkswagen": {
        "Taigun": {"Comfortline MT": 1149000, "Highline MT": 1349000, "Topline DSG": 1749000, "GT DSG": 1899000},
        "Virtus": {"Comfortline MT": 1149000, "Highline MT": 1349000, "Topline DSG": 1649000, "GT DSG": 1849000},
    },
    "Skoda": {
        "Kushaq": {"Active MT": 1149000, "Ambition MT": 1349000, "Style DSG": 1749000, "Monte Carlo DSG": 1899000},
        "Slavia": {"Active MT": 1149000, "Ambition MT": 1349000, "Style DSG": 1649000, "Monte Carlo DSG": 1849000},
    },
}

state_rto = {
    "Andhra Pradesh": {"petrol": 12, "diesel": 14, "electric": 0, "cng": 11, "hybrid": 6, "reg": 1.5, "name": "AP"},
    "Arunachal Pradesh": {"petrol": 4, "diesel": 4, "electric": 0, "cng": 4, "hybrid": 2, "reg": 1, "name": "AR"},
    "Assam": {"petrol": 8, "diesel": 10, "electric": 0, "cng": 8, "hybrid": 4, "reg": 2, "name": "AS"},
    "Bihar": {"petrol": 9, "diesel": 10, "electric": 0, "cng": 8, "hybrid": 4, "reg": 2, "name": "BR"},
    "Chhattisgarh": {"petrol": 8, "diesel": 9, "electric": 0, "cng": 7, "hybrid": 4, "reg": 1, "name": "CG"},
    "Goa": {"petrol": 9, "diesel": 10, "electric": 0, "cng": 9, "hybrid": 5, "reg": 2, "name": "GA"},
    "Gujarat": {"petrol": 6, "diesel": 6, "electric": 0, "cng": 5, "hybrid": 3, "reg": 1, "name": "GJ"},
    "Haryana": {"petrol": 7, "diesel": 7, "electric": 0, "cng": 6, "hybrid": 4, "reg": 2, "name": "HR"},
    "Himachal Pradesh": {"petrol": 3, "diesel": 3, "electric": 0, "cng": 3, "hybrid": 2, "reg": 1, "name": "HP"},
    "Jharkhand": {"petrol": 8, "diesel": 9, "electric": 0, "cng": 8, "hybrid": 4, "reg": 2, "name": "JH"},
    "Karnataka": {"petrol": 13, "diesel": 14, "electric": 0, "cng": 12, "hybrid": 7, "reg": 1, "name": "KA"},
    "Kerala": {"petrol": 8, "diesel": 9, "electric": 0, "cng": 8, "hybrid": 8, "reg": 1, "name": "KL"},
    "Madhya Pradesh": {"petrol": 8, "diesel": 9, "electric": 0, "cng": 8, "hybrid": 4, "reg": 2, "name": "MP"},
    "Maharashtra": {"petrol": 11, "diesel": 13, "electric": 0, "cng": 7, "hybrid": 6, "reg": 1, "name": "MH"},
    "Manipur": {"petrol": 5, "diesel": 5, "electric": 0, "cng": 5, "hybrid": 3, "reg": 1, "name": "MN"},
    "Meghalaya": {"petrol": 5, "diesel": 5, "electric": 0, "cng": 5, "hybrid": 3, "reg": 1, "name": "ML"},
    "Mizoram": {"petrol": 5, "diesel": 5, "electric": 0, "cng": 5, "hybrid": 3, "reg": 1, "name": "MZ"},
    "Nagaland": {"petrol": 5, "diesel": 5, "electric": 0, "cng": 5, "hybrid": 3, "reg": 1, "name": "NL"},
    "Odisha": {"petrol": 8, "diesel": 9, "electric": 0, "cng": 7, "hybrid": 4, "reg": 1, "name": "OD"},
    "Punjab": {"petrol": 8, "diesel": 8, "electric": 0, "cng": 7, "hybrid": 4, "reg": 2, "name": "PB"},
    "Rajasthan": {"petrol": 6, "diesel": 6, "electric": 0, "cng": 5, "hybrid": 3, "reg": 1, "name": "RJ"},
    "Sikkim": {"petrol": 4, "diesel": 4, "electric": 0, "cng": 4, "hybrid": 2, "reg": 1, "name": "SK"},
    "Tamil Nadu": {"petrol": 10, "diesel": 10, "electric": 0, "cng": 9, "hybrid": 5, "reg": 4, "name": "TN"},
    "Telangana": {"petrol": 12, "diesel": 14, "electric": 0, "cng": 11, "hybrid": 6, "reg": 0.5, "name": "TS"},
    "Tripura": {"petrol": 5, "diesel": 5, "electric": 0, "cng": 5, "hybrid": 3, "reg": 1, "name": "TR"},
    "Uttar Pradesh": {"petrol": 8, "diesel": 9, "electric": 0, "cng": 8, "hybrid": 4, "reg": 1, "name": "UP"},
    "Uttarakhand": {"petrol": 5, "diesel": 6, "electric": 0, "cng": 5, "hybrid": 3, "reg": 1, "name": "UK"},
    "West Bengal": {"petrol": 7, "diesel": 7, "electric": 0, "cng": 6, "hybrid": 4, "reg": 1, "name": "WB"},
    "Andaman & Nicobar Islands": {"petrol": 6, "diesel": 6, "electric": 0, "cng": 5, "hybrid": 3, "reg": 1, "name": "AN"},
    "Chandigarh": {"petrol": 6, "diesel": 6, "electric": 0, "cng": 5, "hybrid": 3, "reg": 1, "name": "CH"},
    "Dadra & Nagar Haveli and Daman & Diu": {"petrol": 6, "diesel": 6, "electric": 0, "cng": 5, "hybrid": 3, "reg": 1, "name": "DN"},
    "Delhi": {"petrol": 4, "diesel": 5, "electric": 0, "cng": 4, "hybrid": 2, "reg": 1, "name": "DL"},
    "Jammu & Kashmir": {"petrol": 7, "diesel": 8, "electric": 0, "cng": 6, "hybrid": 4, "reg": 1, "name": "JK"},
    "Ladakh": {"petrol": 3, "diesel": 3, "electric": 0, "cng": 3, "hybrid": 2, "reg": 0.5, "name": "LA"},
    "Lakshadweep": {"petrol": 4, "diesel": 4, "electric": 0, "cng": 4, "hybrid": 2, "reg": 1, "name": "LD"},
    "Puducherry": {"petrol": 8, "diesel": 8, "electric": 0, "cng": 7, "hybrid": 4, "reg": 2, "name": "PY"},
}


def on_road_page() -> str:
    faqs = [
        ("What is on-road price and what does it include?", "On-road price is the amount you actually pay to take delivery and legally drive the car. It starts with ex-showroom price, then adds road tax, registration charges, insurance, number plate or Fastag charges, dealer handling if applicable, and TCS for cars above ₹10 lakh. It can also include optional accessories, extended warranty, RSA, and hypothecation charges if financed. The calculator separates compulsory and optional components so you can compare a dealer quote line by line. Always ask the dealer for a written breakup because bundled packages can hide negotiable charges."),
        ("Which state has the lowest RTO charges in India?", "There is no single permanent lowest state for every vehicle because RTO tax depends on price slab, fuel type, vehicle class, seating capacity, and state policy. In many common private car cases, Delhi, Himachal Pradesh, Ladakh, and some North-Eastern states can look cheaper than high-tax states such as Karnataka, Andhra Pradesh, Telangana, Maharashtra, and Tamil Nadu. Electric vehicles may have zero or reduced road tax in several states. Use the comparison table after calculation to see how the same ex-showroom price changes across states under the assumptions used on this page."),
        ("What is TCS on car purchase?", "TCS means Tax Collected at Source. Under Indian income tax rules, the seller collects 1% TCS when a motor vehicle sale value crosses ₹10 lakh. It is not an extra tax cost forever; it appears in Form 26AS/AIS and can usually be claimed as credit when filing your income tax return, subject to your PAN and return details. Buyers often confuse TCS with GST or road tax, but it is separate from both. This calculator applies 1% TCS when the ex-showroom price is ₹10 lakh or more."),
        ("Can I register a car in a different state to save money?", "Registering in a cheaper state only to save tax is risky if the car is mainly kept or used in another state. RTO rules generally expect registration where the vehicle is ordinarily kept, and long-term use in another state can require re-registration, road tax adjustment, NOC, or penalties depending on local enforcement. Genuine cases such as transfer, work relocation, or residence in another state are different. Before choosing a registration state, consider residence proof, insurance address, loan hypothecation, service access, resale value, and compliance. Savings should not come at the cost of legal uncertainty."),
        ("What is the difference between ex-showroom and on-road price?", "Ex-showroom price is the dealer or manufacturer price before state-level registration costs and insurance. It usually includes factory price, dealer margin, GST, and compensation cess where applicable, but it does not represent the final amount needed to drive away. On-road price is the complete ownership-entry cost after adding RTO road tax, registration, insurance, Fastag, TCS where applicable, and optional dealer charges. A car advertised at ₹8.50 lakh ex-showroom can easily become ₹9.80 lakh to ₹10.80 lakh on-road depending on state and fuel type. Always negotiate using on-road price."),
    ]
    body = f"""
    <section class="calc-widget" style="border-color:#f97316;">
      <div class="calc-step" id="step-car">
        <h3 style="font-size:15px; margin-bottom:12px;">Step 1 — Select your car</h3>
        <div class="result-grid">
          <div class="calc-input-group"><label for="car-brand">Car brand</label><select id="car-brand"><option value="">Select brand</option></select></div>
          <div class="calc-input-group"><label for="car-model">Model</label><select id="car-model" disabled><option value="">Select model first</option></select></div>
          <div class="calc-input-group"><label for="car-variant">Variant</label><select id="car-variant" disabled><option value="">Select model first</option></select></div>
          <div class="calc-input-group"><label for="fuel-type">Fuel type</label><select id="fuel-type"><option value="petrol">Petrol</option><option value="diesel">Diesel</option><option value="cng">CNG</option><option value="electric">Electric (EV)</option><option value="hybrid">Hybrid</option></select></div>
        </div>
        <div class="calc-input-group"><label for="ex-showroom">Ex-showroom price (₹) <span style="font-size:11px; color:var(--text-muted)">— auto-filled when variant selected, or enter manually</span></label><input type="number" id="ex-showroom" placeholder="e.g. 850000" min="100000"></div>
      </div>
      <div class="calc-step" style="margin-top:16px; padding-top:16px; border-top:0.5px solid var(--border);">
        <h3 style="font-size:15px; margin-bottom:12px;">Step 2 — Select state &amp; options</h3>
        <div class="result-grid">
          <div class="calc-input-group"><label for="reg-state">Registration state</label><select id="reg-state"></select></div>
          <div class="calc-input-group"><label for="seating">Seating capacity</label><select id="seating"><option value="upto10">Up to 10 seater (car)</option><option value="above10">Above 10 seater (van/bus)</option></select></div>
        </div>
        <div style="display:flex; gap:16px; flex-wrap:wrap; margin-top:8px;">
          <label style="display:flex; align-items:center; gap:6px; font-size:13px; cursor:pointer;"><input type="checkbox" id="incl-insurance" checked> Include 1st year insurance (~2.5% of IDV)</label>
          <label style="display:flex; align-items:center; gap:6px; font-size:13px; cursor:pointer;"><input type="checkbox" id="incl-fastag" checked> Include Fastag (₹500)</label>
          <label style="display:flex; align-items:center; gap:6px; font-size:13px; cursor:pointer;"><input type="checkbox" id="incl-handling"> Include handling/logistics charges</label>
          <div class="calc-input-group" style="flex:1; min-width:150px;"><label for="handling-amt">Handling charges (₹)</label><input type="number" id="handling-amt" value="7500" placeholder="e.g. 7500"></div>
        </div>
      </div>
      <button class="calc-btn" id="calc-btn" style="background:#f97316; margin-top:16px;">Calculate On-Road Price</button>
      <div class="calc-result" id="calc-result" style="border-color:#f97316; background:#fff7ed; display:none; margin-top:16px;">
        <div style="text-align:center; margin-bottom:14px;"><div style="font-size:28px; font-weight:700; color:#f97316;" id="total-price">—</div><div style="font-size:13px; color:var(--text-secondary);">Total On-Road Price</div><div style="font-size:12px; color:var(--text-muted); margin-top:4px;" id="state-note"></div></div>
        <table style="width:100%; border-collapse:collapse; font-size:13px;" id="breakdown-table"><thead><tr><th style="text-align:left; padding:6px 8px; border-bottom:1px solid #fed7aa; color:#7c2d12;">Component</th><th style="text-align:right; padding:6px 8px; border-bottom:1px solid #fed7aa; color:#7c2d12;">Amount</th><th style="text-align:right; padding:6px 8px; border-bottom:1px solid #fed7aa; color:#7c2d12;">% of ex-showroom</th></tr></thead><tbody id="breakdown-tbody"></tbody></table>
      </div>
    </section>
    <section id="state-comparison" style="display:none; margin-top:20px;">
      <h2>On-Road Price Comparison — All States</h2>
      <p style="color:var(--text-secondary); margin-bottom:8px;" id="comparison-note"></p>
      <p style="font-size:13px; color:var(--text-muted); margin-bottom:12px;">Same car, different state = different price. RTO tax is the biggest variable. Includes standard insurance, Fastag, and TCS where applicable.</p>
      <div style="overflow-x:auto;"><table style="width:100%; border-collapse:collapse; font-size:13px;"><thead><tr style="background:var(--bg-secondary);"><th style="text-align:left; padding:7px 8px; border-bottom:1px solid var(--border);">State</th><th style="text-align:right; padding:7px 8px; border-bottom:1px solid var(--border);">RTO Rate</th><th style="text-align:right; padding:7px 8px; border-bottom:1px solid var(--border);">RTO Tax</th><th style="text-align:right; padding:7px 8px; border-bottom:1px solid var(--border);">On-Road Price</th></tr></thead><tbody id="comparison-tbody"></tbody></table></div>
    </section>
    <section class="content-section"><h2>How to use</h2>{how_to(["Select the car brand, model, and variant so the ex-showroom price is auto-filled.", "Change the fuel type if the selected variant is diesel, CNG, electric, or hybrid.", "Choose the state or union territory where the car will be registered.", "Select optional items such as insurance, Fastag, and handling charges to match the dealer quote.", "Press calculate and compare the full on-road breakup with the all-state comparison table."])}</section>
    <section class="content-section"><h2>Formula</h2><p>The on-road price formula is: ex-showroom price plus state road tax plus registration charges plus insurance plus Fastag plus dealer handling charges plus TCS where applicable, minus any electric vehicle subsidy assumed in the calculator. RTO road tax is the largest variable and is calculated as a percentage of the ex-showroom price based on state and fuel type. Registration charges are a separate state-level percentage or fee. Insurance is estimated at 2.5% of IDV for a first-year comprehensive policy, which is reasonable for comparison but not a final quote.</p><p>TCS is calculated at 1% when the vehicle value crosses ₹10 lakh. It is collected by the seller and appears as tax credit, so it should be reconciled during income tax filing. Dealer handling, accessories, extended warranty, RSA, hypothecation, fancy number fees, and insurance add-ons may change the final invoice. Treat this calculator as a transparent audit of a dealer quote, not as a substitute for the final invoice issued by the showroom or RTO.</p></section>
    <section class="content-section"><h2>Worked example: Maruti Swift ZXi in Andhra Pradesh</h2><p>Suppose you select Maruti Suzuki Swift ZXi with an ex-showroom price of ₹8,89,000 and register it in Andhra Pradesh as a petrol car. AP road tax is estimated at 12%, so road tax is about ₹1,06,680. Registration at 1.5% adds about ₹13,335. First-year comprehensive insurance at 2.5% adds about ₹22,225, and Fastag adds ₹500. Since the car is below ₹10 lakh, TCS does not apply. The estimated on-road price becomes about ₹10,31,740 before optional dealer handling or accessories.</p><p>This example shows why buyers should never compare only ex-showroom prices. A car that appears under ₹9 lakh can cross ₹10 lakh on-road in higher-tax states. When negotiating, ask the dealer to separate mandatory government charges from dealer-controlled add-ons. Insurance can often be compared externally, handling charges may be negotiable, and accessories should be accepted only when they are useful and priced fairly.</p></section>
    <section class="content-section"><h2>Popular car on-road estimates in Andhra Pradesh</h2>{table(["Car", "Ex-showroom", "Fuel", "Approx AP on-road"], [["Maruti Alto K10 VXi", "₹4,49,000", "Petrol", "₹5,24,000"], ["Maruti Swift ZXi", "₹8,89,000", "Petrol", "₹10,32,000"], ["Hyundai i20 Sportz", "₹10,49,000", "Petrol", "₹12,29,000"], ["Tata Punch Adventure", "₹7,29,000", "Petrol", "₹8,47,000"], ["Tata Nexon Creative", "₹12,49,000", "Petrol", "₹14,70,000"], ["Hyundai Creta S", "₹13,99,000", "Petrol", "₹16,48,000"], ["Mahindra XUV700 AX5", "₹19,99,000", "Petrol", "₹23,62,000"], ["Toyota Fortuner Diesel AT", "₹38,99,000", "Diesel", "₹47,25,000"], ["Kia Seltos HTX", "₹15,99,000", "Petrol", "₹18,88,000"], ["MG Comet EV", "₹7,99,000", "Electric", "₹6,69,000 after assumed subsidy"]])}</section>
    <section class="content-section"><h2>Important notes for India</h2><ul class="summary-list"><li>RTO rates and EV concessions change by state notification; verify before payment.</li><li>TCS on cars above ₹10 lakh is a tax credit item, not the same as GST or road tax.</li><li>Insurance premiums vary by IDV, add-ons, claim history, location, and insurer.</li><li>Dealer handling and accessory bundles are not always statutory government charges.</li></ul></section>
    {faq_html(faqs)}
    """
    script = f"""
{COMMON_JS}
(function() {{
const carData = {json.dumps(car_data, ensure_ascii=False)};
const stateRTO = {json.dumps(state_rto, ensure_ascii=False)};
const brandSel = document.getElementById('car-brand');
Object.keys(carData).sort().forEach(brand => {{ const opt = document.createElement('option'); opt.value = brand; opt.textContent = brand; brandSel.appendChild(opt); }});
const stateSel = document.getElementById('reg-state');
const apOpt = document.createElement('option'); apOpt.value = 'Andhra Pradesh'; apOpt.textContent = 'Andhra Pradesh'; stateSel.appendChild(apOpt);
Object.keys(stateRTO).filter(s => s !== 'Andhra Pradesh').sort().forEach(state => {{ const opt = document.createElement('option'); opt.value = state; opt.textContent = state; stateSel.appendChild(opt); }});
brandSel.addEventListener('change', function() {{
  const modelSel = document.getElementById('car-model'); const variantSel = document.getElementById('car-variant');
  modelSel.innerHTML = '<option value="">Select model</option>'; variantSel.innerHTML = '<option value="">Select model first</option>';
  modelSel.disabled = false; variantSel.disabled = true; document.getElementById('ex-showroom').value = '';
  if (!this.value) return;
  Object.keys(carData[this.value]).sort().forEach(model => {{ const opt = document.createElement('option'); opt.value = model; opt.textContent = model; modelSel.appendChild(opt); }});
}});
document.getElementById('car-model').addEventListener('change', function() {{
  const brand = brandSel.value; const variantSel = document.getElementById('car-variant');
  variantSel.innerHTML = '<option value="">Select variant</option>'; variantSel.disabled = false;
  if (!this.value || !brand) return;
  Object.keys(carData[brand][this.value]).forEach(variant => {{ const price = carData[brand][this.value][variant]; const opt = document.createElement('option'); opt.value = price; opt.textContent = `${{variant}} — ${{formatINR(price)}}`; variantSel.appendChild(opt); }});
}});
document.getElementById('car-variant').addEventListener('change', function() {{ if (this.value) document.getElementById('ex-showroom').value = this.value; }});
document.getElementById('calc-btn').addEventListener('click', calculate);
function calculate() {{
  const exShowroom = num('ex-showroom'); const state = document.getElementById('reg-state').value; const fuel = document.getElementById('fuel-type').value;
  const inclInsurance = document.getElementById('incl-insurance').checked; const inclFastag = document.getElementById('incl-fastag').checked; const inclHandling = document.getElementById('incl-handling').checked; const handlingAmt = num('handling-amt');
  if (!exShowroom || exShowroom < 50000) {{ alert('Please enter a valid ex-showroom price'); return; }}
  const rto = stateRTO[state]; const rtoRate = rto[fuel] ?? rto.petrol; const regRate = rto.reg;
  const rtoTax = Math.round(exShowroom * rtoRate / 100); const regCharges = Math.round(exShowroom * regRate / 100); const tcs = exShowroom >= 1000000 ? Math.round(exShowroom * 0.01) : 0;
  const insurance = inclInsurance ? Math.round(exShowroom * 0.025) : 0; const fastag = inclFastag ? 500 : 0; const handling = inclHandling ? handlingAmt : 0; const evSubsidy = fuel === 'electric' ? -150000 : 0;
  const total = exShowroom + rtoTax + regCharges + tcs + insurance + fastag + handling + evSubsidy;
  setText('total-price', formatINR(total)); setText('state-note', `Registered in ${{state}} | Fuel: ${{fuel.toUpperCase()}} | RTO: ${{rtoRate}}%`);
  const rows = [
    {{ label: 'Ex-Showroom Price', amount: exShowroom, note: 'Base price from dealer' }},
    {{ label: `RTO Road Tax (${{rtoRate}}%)`, amount: rtoTax, note: `${{state}} ${{fuel}} rate` }},
    {{ label: `Registration Charges (${{regRate}}%)`, amount: regCharges, note: 'State registration' }},
    ...(tcs > 0 ? [{{ label: 'TCS (1% above ₹10L)', amount: tcs, note: 'Tax Collected at Source' }}] : []),
    ...(insurance > 0 ? [{{ label: 'Comprehensive Insurance (1yr)', amount: insurance, note: '~2.5% of IDV' }}] : []),
    ...(fastag > 0 ? [{{ label: 'Fastag', amount: fastag, note: 'Mandatory' }}] : []),
    ...(handling > 0 ? [{{ label: 'Handling / Logistics', amount: handling, note: 'Dealer charges' }}] : []),
    ...(evSubsidy < 0 ? [{{ label: 'FAME-II Subsidy', amount: evSubsidy, note: 'Approx EV subsidy assumption' }}] : []),
    {{ label: 'TOTAL ON-ROAD PRICE', amount: total, bold: true }},
  ];
  const tbody = document.getElementById('breakdown-tbody'); tbody.innerHTML = '';
  rows.forEach(row => {{
    const pct = row.label === 'TOTAL ON-ROAD PRICE' ? '100%' : ((Math.abs(row.amount) / exShowroom) * 100).toFixed(1) + '%';
    const tr = document.createElement('tr');
    tr.innerHTML = `<td style="padding:6px 8px; border-bottom:0.5px solid #fed7aa; ${{row.bold ? 'font-weight:600; background:#fff7ed;' : ''}}">${{row.label}}${{row.note ? `<span style="font-size:11px; color:var(--text-muted); display:block;">${{row.note}}</span>` : ''}}</td><td style="text-align:right; padding:6px 8px; border-bottom:0.5px solid #fed7aa; ${{row.bold ? 'font-weight:700; font-size:15px; background:#fff7ed; color:#c2410c;' : ''}} ${{row.amount < 0 ? 'color:#16a34a;' : ''}}">${{row.amount < 0 ? '-' : ''}}${{formatINR(Math.abs(row.amount))}}</td><td style="text-align:right; padding:6px 8px; border-bottom:0.5px solid #fed7aa; color:var(--text-muted); font-size:12px; ${{row.bold ? 'background:#fff7ed;' : ''}}">${{pct}}</td>`;
    tbody.appendChild(tr);
  }});
  document.getElementById('calc-result').style.display = 'block';
  renderStateComparison(exShowroom, fuel);
}}
function renderStateComparison(exShowroom, fuel) {{
  const container = document.getElementById('state-comparison');
  const results = Object.entries(stateRTO).map(([state, rto]) => {{ const rtoRate = rto[fuel] ?? rto.petrol; const rtoTax = exShowroom * rtoRate / 100; const regCharges = exShowroom * rto.reg / 100; const insurance = exShowroom * 0.025; const fastag = 500; const tcs = exShowroom >= 1000000 ? exShowroom * 0.01 : 0; const total = exShowroom + rtoTax + regCharges + insurance + fastag + tcs; return {{ state, total: Math.round(total), rtoRate, rtoTax: Math.round(rtoTax) }}; }}).sort((a, b) => a.total - b.total);
  const cheapest = results[0]; const mostExpensive = results[results.length - 1]; const savings = mostExpensive.total - cheapest.total;
  container.style.display = 'block'; setText('comparison-note', `Buying in ${{cheapest.state}} saves you ${{formatINR(savings)}} vs buying in ${{mostExpensive.state}}`);
  const tbody = document.getElementById('comparison-tbody'); tbody.innerHTML = '';
  results.forEach((r, i) => {{ const tr = document.createElement('tr'); const isCheapest = i === 0; const isMostExpensive = i === results.length - 1; tr.innerHTML = `<td style="padding:5px 8px; border-bottom:0.5px solid var(--border); ${{isCheapest ? 'color:#16a34a; font-weight:500;' : isMostExpensive ? 'color:#dc2626;' : ''}}">${{isCheapest ? '✓ ' : isMostExpensive ? '⚠ ' : ''}}${{r.state}}</td><td style="text-align:right; padding:5px 8px; border-bottom:0.5px solid var(--border);">${{r.rtoRate}}%</td><td style="text-align:right; padding:5px 8px; border-bottom:0.5px solid var(--border);">${{formatINR(r.rtoTax)}}</td><td style="text-align:right; padding:5px 8px; border-bottom:0.5px solid var(--border); font-weight:500; ${{isCheapest ? 'color:#16a34a;' : isMostExpensive ? 'color:#dc2626;' : ''}}">${{formatINR(r.total)}}</td>`; tbody.appendChild(tr); }});
}}
}})();
"""
    return page(
        "on-road-price-calculator.html",
        "On-Road Price Calculator India — Car On-Road Price 2025 | CalcHub",
        "Calculate on-road price of any car in India. Select car brand, model, variant and state to get complete breakup of RTO, insurance, TCS and other charges. Free and accurate.",
        "Car On-Road Price Calculator India",
        "The on-road price calculator gives you the complete cost of buying any car in India — beyond just the showroom price. It adds RTO registration charges, which vary by state, first-year comprehensive insurance, Fastag, TCS for cars above ₹10 lakh, and handling charges. The on-road price can be 15–25% higher than the ex-showroom price depending on which state you register the car in.",
        body,
        script,
        faqs,
    )


universities = {
    "CBSE (Class 10 & 12)": {"formula": "cgpa * 9.5", "multiplier": 9.5, "additive": 0, "scale": 10, "example": "CGPA 8.0 = 76%", "note": "Official CBSE formula. Applicable for Class 10 board results.", "states": ["All India"]},
    "VTU (Visvesvaraya Technological University)": {"formula": "cgpa * 10", "multiplier": 10, "additive": 0, "scale": 10, "example": "CGPA 8.0 = 80%", "note": "VTU Belagavi formula. Used for B.E/B.Tech results from VTU.", "states": ["Karnataka"]},
    "Anna University": {"formula": "(cgpa - 0.5) * 10", "multiplier": 10, "additive": -0.5, "scale": 10, "example": "CGPA 8.0 = 75%", "note": "Anna University Chennai formula for B.E/B.Tech.", "states": ["Tamil Nadu"]},
    "JNTU Hyderabad": {"formula": "cgpa * 10", "multiplier": 10, "additive": 0, "scale": 10, "example": "CGPA 8.0 = 80%", "note": "JNTU Hyderabad formula for B.Tech programs.", "states": ["Telangana"]},
    "JNTU Kakinada": {"formula": "cgpa * 10", "multiplier": 10, "additive": 0, "scale": 10, "example": "CGPA 8.0 = 80%", "note": "JNTUK formula for B.Tech programs in Andhra Pradesh.", "states": ["Andhra Pradesh"]},
    "JNTU Anantapur": {"formula": "cgpa * 10", "multiplier": 10, "additive": 0, "scale": 10, "example": "CGPA 8.0 = 80%", "note": "JNTUA formula for B.Tech programs.", "states": ["Andhra Pradesh"]},
    "Mumbai University": {"formula": "cgpa * 7.1 + 11", "multiplier": 7.1, "additive": 11, "scale": 10, "example": "CGPA 8.0 = 67.8%", "note": "Mumbai University formula. Unique additive formula.", "states": ["Maharashtra"]},
    "Pune University (SPPU)": {"formula": "cgpa * 10", "multiplier": 10, "additive": 0, "scale": 10, "example": "CGPA 8.0 = 80%", "note": "Savitribai Phule Pune University formula.", "states": ["Maharashtra"]},
    "Delhi University": {"formula": "(cgpa / 10) * 100", "multiplier": 10, "additive": 0, "scale": 10, "example": "CGPA 8.0 = 80%", "note": "DU uses a 10-point scale. Conversion varies by department.", "states": ["Delhi"]},
    "Osmania University": {"formula": "cgpa * 10", "multiplier": 10, "additive": 0, "scale": 10, "example": "CGPA 8.0 = 80%", "note": "Osmania University Hyderabad formula.", "states": ["Telangana"]},
    "Andhra University": {"formula": "cgpa * 10", "multiplier": 10, "additive": 0, "scale": 10, "example": "CGPA 8.0 = 80%", "note": "Andhra University Visakhapatnam formula.", "states": ["Andhra Pradesh"]},
    "Calicut University": {"formula": "cgpa * 10", "multiplier": 10, "additive": 0, "scale": 10, "example": "CGPA 8.0 = 80%", "note": "University of Calicut formula for UG programs.", "states": ["Kerala"]},
    "Bangalore University": {"formula": "cgpa * 10", "multiplier": 10, "additive": 0, "scale": 10, "example": "CGPA 8.0 = 80%", "note": "Bangalore University formula.", "states": ["Karnataka"]},
    "Custom / Other University": {"formula": "custom", "multiplier": None, "additive": 0, "scale": 10, "example": "Enter your multiplier", "note": "If your university is not listed, enter the multiplier manually.", "states": ["All India"]},
}


def cgpa_page() -> str:
    faqs = [
        ("What is CGPA and how is it different from percentage?", "CGPA means Cumulative Grade Point Average. It is an average of grade points across subjects or semesters, usually on a 10-point scale in India. Percentage expresses marks out of 100. They are related but not identical because CGPA compresses marks into grade bands, while percentage is a direct numeric scale. Universities therefore publish conversion rules for jobs, higher studies, scholarships, and government applications. A CGPA of 8.0 can become 76%, 80%, 75%, or 67.8% depending on the university formula, so always use the rule printed by your board or university."),
        ("Why does each university use a different conversion formula?", "Indian universities design grading systems independently. Some use a simple multiplier such as CGPA × 10 because the grade scale is intended to map directly to percentage. CBSE uses 9.5 because it was derived from historical performance of students under the board’s grading system. Mumbai University uses CGPA × 7.1 + 11, which produces lower percentages for the same CGPA than many engineering universities. These differences are not mistakes; they reflect academic regulations. For official submissions, attach the university conversion certificate or refer to the regulation page if asked."),
        ("Which formula does CBSE use for CGPA to percentage?", "CBSE commonly uses CGPA × 9.5 for Class 10 board result conversion. For example, a CGPA of 8.0 becomes 76%, and a CGPA of 9.5 becomes 90.25%. This formula is widely accepted for CBSE school records, but students should still check the current marksheet, migration certificate, or school instructions when applying to colleges or jobs. If a form asks for marks obtained and total marks rather than percentage, do not force a CGPA conversion. Use the format requested by the institution or recruitment notice."),
        ("How do I convert CGPA for a government job application?", "For government jobs, read the official notification carefully. Many recruitment forms ask for percentage and specify that candidates must use the formula prescribed by their university or board. Select your university in this calculator and use that percentage, but keep proof ready. If your university has a conversion certificate, upload or produce it when required. If the university is not listed, use the custom multiplier only when you know the exact official rule. Do not choose a formula that gives a higher percentage simply because it looks more favorable; that can create document-verification issues later."),
        ("Is CGPA 8.0 a good score for placement?", "A CGPA of 8.0 is generally considered strong in many Indian engineering, commerce, and science programs, especially when the minimum placement cutoff is 6.5 or 7.0. However, its meaning depends on the university, branch, grading strictness, and recruiter criteria. In CBSE it converts to 76%; in VTU or JNTU it converts to 80%; in Anna University it becomes 75%; and in Mumbai University it becomes 67.8%. Recruiters often look at projects, internships, coding skills, communication, and consistency along with CGPA. Use percentage conversion for eligibility, not as the only measure of readiness."),
    ]
    body = f"""
    <section class="calc-widget" style="border-color:#f97316;">
      <div class="field-grid">
        <div class="calc-input-group"><label for="cgpa">CGPA</label><input id="cgpa" type="number" min="0" max="10" step="0.01" value="8.00"></div>
        <div class="calc-input-group"><label for="university">University / Board</label><select id="university"></select></div>
        <div class="calc-input-group" id="custom-wrap" style="display:none;"><label for="custom-multiplier">Custom multiplier</label><input id="custom-multiplier" type="number" step="0.01" value="10"></div>
      </div>
      <button class="calc-btn" id="calculate" style="background:#f97316;">Convert CGPA to Percentage</button>
      <div class="calc-result show" id="cgpa-result"></div>
      <div style="margin-top:18px; padding-top:16px; border-top:0.5px solid var(--border);">
        <h3 style="font-size:15px; margin-bottom:12px;">Reverse calculator — Percentage to CGPA</h3>
        <div class="field-grid"><div class="calc-input-group"><label for="percentage">Percentage</label><input id="percentage" type="number" min="0" max="100" step="0.01" value="80"></div><div class="calc-input-group"><label for="reverse-university">University / Board</label><select id="reverse-university"></select></div></div>
        <button class="calc-btn" id="reverse-btn" type="button" style="background:#f97316;">Convert Percentage to CGPA</button>
        <div class="calc-result" id="reverse-result"></div>
      </div>
    </section>
    <section id="university-comparison" class="content-section"><h2>Compare across universities</h2><p id="comparison-summary" style="color:var(--text-secondary);"></p><div style="overflow-x:auto;"><table class="reference-table"><thead><tr><th>University</th><th>Formula</th><th>Converted percentage</th><th>Notes</th></tr></thead><tbody id="comparison-body"></tbody></table></div></section>
    <section class="content-section"><h2>How to use</h2>{how_to(["Enter your CGPA exactly as shown on your marksheet.", "Select your university, board, or custom formula option.", "Use custom multiplier only when your institution has published a specific conversion rule.", "Review the percentage, class, formula, and comparison table.", "Use the reverse calculator when a job form gives percentage and you need an approximate CGPA."])}</section>
    <section class="content-section"><h2>Formula explanation</h2><p>CGPA conversion is not a universal mathematical truth; it is an academic rule. CBSE multiplies CGPA by 9.5. VTU, JNTU Hyderabad, JNTU Kakinada, JNTU Anantapur, Pune University, Osmania University, Andhra University, Calicut University, Bangalore University, and many other universities commonly use CGPA × 10. Anna University uses (CGPA − 0.5) × 10, which means an 8.0 CGPA becomes 75%. Mumbai University uses CGPA × 7.1 + 11, so the same 8.0 CGPA becomes 67.8%.</p><p>The calculator uses these formulas exactly as listed, then caps percentage between 0 and 100 for practical display. For official documents, the university’s latest regulation, marksheet note, or conversion certificate should be treated as final. If your institution changed grading rules in a particular regulation year, use the rule that applies to your batch.</p></section>
    <section class="content-section"><h2>Using CGPA in Indian applications</h2><p>For Indian campus placements, private job portals, government recruitment forms, foreign university applications, and scholarship portals, enter marks in the same format requested by the form. If the form asks for percentage, convert using your university’s official formula and keep the proof ready for document verification. If the form has separate boxes for CGPA and scale, enter the CGPA exactly as printed and use 10 as the scale unless your marksheet uses a different maximum. For semester-wise forms, do not average percentages after converting each SGPA unless the university tells you to do so. The safest practice is to use final CGPA from the consolidated marks memo, the published conversion rule, and the same rounded percentage everywhere in your application documents.</p></section>
    <section class="content-section"><h2>Reference table: CGPA to percentage</h2><div style="overflow-x:auto;">{table(["CGPA", "CBSE", "VTU", "Anna University", "JNTU"], [[str(x), f"{x*9.5:.2f}%", f"{x*10:.2f}%", f"{(x-0.5)*10:.2f}%", f"{x*10:.2f}%"] for x in [10, 9.5, 9, 8.5, 8, 7.5, 7, 6.5, 6]])}</div></section>
    <section class="content-section"><h2>Grade classification table</h2>{table(["Percentage", "Class", "CGPA (CBSE approx)"], [["90–100%", "Outstanding / O", "9.5–10"], ["75–89%", "First Class with Distinction", "7.9–9.4"], ["60–74%", "First Class", "6.3–7.8"], ["50–59%", "Second Class", "5.3–6.2"], ["40–49%", "Pass Class", "4.2–5.2"], ["Below 40%", "Fail", "Below 4.2"]])}</section>
    <section class="content-section"><h2>Important notes for India</h2><ul class="summary-list"><li>Use the formula printed on your university marksheet or conversion certificate where available.</li><li>Government job forms may ask for percentage, CGPA, or both; follow the notification wording.</li><li>Some universities use different rules for older regulation batches.</li><li>Do not mix semester GPA, SGPA, and final CGPA unless the form specifically allows it.</li></ul></section>
    {faq_html(faqs)}
    """
    script = f"""
{COMMON_JS}
(function() {{
const universities = {json.dumps(universities, ensure_ascii=False)};
const uSel = document.getElementById('university');
const rSel = document.getElementById('reverse-university');
Object.keys(universities).forEach(name => {{ uSel.add(new Option(name, name)); rSel.add(new Option(name, name)); }});
function convert(name, cgpa) {{
  const u = universities[name];
  if (u.formula === 'custom') return cgpa * num('custom-multiplier');
  if (name === 'Anna University') return (cgpa - 0.5) * 10;
  if (name === 'Mumbai University') return cgpa * 7.1 + 11;
  return cgpa * u.multiplier;
}}
function reverse(name, pct) {{
  const u = universities[name];
  if (u.formula === 'custom') return pct / num('custom-multiplier');
  if (name === 'Anna University') return pct / 10 + 0.5;
  if (name === 'Mumbai University') return (pct - 11) / 7.1;
  return pct / u.multiplier;
}}
function gradeClass(p) {{ if (p >= 90) return 'Outstanding / O'; if (p >= 75) return 'First Class with Distinction'; if (p >= 60) return 'First Class'; if (p >= 50) return 'Second Class'; if (p >= 40) return 'Pass Class'; return 'Fail'; }}
function calculate() {{
  const cgpa = num('cgpa'); const name = uSel.value;
  document.getElementById('custom-wrap').style.display = name === 'Custom / Other University' ? 'block' : 'none';
  if (cgpa < 0 || cgpa > 10) {{ showError('Enter CGPA between 0 and 10'); return; }}
  const pct = Math.min(100, Math.max(0, convert(name, cgpa)));
  const u = universities[name];
  showResultCards('cgpa-result', [['Percentage', pct.toFixed(2) + '%'], ['Grade class', gradeClass(pct)], ['Formula used', u.formula === 'custom' ? 'CGPA × custom multiplier' : u.formula], ['Scale', u.scale + '-point scale']]);
  renderComparison(cgpa, name);
}}
function reverseCalc() {{
  const pct = num('percentage'); const name = rSel.value;
  const cgpa = Math.min(10, Math.max(0, reverse(name, pct)));
  showResultCards('reverse-result', [['Approx CGPA', cgpa.toFixed(2)], ['University', name], ['Input percentage', pct.toFixed(2) + '%'], ['Formula', universities[name].formula]]);
}}
function renderComparison(cgpa, selected) {{
  const rows = Object.keys(universities).filter(n => universities[n].formula !== 'custom').map(name => ({{ name, pct: Math.min(100, Math.max(0, convert(name, cgpa))), u: universities[name] }}));
  const hi = rows.reduce((a,b) => b.pct > a.pct ? b : a); const lo = rows.reduce((a,b) => b.pct < a.pct ? b : a);
  setText('comparison-summary', `Your CGPA ${{cgpa.toFixed(2)}} ranges from ${{lo.pct.toFixed(2)}}% at ${{lo.name}} to ${{hi.pct.toFixed(2)}}% at ${{hi.name}}.`);
  const tbody = document.getElementById('comparison-body'); tbody.innerHTML = '';
  rows.forEach(r => {{ const tr = document.createElement('tr'); const selectedStyle = r.name === selected ? 'background:#fff7ed; font-weight:600;' : ''; tr.innerHTML = `<td style="${{selectedStyle}}">${{r.name}}</td><td>${{r.u.formula}}</td><td style="${{selectedStyle}}">${{r.pct.toFixed(2)}}%</td><td>${{r.u.note}}</td>`; tbody.appendChild(tr); }});
}}
uSel.addEventListener('change', calculate);
document.getElementById('calculate').addEventListener('click', calculate);
document.getElementById('reverse-btn').addEventListener('click', reverseCalc);
window.addEventListener('load', () => {{ calculate(); reverseCalc(); }});
}})();
"""
    return page(
        "cgpa-to-percentage-calculator.html",
        "CGPA to Percentage Calculator — All Indian Universities | CalcHub",
        "Convert CGPA to percentage for CBSE, VTU, Anna University, JNTU, Mumbai University, Pune University and 15+ Indian universities. Also converts percentage to CGPA.",
        "CGPA to Percentage Calculator",
        "The CGPA to percentage calculator converts your Cumulative Grade Point Average to a percentage for all major Indian universities and boards. Each university uses a different multiplier formula — CBSE uses CGPA × 9.5, while VTU and JNTU Hyderabad use CGPA × 10. This matters when applying for jobs, higher education, or government exams where percentage is required. Enter your CGPA, select your university, and get the exact conversion with the formula used.",
        body,
        script,
        faqs,
    )


def epf_page() -> str:
    faqs = [
        ("What is the current EPF interest rate?", "The calculator uses 8.25% as the default EPF interest rate, matching the rate announced for recent EPFO calculations. EPF interest is declared by EPFO and credited after government approval, so the rate can change for future financial years. Use the editable interest-rate field if EPFO notifies a different rate or if you want to compare conservative and optimistic scenarios. The declared rate is annual, but interest is generally calculated on the monthly running balance and credited annually. For final balance, always compare the calculator with your EPFO passbook."),
        ("What is the difference between EPF and EPS?", "EPF is the provident fund savings account where employee contribution and part of employer contribution accumulate with interest. EPS is the Employees’ Pension Scheme, funded from the employer contribution, and it is meant to provide pension benefits subject to eligibility rules. For most employees, 12% of Basic + DA is deducted from salary as employee EPF contribution. The employer also contributes 12%, but 8.33% goes to EPS and 3.67% goes to EPF, subject to wage ceiling rules. This calculator shows EPF corpus and an approximate EPS pension estimate separately."),
        ("Can I withdraw EPF before retirement?", "EPF is designed for retirement, but partial withdrawals are permitted for specific reasons such as housing, illness, education, marriage, unemployment, and certain emergencies, subject to EPFO rules and service conditions. Full withdrawal is generally allowed after retirement or after a qualifying period of unemployment. Frequent withdrawals reduce compounding and can sharply reduce retirement corpus. Before withdrawing, check whether a loan, emergency fund, or partial claim is more appropriate. Use this calculator to see the future cost of taking money out early, then verify eligibility on the EPFO portal."),
        ("Is EPF interest taxable?", "EPF usually has EEE-style tax treatment for many employees: contribution can qualify for deduction under Section 80C, interest is generally tax-free within applicable limits, and withdrawal after five years of continuous service is usually tax-free. However, tax rules changed for high employee contributions; interest on employee contribution above specified annual limits can become taxable. Employer contribution above prescribed limits can also have tax implications. If you are a high-income employee, contribute heavily through VPF, or have job changes and withdrawals before five years, check with a tax professional."),
        ("How do I check my EPF balance online?", "You can check EPF balance through the EPFO member passbook portal, UMANG app, SMS, missed call facility, or through employer-provided payroll records. You generally need an activated UAN linked with Aadhaar, PAN, mobile number, and bank details for smooth access and claims. The EPFO passbook shows employee contribution, employer EPF contribution, pension contribution, interest credit, transfers, and withdrawals. This calculator is useful for projection, but your passbook is the official record. Reconcile your salary slips with passbook entries at least once or twice a year."),
    ]
    body = f"""
    <section class="calc-widget" style="border-color:#f97316;">
      <div class="field-grid">
        <div class="calc-input-group"><label for="current-age">Current age</label><input id="current-age" type="number" value="30"></div>
        <div class="calc-input-group"><label for="retirement-age">Retirement age</label><input id="retirement-age" type="number" value="58"></div>
        <div class="calc-input-group"><label for="basic-salary">Monthly Basic + DA salary (₹)</label><input id="basic-salary" type="number" value="50000"></div>
        <div class="calc-input-group"><label for="current-balance">Current EPF balance (₹)</label><input id="current-balance" type="number" value="0"></div>
        <div class="calc-input-group"><label for="increment">Expected annual salary increment (%)</label><input id="increment" type="number" step="0.1" value="8"></div>
        <div class="calc-input-group"><label for="interest-rate">EPF interest rate (%)</label><input id="interest-rate" type="number" step="0.01" value="8.25"></div>
      </div>
      <button class="calc-btn" id="calculate" style="background:#f97316;">Calculate EPF corpus</button>
      <div class="calc-result show" id="epf-results"></div>
      <div class="chart-container"><canvas id="epf-chart"></canvas></div>
    </section>
    <section class="content-section"><h2>Compare EPF contribution scenarios</h2><p style="color:var(--text-secondary);">Use this table to see how salary increment and interest assumptions change the retirement corpus. It keeps the same current age, retirement age, salary, and opening balance.</p><div style="overflow-x:auto;"><table class="reference-table"><thead><tr><th>Scenario</th><th>Increment</th><th>Interest rate</th><th>Projected corpus</th></tr></thead><tbody id="scenario-body"></tbody></table></div></section>
    <section class="content-section"><h2>Year-wise EPF balance</h2><div style="overflow-x:auto;"><table class="reference-table"><thead><tr><th>Year</th><th>Age</th><th>Monthly salary</th><th>Annual contribution</th><th>Interest earned</th><th>EPF balance</th></tr></thead><tbody id="year-body"></tbody></table></div></section>
    <section class="content-section"><h2>What is EPF and EPS?</h2><p>EPF is the long-term retirement savings account managed through the Employees’ Provident Fund Organisation. The employee contributes 12% of Basic + DA every month. The employer also contributes 12%, but the split is not identical: a portion goes to EPF and a portion goes to EPS, the pension scheme. EPF earns annual interest and builds a lump-sum retirement corpus. EPS does not accumulate like a savings account in the same way; it supports pension eligibility based on service and pensionable salary rules.</p><p>This distinction matters because employees often assume the full employer 12% goes into EPF balance. In the standard split, 3.67% goes to EPF and 8.33% goes to EPS, subject to wage ceiling and statutory rules. Your passbook shows both components separately.</p></section>
    <section class="content-section"><h2>How EPF interest is calculated</h2><p>EPF interest is based on the monthly running balance. A simplified year projection can estimate interest on opening balance plus roughly half of annual contributions, because contributions are added throughout the year. The official calculation works month by month and interest is credited annually after the rate is declared. This calculator follows a transparent projection model: it increases salary each year by the increment rate, calculates employee and employer EPF contributions, estimates interest, and carries the closing balance to the next year.</p></section>
    <section class="content-section"><h2>Checking EPF against your salary slip</h2><p>To verify your PF deduction, first find Basic + DA on the monthly salary slip. Employee PF should normally be 12% of that amount, unless your organisation uses a wage ceiling or a specific PF structure. Then compare the employer EPF and EPS entries in the EPFO passbook, because the employer contribution is split between the provident fund and pension scheme. If the passbook does not match payroll for several months, ask HR to confirm UAN mapping, wage ceiling treatment, date of joining, and whether arrears were posted later. Small timing differences are common, but missing contributions should be resolved early.</p></section>
    <section class="content-section"><h2>Tax benefits and withdrawal rules</h2><p>EPF is one of India’s strongest salary-linked retirement products because it combines disciplined monthly savings, employer contribution, and tax-friendly treatment. Employee contribution can qualify under Section 80C, interest is generally tax-free within applicable limits, and withdrawal after five years of continuous service is usually tax-free. Premature withdrawal, high employee contributions, and employer contribution above prescribed limits can change tax treatment. Partial withdrawals are allowed for defined purposes such as housing, illness, marriage, education, or unemployment, but they reduce compounding.</p></section>
    <section class="content-section"><h2>EPF interest rates for last 10 years</h2>{table(["Financial year", "EPF interest rate"], [["2024-25", "8.25%"], ["2023-24", "8.25%"], ["2022-23", "8.15%"], ["2021-22", "8.10%"], ["2020-21", "8.50%"], ["2019-20", "8.50%"], ["2018-19", "8.65%"], ["2017-18", "8.55%"], ["2016-17", "8.65%"], ["2015-16", "8.80%"]])}</section>
    <section class="content-section"><h2>Important notes for India</h2><ul class="summary-list"><li>EPF rate is declared by EPFO and may be credited after government approval.</li><li>Employer EPS contribution rules can depend on wage ceiling and employee category.</li><li>High VPF or employee contribution can create taxable interest under current rules.</li><li>The EPFO passbook is the official balance; this calculator is a projection tool.</li></ul></section>
    {faq_html(faqs)}
    """
    script = f"""
{COMMON_JS}
(function() {{
let chart;
function project(incrementOverride, rateOverride) {{
  const currentAge = parseInt(document.getElementById('current-age').value);
  const retirementAge = parseInt(document.getElementById('retirement-age').value);
  const basicSalary = num('basic-salary'); const currentBalance = num('current-balance');
  const increment = (incrementOverride ?? num('increment')) / 100; const interestRate = (rateOverride ?? num('interest-rate')) / 100;
  const years = retirementAge - currentAge; let balance = currentBalance; let salary = basicSalary; const yearData = [];
  for (let y = 1; y <= years; y++) {{
    const empContrib = salary * 0.12; const emplContrib = salary * 0.0367; const monthlyTotal = empContrib + emplContrib; const annualContrib = monthlyTotal * 12; const interestEarned = (balance + annualContrib / 2) * interestRate;
    balance += annualContrib + interestEarned;
    yearData.push({{ year: y, age: currentAge + y, salary: Math.round(salary), annualContrib: Math.round(annualContrib), interest: Math.round(interestEarned), balance: Math.round(balance) }});
    salary *= (1 + increment);
  }}
  return {{ years, balance, basicSalary, yearData }};
}}
function calculateEPF() {{
  const currentAge = parseInt(document.getElementById('current-age').value); const retirementAge = parseInt(document.getElementById('retirement-age').value); const basicSalary = num('basic-salary');
  const out = project(); if (out.years <= 0) {{ showError('Retirement age must be greater than current age'); return; }}
  const monthlyEPS = Math.min((basicSalary * out.years) / 70, 7500);
  showResultCards('epf-results', [['EPF Corpus at Retirement', formatLakhCrore(out.balance)], ['Monthly Employee PF', formatINR(basicSalary * 0.12)], ['Monthly Employer PF', formatINR(basicSalary * 0.0367)], ['Total Monthly PF', formatINR(basicSalary * 0.1567)], ['Est. Monthly EPS Pension', formatINR(monthlyEPS)], ['Years to Retirement', out.years + ' years']]);
  renderYearTable(out.yearData); renderScenarios(); drawChart(out.yearData);
}}
function drawChart(data) {{
  if (typeof Chart === 'undefined') return; const ctx = document.getElementById('epf-chart'); if (chart) chart.destroy();
  chart = new Chart(ctx, {{ type: 'bar', data: {{ labels: data.map(d => 'Age ' + d.age), datasets: [{{ label: 'Annual Contribution', data: data.map(d => d.annualContrib), backgroundColor: '#2563eb', stack: 'epf' }}, {{ label: 'Interest Earned', data: data.map(d => d.interest), backgroundColor: '#16a34a', stack: 'epf' }}] }}, options: {{ responsive: true, maintainAspectRatio: false, scales: {{ x: {{ stacked: true }}, y: {{ stacked: true }} }} }} }});
}}
function renderYearTable(data) {{ const body = document.getElementById('year-body'); body.innerHTML = data.map(d => `<tr><td>${{d.year}}</td><td>${{d.age}}</td><td>${{formatINR(d.salary)}}</td><td>${{formatINR(d.annualContrib)}}</td><td>${{formatINR(d.interest)}}</td><td>${{formatLakhCrore(d.balance)}}</td></tr>`).join(''); }}
function renderScenarios() {{ const scenarios = [['Conservative', 5, 7.5], ['Current default', num('increment'), num('interest-rate')], ['High increment', 10, num('interest-rate')], ['Lower EPF rate', num('increment'), 7.0], ['Higher EPF rate', num('increment'), 8.75]]; document.getElementById('scenario-body').innerHTML = scenarios.map(s => `<tr><td>${{s[0]}}</td><td>${{s[1]}}%</td><td>${{s[2]}}%</td><td>${{formatLakhCrore(project(s[1], s[2]).balance)}}</td></tr>`).join(''); }}
document.getElementById('calculate').addEventListener('click', calculateEPF);
window.addEventListener('load', calculateEPF);
}})();
"""
    return page(
        "pf-epf-calculator.html",
        "EPF Calculator — PF Balance and Retirement Corpus | CalcHub",
        "Free EPF/PF calculator India. Calculate monthly PF contribution, total corpus at retirement and year-wise growth. Based on current EPFO interest rate of 8.25%.",
        "EPF / PF Calculator (Employee Provident Fund)",
        "The EPF calculator estimates your provident fund corpus at retirement using monthly Basic + DA salary, employee contribution, employer EPF contribution, expected salary increment, current EPF balance, and EPFO interest rate. It separates EPF and EPS, shows the monthly deduction and employer split, and builds a year-wise table so you can see how compounding works over time. Use it to test retirement scenarios before changing jobs, increasing VPF, or withdrawing PF early.",
        body,
        script,
        faqs,
        chart=True,
    )


def gratuity_page() -> str:
    faqs = [
        ("What is gratuity and who is eligible?", "Gratuity is a lump-sum benefit paid by an employer as a reward for long service. In the private sector, eligibility generally starts after five years of continuous service under the Payment of Gratuity Act, 1972, unless death or disability applies. The amount is based on last drawn Basic + DA and completed years of service. It is separate from PF, bonus, leave encashment, and notice pay. Employees in factories, shops, establishments, mines, ports, plantations, oilfields, railway companies, and other covered organisations may be eligible when the Act applies."),
        ("What is the minimum service period for gratuity?", "The normal minimum service period is five years of continuous service for employees covered under the Payment of Gratuity Act. A commonly discussed exception applies when employment ends due to death or disablement; in such cases, the five-year condition does not apply. Courts and employers may also consider specific interpretations for service beyond four years and 240 days, but payroll departments often follow conservative internal rules. The safest approach is to check your appointment terms, HR policy, and the Act. This calculator shows a not-eligible message when service is below five years for non-government cases."),
        ("What is the maximum gratuity amount in India?", "For many non-government employees, the tax-exempt gratuity limit is ₹20 lakh. The statutory ceiling under the Act has also been aligned around this level for covered employees. If an employer pays more, the excess may be taxable depending on employee category, organisation type, and tax rules. Government employees can have separate rules and often receive different retirement benefit treatment. This calculator applies a ₹20 lakh cap for the displayed payable amount and tax-exempt amount for private-sector planning. For senior roles with high salary and long tenure, consult payroll or a tax adviser."),
        ("Is gratuity taxable in India?", "Gratuity taxation depends on whether the employee is a government employee, covered by the Payment of Gratuity Act, or not covered. Government gratuity can be fully exempt under specific rules. For private employees, exemption is generally limited to the least of actual gratuity received, the statutory/tax exemption limit, and the formula-based amount. Amounts above the exempt limit can be taxable as salary income. This calculator highlights the ₹20 lakh planning threshold, but final tax treatment should be checked with payroll, Form 16, and a qualified tax professional before filing the return."),
        ("What happens to gratuity if an employee dies or is disabled?", "If an employee dies or becomes disabled due to accident or disease, gratuity can become payable even if five years of service have not been completed. The amount is usually paid to the nominee or legal heir in case of death. Employers may need nomination records, death certificate, disability documentation, bank details, and claim forms. This exception exists because gratuity is a social security benefit, not merely a voluntary reward. The exact process depends on employer records and applicable law. Families should contact HR quickly and keep all employment documents available."),
    ]
    body = f"""
    <section class="calc-widget" style="border-color:#f97316;">
      <div class="field-grid">
        <div class="calc-input-group"><label for="salary">Last drawn monthly salary (Basic + DA) (₹)</label><input id="salary" type="number" value="50000"></div>
        <div class="calc-input-group"><label for="years">Years of service</label><input id="years" type="number" step="0.1" value="10"></div>
        <div class="calc-input-group"><label for="org-type">Organisation type</label><select id="org-type"><option value="covered">Covered under Gratuity Act</option><option value="not-covered">Not covered under Gratuity Act</option><option value="govt">Government employee</option></select></div>
      </div>
      <button class="calc-btn" id="calculate" style="background:#f97316;">Calculate gratuity</button>
      <div class="calc-result show" id="gratuity-results"></div>
      <p id="result-note" class="small-note" style="margin-top:1rem;"></p>
    </section>
    <section class="content-section"><h2>How gratuity changes with years of service</h2><p style="color:var(--text-secondary);">The table updates from your salary input and shows how service length changes the payout. This helps employees decide whether another year of service meaningfully changes the benefit.</p><div style="overflow-x:auto;"><table class="reference-table"><thead><tr><th>Service</th><th>Projected gratuity</th></tr></thead><tbody id="projection-body"></tbody></table></div></section>
    <section class="content-section"><h2>How to use</h2>{how_to(["Enter your last drawn monthly Basic + DA, not gross CTC.", "Enter completed years of continuous service, using decimals if needed.", "Select whether your organisation is covered under the Act, not covered, or government.", "Press calculate to view gratuity, tax-exempt amount, taxable amount, and formula.", "Use the projection table to compare service lengths such as 5, 10, 15, 20, and 30 years."])}</section>
    <section class="content-section"><h2>Formula</h2><p>For organisations covered under the Payment of Gratuity Act, the formula is: Gratuity = Monthly Salary × 15 × completed years of service ÷ 26. Salary means last drawn Basic + Dearness Allowance. The number 15 represents 15 days of salary for every completed year, and 26 represents working days in a month. For organisations not covered under the Act, a 30-day month convention is often used for estimates: Monthly Salary × 15 × completed years ÷ 30. Government employees may follow separate retirement rules.</p><p>Service years are usually counted as completed years for formula purposes. The calculator floors decimal years for covered and not-covered formula estimates, while the government option uses the entered decimal value for a half-month salary estimate. Payroll policy and law should be checked for final settlement.</p></section>
    <section class="content-section"><h2>Worked example</h2><p>If an employee’s last drawn Basic + DA is ₹50,000 and completed service is 10 years in a covered organisation, gratuity is ₹50,000 × 15 × 10 ÷ 26 = ₹2,88,462. If service is 20 years at the same salary, the formula gives ₹5,76,923. At high salary and long service, the formula amount can cross the statutory or tax-exempt limit. This is why the calculator also shows the ₹20 lakh exemption planning threshold.</p></section>
    <section class="content-section"><h2>Reference table: gratuity by salary and service</h2>{table(["Monthly salary", "5 years", "10 years", "15 years", "20 years"], [["₹25,000", "₹72,115", "₹1,44,231", "₹2,16,346", "₹2,88,462"], ["₹50,000", "₹1,44,231", "₹2,88,462", "₹4,32,692", "₹5,76,923"], ["₹75,000", "₹2,16,346", "₹4,32,692", "₹6,49,038", "₹8,65,385"], ["₹1,00,000", "₹2,88,462", "₹5,76,923", "₹8,65,385", "₹11,53,846"]])}</section>
    <section class="content-section"><h2>Does gratuity amount change by state?</h2><p>For private-sector employees covered under the Payment of Gratuity Act, the core gratuity formula is a central law and is broadly the same across Indian states. Andhra Pradesh, Telangana, Karnataka, Maharashtra, Tamil Nadu, Delhi, Gujarat, and other states do not use different private-sector formulas merely because the employee works there. State government employees may have service rules, retirement rules, and administrative procedures that differ from central government or private employment.</p>{table(["Employee category", "Formula basis", "State impact"], [["Central Government", "Service rules and retirement benefit rules", "Not based on private-sector state formula"], ["State Government", "State service rules", "Can differ by state cadre and notification"], ["Private sector covered under Act", "Salary × 15 × years ÷ 26", "Central formula broadly applies across states"], ["Private sector not covered", "Contract/policy estimate, often ÷ 30", "Depends on employer policy"]])}</section>
    <section class="content-section"><h2>Important notes for India</h2><ul class="summary-list"><li>Minimum five years service is generally required, except death or disability cases.</li><li>Use Basic + DA, not CTC, gross salary, bonus, or reimbursements.</li><li>₹20 lakh is an important exemption and ceiling threshold for private-sector planning.</li><li>Final settlement should match HR policy, service record, nomination, and tax rules.</li></ul></section>
    {faq_html(faqs)}
    """
    script = f"""
{COMMON_JS}
(function() {{
function calcFor(salary, years, orgType) {{
  const roundedYears = Math.floor(years); let gratuity = 0; let formula = ''; let note = '';
  if (orgType === 'covered') {{ gratuity = (salary * 15 * roundedYears) / 26; formula = `(${{formatINR(salary)}} × 15 × ${{roundedYears}}) ÷ 26 = ${{formatINR(gratuity)}}`; note = 'Calculated as per Payment of Gratuity Act, 1972. 26 working days per month used.'; }}
  else if (orgType === 'govt') {{ gratuity = salary * 0.5 * years; formula = `${{formatINR(salary)}} × 0.5 × ${{years}} = ${{formatINR(gratuity)}}`; note = 'Government employee estimate: half month salary per year of service.'; }}
  else {{ gratuity = (salary * 15 * roundedYears) / 30; formula = `(${{formatINR(salary)}} × 15 × ${{roundedYears}}) ÷ 30 = ${{formatINR(gratuity)}}`; note = 'Organisation not covered under Gratuity Act. Using 30-day month convention.'; }}
  return {{ gratuity, formula, note }};
}}
function calculateGratuity() {{
  const salary = num('salary'); const years = Number(document.getElementById('years').value); const orgType = document.getElementById('org-type').value;
  if (!salary || salary <= 0) {{ showError('Enter valid salary'); return; }}
  if (years < 5 && orgType !== 'govt') {{ showResultCards('gratuity-results', [['Eligibility', 'NOT ELIGIBLE']]); setText('result-note', 'Minimum 5 years of continuous service required for gratuity under the Payment of Gratuity Act, 1972.'); renderProjection(salary, orgType); return; }}
  const r = calcFor(salary, years, orgType); const maxLimit = 2000000; const actual = Math.min(r.gratuity, maxLimit); const taxExempt = Math.min(actual, maxLimit); const taxable = Math.max(0, r.gratuity - maxLimit);
  showResultCards('gratuity-results', [['Gratuity Amount', formatINR(actual)], ['Tax Exempt (up to ₹20L)', formatINR(taxExempt)], ['Taxable Gratuity', formatINR(taxable)], ['Formula Used', r.formula]]);
  setText('result-note', r.note); renderProjection(salary, orgType);
}}
function renderProjection(salary, orgType) {{ const years = [5,8,10,15,20,25,30]; document.getElementById('projection-body').innerHTML = years.map(y => `<tr><td>${{y}} years</td><td>${{formatINR(Math.min(calcFor(salary, y, orgType).gratuity, 2000000))}}</td></tr>`).join(''); }}
document.getElementById('calculate').addEventListener('click', calculateGratuity);
window.addEventListener('load', calculateGratuity);
}})();
"""
    return page(
        "gratuity-calculator.html",
        "Gratuity Calculator India — Gratuity Amount as per Act | CalcHub",
        "Free gratuity calculator India. Calculate gratuity amount as per Payment of Gratuity Act 1972. Shows eligibility, tax exemption limit and formula with examples.",
        "Gratuity Calculator India",
        "The gratuity calculator estimates the lump-sum amount payable to an employee in India based on last drawn Basic + DA, years of service, and organisation type. It follows the Payment of Gratuity Act formula for covered private-sector establishments, includes a not-covered estimate, and gives a separate government employee option. The result shows eligibility, formula, tax-exempt limit, and the effect of longer service.",
        body,
        script,
        faqs,
    )


def ssy_page() -> str:
    faqs = [
        ("What is Sukanya Samriddhi Yojana and who can open the account?", "Sukanya Samriddhi Yojana is a Government of India small-savings scheme meant for a girl child’s long-term education and marriage goals. A parent or legal guardian can open the account in the name of a girl child up to age 10. The scheme allows deposits within yearly limits, earns government-notified interest, and matures 21 years from account opening. It is popular because it combines a high small-savings rate, Section 80C deduction, and tax-free maturity. Families can generally open accounts for two daughters, with special rules for twins or triplets."),
        ("What is the current SSY interest rate for 2025-26?", "This calculator uses 8.2% as the default SSY rate for Q1 FY2025-26, matching the notified small-savings rate used in the page assumptions. SSY rates are reviewed by the government every quarter, so future quarters can remain unchanged or be revised. The rate is annual and compounded yearly. If a new rate is notified, enter it manually in the interest-rate field before calculating. Long-term maturity can change by lakhs when the rate changes, especially when deposits are near the ₹1.5 lakh yearly maximum."),
        ("When does the SSY account mature?", "An SSY account matures 21 years from the date of opening. Deposits are required only for the first 15 years, but the account continues to earn interest until maturity. If the account is opened when the daughter is age 0, maturity happens around age 21. If opened at age 8, there are fewer years until age 21 in this calculator’s age-based view, so the maturity amount is lower for the same annual deposit. Starting early gives the money more years to compound, which is the biggest advantage of SSY."),
        ("Can I withdraw money from SSY before maturity?", "Partial withdrawal is allowed after the girl turns 18, generally up to 50% of the balance for higher education or marriage-related purposes, subject to documentation and scheme rules. Premature closure is restricted and generally allowed only on compassionate grounds after a specified period, such as serious illness or death of the account holder. This calculator shows the balance at age 18 and the 50% withdrawal reference amount. Treat it as a planning estimate and confirm withdrawal rules with the post office or bank where the account is maintained."),
        ("Is SSY better than PPF for saving for a daughter's future?", "SSY and PPF are both high-quality government-backed savings options, but they serve different purposes. SSY is specifically for a girl child and currently offers a higher rate than PPF, with tax-free maturity and Section 80C benefit. PPF is more flexible because any eligible individual can open it and it has a 15-year maturity. SSY has stricter withdrawal rules and a longer child-linked goal. For a daughter’s education or marriage corpus, SSY can be excellent; for general family liquidity and retirement planning, PPF may be more flexible."),
    ]
    body = f"""
    <section class="calc-widget" style="border-color:#f97316;">
      <div class="field-grid">
        <div class="calc-input-group"><label for="daughter-age">Daughter's current age</label><select id="daughter-age">{"".join(f'<option value="{i}">{i} years</option>' for i in range(11))}</select></div>
        <div class="calc-input-group"><label for="annual-deposit">Annual deposit amount (₹)</label><div class="dual-control"><input id="annual-deposit-range" type="range" min="500" max="150000" step="500" value="50000"><input id="annual-deposit" type="number" min="250" max="150000" value="50000"></div><span class="hint">Minimum ₹250/year, maximum ₹1,50,000/year.</span></div>
        <div class="calc-input-group"><label for="ssy-rate">SSY interest rate (%)</label><input id="ssy-rate" type="number" step="0.1" value="8.2"></div>
        <div class="calc-input-group"><label for="start-year">Deposit start year</label><input id="start-year" type="number" value="2025"></div>
      </div>
      <button class="calc-btn" id="calculate" style="background:#f97316;">Calculate SSY maturity</button>
      <div class="calc-result show" id="ssy-results"></div>
      <div class="chart-container"><canvas id="ssy-chart"></canvas></div>
    </section>
    <section class="content-section"><h2>SSY vs other government savings schemes</h2>{table(["Feature", "SSY", "PPF", "NSC", "FD (SBI)"], [["Interest rate", "8.2%", "7.1%", "7.7%", "6.5–7%"], ["Tax benefit (80C)", "Yes", "Yes", "Yes", "Yes (5yr FD)"], ["Maturity", "21 years", "15 years", "5 years", "1–10 years"], ["Tax on maturity", "Tax-free (EEE)", "Tax-free (EEE)", "Taxable", "Taxable"], ["Who can invest", "Girl child", "Any individual", "Any individual", "Any individual"], ["Minimum deposit", "₹250/yr", "₹500/yr", "₹100", "₹1,000"], ["Maximum deposit", "₹1.5L/yr", "₹1.5L/yr", "No limit", "No limit"], ["Premature closure", "Very restricted", "After 5yr", "No", "Penalty"]])}</section>
    <section class="content-section"><h2>Year-wise SSY balance</h2><div style="overflow-x:auto;"><table class="reference-table"><thead><tr><th>Year</th><th>Daughter's age</th><th>Annual deposit</th><th>Interest earned</th><th>Closing balance</th><th>Notes</th></tr></thead><tbody id="ssy-year-body"></tbody></table></div></section>
    <section class="content-section"><h2>How to use</h2>{how_to(["Select your daughter's current age from 0 to 10 years.", "Enter the annual deposit between ₹250 and ₹1,50,000.", "Keep the default 8.2% rate or enter the latest notified SSY rate.", "Enter the deposit start year for a calendar-style year-wise table.", "Review maturity amount, age-18 withdrawal reference, chart, and year-wise balance."])}</section>
    <section class="content-section"><h2>Important SSY rules</h2><ul class="summary-list"><li>Account can be opened for a girl child aged 0 to 10 years.</li><li>Maximum 2 accounts per family, with exception for twins or triplets.</li><li>NRIs cannot open a new SSY account under normal scheme rules.</li><li>Minimum deposit is ₹250/year and maximum is ₹1,50,000/year.</li><li>Deposits are made for 15 years from account opening.</li><li>Account matures 21 years from opening.</li><li>Partial withdrawal up to 50% of balance is allowed after age 18 for education or marriage.</li><li>Premature closure is very restricted and usually allowed only on compassionate grounds.</li><li>SSY is EEE: investment, interest, and maturity are tax-free under current rules.</li></ul></section>
    <section class="content-section"><h2>Formula and compounding</h2><p>SSY interest is compounded annually at the government-notified rate. The practical projection is: opening balance plus current year deposit earns interest, then closing balance is carried forward. Deposits are assumed to be made for the first 15 years only. After that, no further deposit is added, but the account continues earning interest until maturity. Because compounding continues after deposits stop, early deposits are very powerful.</p><p>The calculator also estimates balance at age 18 because partial withdrawal can become relevant for education or marriage planning. It shows 50% of the age-18 balance as a reference, not as an automatic withdrawal. Actual withdrawal requires scheme conditions and documentation.</p></section>
    <section class="content-section"><h2>Important notes for India</h2><ul class="summary-list"><li>SSY rates are notified quarterly by the Government of India and can change.</li><li>Deposits above ₹1.5 lakh per year do not qualify within the scheme limit.</li><li>Missing minimum yearly deposit can make the account irregular until revived with penalty.</li><li>Keep passbook entries and guardian details updated with the bank or post office.</li></ul></section>
    {faq_html(faqs)}
    """
    script = f"""
{COMMON_JS}
(function() {{
let chart;
function calculateSSY() {{
  const daughterAge = parseInt(document.getElementById('daughter-age').value); const annualDeposit = num('annual-deposit'); const rate = num('ssy-rate') / 100; const startYear = parseInt(document.getElementById('start-year').value);
  const maturityAge = 21; const depositYears = 15; const totalYears = maturityAge - daughterAge;
  if (annualDeposit < 250) {{ showError('Minimum deposit is ₹250 per year'); return; }}
  if (annualDeposit > 150000) {{ showError('Maximum deposit is ₹1,50,000 per year'); return; }}
  let balance = 0; let totalDeposited = 0; const yearData = [];
  for (let y = 1; y <= totalYears; y++) {{
    const currentAge = daughterAge + y; const isDepositYear = y <= depositYears; const deposit = isDepositYear ? annualDeposit : 0; if (isDepositYear) totalDeposited += deposit;
    const interest = (balance + deposit) * rate; balance += deposit + interest;
    const notes = []; if (isDepositYear) notes.push('Deposits active'); else notes.push('Interest only'); if (currentAge === 18) notes.push('Partial withdrawal eligible'); if (currentAge === 21) notes.push('Maturity');
    yearData.push({{ year: startYear + y - 1, daughterAge: currentAge, deposit: Math.round(deposit), interest: Math.round(interest), balance: Math.round(balance), totalDeposited: Math.round(totalDeposited), notes: notes.join(', ') }});
  }}
  const maturityAmount = Math.round(balance); const totalInterest = maturityAmount - totalDeposited; const age18Balance = yearData.find(d => d.daughterAge === 18)?.balance || 0;
  showResultCards('ssy-results', [['Maturity Amount (age 21)', formatLakhCrore(maturityAmount)], ['Total Deposited', formatLakhCrore(totalDeposited)], ['Total Interest Earned', formatLakhCrore(totalInterest)], ['Balance at Age 18', formatLakhCrore(age18Balance)], ['Max withdrawal at 18 (50%)', formatLakhCrore(age18Balance * 0.5)], ['Deposit period', depositYears + ' years (until age ' + (daughterAge + depositYears) + ')']]);
  renderSSYTable(yearData); drawSSYChart(yearData);
}}
function renderSSYTable(data) {{ document.getElementById('ssy-year-body').innerHTML = data.map(d => `<tr><td>${{d.year}}</td><td>${{d.daughterAge}}</td><td>${{formatINR(d.deposit)}}</td><td>${{formatINR(d.interest)}}</td><td>${{formatLakhCrore(d.balance)}}</td><td>${{d.notes}}</td></tr>`).join(''); }}
const markers = {{ id: 'ssyMarkers', afterDraw(chart) {{ const x = chart.scales.x; const top = chart.chartArea.top; const bottom = chart.chartArea.bottom; const ctx = chart.ctx; const drawLine = (index, color, label) => {{ if (index < 0 || index >= chart.data.labels.length) return; const xp = x.getPixelForValue(index); ctx.save(); ctx.strokeStyle = color; ctx.setLineDash([5,5]); ctx.beginPath(); ctx.moveTo(xp, top); ctx.lineTo(xp, bottom); ctx.stroke(); ctx.setLineDash([]); ctx.fillStyle = color; ctx.font = '11px Inter, sans-serif'; ctx.fillText(label, xp + 4, top + 12); ctx.restore(); }}; drawLine(14, '#ef4444', 'Deposit stop'); const age18Index = chart.data.rawAges ? chart.data.rawAges.indexOf(18) : -1; drawLine(age18Index, '#f97316', 'Age 18'); drawLine(chart.data.labels.length - 1, '#d97706', '★ Maturity'); }} }};
function drawSSYChart(data) {{
  if (typeof Chart === 'undefined') return; const ctx = document.getElementById('ssy-chart'); if (chart) chart.destroy();
  chart = new Chart(ctx, {{ type: 'bar', data: {{ labels: data.map(d => String(d.year)), rawAges: data.map(d => d.daughterAge), datasets: [{{ label: 'Cumulative deposits', data: data.map(d => d.totalDeposited), backgroundColor: '#2563eb', stack: 'ssy' }}, {{ label: 'Cumulative interest', data: data.map(d => d.balance - d.totalDeposited), backgroundColor: '#16a34a', stack: 'ssy' }}] }}, options: {{ responsive: true, maintainAspectRatio: false, scales: {{ x: {{ stacked: true }}, y: {{ stacked: true }} }} }}, plugins: [markers] }});
}}
document.getElementById('annual-deposit-range').addEventListener('input', e => {{ document.getElementById('annual-deposit').value = e.target.value; calculateSSY(); }});
document.getElementById('annual-deposit').addEventListener('input', e => {{ document.getElementById('annual-deposit-range').value = e.target.value; }});
document.getElementById('calculate').addEventListener('click', calculateSSY);
window.addEventListener('load', calculateSSY);
}})();
"""
    return page(
        "sukanya-samriddhi-calculator.html",
        "Sukanya Samriddhi Yojana Calculator 2025 — SSY Maturity | CalcHub",
        "Free SSY calculator for Sukanya Samriddhi Yojana. Calculate maturity amount, year-wise balance and interest earned. Current SSY interest rate 8.2% for Q1 2025-26.",
        "Sukanya Samriddhi Yojana (SSY) Calculator 2025",
        "The Sukanya Samriddhi Yojana calculator estimates the maturity value of an SSY account for your daughter using annual deposit, current age, notified interest rate, and deposit start year. It follows the core SSY rule that deposits are made for 15 years while the account earns interest until maturity around age 21. The result shows total deposited, interest earned, age-18 withdrawal reference, and a year-wise table for planning education and marriage goals.",
        body,
        script,
        faqs,
        chart=True,
    )


def main() -> None:
    pages = {
        "on-road-price-calculator.html": on_road_page(),
        "cgpa-to-percentage-calculator.html": cgpa_page(),
        "pf-epf-calculator.html": epf_page(),
        "gratuity-calculator.html": gratuity_page(),
        "sukanya-samriddhi-calculator.html": ssy_page(),
    }
    for name, content in pages.items():
        (INDIA / name).write_text(content, encoding="utf-8", newline="")
    for name in pages:
        text = re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", (INDIA / name).read_text(encoding="utf-8"), flags=re.S)
        words = len(re.findall(r"[A-Za-z0-9₹%'-]+", text))
        if words < 1200:
            raise RuntimeError(f"{name} has only {words} words")
        print(f"{name}: {words} words")


if __name__ == "__main__":
    main()
