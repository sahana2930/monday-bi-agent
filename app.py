import streamlit as st
import pandas as pd
import requests

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="AI Business Intelligence Agent",
    layout="wide"
)

st.title("AI Business Intelligence Agent (Live monday.com)")

# ==========================================================
# MONDAY API CONFIGURATION
# ==========================================================

API_TOKEN = "ABC"  # Replace with your token
API_URL = "https://api.monday.com/v2"

HEADERS = {
    "Authorization": API_TOKEN,
    "Content-Type": "application/json"
}

DEALS_BOARD_ID = 5026841268
WORK_ORDERS_BOARD_ID = 5026841696

# ==========================================================
# AUTHENTICATION CHECK
# ==========================================================

def check_auth():
    query = """ query { me { id name } } """
    response = requests.post(API_URL, json={"query": query}, headers=HEADERS)
    return response.json()

auth_response = check_auth()

if "data" not in auth_response:
    st.error("Authentication Failed. Check API Token.")
    st.stop()

# ==========================================================
# FETCH BOARD DATA
# ==========================================================

def fetch_board(board_id):

    query = f"""
    query {{
        boards(ids: {board_id}) {{
            columns {{
                id
                title
            }}
            items_page {{
                items {{
                    name
                    column_values {{
                        id
                        text
                    }}
                }}
            }}
        }}
    }}
    """

    response = requests.post(API_URL, json={"query": query}, headers=HEADERS)
    result = response.json()

    if "data" not in result:
        st.error("Board Fetch Failed.")
        st.stop()

    board = result["data"]["boards"][0]
    column_map = {col["id"]: col["title"].lower() for col in board["columns"]}

    rows = []

    for item in board["items_page"]["items"]:
        row = {"item": item["name"]}

        for col in item["column_values"]:
            column_title = column_map.get(col["id"], col["id"])
            row[column_title] = col["text"]

        rows.append(row)

    return pd.DataFrame(rows)

# ==========================================================
# LOAD LIVE DATA
# ==========================================================

with st.spinner("Loading Deals Board..."):
    deals_df = fetch_board(DEALS_BOARD_ID)

with st.spinner("Loading Work Orders Board..."):
    work_orders_df = fetch_board(WORK_ORDERS_BOARD_ID)

# ==========================================================
# DATA CLEANING FUNCTION
# ==========================================================

