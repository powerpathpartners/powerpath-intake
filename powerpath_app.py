import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="The PowerPath Index", page_icon="⚡", layout="wide")

# --- GLOBAL STYLES ---
st.markdown("""
    <style>
        /* Center all headers and reduce default padding */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            max-width: 1200px;
            margin: auto;
        }
        h1, h2, h3 {
            text-align: center !important;
        }
        /* Increase font sizes */
        .main-title {
            font-size: 350% !important;
            margin-bottom: 0;
        }
        .sub-title {
            font-size: 350% !important;
            font-weight: 400;
            margin-top: 0.3rem;
            margin-bottom: 1.5rem;
        }
        /* Adjust logo spacing */
        .logo-container img {
            margin-top: 0.5in;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 160px;
        }
        /* Style submit button */
        div.stButton > button {
            background-color: #0052cc;
            color: white;
            border-radius: 8px;
            height: 3em;
            font-size: 16px;
            font-weight: 600;
            border: none;
        }
        div.stButton > button:hover {
            background-color: #003d99;
            transition: 0.2s;
        }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="logo-container">
        <img src="PPP logo transparent bg.png" alt="PowerPath Logo">
    </div>
    <h1 class="main-title">The PowerPath Index</h1>
    <h3 class="sub-title">Project Intake Form</h3>
""", unsafe_allow_html=True)

st.markdown("---")

# --- FORM ---
st.header("Project Information")

with st.form("project_form"):
    col1, col2 = st.columns(2)
    with col1:
        project_name = st.text_input("Project Name")
        location = st.text_input("Location (City, State)")
        acreage = st.number_input("Acreage", min_value=0.0, step=0.1)
        owner = st.text_input("Owner/Developer")

    with col2:
        capacity = st.text_input("Planned Capacity (MW)")
        utility = st.text_input("Utility or Co-op")
        interconnect_status = st.selectbox(
            "Interconnect Status",
            ["Not Started", "In Progress", "Approved", "Operational"]
        )
        has_substation = st.radio("Substation Onsite?", ["Yes", "No"])

    st.markdown("---")
    st.header("Power & Energy Details")

    col3, col4 = st.columns(2)
    with col3:
        primary_power_source = st.text_input("Primary Power Source (e.g., Grid, Solar, Gas, BTM)")
        secondary_source = st.text_input("Secondary Power Source (if any)")
        total_capacity = st.text_input("Total Available Capacity (MW)")
    with col4:
        renewable_mix = st.slider("Renewable Energy %", 0, 100, 50)
        grid_tie = st.text_input("Grid Tie Voltage (kV)")
        microgrid_ready = st.radio("Microgrid-Ready?", ["Yes", "No"])

    st.markdown("---")
    st.header("Development & Leasing Details")

    col5, col6 = st.columns(2)
    with col5:
        permitting = st.text_input("Permitting Status")
        site_control = st.selectbox("Site Control", ["Owned", "LOI", "Option", "None"])
    with col6:
        leasing_status = st.selectbox(
            "Leasing Status",
            ["Not Marketed", "In Discussion", "LOI Signed", "Leased"]
        )
        target_tenants = st.text_area("Target Tenants / Hyperscalers")

    st.markdown("---")
    submitted = st.form_submit_button("Submit Project")

if submitted:
    st.success(f"✅ Project '{project_name}' submitted successfully!")
    st.write("**Summary:**")
    st.json({
        "Project Name": project_name,
        "Location": location,
        "Acreage": acreage,
        "Owner/Developer": owner,
        "Capacity (MW)": capacity,
        "Utility/Co-op": utility,
        "Interconnect Status": interconnect_status,
        "Substation Onsite": has_substation,
        "Primary Power Source": primary_power_source,
        "Secondary Power Source": secondary_source,
        "Total Capacity": total_capacity,
        "Renewable Mix %": renewable_mix,
        "Grid Tie Voltage": grid_tie,
        "Microgrid Ready": microgrid_ready,
        "Permitting Status": permitting,
        "Site Control": site_control,
        "Leasing Status": leasing_status,
        "Target Tenants": target_tenants
    })
