"""Pytest Unit & Integration Tests for SwiftLog Validation Suite."""
import pytest
import pandas as pd
from src.validation import (
    validate_single_dataset,
    validate_foreign_keys,
    validate_all_swiftlog_data,
    SCHEMA_DEFINITIONS,
)


def test_schema_definitions_integrity():
    assert len(SCHEMA_DEFINITIONS) == 11
    assert "SwiftLog_Orders.csv" in SCHEMA_DEFINITIONS
    assert "SwiftLog_Customers.csv" in SCHEMA_DEFINITIONS


def test_validate_customers_raw():
    df = pd.read_csv("data/raw/SwiftLog_Customers.csv")
    res = validate_single_dataset(df, "SwiftLog_Customers.csv")
    assert res["passed"] is True
    assert res["rows"] == 1000
    assert res["primary_key_unique"] is True


def test_validate_orders_raw():
    df = pd.read_csv("data/raw/SwiftLog_Orders.csv")
    res = validate_single_dataset(df, "SwiftLog_Orders.csv")
    assert res["passed"] is True
    assert res["rows"] == 5000
    assert res["primary_key_unique"] is True


def test_validate_all_data_overall():
    summary = validate_all_swiftlog_data("data/raw")
    assert summary["overall_passed"] is True
    assert summary["total_tables_checked"] == 11
    assert summary["total_records_checked"] > 30000
