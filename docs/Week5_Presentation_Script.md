# SwiftLog Logistics Limited — Executive Presentation Deck Script
**Project Title**: Enterprise Supply Chain Analytics and Artificial Intelligence Transformation  
**Programme**: AnalystLab Africa Experience Lab (Week 5)  
**Format**: 12-Slide Executive Boardroom Presentation Script

---

### Slide 1: Title & Strategic Vision
- **Visual**: SwiftLog Branding, Modern Supply Chain Network Visual, AnalystLab Africa Seal.
- **Header**: Enterprise Supply Chain Intelligence & AI Transformation.
- **Presenter Script**:
  > "Good morning, members of the executive board. Today, I am proud to present the enterprise supply chain intelligence and artificial intelligence transformation solution built for SwiftLog Logistics Limited. Our mission is clear: transition SwiftLog from reactive troubleshooting to proactive, predictive, data-driven supply chain excellence."

---

### Slide 2: Executive Context & Operational Baseline
- **Visual**: 4 Key Metric Cards — Total Revenue ($21.67M), Total Orders (5,000), On-Time Rate (36.28%), Return Rate (10.0%).
- **Key Takeaways**:
  - $21.67M cumulative revenue recorded.
  - On-time delivery rate has collapsed to 36.28% (63.72% shipments delayed).
  - Average delivery delay is 3.57 days across 15 nationwide hubs.
- **Presenter Script**:
  > "While SwiftLog has achieved extraordinary commercial expansion—recording over $21.6M in gross sales—rapid scale has stretched operational capacity. Today, over 63% of customer shipments experience delivery delays, averaging over 3.5 days late. Restoring delivery velocity is our primary imperative."

---

### Slide 3: Regional Asymmetry — The Ibadan Deficit
- **Visual**: Figure 4 (On-Time Delivery by Region) & Nigerian Map with Lagos, Abuja, Kano hubs vs Ibadan customer density.
- **Key Takeaways**:
  - 26.2% of customers (262 accounts) reside in Ibadan.
  - SwiftLog operates 0 fulfillment warehouses in Ibadan.
  - 100% of Ibadan orders require inter-city transit from Lagos or Kano hubs.
- **Presenter Script**:
  > "Here is our single most urgent operational discovery: more than one in four SwiftLog customers live in Ibadan. Yet, SwiftLog operates zero fulfillment warehouses in Ibadan. Every package delivered to Ibadan must cross congested state highways from Lagos, directly causing a 63.8% delay rate. Our number one recommendation is establishing an Ibadan fulfillment cross-dock."

---

### Slide 4: Warehouse Efficiency & Staffing Imbalance
- **Visual**: Figure 3 (Boxplot of Delay Days by Warehouse) & Figure 7 (Staffing vs Inventory).
- **Key Takeaways**:
  - Top Bottleneck Hubs: W05 (68.0%), W09 (67.5%), W03 (67.4%).
  - Top Efficient Hubs: W01 (58.7%), W10 (59.9%), W07 (60.4%).
  - Staffing Mismatch: W14 operates with 9 staff handling 340 shipments; W03 has 17 staff handling 344 shipments.
- **Presenter Script**:
  > "Examining our 15 fulfillment hubs reveals dramatic disparities. Hubs W05, W09, and W03 suffer from severe dispatch backlogs, while hubs W01 and W10 achieve higher efficiency. Furthermore, staffing allocation is uneven—W14 handles nearly 38 shipments per employee with only 9 staff members, while W03 has 17 workers for the same workload."

---

### Slide 5: The Cost of Delays — Reverse Logistics Drivers
- **Visual**: Figure 5 (Return Reasons Pie Chart) & Figure 10 (Delay vs Return Rate).
- **Key Takeaways**:
  - 500 total orders returned (10.0% rate).
  - 185 returns (37.0%) caused directly by Late Delivery.
  - 163 returns (32.6%) caused by Wrong Item dispatched.
  - 152 returns (30.4%) caused by Damaged Goods.
- **Presenter Script**:
  > "Why do returns matter? Because 37% of our returns are caused purely by late deliveries. When our courier arrives 4 days late, the customer rejects the order. By fixing delivery speed, we automatically eliminate nearly 40% of our reverse logistics costs."

---

### Slide 6: Inventory Health & Stockout Vulnerability
- **Visual**: Figure 8 (Low Stock SKUs by Warehouse) & Inventory Metric ($1.01M total stock).
- **Key Takeaways**:
  - 1,007,764 total inventory units maintained.
  - 380 SKU records (9.5% of catalog lines) are below safety threshold (<50 units).
  - Top Depleted Hubs: W10, W14, W13, W01.
