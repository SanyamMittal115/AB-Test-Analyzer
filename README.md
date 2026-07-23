# 📊 A/B Test Analyzer & AI Decision Copilot

An end-to-end statistical engine and AI-assisted decision-support platform built to bridge the gap between experimental data and product deployment strategies.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/) 

---

## 🎯 Why This Project Matters

Product Managers and Growth Teams frequently run A/B tests, but translating statistical metrics ($p$-values, variance, relative lift) into crisp, executive-ready deployment decisions often leads to bottlenecks or high-risk launches.

This platform automates statistical hypothesis testing, enforces sample-size health checks, generates plain-English **Ship / Kill / Hold** recommendations, and leverages an LLM Copilot to output strategic post-experiment next steps.

---

## ✨ Key Features

* **📊 Automated Statistical Testing:** Executes Chi-Square tests of independence ($\chi^2$) to evaluate conversion rates across Control and Variant groups.
* **🛡️ Guardrail Engine:** Automatically flags underpowered tests when sample sizes fall below defined statistical thresholds to prevent Type I and Type II errors.
* **📝 Dynamic Decision Memos:** Generates color-coded, plain-English executive summaries (`🚀 Ship It`, `❌ Kill It`, `⏹️ Do Not Ship`, `⚠️ Inconclusive`).
* **📈 Interactive Plotly Visualizations:** Clear conversion rate comparisons and experiment diagnostic tables.
* **🤖 AI Product Manager Copilot:** Powered by OpenAI (`gpt-3.5-turbo`), this module analyzes experiment nuances to generate strategic follow-up roadmaps (qualitative research, cohort segmentation, or rollout strategies). *Includes a built-in zero-cost fallback demo mode.*
* **📁 Flexible Data Ingestion:** Test immediately with built-in synthetic user simulations or upload custom event logs via CSV.

---

## 📂 Expected CSV File Format

If uploading a custom CSV file, your data should follow this structure:

| Column Name | Type | Description |
| :--- | :--- | :--- |
| `user_id` | String | Unique user or session identifier |
| `group` | String | Experiment assignment (`Control` or `Variant`) |
| `converted` | Integer | Binary conversion outcome (`1` for success, `0` for no action) |

---

## 🛠️ Tech Stack & Architecture

* **Frontend & Framework:** Streamlit
* **Data Processing & Stats:** Pandas, NumPy, SciPy (Chi-Square contingency testing)
* **Data Visualization:** Plotly Express
* **AI / LLM Integration:** OpenAI API (`gpt-3.5-turbo`)

---

## 🚀 Quickstart & Local Setup

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/ab-test-analyzer.git](https://github.com/YOUR_GITHUB_USERNAME/ab-test-analyzer.git)
cd ab-test-analyzer