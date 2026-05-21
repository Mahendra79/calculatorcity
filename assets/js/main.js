const calculators = [
  {
    "name": "Age Calculator",
    "url": "/date-time/age-calculator.html",
    "category": "Date & Time",
    "keywords": "age calculator"
  },
  {
    "name": "Date Difference Calculator",
    "url": "/date-time/date-difference-calculator.html",
    "category": "Date & Time",
    "keywords": "date difference calculator"
  },
  {
    "name": "Days Until Calculator",
    "url": "/date-time/days-until-calculator.html",
    "category": "Date & Time",
    "keywords": "days until calculator"
  },
  {
    "name": "Leap Year Calculator",
    "url": "/date-time/leap-year-calculator.html",
    "category": "Date & Time",
    "keywords": "leap year calculator"
  },
  {
    "name": "Retirement Date Calculator",
    "url": "/date-time/retirement-date-calculator.html",
    "category": "Date & Time",
    "keywords": "retirement date calculator"
  },
  {
    "name": "Time Calculator",
    "url": "/date-time/time-calculator.html",
    "category": "Date & Time",
    "keywords": "time calculator"
  },
  {
    "name": "Time Zone Converter",
    "url": "/date-time/time-zone-converter.html",
    "category": "Date & Time",
    "keywords": "time zone converter"
  },
  {
    "name": "Unix Timestamp Converter",
    "url": "/date-time/unix-timestamp-converter.html",
    "category": "Date & Time",
    "keywords": "unix timestamp converter"
  },
  {
    "name": "Week Number Calculator",
    "url": "/date-time/week-number-calculator.html",
    "category": "Date & Time",
    "keywords": "week number calculator"
  },
  {
    "name": "Working Days Calculator",
    "url": "/date-time/working-days-calculator.html",
    "category": "Date & Time",
    "keywords": "working days calculator"
  },
  {
    "name": "Break-Even Calculator",
    "url": "/finance/break-even-calculator.html",
    "category": "Finance",
    "keywords": "break even calculator"
  },
  {
    "name": "Compound Interest Calculator",
    "url": "/finance/compound-interest-calculator.html",
    "category": "Finance",
    "keywords": "compound interest calculator"
  },
  {
    "name": "Currency Converter",
    "url": "/finance/currency-converter.html",
    "category": "Finance",
    "keywords": "currency converter"
  },
  {
    "name": "Discount Calculator",
    "url": "/finance/discount-calculator.html",
    "category": "Finance",
    "keywords": "discount calculator"
  },
  {
    "name": "Inflation Calculator",
    "url": "/finance/inflation-calculator.html",
    "category": "Finance",
    "keywords": "inflation calculator"
  },
  {
    "name": "Loan EMI Calculator",
    "url": "/finance/loan-emi-calculator.html",
    "category": "Finance",
    "keywords": "loan emi calculator"
  },
  {
    "name": "Mortgage Calculator",
    "url": "/finance/mortgage-calculator.html",
    "category": "Finance",
    "keywords": "mortgage calculator"
  },
  {
    "name": "ROI Calculator",
    "url": "/finance/roi-calculator.html",
    "category": "Finance",
    "keywords": "roi calculator"
  },
  {
    "name": "Simple Interest Calculator",
    "url": "/finance/simple-interest-calculator.html",
    "category": "Finance",
    "keywords": "simple interest calculator"
  },
  {
    "name": "Tip Calculator",
    "url": "/finance/tip-calculator.html",
    "category": "Finance",
    "keywords": "tip calculator"
  },
  {
    "name": "BMI Calculator",
    "url": "/health-fitness/bmi-calculator.html",
    "category": "Health & Fitness",
    "keywords": "bmi calculator"
  },
  {
    "name": "Body Fat Calculator",
    "url": "/health-fitness/body-fat-calculator.html",
    "category": "Health & Fitness",
    "keywords": "body fat calculator"
  },
  {
    "name": "Calorie Calculator",
    "url": "/health-fitness/calorie-calculator.html",
    "category": "Health & Fitness",
    "keywords": "calorie calculator"
  },
  {
    "name": "Heart Rate Zone Calculator",
    "url": "/health-fitness/heart-rate-zone-calculator.html",
    "category": "Health & Fitness",
    "keywords": "heart rate zone calculator"
  },
  {
    "name": "Ideal Weight Calculator",
    "url": "/health-fitness/ideal-weight-calculator.html",
    "category": "Health & Fitness",
    "keywords": "ideal weight calculator"
  },
  {
    "name": "Pregnancy Calculator",
    "url": "/health-fitness/pregnancy-calculator.html",
    "category": "Health & Fitness",
    "keywords": "pregnancy calculator"
  },
  {
    "name": "Protein Intake Calculator",
    "url": "/health-fitness/protein-intake-calculator.html",
    "category": "Health & Fitness",
    "keywords": "protein intake calculator"
  },
  {
    "name": "Sleep Calculator",
    "url": "/health-fitness/sleep-calculator.html",
    "category": "Health & Fitness",
    "keywords": "sleep calculator"
  },
  {
    "name": "Steps to Calories Calculator",
    "url": "/health-fitness/steps-to-calories-calculator.html",
    "category": "Health & Fitness",
    "keywords": "steps to calories calculator"
  },
  {
    "name": "Water Intake Calculator",
    "url": "/health-fitness/water-intake-calculator.html",
    "category": "Health & Fitness",
    "keywords": "water intake calculator"
  },
  {
    "name": "Advance Tax Calculator India",
    "url": "/india/advance-tax-calculator.html",
    "category": "India",
    "keywords": "advance tax calculator india india rupee tax investment loan gst salary"
  },
  {
    "name": "Andhra Pradesh Electricity Bill Calculator",
    "url": "/india/ap-electricity-bill-calculator.html",
    "category": "India",
    "keywords": "andhra pradesh electricity bill calculator india rupee tax investment loan gst salary"
  },
  {
    "name": "Electricity Bill Calculator India",
    "url": "/india/electricity/index.html",
    "category": "India",
    "keywords": "electricity bill calculator india all states discom tariff slab units kwh power bill"
  },
  {
    "name": "Car Loan EMI Calculator",
    "url": "/india/car-loan-emi-calculator.html",
    "category": "India",
    "keywords": "car loan emi calculator india rupee tax investment loan gst salary"
  },
  {
    "name": "CGPA to Percentage Calculator",
    "url": "/india/cgpa-to-percentage-calculator.html",
    "category": "India",
    "keywords": "cgpa to percentage calculator india rupee tax investment loan gst salary"
  },
  {
    "name": "CTC to In-Hand Salary Calculator",
    "url": "/india/ctc-salary-calculator.html",
    "category": "India",
    "keywords": "ctc to in hand salary calculator india rupee tax investment loan gst salary"
  },
  {
    "name": "Fixed Deposit (FD) Calculator",
    "url": "/india/fd-calculator.html",
    "category": "India",
    "keywords": "fixed deposit  fd  calculator india rupee tax investment loan gst salary"
  },
  {
    "name": "Gold Price Calculator India",
    "url": "/india/gold-price-calculator.html",
    "category": "India",
    "keywords": "gold price calculator india india rupee tax investment loan gst salary"
  },
  {
    "name": "Gratuity Calculator",
    "url": "/india/gratuity-calculator.html",
    "category": "India",
    "keywords": "gratuity calculator india rupee tax investment loan gst salary"
  },
  {
    "name": "GST Calculator",
    "url": "/india/gst-calculator.html",
    "category": "India",
    "keywords": "gst calculator india rupee tax investment loan gst salary"
  },
  {
    "name": "Home Loan EMI Calculator",
    "url": "/india/home-loan-emi-calculator.html",
    "category": "India",
    "keywords": "home loan emi calculator india rupee tax investment loan gst salary"
  },
  {
    "name": "HRA Exemption Calculator (Section 10-13A)",
    "url": "/india/hra-exemption-calculator.html",
    "category": "India",
    "keywords": "hra exemption calculator  section 10 13a  india rupee tax investment loan gst salary"
  },
  {
    "name": "Income Tax Calculator India (FY 2024-25)",
    "url": "/india/income-tax-calculator.html",
    "category": "India",
    "keywords": "income tax calculator india  fy 2024 25  india rupee tax investment loan gst salary"
  },
  {
    "name": "NPS Calculator (National Pension Scheme)",
    "url": "/india/nps-calculator.html",
    "category": "India",
    "keywords": "nps calculator  national pension scheme  india rupee tax investment loan gst salary"
  },
  {
    "name": "Car On-Road Price Calculator India",
    "url": "/india/on-road-price-calculator.html",
    "category": "India",
    "keywords": "car on road price calculator india india rupee tax investment loan gst salary"
  },
  {
    "name": "EPF / PF Calculator (Employee Provident Fund)",
    "url": "/india/pf-epf-calculator.html",
    "category": "India",
    "keywords": "epf   pf calculator  employee provident fund  india rupee tax investment loan gst salary"
  },
  {
    "name": "PPF Calculator (Public Provident Fund)",
    "url": "/india/ppf-calculator.html",
    "category": "India",
    "keywords": "ppf calculator  public provident fund  india rupee tax investment loan gst salary"
  },
  {
    "name": "SIP Calculator (Systematic Investment Plan)",
    "url": "/india/sip-calculator.html",
    "category": "India",
    "keywords": "sip calculator  systematic investment plan  india rupee tax investment loan gst salary"
  },
  {
    "name": "Stamp Duty India Calculator",
    "url": "/india/stamp-duty/index.html",
    "category": "India",
    "keywords": "stamp duty calculator india property registration charges state wise women discount circle rate"
  },
  {
    "name": "Delhi Stamp Duty Calculator",
    "url": "/india/stamp-duty/delhi.html",
    "category": "India",
    "keywords": "delhi stamp duty calculator property registration women discount circle rate"
  },
  {
    "name": "Maharashtra Stamp Duty Calculator",
    "url": "/india/stamp-duty/maharashtra.html",
    "category": "India",
    "keywords": "maharashtra mumbai pune stamp duty calculator property registration women discount metro cess"
  },
  {
    "name": "Karnataka Stamp Duty Calculator",
    "url": "/india/stamp-duty/karnataka.html",
    "category": "India",
    "keywords": "karnataka bengaluru stamp duty calculator property registration kaveri guideline value"
  },
  {
    "name": "Tamil Nadu Stamp Duty Calculator",
    "url": "/india/stamp-duty/tamil-nadu.html",
    "category": "India",
    "keywords": "tamil nadu chennai stamp duty calculator property registration tnreginet guideline value"
  },
  {
    "name": "Telangana Stamp Duty Calculator",
    "url": "/india/stamp-duty/telangana.html",
    "category": "India",
    "keywords": "telangana hyderabad stamp duty calculator property registration transfer duty igrs"
  },
  {
    "name": "Andhra Pradesh Stamp Duty Calculator",
    "url": "/india/stamp-duty/andhra-pradesh.html",
    "category": "India",
    "keywords": "andhra pradesh ap stamp duty calculator property registration transfer duty"
  },
  {
    "name": "Gujarat Stamp Duty Calculator",
    "url": "/india/stamp-duty/gujarat.html",
    "category": "India",
    "keywords": "gujarat ahmedabad stamp duty calculator property registration jantri garvi"
  },
  {
    "name": "Uttar Pradesh Stamp Duty Calculator",
    "url": "/india/stamp-duty/uttar-pradesh.html",
    "category": "India",
    "keywords": "uttar pradesh up noida lucknow stamp duty calculator property registration women discount"
  },
  {
    "name": "West Bengal Stamp Duty Calculator",
    "url": "/india/stamp-duty/west-bengal.html",
    "category": "India",
    "keywords": "west bengal kolkata stamp duty calculator property registration urban rural"
  },
  {
    "name": "Sukanya Samriddhi Yojana (SSY) Calculator",
    "url": "/india/sukanya-samriddhi-calculator.html",
    "category": "India",
    "keywords": "sukanya samriddhi yojana  ssy  calculator india rupee tax investment loan gst salary"
  },
  {
    "name": "TDS Calculator India",
    "url": "/india/tds-calculator.html",
    "category": "India",
    "keywords": "tds calculator india india rupee tax investment loan gst salary"
  },
  {
    "name": "Average Calculator (Mean, Median, Mode, Range)",
    "url": "/maths/average-calculator.html",
    "category": "Math",
    "keywords": "average calculator  mean  median  mode  range "
  },
  {
    "name": "Exponent Calculator",
    "url": "/maths/exponent-calculator.html",
    "category": "Math",
    "keywords": "exponent calculator"
  },
  {
    "name": "Fraction Calculator",
    "url": "/maths/fraction-calculator.html",
    "category": "Math",
    "keywords": "fraction calculator"
  },
  {
    "name": "LCM and HCF Calculator",
    "url": "/maths/lcm-hcf-calculator.html",
    "category": "Math",
    "keywords": "lcm and hcf calculator"
  },
  {
    "name": "Percentage Calculator",
    "url": "/maths/percentage-calculator.html",
    "category": "Math",
    "keywords": "percentage calculator"
  },
  {
    "name": "Probability Calculator",
    "url": "/maths/probability-calculator.html",
    "category": "Math",
    "keywords": "probability calculator"
  },
  {
    "name": "Quadratic Equation Solver",
    "url": "/maths/quadratic-equation-solver.html",
    "category": "Math",
    "keywords": "quadratic equation solver"
  },
  {
    "name": "Ratio Calculator",
    "url": "/maths/ratio-calculator.html",
    "category": "Math",
    "keywords": "ratio calculator"
  },
  {
    "name": "Scientific Calculator",
    "url": "/maths/scientific-calculator.html",
    "category": "Math",
    "keywords": "scientific calculator"
  },
  {
    "name": "Square Root Calculator",
    "url": "/maths/square-root-calculator.html",
    "category": "Math",
    "keywords": "square root calculator"
  },
  {
    "name": "Density Calculator",
    "url": "/science-other/density-calculator.html",
    "category": "Science & Other",
    "keywords": "density calculator"
  },
  {
    "name": "Electricity Cost Calculator",
    "url": "/science-other/electricity-cost-calculator.html",
    "category": "Science & Other",
    "keywords": "electricity cost calculator"
  },
  {
    "name": "Fuel Efficiency Calculator",
    "url": "/science-other/fuel-efficiency-calculator.html",
    "category": "Science & Other",
    "keywords": "fuel efficiency calculator"
  },
  {
    "name": "GPA Calculator",
    "url": "/science-other/gpa-calculator.html",
    "category": "Science & Other",
    "keywords": "gpa calculator"
  },
  {
    "name": "Grade Calculator",
    "url": "/science-other/grade-calculator.html",
    "category": "Science & Other",
    "keywords": "grade calculator"
  },
  {
    "name": "Ohm's Law Calculator",
    "url": "/science-other/ohms-law-calculator.html",
    "category": "Science & Other",
    "keywords": "ohm s law calculator"
  },
  {
    "name": "Password Generator",
    "url": "/science-other/password-generator.html",
    "category": "Science & Other",
    "keywords": "password generator"
  },
  {
    "name": "Random Number Generator",
    "url": "/science-other/random-number-generator.html",
    "category": "Science & Other",
    "keywords": "random number generator"
  },
  {
    "name": "Speed Distance Time Calculator",
    "url": "/science-other/speed-distance-time-calculator.html",
    "category": "Science & Other",
    "keywords": "speed distance time calculator"
  },
  {
    "name": "Word Counter",
    "url": "/science-other/word-character-counter.html",
    "category": "Science & Other",
    "keywords": "word counter"
  },
  {
    "name": "Area Converter",
    "url": "/unit-converter/area-converter.html",
    "category": "Unit Converter",
    "keywords": "area converter"
  },
  {
    "name": "Data Storage Converter",
    "url": "/unit-converter/data-storage-converter.html",
    "category": "Unit Converter",
    "keywords": "data storage converter"
  },
  {
    "name": "Energy Converter",
    "url": "/unit-converter/energy-converter.html",
    "category": "Unit Converter",
    "keywords": "energy converter"
  },
  {
    "name": "Length Converter",
    "url": "/unit-converter/length-converter.html",
    "category": "Unit Converter",
    "keywords": "length converter"
  },
  {
    "name": "Number System Converter",
    "url": "/unit-converter/number-system-converter.html",
    "category": "Unit Converter",
    "keywords": "number system converter"
  },
  {
    "name": "Pressure Converter",
    "url": "/unit-converter/pressure-converter.html",
    "category": "Unit Converter",
    "keywords": "pressure converter"
  },
  {
    "name": "Speed Converter",
    "url": "/unit-converter/speed-converter.html",
    "category": "Unit Converter",
    "keywords": "speed converter"
  },
  {
    "name": "Temperature Converter",
    "url": "/unit-converter/temperature-converter.html",
    "category": "Unit Converter",
    "keywords": "temperature converter"
  },
  {
    "name": "Volume Converter",
    "url": "/unit-converter/volume-converter.html",
    "category": "Unit Converter",
    "keywords": "volume converter"
  },
  {
    "name": "Weight Converter",
    "url": "/unit-converter/weight-converter.html",
    "category": "Unit Converter",
    "keywords": "weight converter"
  }
];

