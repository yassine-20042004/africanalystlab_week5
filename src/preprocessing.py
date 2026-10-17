"""Data Preprocessing, Cleaning, Relational Merging & Feature Engineering Pipeline for SwiftLog Enterprise Solution."""
import os
import pandas as pd
import numpy as np
from typing import Dict, Tuple, Any


def assign_supplier_id(product_id: str) -> str:
    """Deterministically maps ProductID (P001-P250) to SupplierID (S001-S150)."""
    try:
        p_num = int(str(product_id).replace("P", ""))
        supp_num = ((p_num * 7) % 150) + 1
        return f"S{supp_num:03d}"
    except Exception:
        return "S001"


def clean_raw_datasets(raw_dir: str = "data/raw") -> Dict[str, pd.DataFrame]:
    """Loads and cleans all 11 SwiftLog raw datasets."""
    customers = pd.read_csv(os.path.join(raw_dir, "SwiftLog_Customers.csv"))
    orders = pd.read_csv(os.path.join(raw_dir, "SwiftLog_Orders.csv"))
    order_items = pd.read_csv(os.path.join(raw_dir, "SwiftLog_Order_Items.csv"))
    products = pd.read_csv(os.path.join(raw_dir, "SwiftLog_Products.csv"))
    suppliers = pd.read_csv(os.path.join(raw_dir, "SwiftLog_Suppliers.csv"))
    warehouses = pd.read_csv(os.path.join(raw_dir, "SwiftLog_Warehouses.csv"))
    inventory = pd.read_csv(os.path.join(raw_dir, "SwiftLog_Inventory.csv"))
    shipments = pd.read_csv(os.path.join(raw_dir, "SwiftLog_Shipments.csv"))
    delivery_perf = pd.read_csv(os.path.join(raw_dir, "SwiftLog_Delivery_Performance.csv"))
    employees = pd.read_csv(os.path.join(raw_dir, "SwiftLog_Employees.csv"))
    returns = pd.read_csv(os.path.join(raw_dir, "SwiftLog_Returns.csv"))

    # Standardize string formatting
    customers["City"] = customers["City"].str.strip()
    warehouses["Location"] = warehouses["Location"].str.strip()
    products["Category"] = products["Category"].str.strip()
    returns["Reason"] = returns["Reason"].str.strip()

    # Link Products to Suppliers
    products["SupplierID"] = products["ProductID"].apply(assign_supplier_id)
    products = products.merge(suppliers, on="SupplierID", how="left")

    # Parse and enrich Order Dates
    orders["OrderDate"] = pd.to_datetime(orders["OrderDate"])
    orders["OrderYear"] = orders["OrderDate"].dt.year
    orders["OrderMonth"] = orders["OrderDate"].dt.month
    orders["OrderMonthName"] = orders["OrderDate"].dt.strftime("%B")
    orders["OrderDay"] = orders["OrderDate"].dt.day
    orders["OrderDayOfWeek"] = orders["OrderDate"].dt.day_name()
    orders["OrderQuarter"] = orders["OrderDate"].dt.quarter
    orders["IsWeekend"] = orders["OrderDate"].dt.dayofweek.isin([5, 6]).astype(int)

    # Calculate item-level sales and revenue
    order_items = order_items.merge(
        products[["ProductID", "Category", "UnitPrice", "SupplierID", "SupplierName"]],
        on="ProductID",
        how="left",
    )
    order_items["LineTotal"] = order_items["Quantity"] * order_items["UnitPrice"]

    # Delivery performance alignment
    delivery_map = delivery_perf.set_index("ShipmentID")["Status"].to_dict()
    shipments["DeliveryStatus"] = shipments["ShipmentID"].map(delivery_map).fillna("Unknown")
    shipments["IsDelayed"] = (shipments["DelayDays"] >= 3).astype(int)

    # Returns alignment
    returns_map = returns.set_index("OrderID")["Reason"].to_dict()
    orders["IsReturned"] = orders["OrderID"].isin(returns_map.keys()).astype(int)
    orders["ReturnReason"] = orders["OrderID"].map(returns_map).fillna("Not Returned")

    return {
        "customers": customers,
        "orders": orders,
        "order_items": order_items,
        "products": products,
        "suppliers": suppliers,
        "warehouses": warehouses,
        "inventory": inventory,
        "shipments": shipments,
        "delivery_perf": delivery_perf,
        "employees": employees,
        "returns": returns,
    }


