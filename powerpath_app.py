import streamlit as st
import pandas as pd
import gspread
from datetime import datetime
from gspread_dataframe import set_with_dataframe

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="PowerPath Intake", layout="wide")

# ---------- STYLE ----------
st.markdown("""
    <style>
        body { background-color: #f6f8fa; color: #222; }
        .block-container { padding-top: 1rem; padding-bottom: 2rem; }
        h1, h2, h3 { color: #044874 !important; }
        div[data-testid="stExpanderHeader"] { background-color: #04487410; font-weight:600; }
    </style>
""", unsafe_allow_html=True)

# ---------- LOAD SHEET ----------
SHEET_URL = "https://docs.google.com/spreadsheets/d/1_K7AOyKjzdwfqM7V9x6FxJYkVz-OSB5nNKbZtygLsak/export?format=csv"
SHEET_NAME = "PowerPath Project Intake Form (Responses)"
SUBMISSION_TAB = "Submissions"

try:
    df = pd.read_csv(SHEET_URL)
except Exception as e:
    st.error("❌ Could not load the Google Sheet. Make sure link sharing is set to 'Anyone with the link → Viewer'.")
    st.stop()

# --- normalize headers and clean up ---
df.columns = df.columns.str.strip().str.lower()
df = df.dropna(axis=1, how='all')
expected_cols = ["question category","subcategory_code","question","answer_type","priority","weight"]
df = df[[c for c in expected_cols if c in df.columns]]

# ---------- HEADER ----------
st.title("⚡ PowerPath Project Intake Form")
st.caption("Assess and score potential data center development opportunities using PowerPath’s weighted readiness model.")

# ---------- BASIC INFO ----------
project_name = st.text_input("Project Name")
submitted_by = st.text_input("Submitted By")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

st.markdown("---")

# ---------- BUILD FORM ----------
answers = {}
scores = {}
category_scores = {}

categories = df["question category"].unique()

for cat in categories:
    with st.expander(cat, expanded=False):
        subset = df[df["question category"] == cat]
        total_cat_weight = subset["weight"].sum()
        cat_score = 0

        for _, row in subset.iterrows():
            q_code = row["subcategory_code"]
            q_text = row["question"]
            q_type = str(row["answer_type"]).strip().lower()
            weight = float(row.get("weight", 1))

            default = str(row.get("answer", "")) if "answer" in df.columns else ""

            if "yes/no" in q_type:
                ans = st.radio(q_text, ["Yes", "No"], key=q_code, index=0 if default.lower() == "yes" else 1)
                score = weight if ans == "Yes" else 0
            elif "date" in q_type:
                ans = st.date_input(q_text, key=q_code)
                score = weight if ans else 0
            elif "numeric" in q_type:
                ans = st.number_input(q_text, key=q_code)
                score = weight if ans else 0
            else:
                ans = st.text_input(q_text, key=q_code, value=default)
                score = weight if ans else 0

            answers[q_code] = ans
            scores[q_code] = score
            cat_score += score

        pct = (cat_score / total_cat_weight) * 100 if total_cat_weight > 0 else 0
        category_scores[cat] = pct

        color = "🟩" if pct >= 75 else "🟨" if pct >= 50 else "🟥"
        st.write(f"**{color} {cat} Score: {pct:.1f}%**")

st.markdown("---")

# ---------- TOTAL SCORE ----------
total_score = sum(scores.values())
max_score = df["weight"].sum()
index_pct = round((total_score / max_score) * 100, 1)
tier = (
    "Tier 1 – Hyperscale Ready" if index_pct >= 75 else
    "Tier 2 – Advanced Development" if index_pct >= 50 else
    "Tier 3 – Viable with Conditions" if index_pct >= 25 else
    "Tier 4 – Early Stage"
)

st.header("📊 PowerPath Index Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Weighted Score", f"{total_score:.1f}")
col2.metric("PowerPath Index", f"{index_pct}%")
col3.metric("Readiness Tier", tier)

# ---------- CATEGORY SCORE VISUALS ----------
st.markdown("### Category Breakdown")
for cat, pct in category_scores.items():
    color = "#00b050" if pct >= 75 else "#ffc000" if pct >= 50 else "#c00000"
    st.progress(pct / 100)
    st.write(f"**{cat}** — {pct:.1f}%")

# ---------- SAVE ----------
st.markdown("---")
st.subheader("Save Submission")

if st.button("💾 Save Results to Sheet"):
    try:
        gc = gspread.service_account_from_dict({
            "type": "service_account",
            "project_id": "powerpath-intake",
            "private_key_id": "",
            "private_key": "",
            "client_email": "",
            "client_id": "",
            "token_uri": "https://oauth2.googleapis.com/token",
        })
        sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1_K7AOyKjzdwfqM7V9x6FxJYkVz-OSB5nNKbZtygLsak")
        try:
            ws = sh.worksheet(SUBMISSION_TAB)
        except:
            ws = sh.add_worksheet(title=SUBMISSION_TAB, rows="100", cols="20")

        data = {
            "Timestamp": [timestamp],
            "Project Name": [project_name],
            "Submitted By": [submitted_by],
            "PowerPath Index": [index_pct],
            "Tier": [tier],
            "Total Score": [total_score],
        }
        for cat, pct in category_scores.items():
            data[cat] = [pct]

        df_submit = pd.DataFrame(data)
        existing = pd.DataFrame(ws.get_all_records())
        combined = pd.concat([existing, df_submit], ignore_index=True)
        ws.clear()
        set_with_dataframe(ws, combined)

        st.success(f"✅ Submission saved for project: {project_name}")
    except Exception as e:
        st.error("⚠️ Could not write to Google Sheet. (Public access mode only reads — full save requires API key setup.)")