function debounce(fn, ms) {
  let timer;
  return function debounced(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), ms);
  };
}

function formatIndianNumber(n) {
  const number = Number(n);
  if (!Number.isFinite(number)) return "0";
  return number.toLocaleString("en-IN", { maximumFractionDigits: 2 });
}

function formatCurrency(n, symbol = "$") {
  return `${symbol}${formatIndianNumber(Number(n).toFixed(2))}`;
}

function getPreferredNumberLocale() {
  const language = navigator.language || "en-US";
  const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
  if (/(^|-)IN\b/i.test(language) || timeZone === "Asia/Kolkata" || timeZone === "Asia/Calcutta") {
    return "en-IN";
  }
  return language;
}

function usesIndianNumberSystem() {
  return getPreferredNumberLocale() === "en-IN";
}

function parseFormattedNumber(value) {
  if (typeof value === "number") return Number.isFinite(value) ? value : 0;
  const cleaned = String(value || "").replace(/[^\d.-]/g, "");
  const normalized = cleaned
    .replace(/(?!^)-/g, "")
    .replace(/^(-?)\./, "$10.")
    .replace(/(\..*)\./g, "$1");
  const number = Number(normalized);
  return Number.isFinite(number) ? number : 0;
}

function formatInputNumber(value) {
  const raw = String(value || "").trim();
  if (!raw) return "";
  const cleaned = raw.replace(/[^\d.-]/g, "");
  if (!cleaned || cleaned === "-" || cleaned === ".") return cleaned;
  const isNegative = cleaned.trim().startsWith("-");
  const unsigned = cleaned.replace(/-/g, "");
  const hasDecimal = unsigned.includes(".");
  const [integerPart, ...decimalParts] = unsigned.split(".");
  const decimals = decimalParts.join("").replace(/\D/g, "");
  const integer = integerPart.replace(/\D/g, "") || "0";
  const formattedInteger = Number(integer).toLocaleString(getPreferredNumberLocale(), { maximumFractionDigits: 0 });
  return `${isNegative ? "-" : ""}${formattedInteger}${hasDecimal ? `.${decimals}` : ""}`;
}

