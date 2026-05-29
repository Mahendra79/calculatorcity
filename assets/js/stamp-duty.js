(function () {
  "use strict";

  // ─── Smooth page transitions — NO flicker ───
  document.addEventListener("DOMContentLoaded", () => {
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        document.body.classList.add("page-loaded");
      });
    });
  });

  function normalizeHref(href) {
    if (!href || href === "#") return "";
    try {
      return new URL(href, window.location.href).href;
    } catch (_) {
      return href;
    }
  }

  function prefetchPage(href) {
    if (!href) return;
    const normalized = normalizeHref(href);
    if (!normalized || normalized === window.location.href) return;
    const exists = Array.from(document.querySelectorAll('link[rel="prefetch"]'))
      .some(link => normalizeHref(link.getAttribute("href")) === normalized || link.href === normalized);
    if (exists) return;
    const link = document.createElement("link");
    link.rel = "prefetch";
    link.href = href;
    document.head.appendChild(link);
  }

  function navigateTo(href) {
    if (!href) return;
    const normalized = normalizeHref(href);
    if (!normalized || normalized === window.location.href) return;
    document.body.classList.add("page-exit");
    setTimeout(() => { window.location.href = href; }, 150);
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.addEventListener("mouseover", event => {
      const el = event.target.closest("[data-state-link]");
      if (el) prefetchPage(el.dataset.href || el.getAttribute("href"));
    });
    document.addEventListener("focusin", event => {
      const el = event.target.closest("[data-state-link]");
      if (el) prefetchPage(el.dataset.href || el.getAttribute("href"));
    });
    document.addEventListener("click", event => {
      const el = event.target.closest("[data-state-link]");
      if (!el || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      navigateTo(el.dataset.href || el.getAttribute("href"));
    });
  });

  const data = window.stampDutyData || {};
  const stateOrder = window.stampDutyStateOrder || Object.keys(data);
  const CANONICAL_BASE_URL = "/india/stamp-duty/";
  const BRAND_COLOR = "#f97316";
  const BRAND_LIGHT = "#fff7ed";
  const BRAND_BORDER = "#fed7aa";

  let currentStateSlug = null;
  let currentGender = "male";
  let currentPropType = "residential";
  let isRural = false;

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

  function byId(id) {
    return document.getElementById(id);
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
    const div = document.createElement("div");
    div.innerHTML = value || "";
    return div.textContent || div.innerText || "";
  }

  function stateUrl(slug) {
    return slug + ".html";
  }

  function stateCanonicalPath(slug) {
    return CANONICAL_BASE_URL + slug + ".html";
  }

  function formatINR(value) {
    const number = Number(value);
    if (!Number.isFinite(number)) return "₹0";
    const rounded = Math.abs(Math.round(number));
    const input = String(rounded);
    let result = input.slice(-3);
    let remaining = input.slice(0, -3);
    while (remaining.length > 2) {
      result = remaining.slice(-2) + "," + result;
      remaining = remaining.slice(0, -2);
    }
    if (remaining) result = remaining + "," + result;
    return (number < 0 ? "-₹" : "₹") + result;
  }

  function formatLakhCrore(value) {
    const number = Number(value) || 0;
    if (Math.abs(number) >= 10000000) return "₹" + (number / 10000000).toFixed(2) + " Cr";
    if (Math.abs(number) >= 100000) return "₹" + (number / 100000).toFixed(2) + " L";
    return formatINR(number);
  }

  function numberToWords(value) {
    const number = Number(value);
    if (!Number.isFinite(number) || number <= 0) return "";
    if (number >= 10000000) return "₹" + (number / 10000000).toFixed(2) + " Crore";
    if (number >= 100000) return "₹" + (number / 100000).toFixed(2) + " Lakh";
    if (number >= 1000) return "₹" + (number / 1000).toFixed(1) + " Thousand";
    return "₹" + number;
  }

  function formatPercent(value, decimals) {
    const number = Number(value) || 0;
    const places = decimals == null ? (Number.isInteger(number) ? 0 : 2) : decimals;
    return number.toFixed(places).replace(/\.?0+$/, "") + "%";
  }

  function parseAmount(value) {
    const cleaned = String(value || "").replace(/[^\d.-]/g, "").replace(/(?!^)-/g, "").replace(/(\..*)\./g, "$1");
    const number = Number(cleaned);
    return Number.isFinite(number) ? number : 0;
  }

  function safeSetText(id, value) {
    const el = byId(id);
    if (el) el.textContent = value;
  }

  function safeSetHTML(id, value) {
    const el = byId(id);
    if (el) el.innerHTML = value;
  }

  function setDisplay(id, value) {
    const el = byId(id);
    if (el) el.style.display = value;
  }

  function buildFaqSchema(items) {
    return {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": (items || []).map(item => ({
        "@type": "Question",
        "name": item.q,
        "acceptedAnswer": { "@type": "Answer", "text": stripHTML(item.a) }
      }))
    };
  }

  function updateFaqSchema(items) {
    const schema = byId("schema-faq");
    if (schema) schema.textContent = JSON.stringify(buildFaqSchema(items), null, 2);
  }

  function populateDropdown() {
    const select = byId("state-select");
    if (!select) return;
    select.textContent = "";
    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = "— Choose your state —";
    select.appendChild(placeholder);

    const groups = {
      "South India": ["andhra-pradesh", "telangana", "karnataka", "tamil-nadu", "kerala", "goa"],
      "West India": ["maharashtra", "gujarat"],
      "North India": ["delhi", "uttar-pradesh", "rajasthan", "haryana", "punjab", "himachal-pradesh", "uttarakhand", "jammu-kashmir"],
      "East India": ["west-bengal", "bihar", "odisha", "jharkhand", "chhattisgarh"],
      "Central India": ["madhya-pradesh"],
      "Northeast": ["assam"],
      "Union Territories": ["chandigarh", "puducherry", "ladakh", "andaman-nicobar"]
    };

    Object.entries(groups).forEach(([label, slugs]) => {
      const optgroup = document.createElement("optgroup");
      optgroup.label = label;
      slugs.forEach(slug => {
        const state = data[slug];
        if (!state) return;
        const option = document.createElement("option");
        option.value = slug;
        option.textContent = state.name;
        option.dataset.stateLink = "";
        option.dataset.href = stateUrl(slug);
        optgroup.appendChild(option);
      });
      select.appendChild(optgroup);
    });
  }

  function stateTotalRate(state, gender) {
    const key = gender || "male";
    return (state.stampDuty[key] || state.stampDuty.male || 0) +
      (state.registrationCharges[key] || state.registrationCharges.male || 0) +
      (state.transferDuty || 0);
  }

  function buildStateTiles() {
    const grid = byId("states-grid");
    if (!grid) return;
    grid.textContent = "";
    stateOrder.forEach(slug => {
      const state = data[slug];
      if (!state) return;
      const tile = document.createElement("a");
      tile.className = "state-tile";
      tile.href = stateUrl(slug);
      tile.style.setProperty("--tile-color", BRAND_COLOR);
      tile.style.setProperty("--tile-light", BRAND_LIGHT);
      tile.dataset.slug = slug;
      tile.dataset.stateLink = "";
      tile.dataset.href = stateUrl(slug);
      tile.setAttribute("aria-label", state.name + " stamp duty calculator");
      tile.innerHTML =
        '<span class="state-tile-name">' + escapeHTML(state.name) + '</span>' +
        '<span class="state-tile-rate">' + formatPercent(state.stampDuty.male) + ' + ' + formatPercent(state.registrationCharges.male) + ' = ' + formatPercent(stateTotalRate(state, "male"), 1) + '</span>';
      grid.appendChild(tile);
    });
  }

  function renderIndexRatesTable() {
    const rows = stateOrder.map(slug => {
      const state = data[slug];
      if (!state) return "";
      const women = state.hasWomenDiscount ? formatPercent(state.stampDuty.female) : "No broad discount";
      return '<tr>' +
        '<td><a data-state-link data-href="' + escapeHTML(stateUrl(slug)) + '" href="' + escapeHTML(stateUrl(slug)) + '">' + escapeHTML(state.name) + '</a></td>' +
        '<td>' + formatPercent(state.stampDuty.male) + '</td>' +
        '<td>' + women + '</td>' +
        '<td>' + formatPercent(state.registrationCharges.male) + '</td>' +
        '<td style="font-weight:600;">' + formatPercent(stateTotalRate(state, "male"), 2) + '</td>' +
        '</tr>';
    }).join("");

    safeSetText("content-h2-rates", "Stamp duty rates comparison — all states & UTs");
    safeSetHTML("content-rates-table", '<div style="overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 0 -1rem; padding: 0 1rem;"><table class="rates-table" style="min-width: 500px;"><thead><tr><th>State / UT</th><th>Men stamp</th><th>Women stamp</th><th>Registration</th><th>Total</th></tr></thead><tbody>' + rows + '</tbody></table></div>');
    setDisplay("content-rates-section", "block");
    renderFaq(defaultFaq);
    updateFaqSchema(defaultFaq);
  }

  function detectCurrentState() {
    if (window.STAMP_DUTY_INITIAL_STATE && data[window.STAMP_DUTY_INITIAL_STATE]) {
      return window.STAMP_DUTY_INITIAL_STATE;
    }
    const filename = window.location.pathname.split("/").pop().replace(".html", "");
    return filename && filename !== "index" && data[filename] ? filename : null;
  }

  function syncSeo(state) {
    const pageTitle = byId("page-title");
    if (pageTitle) pageTitle.textContent = state.seo.title;
    document.title = state.seo.title;
    const meta = byId("page-meta");
    if (meta) meta.setAttribute("content", state.seo.description);
    const canonical = byId("page-canonical");
    if (canonical) canonical.setAttribute("href", "https://calculatorcity.in" + stateCanonicalPath(state.slug));
    const ogTitle = byId("og-title");
    if (ogTitle) ogTitle.setAttribute("content", state.seo.title);
    const ogDescription = byId("og-description");
    if (ogDescription) ogDescription.setAttribute("content", state.seo.description);
    const ogUrl = byId("og-url");
    if (ogUrl) ogUrl.setAttribute("content", "https://calculatorcity.in" + stateCanonicalPath(state.slug));
    updateFaqSchema(state.content.faq);
  }

  function loadState(slug) {
    const state = data[slug];
    if (!state) return;
    currentStateSlug = slug;
    isRural = false;

    syncSeo(state);
    document.documentElement.style.setProperty("--state-color", BRAND_COLOR);
    document.documentElement.style.setProperty("--state-light", BRAND_LIGHT);
    document.documentElement.style.setProperty("--state-border", BRAND_BORDER);

    safeSetText("page-h1", state.seo.h1);
    safeSetText("page-subtitle", state.seo.subtitle);
    safeSetText("breadcrumb-current", state.seo.h1);
    safeSetText("state-flag", state.flag);
    safeSetText("state-info-name", state.name);
    safeSetText("state-info-sub", "Stamp duty: " + formatPercent(state.stampDuty.male) + " • Registration: " + formatPercent(state.registrationCharges.male) + (state.transferDuty ? " • Transfer duty: " + formatPercent(state.transferDuty) : ""));

    const select = byId("state-select");
    if (select) select.value = slug;

    const infoBar = byId("state-info-bar");
    if (infoBar) {
      infoBar.style.display = "flex";
      infoBar.style.borderColor = BRAND_COLOR;
    }
    setDisplay("calc-widget", "block");
    setDisplay("rates-summary-card", "block");
    setDisplay("tariff-summary", "block");

    const badges = byId("state-badges");
    if (badges) {
      badges.textContent = "";
      if (state.hasWomenDiscount) {
        const badge = document.createElement("span");
        badge.className = "badge badge-women";
        badge.textContent = "💝 Women save " + formatPercent(state.womenDiscount);
        badges.appendChild(badge);
      }
      if (state.transferDuty > 0) {
        const badge = document.createElement("span");
        badge.className = "badge badge-transfer";
        badge.textContent = "+ " + formatPercent(state.transferDuty) + " Transfer duty";
        badges.appendChild(badge);
      }
    }

    const womenBadge = byId("women-discount-badge");
    if (womenBadge) {
      womenBadge.classList.toggle("show", Boolean(state.hasWomenDiscount));
      safeSetText("women-discount-text", state.hasWomenDiscount
        ? "Women buyers get " + formatPercent(state.womenDiscount) + " discount in " + state.name + " — pay " + formatPercent(state.stampDuty.female) + " instead of " + formatPercent(state.stampDuty.male)
        : "");
    }

    const ruralToggle = byId("rural-toggle");
    if (ruralToggle) ruralToggle.checked = false;
    setDisplay("urban-rural-row", state.hasUrbanRural ? "block" : "none");

    document.querySelectorAll(".state-tile").forEach(tile => {
      tile.classList.toggle("active-state", tile.dataset.slug === slug);
    });

    renderRatesSummary(state);
    renderTariffSummary(state);
    updateContent(state);
    resetResultState();
  }

  function renderRatesSummary(state) {
    const totalMen = stateTotalRate(state, "male");
    const totalWomen = state.hasWomenDiscount ? stateTotalRate(state, "female") : null;
    safeSetHTML("rates-summary",
      '<div class="quick-fact">👨 Men: ' + formatPercent(state.stampDuty.male) + ' stamp duty</div>' +
      (state.hasWomenDiscount ? '<div class="quick-fact fact-women">👩 Women: ' + formatPercent(state.stampDuty.female) + ' stamp duty</div>' : "") +
      '<div class="quick-fact">📝 Registration: ' + formatPercent(state.registrationCharges.male) + '</div>' +
      (state.transferDuty > 0 ? '<div class="quick-fact">🔄 Transfer duty: ' + formatPercent(state.transferDuty) + '</div>' : "") +
      '<div class="quick-fact quick-fact-total">Total (men): ~' + formatPercent(totalMen, 2) + (totalWomen != null ? ' | Total (women): ~' + formatPercent(totalWomen, 2) : "") + '</div>'
    );
  }

  function renderTariffSummary(state) {
    const totalMen = stateTotalRate(state, "male");
    safeSetText("tariff-summary-title", state.name + " stamp duty rates 2025");
    safeSetHTML("tariff-grid",
      '<div class="tariff-item"><div class="tariff-val">' + formatPercent(state.stampDuty.male) + '</div><div class="tariff-lbl">Stamp duty (men)</div></div>' +
      (state.hasWomenDiscount ? '<div class="tariff-item"><div class="tariff-val tariff-women">' + formatPercent(state.stampDuty.female) + '</div><div class="tariff-lbl">Stamp duty (women)</div></div>' : "") +
      '<div class="tariff-item"><div class="tariff-val">' + formatPercent(state.registrationCharges.male) + '</div><div class="tariff-lbl">Registration</div></div>' +
      (state.transferDuty > 0 ? '<div class="tariff-item"><div class="tariff-val tariff-transfer">' + formatPercent(state.transferDuty) + '</div><div class="tariff-lbl">Transfer duty</div></div>' : "") +
      '<div class="tariff-item"><div class="tariff-val">' + formatPercent(totalMen, 2) + '</div><div class="tariff-lbl">Total (men)</div></div>'
    );
  }

  function updateContent(state) {
    safeSetText("content-h2-how", "How is stamp duty calculated in " + state.name + "?");
    safeSetHTML("content-how-text", state.content.howItWorks || "");
    safeSetHTML("content-state-text", state.content.stateSpecific || "");
    setDisplay("content-state-section", state.content.stateSpecific ? "block" : "none");
    renderStateRatesTable(state);
    renderFaq(state.content.faq || []);
    safeSetText("content-h2-faq", state.name + " stamp duty — frequently asked questions");
  }

  function renderStateRatesTable(state) {
    const propNames = {
      residential: "🏠 Residential",
      commercial: "🏢 Commercial",
      agricultural: "🌾 Agricultural"
    };
    let html = '<table class="rates-table"><thead><tr><th>Property type</th><th>Stamp duty</th><th>Registration</th>';
    if (state.transferDuty > 0) html += "<th>Transfer duty</th>";
    html += "<th>Total</th></tr></thead><tbody>";
    Object.entries(state.propertyTypes || {}).forEach(([type, rates]) => {
      const stamp = rates.stamp || rates.male || state.stampDuty.male;
      const reg = rates.reg || state.registrationCharges.male;
      const total = stamp + reg + (state.transferDuty || 0);
      html += "<tr><td>" + escapeHTML(propNames[type] || type) + "</td><td>" + formatPercent(stamp) + "</td><td>" + formatPercent(reg) + "</td>";
      if (state.transferDuty > 0) html += "<td>" + formatPercent(state.transferDuty) + "</td>";
      html += '<td style="font-weight:600;">' + formatPercent(total, 2) + "</td></tr>";
    });
    if (state.hasWomenDiscount) {
      html += '<tr class="women-rate-row"><td colspan="5">💝 Women buyers get ' + formatPercent(state.womenDiscount) + " discount on stamp duty in " + escapeHTML(state.name) + "</td></tr>";
    }
    html += "</tbody></table>";
    if (state.notes) html += '<p class="rate-note">📌 ' + escapeHTML(state.notes) + "</p>";
    safeSetText("content-h2-rates", state.name + " stamp duty rates — all property types");
    safeSetHTML("content-rates-table", html);
    setDisplay("content-rates-section", "block");
  }

  function renderFaq(items) {
    const list = byId("faq-list");
    if (!list) return;
    list.textContent = "";
    (items || []).forEach((item, index) => {
      const div = document.createElement("div");
      div.className = "faq-item";
      div.innerHTML =
        '<button class="faq-q-btn" type="button" aria-expanded="false" aria-controls="faq-a-' + index + '">' +
        escapeHTML(item.q) + ' <span class="faq-chevron">▾</span></button>' +
        '<div class="faq-answer" id="faq-a-' + index + '">' + escapeHTML(item.a) + "</div>";
      list.appendChild(div);
    });
  }

  function resetResultState() {
    setDisplay("results-box", "none");
    const input = byId("property-value");
    if (input && !input.dataset.keepValue) input.value = "";
    safeSetText("amount-display", "Enter value");
    safeSetText("amount-in-words", "");
    showInputError("");
  }

  function getRatesForCurrentSelection(value) {
    const state = data[currentStateSlug];
    const propData = (state.propertyTypes && state.propertyTypes[currentPropType]) || state.propertyTypes.residential || {};
    let stampRate;

    if (currentGender === "female" && state.hasWomenDiscount) {
      stampRate = propData.female || state.stampDuty.female;
    } else if (currentGender === "joint") {
      stampRate = propData.joint || state.stampDuty.joint || ((state.stampDuty.male + state.stampDuty.female) / 2);
    } else {
      stampRate = propData.stamp || propData.male || state.stampDuty.male;
    }

    if (isRural && state.hasUrbanRural && state.rural) {
      stampRate = state.rural[currentGender] || state.rural.stamp || stampRate;
    }

    if (currentStateSlug === "karnataka") {
      if (value < 2000000) stampRate = 2;
      else if (value < 4500000) stampRate = 3;
      else stampRate = 5;
    }

    const regRate = propData.reg || state.registrationCharges[currentGender] || state.registrationCharges.male;
    return { stampRate, regRate, transferRate: state.transferDuty || 0 };
  }

  function showInputError(message) {
    const box = byId("calc-error");
    if (!box) return;
    box.textContent = message;
    box.hidden = !message;
  }

  function calculate() {
    if (!currentStateSlug) return;
    const state = data[currentStateSlug];
    const value = parseAmount(byId("property-value") ? byId("property-value").value : "");
    if (!value || value < 1000) {
      showInputError("Enter a valid property value above ₹1,000.");
      return;
    }
    showInputError("");

    const rates = getRatesForCurrentSelection(value);
    const stampAmount = value * rates.stampRate / 100;
    let regAmount = value * rates.regRate / 100;
    const uncappedRegAmount = regAmount;
    if (state.registrationCap) regAmount = Math.min(regAmount, state.registrationCap);
    const transferAmount = value * rates.transferRate / 100;
    const total = stampAmount + regAmount + transferAmount;
    const totalPct = value ? (total / value) * 100 : 0;

    safeSetText("result-total", formatINR(total));
    safeSetText("result-meta", (currentGender === "female" ? "👩 Women rate" : currentGender === "joint" ? "👫 Joint rate" : "👨 Men rate") + " • " + state.name + " • " + numberToWords(value) + " property");

    renderWomenSavings(state, value);
    renderBreakdown(value, rates, stampAmount, regAmount, uncappedRegAmount, transferAmount, total, totalPct);
    renderStateComparison(value);
    renderTips(state, value);

    setDisplay("results-box", "block");
    const results = byId("results-box");
    if (results) results.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  function renderWomenSavings(state, value) {
    const banner = byId("women-savings-banner");
    if (!banner) return;
    if (!state.hasWomenDiscount) {
      banner.classList.remove("show");
      return;
    }
    const savings = (state.stampDuty.male - state.stampDuty.female) * value / 100;
    if (currentGender === "male" && savings > 0) {
      banner.classList.add("show");
      safeSetText("women-savings-text", "💝 If a woman buyer registers this property, she saves " + formatINR(savings) + " on stamp duty (pays " + formatPercent(state.stampDuty.female) + " instead of " + formatPercent(state.stampDuty.male) + ").");
    } else if (currentGender === "female" && savings > 0) {
      banner.classList.add("show");
      safeSetText("women-savings-text", "💝 You are saving " + formatINR(savings) + " vs a male buyer with the women discount in " + state.name + ".");
    } else {
      banner.classList.remove("show");
    }
  }

  function renderBreakdown(value, rates, stampAmount, regAmount, uncappedRegAmount, transferAmount, total, totalPct) {
    const tbody = byId("breakdown-tbody");
    const tfoot = byId("breakdown-tfoot");
    if (!tbody || !tfoot) return;
    tbody.textContent = "";

    const rows = [
      { label: "Property value", rate: "", amount: value },
      { label: "Stamp duty", rate: formatPercent(rates.stampRate), amount: stampAmount },
      {
        label: regAmount < uncappedRegAmount ? "Registration charges (capped)" : "Registration charges",
        rate: formatPercent(rates.regRate),
        amount: regAmount
      }
    ];
    if (transferAmount > 0) rows.push({ label: "Transfer duty", rate: formatPercent(rates.transferRate), amount: transferAmount });

    rows.forEach(row => {
      const tr = document.createElement("tr");
      tr.innerHTML = "<td>" + escapeHTML(row.label) + '</td><td class="breakdown-rate">' + escapeHTML(row.rate) + "</td><td>" + formatINR(row.amount) + "</td>";
      tbody.appendChild(tr);
    });

    tfoot.innerHTML =
      '<tr class="total-row"><td colspan="2"><strong>Total cost to register</strong></td><td><strong>' + formatINR(total) + "</strong></td></tr>" +
      '<tr><td colspan="2">As % of property value</td><td>' + formatPercent(totalPct, 2) + "</td></tr>" +
      '<tr><td colspan="2">Total cost incl. property</td><td>' + formatINR(value + total) + "</td></tr>";
  }

  function totalForState(slug, value, gender) {
    const state = data[slug];
    if (!state) return 0;
    const stampRate = state.stampDuty[gender] || state.stampDuty.male || 0;
    const regRate = state.registrationCharges[gender] || state.registrationCharges.male || 0;
    const stamp = value * stampRate / 100;
    let reg = value * regRate / 100;
    if (state.registrationCap) reg = Math.min(reg, state.registrationCap);
    const transfer = value * (state.transferDuty || 0) / 100;
    return stamp + reg + transfer;
  }

  function renderStateComparison(value) {
    const grid = byId("compare-grid");
    if (!grid) return;
    grid.textContent = "";
    const currentTotal = totalForState(currentStateSlug, value, "male");
    stateOrder.filter(slug => slug !== currentStateSlug).slice(0, 8).forEach(slug => {
      const state = data[slug];
      const total = totalForState(slug, value, "male");
      const isCheaper = total < currentTotal;
      const item = document.createElement("a");
      item.className = "compare-item" + (isCheaper ? " cheaper" : total > currentTotal ? " expensive" : "");
      item.href = stateUrl(slug);
      item.style.setProperty("--tile-color", BRAND_COLOR);
      item.style.setProperty("--tile-light", BRAND_LIGHT);
      item.dataset.stateLink = "";
      item.dataset.href = stateUrl(slug);
      item.innerHTML =
        '<div class="compare-item-name">' + escapeHTML(state.name) + '</div>' +
        '<div class="compare-item-total">' + formatINR(total) + '</div>' +
        '<div class="compare-item-rate">' + formatPercent(stateTotalRate(state, "male"), 2) + " total " + (isCheaper ? "✓ cheaper" : total > currentTotal ? "▲ costlier" : "") + "</div>";
      grid.appendChild(item);
    });
  }

  function renderTips(state, value) {
    const list = byId("tips-list");
    if (!list) return;
    list.textContent = "";
    const tips = [];
    if (state.hasWomenDiscount && currentGender !== "female") {
      const savings = (state.stampDuty.male - state.stampDuty.female) * value / 100;
      if (savings > 0) tips.push({ icon: "💝", text: "Register in a woman's name to save " + formatINR(savings) + " in " + state.name + ". Women pay " + formatPercent(state.stampDuty.female) + " vs " + formatPercent(state.stampDuty.male) + " for men." });
    }
    if (currentStateSlug !== "telangana") {
      const saving = totalForState(currentStateSlug, value, "male") - totalForState("telangana", value, "male");
      if (saving > 0) tips.push({ icon: "📊", text: "Same property in Telangana would cost " + formatINR(saving) + " less in stamp duty and registration charges using the base male rate." });
    }
    tips.push({ icon: "📋", text: "Get an accurate valuation first. If circle rate is higher than the agreement value, stamp duty is calculated on circle rate." });
    tips.push({ icon: "🏠", text: "Under-construction properties may attract GST separately. Ready-to-move resale properties usually carry stamp duty and registration charges." });
    tips.push({ icon: "💰", text: "Stamp duty and registration charges can qualify under Section 80C up to the annual limit when conditions are met." });

    tips.slice(0, 4).forEach(tip => {
      const item = document.createElement("div");
      item.className = "tip-item";
      item.innerHTML = '<span class="tip-icon">' + tip.icon + '</span><span>' + escapeHTML(tip.text) + "</span>";
      list.appendChild(item);
    });
  }

  function setupEventListeners() {
    const select = byId("state-select");
    if (select) {
      select.addEventListener("change", function () {
        const option = this.options[this.selectedIndex];
        if (option && option.value) navigateTo(option.dataset.href || stateUrl(option.value));
      });
    }

    const calcButton = byId("calc-btn");
    if (calcButton) calcButton.addEventListener("click", calculate);

    const genderTabs = byId("gender-tabs");
    if (genderTabs) {
      genderTabs.addEventListener("click", event => {
        const tab = event.target.closest(".gender-tab");
        if (!tab) return;
        genderTabs.querySelectorAll(".gender-tab").forEach(item => item.classList.remove("active"));
        tab.classList.add("active");
        currentGender = tab.dataset.gender || "male";
        if (byId("results-box") && byId("results-box").style.display !== "none") calculate();
      });
    }

    const propTabs = byId("prop-tabs");
    if (propTabs) {
      propTabs.addEventListener("click", event => {
        const tab = event.target.closest(".prop-tab");
        if (!tab) return;
        propTabs.querySelectorAll(".prop-tab").forEach(item => item.classList.remove("active"));
        tab.classList.add("active");
        currentPropType = tab.dataset.prop || "residential";
        if (byId("results-box") && byId("results-box").style.display !== "none") calculate();
      });
    }

    const ruralToggle = byId("rural-toggle");
    if (ruralToggle) {
      ruralToggle.addEventListener("change", function () {
        isRural = this.checked;
        if (byId("results-box") && byId("results-box").style.display !== "none") calculate();
      });
    }

    const input = byId("property-value");
    if (input) {
      input.addEventListener("input", function () {
        const value = parseAmount(this.value);
        if (value > 0) {
          safeSetText("amount-display", numberToWords(value));
          safeSetText("amount-in-words", formatINR(value));
        } else {
          safeSetText("amount-display", "Enter value");
          safeSetText("amount-in-words", "");
        }
        showInputError("");
      });
      input.addEventListener("keydown", event => {
        if (event.key === "Enter") calculate();
      });
    }

    const faqList = byId("faq-list");
    if (faqList) {
      faqList.addEventListener("click", event => {
        const button = event.target.closest(".faq-q-btn");
        if (!button) return;
        const answer = button.parentElement ? button.parentElement.querySelector(".faq-answer") : null;
        const open = answer ? answer.classList.toggle("open") : false;
        button.setAttribute("aria-expanded", String(open));
      });
    }
  }

  function init() {
    populateDropdown();
    buildStateTiles();
    setupEventListeners();
    const slug = detectCurrentState();
    if (slug) {
      loadState(slug);
    } else {
      renderIndexRatesTable();
      updateFaqSchema(defaultFaq);
    }
  }

  window.StampDutyCalculator = {
    loadState,
    navigateTo,
    prefetchPage,
    calculate
  };

  document.addEventListener("DOMContentLoaded", init);
})();
