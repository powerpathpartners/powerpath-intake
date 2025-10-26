import streamlit as st
import pandas as pd
import os
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="The PowerPath Index")

# --- HEADER ---
st.title("⚡ The PowerPath Index™")
st.subheader("Project Intake Form")
st.markdown("---")

# --- PROPERTY INFORMATION ---
st.header("📋 Property Information")

property_name = st.text_input("Property Name *", placeholder="e.g., Austin Data Center Site")
property_id = st.text_input("Property ID *", placeholder="e.g., PROP-001")
evaluator_name = st.text_input("Evaluator Name *", placeholder="Your name")
location = st.text_input("Location/State *", placeholder="e.g., Austin, Texas")

st.divider()

# --- CATEGORY 1: POWER & INFRASTRUCTURE ---
st.header("⚙️ Power & Infrastructure")

grid_capacity = st.selectbox(
    "Available Grid Capacity (MW)",
    ["<50 MW", "50–150 MW", "150–300 MW", "300+ MW"]
)
distance_to_sub = st.number_input("Distance to Substation (in miles)", min_value=0.0, step=0.1)
onsite_gen = st.selectbox(
    "On-Site Generation or BTM Capability",
    ["None", "Planned", "Partial", "Full Microgrid / BESS"]
)

# --- CATEGORY 2: SITE READINESS ---
st.header("🏗️ Site Readiness")

zoning = st.selectbox(
    "Zoning & Permitting Status",
    ["Unzoned / Agricultural", "In Process", "Pre-approved", "Fully Permitted"]
)
access = st.selectbox(
    "Road / Utility Access",
    ["Limited / Dirt Road", "Improved Road", "Adjacent Highway", "Dual Access Routes"]
)
site_control = st.selectbox(
    "Site Control",
    ["LOI / Option Only", "Under Contract", "Owned", "JV / Long-Term Lease"]
)

# --- CATEGORY 3: ENERGY & ENVIRONMENT ---
st.header("🌿 Energy & Environment")

renewable_pct = st.slider("Renewable Energy Availability (%)", 0, 100, 50)
carbon_score = st.selectbox(
    "Carbon Intensity of Power Mix",
    ["High (>600 gCO₂/kWh)", "Moderate (400–600)", "Low (200–400)", "Very Low (<200)"]
)
water_availability = st.selectbox(
    "Water Availability",
    ["None", "Limited", "Adequate", "Abundant / Closed Loop"]
)

# --- CATEGORY 4: ECONOMICS ---
st.header("💰 Economics")

land_cost = st.number_input("Land Cost (in USD per acre)", min_value=0.0, step=1000.0)
dev_cost = st.number_input("Estimated Development Cost (in USD millions)", min_value=0.0, step=1.0)
tax_incentives = st.selectbox(
    "Tax Incentive Availability",
    ["None", "Local Only", "State + Local", "Federal + State + Local"]
)

# --- SCORING LOGIC ---
def score_dropdown(value, mapping):
    return mapping.get(value, 0)

# Simple mappings (adjust as needed)
grid_score = score_dropdown(grid_capacity, {
    "<50 MW": 25, "50–150 MW": 50, "150–300 MW": 75, "300+ MW": 100
})
onsite_score = score_dropdown(onsite_gen, {
    "None": 0, "Planned": 50, "Partial": 75, "Full Microgrid / BESS": 100
})
zoning_score = score_dropdown(zoning, {
    "Unzoned / Agricultural": 25, "In Process": 50, "Pre-approved": 75, "Fully Permitted": 100
})
access_score = score_dropdown(access, {
    "Limited / Dirt Road": 25, "Improved Road": 50, "Adjacent Highway": 75, "Dual Access Routes": 100
})
site_score = score_dropdown(site_control, {
    "LOI / Option Only": 25, "Under Contract": 50, "Owned": 75, "JV / Long-Term Lease": 100
})
carbon_score_val = score_dropdown(carbon_score, {
    "High (>600 gCO₂/kWh)": 25, "Moderate (400–600)": 50,
    "Low (200–400)": 75, "Very Low (<200)": 100
})
water_score = score_dropdown(water_availability, {
    "None": 25, "Limited": 50, "Adequate": 75, "Abundant / Closed Loop": 100
})
tax_score = score_dropdown(tax_incentives, {
    "None": 25, "Local Only": 50, "State + Local": 75, "Federal + State + Local": 100
})

# Derived metrics
distance_score = max(0, 100 - (distance_to_sub * 2))
renewable_score = renewable_pct

# Weighted average
total_score = (
    (grid_score * 0.15) +
    (onsite_score * 0.1) +
    (distance_score * 0.1) +
    (zoning_score * 0.1) +
    (access_score * 0.1) +
    (site_score * 0.1) +
    (renewable_score * 0.1) +
    (carbon_score_val * 0.1) +
    (water_score * 0.05) +
    (tax_score * 0.1)
)

index = round(total_score, 1)
if index >= 80:
    tier = "Tier 1 – Prime"
elif index >= 60:
    tier = "Tier 2 – Viable"
else:
    tier = "Tier 3 – Developing"

# --- SUBMIT ---
if st.button("Submit Evaluation"):
    if not property_name or not property_id or not evaluator_name or not location:
        st.warning("Please fill in all required fields before submitting.")
    else:
        data = {
            "Property Name": property_name,
            "Property ID": property_id,
            "Evaluator": evaluator_name,
            "Location": location,
            "Grid Capacity": grid_capacity,
            "Distance (miles)": distance_to_sub,
            "Onsite Generation": onsite_gen,
            "Zoning": zoning,
            "Access": access,
            "Site Control": site_control,
            "Renewable (%)": renewable_pct,
            "Carbon Score": carbon_score,
            "Water Availability": water_availability,
            "Land Cost (USD/acre)": land_cost,
            "Development Cost (USD M)": dev_cost,
            "Tax Incentives": tax_incentives,
            "PowerPath Index": index,
            "Tier": tier
        }
        df = pd.DataFrame([data])

        # Save to CSV
        csv_path = "submissions.csv"
        if os.path.exists(csv_path):
            df.to_csv(csv_path, mode="a", header=False, index=False)
        else:
            df.to_csv(csv_path, index=False)

        # Save to Google Sheets
        try:
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]
            creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
            client = gspread.authorize(creds)
            sheet = client.open("PowerPath Project Intake Form (Responses)").worksheet("submissions")
            sheet.append_row(list(data.values()))
            st.success("✅ Submission saved to Google Sheets and CSV successfully!")
        except Exception as e:
            st.warning(f"⚠️ CSV saved but Google Sheets upload failed: {e}")

# --- RESULTS ---
st.markdown("---")
st.header("Results")

st.metric("PowerPath Index", f"{index}")
st.metric("Readiness Tier", tier)

chart_data = pd.DataFrame({
    "Category": [
        "Power/Grid", "Onsite", "Distance", "Zoning", "Access",
        "Site Control", "Renewables", "Carbon", "Water", "Tax"
    ],
    "Score": [
        grid_score, onsite_score, distance_score, zoning_score,
        access_score, site_score, renewable_score, carbon_score_val,
        water_score, tax_score
    ]
}).set_index("Category")

st.bar_chart(chart_data)