function unformatAmountInput(input) {
  if (!input || input.dataset.amountFormat !== "true") return;
  const raw = String(input.value || "").trim();
  if (!raw) return;
  const cleaned = raw.replace(/[^\d.-]/g, "").replace(/(?!^)-/g, "").replace(/(\..*)\./g, "$1");
  input.value = cleaned;
}

function formatAmountInput(input) {
  if (!input || input.dataset.amountFormat !== "true") return;
  input.value = formatInputNumber(input.value);
}

function shouldFormatAmountInput(input) {
  if (!input || input.dataset.noAmountFormat === "true") return false;
  if (input.type === "range" || input.type === "checkbox" || input.type === "radio") return false;
  const group = input.closest(".calc-input-group") || input.parentElement;
  const label = group ? (group.querySelector("label")?.textContent || "") : "";
  const prefix = group ? (group.querySelector(".input-prefix span")?.textContent || "") : "";
  const haystack = `${label} ${prefix} ${input.id || ""}`.toLowerCase();
  if (/[₹$€£]/.test(prefix) || /[₹$€£]/.test(label)) return true;
  if (/(rate|percentage|percent|years|months|age|cgpa|grade|height|weight|units|kwh|load|tenure|period|temperature|speed|distance|time|score|ratio)/i.test(label)) {
    return false;
  }
  return /(amount|price|cost|salary|income|principal|loan|payment|rent|investment|contribution|balance|value|fee|tax|tds|deduction|deposit|revenue|expense|sales|profit|commission|insurance|ctc|hra|pf|emi)/i.test(haystack);
}

