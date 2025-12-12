import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Constants
DATA_PATH = "C:/Users/visha/Downloads/india_housing_prices.csv"

# Load and Clean Data
def load_and_clean(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV not found at {path}")

    st.write("\n📌 Loading dataset...")
    df = pd.read_csv(path)
    df = df.drop_duplicates().reset_index(drop=True)

    numeric_cols = [
        "Price_in_Lakhs", "Size_in_SqFt", "BHK", "Year_Built",
        "Nearby_Schools", "Nearby_Hospitals", "Parking_Space"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='ignore')

    df.loc[df["Size_in_SqFt"] == 0, "Size_in_SqFt"] = np.nan
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].fillna(df[col].mode().iloc[0])

    if "Price_in_Lakhs" in df.columns and "Size_in_SqFt" in df.columns:
        df["Price_per_SqFt"] = (df["Price_in_Lakhs"] * 100000) / df["Size_in_SqFt"]

    if "Year_Built" in df.columns:
        df["Age_of_Property"] = 2025 - df["Year_Built"]

    if "Parking_Space" in df.columns:
        df["Has_Parking"] = df["Parking_Space"].apply(lambda x: 1 if x > 0 else 0)

    return df

# Load the dataset
df = load_and_clean(DATA_PATH)

# Top: show cleaned dataset preview and download
# ---------------------------
st.subheader("Cleaned dataset preview")
st.write("A quick look at the cleaned data used by the app.")
with st.expander("Data Preview"):
    st.dataframe(df)

# Download button
csv_bytes = df.to_csv(index=False).encode()
st.download_button("Download cleaned CSV", csv_bytes, file_name="india_housing_prices_cleaned.csv")

# Streamlit App Title
st.title("🏠 Real Estate Investment Advisor Dashboard")

st.sidebar.header("Filters")
states = ["All"] + sorted(df["State"].dropna().unique()) if "State" in df.columns else ["All"]
state_sel = st.sidebar.selectbox("Select State", states)

# City dropdown depends on state
if "City" in df.columns:
    if state_sel != "All" and "State" in df.columns:
        cities = ["All"] + sorted(df.loc[df["State"] == state_sel, "City"].dropna().unique())
    else:
        cities = ["All"] + sorted(df["City"].dropna().unique())
else:
    cities = ["All"]
city_sel = st.sidebar.selectbox("Select City", cities)

# BHK dropdown
if "BHK" in df.columns:
    bhk_options = ["All"] + sorted(df["BHK"].dropna().astype(int).unique().tolist())
else:
    bhk_options = ["All"]
bhk_sel = st.sidebar.selectbox("Select BHK", bhk_options)

min_price, max_price = st.sidebar.slider(
    "Price Range (Lakhs)", 
    min_value=int(df["Price_in_Lakhs"].min()), 
    max_value=int(df["Price_in_Lakhs"].max()), 
    value=(10, 500)
)

st.sidebar.markdown("---")
st.sidebar.write("<h style='color:Yellow;'>Filters update - charts & KPIs interactively.</h>",unsafe_allow_html=True)

# ---------------------------
# Apply filters to dataframe
# ---------------------------
filtered = df.copy()
if state_sel != "All" and "State" in df.columns:
    filtered = filtered[filtered["State"] == state_sel]
if city_sel != "All" and "City" in df.columns:
    filtered = filtered[filtered["City"] == city_sel]
if bhk_sel != "All" and "BHK" in df.columns:
    filtered = filtered[filtered["BHK"] == bhk_sel]

# ---------------------------
# KPIs (top row)
# ---------------------------
st.subheader("Key Metrics (Cards)")
k1, k2, k3, k4, K5 = st.columns(5)

k1.metric("Properties", len(filtered))
k2.metric("Avg Price (Lakhs)", round(filtered["Price_in_Lakhs"].mean(), 2) if "Price_in_Lakhs" in filtered.columns and len(filtered)>0 else "N/A")
k3.metric("Median Price/SqFt", round(filtered["Price_per_SqFt"].median(), 2) if "Price_per_SqFt" in filtered.columns and len(filtered)>0 else "N/A")
k4.metric("Avg Size (SqFt)", round(filtered["Size_in_SqFt"].mean(), 2) if "Size_in_SqFt" in filtered.columns and len(filtered)>0 else "N/A")
K5.metric("Avg Price per SqFt", round(filtered["Price_per_SqFt"].mean(), 2))


# Visual Insights
st.markdown("<h2 style ='color:Yellow;'>Visual Insights</h2>",unsafe_allow_html=True)

