"""Streamlit Interactive Enterprise Application for SwiftLog Logistics Analytics & AI Transformation."""
import os
import joblib
import pandas as pd
import numpy as np
import streamlit as st

# Configure page
st.set_page_config(
    page_title="SwiftLog Logistics Intelligence Hub",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern design aesthetics
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 20px;
        border-radius: 12px;
        color: white;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .metric-val {
        font-size: 28px;
        font-weight: 700;
        color: #38bdf8;
    }
    .metric-sub {
        font-size: 13px;
        color: #94a3b8;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    master = pd.read_csv("data/processed/feature_engineered_master.csv")
    wh = pd.read_csv("data/processed/warehouse_performance.csv")
    cust = pd.read_csv("data/processed/customer_rfm_segments.csv")
    inv = pd.read_csv("data/processed/cleaned_inventory.csv")
    supp = pd.read_csv("data/processed/supplier_scorecard.csv")
    return master, wh, cust, inv, supp


@st.cache_resource
def load_models():
    delay_pipe = joblib.load("models/delivery_delay_model.pkl")
    return delay_pipe


master_df, wh_df, cust_df, inv_df, supp_df = load_data()
delay_pipe = load_models()

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/color/96/delivery.png", width=70)
st.sidebar.title("SwiftLog Logistics")
st.sidebar.caption("Enterprise Supply Chain & AI Transformation")
st.sidebar.markdown("---")

nav_choice = st.sidebar.radio(
    "Navigation Track",
    [
        "📊 Executive KPI Command Center",
        "👥 Customer RFM Analytics",
        "🏭 Warehouse & Inventory Hub",
        "🔮 ML Predictive Sandbox",
        "🤖 GenAI Logistics Assistant & Workflows",
    ],
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **AnalystLab Africa Experience Lab**\nWeek 5 Enterprise Capstone")

# ==============================================================================
# TAB 1: EXECUTIVE KPI COMMAND CENTER
# ==============================================================================
if nav_choice == "📊 Executive KPI Command Center":
    st.title("🚚 Executive Logistics Command Center")
    st.markdown("Real-time operational telemetry, revenue performance, and logistics bottlenecks.")

    total_rev = master_df["OrderTotalRevenue"].sum()
    total_orders = len(master_df)
    delayed_orders = master_df["IsDelayed"].sum()
    ontime_pct = (1 - (delayed_orders / total_orders)) * 100
    avg_delay = master_df["DelayDays"].mean()
    total_stock = inv_df["Stock"].sum()

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-sub">Cumulative Revenue</div>
            <div class="metric-val">${total_rev/1e6:.2f}M</div>
            <div class="metric-sub">Across 5,000 Orders</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-sub">On-Time Delivery Rate</div>
            <div class="metric-val" style="color: {'#ef4444' if ontime_pct < 50 else '#22c55e'};">{ontime_pct:.1f}%</div>
            <div class="metric-sub">Delayed: {delayed_orders:,} orders</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-sub">Average Transit Delay</div>
            <div class="metric-val" style="color: #f59e0b;">{avg_delay:.2f} Days</div>
            <div class="metric-sub">Max Recorded: 7.0 Days</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-sub">Product Return Rate</div>
            <div class="metric-val" style="color: #ec4899;">10.0%</div>
            <div class="metric-sub">500 Total Returns</div>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-sub">Warehouse Inventory</div>
            <div class="metric-val" style="color: #10b981;">{total_stock/1e6:.2f}M</div>
            <div class="metric-sub">15 Operational Hubs</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("###")
    st.subheader("Key Visual Trajectories")
    c1, c2 = st.columns(2)
    with c1:
        st.image("reports/figures/01_monthly_revenue_order_trend.png", caption="Monthly Revenue & Order Count (Peak in August & April)")
    with c2:
        st.image("reports/figures/02_category_revenue_profitability.png", caption="Revenue by Category (Fashion leads at $8.06M)")

    st.markdown("---")
    st.subheader("Critical Operational Vulnerabilities Identified")
    st.error("🚨 **1. Ibadan Fulfillment Deficit**: 26.2% of customers reside in Ibadan, but SwiftLog operates zero local fulfillment warehouses, causing chronic inter-city delays.")
    st.warning("⚠️ **2. High Delay Hubs**: Warehouses W05 (68.0%), W09 (67.5%), and W03 (67.4%) experience severe bottleneck delays.")
    st.warning("⚠️ **3. Return Correlation**: 37% of all product returns are triggered solely by Late Deliveries.")

# ==============================================================================
# TAB 2: CUSTOMER RFM ANALYTICS
# ==============================================================================
elif nav_choice == "👥 Customer RFM Analytics":
    st.title("👥 Customer Intelligence & Behavioral Segmentation")
    st.markdown("Segmentation of 1,000 corporate and retail accounts across Recency, Frequency, and Monetary spend.")

    c1, c2 = st.columns([1, 1])
    with c1:
        st.image("reports/figures/06_customer_rfm_segment_distribution.png", caption="Customer RFM Spend vs Frequency")
    with c2:
        st.image("reports/figures/04_on_time_delivery_rate_by_region.png", caption="On-Time Delivery by Destination City")

    st.subheader("Top Revenue-Contributing Customers (VIP Tier 1)")
    top_cust = cust_df.sort_values("TotalSpend", ascending=False).head(10)[
        ["CustomerID", "CustomerName", "City", "OrderFrequency", "TotalSpend", "AvgOrderValue", "CustomerSegment"]
    ]
    st.dataframe(top_cust, use_container_width=True)

# ==============================================================================
# TAB 3: WAREHOUSE & INVENTORY HUB
# ==============================================================================
elif nav_choice == "🏭 Warehouse & Inventory Hub":
    st.title("🏭 Warehouse Operations & Inventory Health")
    st.markdown("Analysis of 15 regional fulfillment hubs, staffing allocation, and safety stock compliance.")

    c1, c2 = st.columns(2)
    with c1:
        st.image("reports/figures/03_delivery_delay_distribution_by_warehouse.png", caption="Transit Delay Distribution across Hubs")
    with c2:
        st.image("reports/figures/08_inventory_stock_vs_demand_scatter.png", caption="Critical Depleted SKUs (< 50 Units) by Warehouse")

    st.subheader("Warehouse Performance Scorecard")
    st.dataframe(wh_df[[
        "WarehouseID", "Location", "StaffCount", "TotalStockUnits", "TotalShipments",
        "DelayRate", "AverageDelayDays", "WarehouseEfficiencyScore"
    ]], use_container_width=True)

# ==============================================================================
# TAB 4: ML PREDICTIVE SANDBOX
# ==============================================================================
elif nav_choice == "🔮 ML Predictive Sandbox":
    st.title("🔮 Machine Learning Predictive Sandbox")
    st.markdown("Real-time inference using trained scikit-learn models for delivery delay risk scoring.")

    c1, c2, c3 = st.columns(3)
    with c1:
        city = st.selectbox("Destination City", ["Ibadan", "Lagos", "Kano", "Abuja"])
        wh_id = st.selectbox("Dispatch Warehouse", [f"W{i:02d}" for i in range(1, 16)], index=4)
        order_val = st.number_input("Order Total ($ USD)", value=3500.0, step=100.0)
    with c2:
        qty = st.slider("Total Quantity Ordered", 1, 50, 10)
        skus = st.slider("Distinct SKU Count", 1, 10, 3)
        month = st.slider("Order Month", 1, 12, 8)
    with c3:
        day_of_week = st.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        segment = st.selectbox("Customer Segment", ["VIP Tier 1", "Loyal High-Value", "Frequent Regular", "Occasional / Low-Frequency"])

    if st.button("Run Predictive Risk Scoring", type="primary"):
        # Synthesize feature input
        wh_row = wh_df[wh_df["WarehouseID"] == wh_id].iloc[0]
        input_row = pd.DataFrame([{
            "City": city,
            "WarehouseID": wh_id,
            "Location": wh_row["Location"],
            "OrderTotalRevenue": order_val,
            "TotalQuantityOrdered": qty,
            "UniqueProductCount": skus,
            "AvgItemPrice": order_val / max(qty, 1),
            "Qty_Electronics": int(qty * 0.3),
            "Qty_Fashion": int(qty * 0.4),
            "Qty_Food": int(qty * 0.3),
            "StaffCount": wh_row["StaffCount"],
            "TotalStockUnits": wh_row["TotalStockUnits"],
            "WarehouseEfficiencyScore": wh_row["WarehouseEfficiencyScore"],
            "IsInterCityRoute": int(city != wh_row["Location"]),
            "IsPeakMonth": int(month in [3, 4, 8]),
            "IsWeekend": int(day_of_week in ["Saturday", "Sunday"]),
            "OrderMonth": month,
            "OrderDayOfWeek": day_of_week,
            "CustomerSegment": segment,
        }])

        proba = float(delay_pipe.predict_proba(input_row)[0][1])
        pred = int(delay_pipe.predict(input_row)[0])

        st.markdown("---")
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric("Predicted Delivery Status", "Delayed (>= 3 Days)" if pred == 1 else "On Time (< 3 Days)")
            st.metric("Delay Probability", f"{proba*100:.1f}%")
        with res_col2:
            if proba >= 0.60:
                st.error("🚨 **High Risk Dispatch**: Reroute to secondary regional carrier or prioritize morning express linehaul.")
            elif proba >= 0.45:
                st.warning("⚠️ **Moderate Delay Risk**: Monitor dispatch cutoff time and ensure pre-manifest scan.")
            else:
                st.success("✅ **Low Delay Risk**: Standard ground fulfillment recommended.")

    st.markdown("---")
    st.subheader("Model Benchmark & Confusion Matrix")
    b1, b2 = st.columns(2)
    with b1:
        st.image("reports/figures/11_ml_model_comparison_benchmark.png")
    with b2:
        st.image("reports/figures/13_delivery_delay_confusion_matrix.png")

# ==============================================================================
# TAB 5: GENAI ASSISTANT & AUTOMATED WORKFLOWS
# ==============================================================================
elif nav_choice == "🤖 GenAI Logistics Assistant & Workflows":
    st.title("🤖 Grounded GenAI Logistics Assistant & Workflows")
    st.markdown("Retrieval-Augmented Generation (RAG) assistant grounded on SwiftLog operational data.")

    from src.assistant import SwiftLogAIAssistant
    from src.workflows import SwiftLogWorkflowEngine

    assistant = SwiftLogAIAssistant()
    wf_engine = SwiftLogWorkflowEngine()

    tab_chat, tab_auto = st.tabs(["💬 Interactive Assistant Chat", "⚙️ Automated AI Workflows"])

    with tab_chat:
        st.markdown("Ask anything regarding order status (e.g. `Where is order O00001?`), warehouse performance, or inventory alerts.")
        user_input = st.text_input("Enter your logistics prompt:", value="Where is order O00001?")
        if st.button("Send Inquiry"):
            with st.spinner("Analyzing operational telemetry..."):
                response = assistant.answer(user_input)
                st.markdown(response["response"])
                st.caption(f"🔧 Tool Used: {response['tool_used']} | Grounding Confidence: {response['confidence']*100:.1f}%")
                if response.get("sources"):
                    st.info("📚 Sources: " + ", ".join(response["sources"]))

    with tab_auto:
        st.subheader("Trigger Automated Enterprise Workflows")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📋 Generate Daily Executive Briefing"):
                b = wf_engine.run_daily_executive_briefing()
                st.code(b["briefing_markdown"])
        with c2:
            if st.button("📦 Scan for Severe Delay Anomalies"):
                s = wf_engine.run_shipment_delay_anomaly_scanner()
                st.code(s["alert_summary"])
            if st.button("🔄 Generate Restocking Purchase Orders"):
                r = wf_engine.run_inventory_restocking_recommender()
                st.code(r["report_summary"])
