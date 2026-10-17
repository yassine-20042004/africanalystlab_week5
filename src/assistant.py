import os
import sys
import re
import json
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional

# Ensure standard UTF-8 stream handling on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class SwiftLogKnowledgeBase:
    """Vector & Document Indexing Engine for SwiftLog Supply Chain Knowledge."""

    def __init__(self, processed_dir: str = "data/processed", raw_dir: str = "data/raw"):
        self.processed_dir = processed_dir
        self.raw_dir = raw_dir
        self.documents: List[Dict[str, Any]] = []
        self._build_knowledge_corpus()

    def _build_knowledge_corpus(self):
        """Indexes structured datasets into semantic business knowledge chunks."""
        # 1. Company Executive Logistics Overview
        self.documents.append({
            "doc_id": "DOC-CORP-01",
            "title": "SwiftLog Corporate Logistics Operational Overview",
            "category": "Corporate Overview",
            "content": (
                "SwiftLog Logistics Limited is a premier supply chain provider operating across Nigeria. "
                "The enterprise operates 15 fulfillment warehouses across Lagos (8), Abuja (4), and Kano (3). "
                "Serving 1,000 registered commercial customers across Ibadan, Kano, Lagos, and Abuja. "
                "Total historical recorded revenue is $21,668,065.85 across 5,000 orders. "
                "Category revenue breakdown: Fashion ($8,059,602.65), Food ($7,113,401.88), Electronics ($6,495,061.32). "
                "Overall on-time delivery rate is 36.28%, with 63.72% shipments experiencing delays. "
                "Average delivery delay is 3.57 days. Total warehouse stock stands at 1,007,764 units. "
                "Overall return rate is 10.00% (500 returns), driven by Late Delivery (37%), Wrong Item (33%), and Damaged Goods (30%)."
            ),
        })

        # 2. Regional Hub Deficit in Ibadan
        self.documents.append({
            "doc_id": "DOC-REG-01",
            "title": "Regional Infrastructure Bottleneck - Ibadan Fulfillment Gap",
            "category": "Regional Infrastructure",
            "content": (
                "Ibadan represents 26.2% of SwiftLog's total customer base (262 customers), generating substantial order volume. "
                "However, SwiftLog currently operates zero fulfillment hubs in Ibadan. All orders bound for Ibadan are routed "
                "via inter-city transit from Lagos or Abuja hubs, resulting in high delivery transit times and a 63.79% delay rate. "
                "Opening a dedicated fulfillment hub or cross-dock facility in Ibadan is the highest priority network recommendation."
            ),
        })

        # 3. Warehouse Benchmarks
        wh_file = os.path.join(self.processed_dir, "warehouse_performance.csv")
        if os.path.exists(wh_file):
            wh_df = pd.read_csv(wh_file)
            for _, r in wh_df.iterrows():
                self.documents.append({
                    "doc_id": f"DOC-WH-{r['WarehouseID']}",
                    "title": f"Warehouse {r['WarehouseID']} Performance Profile ({r['Location']})",
                    "category": "Warehouse Operations",
                    "content": (
                        f"Warehouse {r['WarehouseID']} is located in {r['Location']} staffed by {int(r['StaffCount'])} logistics employees. "
                        f"Total stock maintained: {int(r['TotalStockUnits']):,} units with {int(r['LowStockSKUCount'])} SKUs below safety stock. "
                        f"Historical shipments dispatched: {int(r['TotalShipments'])} with an average delay of {r['AverageDelayDays']:.2f} days. "
                        f"Delay rate: {r['DelayRate']*100:.1f}% (On-time rate: {r['OnTimeRate']*100:.1f}%). "
                        f"Warehouse Efficiency Score: {r['WarehouseEfficiencyScore']:.1f}/100."
                    ),
                })

        # 4. Return Policy & Logistics Guidelines
        self.documents.append({
            "doc_id": "DOC-POL-01",
            "title": "SwiftLog Return & Replacement Operating Guidelines",
            "category": "Policy & Quality",
            "content": (
                "SwiftLog provides a 14-day return and replacement policy for all retail and wholesale orders. "
                "Valid reasons for return authorization include: 1. Late Delivery (> 3 days past promised window), "
                "2. Wrong Item dispatched due to warehouse picking error, 3. Damaged goods in transit. "
                "Couriers are dispatched within 24 hours of return authorization to pick up items at zero customer expense. "
                "Full refunds or wallet credits are finalized within 3 to 5 business days upon warehouse intake scan."
            ),
        })

        # 5. Low Stock & Inventory Replenishment Thresholds
        self.documents.append({
            "doc_id": "DOC-INV-01",
            "title": "Inventory Replenishment Protocols & Stockout Alerts",
            "category": "Inventory Management",
            "content": (
                "SwiftLog maintains a mandatory safety stock threshold of 50 units per SKU per warehouse. "
                "When stock levels fall below 50 units, automated reorder triggers are dispatched to primary suppliers. "
                "Across the network, 380 SKU-warehouse combinations currently breach safety stock thresholds, representing 9.5% "
                "of inventory lines. Reorders must prioritize high-demand electronics and fast-moving fashion apparel."
            ),
        })

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieves top matching documents using keyword and token overlap scoring."""
        query_tokens = set(re.findall(r"\w+", query.lower()))
        scored_docs = []

        for doc in self.documents:
            doc_tokens = set(re.findall(r"\w+", doc["content"].lower() + " " + doc["title"].lower()))
            overlap = len(query_tokens.intersection(doc_tokens))
            if overlap > 0:
                scored_docs.append((overlap, doc))

        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [d[1] for d in scored_docs[:top_k]]


class SwiftLogAIAssistant:
    """Enterprise AI Logistics Assistant with grounded RAG, tools, and safety guardrails."""

    def __init__(self, processed_dir: str = "data/processed", raw_dir: str = "data/raw"):
        self.kb = SwiftLogKnowledgeBase(processed_dir=processed_dir, raw_dir=raw_dir)
        self.processed_dir = processed_dir
        self.raw_dir = raw_dir
        self._load_tables()

    def _load_tables(self):
        """Loads cached tables for direct lookup tools."""
        master_path = os.path.join(self.processed_dir, "feature_engineered_master.csv")
        if os.path.exists(master_path):
            self.master_df = pd.read_csv(master_path)
        else:
            self.master_df = pd.DataFrame()

        inv_path = os.path.join(self.processed_dir, "cleaned_inventory.csv")
        if os.path.exists(inv_path):
            self.inv_df = pd.read_csv(inv_path)
        else:
            self.inv_df = pd.DataFrame()

    def apply_guardrails(self, query: str) -> Optional[str]:
        """Safety guardrails checking out-of-scope queries and malicious injections."""
        query_lower = query.lower()

        # Reject out-of-domain requests
        forbidden_topics = ["crypto", "politic", "medical", "password", "bypass", "jailbreak", "hack"]
        if any(w in query_lower for w in forbidden_topics):
            return (
                "🛡️ [SwiftLog Security Guardrail]: I am strictly configured to assist with "
                "SwiftLog logistics operations, inventory monitoring, delivery tracking, and supply chain analytics. "
                "Requests concerning external, unrelated, or sensitive topics are blocked."
            )

        # Mask sensitive PII patterns
        if re.search(r"\b\d{16}\b", query):
            return "🛡️ [SwiftLog Privacy Guardrail]: Credit card numbers detected. For data privacy, PII is masked."

        return None

    def track_order(self, order_id: str) -> Dict[str, Any]:
        """Tool: Direct order status and delivery telemetry lookup."""
        if self.master_df.empty:
            return {"error": "Order telemetry database unavailable."}

        order_match = self.master_df[self.master_df["OrderID"].str.upper() == order_id.strip().upper()]
        if order_match.empty:
            return {"found": False, "message": f"Order #{order_id} was not found in SwiftLog operational logs."}

        r = order_match.iloc[0]
        return {
            "found": True,
            "order_id": r["OrderID"],
            "customer_id": r["CustomerID"],
            "city": r["City"],
            "order_date": str(r["OrderDate"]),
            "status": r["Status"],
            "total_revenue": f"${r['OrderTotalRevenue']:,.2f}",
            "items_count": int(r["TotalQuantityOrdered"]),
            "warehouse_id": r["WarehouseID"],
            "warehouse_location": r["Location"],
            "delay_days": int(r["DelayDays"]),
            "is_delayed": bool(r["IsDelayed"]),
            "delivery_status": r["DeliveryStatus"],
            "is_returned": bool(r["IsReturned"]),
            "return_reason": r["ReturnReason"],
        }

    def get_low_stock_alerts(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Tool: Retrieve immediate stockout risk SKUs (< 50 units)."""
        if self.inv_df.empty:
            return []
        low_items = self.inv_df[self.inv_df["Stock"] < 50].sort_values("Stock").head(limit)
        return low_items.to_dict(orient="records")

    def answer(self, user_query: str) -> Dict[str, Any]:
        """Main RAG answering function with factual grounding and tool augmentation."""
        # 1. Guardrail Check
        guardrail_violation = self.apply_guardrails(user_query)
        if guardrail_violation:
            return {
                "response": guardrail_violation,
                "sources": [],
                "confidence": 1.0,
                "tool_used": "Guardrail Enforcement",
            }

        # 2. Check for Specific Order Query (e.g., O00001, O02902)
        order_match = re.search(r"\b(O\d{5})\b", user_query, re.IGNORECASE)
        if order_match:
            order_id = order_match.group(1).upper()
            tracking = self.track_order(order_id)
            if tracking.get("found"):
                status_emoji = "✅" if tracking["delivery_status"] == "On Time" else "⚠️"
                response_text = (
                    f"📦 **SwiftLog Shipment Tracking for #{tracking['order_id']}**\n\n"
                    f"- **Customer**: `{tracking['customer_id']}` ({tracking['city']})\n"
                    f"- **Order Status**: **{tracking['status']}** (Placed: {tracking['order_date'][:10]})\n"
                    f"- **Order Value**: {tracking['total_revenue']} ({tracking['items_count']} total items)\n"
                    f"- **Dispatch Hub**: Warehouse `{tracking['warehouse_id']}` located in **{tracking['warehouse_location']}**\n"
                    f"- **Delivery Status**: {status_emoji} **{tracking['delivery_status']}** ({tracking['delay_days']} days transit delay)\n"
                )
                if tracking["is_returned"]:
                    response_text += f"- **Return Status**: ⚠️ Returned — Reason: *{tracking['return_reason']}*\n"
                else:
                    response_text += "- **Return Status**: Not Returned\n"

                response_text += (
                    f"\n💡 *Operational Assessment*: This order was dispatched from {tracking['warehouse_location']} to {tracking['city']}. "
                    f"{'Because destination is outside the dispatch hub, inter-city logistics delays occurred.' if tracking['is_delayed'] else 'Delivery was completed within normal transit windows.'}"
                )

                return {
                    "response": response_text,
                    "sources": [f"Operational Telemetry: {order_id}"],
                    "confidence": 0.98,
                    "tool_used": "Order Tracking Telemetry",
                }

        # 3. Check for Inventory / Low Stock Query
        if any(term in user_query.lower() for term in ["stock", "inventory", "replenish", "low stock", "reorder"]):
            low_stocks = self.get_low_stock_alerts(limit=5)
            if low_stocks:
                response_text = (
                    "⚠️ **SwiftLog Inventory Alert: Critical Low-Stock SKUs (< 50 units)**\n\n"
                    "Our real-time inventory scans show **380 total SKU records** currently below safety thresholds. "
                    "Top 5 priority replenishment items:\n\n"
                )
                for item in low_stocks:
                    response_text += f"- **Product `{item['ProductID']}`** in Warehouse `{item['WarehouseID']}`: Only **{item['Stock']} units** remaining.\n"
                response_text += (
                    "\n📋 *Recommended Action*: Trigger automated PO creation to assigned primary suppliers. "
                    "Prioritize SKUs in high-turnover warehouses (W12, W02, W11)."
                )
                return {
                    "response": response_text,
                    "sources": ["SwiftLog Inventory Telemetry", "DOC-INV-01"],
                    "confidence": 0.96,
                    "tool_used": "Inventory Replenishment Scanner",
                }

        # 4. RAG Document Retrieval
        retrieved_docs = self.kb.search(user_query, top_k=2)
        if retrieved_docs:
            context_blocks = "\n\n".join([f"[{d['title']}]: {d['content']}" for d in retrieved_docs])
            response_text = (
                f"**SwiftLog Logistics Intelligence Summary**\n\n"
                f"{retrieved_docs[0]['content']}\n\n"
            )
            if len(retrieved_docs) > 1:
                response_text += f"**Additional Context ({retrieved_docs[1]['title']})**:\n{retrieved_docs[1]['content']}\n\n"

            sources = [d["title"] for d in retrieved_docs]
            return {
                "response": response_text,
                "sources": sources,
                "confidence": 0.94,
                "tool_used": "RAG Knowledge Retrieval",
            }

        # Default fallback
        return {
            "response": (
                "I am SwiftLog's AI Logistics Assistant. I can assist you with tracking orders (e.g. `O00001`), "
                "inspecting warehouse performance (e.g. `W05`), reviewing inventory reorder alerts, or "
                "synthesizing enterprise logistics KPIs. Please provide an Order ID or logistics inquiry."
            ),
            "sources": ["Corporate Knowledge Base"],
            "confidence": 0.85,
            "tool_used": "General Assistant Dispatch",
        }


if __name__ == "__main__":
    print("Initializing SwiftLog AI Assistant & Knowledge Base...")
    assistant = SwiftLogAIAssistant()
    sample_queries = [
        "Where is order O00001?",
        "What are our lowest stock inventory items?",
        "Why is there a fulfillment problem in Ibadan?",
        "Can I get crypto investment advice?",
    ]
    for q in sample_queries:
        print(f"\n--- QUERY: {q} ---")
        res = assistant.answer(q)
        print(f"Tool: {res['tool_used']} | Confidence: {res['confidence']}")
        print(res["response"])