# Price Distribution
st.subheader("Price Distribution")
plt.figure(figsize=(7, 4))
plt.hist(filtered["Price_in_Lakhs"], bins=20, alpha=0.7, color='blue')
plt.title("Price Distribution (Lakhs)")
plt.xlabel("Price (Lakhs)")
plt.ylabel("Count")
st.pyplot(plt)

# BHK Distribution
st.subheader("BHK Distribution")
plt.figure(figsize=(7, 4))
filtered["BHK"].value_counts().sort_index().plot(kind='bar', color='cyan')
plt.title("BHK Distribution")
plt.xlabel("BHK")
plt.ylabel("Count")
st.pyplot(plt)

# Average Price by City
if "City" in df.columns and "Price_in_Lakhs" in df.columns:
    st.subheader("Average Price by City")
    city_avg = df.groupby("City")["Price_in_Lakhs"].mean().sort_values()
    plt.figure(figsize=(10, 4))
    city_avg.plot(kind='bar')
    filtered["City"].value_counts().sort_index().plot(kind='bar')
    plt.title("Average Price by City")
    plt.ylabel("Avg Price (Lakhs)")
    plt.xticks(rotation=45)
    st.pyplot(plt)


# Heatmap of Median Prices
st.subheader("Heatmap: Median Price by State & City")
heatmap_data = df.pivot_table(values="Price_in_Lakhs", index="State", columns="City", aggfunc="median")
plt.figure(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap='coolwarm', annot=True)
plt.title("Heatmap: State × City Median Prices")
st.pyplot(plt)

# Median Price by BHK Trend
st.subheader("Median Price by BHK")
median_price_by_bhk = df.groupby("BHK")["Price_in_Lakhs"].median()

plt.figure(figsize=(6, 4))
plt.plot(median_price_by_bhk.index, median_price_by_bhk.values, marker='o')
plt.title("Median Price by BHK")
plt.xlabel("BHK")
plt.ylabel("Median Price (Lakhs)")
plt.grid(True)
st.pyplot(plt)


# Outlier Detection for Price
st.subheader("Outlier Detection for Price")
q1 = df["Price_in_Lakhs"].quantile(0.25)
q3 = df["Price_in_Lakhs"].quantile(0.75)
iqr = q3 - q1
upper_limit = q3 + 1.5 * iqr
outliers = df[df["Price_in_Lakhs"] > upper_limit]
st.write("Outliers (Highest Prices):", outliers[["Price_in_Lakhs", "City", "State"]].head(10))


# Future Price Prediction
st.sidebar.header("Visual Insights -")
st.sidebar.subheader("Future Price Predictor")
current_price = st.sidebar.number_input("Current Price (Lakhs)", min_value=0)
growth_rate = st.sidebar.number_input("Expected Annual Growth Rate (%)", min_value=0.0, max_value=100.0, value=8.0)
years = st.sidebar.number_input("Number of Years to Project", min_value=1, max_value=30, value=5)

st.write("<h2 style ='color:Yellow;'>📌 Investment Analysis</h2>",unsafe_allow_html=True)

# Calculate Future Price
if current_price > 0:
    future_price = current_price * ((1 + (growth_rate / 100)) ** years)
    st.subheader(f"Estimated Price after {years} Years: {future_price:.2f} Lakhs")
    

# Investment Classification
st.sidebar.header("Investment Analysis")
price_per_sqft = st.sidebar.number_input("Price per SqFt", min_value=0.0)
median_price = df["Price_per_SqFt"].median()

if price_per_sqft <= median_price:
    investment_status = "Good Investment"
else:
    investment_status = "Not a Good Investment"

st.write(f"### Investment Status: <h style ='color:Green;'>{investment_status}</h>",unsafe_allow_html=True)

# Conclusion
st.write("<h6 style='color:Cyan;'>✔ EDA COMPLETED SUCCESSFULLY! Explore the insights and make informed decisions</h6>",unsafe_allow_html=True)


#********************************************************************************************

# Colored subheader using HTML
st.markdown(
    "<h3 style='color: Red;'>***Custom Evaluation Matrics (Calulator)***</h3>",
    unsafe_allow_html=True
)

# prepare dropdown options from cleaned df
state_options = ["--select--"] + sorted(df["State"].dropna().unique()) if "State" in df.columns else ["--select--"]
city_options = ["--select--"] + sorted(df["City"].dropna().unique()) if "City" in df.columns else ["--select--"]
bhk_options_eval = ["--select--"] + sorted(df["BHK"].dropna().astype(int).unique()) if "BHK" in df.columns else ["--select--"]

