import streamlit as st
import pandas as pd
import os
import gspread
from google.oauth2.service_account import Credentials

# --- PAGE SETUP ---
st.set_page_config(page_title="The PowerPath Index", page_icon="⚡")

# --- HEADER ---
st.title("⚡ The PowerPath Index™")
st.subheader("Project Intake Form")
st.markdown("---")

# --- OPTIONAL LOGO ---
# st.image("powerpath_logo.png", width=200)

# --- PROPERTY INFORMATION ---
st.markdown("## 📋 Property Information")

property_name = st.text_input("Property Name *", placeholder="e.g., Austin Data Center Site")
property_id = st.text_input("Property ID *", placeholder="e.g., PROP-001")
evaluator_name = st.text_input("Evaluator Name *", placeholder="Your name")
location = st.text_input("Location/State *", placeholder="e.g., Austin,*_
