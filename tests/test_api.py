"""Pytest Unit & Integration Tests for SwiftLog FastAPI Service."""
import pytest
from fastapi.testclient import TestClient
from src.api import app


client = TestClient(app)


def test_root_endpoint():
    res = client.get("/")
    assert res.status_code == 200
    assert "SwiftLog" in res.json()["service"]


def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"


def test_analytics_kpis():
    res = client.get("/analytics/kpis")
    assert res.status_code == 200
    data = res.json()
    assert data["total_revenue"] > 20000000
    assert data["total_orders"] == 5000
    assert "on_time_delivery_rate" in data


def test_analytics_warehouses():
    res = client.get("/analytics/warehouses")
    assert res.status_code == 200
    whs = res.json()
    assert len(whs) == 15
    assert whs[0]["WarehouseID"] == "W01"


def test_predict_delivery_delay_endpoint():
    payload = {
        "City": "Ibadan",
        "WarehouseID": "W05",
        "Location": "Lagos",
        "OrderTotalRevenue": 4500.0,
        "TotalQuantityOrdered": 12,
        "UniqueProductCount": 3,
        "AvgItemPrice": 375.0,
        "Qty_Electronics": 2,
        "Qty_Fashion": 8,
        "Qty_Food": 2,
        "StaffCount": 14,
        "TotalStockUnits": 63125,
        "WarehouseEfficiencyScore": 48.5,
        "IsInterCityRoute": 1,
        "IsPeakMonth": 0,
        "IsWeekend": 0,
        "OrderMonth": 7,
        "OrderDayOfWeek": "Wednesday",
        "CustomerSegment": "Loyal High-Value",
    }
    res = client.post("/predict/delivery-delay", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "delay_probability" in data
    assert data["is_delayed_flag"] in [0, 1]


def test_assistant_chat_endpoint():
    payload = {"message": "Where is order O00001?"}
    res = client.post("/assistant/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "response" in data
    assert "O00001" in data["response"]


def test_workflow_endpoints():
    r_brief = client.get("/workflows/executive-briefing")
    assert r_brief.status_code == 200
    assert "briefing_markdown" in r_brief.json()

    r_restock = client.get("/workflows/restock-alerts")
    assert r_restock.status_code == 200
    assert r_restock.json()["total_breached_skus"] == 380
