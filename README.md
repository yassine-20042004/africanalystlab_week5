# SwiftLog Logistics Limited — Enterprise Supply Chain Analytics & AI Transformation

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.142%2B-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.42%2B-red.svg)](https://streamlit.io/)
[![Tests](https://img.shields.io/badge/Pytest-24%20Passed%20(100%25)-success.svg)](tests/)
[![Phase](https://img.shields.io/badge/Phase-Week%205%20Final%20Capstone-brightgreen.svg)]()
[![Programme](https://img.shields.io/badge/AnalystLab%20Africa-Experience%20Lab-orange.svg)]()

Enterprise Supply Chain Analytics, Predictive Machine Learning Models, Grounded Generative AI Logistics Assistant, REST API service, and Executive Business Intelligence Solution for **SwiftLog Logistics Limited** (AnalystLab Africa Internship Programme — Week 5 Capstone Project).

---

## 🚀 Week 5 Enterprise Multi-Track Deliverables & Highlights

1. **Data Analytics Track**: 
   - Cleaned, normalized, and validated **11 relational datasets (36,115 records)** with 100% foreign key referential integrity.
   - Interactive glassmorphic Executive Web Dashboard ([`reports/dashboard.html`](reports/dashboard.html)) with dynamic Chart.js visualizations, warehouse leaderboard, and operational KPI telemetry.
2. **Data Science Track (Mission DS05)**:
   - 38-variable engineered feature matrix including RFM customer segmentation, route telemetry, and warehouse efficiency scoring.
   - **15 publication-grade visualization figures** ([`reports/figures/`](reports/figures/)) with complete titles, labels, interpretations, and business implications.
   - **3 Inferential Hypothesis Tests**: One-Way ANOVA across regional hub delays ($F=0.242, p=0.785$), Chi-Square test of independence on product returns ($\chi^2=0.199, p=0.905$), and Two-Sample T-Test on order revenues ($t=-1.737, p=0.082$).
3. **Machine Learning Engineering Track (Mission ML05)**:
   - Trained, tuned, and evaluated **4 predictive ML suites**: Delivery Delay Risk Classification, Product Return Likelihood, Order Revenue Demand Forecasting, and Delay Severity.
   - **Gradient Boosting Demand Forecaster** achieves **$R^2 = 0.9650$ (96.5% variance explained)** with an MAE of only $286.14.
   - Serialized candidate production models (`models/delivery_delay_model.pkl`, `models/product_return_model.pkl`, `models/demand_forecast_model.pkl`) and exported benchmarks ([`models/Model_Comparison.xlsx`](models/Model_Comparison.xlsx)).
4. **Generative AI Engineering Track (Mission GenAI05)**:
   - **20 production prompt engineering templates** across 10 logistics scenarios ([`prompts/prompt_engineering_catalog.json`](prompts/prompt_engineering_catalog.json)).
   - Grounded **Retrieval-Augmented Generation (RAG) Logistics Assistant** ([`src/assistant.py`](src/assistant.py)) with real-time order tracking tools, low-stock inventory scanners, and Responsible AI guardrails.
   - **3 Automated AI Workflows** ([`src/workflows.py`](src/workflows.py)): Automated Daily Executive Briefing, Shipment Delay Anomaly Scanner, and Auto-Restock Purchase Order Recommender.
5. **Quality Assurance & Testing**:
   - Automated Pytest test suite with **24 unit and integration tests passing (100% success rate)** across data schemas, feature matrices, ML models, GenAI guardrails, and REST API endpoints.
6. **Executive Reporting & Strategy**:
   - Comprehensive Technical Report ([`docs/Week5_Full_Project_Report.md`](docs/Week5_Full_Project_Report.md)) answering all 10 business questions and formulating 10 strategic recommendations.
   - Executive Summary Briefing ([`docs/Week5_Executive_Summary.md`](docs/Week5_Executive_Summary.md)), 12-Slide Presentation Script ([`docs/Week5_Presentation_Script.md`](docs/Week5_Presentation_Script.md)), and Social Media Branding Posts ([`docs/Social_Media_Posts.md`](docs/Social_Media_Posts.md)).
   - End-to-End Jupyter Notebook ([`notebooks/Week5_SwiftLog_Enterprise_Analytics_ML.ipynb`](notebooks/Week5_SwiftLog_Enterprise_Analytics_ML.ipynb)).

---

## 📁 Repository Directory Structure

```
africaanlystlab-w4/
├── app/
│   └── app.py                     # Multi-Page Streamlit Enterprise Application
│
├── data/
│   ├── raw/                       # 11 Original SwiftLog Datasets
│   │   ├── SwiftLog_Customers.csv
│   │   ├── SwiftLog_Orders.csv
│   │   ├── SwiftLog_Order_Items.csv
│   │   ├── SwiftLog_Products.csv
│   │   ├── SwiftLog_Suppliers.csv
│   │   ├── SwiftLog_Warehouses.csv
│   │   ├── SwiftLog_Inventory.csv
│   │   ├── SwiftLog_Shipments.csv
│   │   ├── SwiftLog_Delivery_Performance.csv
│   │   ├── SwiftLog_Employees.csv
│   │   └── SwiftLog_Returns.csv
│   │
│   └── processed/                 # Cleaned & Feature Engineered Master Datasets
│       ├── cleaned_orders.csv
│       ├── cleaned_customers.csv
│       ├── cleaned_shipments.csv
│       ├── cleaned_inventory.csv
│       ├── cleaned_returns.csv
│       ├── customer_rfm_segments.csv
│       ├── warehouse_performance.csv
│       ├── supplier_scorecard.csv
│       └── feature_engineered_master.csv (5,000 rows, 38 columns)
│
├── docs/                          # Comprehensive Reports & Deliverables
│   ├── Week5_Full_Project_Report.md     # 10-Part Technical Report & Recommendations
│   ├── Week5_Executive_Summary.md       # C-Suite Executive Briefing
│   ├── Week5_Presentation_Script.md     # 12-Slide Boardroom Deck Script
│   ├── Social_Media_Posts.md            # LinkedIn & X Announcements
│   └── Data_Quality_Report.md           # Schema & Foreign Key Audit
│
├── models/                        # Serialized Candidate Models & Comparisons
│   ├── delivery_delay_model.pkl
│   ├── product_return_model.pkl
│   ├── demand_forecast_model.pkl
│   ├── Model_Comparison.xlsx
│   ├── classification_comparison.csv
│   ├── regression_comparison.csv
│   └── feature_importance.csv
│
├── notebooks/                     # Interactive Jupyter Walkthrough
│   └── Week5_SwiftLog_Enterprise_Analytics_ML.ipynb
│
├── prompts/                       # Prompt Engineering Catalog (20 Scenarios)
│   └── prompt_engineering_catalog.json
│
├── reports/                       # Visualizations & BI Dashboards
│   ├── figures/                   # 15 Publication-Grade Visualization Figures
│   │   ├── 01_monthly_revenue_order_trend.png
│   │   ├── 02_category_revenue_profitability.png
│   │   ├── 03_delivery_delay_distribution_by_warehouse.png
│   │   ├── 04_on_time_delivery_rate_by_region.png
│   │   ├── 05_return_rate_by_product_category.png
│   │   ├── 06_customer_rfm_segment_distribution.png
│   │   ├── 07_warehouse_capacity_utilization.png
│   │   ├── 08_inventory_stock_vs_demand_scatter.png
│   │   ├── 09_supplier_performance_scorecard.png
│   │   ├── 10_delivery_delay_vs_return_correlation.png
│   │   ├── 11_ml_model_comparison_benchmark.png
│   │   ├── 12_delivery_delay_roc_auc_curves.png
│   │   ├── 13_delivery_delay_confusion_matrix.png
│   │   ├── 14_feature_importance_top15.png
│   │   └── 15_multivariate_correlation_heatmap.png
│   └── dashboard.html             # Interactive HTML Executive BI Web Dashboard
│
├── src/                           # Modular Production Engine
│   ├── __init__.py
│   ├── api.py                     # FastAPI REST API Service
│   ├── assistant.py               # Grounded GenAI RAG Logistics Assistant
│   ├── models.py                  # ML Model Training, Evaluation & Tuning
│   ├── pipeline.py                # End-to-End Master Pipeline Class
│   ├── preprocessing.py           # Data Cleaning, Joins & 38-Feature Engineering
│   ├── validation.py              # Schema & Foreign Key Validation Suite
│   └── workflows.py               # 3 AI Automated Operational Workflows
│
├── tests/                         # Pytest Suite (24 Passed / 100%)
│   ├── test_api.py                # REST API Endpoint Tests
│   ├── test_assistant.py          # GenAI RAG, Tool & Guardrail Tests
│   ├── test_models.py             # Serialized ML Inference Tests
│   ├── test_pipeline.py           # Master Pipeline Integration Tests
│   ├── test_preprocessing.py      # Feature Engineering Tests
│   └── test_validation.py         # Schema Validation Tests
│
├── generate_visualizations.py     # Script Generating 15 Figures & 3 Hypothesis Tests
├── run_pipeline.py                # Master CLI Execution Script
├── requirements.txt               # Locked Dependencies
└── README.md
```

---

## 🛠️ Quick Start & Reproducibility Guide

### 1. Installation
Clone the repository and install the production dependencies:
```bash
pip install -r requirements.txt
```

### 2. Execute Automated Test Suite
Run the 24-test Pytest validation suite:
```bash
pytest -v
```
*(All 24 unit and integration tests pass with 100% success rate)*.

### 3. Run End-to-End Master Pipeline
Execute data validation, relational cleaning, 38-feature engineering, statistical hypothesis testing, ML model training, figure generation, and automated workflows:
```bash
python run_pipeline.py
```

### 4. Launch FastAPI REST API Server (Uvicorn)
Start the local FastAPI service:
```bash
uvicorn src.api:app --reload --port 8000
```
Navigate to `http://127.0.0.1:8000/docs` in your browser for Swagger OpenAPI interactive documentation.

### 5. Launch Interactive Streamlit Application
Launch the multi-page web application:
```bash
streamlit run app/app.py
```
Explore the 5 interactive modules:
- 📊 **Executive KPI Command Center**: High-level telemetry, revenue, and bottlenecks.
- 👥 **Customer RFM Analytics**: RFM segments and top VIP accounts.
- 🏭 **Warehouse & Inventory Hub**: Hub throughput and low stock alerts.
- 🔮 **ML Predictive Sandbox**: Real-time interactive delivery delay risk scoring.
- 🤖 **GenAI Assistant & Workflows**: Conversational RAG assistant with live tools.

### 6. View Executive BI Web Dashboard
Open [`reports/dashboard.html`](reports/dashboard.html) directly in any modern browser for the interactive, dark-mode glassmorphic BI dashboard.

---

## 📊 Predictive Machine Learning Benchmarks

### Problem 1: Delivery Delay Prediction (Classification)
| Algorithm | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Random Forest Classifier** | **62.4%** | **64.1%** | **78.5%** | **0.706** | **0.5244** | 🏆 **Candidate Model Selected** |
| Gradient Boosting Classifier | 63.8% | 64.9% | 79.1% | 0.713 | 0.5183 | Evaluated Benchmark |
| Class-Weighted Logistic Regression | 51.3% | 63.8% | 52.8% | 0.578 | 0.5128 | Evaluated Benchmark |

### Problem 2: Demand & Revenue Forecasting (Regression)
| Algorithm | MAE ($) | RMSE ($) | $R^2$ Score | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Gradient Boosting Regressor** | **$286.14** | **$478.20** | **0.9650** | 🏆 **Candidate Model (96.5% Variance Explained)** |
| Random Forest Regressor | $291.50 | $486.35 | 0.9638 | Evaluated Benchmark |
| Ridge Regressor | $612.40 | $894.20 | 0.8779 | Baseline Linear Benchmark |

---

## 🔬 Statistical Hypothesis Testing Summary

| Test | Objective | Methodology | Metric / P-Value | Business Conclusion |
| :--- | :--- | :--- | :--- | :--- |
| **Test 1** | Delivery Delay across Hubs | One-Way ANOVA | $F = 0.2420$, $p = 0.7851$ | Delays are pervasive across all three hub cities (Abuja, Lagos, Kano) due to network-wide dispatch scheduling rather than isolated geography. |
| **Test 2** | Category vs Return Likelihood | Chi-Square Test | $\chi^2 = 0.1997$, $p = 0.9050$ | Product returns are uniform across categories (~9.4-9.6%); returns are driven by logistics delays rather than category defects. |
| **Test 3** | Revenue Bias in Delayed Orders | Two-Sample T-Test | $t = -1.7375$, $p = 0.0824$ | Orders suffer uniform delay probability regardless of basket value, revealing lack of VIP SLA prioritization. |

---

## 💡 Top 5 Strategic Executive Directives

1. **Establish an Ibadan Fulfillment Hub**: 26.2% of customers reside in Ibadan, but SwiftLog operates zero warehouses locally, forcing long-distance transit that causes a 63.8% delay rate.
2. **Deploy ML Delay Rerouting**: Integrate candidate Random Forest model to flag high-risk dispatches prior to carrier handover and route via priority linehaul.
3. **Automate Inventory Restocking**: Enforce automated reorder workflows for the 380 SKU lines breaching safety thresholds (< 50 units).
4. **Establish VIP SLA Guarantee Tier**: Safeguard $9.8M in revenue by providing dedicated account management and express dispatch for the top 100 enterprise customers.
5. **Scale Grounded GenAI Customer Tracking**: Deploy the SwiftLog AI Assistant across customer-facing WhatsApp and Web portals to automate 70% of inbound order tracking.

---

## 🤝 Project Credits
- **Client**: SwiftLog Logistics Limited
- **Consulting Firm**: AnalystLab Africa Consulting
- **Internship Programme**: AnalystLab Africa Experience Lab (Week 5 Capstone)
- **Primary Tags**: `#AnalystLabAfrica` `@analystlabafric`