col_a, col_b, col_c = st.columns(3)
with col_a:
    eval_state = st.selectbox("State", state_options)
with col_b:
    eval_city = st.selectbox("City", city_options)
with col_c:
    eval_bhk = st.selectbox("BHK", bhk_options_eval)

col_d, col_e = st.columns(2)
with col_d:
    eval_size = st.number_input("Size (SqFt)", min_value=100, value=1000)
with col_e:
    eval_price = st.number_input("Current Price (Lakhs)", min_value=0.0, value=float(df["Price_in_Lakhs"].median()) if "Price_in_Lakhs" in df.columns else 50.0)

eval_parking = st.checkbox("Has Parking", value=False)
eval_avail = st.selectbox("Availability", ["available", "under construction", "resale", "sold"])

# growth rate input
st.write("Enter annual growth rate (decimal). Example: 0.08 for 8%")
growth_input = st.number_input("Annual growth rate", min_value=0.0, max_value=1.0, value=0.08, step=0.01)

if st.button("Evaluate"):
    # compute price per sqft
    pps = (eval_price * 100000) / eval_size if eval_size > 0 else np.nan
    # estimated future price
    future_price = eval_price * (1 + growth_input) ** 5
    # city median ppsqft for comparison
    if eval_city != "--select--" and "City" in df.columns:
        city_med_pps = df.loc[df["City"] == eval_city, "Price_per_SqFt"].median()
    else:
        city_med_pps = df["Price_per_SqFt"].median() if "Price_per_SqFt" in df.columns else np.nan

    # basic multi-factor scoring (very simple weights)
    score = 0.0
    total_w = 0.0
    # price per sqft vs city median (weight 0.4)
    total_w += 0.4
    if not np.isnan(pps) and not np.isnan(city_med_pps):
        if pps <= city_med_pps:
            score += 0.4
        else:
            # partial credit if within 10%
            diff = (pps - city_med_pps) / city_med_pps
            if diff < 0.1:
                score += 0.2
    # BHK (weight 0.15)
    total_w += 0.15
    try:
        if int(eval_bhk) >= 3:
            score += 0.15
    except:
        pass
    # availability (weight 0.15)
    total_w += 0.15
    if str(eval_avail).lower() in ["available", "ready", "resale"]:
        score += 0.15
    # parking (weight 0.1)
    total_w += 0.1
    if eval_parking:
        score += 0.05
    # price vs city average (weight 0.2)
    total_w += 0.2
    city_avg_price = df.loc[df["City"] == eval_city, "Price_in_Lakhs"].median() if (eval_city != "--select--" and "City" in df.columns) else df["Price_in_Lakhs"].median() if "Price_in_Lakhs" in df.columns else np.nan
    if not np.isnan(city_avg_price) and eval_price <= city_avg_price:
        score += 0.2

    invest_pct = (score / total_w) * 100 if total_w > 0 else 50.0
    invest_label = "GOOD INVESTMENT" if invest_pct >= 50 else "NOT GOOD"

    # confidence: simple rule - closeness to city median PPSQFT
    if not np.isnan(city_med_pps) and city_med_pps > 0:
        conf = 1 - min(abs(pps - city_med_pps) / city_med_pps, 1.0)
        conf_pct = round(conf * 100, 1)
    else:
        conf_pct = 60.0

    st.markdown("### Evaluation Result")
    st.write(f"- **Price per SqFt:** {round(pps,2) if not np.isnan(pps) else 'N/A'}")
    st.write(f"- **City median Price per SqFt:** {round(city_med_pps,2) if not np.isnan(city_med_pps) else 'N/A'}")
    st.write(f"- **Estimated Future Price (5 yrs at {growth_input*100:.1f}% p.a.):** **{round(future_price,2)} Lakhs**")
    st.write(f"- **Investment Score:** {round(invest_pct,1)}% → **{invest_label}**")
    st.write(f"- **Classification confidence :** {conf_pct}%")

    # Simple feature importance by absolute correlation to Price_per_SqFt (rule-based)
    st.markdown("#### Feature importance (corr with Price_per_SqFt)")
    if "Price_per_SqFt" in df.columns:
        corrs = {}
        for col in ["Size_in_SqFt", "BHK", "Nearby_Schools", "Has_Parking", "Price_in_Lakhs"]:
            if col in df.columns:
                try:
                    corr = abs(df[col].corr(df["Price_per_SqFt"]))
                    corrs[col] = round(corr, 3) if not np.isnan(corr) else 0
                except:
                    corrs[col] = 0
        st.json(corrs)
    else:
        st.info("Price_per_SqFt not in dataset — feature importance not available.")

st.markdown("---")