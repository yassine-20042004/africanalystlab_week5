"""Pytest Unit & Integration Tests for SwiftLog Preprocessing & Feature Engineering."""
import os
import pytest
import pandas as pd
from src.preprocessing import (
    clean_raw_datasets,
    compute_warehouse_metrics,
    compute_customer_rfm_segments,
    run_full_preprocessing,
)


def test_clean_raw_datasets():
    cleaned = clean_raw_datasets("data/raw")
    assert len(cleaned) == 11
    assert "orders" in cleaned
    assert "OrderMonth" in cleaned["orders"].columns
    assert "IsWeekend" in cleaned["orders"].columns
    assert "LineTotal" in cleaned["order_items"].columns


def test_customer_rfm_segmentation():
    cleaned = clean_raw_datasets("data/raw")
    cust_master = compute_customer_rfm_segments(
        cleaned["customers"], cleaned["orders"], cleaned["order_items"]
    )
    assert len(cust_master) == 1000
    assert "CustomerSegment" in cust_master.columns
    assert "CustomerLifetimeValue" in cust_master.columns
    assert cust_master["TotalSpend"].sum() > 20000000


def test_warehouse_metrics_aggregation():
    cleaned = clean_raw_datasets("data/raw")
    wh_perf = compute_warehouse_metrics(
        cleaned["warehouses"],
        cleaned["shipments"],
        cleaned["inventory"],
        cleaned["employees"],
    )
    assert len(wh_perf) == 15
    assert "WarehouseEfficiencyScore" in wh_perf.columns
    assert "DelayRate" in wh_perf.columns
    assert wh_perf["DelayRate"].mean() > 0.50


def test_processed_master_feature_matrix():
    path = "data/processed/feature_engineered_master.csv"
    assert os.path.exists(path)
    df = pd.read_csv(path)
    assert len(df) == 5000
    assert df.isnull().sum().sum() == 0
    assert "IsInterCityRoute" in df.columns
    assert "IsDelayed" in df.columns
