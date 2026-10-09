# 💰 Personal Finance Analysis (Python + Excel)

## 📌 Project Overview
This project takes a messy, real-world-style personal finance dataset and cleans it step by step using **Python (pandas)**. The cleaned data is then used to build an interactive dashboard in **Excel** to present spending insights.

## 🎯 Objective
- Practice real-world data cleaning: missing values, duplicates, inconsistent formatting, mixed date formats, messy currency values
- Analyze spending patterns from the cleaned data (by category, by month, by payment mode)
- Auto-generate an Excel report using Python (formulas + charts, not hardcoded values)

## 🛠️ Tools & Technologies
- **Python** — pandas (data cleaning), openpyxl (Excel report generation)
- **Excel** — dashboard, KPIs, charts (via formulas: SUMIF, INDEX/MATCH, COUNTIF)

## 📂 Project Structure
```
├── data/
│   ├── expenses_raw.csv              → Original messy dataset (230 rows)
│   └── expenses_cleaned.csv          → Cleaned dataset (216 rows)
├── scripts/
│   └── clean_data.py                 → Step-by-step pandas cleaning script
├── excel/
│   └── Expense_Analysis_Report.xlsx  → Dashboard with KPIs + 6 charts
└── README.md                         → Project documentation
```

## 🧹 Data Cleaning Steps (see `scripts/clean_data.py`)
1. Removed 10 exact duplicate rows
2. Standardized the `Category` column (fixed casing, trimmed whitespace, corrected typos using a mapping dictionary)
3. Standardized the `Payment_Mode` column
4. Cleaned the `Amount` column — removed currency symbols (₹, Rs.), fixed comma-as-decimal formatting, removed negative signs
5. Parsed mixed date formats (`DD-MM-YYYY`, `MM/DD/YYYY`, `YYYY-MM-DD`) into one consistent format
6. Handled missing values — dropped rows that were unusable (missing Amount or Date), filled the rest with "Unknown"
7. Added derived `Year` and `Month` columns for easier grouping

## 📊 Key Insights
| Metric | Value |
|---|---|
| Total Spend | ₹4,45,553 |
| Total Transactions | 216 |
| Average Transaction | ₹2,062.75 |
| Top Spending Category | Rent |

## 📈 Excel Dashboard
The Excel report includes:
- **Dashboard** sheet — 4 KPI cards + 6 charts (Spend by Category, Monthly Trend, Payment Mode split, Transaction Count by Category, Top 5 Highest Expenses)
- **Cleaned Data** sheet — the processed dataset
- **Chart Data** sheet (hidden) — helper tables that feed the charts
- **How It Was Cleaned** sheet — documentation of every cleaning decision

## 🚀 How to Reproduce
1. Run `python clean_data.py` on `expenses_raw.csv` to generate `expenses_cleaned.csv`
2. Run `python build_expense_excel.py` to generate the Excel dashboard
3. Open `Expense_Analysis_Report.xlsx` in Excel to view the dashboard

## 💡 Key Takeaway
This project demonstrates a common real-world analyst workflow: cleaning messy, inconsistent data with Python before it can be trusted for reporting, then presenting the results in a business-friendly Excel dashboard.

---
**Author:** [Your Name] | Data Analyst Portfolio Project
