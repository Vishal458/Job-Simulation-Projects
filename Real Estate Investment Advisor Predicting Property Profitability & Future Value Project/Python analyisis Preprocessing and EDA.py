"""
STEP 1 + STEP 2 ANALYSIS SCRIPT
Real Estate Investment Advisor (Beginner Friendly)
NO Streamlit, NO ML — Pure Analysis

Run:
    python step1_step2_analysis.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ======================================================
# STEP 1 — LOAD & CLEAN THE DATA
# ======================================================

DATA_PATH = "C:/Users/visha/Downloads/india_housing_prices.csv"

def load_and_clean(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV not found at {path}")

    print("\n📌 Loading dataset...")
    df = pd.read_csv(path)

    # Remove duplicates
    df = df.drop_duplicates().reset_index(drop=True)

    # Convert common numeric columns
    numeric_cols = [
        "Price_in_Lakhs", "Size_in_SqFt", "BHK",
        "Year_Built", "Nearby_Schools", "Nearby_Hospitals",
        "Parking_Space", "Price_per_SqFt"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="ignore")

    # Replace zero size with NaN (avoid divide-by-zero)
    if "Size_in_SqFt" in df.columns:
        df.loc[df["Size_in_SqFt"] == 0, "Size_in_SqFt"] = np.nan

    # Fill numeric missing values
    df[df.select_dtypes(include='number').columns] = df[df.select_dtypes(include='number').columns].fillna(
        df.select_dtypes(include='number').median()
    )

    # Fill categorical missing with mode
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].fillna(df[col].mode().iloc[0])

    # Create Price per square ft
    if {"Price_in_Lakhs", "Size_in_SqFt"}.issubset(df.columns):
        df["Price_per_SqFt"] = (df["Price_in_Lakhs"] * 100000) / df["Size_in_SqFt"]

    # Create Age of property
    if "Year_Built" in df.columns:
        df["Age_of_Property"] = 2025 - df["Year_Built"]

    # Parking flag
    if "Parking_Space" in df.columns:
        df["Has_Parking"] = df["Parking_Space"].apply(lambda x: 1 if x > 0 else 0)

    print("✅ Cleaning completed.")
    return df


df = load_and_clean(DATA_PATH)

print("\n📌 Cleaned dataset preview:")
print(df.head())

# Save cleaned file
df.to_csv("cleaned_india_housing.csv", index=False)
print("\n📁 Cleaned CSV exported as cleaned_india_housing.csv")


# ======================================================
# STEP 2 — EDA (Exploratory Data Analysis)
# ======================================================

print("\n📊 Starting EDA...")

# -----------------------------
# Summary stats
# -----------------------------
print("\n📌 Summary Statistics:")
print(df.describe())

# -----------------------------------------------
# 1. Price Distribution
# -----------------------------------------------
plt.figure(figsize=(7,4))
plt.hist(df["Price_in_Lakhs"], bins=20, alpha=0.7)
plt.title("Price Distribution (Lakhs)")
plt.xlabel("Price (Lakhs)")
plt.ylabel("Count")
plt.show()

# -----------------------------------------------
# 2. BHK Distribution
# -----------------------------------------------
if "BHK" in df.columns:
    plt.figure(figsize=(7,4))
    df["BHK"].value_counts().sort_index().plot(kind="bar")
    plt.title("BHK Distribution")
    plt.xlabel("BHK")
    plt.ylabel("Count")
    plt.show()

# -----------------------------------------------
# 3. City-wise Average Price
# -----------------------------------------------
if {"City", "Price_in_Lakhs"}.issubset(df.columns):
    city_avg = df.groupby("City")["Price_in_Lakhs"].mean().sort_values()

    plt.figure(figsize=(10,4))
    city_avg.plot(kind="bar")
    plt.title("Average Price by City")
    plt.ylabel("Avg Price (Lakhs)")
    plt.xticks(rotation=45)
    plt.show()

# -----------------------------------------------
# 4. State-wise Property Count
# -----------------------------------------------
if "State" in df.columns:
    plt.figure(figsize=(10,4))
    df["State"].value_counts().plot(kind="bar")
    plt.title("Properties per State")
    plt.xlabel("State")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.show()

# -----------------------------------------------
# 5. Size vs Price Scatter
# -----------------------------------------------
if {"Size_in_SqFt", "Price_in_Lakhs"}.issubset(df.columns):
    plt.figure(figsize=(7,5))
    plt.scatter(df["Size_in_SqFt"], df["Price_in_Lakhs"], alpha=0.5)
    plt.title("Size vs Price")
    plt.xlabel("Size (SqFt)")
    plt.ylabel("Price (Lakhs)")
    plt.show()

# -----------------------------------------------
# 6. Median Price by BHK Trend
# -----------------------------------------------
if {"BHK", "Price_in_Lakhs"}.issubset(df.columns):
    trend = df.groupby("BHK")["Price_in_Lakhs"].median()

    plt.figure(figsize=(6,4))
    plt.plot(trend.index, trend.values, marker="o")
    plt.xlabel("BHK")
    plt.ylabel("Median Price (Lakhs)")
    plt.title("Median Price by BHK")
    plt.grid(True)
    plt.show()

# -----------------------------------------------
# 7. Outlier Detection (Price)
# -----------------------------------------------
if "Price_in_Lakhs" in df.columns:
    q1 = df["Price_in_Lakhs"].quantile(0.25)
    q3 = df["Price_in_Lakhs"].quantile(0.75)
    iqr = q3 - q1
    upper = q3 + 1.5 * iqr

    outliers = df[df["Price_in_Lakhs"] > upper]

    print("\n🚨 Outliers detected (highest prices):")
    print(outliers.head(10))

# -----------------------------------------------
# 8. Heatmap: Median Price by State & City
# -----------------------------------------------
if {"State", "City", "Price_in_Lakhs"}.issubset(df.columns):
    pivot = df.pivot_table(values="Price_in_Lakhs", index="State", columns="City", aggfunc="median")

    plt.figure(figsize=(12,6))
    plt.imshow(pivot.fillna(0), cmap="coolwarm", aspect="auto")
    plt.title("Heatmap: State × City Median Prices")
    plt.xticks(range(len(pivot.columns)), pivot.columns, rotation=45)
    plt.yticks(range(len(pivot.index)), pivot.index)
    plt.colorbar(label="Median Price (Lakhs)")
    plt.show()

print("\n🎉 EDA COMPLETED SUCCESSFULLY!")
