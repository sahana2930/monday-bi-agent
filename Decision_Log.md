Skylark Drones – Decision Log

Project: Monday.com Business Intelligence Agent

1. Key Assumptions

The Deals and Work Orders boards may contain inconsistent column names and formats.

Probability values may be stored either as numeric percentages or as text labels (High/Medium/Low).

Founder-level queries are high-level business questions rather than technical queries.

Boards may contain missing values, blank rows, improperly formatted numbers, or inconsistent date formats.

The solution must remain read-only and should not modify monday.com data.

2. Architecture & Design Decisions
API Integration

Used monday.com GraphQL API for direct and flexible data access.

Implemented authentication validation before processing any data.

Used dynamic column mapping (column ID → column title) to handle schema changes.

Avoided hardcoding column names to increase resilience.

Data Cleaning Strategy

To handle messy real-world data:

Normalized column names to lowercase.

Removed formatting characters (₹, commas, percentage symbols).

Converted numeric fields safely using errors="coerce".

Dynamically parsed date columns.

Dropped fully empty rows.

Replaced missing values with safe defaults.

Ensured system does not fail even if expected columns are missing.

This ensures data resilience and graceful degradation.

Query Engine Design

Implemented rule-based NLP using keyword intent detection.

Supported multi-intent queries (e.g., pipeline + forecast in one question).

Structured responses in executive-friendly bullet format.

Designed responses to provide insight, not just raw numbers.

Due to time constraints (6-hour limit), a full LLM-based parser was not implemented.

Business Intelligence Layer

Implemented the following business metrics:

Total Pipeline

Weighted Forecast

Sector Performance

Quarter Performance

Risk Concentration

Leadership Executive Summary

Work Order Count

Pipeline per Work Order (cross-board intelligence)

The agent combines Deals and Work Orders data to provide operational context.

3. Trade-offs

Chose rule-based NLP instead of LLM-based parsing to avoid external AI dependency and cost.

Simplified pagination handling for large boards.

Prioritized reliability and data cleaning over UI enhancements.

Focused on backend intelligence rather than advanced visualizations.

4. Interpretation of “Leadership Updates”

I interpreted “leadership updates” as a concise executive snapshot including:

Total Pipeline

Weighted Forecast

Active Deals

Work Order Volume

Sector Distribution

Risk Exposure

Pipeline per Work Order

This provides a board-ready summary suitable for founders and executives.

5. Improvements with More Time

If extended development time were available, I would:

Integrate an LLM-based semantic intent parser.

Add predictive revenue forecasting.

Implement caching for performance optimization.

Add visual KPI dashboards and charts.

Support full pagination for large boards.

Build deeper cross-board relationship modeling (Deal → Execution tracking).