function prepareAmountInputsForCalculation() {
  document.querySelectorAll('input[data-amount-format="true"]').forEach(unformatAmountInput);
}

function reformatAmountInputs() {
  document.querySelectorAll('input[data-amount-format="true"]').forEach(formatAmountInput);
}

function scheduleAmountInputReformat() {
  window.setTimeout(reformatAmountInputs, 0);
}

function initAmountInputFormatting() {
  document.querySelectorAll(".calc-widget input").forEach((input) => {
    if (!shouldFormatAmountInput(input)) return;
    input.dataset.amountFormat = "true";
    input.dataset.originalType = input.type || "text";
    input.type = "text";
    input.inputMode = "decimal";
    input.autocomplete = "off";
    formatAmountInput(input);
  });
}

function updateRangeInput(range) {
  if (!range || range.type !== "range") return;
  const min = parseFormattedNumber(range.min);
  const max = parseFormattedNumber(range.max);
  const current = parseFormattedNumber(range.value);
  const denominator = max - min;
  const progress = denominator > 0 ? ((current - min) / denominator) * 100 : 0;
  range.style.setProperty("--range-progress", `${Math.min(100, Math.max(0, progress))}%`);
}

function updateAllRangeInputs() {
  document.querySelectorAll('.calc-widget input[type="range"]').forEach(updateRangeInput);
}

