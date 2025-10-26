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

# --- OPTIONAL LO