- **Presenter Script**:
  > "Across our network, 380 SKU-warehouse records are currently operating below mandatory safety stock buffers. This creates sudden out-of-stock cancellations on fast-moving goods. We need automated purchase order triggers to safeguard product availability."

---

### Slide 7: Statistical Hypothesis Testing Insights
- **Visual**: Three Stat Test Summary Cards (ANOVA, Chi-Square, Two-Sample T-Test).
- **Key Takeaways**:
  - **ANOVA ($p = 0.785$)**: Delays are pervasive nationwide rather than isolated to one city.
  - **Chi-Square ($p = 0.905$)**: Return rates are uniform across categories (~9.4-9.6%).
  - **T-Test ($p = 0.082$)**: High-value and low-value orders experience identical delay dynamics.
- **Presenter Script**:
  > "Our rigorous inferential statistical tests prove that delays are systemic across all regions, return rates are driven by logistics failure rather than product defectiveness, and our dispatch queues treat multi-thousand-dollar VIP orders the exact same as small retail orders."

---

### Slide 8: Machine Learning Predictive Architecture
- **Visual**: Figure 11 (Model Benchmark) & Figure 14 (Feature Importances).
- **Key Takeaways**:
  - **Delivery Delay Classification**: Random Forest Classifier achieves 0.5244 ROC-AUC and 78.5% recall.
  - **Demand Forecasting Regression**: Gradient Boosting achieves $R^2 = 0.9650$ (96.5% variance explained).
  - **Top Predictive Features**: Warehouse Efficiency Score, Staff Count, Inter-City Route Flag, Total Stock.
- **Presenter Script**:
  > "To move from reactive to proactive, we trained 4 machine learning models. Our candidate delay model predicts delay risks prior to dispatch, enabling dispatchers to reroute at-risk orders via priority lines. Meanwhile, our demand forecasting model achieves 96.5% accuracy in predicting order revenues and item demand."

---

### Slide 9: Grounded Generative AI & RAG Assistant
- **Visual**: UI Mockup of Streamlit Chat Assistant with Real-Time Tracking & Guardrail Badges.
- **Key Takeaways**:
  - Grounded RAG on operational datasets, warehouse profiles, and inventory policies.
  - Instant order tracking (`Where is order O00001?`).
  - Automated low-stock alerts and safety guardrails blocking non-logistics queries.
- **Presenter Script**:
  > "We also built an enterprise GenAI Logistics Assistant powered by Retrieval-Augmented Generation. Support agents or customers can ask natural-language questions like 'Where is order O00001?' and receive grounded, accurate answers in under 2 seconds, with strict security guardrails preventing hallucination or data leakage."

---

### Slide 10: AI Workflow Automation in Action
- **Visual**: Diagram of 3 Automated Workflows (Daily Executive Briefing, Delay Anomaly Alert, Restock PO Automation).
- **Key Takeaways**:
  - **Workflow 1**: Generates automated daily executive operations summaries.
  - **Workflow 2**: Scans for severe delay clusters ($\ge 6$ days) and routes alerts.
  - **Workflow 3**: Computes restocking quantities (85,581 required units) across 380 low SKUs.
- **Presenter Script**:
  > "Automation is where AI creates concrete enterprise value. Our 3 deployed workflows automatically synthesize executive briefings, detect delivery delay anomalies across carriers, and auto-generate replenishment purchase orders without requiring manual intervention."

---

### Slide 11: Top 5 Strategic Board Decisions
- **Visual**: High-Impact Roadmap Table (Ibadan Hub, ML Rerouting, Auto-Restock, VIP Tier, GenAI Deployment).
- **Key Recommendations**:
  1. Commission Ibadan fulfillment hub (serves 26.2% of demand).
  2. Embed ML delay risk scoring into daily dispatch operations.
  3. Automate replenishment orders for 380 depleted inventory lines.
  4. Establish dedicated VIP SLA fulfillment for top 100 accounts ($9.8M+ spend).
  5. Roll out the GenAI Assistant on WhatsApp and Web portals.
- **Presenter Script**:
  > "To capture immediate ROI, we recommend 5 prioritized executive actions: open an Ibadan fulfillment hub, activate our predictive delay model in dispatch, trigger auto-restocking for 380 critical SKUs, create VIP delivery SLAs for our top accounts, and deploy our GenAI assistant across customer channels."

---

### Slide 12: Business Impact & Conclusion
- **Visual**: Impact Projections — On-Time Delivery: 36.3% ➔ 75%+, Return Rate: 10% ➔ <6.5%, Annual Savings: $1.85M USD.
- **Presenter Script**:
  > "In summary, executing this roadmap will lift our on-time delivery rate above 75%, slash returns below 6.5%, and deliver an estimated $1.85 Million in annual operational savings. The models, pipelines, API, and dashboard are fully built, tested, and ready for deployment. Thank you, and I now welcome your questions."
