# Tiller Restaurant Analytics

Data Analytics project analyzing transaction data from Tiller (by SumUp).

## Project Structure

- `docs/` - Documentation and analysis artifacts
  - `phase_2_eda/` - Phase 2.5 Exploratory Data Analysis
    - [Notebook](./docs/phase_2_eda/phase_2_exploratory_analysis.ipynb)
    - [Charts](./docs/phase_2_eda/)

## Phase 2: Data Understanding & Feasibility

### 2.5 Exploratory Data Analysis

[View Notebook](./docs/phase_2_eda/phase_2_exploratory_analysis.ipynb)

**Key Findings:**
- Store 4151 represents 68% of orders but has lowest AOV (€7.03)
- Clear temporal patterns (weekly, hourly)
- Strong transaction economics: more items/customers → higher AOV
- CARD (52%) and CASH (44%) dominate payments
- 20%+ financial anomalies (negative values)

## Dataset

- **BigQuery:** `le-wagon-da-502302.tiller`
- **Tables:** order_data, order_line, payment_data, store_data
- **Records:** 1.28M orders, 3.92M order lines, 1.40M payments
- **Period:** Oct 2015 – Nov 2020