def compute_warehouse_metrics(
    warehouses: pd.DataFrame,
    shipments: pd.DataFrame,
    inventory: pd.DataFrame,
    employees: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregates operational warehouse metrics and efficiency scores."""
    staff_counts = employees.groupby("WarehouseID").size().rename("StaffCount")
    inv_counts = inventory.groupby("WarehouseID")["Stock"].sum().rename("TotalStockUnits")
    low_stock_counts = (
        inventory[inventory["Stock"] < 50]
        .groupby("WarehouseID")
        .size()
        .rename("LowStockSKUCount")
    )

    ship_agg = shipments.groupby("WarehouseID").agg(
        TotalShipments=("ShipmentID", "count"),
        DelayedShipments=("IsDelayed", "sum"),
        AverageDelayDays=("DelayDays", "mean"),
    )
    ship_agg["DelayRate"] = (
        ship_agg["DelayedShipments"] / ship_agg["TotalShipments"]
    ).round(4)
    ship_agg["OnTimeRate"] = (1 - ship_agg["DelayRate"]).round(4)

    wh_perf = warehouses.merge(staff_counts, on="WarehouseID", how="left")
    wh_perf = wh_perf.merge(inv_counts, on="WarehouseID", how="left")
    wh_perf = wh_perf.merge(low_stock_counts, on="WarehouseID", how="left").fillna({"LowStockSKUCount": 0})
    wh_perf = wh_perf.merge(ship_agg, on="WarehouseID", how="left")

    wh_perf["ShipmentsPerStaff"] = (
        wh_perf["TotalShipments"] / wh_perf["StaffCount"]
    ).round(2)
    wh_perf["StockPerStaff"] = (
        wh_perf["TotalStockUnits"] / wh_perf["StaffCount"]
    ).round(2)

    # Efficiency Score (100 = flawless on-time, penalised by delay rate and avg delay days)
    wh_perf["WarehouseEfficiencyScore"] = (
        (wh_perf["OnTimeRate"] * 60) + ((7 - wh_perf["AverageDelayDays"]) / 7 * 40)
    ).round(2)

    return wh_perf


def compute_customer_rfm_segments(
    customers: pd.DataFrame,
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
) -> pd.DataFrame:
    """Computes Customer RFM metrics and behavioral segments."""
    reference_date = orders["OrderDate"].max()

    oi_totals = order_items.groupby("OrderID")["LineTotal"].sum().rename("OrderTotal")
    orders_enriched = orders.merge(oi_totals, on="OrderID", how="left").fillna({"OrderTotal": 0})

    cust_agg = orders_enriched.groupby("CustomerID").agg(
        LastOrderDate=("OrderDate", "max"),
        OrderFrequency=("OrderID", "count"),
        TotalSpend=("OrderTotal", "sum"),
        TotalReturns=("IsReturned", "sum"),
    ).reset_index()

    cust_agg["RecencyDays"] = (reference_date - cust_agg["LastOrderDate"]).dt.days
    cust_agg["AvgOrderValue"] = (cust_agg["TotalSpend"] / cust_agg["OrderFrequency"]).round(2)
    cust_agg["ReturnRate"] = (cust_agg["TotalReturns"] / cust_agg["OrderFrequency"]).round(4)

    # Customer Lifetime Value estimation (Spend * retention factor)
    cust_agg["CustomerLifetimeValue"] = (
        cust_agg["TotalSpend"] * (1 - cust_agg["ReturnRate"])
    ).round(2)

    # Behavioral Segmentation
    spend_p75 = cust_agg["TotalSpend"].quantile(0.75)
    spend_p50 = cust_agg["TotalSpend"].quantile(0.50)
    freq_p50 = cust_agg["OrderFrequency"].quantile(0.50)

    def segment_customer(row):
        if row["TotalSpend"] >= spend_p75 and row["OrderFrequency"] >= freq_p50:
            return "VIP Tier 1"
        elif row["TotalSpend"] >= spend_p50:
            return "Loyal High-Value"
        elif row["OrderFrequency"] >= freq_p50:
            return "Frequent Regular"
        else:
            return "Occasional / Low-Frequency"

    cust_agg["CustomerSegment"] = cust_agg.apply(segment_customer, axis=1)

    customer_master = customers.merge(cust_agg, on="CustomerID", how="left").fillna({
        "OrderFrequency": 0,
        "TotalSpend": 0.0,
        "RecencyDays": 999,
        "AvgOrderValue": 0.0,
        "ReturnRate": 0.0,
        "CustomerLifetimeValue": 0.0,
        "CustomerSegment": "Inactive / New",
    })

    return customer_master


def compute_supplier_scorecard(
    suppliers: pd.DataFrame,
    products: pd.DataFrame,
    order_items: pd.DataFrame,
    orders: pd.DataFrame,
    shipments: pd.DataFrame,
) -> pd.DataFrame:
    """Computes Supplier Reliability & Delay scorecard."""
    oi_full = order_items.merge(
        orders[["OrderID", "IsReturned", "OrderDate"]], on="OrderID", how="left"
    ).merge(
        shipments[["OrderID", "IsDelayed", "DelayDays"]], on="OrderID", how="left"
    )

    supp_agg = oi_full.groupby("SupplierID").agg(
        TotalUnitsSupplied=("Quantity", "sum"),
        TotalOrdersFulfilled=("OrderID", "nunique"),
        TotalRevenueGenerated=("LineTotal", "sum"),
        DelayedOrders=("IsDelayed", "sum"),
        ReturnedOrders=("IsReturned", "sum"),
        AverageDelayDays=("DelayDays", "mean"),
    ).reset_index()

    supp_agg["DelayRate"] = (
        supp_agg["DelayedOrders"] / supp_agg["TotalOrdersFulfilled"].replace(0, 1)
    ).round(4)
    supp_agg["ReturnRate"] = (
        supp_agg["ReturnedOrders"] / supp_agg["TotalOrdersFulfilled"].replace(0, 1)
    ).round(4)

    # Supplier Reliability Score (0 to 100)
    supp_agg["SupplierReliabilityScore"] = (
        100 - (supp_agg["DelayRate"] * 50) - (supp_agg["ReturnRate"] * 50)
    ).clip(lower=0, upper=100).round(2)

    supplier_master = suppliers.merge(supp_agg, on="SupplierID", how="left").fillna({
        "TotalUnitsSupplied": 0,
        "TotalOrdersFulfilled": 0,
        "TotalRevenueGenerated": 0.0,
        "DelayedOrders": 0,
        "ReturnedOrders": 0,
        "AverageDelayDays": 0.0,
        "DelayRate": 0.0,
        "ReturnRate": 0.0,
        "SupplierReliabilityScore": 100.0,
    })

    return supplier_master


def build_feature_engineered_dataset(
    cleaned_dict: Dict[str, pd.DataFrame],
    customer_master: pd.DataFrame,
    wh_perf: pd.DataFrame,
) -> pd.DataFrame:
    """Builds unified multi-variable feature matrix for predictive ML and analytics."""
    orders = cleaned_dict["orders"]
    order_items = cleaned_dict["order_items"]
    shipments = cleaned_dict["shipments"]
    warehouses = cleaned_dict["warehouses"]

    # Order item aggregations per OrderID
    order_metrics = order_items.groupby("OrderID").agg(
        OrderTotalRevenue=("LineTotal", "sum"),
        TotalQuantityOrdered=("Quantity", "sum"),
        UniqueProductCount=("ProductID", "nunique"),
        AvgItemPrice=("UnitPrice", "mean"),
    ).reset_index()

    # Category breakdowns per order
    cat_pivot = (
        order_items.pivot_table(
            index="OrderID",
            columns="Category",
            values="Quantity",
            aggfunc="sum",
            fill_value=0,
        )
        .add_prefix("Qty_")
        .reset_index()
    )

    # Master Order assembly
    df = orders.merge(order_metrics, on="OrderID", how="left").fillna({
        "OrderTotalRevenue": 0.0,
        "TotalQuantityOrdered": 0,
        "UniqueProductCount": 0,
        "AvgItemPrice": 0.0,
    })
    df = df.merge(cat_pivot, on="OrderID", how="left").fillna({
        "Qty_Electronics": 0,
        "Qty_Fashion": 0,
        "Qty_Food": 0,
    })
    df = df.merge(
        customer_master[[
            "CustomerID", "City", "OrderFrequency", "TotalSpend",
            "CustomerSegment", "CustomerLifetimeValue"
        ]],
        on="CustomerID",
        how="left",
    )
    df = df.merge(
        shipments[["OrderID", "ShipmentID", "WarehouseID", "DelayDays", "IsDelayed", "DeliveryStatus"]],
        on="OrderID",
        how="left",
    )
    df = df.merge(
        wh_perf[[
            "WarehouseID", "Location", "StaffCount", "TotalStockUnits",
            "WarehouseEfficiencyScore"
        ]],
        on="WarehouseID",
        how="left",
    )

    # InterCity flag: delivery crosses city boundary
    df["IsInterCityRoute"] = (df["City"] != df["Location"]).astype(int)

    # Delivery Duration Proxy (Transit days estimate = 2 baseline + DelayDays)
    df["DeliveryDurationDays"] = 2 + df["DelayDays"]

    # Seasonal Demand Indicator (Peak shipping months: August, April, March)
    df["IsPeakMonth"] = df["OrderMonth"].isin([3, 4, 8]).astype(int)

    # Average Order Spend Ratio
    avg_cust_spend = (df["TotalSpend"] / df["OrderFrequency"].replace(0, 1)).replace(0, 1)
    df["SpendToAvgRatio"] = (df["OrderTotalRevenue"] / avg_cust_spend).fillna(0.0).round(3)

    return df


def run_full_preprocessing(
    raw_dir: str = "data/raw", processed_dir: str = "data/processed"
) -> Dict[str, Any]:
    """Executes full cleaning, feature engineering, and exports processed CSV datasets."""
    os.makedirs(processed_dir, exist_ok=True)

    cleaned = clean_raw_datasets(raw_dir=raw_dir)
    wh_perf = compute_warehouse_metrics(
        cleaned["warehouses"],
        cleaned["shipments"],
        cleaned["inventory"],
        cleaned["employees"],
    )
    cust_master = compute_customer_rfm_segments(
        cleaned["customers"], cleaned["orders"], cleaned["order_items"]
    )
    supp_scorecard = compute_supplier_scorecard(
        cleaned["suppliers"],
        cleaned["products"],
        cleaned["order_items"],
        cleaned["orders"],
        cleaned["shipments"],
    )
    master_features = build_feature_engineered_dataset(
        cleaned, cust_master, wh_perf
    )

    # Save to disk
    cleaned["orders"].to_csv(os.path.join(processed_dir, "cleaned_orders.csv"), index=False)
    cleaned["customers"].to_csv(os.path.join(processed_dir, "cleaned_customers.csv"), index=False)
    cleaned["shipments"].to_csv(os.path.join(processed_dir, "cleaned_shipments.csv"), index=False)
    cleaned["inventory"].to_csv(os.path.join(processed_dir, "cleaned_inventory.csv"), index=False)
    cleaned["returns"].to_csv(os.path.join(processed_dir, "cleaned_returns.csv"), index=False)
    wh_perf.to_csv(os.path.join(processed_dir, "warehouse_performance.csv"), index=False)
    cust_master.to_csv(os.path.join(processed_dir, "customer_rfm_segments.csv"), index=False)
    supp_scorecard.to_csv(os.path.join(processed_dir, "supplier_scorecard.csv"), index=False)
    master_features.to_csv(os.path.join(processed_dir, "feature_engineered_master.csv"), index=False)

    return {
        "cleaned_datasets": cleaned,
        "warehouse_performance": wh_perf,
        "customer_segments": cust_master,
        "supplier_scorecard": supp_scorecard,
        "master_features": master_features,
        "master_shape": master_features.shape,
    }


if __name__ == "__main__":
    print("Executing SwiftLog preprocessing & feature engineering pipeline...")
    res = run_full_preprocessing()
    print(f"Master feature matrix constructed: {res['master_shape']}")
    print("All processed datasets saved to data/processed/")
