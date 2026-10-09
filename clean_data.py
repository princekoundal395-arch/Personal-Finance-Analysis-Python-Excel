"""
==============================================================
PERSONAL EXPENSE ANALYSIS - DATA CLEANING WITH PANDAS
==============================================================
Ye script ek "messy" (real-world jaisi dirty) expenses.csv file
ko step-by-step clean karta hai. Har step ke upar comment mein
likha hai KYA kiya ja raha hai aur KYUN.

Common real-world data problems jo yahan handle kiye gaye hain:
1. Missing values (khali cells)
2. Duplicate rows (same entry do baar)
3. Inconsistent text casing (Food, food, FOOD)
4. Extra whitespace (" Food ", "Food ")
5. Typos/variants (Entertainement vs Entertainment)
6. Messy number formats (₹500, Rs.500, "-500", "500,00")
7. Mixed date formats (01-04-2024, 01/04/2024, 2024-04-01)
==============================================================
"""

import pandas as pd

# ------------------------------------------------------------
# STEP 1: Load the raw CSV file
# ------------------------------------------------------------
df = pd.read_csv("data/expenses_raw.csv")
print("STEP 1: Raw data loaded")
print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
print(df.head(), "\n")


# ------------------------------------------------------------
# STEP 2: First look — inspect the mess before fixing anything
# ------------------------------------------------------------
# .isnull().sum() batata hai har column mein kitni missing values hain
print("STEP 2: Missing values per column")
print(df.isnull().sum(), "\n")

# .duplicated().sum() batata hai kitni pura-pura duplicate rows hain
print("Duplicate rows found:", df.duplicated().sum(), "\n")


# ------------------------------------------------------------
# STEP 3: Remove exact duplicate rows
# ------------------------------------------------------------
# drop_duplicates() saari columns match hone par duplicate row hata deta hai
before = len(df)
df = df.drop_duplicates()
after = len(df)
print(f"STEP 3: Removed {before - after} duplicate rows. New shape: {df.shape}\n")


# ------------------------------------------------------------
# STEP 4: Clean the 'Category' column
# ------------------------------------------------------------
# Problem: "Food", "food", " Food ", "Foods" — sab same category hain
# lekin text alag hone se pandas inhe alag treat karega.

# 4a) Extra whitespace hatao (dono taraf se) aur sabko Title Case mein badlo
df['Category'] = df['Category'].str.strip().str.title()

# 4b) Ab bhi kuch typos/variants bache honge (jaise "Entertainement", "Grocery")
#     Ek "mapping dictionary" banate hain jo galat spelling ko sahi se jodta hai
category_fix_map = {
    "Foods": "Food",
    "Grocery": "Groceries",
    "Entertainement": "Entertainment",
    "Health Care": "Healthcare",
    "Misc": "Other",
    "Transportation": "Transport",
    "Utility": "Utilities",
}
# .replace() dictionary use karke values ko replace karta hai
df['Category'] = df['Category'].replace(category_fix_map)

print("STEP 4: Category column cleaned. Unique categories now:")
print(sorted(df['Category'].dropna().unique()), "\n")


# ------------------------------------------------------------
# STEP 5: Clean the 'Payment_Mode' column (same idea as Category)
# ------------------------------------------------------------
df['Payment_Mode'] = df['Payment_Mode'].str.strip().str.title()
# "Upi" ko "UPI" jaisa proper acronym banate hain
df['Payment_Mode'] = df['Payment_Mode'].replace({"Upi": "UPI"})

print("STEP 5: Payment_Mode cleaned. Unique values:")
print(sorted(df['Payment_Mode'].dropna().unique()), "\n")


# ------------------------------------------------------------
# STEP 6: Clean the 'Amount' column (the messiest one!)
# ------------------------------------------------------------
# Problem examples: "₹500", "Rs.500", " 500 ", "-500", "2645,00"
# Hume isse ek clean NUMBER (float) mein badalna hai.

def clean_amount(value):
    """Ek single Amount value ko clean number mein convert karta hai."""
    if pd.isna(value):
        return None  # missing value ko missing hi rehne do (abhi ke liye)
    
    value = str(value).strip()          # whitespace hatao
    value = value.replace("₹", "")       # currency symbol hatao
    value = value.replace("Rs.", "")     # "Rs." hatao
    value = value.replace(" ", "")

    # Is dataset mein comma paise ke liye decimal marker jaisa use hua hai
    # (e.g. "2645,00" ka matlab 2645 rupees, 00 paise -> 2645.00)
    # isliye comma ko hataने ki jagah "." se replace karna zaroori hai,
    # warna "2645,00" galti se "264500" ban jayega (100 guna zyada!)
    value = value.replace(",", ".")
    
    try:
        num = float(value)
    except ValueError:
        return None  # agar phir bhi convert na ho, use missing maan lo
    
    return abs(num)  # negative signs hata do (expense hamesha positive hona chahiye)

# .apply() column ke har value par ye function chalata hai
df['Amount'] = df['Amount'].apply(clean_amount)

print("STEP 6: Amount column cleaned. Sample values:")
print(df['Amount'].head(10), "\n")


# ------------------------------------------------------------
# STEP 7: Clean the 'Date' column (mixed formats!)
# ------------------------------------------------------------
# pd.to_datetime() ke saath format=None dete hain aur dayfirst try karte hain,
# lekin mixed formats ke liye best approach hai "infer" mode use karna.
df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=False, errors='coerce')

print("STEP 7: Date column converted. Sample values:")
print(df['Date'].head(10), "\n")
print("Rows where date could not be parsed:", df['Date'].isnull().sum(), "\n")


# ------------------------------------------------------------
# STEP 8: Handle remaining missing values
# ------------------------------------------------------------
# Ab dekhte hain kitni missing values reh gayi hain har column mein
print("STEP 8: Missing values after cleaning:")
print(df.isnull().sum(), "\n")

# Decision: 
# - Agar Amount ya Date missing hai, wo row analysis ke liye useless hai -> drop karo
# - Agar Category/Description/Payment_Mode missing hai -> "Unknown" se fill karo
df = df.dropna(subset=['Amount', 'Date'])
df['Category'] = df['Category'].fillna("Unknown")
df['Description'] = df['Description'].fillna("Not specified")
df['Payment_Mode'] = df['Payment_Mode'].fillna("Unknown")

print(f"STEP 8b: After dropping unusable rows, shape: {df.shape}\n")


# ------------------------------------------------------------
# STEP 9: Add helpful derived columns (Month, Year) for analysis
# ------------------------------------------------------------
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month_name()

print("STEP 9: Added Year and Month columns\n")


# ------------------------------------------------------------
# STEP 10: Final check and save cleaned data
# ------------------------------------------------------------
df = df.sort_values('Date').reset_index(drop=True)

print("STEP 10: Final cleaned data")
print(df.dtypes)
print(df.head())

df.to_csv("expenses_cleaned.csv", index=False)
print("\nSaved cleaned file as expenses_cleaned.csv")
print(f"Final shape: {df.shape[0]} rows, {df.shape[1]} columns")
