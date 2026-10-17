"""Production FastAPI REST API Service for SwiftLog Logistics Analytics & AI Transformation."""
import os
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from src.assistant import SwiftLogAIAssistant
from src.workflows import SwiftLogWorkflowEngine


app = FastAPI(
    title="SwiftLog Logistics Intelligence & AI Transformation API",
    description="Enterprise REST API service providing predictive ML inference, GenAI assistant interaction, real-time KPI telemetry, and automated operational workflows.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global caches
MODELS: Dict[str, Any] = {}
ASSISTANT: Optional[SwiftLogAIAssistant] = None
WORKFLOWS: Optional[SwiftLogWorkflowEngine] = None
DATA_CACHE: Dict[str, pd.DataFrame] = {}


def get_assistant() -> SwiftLogAIAssistant:
    global ASSISTANT
    if ASSISTANT is None:
        ASSISTANT = SwiftLogAIAssistant()
    return ASSISTANT


def get_workflows() -> SwiftLogWorkflowEngine:
    global WORKFLOWS
    if WORKFLOWS is None:
        WORKFLOWS = SwiftLogWorkflowEngine()
    return WORKFLOWS


def load_cached_model(model_name: str):
    """Loads and caches scikit-learn model pipelines."""
    if model_name not in MODELS:
        path = os.path.join("models", f"{model_name}.pkl")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Serialized model artifact not found: {path}")
        MODELS[model_name] = joblib.load(path)
    return MODELS[model_name]


# Request Schemas
class DelayPredictionRequest(BaseModel):
    City: str = Field(..., example="Ibadan", description="Customer destination city")
    WarehouseID: str = Field(..., example="W05", description="Dispatch fulfillment warehouse ID")
    Location: str = Field(..., example="Lagos", description="Warehouse location city")
    OrderTotalRevenue: float = Field(..., example=4500.0, description="Total order amount in USD")
    TotalQuantityOrdered: int = Field(..., example=12, description="Total items in order")
    UniqueProductCount: int = Field(..., example=3, description="Distinct SKUs in order")
    AvgItemPrice: float = Field(..., example=375.0, description="Average unit price")
    Qty_Electronics: int = Field(0, example=2)
    Qty_Fashion: int = Field(0, example=8)
    Qty_Food: int = Field(0, example=2)
    StaffCount: int = Field(14, example=14)
    TotalStockUnits: int = Field(63125, example=63125)
    WarehouseEfficiencyScore: float = Field(48.5, example=48.5)
    IsInterCityRoute: int = Field(1, example=1)
    IsPeakMonth: int = Field(0, example=0)
    IsWeekend: int = Field(0, example=0)
    OrderMonth: int = Field(7, example=7)
    OrderDayOfWeek: str = Field("Wednesday", example="Wednesday")
    CustomerSegment: str = Field("Loyal High-Value", example="Loyal High-Value")


class ReturnPredictionRequest(BaseModel):
    City: str = Field(..., example="Lagos")
    WarehouseID: str = Field(..., example="W04")
    OrderTotalRevenue: float = Field(..., example=2500.0)
    TotalQuantityOrdered: int = Field(..., example=5)
    UniqueProductCount: int = Field(..., example=2)
    AvgItemPrice: float = Field(..., example=500.0)
    Qty_Electronics: int = Field(0, example=3)
    Qty_Fashion: int = Field(0, example=2)
    Qty_Food: int = Field(0, example=0)
    DelayDays: int = Field(4, example=4)
    IsDelayed: int = Field(1, example=1)
    SpendToAvgRatio: float = Field(1.1, example=1.1)
    OrderFrequency: int = Field(5, example=5)
    OrderDayOfWeek: str = Field("Monday", example="Monday")
    CustomerSegment: str = Field("Frequent Regular", example="Frequent Regular")


class AssistantChatRequest(BaseModel):
    message: str = Field(..., example="Where is order O00001?", description="User logistics prompt")


# Endpoints
@app.get("/", tags=["System"])
def root_info():
    """Returns top-level API metadata and documentation links."""
    return {
        "service": "SwiftLog Logistics Intelligence & AI Transformation API",
        "internship_programme": "AnalystLab Africa Experience Lab",
        "week": "Week 5",
        "status": "online",
        "documentation": "/docs",
        "endpoints": [
            "/health",
            "/analytics/kpis",
            "/analytics/warehouses",
            "/predict/delivery-delay",
            "/predict/return-risk",
            "/assistant/chat",
            "/workflows/executive-briefing",
            "/workflows/restock-alerts",
        ],
    }


@app.get("/health", tags=["System"])
def health_check():
    """System health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "environment": "production",
    }


@app.get("/analytics/kpis", tags=["Analytics"])
def get_enterprise_kpis():
    """Returns high-level supply chain business metrics."""
    try:
        master_path = "data/processed/feature_engineered_master.csv"
        df = pd.read_csv(master_path)
        total_rev = float(df["OrderTotalRevenue"].sum())
        total_orders = int(len(df))
        delayed = int(df["IsDelayed"].sum())
        on_time_rate = round((1 - (delayed / total_orders)) * 100, 2)
        returns = int(df["IsReturned"].sum())
        return_rate = round((returns / total_orders) * 100, 2)

        return {
            "total_revenue": total_rev,
            "total_orders": total_orders,
            "on_time_delivery_rate": on_time_rate,
            "delayed_shipments": delayed,
            "average_delay_days": round(float(df["DelayDays"].mean()), 2),
            "total_returns": returns,
            "return_rate": return_rate,
            "total_customers": 1000,
            "total_warehouses": 15,
            "total_products": 250,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed loading KPI metrics: {e}")


@app.get("/analytics/warehouses", tags=["Analytics"])
def get_warehouses():
    """Returns warehouse performance metrics and efficiency rankings."""
    try:
        wh_path = "data/processed/warehouse_performance.csv"
        df = pd.read_csv(wh_path)
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed loading warehouse performance: {e}")


@app.post("/predict/delivery-delay", tags=["Machine Learning"])
def predict_delivery_delay(req: DelayPredictionRequest):
    """Predicts delivery delay probability for an inbound shipment."""
    try:
        pipe = load_cached_model("delivery_delay_model")
        input_data = pd.DataFrame([req.model_dump()])
        pred = int(pipe.predict(input_data)[0])
        proba = float(pipe.predict_proba(input_data)[0][1])

        risk_category = "Low Risk" if proba < 0.40 else ("Moderate Risk" if proba < 0.65 else "High Delay Risk")

        return {
            "prediction": "Delayed" if pred == 1 else "On Time",
            "is_delayed_flag": pred,
            "delay_probability": round(proba, 4),
            "risk_assessment": risk_category,
            "recommendation": "Route via expedited linehaul hub" if proba >= 0.50 else "Standard ground dispatch",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {e}")


@app.post("/predict/return-risk", tags=["Machine Learning"])
def predict_return_risk(req: ReturnPredictionRequest):
    """Predicts product return likelihood for an order."""
    try:
        pipe = load_cached_model("product_return_model")
        input_data = pd.DataFrame([req.model_dump()])
        pred = int(pipe.predict(input_data)[0])
        proba = float(pipe.predict_proba(input_data)[0][1])

        return {
            "prediction": "Returned" if pred == 1 else "Retained",
            "is_returned_flag": pred,
            "return_probability": round(proba, 4),
            "risk_level": "High Return Risk" if proba >= 0.20 else "Normal Risk",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {e}")


@app.post("/assistant/chat", tags=["Generative AI"])
def chat_with_assistant(req: AssistantChatRequest):
    """Interacts with the grounded GenAI Logistics Assistant."""
    try:
        bot = get_assistant()
        result = bot.answer(req.message)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Assistant execution error: {e}")


@app.get("/workflows/executive-briefing", tags=["Automated Workflows"])
def trigger_executive_briefing():
    """Generates on-demand daily executive operations briefing."""
    try:
        wf = get_workflows()
        return wf.run_daily_executive_briefing()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow failed: {e}")


@app.get("/workflows/restock-alerts", tags=["Automated Workflows"])
def trigger_restock_alerts():
    """Generates inventory replenishment recommendations for depleted SKUs."""
    try:
        wf = get_workflows()
        return wf.run_inventory_restocking_recommender()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow failed: {e}")
