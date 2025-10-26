import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime
from PIL import Image

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="The PowerPath Index", layout="wide")

# ---------- STYLE ----------
st.markdown("""
    <style>
        body { background-color: #f6f8fa; color: #222; }
        .block-container { padding-top: 1rem; padding-bottom: 2rem; }
        h1, h2, h3 { color: #044874 !important; }
        .title-text { font-size: 2.2rem; font-weight: 700; color: #044874; text-align: center; }
        .subtitle-text { font-size: 1.2rem; color: #444; text-align: center; margin-top: -0.3rem; }
        div[data-testid="stExpanderHeader"] {
            background-color: #04487410;
            font-weight: 600;
            color: #044874 !important;
        }
        .stButton>button {
            background-color: #044874 !important;
            color: white !important;
            font-weight: 600 !important;
            border-radius: 6px !important;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- LOGO & HEADER ----------
logo = Image.open("PPP logo transparent bg.png")
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
st.image(logo, width=160)
st.markdown("<div class='title-text'>The PowerPath Index™</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-text'>Project Intake Form</div><br>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------- LOAD GOOGLE SHEET ----------
SHEET_ID = "1_K7AOyKjzdwfqM7V9x6FxJYkVz-OSB5nNKbZtygLsak"
SHEET_NAME = "PowerPath Project Intake Form (Responses)"
encoded_name = urllib.parse.quote(SHEET_NAME)
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_name}"

@st.cache_data(ttl=300)
def load_data():
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip().str.lower()
    return df

df = load_data()

# ---------- FORM ----------
st.markdown("Use this tool to assess project readiness across key development categories. Responses auto-score against PowerPath benchmarks.")

responses = {}
categories = df["question category"].unique()

for category in categories:
    with st.expander(f"### {category}"):
        subset = df[df["question category"] == category]
        for _, row in subset.iterrows():
            q = row["question"]
            q_type = row["answer_type"].lower()
            key = row["subcategory_code"]

            if "yes/no" in q_type:
                responses[key] = st.radio(q, ["Yes", "No"], key=key)
            elif "numeric" in q_type:
                responses[key] = st.number_input(q, step=1.0, key=key)
            elif "date" in q_type:
                responses[key] = st.date_input(q, key=key)
            elif "text" in q_type:
                responses[key] = st.text_input(q, key=key)
            else:
                responses[key] = st.text_input(q, key=key)

# ---------- SUBMIT ----------
if st.button("Submit Intake"):
    st.success("✅ Intake submitted successfully!")
    st.session_state["responses"] = responses

# ---------- SCORING ----------
def score_response(row, responses):
    ans = responses.get(row["subcategory_code"], "")
    if "yes/no" in row["answer_type"].lower():
        return row["weight"] if ans == "Yes" else 0
    elif "numeric" in row["answer_type"].lower():
        try:
            val = float(ans)
            if val > 0:
                return min(row["weight"], row["weight"] * 0.75)
            else:
                return 0
        except:
            return 0
    elif "date" in row["answer_type"].lower():
        return row["weight"] * 0.8
    elif "text" in row["answer_type"].lower():
        return row["weight"] * 0.5 if ans.strip() else 0
    return 0

# ---------- RESULTS ----------
if "responses" in st.session_state:
    df["auto_score"] = df.apply(lambda r: score_response(r, st.session_state["responses"]), axis=1)
    total_weight = df["weight"].sum()
    total_score = df["auto_score"].sum()
    readiness = round((total_score / total_weight) * 100, 1)
    tier = (
        "Tier 1 – Hyperscale Ready" if readiness >= 85 else
        "Tier 2 – Advanced" if readiness >= 65 else
        "Tier 3 – Developing" if readiness >= 40 else
        "Tier 4 – Early Stage"
    )

    st.markdown("---")
    st.subheader("📊 PowerPath Index Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Weighted Score", f"{total_score:.1f}")
    col2.metric("PowerPath Index", f"{readiness}%")
    col3.metric("Readiness Tier", tier)

    st.markdown("#### Category Breakdown")
    cat_scores = df.groupby("question category")["auto_score"].sum() / df.groupby("question category")["weight"].sum() * 100
    st.bar_chart(cat_scores)

else:
    st.info("⬆️ Fill out the intake form above to calculate readiness and generate your PowerPath Index.")