function scheduleRangeInputRefresh() {
  window.setTimeout(updateAllRangeInputs, 0);
}

function initRangeInputStyling() {
  updateAllRangeInputs();
}

document.addEventListener("input", () => {
  prepareAmountInputsForCalculation();
  scheduleAmountInputReformat();
  scheduleRangeInputRefresh();
}, true);

document.addEventListener("change", () => {
  prepareAmountInputsForCalculation();
  scheduleAmountInputReformat();
  scheduleRangeInputRefresh();
}, true);

document.addEventListener("click", () => {
  prepareAmountInputsForCalculation();
  scheduleAmountInputReformat();
  scheduleRangeInputRefresh();
}, true);

function resolveCalculatorUrl(url) {
  if (!url.startsWith("/")) return url;
  const currentPath = window.location.pathname.replace(/\\/g, "/");
  const firstSegment = currentPath.split("/").filter(Boolean)[0] || "";
  const rootSections = new Set(["maths", "india", "finance", "unit", "health-fitness", "date-time", "science-other", "company", "assets"]);
  if (window.location.protocol !== "file:" && window.location.hostname.endsWith("github.io") && firstSegment && !rootSections.has(firstSegment)) {
    return `/${firstSegment}${url}`;
  }
  if (window.location.protocol !== "file:") return url;
  const isSubPage = /\/(maths|india|finance|unit|health-fitness|date-time|science-other)\//.test(currentPath);
  return `${isSubPage ? "../" : ""}${url.slice(1)}`;
}

