"""Pytest Unit & Integration Tests for SwiftLog Machine Learning Models."""
import os
import joblib
import pytest
import pandas as pd
import numpy as np


def test_serialized_models_exist():
    assert os.path.exists("models/delivery_delay_model.pkl")
    assert os.path.exists("models/product_return_model.pkl")
    assert os.path.exists("models/demand_forecast_model.pkl")


def test_delivery_delay_model_inference():
    pipe = joblib.load("models/delivery_delay_model.pkl")
    sample_input = pd.DataFrame([{
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
    }])

    pred = pipe.predict(sample_input)
    assert pred[0] in [0, 1]

    proba = pipe.predict_proba(sample_input)
    assert proba.shape == (1, 2)
    assert np.isclose(proba.sum(), 1.0)


def test_demand_forecast_model_inference():
    pipe = joblib.load("models/demand_forecast_model.pkl")
    sample_input = pd.DataFrame([{
        "TotalQuantityOrdered": 10,
        "UniqueProductCount": 3,
        "AvgItemPrice": 350.0,
        "Qty_Electronics": 3,
        "Qty_Fashion": 4,
        "Qty_Food": 3,
        "OrderFrequency": 8,
        "TotalSpend": 45000.0,
        "OrderMonth": 5,
        "City": "Lagos",
        "CustomerSegment": "VIP Tier 1",
    }])

    pred = pipe.predict(sample_input)
    assert pred[0] > 0
