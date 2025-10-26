import streamlit as st
import pandas as pd
import os
import gspread
from google.oauth2.service_account import Credentials

# --- PAGE SETUP ---
st.set_page_config(page_title="The PowerPath Index")

# --- HEADER ---
st.title("The PowerPath Index")
st.subheader("Project Intake Form")
st.write("---")

# --- PROPERTY INFORMATION ---
st.header("Property Information")

property_name = st.text_input("Property Name *", placeholder="e.g., Austin Data Center Site")
property_id = st.text_input("Property ID *", placeholder="e.g., PROP-001")
evaluator_name = st.text_input("Evaluator Name *", placeholder="Your name")
location = st.text_input("Location/State *", placeholder="e.g., Austin, Texas")

st.write("---")

# --- SITE METRICS ---
st.header("Site Metrics")

cost = st.number_input("Estimated Project Cost (in USD)", min_value=0.0, step=100000.0)
distance = st.number_input("Distance to Substation (in miles)", min_value=0.0, step=0.1)
power_capacity = st.number_input("Available Power Capacity (MW)", min_value=0.0, step=1.0)
renewable_pct = st.slider("Renewable Energy Availability (%)", 0, 100, 50)

# --- SCORE CALCULATION ---
score = (power_capacity * 2) + (100 - distance) + (renewable_pct / 2)
index = min(score / 2, 100)
tier = "Tier 1 – Prime" if index >= 80 else "Tier 2 – Viable" if index >= 60 else "Tier 3 – Developing"

# --- SUBMIT BUTTON ---
if st.button("Submit Evaluation"):
    if not property_name or not property_id or not evaluator_name or not location:
        st.warning("Please fill in all required fields before submitting.")
    else:
        data = {
            "Property Name": property_name,
            "Property ID": property_id,
            "Evaluator": evaluator_name,
            "Location": location,
            "Estimated Cost (USD)": cost,
            "Distance (miles)": distance,
            "Power Capacity (MW)": power_capacity,
            "Renewable (%)": renewable_pct,
            "PowerPath Index": round(index, 2),
            "Tier": tier
        }
        df = pd.DataFrame([data])

        # --- SAVE TO CSV ---
        csv_path = "submissions.csv"
        if os.path.exists(csv_path):
            df.to_csv(csv_path, mode="a", header=False, index=False)
        else:
            df.to_csv(csv_path, index=False)

        # --- SAVE TO GOOGLE SHEETS ---
        try:
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]
            creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
            client = gspread.authorize(creds)
            sheet = client.open("PowerPath Project Intake Form (Responses)").worksheet("submissions")
            sheet.append_row(list(data.values()))
            st.success("Submission saved to Google Sheets and CSV successfully!")
        except Exception as e:
            st.warning(f"CSV saved but Google Sheets upload failed: {e}")

# --- DISPLAY RESULTS ---
st.write("---")
st.header("Results")
st.metric(label="PowerPath Index", value=f"{index:.1f}")
st.metric(label="Readiness Tier", value=tier)

chart_df = pd.DataFrame({
    "Category": ["Power", "Distance", "Renewables"],
    "Score": [power_capacity * 2, 100 - distance, renewable_pct / 2]
}).set_index("Category")
st.bar_chart(chart_df)
