import streamlit as st
import pandas as pd

# --- PAGE SETUP ---
st.set_page_config(page_title="The PowerPath Index", page_icon="⚡", layout="wide")

# --- LOGO + HEADER ---
st.markdown(
    """
    <div style="text-align:center; margin-top: -10px; margin-bottom: -10px;">
        <img src="powerpath_logo.png" width="160" style="margin-top:0.5in;">
    </div>
    <h1 style="text-align:center; font-size:350%; margin-bottom:0;">
        The PowerPath Index
    </h1>
    <h3 style="text-align:center; font-size:350%; font-weight:normal; margin-top:5px;">
        Project Intake Form
    </h3>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# --- FORM SETUP ---
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
    st.write({
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
