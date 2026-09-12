# Tiller — Analytics → Product

A product analytics project using historical Tiller POS data to identify a high-value business opportunity and translate the analytical findings into a product opportunity for decision support.

> **Project status: Complete — Analytics handover to Product**

---

## Overview

This project explores how Tiller's POS data could be used to provide more useful analytical insights and decision support to business customers.

The work followed an end-to-end path from **business context → data understanding → opportunity identification → focused analysis → product handover**.

The final focus was **short-term store-level demand forecasting**.

### Business question

> **Can Tiller forecast weekly store-level demand 1–2 weeks ahead using historical patterns?**

---

## Project Journey

| Phase                                | Focus                                                                | Outcome                                                                  |
| ------------------------------------ | -------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **Phase 1 — Business Context**       | Understand the business problem and define the analytical direction  | Established the opportunity around data-driven customer decision support |
| **Phase 2 — Data Understanding**     | Assess data quality, structure, behaviour and analytical feasibility | Identified several credible product opportunities                        |
| **Phase 3 — Opportunity Definition** | Compare opportunities and investigate the strongest candidate        | Selected demand forecasting for focused analysis                         |
| **Product Handover**                 | Translate analytical findings into a product opportunity             | Defined a store-level forecasting and reliability concept                |

---

## Key Findings

The analysis found that historical demand contains meaningful predictive signal at the store level.

The main findings were:

* **Recent demand is predictive:** previous-week demand provided a strong baseline for forecasting one week ahead.
* **Simple approaches performed well:** more complex forecasting approaches did not consistently improve accuracy enough to justify their additional complexity.
* **Calendar effects were mixed:** calendar information improved forecasts for most stores but did not improve the pooled result.
* **Store volume matters:** higher-volume stores were generally somewhat easier to forecast, although volume alone did not explain forecastability.
* **Trend-aware forecasting did not improve performance:** incorporating short-term trend information made forecasts less accurate in this dataset.
* **Forecast reliability varies:** periods of sudden demand change were substantially harder to forecast, indicating that a forecast should be accompanied by contextual information about its reliability.

### Overall conclusion

The analysis supports a product opportunity around **simple short-term demand forecasting combined with a reliability/context signal**, rather than a complex forecasting model.

---

## Product Opportunity

The analytical work translates into a potential decision-support capability for Tiller customers:

**Expected demand → Store context → Reliability signal → Better-informed decision**

The opportunity is not simply to provide a forecast number, but to help a business understand:

* what demand is likely to look like in the near term;
* how reliable that forecast is;
* when recent demand behaviour is unusually unstable.

This creates a potential foundation for operational and commercial planning decisions.

---

## Data

The analysis used historical Tiller POS data covering **2015–2020**, including:

* **1.28M orders**
* **3.92M order lines**
* **1.40M payments**
* **21 stores**
* **12K+ products**

The analysis considered transaction, product, payment, store and temporal information.

The dataset reflects historical Tiller activity and therefore should be understood as an analytical case study rather than a representation of current SumUp production data.

---

## Repository Structure

```text
tiller/
├── charts/
│   ├── 02_data_understanding/
│   ├── 03_demand_forecasting/
│   └── 03_opportunity_definition/
│
├── data/
│
├── notebooks/
│   ├── 02_eda_complete.ipynb
│   ├── 03_question_selection.ipynb
│   └── 03b_demand_forecasting.ipynb
│
├── presentations/
│   ├── Tiller_Phase2_Opportunity_Exploration.pdf
│   └── Tiller_Phase_3__10-Minute_Presentation.pdf
│
└── README.md
```

### Where to start

**For the overall analytical story**

→ `notebooks/02_eda_complete.ipynb`

**For opportunity selection**

→ `notebooks/03_question_selection.ipynb`

**For the final demand forecasting analysis**

→ `notebooks/03b_demand_forecasting.ipynb`

**For the executive presentation**

→ `presentations/Tiller_Phase_3__10-Minute_Presentation.pdf`

**For the earlier opportunity exploration**

→ `presentations/Tiller_Phase2_Opportunity_Exploration.pdf`

---

## Final Handover

This repository represents the completed **Analytics workstream**.

The output of the work is a defined product opportunity supported by the available data:

> **Short-term store-level demand forecasting with contextual reliability information.**

The analytical work ends at this handover point. Product discovery, customer validation, workflow design and subsequent product development are outside the scope of this repository.
