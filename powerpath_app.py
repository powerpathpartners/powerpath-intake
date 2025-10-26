import streamlit as st

st.set_page_config(page_title="The PowerPath Index", layout="wide")

st.title("The PowerPath Index™")
st.subheader("Project Intake Form")

st.markdown("### Project Information")
col1, col2 = st.columns(2)
with col1:
    project_name = st.text_input("Project Name")
    location = st.text_input("Location (City, State)")
    acreage = st.number_input("Acreage", 0.0)
    owner = st.text_input("Owner/Developer")
with col2:
    capacity = st.text_input("Planned Capacity (MW)")
    utility = st.text_input("Utility or Co-op")
    interconnect = st.selectbox("Interconnect Status", ["Not Started", "In Progress", "Completed"])
    substation = st.radio("Substation Onsite?", ["Yes", "No"])

st.markdown("### Power & Energy Details")
col3, col4 = st.columns(2)
with col3:
    primary_power = st.text_input("Primary Power Source (e.g., Grid, Solar, Gas, BTM)")
    secondary_power = st.text_input("Secondary Power Source (if any)")
    total_capacity = st.text_input("Total Available Capacity (MW)")
with col4:
    renewable_pct = st.slider("Renewable Energy %", 0, 100, 0)
    grid_voltage = st.text_input("Grid Tie Voltage (kV)")
    microgrid_ready = st.radio("Microgrid-Ready?", ["Yes", "No"])

st.markdown("### Development & Leasing Details")
col5, col6 = st.columns(2)
with col5:
    permit_status = st.text_input("Permitting Status")
    site_control = st.selectbox("Site Control", ["Owned", "Optioned", "LOI", "In Negotiation"])
with col6:
    leasing_status = st.selectbox("Leasing Status", ["Not Marketed", "In Market", "LOI Signed", "Leased"])
    tenants = st.text_area("Target Tenants / Hyperscalers")
