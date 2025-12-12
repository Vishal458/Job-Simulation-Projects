Real Estate Investment Advisor Project Report-------------------------------------------

This report summarizes:
• Step 1: Data Cleaning
• Step 2: EDA
• Rule-based feature creation
• Streamlit Dashboard Design

Dataset:
India Housing Prices (cleaned)

Key Processes:
• Duplicate removal
• Missing value treatment
• Numeric type conversion
• Price_per_SqFt and Age_of_Property creation
• Outlier detection using IQR
• Trend analysis and heatmaps

Problem Statement
Develop a machine learning application to assist potential investors in making real estate decisions. The system should:
1.	Classify whether a property is a "Good Investment" (Classification).
2.	Predict the estimated property price after 5 years (Regression).
Use the provided dataset to preprocess and analyze the data, engineer relevant features, and deploy a user-interactive application using Streamlit that provides investment recommendations and price forecasts. MLflow will be used for experiment tracking.

Business Use Cases
✅ Empower real estate investors with intelligent tools to assess long-term returns.
✅ Support buyers in choosing high-return properties in developing areas.
✅ Help real estate companies automate investment analysis for listings.
✅ Improve customer trust in real estate platforms with data-backed predictions.

Approach
🔹 Step 1: Data Preprocessing
●	Handle missing values and duplicates.

●	Normalize or scale numerical features.

●	Encode categorical features like Location and Property_Type.

●	Create new features like Price per Sqft, School Density Score, etc.
●	Create a binary label "Good Investment" based on domain rules (e.g., appreciation rate > threshold).

🔹 Step 2: Exploratory Data Analysis (EDA)
●	Price trends by city

●	Correlation between area and investment return

●	Impact of crime rate on good investment classification

●	Relationship between infrastructure score and resale value

🔹 Step 5: Streamlit App
●	A user-friendly form for entering property details, filtering out properties by area, price, BHK etc.

●	Show:

○	Classification: “Is this a Good Investment?”

○	Regression: “Estimated Price after 5 Years”

●	Add visual insights (e.g., location-wise heatmaps, trend charts)

●	Show model confidence scores & feature importance