function renderSearchResults(results, container) {
  if (!container) return;
  if (!results.length) {
    container.innerHTML = '<div class="search-result-item"><span class="search-result-name">No calculators found</span></div>';
    container.classList.add("open");
    return;
  }
  container.innerHTML = results.slice(0, 8).map((item) => `
    <a class="search-result-item" href="${resolveCalculatorUrl(item.url)}">
      <span class="search-result-name">${item.name}</span>
      <span class="search-result-cat">${item.category}</span>
    </a>
  `).join("");
  container.classList.add("open");
}

function initSearch() {
  document.querySelectorAll("[data-search-input]").forEach((input) => {
    let resultsBox = input.parentElement.querySelector(".search-results");
    if (!resultsBox) {
      resultsBox = document.createElement("div");
      resultsBox.className = "search-results";
      input.parentElement.appendChild(resultsBox);
    }

    input.addEventListener("keyup", debounce(() => {
      const query = input.value.trim().toLowerCase();
      if (query.length < 2) {
        resultsBox.classList.remove("open");
        resultsBox.innerHTML = "";
        return;
      }
      const results = calculators.filter((calc) => {
        const haystack = `${calc.name} ${calc.category} ${calc.keywords}`.toLowerCase();
        return haystack.includes(query);
      });
      renderSearchResults(results, resultsBox);
    }, 120));

    document.addEventListener("click", (event) => {
      if (!input.parentElement.contains(event.target)) {
        resultsBox.classList.remove("open");
      }
    });
  });
}

function initMobileMenu() {
  const button = document.querySelector("[data-mobile-menu-btn]");
  const nav = document.querySelector("[data-mobile-nav]");
  if (!button || !nav) return;
  button.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("open");
    button.setAttribute("aria-expanded", String(isOpen));
  });
}

