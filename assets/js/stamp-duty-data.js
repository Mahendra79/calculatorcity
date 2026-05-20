(function () {
  "use strict";

  const stampDutyData = {
    "andhra-pradesh": {
      name: "Andhra Pradesh",
      slug: "andhra-pradesh",
      color: "#0ea5e9",
      flag: "🏛️",
      stampDuty: { male: 5, female: 5, joint: 5 },
      registrationCharges: { male: 1.5, female: 1.5, joint: 1.5 },
      transferDuty: 1.5,
      hasWomenDiscount: false,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { stamp: 5, reg: 1.5 },
        commercial: { stamp: 5, reg: 1.5 },
        agricultural: { stamp: 1, reg: 0.5 }
      },
      minimumValue: null,
      notes: "AP charges additional transfer duty of 1.5% on property transfers. Total effective cost: 8% of property value.",
      seo: {
        title: "AP Stamp Duty Calculator 2025 — Andhra Pradesh Property Registration | Calculatorcity",
        description: "Calculate stamp duty and registration charges for property purchase in Andhra Pradesh. AP stamp duty is 5% + 1.5% registration + 1.5% transfer duty. Free and accurate.",
        h1: "Andhra Pradesh Stamp Duty Calculator",
        subtitle: "Calculate AP property stamp duty, registration charges and transfer duty instantly."
      },
      content: {
        howItWorks: `<p>Andhra Pradesh charges stamp duty at <strong>5% of the property market value or circle rate (whichever is higher)</strong>, plus a registration charge of 1.5% and an additional transfer duty of 1.5%. This makes the total transaction cost approximately 8% of the property value in AP.</p>
      <p>The stamp duty is calculated on the higher of: (1) the actual transaction value, or (2) the government-declared circle rate (also called market value guideline) for that locality. If you buy a property for ₹50 lakhs but the circle rate is ₹60 lakhs, stamp duty is calculated on ₹60 lakhs.</p>
      <p>Unlike states like Maharashtra and Delhi, Andhra Pradesh does not offer a women discount on stamp duty. Both male and female buyers pay the same rates.</p>`,
        stateSpecific: `<h2>AP property registration process</h2>
      <p>Property registration in AP is handled through the Registration and Stamps Department. You can register property at the Sub-Registrar Office (SRO) of the district where the property is located. AP offers online slot booking for registration appointments through the Dharani portal.</p>
      <p>The <strong>Dharani portal</strong> is AP's integrated land records management system that handles agricultural land transactions, while the Registration department handles urban property registrations.</p>
      <h2>Documents required for AP property registration</h2>
      <p>Original sale deed, parent documents, Pattadar passbook (for agricultural land), Encumbrance Certificate (EC), identity proof of buyer and seller, two witnesses with ID proof, and demand draft for stamp duty and registration charges payable to the Sub-Registrar.</p>`,
        faq: [
          { q: "What is the stamp duty rate in Andhra Pradesh 2025?", a: "Andhra Pradesh stamp duty is 5% of the property value for all categories (residential, commercial). In addition, 1.5% registration charges and 1.5% transfer duty are levied, making the total effective cost approximately 8% of property value. For agricultural land, stamp duty is 1% with 0.5% registration charges." },
          { q: "Does AP offer women discount on stamp duty?", a: "No. Andhra Pradesh does not offer a special discount on stamp duty for women buyers. Both male and female buyers pay the same 5% stamp duty and 1.5% registration charges. This is unlike Delhi (2% less for women), Maharashtra (1% concession), and Haryana (2% less for women)." },
          { q: "What is transfer duty in AP?", a: "Andhra Pradesh levies an additional Transfer Duty of 1.5% on property purchases, over and above the stamp duty and registration charges. This makes AP's total property transaction cost approximately 8% (5% + 1.5% + 1.5%), which is higher than many neighbouring states like Telangana (5%) and Gujarat (5.9%)." },
          { q: "What is the circle rate in Andhra Pradesh?", a: "Circle rate (called Guideline Value in AP) is the minimum value set by the government for property transactions in a specific area. Stamp duty is calculated on the circle rate or actual transaction value, whichever is higher. Circle rates are fixed by the Registration and Stamps Department and vary by locality, road type, and property category." },
          { q: "How to pay stamp duty in Andhra Pradesh?", a: "Stamp duty in AP can be paid through e-stamping at authorised stamp vendors, or through demand draft at the Sub-Registrar Office. Online payment is also available through the CFMS (Comprehensive Financial Management System) portal. The payment must be made before or at the time of registration at the Sub-Registrar Office." },
          { q: "What is the registration fee for property in AP?", a: "Registration charges in AP are 1.5% of the property value or circle rate (whichever is higher). There is no upper cap on registration fees in AP. For a ₹50 lakh property, the registration charge would be ₹75,000. This is in addition to stamp duty (₹2.50 lakh) and transfer duty (₹75,000)." }
        ]
      }
    },

    telangana: {
      name: "Telangana",
      slug: "telangana",
      color: "#f97316",
      flag: "🌿",
      stampDuty: { male: 4, female: 4, joint: 4 },
      registrationCharges: { male: 0.5, female: 0.5, joint: 0.5 },
      transferDuty: 1.5,
      hasWomenDiscount: false,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { stamp: 4, reg: 0.5 },
        commercial: { stamp: 4, reg: 0.5 },
        agricultural: { stamp: 1, reg: 0.5 }
      },
      minimumValue: null,
      notes: "Telangana has lowest registration charges (0.5%) in South India. Transfer duty of 1.5% additional.",
      seo: {
        title: "Telangana Stamp Duty Calculator 2025 — TS Property Registration | Calculatorcity",
        description: "Calculate stamp duty and registration charges for property in Telangana. TS stamp duty 4% + 0.5% registration + 1.5% transfer duty. Accurate and instant.",
        h1: "Telangana Stamp Duty Calculator",
        subtitle: "Calculate TS property stamp duty, registration charges and transfer duty."
      },
      content: {
        howItWorks: `<p>Telangana charges stamp duty at <strong>4% of the property value</strong>, which is lower than Andhra Pradesh (5%). The registration charge is just 0.5% — one of the lowest in South India. However, a transfer duty of 1.5% is additionally levied, making the effective total approximately 6% of property value.</p>
      <p>Telangana's IGRS (Inspector General of Registration and Stamps) department manages property registrations. The state's Dharani portal handles agricultural land mutations while urban property registrations go through the Registration department.</p>`,
        stateSpecific: `<h2>IGRS Telangana — property registration</h2>
      <p>Telangana's IGRS portal (igrs.telangana.gov.in) allows online slot booking for property registration. The Sub-Registrar Office of the mandal/area where property is located handles registrations.</p>
      <h2>Hyderabad property registration</h2>
      <p>Hyderabad properties fall under GHMC limits. Urban properties have different circle rates set by IGRS TS. High-demand areas like Banjara Hills, Jubilee Hills, Gachibowli have significantly higher circle rates than peripheral areas.</p>`,
        faq: [
          { q: "What is stamp duty in Telangana 2025?", a: "Telangana stamp duty is 4% of property value. Registration charges are 0.5% and transfer duty is 1.5%. Total effective cost is approximately 6% of property value. This is lower than AP (8%) and Maharashtra (6-7%)." },
          { q: "Is stamp duty lower in TS or AP?", a: "Telangana has lower stamp duty (4%) compared to AP (5%). TS registration charges (0.5%) are also lower than AP (1.5%). However both states levy 1.5% transfer duty. Total: TS = 6%, AP = 8%. Buying in TS saves approximately 2% of property value." },
          { q: "What is the IGRS Telangana website?", a: "IGRS Telangana website is igrs.telangana.gov.in. You can check property market values, book registration slots, search encumbrance certificates, and pay stamp duty online through this portal." },
          { q: "Does Telangana offer stamp duty reduction for women?", a: "No. Telangana does not offer a special women discount on stamp duty. All buyers regardless of gender pay the same 4% stamp duty and 0.5% registration charges." },
          { q: "What documents are needed for property registration in Telangana?", a: "You need: original sale deed, parent documents (chain of title), EC (Encumbrance Certificate), Pattadar Passbook for agricultural land, identity proof of buyer and seller, address proof, two witnesses with ID, and demand draft for stamp duty and registration charges." },
          { q: "How to check circle rate in Telangana?", a: "Circle rates (market values) in Telangana can be checked on the IGRS TS website. Select the district, mandal, and village/locality to see the current guideline value per square yard or square foot for your area." }
        ]
      }
    },

    karnataka: {
      name: "Karnataka",
      slug: "karnataka",
      color: "#dc2626",
      flag: "🦁",
      stampDuty: { male: 5, female: 5, joint: 5 },
      registrationCharges: { male: 1, female: 1, joint: 1 },
      transferDuty: 0,
      hasWomenDiscount: false,
      hasUrbanRural: true,
      urban: { stamp: 5, reg: 1 },
      rural: { stamp: 3, reg: 1 },
      propertyTypes: {
        residential: { stamp: 5, reg: 1 },
        commercial: { stamp: 5, reg: 1 },
        agricultural: { stamp: 3, reg: 1 }
      },
      minimumValue: 2000000,
      belowMinStamp: 2,
      notes: "KA: 2% for properties below ₹20L, 3% for ₹20L-₹45L, 5% above ₹45L. Different for affordable housing.",
      seo: {
        title: "Karnataka Stamp Duty Calculator 2025 — Property Registration KA | Calculatorcity",
        description: "Calculate stamp duty for Karnataka property. Stamp duty 2-5% based on property value. Bengaluru, Mysuru, Hubli registration charges. Free and accurate.",
        h1: "Karnataka Stamp Duty Calculator",
        subtitle: "Karnataka property stamp duty — rates vary by property value. Bengaluru and all KA districts."
      },
      content: {
        howItWorks: `<p>Karnataka has a <strong>tiered stamp duty structure</strong> based on property value: 2% for properties below ₹20 lakhs, 3% for properties between ₹20 lakhs and ₹45 lakhs, and 5% for properties above ₹45 lakhs. Registration charges are 1% across all categories.</p>
      <p>This tiered structure makes Karnataka relatively affordable for first-time homebuyers purchasing properties in the ₹20-45 lakh range. The KAVERI portal (kaveri.karnataka.gov.in) manages all property registration services.</p>`,
        stateSpecific: `<h2>Bengaluru property registration</h2>
      <p>Bengaluru properties have some of the highest circle rates in Karnataka due to IT corridor demand. Areas like Whitefield, Electronic City, Sarjapur Road, and Hebbal have high market values. Registration must be done at the Sub-Registrar Office of the zone where property is located.</p>
      <h2>KAVERI portal — Karnataka registration</h2>
      <p>The KAVERI (Karnataka Valuation and E-Registration) portal allows online appointment booking, property valuation lookup, stamp duty payment, and document upload. This has significantly reduced registration time in Karnataka.</p>`,
        faq: [
          { q: "What is stamp duty in Karnataka 2025?", a: "Karnataka stamp duty depends on property value: 2% for below ₹20 lakhs, 3% for ₹20 lakhs to ₹45 lakhs, and 5% for above ₹45 lakhs. Registration charges are 1% across all values. Total cost: 3% (below 20L), 4% (20-45L), or 6% (above 45L)." },
          { q: "What is KAVERI online registration Karnataka?", a: "KAVERI (Karnataka Valuation and E-Registration) is the official portal for property registration in Karnataka. Visit kaveri.karnataka.gov.in to search property values, book appointments, pay stamp duty online, and track registration status." },
          { q: "Is there women discount on stamp duty in Karnataka?", a: "Karnataka does not have a specific women discount on stamp duty. All buyers pay the same rates based on property value (2-5%). Some affordable housing schemes may have different rates but these are not gender-specific." },
          { q: "How is stamp duty calculated for Bengaluru property?", a: "For a ₹80 lakh Bengaluru flat: stamp duty = 5% × ₹80L = ₹4,00,000. Registration = 1% × ₹80L = ₹80,000. Total = ₹4,80,000. Note: if the guideline value is higher than ₹80L, calculation is on the guideline value." },
          { q: "What are the documents for property registration in Karnataka?", a: "Required documents: original sale deed (on stamp paper), earlier title documents, Khata certificate and extract, tax paid receipts, EC (Encumbrance Certificate), identity and address proof of buyer and seller, two witnesses." },
          { q: "What is guideline value in Karnataka?", a: "Guideline value is the minimum value set by the government for property in a specific locality in Karnataka. Stamp duty is calculated on guideline value or actual transaction value whichever is higher. Check current guideline values on the KAVERI portal by entering the locality details." }
        ]
      }
    },

    "tamil-nadu": {
      name: "Tamil Nadu",
      slug: "tamil-nadu",
      color: "#7c3aed",
      flag: "🌺",
      stampDuty: { male: 7, female: 7, joint: 7 },
      registrationCharges: { male: 4, female: 4, joint: 4 },
      transferDuty: 0,
      hasWomenDiscount: false,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { stamp: 7, reg: 4 },
        commercial: { stamp: 7, reg: 4 },
        agricultural: { stamp: 4, reg: 2 }
      },
      minimumValue: null,
      notes: "Tamil Nadu has highest registration charges (4%) in India. Total: 11% of property value.",
      seo: {
        title: "Tamil Nadu Stamp Duty Calculator 2025 — TN Property Registration | Calculatorcity",
        description: "Calculate stamp duty for Tamil Nadu property. TN stamp duty 7% + 4% registration = 11% total. Chennai, Coimbatore, Madurai registration charges. Accurate.",
        h1: "Tamil Nadu Stamp Duty Calculator",
        subtitle: "TN property stamp duty — 7% stamp duty + 4% registration. Highest in South India."
      },
      content: {
        howItWorks: `<p>Tamil Nadu has the <strong>highest property registration cost in South India</strong> — stamp duty at 7% plus registration charges at 4%, totalling 11% of property value. This is significantly higher than neighbouring Telangana (6%) and Karnataka (4-6%).</p>
      <p>The Registration Department of Tamil Nadu manages all property registrations. The TNREGINET portal (tnreginet.gov.in) provides guideline values, EC search, and appointment booking services.</p>`,
        stateSpecific: `<h2>Chennai property registration</h2>
      <p>Chennai has very high guideline values, particularly in areas like Anna Nagar, T Nagar, Velachery, OMR, and ECR. The actual stamp duty burden is significant due to both the high property values and the 11% total rate.</p>
      <h2>TNREGINET portal</h2>
      <p>The TNREGINET portal (tnreginet.gov.in) allows you to check guideline values for any area in Tamil Nadu, search encumbrance certificates, book appointments, and check registration status.</p>`,
        faq: [
          { q: "What is stamp duty in Tamil Nadu 2025?", a: "Tamil Nadu stamp duty is 7% of property value, and registration charges are 4% — giving a total of 11%. This is the highest combination in South India. For a ₹50 lakh property: stamp duty = ₹3.5 lakhs, registration = ₹2 lakhs, total = ₹5.5 lakhs additional cost." },
          { q: "Why is Tamil Nadu stamp duty so high?", a: "Tamil Nadu historically has had high stamp duty rates. The 7% stamp duty and 4% registration charges (11% total) are among the highest in India. The high registration charges have been a long-standing policy. States like Telangana (6%) and Karnataka (6%) are significantly cheaper for property registration." },
          { q: "Does TN offer women discount on stamp duty?", a: "Tamil Nadu does not offer a general women discount on stamp duty. Both male and female buyers pay the same 7% stamp duty and 4% registration charges. Some specific government housing schemes may have concessional rates but these are not universally applicable." },
          { q: "What is TNREGINET?", a: "TNREGINET is the official portal of the Tamil Nadu Registration Department (tnreginet.gov.in). It provides services like guideline value search by village/town, encumbrance certificate search, appointment booking for property registration, document status tracking, and certified copy requests." },
          { q: "How to calculate stamp duty for Chennai property?", a: "For a Chennai flat of ₹80 lakhs: Stamp duty = 7% × ₹80L = ₹5,60,000. Registration = 4% × ₹80L = ₹3,20,000. Total additional cost = ₹8,80,000. This is calculated on guideline value or transaction value, whichever is higher." },
          { q: "Can I pay stamp duty online in Tamil Nadu?", a: "Yes. Stamp duty in Tamil Nadu can be paid through the TNREGINET portal using net banking, credit/debit card, or UPI. E-stamping is also available. The payment receipt is required at the time of registration at the Sub-Registrar Office." }
        ]
      }
    },

    maharashtra: {
      name: "Maharashtra",
      slug: "maharashtra",
      color: "#f59e0b",
      flag: "🦁",
      stampDuty: { male: 5, female: 4, joint: 4.5 },
      registrationCharges: { male: 1, female: 1, joint: 1 },
      transferDuty: 0,
      hasWomenDiscount: true,
      womenDiscount: 1,
      hasUrbanRural: true,
      urban: { male: 5, female: 4 },
      rural: { male: 4, female: 3 },
      propertyTypes: {
        residential: { male: 5, female: 4 },
        commercial: { stamp: 5, reg: 1 },
        agricultural: { stamp: 3, reg: 1 }
      },
      minimumValue: null,
      notes: "Women get 1% discount in MH. Metro cess 1% extra in Mumbai and metro areas. Registration capped at ₹30,000 for some categories.",
      seo: {
        title: "Maharashtra Stamp Duty Calculator 2025 — Mumbai Property Registration | Calculatorcity",
        description: "Calculate stamp duty for Maharashtra and Mumbai property. Women get 1% discount. Stamp duty 4-5% + 1% registration. Free and accurate calculator.",
        h1: "Maharashtra Stamp Duty Calculator",
        subtitle: "MH property stamp duty — women get 1% discount. Mumbai, Pune, Nagpur all districts."
      },
      content: {
        howItWorks: `<p>Maharashtra stamp duty is <strong>5% for men and 4% for women</strong> buyers — one of the few states offering a meaningful women discount. For joint registrations, the effective rate is 4.5%. Registration charges are 1% of the property value.</p>
      <p>In Mumbai metropolitan region, an additional 1% Metro Cess is applicable, effectively making it 6% (men) or 5% (women). This metro cess applies within MMRDA limits.</p>
      <p>The Maharashtra IGR (Inspector General of Registration) manages property registrations through the iSarita portal.</p>`,
        stateSpecific: `<h2>Mumbai property — Metro Cess</h2>
      <p>Mumbai and Mumbai Metropolitan Region (MMR) attract an additional 1% Metro Cess on stamp duty. This applies to areas within MMRDA limits including Thane, Navi Mumbai, Kalyan-Dombivali, and surrounding areas. So for a Mumbai man: 5% + 1% metro cess = 6% effective stamp duty.</p>
      <h2>Women discount in Maharashtra</h2>
      <p>Women buyers in Maharashtra pay 4% stamp duty vs 5% for men — saving 1% of the property value. For a ₹1 crore property, women save ₹1 lakh. For joint registration where at least one co-owner is female, the rate is 4.5%.</p>
      <h2>iSarita portal — Maharashtra registration</h2>
      <p>The iSarita portal (igrmaharashtra.gov.in) handles all property registration in Maharashtra. You can search ready reckoner rates, book appointments, pay stamp duty, and track document status.</p>`,
        faq: [
          { q: "What is stamp duty in Maharashtra 2025?", a: "Maharashtra stamp duty is 5% for men and 4% for women buyers. Registration charges are 1%. In Mumbai/MMR area, an additional 1% Metro Cess applies. Total for Mumbai man = 7% (5%+1%+1%), Mumbai woman = 6% (4%+1%+1%). For other MH districts, man = 6%, woman = 5%." },
          { q: "What is the women discount on stamp duty in Maharashtra?", a: "Women buyers in Maharashtra pay 4% stamp duty instead of 5% — a saving of 1% of property value. For a ₹75 lakh property, women save ₹75,000 on stamp duty. For joint purchase with a woman as co-owner, the rate is 4.5%. The property must be in the woman's name to avail this benefit." },
          { q: "What is Metro Cess in Maharashtra?", a: "Metro Cess is an additional 1% stamp duty applicable in the Mumbai Metropolitan Region (MMRDA area) including Mumbai, Thane, Navi Mumbai, Kalyan, Dombivali, Bhiwandi, and surrounding areas. It was introduced for funding metro rail infrastructure. Outside MMR limits, metro cess does not apply." },
          { q: "What is Ready Reckoner rate in Maharashtra?", a: "Ready Reckoner rate is the government-declared minimum value for property in Maharashtra for stamp duty calculation. Stamp duty is calculated on Ready Reckoner rate or actual transaction value, whichever is higher. Annual Ready Reckoner rates are published by Maharashtra IGR and vary by location, floor, age of building." },
          { q: "How to pay stamp duty in Maharashtra?", a: "Stamp duty can be paid online through the iSarita portal (igrmaharashtra.gov.in) using GRAS (Government Receipt Accounting System). You can pay via net banking, credit card, UPI, or at authorised banks. E-stamping is widely available. The challan is submitted at time of registration." },
          { q: "What documents are required for property registration in Maharashtra?", a: "Required: original sale deed, index II of previous registration, property card/7/12 extract, NOC from society (if flat), identity proof, address proof, PAN card, Aadhaar of buyer and seller, two witnesses, and stamp duty payment receipt. Bring originals and self-attested photocopies." }
        ]
      }
    },

    delhi: {
      name: "Delhi",
      slug: "delhi",
      color: "#2563eb",
      flag: "🏛️",
      stampDuty: { male: 6, female: 4, joint: 5 },
      registrationCharges: { male: 1, female: 1, joint: 1 },
      transferDuty: 0,
      hasWomenDiscount: true,
      womenDiscount: 2,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { male: 6, female: 4 },
        commercial: { stamp: 6, reg: 1 },
        agricultural: { stamp: 6, reg: 1 }
      },
      minimumValue: null,
      notes: "Delhi gives 2% discount for women — biggest women discount in India. Registration capped at specific amounts in some cases.",
      seo: {
        title: "Delhi Stamp Duty Calculator 2025 — Property Registration Delhi | Calculatorcity",
        description: "Calculate stamp duty for Delhi property. Women pay only 4% vs 6% for men. Delhi registration charges 1%. Free and accurate stamp duty calculator.",
        h1: "Delhi Stamp Duty Calculator",
        subtitle: "Delhi stamp duty — women pay 4%, men pay 6%. Biggest women discount in India."
      },
      content: {
        howItWorks: `<p>Delhi has the <strong>biggest women discount on stamp duty in India</strong> — women pay just 4% stamp duty while men pay 6%. Registration charges are 1% for all. For a joint purchase, the rate depends on whether a woman is the primary owner.</p>
      <p>Delhi's stamp duty is among the lower rates for men (6%) and the lowest for women (4%) among major Indian cities. The Delhi government periodically offers additional stamp duty rebates to boost the real estate market.</p>`,
        stateSpecific: `<h2>Delhi women stamp duty — biggest saving in India</h2>
      <p>Delhi women buyers save 2% on stamp duty — the highest women discount in any Indian state. On a ₹1 crore property, women save ₹2 lakhs in stamp duty compared to men. This is double the savings compared to Maharashtra (1%) and Haryana (2% but lower base rates).</p>
      <h2>Circle rates in Delhi</h2>
      <p>Delhi has 8 categories of circle rates (A to H) depending on the colony/area. Category A (premium areas like Shanti Niketan, Vasant Vihar) has the highest circle rates. Category H (unapproved colonies) has the lowest. Stamp duty is calculated on circle rate or transaction value, whichever is higher.</p>`,
        faq: [
          { q: "What is stamp duty in Delhi 2025?", a: "Delhi stamp duty is 6% for men and 4% for women. Registration charges are 1% for all. Total for men = 7%, for women = 5% of property value. Delhi's 4% for women is the lowest stamp duty for women among all major Indian cities." },
          { q: "What is the women discount on stamp duty in Delhi?", a: "Women buyers in Delhi pay only 4% stamp duty vs 6% for men — a saving of 2%. For a ₹80 lakh property, women save ₹1,60,000 on stamp duty. This is the largest women discount in India. The property deed must be in the woman's name to avail this rate." },
          { q: "What are Delhi circle rate categories?", a: "Delhi has 8 circle rate categories: Category A (premium colonies — highest rate), B, C, D, E, F, G, H (unapproved colonies — lowest rate). Check Delhi government website or Sub-Registrar office for current category-wise circle rates for your specific colony or area." },
          { q: "How to pay stamp duty in Delhi?", a: "Stamp duty in Delhi can be paid through e-stamping at Stock Holding Corporation of India (SHCIL) branches, or through the Delhi government DORIS portal. You can also pay via bank drafts. After paying, present the e-stamp paper at the Sub-Registrar Office for registration." },
          { q: "Is there stamp duty exemption in Delhi?", a: "Delhi does not have a blanket stamp duty exemption but offers a 2% concession for women buyers. Some government housing schemes (DDA flats) may have different stamp duty arrangements. For SC/ST categories, there may be concessional rates — check with the Sub-Registrar Office." },
          { q: "What is DORIS Delhi?", a: "DORIS (Delhi Online Registration Information System) is the official portal for property registration in Delhi. Visit doris.delhigovt.nic.in for circle rate search, appointment booking, encumbrance certificate, and property registration services." }
        ]
      }
    },

    gujarat: {
      name: "Gujarat",
      slug: "gujarat",
      color: "#d97706",
      flag: "🦁",
      stampDuty: { male: 4.9, female: 4.9, joint: 4.9 },
      registrationCharges: { male: 1, female: 1, joint: 1 },
      transferDuty: 0,
      hasWomenDiscount: false,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { stamp: 4.9, reg: 1 },
        commercial: { stamp: 4.9, reg: 1 },
        agricultural: { stamp: 3.5, reg: 1 }
      },
      minimumValue: null,
      notes: "Gujarat has a unique 4.9% stamp duty (not 5%). Total: 5.9% of property value.",
      seo: {
        title: "Gujarat Stamp Duty Calculator 2025 — Property Registration GJ | Calculatorcity",
        description: "Calculate stamp duty for Gujarat property. Gujarat stamp duty 4.9% + 1% registration = 5.9% total. Ahmedabad, Surat, Vadodara property registration charges.",
        h1: "Gujarat Stamp Duty Calculator",
        subtitle: "Gujarat property stamp duty — 4.9% + 1% registration. Affordable rates in India."
      },
      content: {
        howItWorks: `<p>Gujarat charges stamp duty at <strong>4.9% of property value</strong> — a unique rate slightly below 5%. Registration charges are 1%. The total transaction cost is 5.9% of property value, making Gujarat one of the more affordable states for property registration.</p>
      <p>The Gujarat Registration Department manages all property registrations through the Garvi portal (garvi.gujarat.gov.in).</p>`,
        stateSpecific: `<h2>Garvi portal — Gujarat property registration</h2>
      <p>The Garvi (Gujarat Registration of Valued Property) portal provides online registration services, jantri (circle rate) lookup, encumbrance certificate search, and document status tracking for all Gujarat districts.</p>
      <h2>Jantri rates in Gujarat</h2>
      <p>Jantri is Gujarat's term for circle rate/guideline value. Jantri rates are set by the Revenue Department and vary by locality, zone, and property type. Stamp duty in Gujarat is calculated on jantri value or transaction value, whichever is higher.</p>`,
        faq: [
          { q: "What is stamp duty in Gujarat 2025?", a: "Gujarat stamp duty is 4.9% of property value. Registration charges are 1%. Total = 5.9%. For agricultural land, stamp duty is 3.5% + 1% registration = 4.5%. Gujarat's rates are among the more affordable in India." },
          { q: "What is jantri rate in Gujarat?", a: "Jantri is the government-declared minimum property value in Gujarat, used for stamp duty calculation. Stamp duty is calculated on jantri rate or actual transaction value, whichever is higher. Check current jantri rates on the Garvi portal by selecting district and village/ward." },
          { q: "Does Gujarat offer women discount on stamp duty?", a: "Gujarat does not offer a specific women discount on stamp duty. Both male and female buyers pay the same 4.9% stamp duty and 1% registration charges." },
          { q: "What is the Garvi portal for Gujarat?", a: "Garvi (garvi.gujarat.gov.in) is the official Gujarat property registration portal. Use it for: jantri rate lookup, EC search, appointment booking, stamp duty payment, document status tracking, and certified copy requests." },
          { q: "How to calculate stamp duty for Ahmedabad property?", a: "For an Ahmedabad flat of ₹60 lakhs: Stamp duty = 4.9% × ₹60L = ₹2,94,000. Registration = 1% × ₹60L = ₹60,000. Total = ₹3,54,000. Calculation is on jantri value or ₹60L, whichever is higher." },
          { q: "What documents are required for Gujarat property registration?", a: "Required: sale deed, title documents, Khata/7-12 extract, encumbrance certificate, identity and address proof of buyer and seller, PAN and Aadhaar, two witnesses, and stamp duty payment receipt." }
        ]
      }
    },

    "uttar-pradesh": {
      name: "Uttar Pradesh",
      slug: "uttar-pradesh",
      color: "#16a34a",
      flag: "🌾",
      stampDuty: { male: 7, female: 6, joint: 6.5 },
      registrationCharges: { male: 1, female: 1, joint: 1 },
      registrationCap: 100000,
      transferDuty: 0,
      hasWomenDiscount: true,
      womenDiscount: 1,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { male: 7, female: 6 },
        commercial: { stamp: 7, reg: 1 },
        agricultural: { stamp: 5, reg: 1 }
      },
      minimumValue: null,
      notes: "UP gives 1% discount to women. Registration capped at ₹1 lakh maximum in UP.",
      seo: {
        title: "UP Stamp Duty Calculator 2025 — Uttar Pradesh Property Registration | Calculatorcity",
        description: "Calculate stamp duty for Uttar Pradesh property. UP stamp duty 7% (men) 6% (women) + 1% registration. Lucknow, Noida, Agra, Varanasi registration charges.",
        h1: "Uttar Pradesh Stamp Duty Calculator",
        subtitle: "UP property stamp duty — 7% for men, 6% for women. All UP districts."
      },
      content: {
        howItWorks: `<p>Uttar Pradesh charges stamp duty at <strong>7% for men and 6% for women</strong>. Registration charges are 1% for all buyers, capped at ₹1 lakh maximum. UP has the highest stamp duty rate for men among major Indian states.</p>
      <p>The UP Registration Department (IGRSUP) manages property registrations through the IGRS UP portal.</p>`,
        stateSpecific: `<h2>IGRS UP — registration portal</h2>
      <p>The IGRS UP portal (igrsup.gov.in) provides: appointment booking, circle rate search, EC search, stamp duty payment, and document registration services for all UP districts.</p>
      <h2>Noida property registration</h2>
      <p>Noida (Gautam Buddha Nagar) properties have higher circle rates due to proximity to Delhi. Noida and Greater Noida fall under UP jurisdiction and follow UP stamp duty rates.</p>`,
        faq: [
          { q: "What is stamp duty in Uttar Pradesh 2025?", a: "UP stamp duty is 7% for men and 6% for women. Registration charges are 1% (capped at ₹1 lakh). Total for men = 8%, for women = 7%. UP has the highest stamp duty for male buyers among major Indian states." },
          { q: "What is the women discount on stamp duty in UP?", a: "Women in UP pay 6% stamp duty vs 7% for men — a saving of 1%. Registration charges are the same 1% for all. For joint purchase, the rate is 6.5% if woman is co-owner." },
          { q: "What is the circle rate in Noida UP?", a: "Circle rates in Noida (Gautam Buddha Nagar) vary by sector and property type. Noida has high circle rates in premium sectors near expressways. Check current circle rates on the IGRS UP portal by selecting Gautam Buddha Nagar district." },
          { q: "Is UP stamp duty higher than other states?", a: "Yes, UP has one of the highest stamp duty rates in India at 7% (men) — same as Tamil Nadu. However, UP registration charges are 1% compared to TN's 4%, making UP total (8%) lower than TN total (11%)." },
          { q: "How to book appointment for UP property registration?", a: "Visit igrsup.gov.in, create an account, fill property details, choose Sub-Registrar Office and appointment date. Pay stamp duty online through the portal. Bring all documents on the appointment date." },
          { q: "What is the maximum registration fee in UP?", a: "Registration charges in UP are 1% of property value but are capped at a maximum of ₹1 lakh. So for a ₹2 crore property, registration fee = 1% × ₹2Cr = ₹2 lakhs, but capped at ₹1 lakh. This cap benefits high-value property buyers." }
        ]
      }
    },

    rajasthan: {
      name: "Rajasthan",
      slug: "rajasthan",
      color: "#f59e0b",
      flag: "🐪",
      stampDuty: { male: 6, female: 5, joint: 5.5 },
      registrationCharges: { male: 1, female: 1, joint: 1 },
      transferDuty: 0,
      hasWomenDiscount: true,
      womenDiscount: 1,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { male: 6, female: 5 },
        commercial: { stamp: 6, reg: 1 },
        agricultural: { stamp: 5, reg: 1 }
      },
      minimumValue: null,
      notes: "Rajasthan gives 1% discount for women. Total: men 7%, women 6%.",
      seo: {
        title: "Rajasthan Stamp Duty Calculator 2025 — Property Registration RJ | Calculatorcity",
        description: "Calculate stamp duty for Rajasthan property. Rajasthan stamp duty 6% (men) 5% (women) + 1% registration. Jaipur, Jodhpur, Udaipur registration charges.",
        h1: "Rajasthan Stamp Duty Calculator",
        subtitle: "Rajasthan stamp duty — 6% for men, 5% for women. Jaipur and all RJ districts."
      },
      content: {
        howItWorks: `<p>Rajasthan charges stamp duty at <strong>6% for men and 5% for women</strong>. Registration charges are 1% for all. The Rajasthan Registration Department manages all property registrations.</p>`,
        stateSpecific: `<h2>Jaipur property registration</h2>
      <p>Jaipur is Rajasthan's largest property market. Pink City heritage areas, Malviya Nagar, Vaishali Nagar, and newer areas near Delhi-Mumbai Industrial Corridor have high property values and circle rates.</p>`,
        faq: [
          { q: "What is stamp duty in Rajasthan 2025?", a: "Rajasthan stamp duty is 6% for men and 5% for women. Registration charges are 1%. Total: men = 7%, women = 6%." },
          { q: "Women discount in Rajasthan stamp duty?", a: "1% discount for women buyers. Women pay 5% vs men's 6%." },
          { q: "How to pay stamp duty in Rajasthan?", a: "Pay through e-GRAS portal or RAJSSP. Visit your Sub-Registrar Office for registration." },
          { q: "What is DLC rate in Rajasthan?", a: "DLC (District Level Committee) rate is the circle rate in Rajasthan. Stamp duty is calculated on DLC rate or transaction value, whichever is higher." },
          { q: "What is the registration process in Jaipur?", a: "Book appointment at Sub-Registrar office, pay stamp duty via e-GRAS, bring all documents on appointment date." },
          { q: "Is stamp duty same across all Rajasthan districts?", a: "Stamp duty percentage is same across Rajasthan. But DLC rates (circle rates) differ by district and locality, affecting the base for calculation." }
        ]
      }
    },

    "west-bengal": {
      name: "West Bengal",
      slug: "west-bengal",
      color: "#16a34a",
      flag: "🐅",
      stampDuty: { male: 6, female: 6, joint: 6 },
      registrationCharges: { male: 1, female: 1, joint: 1 },
      transferDuty: 0,
      hasWomenDiscount: false,
      hasUrbanRural: true,
      urban: { stamp: 6, reg: 1 },
      rural: { stamp: 5, reg: 1 },
      propertyTypes: {
        residential: { stamp: 6, reg: 1 },
        commercial: { stamp: 6, reg: 1 },
        agricultural: { stamp: 2, reg: 1 }
      },
      minimumValue: null,
      notes: "WB urban: 6%, rural: 5%. Kolkata is urban. Municipal areas vs panchayat areas different.",
      seo: {
        title: "West Bengal Stamp Duty Calculator 2025 — Property Registration WB | Calculatorcity",
        description: "Calculate stamp duty for West Bengal property. WB stamp duty 6% (urban) 5% (rural) + 1% registration. Kolkata, Howrah, Siliguri registration charges.",
        h1: "West Bengal Stamp Duty Calculator",
        subtitle: "WB stamp duty — 6% urban, 5% rural. Kolkata and all West Bengal districts."
      },
      content: {
        howItWorks: `<p>West Bengal charges <strong>6% stamp duty for urban areas and 5% for rural/panchayat areas</strong>. Registration charges are 1% across all categories. Kolkata and municipal corporation areas are urban; gram panchayat areas are rural.</p>`,
        stateSpecific: `<h2>Kolkata property registration</h2>
      <p>Kolkata falls under urban category (6% stamp duty). The WBREGINET portal manages all WB property registrations. Kolkata suburban areas in North 24 Parganas, South 24 Parganas have growing property markets.</p>`,
        faq: [
          { q: "What is stamp duty in West Bengal 2025?", a: "6% for urban areas (municipal corporations), 5% for rural areas (panchayat areas). Registration charges 1% for all. Kolkata = 6% + 1% = 7%." },
          { q: "Is Kolkata urban or rural for stamp duty?", a: "Kolkata and all municipal corporation areas are urban — 6% stamp duty applies. Areas under gram panchayat are rural — 5% stamp duty." },
          { q: "What is WBREGINET?", a: "WBREGINET is the WB property registration portal. Visit wbreginet.gov.in for circle rate search, EC search, appointment booking." },
          { q: "Women discount in WB stamp duty?", a: "West Bengal does not offer a specific women discount on stamp duty." },
          { q: "What is the circle rate in Kolkata?", a: "Circle rates in Kolkata vary significantly by zone — South Kolkata premium areas vs North Kolkata. Check WBREGINET for current zone-wise rates." },
          { q: "How to register property in Kolkata?", a: "Book appointment on WBREGINET, pay stamp duty via treasury challan, bring documents to Sub-Registrar office on appointment date." }
        ]
      }
    },

    "madhya-pradesh": {
      name: "Madhya Pradesh",
      slug: "madhya-pradesh",
      color: "#7c3aed",
      flag: "🐆",
      stampDuty: { male: 7.5, female: 7.5, joint: 7.5 },
      registrationCharges: { male: 1, female: 1, joint: 1 },
      transferDuty: 0,
      hasWomenDiscount: false,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { stamp: 7.5, reg: 1 },
        commercial: { stamp: 7.5, reg: 1 },
        agricultural: { stamp: 7.5, reg: 1 }
      },
      minimumValue: null,
      notes: "MP has second highest stamp duty at 7.5%. No women discount. Total: 8.5%.",
      seo: {
        title: "MP Stamp Duty Calculator 2025 — Madhya Pradesh Property Registration | Calculatorcity",
        description: "Calculate stamp duty for Madhya Pradesh property. MP stamp duty 7.5% + 1% registration = 8.5% total. Bhopal, Indore, Jabalpur registration charges.",
        h1: "Madhya Pradesh Stamp Duty Calculator",
        subtitle: "MP property stamp duty — 7.5% one of highest in India. Bhopal, Indore all districts."
      },
      content: {
        howItWorks: `<p>Madhya Pradesh has one of the highest stamp duty rates in India at <strong>7.5%</strong>. Registration charges are 1%. Total transaction cost is 8.5% of property value — higher than most Indian states.</p>`,
        stateSpecific: `<h2>SAMPDA portal — MP registration</h2>
      <p>The SAMPDA portal manages property registrations in Madhya Pradesh. Bhopal and Indore are the major property markets in MP with high circle rates in premium areas.</p>`,
        faq: [
          { q: "What is stamp duty in MP 2025?", a: "7.5% stamp duty + 1% registration = 8.5% total. MP has one of the highest stamp duty rates in India." },
          { q: "Does MP offer women discount?", a: "No women discount in Madhya Pradesh. All buyers pay 7.5% stamp duty." },
          { q: "What is the SAMPDA portal?", a: "SAMPDA (sampada.mp.gov.in) is the MP property registration portal for appointments, circle rates, EC search." },
          { q: "Why is MP stamp duty so high?", a: "MP has historically high stamp duty at 7.5%, among the highest in India. Only Himachal Pradesh and some other states have comparable rates." },
          { q: "How to pay stamp duty in MP?", a: "Pay via e-GRAS or SAMPDA portal. Submit at Sub-Registrar office on appointment date." },
          { q: "What is circle rate in Bhopal?", a: "Bhopal circle rates vary by zone and locality. Check SAMPDA portal for current rates in your specific area." }
        ]
      }
    },

    haryana: {
      name: "Haryana",
      slug: "haryana",
      color: "#16a34a",
      flag: "🌾",
      stampDuty: { male: 7, female: 5, joint: 6 },
      registrationCharges: { male: 1, female: 1, joint: 1 },
      transferDuty: 0,
      hasWomenDiscount: true,
      womenDiscount: 2,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { male: 7, female: 5 },
        commercial: { stamp: 7, reg: 1 },
        agricultural: { stamp: 5, reg: 1 }
      },
      minimumValue: null,
      notes: "Haryana gives 2% discount to women — same as Delhi discount amount. Total: men 8%, women 6%.",
      seo: {
        title: "Haryana Stamp Duty Calculator 2025 — Property Registration HR | Calculatorcity",
        description: "Calculate stamp duty for Haryana property. Women pay only 5% vs 7% for men — 2% discount. Gurugram, Faridabad, Chandigarh registration charges.",
        h1: "Haryana Stamp Duty Calculator",
        subtitle: "Haryana stamp duty — women pay 5%, men pay 7%. 2% women discount in Gurugram and all HR."
      },
      content: {
        howItWorks: `<p>Haryana gives a <strong>2% stamp duty discount for women</strong> — women pay 5% while men pay 7%. Registration charges are 1%. Total: men pay 8%, women pay 6%.</p>
      <p>Gurugram (Gurgaon) is Haryana's most expensive property market due to IT/corporate presence. Faridabad, Panchkula, and Sonipat are other major markets.</p>`,
        stateSpecific: `<h2>Gurugram property registration</h2>
      <p>Gurugram falls under Haryana and follows HR stamp duty rates. Given high property values in Gurugram (DLF sectors, Golf Course Road, Cyber City area), the stamp duty amount can be very significant. Women save substantial amounts on Gurugram property registration.</p>`,
        faq: [
          { q: "What is stamp duty in Haryana 2025?", a: "7% for men, 5% for women. Registration 1% for all. Total: men = 8%, women = 6%. Women save 2% — same discount as Delhi." },
          { q: "Women discount in Haryana stamp duty?", a: "2% discount — women pay 5% vs men's 7%. For a ₹1 crore Gurugram property, women save ₹2 lakhs in stamp duty." },
          { q: "What is stamp duty in Gurugram?", a: "Gurugram is in Haryana — same HR rates apply. Men pay 7%, women pay 5% stamp duty + 1% registration for all." },
          { q: "How to pay stamp duty in Haryana?", a: "Pay via HARSAC or e-GRAS. Book appointment at Sub-Registrar office through Jamabandi portal." },
          { q: "What is circle rate in Gurugram?", a: "Gurugram has some of India's highest circle rates for residential apartments. Check Haryana government website or Jamabandi portal for current collector rate by sector." },
          { q: "What documents needed for Haryana property registration?", a: "Sale deed, property documents, identity proof, PAN, Aadhaar, two witnesses, stamp duty payment receipt. Agricultural land needs additional documents." }
        ]
      }
    },

    punjab: {
      name: "Punjab",
      slug: "punjab",
      color: "#16a34a",
      flag: "🌾",
      stampDuty: { male: 7, female: 5, joint: 6 },
      registrationCharges: { male: 1, female: 1, joint: 1 },
      transferDuty: 0,
      hasWomenDiscount: true,
      womenDiscount: 2,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { male: 7, female: 5 },
        commercial: { stamp: 7, reg: 1 },
        agricultural: { stamp: 5, reg: 1 }
      },
      minimumValue: null,
      notes: "Punjab same as Haryana — 2% women discount. Men 8% total, women 6% total.",
      seo: {
        title: "Punjab Stamp Duty Calculator 2025 — Property Registration PB | Calculatorcity",
        description: "Calculate stamp duty for Punjab property. Women pay 5% vs 7% for men. Chandigarh, Amritsar, Ludhiana, Jalandhar registration charges. Free and accurate.",
        h1: "Punjab Stamp Duty Calculator",
        subtitle: "Punjab property stamp duty — 7% for men, 5% for women. All Punjab districts."
      },
      content: {
        howItWorks: `<p>Punjab charges stamp duty at <strong>7% for men and 5% for women</strong> — a 2% discount for women buyers. Registration charges are 1% for all. Total cost: men 8%, women 6%.</p>`,
        stateSpecific: `<h2>Major Punjab property markets</h2>
      <p>Chandigarh (UT, separate rates), Mohali (Punjab — follows Punjab rates), Ludhiana (industrial hub), Amritsar (tourism/heritage), and Jalandhar are major property markets in Punjab.</p>`,
        faq: [
          { q: "What is stamp duty in Punjab 2025?", a: "7% for men, 5% for women + 1% registration. Total: men 8%, women 6%." },
          { q: "Is Chandigarh stamp duty same as Punjab?", a: "No. Chandigarh is a Union Territory with its own rates, different from Punjab. Mohali (near Chandigarh) follows Punjab rates." },
          { q: "Women discount in Punjab?", a: "Women pay 5% vs men's 7% — a 2% saving." },
          { q: "How to register property in Punjab?", a: "Visit PUNJAB LAND RECORDS portal. Book appointment, pay stamp duty, visit Sub-Registrar office." },
          { q: "What is collector rate in Punjab?", a: "Collector rate is Punjab's circle rate. Varies by city, locality, and property type. Check Punjab government website for current rates." },
          { q: "Is Mohali under Punjab or Chandigarh for stamp duty?", a: "Mohali (SAS Nagar) is in Punjab — follows Punjab stamp duty rates (7% men, 5% women). Chandigarh city follows UT rates." }
        ]
      }
    },

    kerala: {
      name: "Kerala",
      slug: "kerala",
      color: "#16a34a",
      flag: "🌴",
      stampDuty: { male: 8, female: 8, joint: 8 },
      registrationCharges: { male: 2, female: 2, joint: 2 },
      transferDuty: 0,
      hasWomenDiscount: false,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { stamp: 8, reg: 2 },
        commercial: { stamp: 8, reg: 2 },
        agricultural: { stamp: 5, reg: 2 }
      },
      minimumValue: null,
      notes: "Kerala has 8% stamp duty + 2% registration = 10% total. High rate.",
      seo: {
        title: "Kerala Stamp Duty Calculator 2025 — Property Registration KL | Calculatorcity",
        description: "Calculate stamp duty for Kerala property. Kerala stamp duty 8% + 2% registration = 10% total. Thiruvananthapuram, Kochi, Kozhikode registration.",
        h1: "Kerala Stamp Duty Calculator",
        subtitle: "Kerala property stamp duty — 8% + 2% registration. All Kerala districts."
      },
      content: {
        howItWorks: `<p>Kerala charges <strong>8% stamp duty</strong> and 2% registration charges, making the total transaction cost 10% — one of the higher rates in India. The Kerala Registration Department handles all property registrations through the PEARL portal.</p>`,
        stateSpecific: `<h2>Kerala PEARL portal</h2><p>PEARL (Property E-Registration and Land records) is Kerala's property registration portal at igr.kerala.gov.in for fair value search, appointments and EC search.</p>`,
        faq: [
          { q: "What is stamp duty in Kerala 2025?", a: "8% stamp duty + 2% registration = 10% total. One of the higher rates in India." },
          { q: "What is fair value in Kerala?", a: "Fair value is Kerala's circle rate. Stamp duty is calculated on fair value or transaction value, whichever is higher. Check on PEARL portal." },
          { q: "Women discount in Kerala?", a: "Kerala does not offer a specific women discount on stamp duty." },
          { q: "What is PEARL portal Kerala?", a: "PEARL portal (igr.kerala.gov.in) for Kerala property registration, fair value search, EC search." },
          { q: "Is stamp duty high in Kerala?", a: "Yes — 10% total (8%+2%) is among the higher rates in India, similar to Tamil Nadu (11%) but higher than AP (8%) and Karnataka (6%)." },
          { q: "How to pay stamp duty in Kerala?", a: "Pay via e-stamping at authorised banks or through Kerala Treasury. Book appointment at Sub-Registrar office." }
        ]
      }
    },

    bihar: {
      name: "Bihar",
      slug: "bihar",
      color: "#16a34a",
      flag: "🦌",
      stampDuty: { male: 6.3, female: 5.7, joint: 6 },
      registrationCharges: { male: 2, female: 2, joint: 2 },
      transferDuty: 0,
      hasWomenDiscount: true,
      womenDiscount: 0.6,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { male: 6.3, female: 5.7 },
        commercial: { stamp: 6.3, reg: 2 },
        agricultural: { stamp: 5, reg: 2 }
      },
      minimumValue: null,
      notes: "Bihar: men 6.3%, women 5.7%. Registration 2%. Unique fractional discount.",
      seo: {
        title: "Bihar Stamp Duty Calculator 2025 — Property Registration BR | Calculatorcity",
        description: "Calculate stamp duty for Bihar property. Bihar stamp duty 6.3% (men) 5.7% (women) + 2% registration. Patna registration charges.",
        h1: "Bihar Stamp Duty Calculator",
        subtitle: "Bihar property stamp duty — 6.3% for men, 5.7% for women. All Bihar districts."
      },
      content: {
        howItWorks: `<p>Bihar has a unique fractional stamp duty — <strong>6.3% for men and 5.7% for women</strong>. Registration charges are 2%. Total: men 8.3%, women 7.7%.</p>`,
        stateSpecific: `<p>Bihar's property market is centred around Patna. The BIRLEP portal manages property registrations.</p>`,
        faq: [
          { q: "Bihar stamp duty 2025?", a: "6.3% men, 5.7% women + 2% registration. Total: men 8.3%, women 7.7%." },
          { q: "Women discount in Bihar?", a: "0.6% discount — women pay 5.7% vs men's 6.3%." },
          { q: "How to register property in Bihar?", a: "Visit BIRLEP portal (bhumijankari.bihar.gov.in) for appointment booking." },
          { q: "Circle rate Patna?", a: "Patna circle rates vary significantly by locality. Check Bihar government website." },
          { q: "Registration fee in Bihar?", a: "2% registration charges. Calculated on circle rate or transaction value." },
          { q: "What is BIRLEP?", a: "BIRLEP is Bihar's land record and property registration portal." }
        ]
      }
    },

    odisha: {
      name: "Odisha",
      slug: "odisha",
      color: "#f97316",
      flag: "🐅",
      stampDuty: { male: 5, female: 4, joint: 4.5 },
      registrationCharges: { male: 2, female: 2, joint: 2 },
      transferDuty: 0,
      hasWomenDiscount: true,
      womenDiscount: 1,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { male: 5, female: 4 },
        commercial: { stamp: 5, reg: 2 },
        agricultural: { stamp: 3, reg: 2 }
      },
      minimumValue: null,
      notes: "Odisha: 1% women discount. Total: men 7%, women 6%.",
      seo: {
        title: "Odisha Stamp Duty Calculator 2025 — Property Registration OD | Calculatorcity",
        description: "Calculate stamp duty for Odisha property. Odisha stamp duty 5% (men) 4% (women) + 2% registration. Bhubaneswar, Cuttack registration charges.",
        h1: "Odisha Stamp Duty Calculator",
        subtitle: "Odisha property stamp duty — 5% for men, 4% for women. Bhubaneswar all OD districts."
      },
      content: {
        howItWorks: `<p>Odisha charges <strong>5% stamp duty for men and 4% for women</strong>. Registration charges are 2%. Total: men 7%, women 6%.</p>`,
        stateSpecific: `<p>Bhubaneswar is Odisha's largest property market. The IGROD portal manages registrations.</p>`,
        faq: [
          { q: "Odisha stamp duty 2025?", a: "5% men, 4% women + 2% registration. Total: men 7%, women 6%." },
          { q: "Women discount in Odisha?", a: "1% discount — women pay 4% vs men's 5%." },
          { q: "Registration in Bhubaneswar?", a: "Visit IGROD portal (igrodisha.gov.in) for registration." },
          { q: "Circle rate Bhubaneswar?", a: "Bhubaneswar has variable circle rates by zone. Check IGROD portal." },
          { q: "What is IGROD?", a: "Inspector General of Registration Odisha portal for property registration." },
          { q: "Documents for Odisha registration?", a: "Sale deed, previous documents, EC, identity proof, PAN, Aadhaar." }
        ]
      }
    },

    "himachal-pradesh": {
      name: "Himachal Pradesh",
      slug: "himachal-pradesh",
      color: "#2563eb",
      flag: "🏔️",
      stampDuty: { male: 6, female: 4, joint: 5 },
      registrationCharges: { male: 2, female: 2, joint: 2 },
      transferDuty: 0,
      hasWomenDiscount: true,
      womenDiscount: 2,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { male: 6, female: 4 },
        commercial: { stamp: 6, reg: 2 },
        agricultural: { stamp: 6, reg: 2 }
      },
      minimumValue: null,
      notes: "HP: 2% women discount. Strict rules on non-HP residents buying property in HP.",
      seo: {
        title: "HP Stamp Duty Calculator 2025 — Himachal Pradesh Property Registration | Calculatorcity",
        description: "Calculate stamp duty for Himachal Pradesh property. HP stamp duty 6% (men) 4% (women) + 2% registration. Shimla, Manali, Dharamshala.",
        h1: "Himachal Pradesh Stamp Duty Calculator",
        subtitle: "HP stamp duty — 6% for men, 4% for women. Shimla, Manali all HP districts."
      },
      content: {
        howItWorks: `<p>Himachal Pradesh charges <strong>6% stamp duty for men and 4% for women</strong>. Registration charges are 2%. Non-HP residents face restrictions on buying agricultural land and may need special permissions for some property types.</p>`,
        stateSpecific: `<p>HP has strict land laws — non-residents cannot buy agricultural land. Tourists and outsiders can buy residential property in designated areas. Check with Sub-Registrar for current rules.</p>`,
        faq: [
          { q: "HP stamp duty 2025?", a: "6% men, 4% women + 2% registration. Total: men 8%, women 6%." },
          { q: "Can outsiders buy property in HP?", a: "Non-residents can buy residential property but agricultural land is restricted. Check current HP Land Reforms Act provisions." },
          { q: "Women discount HP?", a: "2% discount — women pay 4% vs men's 6%." },
          { q: "How to register property in Shimla?", a: "Visit HP Registration department. Appointment via tehsil office." },
          { q: "Circle rate Shimla?", a: "Shimla circle rates vary significantly by locality. Check HP Revenue Department." },
          { q: "What documents for HP registration?", a: "Sale deed, previous title documents, Fard (land record extract), identity proof, NOC if applicable." }
        ]
      }
    },

    goa: {
      name: "Goa",
      slug: "goa",
      color: "#16a34a",
      flag: "🏖️",
      stampDuty: { male: 3.5, female: 3.5, joint: 3.5 },
      registrationCharges: { male: 3, female: 3, joint: 3 },
      transferDuty: 0,
      hasWomenDiscount: false,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { stamp: 3.5, reg: 3 },
        commercial: { stamp: 3.5, reg: 3 },
        agricultural: { stamp: 3.5, reg: 3 }
      },
      minimumValue: null,
      notes: "Goa: low stamp duty (3.5%) but high registration (3%). Total: 6.5%. Unique ASP (Annual Statement of Property) format.",
      seo: {
        title: "Goa Stamp Duty Calculator 2025 — Property Registration Goa | Calculatorcity",
        description: "Calculate stamp duty for Goa property. Goa stamp duty 3.5% + 3% registration = 6.5% total. Panaji, Margao, Vasco, North Goa South Goa registration charges.",
        h1: "Goa Stamp Duty Calculator",
        subtitle: "Goa property stamp duty — 3.5% stamp duty + 3% registration. Panaji, North and South Goa."
      },
      content: {
        howItWorks: `<p>Goa has a unique property registration structure — <strong>stamp duty is just 3.5%</strong> but registration charges are a high 3%, making the total 6.5%. Goa uses the Portuguese-era property law tradition for some aspects of land records.</p>`,
        stateSpecific: `<p>Goa has Portuguese Inscription property system for old properties alongside regular title-based properties. The DILR (Directorate of Settlement and Land Records) manages Goa's land records alongside the Registration Department.</p>`,
        faq: [
          { q: "Goa stamp duty 2025?", a: "3.5% stamp duty + 3% registration = 6.5% total." },
          { q: "Why is Goa registration charge high?", a: "3% registration in Goa is relatively high. But overall 6.5% total is moderate compared to states like Tamil Nadu (11%) and UP (8%)." },
          { q: "Women discount in Goa?", a: "No women discount in Goa." },
          { q: "Can non-Indians buy property in Goa?", a: "NRIs and foreign nationals face restrictions under FEMA. Consult a property lawyer for current rules." },
          { q: "What is the circle rate in Goa?", a: "Circle rates in Goa vary significantly. Coastal areas (Calangute, Baga, Candolim) have very high circle rates. Check Goa Registration Department." },
          { q: "How to register property in Goa?", a: "Visit Sub-Registrar office in the taluka where property is located. Goa uses taluka-based registration unlike district-based in most states." }
        ]
      }
    },

    jharkhand: {
      name: "Jharkhand",
      slug: "jharkhand",
      color: "#16a34a",
      flag: "🦌",
      stampDuty: { male: 4, female: 4, joint: 4 },
      registrationCharges: { male: 3, female: 3, joint: 3 },
      transferDuty: 0,
      hasWomenDiscount: false,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { stamp: 4, reg: 3 },
        commercial: { stamp: 4, reg: 3 },
        agricultural: { stamp: 4, reg: 3 }
      },
      minimumValue: null,
      notes: "Jharkhand: moderate stamp duty but high registration (3%). Total: 7%.",
      seo: {
        title: "Jharkhand Stamp Duty Calculator 2025 | Calculatorcity",
        description: "Calculate stamp duty for Jharkhand property. JH stamp duty 4% + 3% registration = 7% total. Ranchi, Jamshedpur, Dhanbad registration.",
        h1: "Jharkhand Stamp Duty Calculator",
        subtitle: "Jharkhand property stamp duty — 4% + 3% registration. Ranchi all JH districts."
      },
      content: {
        howItWorks: `<p>Jharkhand charges <strong>4% stamp duty</strong> and 3% registration charges, making the total 7% of property value.</p>`,
        stateSpecific: `<p>Ranchi is Jharkhand's largest property market. Jamshedpur (Tata Steel town) and Dhanbad (coal belt) are other major markets.</p>`,
        faq: [
          { q: "Jharkhand stamp duty?", a: "4% stamp duty + 3% registration = 7% total." },
          { q: "Women discount JH?", a: "No specific women discount in Jharkhand." },
          { q: "Registration in Ranchi?", a: "Visit Sub-Registrar office in Ranchi. JHARNET portal for online services." },
          { q: "Circle rate Ranchi?", a: "Ranchi circle rates set by Revenue Department. Check Jharkhand Bhumi portal." },
          { q: "What is JHARNET?", a: "Jharkhand property registration portal for EC search and appointments." },
          { q: "Documents for JH registration?", a: "Sale deed, property documents, identity proof, witnesses." }
        ]
      }
    },

    chhattisgarh: {
      name: "Chhattisgarh",
      slug: "chhattisgarh",
      color: "#16a34a",
      flag: "🌾",
      stampDuty: { male: 5, female: 4, joint: 4.5 },
      registrationCharges: { male: 4, female: 4, joint: 4 },
      transferDuty: 0,
      hasWomenDiscount: true,
      womenDiscount: 1,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { male: 5, female: 4 },
        commercial: { stamp: 5, reg: 4 },
        agricultural: { stamp: 5, reg: 4 }
      },
      minimumValue: null,
      notes: "CG: 1% women discount but very high registration (4%). Total: men 9%, women 8%.",
      seo: {
        title: "Chhattisgarh Stamp Duty Calculator 2025 | Calculatorcity",
        description: "Calculate stamp duty for Chhattisgarh property. CG stamp duty 5% + 4% registration = 9% total. Raipur Bilaspur registration charges.",
        h1: "Chhattisgarh Stamp Duty Calculator",
        subtitle: "CG property stamp duty — 5% (men) 4% (women) + 4% registration. Raipur all CG."
      },
      content: {
        howItWorks: `<p>Chhattisgarh charges <strong>5% for men and 4% for women</strong> stamp duty. Registration charges are 4% — among the highest in India. Total: men 9%, women 8%.</p>`,
        stateSpecific: `<p>Raipur is CG's major property market. High registration charges make CG property more expensive overall.</p>`,
        faq: [
          { q: "CG stamp duty?", a: "5% men, 4% women + 4% registration. Total: men 9%, women 8%." },
          { q: "Why is CG registration so high?", a: "4% registration in CG is one of the highest in India, making total cost high despite moderate stamp duty." },
          { q: "Women discount CG?", a: "1% discount — women pay 4% vs men's 5%." },
          { q: "Registration in Raipur?", a: "Visit Sub-Registrar office or CG registration portal." },
          { q: "Circle rate Raipur?", a: "Check CG Revenue Department for Raipur area circle rates." },
          { q: "Documents for CG registration?", a: "Sale deed, property documents, identity proof, witnesses." }
        ]
      }
    },

    assam: {
      name: "Assam",
      slug: "assam",
      color: "#16a34a",
      flag: "🦏",
      stampDuty: { male: 8.25, female: 8.25, joint: 8.25 },
      registrationCharges: { male: 1, female: 1, joint: 1 },
      transferDuty: 0,
      hasWomenDiscount: false,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { stamp: 8.25, reg: 1 },
        commercial: { stamp: 8.25, reg: 1 },
        agricultural: { stamp: 5, reg: 1 }
      },
      minimumValue: null,
      notes: "Assam has high stamp duty at 8.25% but low registration (1%). Total: 9.25%.",
      seo: {
        title: "Assam Stamp Duty Calculator 2025 | Calculatorcity",
        description: "Calculate stamp duty for Assam property. Assam stamp duty 8.25% + 1% registration. Guwahati, Dibrugarh registration charges.",
        h1: "Assam Stamp Duty Calculator",
        subtitle: "Assam property stamp duty — 8.25% + 1% registration. Guwahati all Assam."
      },
      content: {
        howItWorks: `<p>Assam has a relatively high stamp duty of <strong>8.25%</strong> but low registration charges of 1%. Total cost: 9.25% of property value.</p>`,
        stateSpecific: `<p>Guwahati is Assam's major property market and NE India's commercial hub. DORIS Assam portal handles registrations.</p>`,
        faq: [
          { q: "Assam stamp duty?", a: "8.25% stamp duty + 1% registration = 9.25% total." },
          { q: "Women discount Assam?", a: "No specific women discount in Assam." },
          { q: "Registration in Guwahati?", a: "Visit Sub-Registrar office. DORIS Assam portal for appointments." },
          { q: "Circle rate Guwahati?", a: "Guwahati circle rates vary by locality. Check Assam Revenue Department." },
          { q: "What is DORIS Assam?", a: "DORIS is Assam's online property registration portal." },
          { q: "Documents for Assam registration?", a: "Sale deed, jamabandi, identity proof, witnesses." }
        ]
      }
    },

    uttarakhand: {
      name: "Uttarakhand",
      slug: "uttarakhand",
      color: "#2563eb",
      flag: "🏔️",
      stampDuty: { male: 5, female: 3.75, joint: 4.375 },
      registrationCharges: { male: 2, female: 2, joint: 2 },
      transferDuty: 0,
      hasWomenDiscount: true,
      womenDiscount: 1.25,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { male: 5, female: 3.75 },
        commercial: { stamp: 5, reg: 2 },
        agricultural: { stamp: 5, reg: 2 }
      },
      minimumValue: null,
      notes: "UK: Women pay 25% less than men (3.75% vs 5%). Total: men 7%, women 5.75%.",
      seo: {
        title: "Uttarakhand Stamp Duty Calculator 2025 | Calculatorcity",
        description: "Calculate stamp duty for Uttarakhand property. UK stamp duty 5% (men) 3.75% (women). Dehradun, Haridwar, Nainital registration charges.",
        h1: "Uttarakhand Stamp Duty Calculator",
        subtitle: "UK property stamp duty — 5% for men, 3.75% for women. Dehradun all UK."
      },
      content: {
        howItWorks: `<p>Uttarakhand gives women a unique discount — women pay <strong>3.75% stamp duty vs 5% for men</strong> (25% less). Registration charges are 2% for all.</p>`,
        stateSpecific: `<p>Dehradun is UK's major property market. Haridwar, Rishikesh, Nainital, and Mussoorie are high-demand areas. Non-residents face some restrictions on buying agricultural land.</p>`,
        faq: [
          { q: "UK stamp duty?", a: "5% men, 3.75% women + 2% registration. Total: men 7%, women 5.75%." },
          { q: "Women discount UK?", a: "25% discount — women pay 3.75% vs men's 5%." },
          { q: "Can outsiders buy in Uttarakhand?", a: "Non-residents can buy residential but agricultural land has restrictions." },
          { q: "Registration in Dehradun?", a: "Visit Sub-Registrar office in Dehradun." },
          { q: "Circle rate Dehradun?", a: "Dehradun circle rates vary. Rajpur Road, EC Road premium areas high rates." },
          { q: "Documents for UK registration?", a: "Sale deed, Khatauni, identity proof, witnesses." }
        ]
      }
    },

    "jammu-kashmir": {
      name: "Jammu & Kashmir",
      slug: "jammu-kashmir",
      color: "#2563eb",
      flag: "🏔️",
      stampDuty: { male: 5, female: 3, joint: 4 },
      registrationCharges: { male: 1, female: 1, joint: 1 },
      transferDuty: 0,
      hasWomenDiscount: true,
      womenDiscount: 2,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { male: 5, female: 3 },
        commercial: { stamp: 5, reg: 1 },
        agricultural: { stamp: 3, reg: 1 }
      },
      minimumValue: null,
      notes: "J&K: 2% women discount. Post-2019 as UT, non-residents can buy property.",
      seo: {
        title: "J&K Stamp Duty Calculator 2025 — Property Registration | Calculatorcity",
        description: "Calculate stamp duty for Jammu Kashmir property. J&K stamp duty 5% (men) 3% (women) + 1% registration. Srinagar, Jammu registration charges.",
        h1: "Jammu & Kashmir Stamp Duty Calculator",
        subtitle: "J&K stamp duty — 5% men, 3% women. Post-2019 non-residents can buy."
      },
      content: {
        howItWorks: `<p>J&K charges <strong>5% stamp duty for men and 3% for women</strong> — a 2% discount. Since becoming a UT in 2019, non-residents of India can now purchase property in J&K (earlier restricted).</p>`,
        stateSpecific: `<p>This is a significant change — before 2019, only J&K domicile holders could buy property. Now any Indian citizen can invest in Srinagar, Jammu, or other J&K areas.</p>`,
        faq: [
          { q: "J&K stamp duty?", a: "5% men, 3% women + 1% registration. Total: men 6%, women 4%." },
          { q: "Can non-J&K people buy property now?", a: "Yes. Since J&K became a UT in 2019, any Indian citizen can buy property in J&K." },
          { q: "Women discount J&K?", a: "2% discount — women pay 3% vs men's 5%." },
          { q: "Is Srinagar property affordable?", a: "Srinagar has growing property market. Circle rates vary by zone." },
          { q: "How to register property in J&K?", a: "Visit Sub-Registrar office in the district. J&K Revenue portal for details." },
          { q: "Documents for J&K registration?", a: "Sale deed, Girdawari, Fard Badar, identity proof, witnesses." }
        ]
      }
    },

    chandigarh: {
      name: "Chandigarh (UT)",
      slug: "chandigarh",
      color: "#16a34a",
      flag: "🌹",
      stampDuty: { male: 6, female: 4, joint: 5 },
      registrationCharges: { male: 1, female: 1, joint: 1 },
      transferDuty: 0,
      hasWomenDiscount: true,
      womenDiscount: 2,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { male: 6, female: 4 },
        commercial: { stamp: 6, reg: 1 },
        agricultural: { stamp: 6, reg: 1 }
      },
      minimumValue: null,
      notes: "Chandigarh UT: 2% women discount. Same as Delhi discount. Total: men 7%, women 5%.",
      seo: {
        title: "Chandigarh Stamp Duty Calculator 2025 — UT Property Registration | Calculatorcity",
        description: "Calculate stamp duty for Chandigarh UT property. Chandigarh stamp duty 6% (men) 4% (women) + 1% registration. Sector-wise registration charges.",
        h1: "Chandigarh Stamp Duty Calculator",
        subtitle: "Chandigarh UT stamp duty — 6% for men, 4% for women. All Chandigarh sectors."
      },
      content: {
        howItWorks: `<p>Chandigarh UT charges <strong>6% stamp duty for men and 4% for women</strong>. Registration charges are 1%. Different from Punjab (which surrounds it) where women pay 5%.</p>`,
        stateSpecific: `<p>Chandigarh has very high property values — sectors near the Capitol Complex, Sector 17, and Sector 35 are premium. Circle rates are high reflecting the planned city's property values.</p>`,
        faq: [
          { q: "Chandigarh stamp duty?", a: "6% men, 4% women + 1% registration. Total: men 7%, women 5%." },
          { q: "Is Chandigarh different from Punjab for stamp duty?", a: "Yes. Chandigarh is a UT with separate rates. Punjab charges 7% (men), Chandigarh charges 6% (men)." },
          { q: "Women discount Chandigarh?", a: "2% discount — women pay 4% vs men's 6%." },
          { q: "Circle rate Chandigarh?", a: "Chandigarh has sector-wise circle rates. Premium sectors have very high rates." },
          { q: "How to register in Chandigarh?", a: "Visit Sub-Registrar office, Sector 17, Chandigarh." },
          { q: "Documents for Chandigarh registration?", a: "Sale deed, allotment letter (if CHB/PUDA), identity proof, witnesses." }
        ]
      }
    },

    puducherry: {
      name: "Puducherry (UT)",
      slug: "puducherry",
      color: "#7c3aed",
      flag: "🌺",
      stampDuty: { male: 5, female: 5, joint: 5 },
      registrationCharges: { male: 2, female: 2, joint: 2 },
      transferDuty: 0,
      hasWomenDiscount: false,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { stamp: 5, reg: 2 },
        commercial: { stamp: 5, reg: 2 },
        agricultural: { stamp: 4, reg: 2 }
      },
      minimumValue: null,
      notes: "Puducherry: 5% + 2% = 7% total. Surrounded by Tamil Nadu but own separate rates.",
      seo: {
        title: "Puducherry Stamp Duty Calculator 2025 | Calculatorcity",
        description: "Calculate stamp duty for Puducherry property. Puducherry stamp duty 5% + 2% registration = 7% total. Different from Tamil Nadu rates.",
        h1: "Puducherry Stamp Duty Calculator",
        subtitle: "Puducherry UT stamp duty — 5% + 2% registration. Separate from TN rates."
      },
      content: {
        howItWorks: `<p>Puducherry UT charges <strong>5% stamp duty and 2% registration</strong> — different from surrounding Tamil Nadu (7% + 4%). Total 7% vs TN's 11% makes Puducherry significantly cheaper for property registration.</p>`,
        stateSpecific: `<p>Puducherry is a popular destination for retirement homes and holiday properties due to its French heritage and lower costs than Chennai. Properties near Auroville, White Town, and Promenade Beach are high-demand.</p>`,
        faq: [
          { q: "Puducherry stamp duty?", a: "5% stamp duty + 2% registration = 7% total. Much cheaper than TN (11%)." },
          { q: "Is Puducherry cheaper than Tamil Nadu for property?", a: "Yes — 7% total vs TN's 11% total. Saving = 4% of property value on Puducherry property." },
          { q: "Women discount Puducherry?", a: "No specific women discount in Puducherry." },
          { q: "Registration in Puducherry?", a: "Visit Sub-Registrar office in Puducherry town." },
          { q: "Can non-residents buy in Puducherry?", a: "Yes, any Indian citizen can buy property in Puducherry UT." },
          { q: "Documents for Puducherry registration?", a: "Sale deed, previous title documents, EC, identity proof, witnesses." }
        ]
      }
    },

    ladakh: {
      name: "Ladakh (UT)",
      slug: "ladakh",
      color: "#2563eb",
      flag: "🏔️",
      stampDuty: { male: 5, female: 3, joint: 4 },
      registrationCharges: { male: 1, female: 1, joint: 1 },
      transferDuty: 0,
      hasWomenDiscount: true,
      womenDiscount: 2,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { male: 5, female: 3 },
        commercial: { stamp: 5, reg: 1 },
        agricultural: { stamp: 3, reg: 1 }
      },
      minimumValue: null,
      notes: "Ladakh UT: 2% women discount. Since 2019 UT, non-residents can buy.",
      seo: {
        title: "Ladakh Stamp Duty Calculator 2025 | Calculatorcity",
        description: "Calculate stamp duty for Ladakh UT property. Ladakh stamp duty 5% (men) 3% (women) + 1% registration. Leh, Kargil registration.",
        h1: "Ladakh Stamp Duty Calculator",
        subtitle: "Ladakh UT stamp duty — 5% men, 3% women. Leh Kargil all Ladakh."
      },
      content: {
        howItWorks: `<p>Ladakh UT charges <strong>5% for men and 3% for women</strong>. Registration charges 1%. Since becoming a UT in 2019, non-residents can purchase property in Ladakh.</p>`,
        stateSpecific: `<p>Leh and Kargil are the main towns. Tourism-driven demand for property in Leh has increased since 2019 UT status change allowing outside investment.</p>`,
        faq: [
          { q: "Ladakh stamp duty?", a: "5% men, 3% women + 1% registration." },
          { q: "Can outsiders buy in Ladakh?", a: "Yes — since 2019 UT status, any Indian can buy." },
          { q: "Women discount Ladakh?", a: "2% discount — women pay 3% vs men's 5%." },
          { q: "Registration in Leh?", a: "Visit Sub-Registrar office in Leh." },
          { q: "Documents for Ladakh registration?", a: "Sale deed, Fard, identity proof, witnesses." },
          { q: "Is property affordable in Leh?", a: "Property prices have risen in Leh due to tourism. Circle rates set by UT administration." }
        ]
      }
    },

    "andaman-nicobar": {
      name: "Andaman & Nicobar",
      slug: "andaman-nicobar",
      color: "#16a34a",
      flag: "🏝️",
      stampDuty: { male: 5, female: 5, joint: 5 },
      registrationCharges: { male: 2, female: 2, joint: 2 },
      transferDuty: 0,
      hasWomenDiscount: false,
      hasUrbanRural: false,
      propertyTypes: {
        residential: { stamp: 5, reg: 2 },
        commercial: { stamp: 5, reg: 2 },
        agricultural: { stamp: 5, reg: 2 }
      },
      minimumValue: null,
      notes: "Andaman: strict restrictions on outsiders buying property. Total 7%.",
      seo: {
        title: "Andaman Nicobar Stamp Duty Calculator 2025 | Calculatorcity",
        description: "Calculate stamp duty for Andaman Nicobar property. AN stamp duty 5% + 2% registration = 7%. Port Blair registration. Restrictions for non-residents.",
        h1: "Andaman & Nicobar Stamp Duty Calculator",
        subtitle: "Andaman UT stamp duty — 5% + 2% registration. Strict outsider restrictions apply."
      },
      content: {
        howItWorks: `<p>Andaman & Nicobar charges <strong>5% stamp duty and 2% registration</strong>. However, there are very strict restrictions on outsiders (non-Andaman residents) purchasing property here. Most properties can only be bought by registered settlers and long-term residents.</p>`,
        stateSpecific: `<p>Due to the tribal areas, protected forests, and restricted zones, property purchase in Andaman is heavily regulated. Non-residents require special permissions. Only Port Blair and a few designated areas allow more open property transactions.</p>`,
        faq: [
          { q: "Can outsiders buy property in Andaman?", a: "Very restricted. Only long-term settlers and certain categories of residents can buy. Non-Andaman residents require special permission from LG office." },
          { q: "Andaman stamp duty?", a: "5% + 2% = 7% total." },
          { q: "Registration in Port Blair?", a: "Sub-Registrar office in Port Blair." },
          { q: "Women discount Andaman?", a: "No women discount." },
          { q: "Documents for Andaman registration?", a: "Residency certificate may be required additionally for property purchase." },
          { q: "What are restricted zones in Andaman?", a: "Tribal reserve areas, forest lands, and certain island areas are restricted. Port Blair and specified settlements are more accessible." }
        ]
      }
    }
  };

  const stampDutyStateOrder = [
    "andhra-pradesh", "telangana", "karnataka", "tamil-nadu", "kerala",
    "maharashtra", "gujarat", "delhi", "uttar-pradesh", "rajasthan",
    "west-bengal", "madhya-pradesh", "haryana", "punjab", "bihar",
    "odisha", "himachal-pradesh", "goa", "jharkhand", "chhattisgarh",
    "assam", "uttarakhand", "jammu-kashmir", "chandigarh", "puducherry",
    "ladakh", "andaman-nicobar"
  ];

  window.stampDutyData = stampDutyData;
  window.stampDutyStateOrder = stampDutyStateOrder;
  window.stampDutyStateColors = {
    "andhra-pradesh": "#0ea5e9",
    telangana: "#f97316",
    karnataka: "#dc2626",
    "tamil-nadu": "#7c3aed",
    kerala: "#16a34a",
    maharashtra: "#f59e0b",
    delhi: "#2563eb",
    gujarat: "#d97706",
    default: "#7c3aed"
  };
})();

