const calculators = [
  { name: 'Percentage Calculator', url: '/maths/percentage-calculator.html', category: 'Math', keywords: 'percent percentage change' },
  { name: 'Fraction Calculator', url: '/maths/fraction-calculator.html', category: 'Math', keywords: 'fraction add subtract multiply divide' },
  { name: 'Average Calculator', url: '/maths/average-calculator.html', category: 'Math', keywords: 'mean median mode range' },
  { name: 'Square Root Calculator', url: '/maths/square-root-calculator.html', category: 'Math', keywords: 'sqrt cube nth root' },
  { name: 'Ratio Calculator', url: '/maths/ratio-calculator.html', category: 'Math', keywords: 'ratio simplify equivalent scale' },
  { name: 'Scientific Calculator', url: '/maths/scientific-calculator.html', category: 'Math', keywords: 'scientific sin cos tan log' },
  { name: 'LCM and HCF Calculator', url: '/maths/lcm-hcf-calculator.html', category: 'Math', keywords: 'lcm hcf gcd factor' },
  { name: 'Exponent Calculator', url: '/maths/exponent-calculator.html', category: 'Math', keywords: 'power exponent' },
  { name: 'Probability Calculator', url: '/maths/probability-calculator.html', category: 'Math', keywords: 'probability combinations permutations' },
  { name: 'Quadratic Equation Solver', url: '/maths/quadratic-equation-solver.html', category: 'Math', keywords: 'quadratic roots discriminant' },
  { name: 'Compound Interest Calculator', url: '/finance/compound-interest-calculator.html', category: 'Finance', keywords: 'compound interest growth' },
  { name: 'Loan EMI Calculator', url: '/finance/loan-emi-calculator.html', category: 'Finance', keywords: 'emi loan amortization' },
  { name: 'Simple Interest Calculator', url: '/finance/simple-interest-calculator.html', category: 'Finance', keywords: 'simple interest' },
  { name: 'Currency Converter', url: '/finance/currency-converter.html', category: 'Finance', keywords: 'currency exchange' },
  { name: 'Discount Calculator', url: '/finance/discount-calculator.html', category: 'Finance', keywords: 'discount sale savings' },
  { name: 'Mortgage Calculator', url: '/finance/mortgage-calculator.html', category: 'Finance', keywords: 'mortgage home loan' },
  { name: 'ROI Calculator', url: '/finance/roi-calculator.html', category: 'Finance', keywords: 'return on investment' },
  { name: 'Tip Calculator', url: '/finance/tip-calculator.html', category: 'Finance', keywords: 'tip split bill' },
  { name: 'Break-Even Calculator', url: '/finance/break-even-calculator.html', category: 'Finance', keywords: 'break even revenue units' },
  { name: 'Inflation Calculator', url: '/finance/inflation-calculator.html', category: 'Finance', keywords: 'inflation money value' },
  { name: 'Length Converter', url: '/unit-converter/length-converter.html', category: 'Unit Converter', keywords: 'length km meter feet inch' },
  { name: 'Weight Converter', url: '/unit-converter/weight-converter.html', category: 'Unit Converter', keywords: 'weight kg pound ounce' },
  { name: 'Temperature Converter', url: '/unit-converter/temperature-converter.html', category: 'Unit Converter', keywords: 'temperature celsius fahrenheit kelvin' },
  { name: 'Speed Converter', url: '/unit-converter/speed-converter.html', category: 'Unit Converter', keywords: 'speed kmh mph knots' },
  { name: 'Area Converter', url: '/unit-converter/area-converter.html', category: 'Unit Converter', keywords: 'area acre hectare cent' },
  { name: 'Volume Converter', url: '/unit-converter/volume-converter.html', category: 'Unit Converter', keywords: 'volume litre gallon cup' },
  { name: 'Data Storage Converter', url: '/unit-converter/data-storage-converter.html', category: 'Unit Converter', keywords: 'data storage bytes mb gb' },
  { name: 'Energy Converter', url: '/unit-converter/energy-converter.html', category: 'Unit Converter', keywords: 'energy joule calorie kwh' },
  { name: 'Pressure Converter', url: '/unit-converter/pressure-converter.html', category: 'Unit Converter', keywords: 'pressure psi bar atm' },
  { name: 'Number System Converter', url: '/unit-converter/number-system-converter.html', category: 'Unit Converter', keywords: 'binary octal decimal hex' },
  { name: 'BMI Calculator', url: '/health-fitness/bmi-calculator.html', category: 'Health & Fitness', keywords: 'bmi body mass index' },
  { name: 'Calorie Calculator', url: '/health-fitness/calorie-calculator.html', category: 'Health & Fitness', keywords: 'calorie tdee bmr' },
  { name: 'Body Fat Percentage Calculator', url: '/health-fitness/body-fat-calculator.html', category: 'Health & Fitness', keywords: 'body fat navy method' },
  { name: 'Ideal Weight Calculator', url: '/health-fitness/ideal-weight-calculator.html', category: 'Health & Fitness', keywords: 'ideal healthy weight' },
  { name: 'Pregnancy Calculator', url: '/health-fitness/pregnancy-calculator.html', category: 'Health & Fitness', keywords: 'pregnancy due date' },
  { name: 'Water Intake Calculator', url: '/health-fitness/water-intake-calculator.html', category: 'Health & Fitness', keywords: 'water hydration' },
  { name: 'Heart Rate Zone Calculator', url: '/health-fitness/heart-rate-zone-calculator.html', category: 'Health & Fitness', keywords: 'heart rate zones' },
  { name: 'Protein Intake Calculator', url: '/health-fitness/protein-intake-calculator.html', category: 'Health & Fitness', keywords: 'protein daily goal' },
  { name: 'Sleep Calculator', url: '/health-fitness/sleep-calculator.html', category: 'Health & Fitness', keywords: 'sleep cycles bedtime' },
  { name: 'Steps to Calories Calculator', url: '/health-fitness/steps-to-calories-calculator.html', category: 'Health & Fitness', keywords: 'steps calories walking' },
  { name: 'Age Calculator', url: '/date-time/age-calculator.html', category: 'Date & Time', keywords: 'age birthday' },
  { name: 'Date Difference Calculator', url: '/date-time/date-difference-calculator.html', category: 'Date & Time', keywords: 'date difference days' },
  { name: 'Time Calculator', url: '/date-time/time-calculator.html', category: 'Date & Time', keywords: 'add subtract time' },
  { name: 'Days Until Calculator', url: '/date-time/days-until-calculator.html', category: 'Date & Time', keywords: 'countdown days until' },
  { name: 'Time Zone Converter', url: '/date-time/time-zone-converter.html', category: 'Date & Time', keywords: 'timezone world clock' },
  { name: 'Working Days Calculator', url: '/date-time/working-days-calculator.html', category: 'Date & Time', keywords: 'business working days' },
  { name: 'Unix Timestamp Converter', url: '/date-time/unix-timestamp-converter.html', category: 'Date & Time', keywords: 'unix timestamp epoch' },
  { name: 'Week Number Calculator', url: '/date-time/week-number-calculator.html', category: 'Date & Time', keywords: 'iso week number' },
  { name: 'Retirement Calculator', url: '/date-time/retirement-date-calculator.html', category: 'Date & Time', keywords: 'retirement date age' },
  { name: 'Leap Year Calculator', url: '/date-time/leap-year-calculator.html', category: 'Date & Time', keywords: 'leap year' },
  { name: "Ohm's Law Calculator", url: '/science-other/ohms-law-calculator.html', category: 'Science & Other', keywords: 'ohm voltage current resistance' },
  { name: 'GPA Calculator', url: '/science-other/gpa-calculator.html', category: 'Science & Other', keywords: 'gpa grade points' },
  { name: 'Grade Calculator', url: '/science-other/grade-calculator.html', category: 'Science & Other', keywords: 'grade final exam' },
  { name: 'Density Calculator', url: '/science-other/density-calculator.html', category: 'Science & Other', keywords: 'density mass volume' },
  { name: 'Speed Distance Time Calculator', url: '/science-other/speed-distance-time-calculator.html', category: 'Science & Other', keywords: 'speed distance time' },
  { name: 'Random Number Generator', url: '/science-other/random-number-generator.html', category: 'Science & Other', keywords: 'random number dice coin' },
  { name: 'Password Generator', url: '/science-other/password-generator.html', category: 'Science & Other', keywords: 'password secure' },
  { name: 'Word Counter', url: '/science-other/word-character-counter.html', category: 'Science & Other', keywords: 'word character counter' },
  { name: 'Fuel Efficiency Calculator', url: '/science-other/fuel-efficiency-calculator.html', category: 'Science & Other', keywords: 'fuel mileage cost' },
  { name: 'Electricity Cost Calculator', url: '/science-other/electricity-cost-calculator.html', category: 'Science & Other', keywords: 'electricity cost kwh' },
  { name: 'GST Calculator', url: '/india/gst-calculator.html', category: 'India', keywords: 'india rupee tax investment loan gst' }
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

function resolveCalculatorUrl(url) {
  if (window.location.protocol !== "file:" || !url.startsWith("/")) return url;
  const currentPath = window.location.pathname.replace(/\\/g, "/");
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

document.addEventListener("DOMContentLoaded", () => {
  initSearch();
  initMobileMenu();
  initFAQ();
});