function initFAQ() {
  document.querySelectorAll(".faq-question").forEach((question) => {
    question.addEventListener("click", () => {
      const item = question.closest(".faq-item");
      const answer = item ? item.querySelector(".faq-answer") : question.nextElementSibling;
      if (!item || !answer) return;
      item.classList.toggle("open");
      answer.classList.toggle("open");
    });
  });
}

function initFeedbackModal() {
  const footerLinks = document.querySelector(".footer-company-links");
  if (!footerLinks || document.querySelector("[data-feedback-open]")) return;

  const openButton = document.createElement("button");
  openButton.type = "button";
  openButton.className = "footer-feedback-btn";
  openButton.dataset.feedbackOpen = "true";
  openButton.textContent = "Feedback";
  footerLinks.appendChild(openButton);

  if (!document.getElementById("feedback-modal")) {
    const overlay = document.createElement("div");
    overlay.className = "feedback-modal-overlay";
    overlay.id = "feedback-modal";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-labelledby", "feedback-title");
    overlay.innerHTML = `
      <div class="feedback-modal">
        <div class="feedback-modal-header">
          <div>
            <h2 class="feedback-modal-title" id="feedback-title">Send feedback</h2>
            <p class="feedback-modal-subtitle">Share a correction, suggestion, or issue. Your email app will open with everything filled in.</p>
          </div>
          <button class="feedback-modal-close" type="button" aria-label="Close feedback" data-feedback-close>&times;</button>
        </div>
        <form class="feedback-form" id="feedback-form">
          <div class="feedback-form-row">
            <span class="feedback-recipient">To: janamahi2010@gmail.com</span>
          </div>
          <div class="feedback-form-row">
            <label for="feedback-subject">Subject</label>
            <input id="feedback-subject" name="subject" type="text" required maxlength="120" placeholder="Feedback about Calculatorcity">
          </div>
          <div class="feedback-form-row">
            <label for="feedback-email">Your email</label>
            <input id="feedback-email" name="email" type="email" placeholder="you@example.com">
          </div>
          <div class="feedback-form-row">
            <label for="feedback-message">Message</label>
            <textarea id="feedback-message" name="message" required placeholder="Tell us what should be improved."></textarea>
          </div>
          <div class="feedback-actions">
            <button class="feedback-secondary" type="button" data-feedback-close>Cancel</button>
            <button class="feedback-submit" type="submit">Open email</button>
          </div>
        </form>
      </div>
    `;
    document.body.appendChild(overlay);
  }

  const overlay = document.getElementById("feedback-modal");
  const form = document.getElementById("feedback-form");
  const subjectInput = document.getElementById("feedback-subject");
  const emailInput = document.getElementById("feedback-email");
  const messageInput = document.getElementById("feedback-message");
  let previousFocus = null;

  function openModal() {
    previousFocus = document.activeElement;
    if (subjectInput && !subjectInput.value) subjectInput.value = `Feedback: ${document.title || "Calculatorcity"}`;
    overlay.classList.add("open");
    document.body.style.overflow = "hidden";
    setTimeout(() => subjectInput && subjectInput.focus(), 0);
  }

  function closeModal() {
    overlay.classList.remove("open");
    document.body.style.overflow = "";
    if (previousFocus && typeof previousFocus.focus === "function") previousFocus.focus();
  }

  openButton.addEventListener("click", openModal);
  overlay.addEventListener("click", event => {
    if (event.target === overlay || event.target.closest("[data-feedback-close]")) closeModal();
  });
  document.addEventListener("keydown", event => {
    if (event.key === "Escape" && overlay.classList.contains("open")) closeModal();
  });
  form.addEventListener("submit", event => {
    event.preventDefault();
    const subject = subjectInput.value.trim();
    const email = emailInput.value.trim();
    const message = messageInput.value.trim();
    if (!subject || !message) return;

    const body = [
      message,
      "",
      email ? `From: ${email}` : "",
      `Page: ${window.location.href}`
    ].filter(Boolean).join("\n");

    window.location.href = `mailto:janamahi2010@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    closeModal();
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initSearch();
  initMobileMenu();
  initFAQ();
  initAmountInputFormatting();
  initRangeInputStyling();
  initFeedbackModal();
});