def clean_dataframe(df):

    df.columns = df.columns.str.strip().str.lower()
    df.dropna(how="all", inplace=True)

    for col in df.columns:

        df[col] = df[col].astype(str).str.strip()

        # Clean numeric fields
        if any(keyword in col for keyword in ["value", "amount"]):
            df[col] = (
                df[col]
                .str.replace(",", "", regex=False)
                .str.replace("₹", "", regex=False)
                .str.replace("%", "", regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Clean date fields
        if "date" in col:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    df.fillna(0, inplace=True)

    return df

deals_df = clean_dataframe(deals_df)
work_orders_df = clean_dataframe(work_orders_df)

# ==========================================================
# METRICS ENGINE
# ==========================================================

# Detect Deal Value Column
deal_value_col = next(
    (c for c in deals_df.columns if "deal" in c and "value" in c),
    None
)

if not deal_value_col:
    deal_value_col = next(
        (c for c in deals_df.columns if "value" in c),
        None
    )

total_pipeline = deals_df[deal_value_col].sum() if deal_value_col else 0

# Detect Probability Column
prob_col = next((c for c in deals_df.columns if "prob" in c), None)

weighted_forecast = 0

if deal_value_col and prob_col:

    deals_df["prob_numeric"] = pd.to_numeric(deals_df[prob_col], errors="coerce")

    probability_map = {
        "high": 80,
        "medium": 50,
        "low": 20
    }

    mask = deals_df["prob_numeric"].isna()

    deals_df.loc[mask, "prob_numeric"] = (
        deals_df.loc[mask, prob_col]
        .astype(str)
        .str.lower()
        .map(probability_map)
    )

    deals_df["weighted"] = (
        deals_df[deal_value_col] *
        deals_df["prob_numeric"] / 100
    )

    weighted_forecast = deals_df["weighted"].sum()

total_work_orders = len(work_orders_df)

# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================

col1, col2, col3 = st.columns(3)

col1.metric("Total Pipeline", round(total_pipeline, 2))
col2.metric("Weighted Forecast", round(weighted_forecast, 2))
col3.metric("Total Work Orders", total_work_orders)

# ==========================================================
# ADVANCED RULE-BASED AI CHATBOT
# ==========================================================

st.divider()
st.subheader("AI Business Intelligence Assistant")

question = st.text_input("Ask a business question")

if question:

    q = question.lower()
    response = []

    # Intent Detection
    metric_pipeline = any(w in q for w in ["pipeline", "revenue", "deal value"])
    metric_forecast = any(w in q for w in ["forecast", "expected"])
    metric_sector = any(w in q for w in ["sector", "industry"])
    metric_quarter = "quarter" in q
    metric_risk = any(w in q for w in ["risk", "exposure"])
    metric_leadership = any(w in q for w in ["leadership", "summary", "board"])

    # PIPELINE
    if metric_pipeline:
        response.append("Pipeline Overview")
        response.append(f"- Total Pipeline: ₹{round(total_pipeline, 2)}")
        response.append(f"- Active Deals: {len(deals_df)}")

    # FORECAST
    if metric_forecast:
        response.append("Forecast Analysis")
        response.append(f"- Weighted Forecast: ₹{round(weighted_forecast, 2)}")

    # SECTOR ANALYSIS
    if metric_sector and deal_value_col:
        industry_col = next(
            (c for c in deals_df.columns if "industry" in c or "sector" in c),
            None
        )

        if industry_col:
            sector_summary = (
                deals_df.groupby(industry_col)[deal_value_col]
                .sum()
                .sort_values(ascending=False)
            )

            response.append("Sector Breakdown")

            for sector, value in sector_summary.head(5).items():
                response.append(f"- {sector}: ₹{round(value, 2)}")

    # QUARTER ANALYSIS
    if metric_quarter and deal_value_col:
        date_col = next((c for c in deals_df.columns if "date" in c), None)

        if date_col:
            current_q = pd.Timestamp.now().quarter
            filtered = deals_df[deals_df[date_col].dt.quarter == current_q]

            response.append("Current Quarter Performance")
            response.append(
                f"- Pipeline This Quarter: ₹{round(filtered[deal_value_col].sum(), 2)}"
            )

    # RISK ANALYSIS
    if metric_risk and deal_value_col:
        industry_col = next(
            (c for c in deals_df.columns if "industry" in c or "sector" in c),
            None
        )

        if industry_col:
            sector_summary = deals_df.groupby(industry_col)[deal_value_col].sum()
            total = sector_summary.sum()

            if total > 0:
                concentration = (sector_summary.max() / total) * 100
                dominant_sector = sector_summary.idxmax()

                response.append("Risk Exposure Analysis")
                response.append(f"- Highest Exposure: {dominant_sector}")
                response.append(f"- Concentration Risk: {round(concentration, 2)}%")

    # LEADERSHIP SUMMARY
    if metric_leadership:
        response.append("Executive Snapshot")
        response.append(f"- Total Pipeline: ₹{round(total_pipeline, 2)}")
        response.append(f"- Weighted Forecast: ₹{round(weighted_forecast, 2)}")
        response.append(f"- Active Deals: {len(deals_df)}")
        response.append(f"- Total Work Orders: {total_work_orders}")

    # DEFAULT
    if not response:
        response.append(
            "I can assist with pipeline, forecast, sector analysis, quarter performance, risk exposure, or leadership summary."
        )


    st.markdown("\n".join(response))
