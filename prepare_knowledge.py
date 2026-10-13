"""
Script to prepare knowledge.md from the PDF document:
'Funding Opportunity - Industry Sector Wise'
Uses pypdf to verify extraction and generates a clean, de-duplicated, compact knowledge.md.
"""
import os
import pypdf

def extract_raw_text(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return ""
    reader = pypdf.PdfReader(pdf_path)
    text = ""
    for idx, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        text += f"\n--- Page {idx+1} ---\n{page_text}"
    return text

def create_knowledge_file():
    knowledge_content = """# Funding Opportunity - Industry Sector Wise: Knowledge Base

## 1. Industry Sector & Cross-Sector Schemes
- **Climate Solution Fund**: Fund up to ₹50 L | Eligibility: DPIIT-recognized startup. Sole proprietorships can apply [with condition] | Sectors: Agri-Tech, Green/Clean Energy
- **Propel Grant**: Grant up to ₹2.5 L (Service) & Grant up to ₹3.5 L (Manuf) + Additional fund up to ₹8 L | Eligibility: Individual, Proprietorship, Partnership, LLP, Pvt Ltd, Not registered yet | Sectors: Agri-Tech, Animal Sector, Healthcare & Bio-Tech, Edu Tech, Waste Management, Green/Clean Energy, Logistic/Mobility, IT/E-Commerce, Cybersecurity, Textile & Handicraft, Fintech, Defence, Major Sector
- **CGSS Scheme (Credit Guarantee Support Scheme)**: Credit Guarantee Support on Loan up to ₹20 Cr | Eligibility: Pvt Ltd, LLP, Partnership with DPIIT | Sectors: Agri-Tech, Food Sector, Animal Sector, Healthcare & Bio-Tech, Edu Tech, Waste Management, AI/IoT/Robotic, Green/Clean Energy, Logistic/Mobility, IT/E-Commerce, Cybersecurity, Textile & Handicraft, Fintech, Defence, Major Sector
- **Global Impact Grant**: Grant up to ₹1.5 Cr (1st Stage), ₹4.5 Cr (2nd Stage) & ₹14 Cr (3rd Stage) | Eligibility: Pvt Ltd, LLP, Partnership, OPC, Limited, Proprietorship, Non-profits, NGO | Sectors: Agri-Tech, Food Sector, Animal Sector, Healthcare & Bio-Tech, Edu Tech, AI/IoT/Robotic, Green/Clean Energy, Semiconductors, IT/E-Commerce, Cybersecurity, Textile & Handicraft, Defence, Construction, NGO Scheme, Major Sector
- **RKVY RAFTAAR**: Grant up to ₹25 L | Eligibility: Pvt Ltd, LLP, Partnership, Proprietorship & Individual | Sectors: Agri-Tech, Food Sector, Animal Sector
- **Idea Grant**: Grant up to ₹1 L | Eligibility: Individual, Proprietorship, Partnership, LLP, Pvt Ltd, Not registered yet | Sectors: Agri-Tech, Green/Clean Energy, Logistic/Mobility, IT/E-Commerce
- **CSR Startup Grant**: Grant up to ₹30 L | Eligibility: Pvt Ltd, LLP, Partnership, OPC | Sectors: Agri-Tech, Healthcare & Bio-Tech, AI/IoT/Robotic, Semiconductors, Logistic/Mobility, Cybersecurity, Defence, Major Sector
- **Velocity Fund**: Funding up to ₹ 9 Cr | Eligibility: Pvt Ltd, LLP, Partnership, Limited Company | Sectors: Agri-Tech, Food Sector, Animal Sector, Waste Management, AI/IoT/Robotic, Green/Clean Energy
- **Growth Grant**: Grant up to ₹1.7 Cr | Eligibility: Applicants must be aged 22 or younger | Sectors: Agri-Tech, Food Sector, Animal Sector, Healthcare & Bio-Tech, Edu Tech, AI/IoT/Robotic, Construction, Young Entrepreneur Scheme
- **Agri-Sure Fund**: Funding up to ₹25 CR (Equity based) | Eligibility: Pvt Ltd, LLP, Partnership (DPIIT) | Sectors: Agri-Tech, Food Sector, Animal Sector
- **Agri-Tech Innovation Grant**: Grant up to ₹7.5 L | Eligibility: Individual Farmer, Farmer Group, Pvt Ltd, LLP, Partnership, Proprietorship & Individual entrepreneur | Sectors: Agri-Tech
- **Early Stage Investment**: Funding up to ₹9.5 Cr | Eligibility: Pvt Ltd & LLP | Sectors: Agri-Tech, Food Sector, Animal Sector, Healthcare & Bio-Tech, Edu Tech, Waste Management, AI/IoT/Robotic, Green/Clean Energy, Semiconductors, Logistic/Mobility, IT/E-Commerce, Cybersecurity, Textile & Handicraft, Fintech, Defence, Construction, Major Sector
- **Social Fund**: Up to INR 2.63 Cr ($300,000 USD) in either unrestricted grant funding or investment capital | Eligibility: Non-profit, mission-driven for-profit entity. Organization is less than 10 years old | Sectors: Agri-Tech, Food Sector, Animal Sector, Healthcare & Bio-Tech, Edu Tech, Waste Management, AI/IoT/Robotic, Green/Clean Energy, Semiconductors, Logistic/Mobility, IT/E-Commerce, Cybersecurity, Textile & Handicraft, Fintech, Defence, Construction, NGO Scheme
- **NAIFF (National Agriculture Infra Financing Facility)**: Loan up to ₹2 Cr with 3% Interest Subsidy | Eligibility: Startup, MSMEs, Individual, FPO, SHG, Co-operative, APMC, other agri based entity | Sectors: Agri-Tech, Food Sector
- **Start up Support Scheme SSS**: Funding from ₹25 L to ₹1 Cr | Eligibility: Pvt Ltd, LLP, Partnership, Proprietorship | Sectors: Agri-Tech, Food Sector, Animal Sector, Healthcare & Bio-Tech, Edu Tech, Waste Management, AI/IoT/Robotic, Green/Clean Energy, Semiconductors, Logistic/Mobility, Textile & Handicraft, Fintech, Defence, Major Sector
- **Invoice Sahay**: Loan up to ₹1 Cr | Eligibility: Proprietorship, Partnership, LLP, Pvt Ltd. Minimum 2 yrs of business vintage | Sectors: Agri-Tech, Animal Sector, Healthcare & Bio-Tech, Edu Tech, Waste Management, AI/IoT/Robotic, Green/Clean Energy, Semiconductors, Logistic/Mobility, IT/E-Commerce, Textile & Handicraft, Fintech, Defence, Construction, Major Sector
- **PMFME (PM Formalisation of Micro food processing Enterprises)**: Capital Subsidy up to ₹ 10 L | Eligibility: Individuals, Proprietorship, Partnership, FPOs, NGOs, Cooperatives, SHGs, Pvt Ltd | Sectors: Food Sector
- **Evolve-Tech Funding**: Funding up to ₹25 L (Equity based) | Eligibility: Pvt Ltd, LLP, Partnership (DPIIT). Revenue generating startups | Sectors: Food Sector, Healthcare & Bio-Tech, Edu Tech, Waste Management, AI/IoT/Robotic, Green/Clean Energy, Semiconductors, Logistic/Mobility, Cybersecurity, Textile & Handicraft, Fintech, Defence, Construction, Major Sector
- **Atom Fund**: Funding up to ₹17.9 Cr for AI sector; Funding up to ₹8.9 Cr (up to $1M) for all sectors | Eligibility: Pvt Ltd, LLP, Partnership, Proprietorship | Sectors: Food Sector, Animal Sector, Healthcare & Bio-Tech, Edu Tech, Waste Management, AI/IoT/Robotic, Semiconductors, Logistic/Mobility, IT/E-Commerce, Cybersecurity, Fintech, Major Sector
- **PMEGP (Prime Minister's Employment Generation Programme)**: Loan up to ₹20 L (Service) & ₹50 L (Mfg) with Capital Subsidy between 15% to 35% | Eligibility: An individual with a new business | Sectors: Food Sector, Edu Tech, AI/IoT/Robotic, Green/Clean Energy, Semiconductors, Logistic/Mobility, IT/E-Commerce, Cybersecurity, Textile & Handicraft, Fintech, Defence, Construction, Major Sector
- **Master Fund**: Funding up to ₹35 L | Eligibility: Private Limited, LLP, Partnerships | Sectors: Food Sector, Edu Tech, Waste Management, Green/Clean Energy, Logistic/Mobility, IT/E-Commerce, Cybersecurity, Textile & Handicraft, Fintech, Defence, Construction, Major Sector
- **Pro-Fund Support**: Funding from ₹2 L to ₹30 L | Eligibility: Pvt Ltd, LLP, Partnership, Proprietorship & Individual | Sectors: Food Sector, Animal Sector, Healthcare & Bio-Tech, Edu Tech, Waste Management, Semiconductors, Logistic/Mobility, IT/E-Commerce, Cybersecurity, Fintech, Defence, Construction, Major Sector
- **Sprint Yojna**: Fund up to ₹25 L | Eligibility: Pvt Ltd, LLP, Partnership, Proprietorship, Other For-profit entities | Sectors: Animal Sector
- **FIDF (Fisheries and Aquaculture Infrastructure Development Fund)**: Loan 80% of Project cost with 3% Interest Subsidy | Eligibility: Private Companies, Entrepreneurs, Cooperative Federations, Other Institution/ Entity | Sectors: Animal Sector
- **AHIDF (Animal Husbandry Infrastructure Development Fund)**: Loan 90% of Project cost with 3% Interest Subsidy | Eligibility: FPOs, Startup, MSMEs, Section 8 companies | Sectors: Animal Sector
- **NGO Kickstarter**: Grant up to ₹15 L | Eligibility: NGOs | Sectors: Healthcare & Bio-Tech, NGO Scheme
- **RDI Fund**: Financing up to 50% of the total assessed project cost | Eligibility: Pvt Ltd, LLP, Registered Partnership | Sectors: Healthcare & Bio-Tech, AI/IoT/Robotic, Green/Clean Energy
- **ScaleUp Grant**: Pilot: Up to ₹2 Cr, Test & Position: Up to ₹15 Cr, Transition to Scale: up to ₹40 Cr | Eligibility: Proprietorship, Partnership, LLP, Pvt Ltd, Non-profits, NGOs, Section 8 | Sectors: Healthcare & Bio-Tech, Waste Management, Semiconductors, Logistic/Mobility, IT/E-Commerce, Cybersecurity, Textile & Handicraft, Construction, NGO Scheme, Major Sector
- **Mudra Loan**: Loan up to ₹20 L | Eligibility: MSMEs | Sectors: Healthcare & Bio-Tech, Edu Tech, Waste Management, Semiconductors, IT/E-Commerce, Cybersecurity, Textile & Handicraft, Fintech, Construction
- **Equity Linked Seed Fund**: Fund up to ₹30 L | Eligibility: Pvt Ltd (DPIIT), Entity age < 5 yrs | Sectors: Healthcare & Bio-Tech
- **Equity Elevator**: Funding up to ₹4 Cr | Eligibility: Pvt Ltd, LLP, Partnership, Proprietorship | Sectors: Edu Tech, AI/IoT/Robotic, Semiconductors, Logistic/Mobility, IT/E-Commerce, Cybersecurity, Textile & Handicraft, Fintech, Defence, Construction, Major Sector
- **CGTMSE**: Loan up to ₹10 Cr | Eligibility: Pvt Ltd, LLP, Partnership, Proprietorship (entity age > 2 yrs) | Sectors: Edu Tech, Waste Management, AI/IoT/Robotic, Semiconductors, Logistic/Mobility, Textile & Handicraft, Fintech, Defence, Construction, Major Sector
- **Inno-Preneurs**: Total Funding up to ₹5 Cr, Reward of INR 50 L | Eligibility: Individual, Partnership, LLP, Pvt Ltd, and Proprietorship | Sectors: Waste Management, Semiconductors, Cybersecurity, Major Sector
- **Sustainability Sprint**: Funding up to ₹40 L | Eligibility: Pvt Ltd, LLP, Partnership | Sectors: Waste Management, Textile & Handicraft
- **Titanium Fund**: Fund up to ₹50 L | Eligibility: Pvt Ltd | Sectors: AI/IoT/Robotic, Green/Clean Energy, Semiconductors
- **Fund for Business Gateway**: Funding up to ₹2 Cr | Eligibility: Pvt Ltd, LLP, Partnership, Section 8 | Sectors: AI/IoT/Robotic
- **Spring Program**: Funding up to ₹1 Cr | Eligibility: Individuals, students, Pvt Ltd, LLP, partnerships, proprietorships | Sectors: AI/IoT/Robotic
- **PoC Pilot Program**: Funding up to INR 50 Lakhs per Project (Up to 80% Grant-in-Aid) | Eligibility: Startup & MSMEs | Sectors: AI/IoT/Robotic, Semiconductors
- **Renewable Energy Innovation Grant**: Grant up to ₹2.5 L | Eligibility: Individual, Startup, MSME, Farmer groups, FPOs, and rural enterprises | Sectors: Green/Clean Energy
- **Deeptech Fund**: Funding up to ₹9.5 Cr | Eligibility: Pvt Ltd | Sectors: Semiconductors
- **Women-Preneur for Bharat**: Fund up to ₹15 L | Eligibility: DPIIT-recognized startup, Women must hold more than 51% equity | Sectors: Logistic/Mobility, Women Entrepreneur
- **Investment for Transformation**: Investment up to ₹3 Cr | Eligibility: Pvt Ltd, LLP, Partnership | Sectors: IT/E-Commerce
- **Cutting-Edge Inception**: Private funding from VC (NVIDIA) | Eligibility: Pvt Ltd, LLP, Partnership, Proprietorship & Other | Sectors: IT/E-Commerce
- **Grant for Textile**: Grant up to ₹50 L | Eligibility: Pvt Ltd, LLP, Partnership & Individual | Sectors: Textile & Handicraft
- **BI Initiative**: Funding up to ₹42 L | Eligibility: Pvt Ltd, LLP, Partnership, Proprietorship | Sectors: Fintech Sector
- **Fintech Bridge**: Funding up to ₹8.6 Cr | Eligibility: Pvt Ltd (DPIIT) | Sectors: Fintech Sector
- **Startup Nivesh**: Fund up to ₹5 Cr | Eligibility: DPIIT-recognized Private Limited | Sectors: Fintech Sector, Defence Sector
- **Defence Fund**: Funding up to ₹3.6 Cr | Eligibility: Proprietorship, Partnership, Pvt Ltd, LLP, Unregistered (they need to register) | Sectors: Defence Sector

## 2. State-Specific Schemes

### Tamil Nadu
- **UYEGP Scheme (TN)**: Capital Subsidy 25% of the Project (Max ₹3.75 lakh) | Eligibility: Individual (age >18 years), Tamilnadu State
- **ARISE Loan (TN)**: Capital Subsidy up to ₹3.5 Lakh | Eligibility: Scheduled Caste and Scheduled Tribe, Age 18–55, Tamilnadu State
- **KKT Program (TN)**: Subsidy up to ₹50,000 (Loan up to ₹3 Lakh) | Eligibility: New entrepreneurs and expansion of existing entrepreneurs, Tamilnadu State
- **NEEDS Yojana [TN]**: Project cost: From ₹10 lakh to ₹5 crore; Subsidy up to 25% (Subject to a maximum limit of ₹75 Lakhs) | Eligibility: Partnership and Proprietorship, Tamilnadu State
- **AABCS Scheme (TN)**: 35% Subsidy (up to ₹1.5 Cr), 6% interest subvention | Eligibility: Only for SC/ST communities. Sole proprietorship, partnership, company from TamilNadu
- **IVP (TN)**: Grant up to ₹3 Lakh for Prototype, Grant up to ₹7 Lakh for commercialization | Eligibility: MSME Registered (Manufacturing), Tamilnadu
- **TWEES Scheme (TN)**: Capital Subsidy up to ₹2,00,000 (max @25%), Project cost up to ₹10 Lakh | Eligibility: Proprietorship, Partnership, LLP & Pvt Ltd, Tamil Nadu State
- **AgriTech Grant (TN)**: Grant up to Rs. 10 L for early-stage Startups; Grant up to Rs. 25 L for growth/expansion stage Startups | Eligibility: Tamil Nadu State (Sector: Agri-Tech)
- **SC/ST Startup Fund (TN)**: Corpus ₹60.80 Cr; Seed fund up to ₹10 L for other sectors | Eligibility: Partnership, LLP & Pvt Ltd (Tamil Nadu State), SC/ST founders
- **Value Addition Project Subsidy (TN)**: Loans up to ₹10 Cr with a 25% capital subsidy; 10% additional subsidy to women and SC/ST entrepreneurs & backward regions; 5% interest subsidy for 5 years | Eligibility: Pvt Ltd, LLP, Partnership, Sole Proprietorship, FPO, Co-operative (Tamil Nadu)
- **Pitch Connect (South)**: Grant up to ₹20 Lakh | Eligibility: DPIIT recognised startups, Tamilnadu State (Sectors: Waste Management)

### Kerala
- **Innovation Grant (KL)**: Grant from ₹3 L TO 30 L | Eligibility: Pvt Ltd, LLP & OPC, Kerala Startup Mission Unique ID, Kerala State
- **Seed Fund (KL)**: Up to ₹15 Lakhs at subsidized interest rate of 6% | Eligibility: DPIIT approved, Kerala Startup Mission Unique ID, Kerala State
- **AgriNext (KL)**: Up to ₹25 Lakhs Grant Support (Up to ₹20L product dev, Up to ₹5L market validation & pilot deployment) | Eligibility: DPIIT Recognized (Reg. Partnership, LLP & Pvt Ltd), Kerala-based startup and FPOs

### Karnataka
- **VC FUND(KA)**: Type A: From ₹50 Lakh to ₹1 Cr (Animation, VFX, Gaming, Comics, Media, Original IP); Type B: From ₹2 Cr to ₹3 Cr (AI, ML, MedTech, EV, Other Disruptive Technologies) | Eligibility: Private Limited from Karnataka
- **Cybersecurity Incentive Policy (KA)**: Internship Incentive: Reimburse ₹10,000/mo (UG) & ₹10,000/mo (PG) max 3 months; R&D Incentive: Conditional grant up to 50% approved R&D (max Rs. 50 lacs); Audit/Incident: Reimburse up to INR 1 lakh | Eligibility: Karnataka-based companies (MSMEs, SMEs, startups, MNCs) in Cyberspace providing cybersecurity solutions

### Telangana
- **AI First Fund (TG)**: Fund up to ₹2 Cr | Eligibility: Pvt Ltd, LLP, Partnership (DPIIT). Only for Telangana State | Sectors: AI, Green/Clean Energy, Cybersecurity

### Maharashtra
- **Venture Fund (MH)**: Fund up to ₹10 Cr | Eligibility: Pvt Ltd (DPIIT). For Maharashtra Only | Sectors: Agri-Tech, Food Sector, Animal Sector, Edu Tech, Waste Management, Green/Clean Energy, Logistic/Mobility, Cybersecurity, Fintech
- **Fund for Agri (MH)**: Funding as per project/ask (Aprox up to ₹20 Lakhs) | Eligibility: Pvt Ltd, LLP, and NGO (Not for profit). Only for Maharashtra based agritech startups
- **Venture Fund for Defence & Aerospace (MH)**: Funding up to ₹50 Cr | Eligibility: Pvt Ltd & Public Ltd. For Maharashtra based | Sector: Defence & Aerospace
- **Empowerment Grant (MH)**: Grant up to ₹10 Lakh | Eligibility: Maharashtra, Chhattisgarh, Daman & Diu and Goa based entities | Sectors: Food Sector, Animal Sector, Healthcare & Bio-Tech, Edu Tech

### Gujarat
- **Srujan Scheme (Guj)**: Grant from ₹2.5 L to ₹10 L | Eligibility: Pvt Ltd, LLP, Partnership, Proprietorship & Individual. Person age < 35 yrs & Gujarat based only | Sectors: Edu Tech, Waste Management, AI/IoT/Robotic, Green/Clean Energy, Semiconductors, Logistic/Mobility, Cybersecurity, Textile & Handicraft, Fintech, Defence, Construction, Major Sector
- **Funding Support (Guj)**: Grant up to ₹30 L & Up to ₹3 Cr Fund | Eligibility: Pvt Ltd, LLP, Partnership. Only for Gujarat based startups | Sectors: Edu Tech, IT/E-Commerce, Cybersecurity, Fintech, Construction
- **Bankable Scheme**: Funding up to ₹25 L | Eligibility: Individual person Age: 18 to 65 Years (Listed under Gujarat Scheme & Textile & Handicraft)

### Uttar Pradesh (UP)
- **Udyami Vikas (UP)**: Phase-I: 100% interest free and guarantee free Loan up to ₹ 5 Lakhs; Phase-II: 100% interest free and guarantee free Loan up to ₹ 7.5 Lakhs (upon returning 1st loan) | Eligibility: Individuals, age 21-40 Yrs, Uttar Pradesh State
- **Funding Support (UP)**: Fund up to ₹15 L | Eligibility: Pvt Ltd, LLP, Partnerships with DPIIT. For UP-based startups | Sectors: Waste Management, IT/E-Commerce, Textile & Handicraft, Defence, Major Sector

### Madhya Pradesh (MP)
- **Udyam Kranti Yojana (MP)**: Loan up to ₹ 50 Lakhs (Manufacturing); Loan up to ₹ 25 Lakhs (Service) | Eligibility: Individuals, and all companies. For Madhya Pradesh State

### Bihar
- **Seed Fund (BR)**: Interest free loan up to ₹10 Lakhs | Eligibility: LLP, Pvt Ltd, OPC, Partnership (DPIIT). Company age <10 years. For Bihar State

### Haryana
- **Seed Fund (HR)**: Grant up to ₹10 Lakhs | Eligibility: Registered Partnership, LLP or Pvt Ltd (DPIIT). For Haryana State. Must be incubated in Haryana at Govt authorised incubator

### Assam
- **Funding Support (AS)**: Funding up to ₹10 L (Idea Stage) & up to ₹20 L (Prototype/MVP Stage) & up to ₹40 L for DeepTech | Eligibility: Pvt Ltd, LLP & Partnership (Assam Based) | Sectors: Agri-Tech, Food Sector, Animal Sector, Healthcare & Bio-Tech, Edu Tech, AI/IoT/Robotic, Green/Clean Energy, Semiconductors, Logistic/Mobility, Cybersecurity, Textile & Handicraft, Fintech, Defence, Construction, Major Sector

## 3. Special Category Schemes

### SC / ST / OBC Caste Entrepreneur Schemes
- **Fund for SC Founder**: Grant up to ₹12 Lakh | Eligibility: Pvt Ltd, LLP, Partnership (DPIIT). For SC Caste Only
- **Financial Assistance for SC, ST & OBC**: Loan up to ₹15 Cr (SC/OBC) & ₹5 Cr (ST) | Eligibility: Pvt Ltd & Public Limited. Entity age > 1 yr | Sectors: Agri-Tech, Food Sector, Animal Sector, Healthcare & Bio-Tech, Waste Management, AI/IoT/Robotic, Green/Clean Energy, Semiconductors, Logistic/Mobility, Textile & Handicraft, Defence, Construction, Major Sector
- **Fund for SC/ST Entrepreneurs**: Funding up to ₹5 Cr (Equity based) | Eligibility: Pvt Ltd, LLP, Partnership, Proprietorship (DPIIT or MSME Approved). 100% stack of SC/ST Candidate (Maharashtra Only on state/category page; cross-listed in Agri-Tech, Food, Animal, Healthcare, Cybersecurity, Construction)
- **Empower SC Entrepreneurs**: Funding up to ₹30 L (Equity-based) | Eligibility: Pvt Ltd, LLP, Partnership. 51% stack of SC Candidate
- **SC/ST Startup Fund (TN)**: Corpus ₹60.80 Cr; Seed fund up to ₹10 L for other sectors | Eligibility: Partnership, LLP & Pvt Ltd (Tamil Nadu State), SC/ST founders

### Young Entrepreneur Schemes
- **Young Innovators Grant**: Grant up to ₹20 L | Eligibility: Any Individual Person age < 25 years
- **Growth Grant**: Grant up to ₹1.7 Cr | Eligibility: Applicants must be aged 22 or younger | Sectors: Agri-Tech, Food Sector, Animal Sector, Healthcare & Bio-Tech, Edu Tech, AI/IoT/Robotic, Construction

### Women Entrepreneur Scheme
- **Women-Preneur for Bharat**: Fund up to ₹15 L | Eligibility: DPIIT-recognized startup. Women must hold more than 51% equity | Sectors: Logistic/Mobility

### NGO Schemes
- **Social Fund**: Up to INR 2.63 Cr ($300,000 USD) grant funding or investment | Eligibility: Non-profit, mission-driven for-profit entity, < 10 years old
- **Global Impact Grant**: Grant up to ₹1.5 Cr (1st Stage), ₹4.5 Cr (2nd Stage) & ₹14 Cr (3rd Stage) | Eligibility: Pvt Ltd, LLP, Partnership, OPC, Limited, Proprietorship, Non-profits, NGO
- **Fund for Agri (MH)**: Funding as per project/ask (Aprox up to ₹20 Lakhs) | Eligibility: Pvt Ltd, LLP, and NGO (Not for profit). Maharashtra agritech startups
- **ScaleUp Grant**: Pilot: Up to ₹2 Cr; Test & Position: Up to ₹15 Cr; Transition to Scale: up to ₹40 Cr | Eligibility: Proprietorship, Partnership, LLP, Pvt Ltd, Non-profits, NGOs, Section 8
- **NGO Kickstarter**: Grant up to ₹15 L | Eligibility: NGOs

## 4. SIDBI Schemes
- **Machinery Finance Assistance - EXPRESS**: Loan up to ₹3 Cr | MSME units in operation >= 3 yrs | Purchase plant & machinery & miscellaneous fixed assets
- **Machinery Finance Assistance - SPEED**: Loan up to ₹15 Cr | MSME units in operation >= 3 yrs | Purchase plant & machinery & miscellaneous fixed assets
- **Sustainable Finance Assistance - Green Finance Scheme (GFS)**: Loan up to ₹50 Cr | MSME units in operation >= 3 yrs, Mfg or services | Green energy, Energy Efficiency, Compressed Bio Gas, Waste/Water, E-Mobility
- **Sustainable Finance Assistance - End to End Energy Efficiency (4E)**: Loan up to ₹15 Cr | MSME units in operation >= 3 yrs, Mfg or services | Green energy, Energy Efficiency, Compressed Bio Gas, Waste/Water, E-Mobility
- **Project Funding Assistance - ARISE**: Loan up to ₹50 Cr | Min 2 yrs operations with audited accounts | Land, factory building, plant & machinery, rooftop solar, energy efficiency
- **Project Funding Assistance - UBHARTE SITARE (US)**: Loan up to 80% of project cost | New and existing projects | Land, factory building, plant & machinery, rooftop solar, energy efficiency
- **Project Funding Assistance - STHAPAN**: Loan up to ₹50 Cr | Promoter exp: 5 yrs for > Rs. 20 Cr, 3 yrs for <= Rs. 20 Cr | Land, factory building, plant & machinery, rooftop solar, energy efficiency
- **Operational Finance Assistance - Working Capital**: Working Capital assistance as per requirement | New and existing entities | For working capital
- **Operational Finance Assistance - SWIFT**: Loan up to ₹3 Cr | Existing entities having 3 yrs operations | For working capital
- **Operational Finance Assistance - STEP**: Loan up to ₹3 Cr (existing customers), ₹2 Cr (new customers) | Min 3 yrs operations (2 yrs if existing customer), operating profit past 2 yrs (1 yr if existing customer)
"""
    return knowledge_content.strip()

if __name__ == "__main__":
    pdf_path = os.path.join("data", "Funding Opportunity - Industry Sector Wise.pdf")
    if os.path.exists(pdf_path):
        print(f"Reading {pdf_path} using pypdf...")
        extracted = extract_raw_text(pdf_path)
        print(f"Extracted {len(extracted)} characters across pages.")
    
    knowledge_text = create_knowledge_file()
    out_path = "knowledge.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(knowledge_text)
    print(f"Successfully generated {out_path} ({len(knowledge_text)} characters, ~{len(knowledge_text.split())} words).")
