# Skylark Drones - Monday.com Business Intelligence Agent

## Project Overview

This project implements a live AI-powered Business Intelligence Agent that integrates directly with monday.com boards (Deals and Work Orders) using the monday.com GraphQL API.

The agent allows founders and executives to ask conversational business questions such as:

- What is the total pipeline?
- What is the weighted forecast?
- Show sector performance
- Show current quarter pipeline
- Give leadership summary

The system dynamically fetches real-time data from monday.com boards and performs cleaning, normalization, and business metric computation before generating responses.

---

## Architecture Overview

The system follows this flow:

Monday.com API  
↓  
GraphQL Data Fetch  
↓  
Data Cleaning & Normalization  
↓  
Business Metrics Engine  
↓  
Conversational Query Engine  
↓  
Streamlit Dashboard UI  

### Components

1. API Layer
   - Uses monday.com GraphQL API
   - Authenticated via Personal API Token
   - Fetches both Deals and Work Orders boards dynamically

2. Data Cleaning Layer
   - Normalizes column names
   - Converts numeric columns
   - Parses date columns
   - Handles missing values
   - Removes formatting symbols (₹, commas)

3. Metrics Layer
   - Total Pipeline
   - Weighted Forecast
   - Sector Performance
   - Quarter Pipeline
   - Leadership Summary
   - Work Order Counts

4. Query Engine
   - Interprets founder-level business questions
   - Matches keywords to business logic
   - Returns contextual responses

---

## How to Run Locally

1. Install dependencies:

pip install -r requirements.txt

2. Add your monday.com Personal API token inside the code:

API_TOKEN = "your_token_here"

3. Run the app:

streamlit run app.py

4. Open the browser link provided by Streamlit.

---

## How to Deploy (Streamlit Cloud)

1. Push project to GitHub
2. Go to https://streamlit.io/cloud
3. Connect repository
4. Add API token in Streamlit Secrets:

API_TOKEN = "your_token_here"

5. Replace in code:

API_TOKEN = st.secrets["API_TOKEN"]

---

## Configuration

### Board IDs

Inside app.py:

DEALS_BOARD_ID = your_deals_board_id  
WORK_ORDERS_BOARD_ID = your_work_orders_board_id  

You can find board ID from monday.com board URL.

---

## Data Resilience Features

- Handles missing/null values
- Cleans inconsistent numeric formats
- Parses date fields
- Detects missing probabilities
- Provides safe defaults when data incomplete

---

## Leadership Update Interpretation

The agent prepares leadership-ready summaries including:

- Pipeline snapshot
- Forecasted revenue
- Active deal count
- Operational workload (work orders)
- Sector distribution

---

## Future Improvements

- Add LLM-based NLP understanding
- Add predictive revenue modeling
- Add automated KPI dashboards
- Improve cross-board relationship mapping