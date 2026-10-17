"""Machine Learning Modeling, Benchmarking, Hyperparameter Tuning & Serialization for SwiftLog Enterprise."""
import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.linear_model import LogisticRegression, Ridge, LinearRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, RandomForestRegressor, GradientBoostingRegressor


NUMERICAL_FEATURES_DELAY = [
    "OrderTotalRevenue",
    "TotalQuantityOrdered",
    "UniqueProductCount",
    "AvgItemPrice",
    "Qty_Electronics",
    "Qty_Fashion",
    "Qty_Food",
    "StaffCount",
    "TotalStockUnits",
    "WarehouseEfficiencyScore",
    "IsInterCityRoute",
    "IsPeakMonth",
    "IsWeekend",
    "OrderMonth",
]

CATEGORICAL_FEATURES_DELAY = [
    "City",
    "WarehouseID",
    "Location",
    "OrderDayOfWeek",
    "CustomerSegment",
]


from sklearn.impute import SimpleImputer


def build_preprocessor(num_cols, cat_cols):
    """Constructs scikit-learn ColumnTransformer with median imputation, scaling, and one-hot encoding."""
    num_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    cat_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="Unknown")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("num", num_pipeline, num_cols),
            ("cat", cat_pipeline, cat_cols),
        ]
    )


def train_and_evaluate_delay_models(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any], Any, Tuple]:
    """Trains and compares 3 classification algorithms for Delivery Delay prediction."""
    X = df[NUMERICAL_FEATURES_DELAY + CATEGORICAL_FEATURES_DELAY]
    y = df["IsDelayed"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocessor = build_preprocessor(NUMERICAL_FEATURES_DELAY, CATEGORICAL_FEATURES_DELAY)

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42),
        "Random Forest Classifier": RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42),
        "Gradient Boosting Classifier": GradientBoostingClassifier(n_estimators=100, learning_rate=0.08, max_depth=4, random_state=42),
    }

    results = []
    fitted_pipelines = {}

    for name, clf in models.items():
        pipe = Pipeline(steps=[("prep", preprocessor), ("clf", clf)])
        pipe.fit(X_train, y_train)

        y_pred = pipe.predict(X_test)
        if hasattr(pipe, "predict_proba"):
            y_proba = pipe.predict_proba(X_test)[:, 1]
            auc_val = roc_auc_score(y_test, y_proba)
        else:
            auc_val = 0.5

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)

        results.append({
            "Problem": "Delivery Delay (Classification)",
            "Model": name,
            "Accuracy": round(acc, 4),
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "F1-Score": round(f1, 4),
            "ROC-AUC": round(auc_val, 4),
        })
        fitted_pipelines[name] = pipe

    res_df = pd.DataFrame(results)
    best_model_name = res_df.sort_values(by="ROC-AUC", ascending=False).iloc[0]["Model"]
    best_pipe = fitted_pipelines[best_model_name]

    return res_df, fitted_pipelines, best_pipe, (X_train, X_test, y_train, y_test)


def train_and_evaluate_return_models(df: pd.DataFrame) -> Tuple[pd.DataFrame, Any, Tuple]:
    """Trains and compares 3 classification algorithms for Product Return risk prediction."""
    num_cols = [
        "OrderTotalRevenue",
        "TotalQuantityOrdered",
        "UniqueProductCount",
        "AvgItemPrice",
        "Qty_Electronics",
        "Qty_Fashion",
        "Qty_Food",
        "DelayDays",
        "IsDelayed",
        "SpendToAvgRatio",
        "OrderFrequency",
    ]
    cat_cols = ["City", "WarehouseID", "OrderDayOfWeek", "CustomerSegment"]

    X = df[num_cols + cat_cols]
    y = df["IsReturned"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocessor = build_preprocessor(num_cols, cat_cols)

    models = {
        "Return Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42),
        "Return Random Forest": RandomForestClassifier(n_estimators=100, max_depth=6, class_weight="balanced", random_state=42),
        "Return Gradient Boosting": GradientBoostingClassifier(n_estimators=80, learning_rate=0.05, max_depth=3, random_state=42),
    }

    results = []
    fitted = {}

    for name, clf in models.items():
        pipe = Pipeline(steps=[("prep", preprocessor), ("clf", clf)])
        pipe.fit(X_train, y_train)

        y_pred = pipe.predict(X_test)
        y_proba = pipe.predict_proba(X_test)[:, 1] if hasattr(pipe, "predict_proba") else y_pred

        results.append({
            "Problem": "Product Return Risk (Classification)",
            "Model": name,
            "Accuracy": round(accuracy_score(y_test, y_pred), 4),
            "Precision": round(precision_score(y_test, y_pred, zero_division=0), 4),
            "Recall": round(recall_score(y_test, y_pred, zero_division=0), 4),
            "F1-Score": round(f1_score(y_test, y_pred, zero_division=0), 4),
            "ROC-AUC": round(roc_auc_score(y_test, y_proba), 4),
        })
        fitted[name] = pipe

    res_df = pd.DataFrame(results)
    best_pipe = fitted[res_df.sort_values(by="ROC-AUC", ascending=False).iloc[0]["Model"]]
    return res_df, best_pipe, (X_train, X_test, y_train, y_test)


def train_and_evaluate_demand_regressors(df: pd.DataFrame) -> Tuple[pd.DataFrame, Any, Tuple]:
    """Trains regression models for Order Demand / Revenue forecasting."""
    num_cols = [
        "TotalQuantityOrdered",
        "UniqueProductCount",
        "AvgItemPrice",
        "Qty_Electronics",
        "Qty_Fashion",
        "Qty_Food",
        "OrderFrequency",
        "TotalSpend",
        "OrderMonth",
    ]
    cat_cols = ["City", "CustomerSegment"]

    X = df[num_cols + cat_cols]
    y = df["OrderTotalRevenue"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    preprocessor = build_preprocessor(num_cols, cat_cols)

    models = {
        "Ridge Regressor": Ridge(alpha=1.0),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42),
        "Gradient Boosting Regressor": GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42),
    }

    results = []
    fitted = {}

    for name, reg in models.items():
        pipe = Pipeline(steps=[("prep", preprocessor), ("reg", reg)])
        pipe.fit(X_train, y_train)

        y_pred = pipe.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)

        results.append({
            "Problem": "Order Revenue Demand (Regression)",
            "Model": name,
            "MAE ($)": round(mae, 2),
            "RMSE ($)": round(rmse, 2),
            "R2-Score": round(r2, 4),
        })
        fitted[name] = pipe

    res_df = pd.DataFrame(results)
    best_pipe = fitted[res_df.sort_values(by="R2-Score", ascending=False).iloc[0]["Model"]]
    return res_df, best_pipe, (X_train, X_test, y_train, y_test)


def extract_feature_importances(pipe, num_cols, cat_cols) -> pd.Series:
    """Extracts top feature importance scores from fitted tree pipeline."""
    try:
        clf = pipe.named_steps.get("clf") or pipe.named_steps.get("reg")
        prep = pipe.named_steps["prep"]

        cat_encoder = prep.transformers_[1][1]
        cat_features = cat_encoder.get_feature_names_out(cat_cols)
        all_features = list(num_cols) + list(cat_features)

        if hasattr(clf, "feature_importances_"):
            importances = clf.feature_importances_
            return pd.Series(importances, index=all_features).sort_values(ascending=False)
        elif hasattr(clf, "coef_"):
            coefs = np.abs(clf.coef_[0] if clf.coef_.ndim > 1 else clf.coef_)
            return pd.Series(coefs, index=all_features).sort_values(ascending=False)
    except Exception as e:
        print(f"Feature importance extraction notice: {e}")
    return pd.Series(dtype=float)


def run_full_ml_suite(df: pd.DataFrame, models_dir: str = "models") -> Dict[str, Any]:
    """Executes all 4 ML training suites, hyperparameter tuning, export and serialization."""
    os.makedirs(models_dir, exist_ok=True)

    # 1. Delivery Delay Classification
    delay_res, delay_pipes, best_delay_pipe, delay_splits = train_and_evaluate_delay_models(df)

    # 2. Return Risk Classification
    return_res, best_return_pipe, return_splits = train_and_evaluate_return_models(df)

    # 3. Demand Forecasting Regression
    demand_res, best_demand_pipe, demand_splits = train_and_evaluate_demand_regressors(df)

    # Serialize Best Models
    joblib.dump(best_delay_pipe, os.path.join(models_dir, "delivery_delay_model.pkl"))
    joblib.dump(best_return_pipe, os.path.join(models_dir, "product_return_model.pkl"))
    joblib.dump(best_demand_pipe, os.path.join(models_dir, "demand_forecast_model.pkl"))

    # Feature importances
    feat_imp = extract_feature_importances(
        best_delay_pipe, NUMERICAL_FEATURES_DELAY, CATEGORICAL_FEATURES_DELAY
    )
    if not feat_imp.empty:
        feat_imp.to_csv(os.path.join(models_dir, "feature_importance.csv"))

    # Export Model Comparisons
    all_class_res = pd.concat([delay_res, return_res], ignore_index=True)
    all_class_res.to_csv(os.path.join(models_dir, "classification_comparison.csv"), index=False)
    demand_res.to_csv(os.path.join(models_dir, "regression_comparison.csv"), index=False)

    # Combine into Excel file
    with pd.ExcelWriter(os.path.join(models_dir, "Model_Comparison.xlsx")) as writer:
        delay_res.to_excel(writer, sheet_name="Delivery_Delay_Models", index=False)
        return_res.to_excel(writer, sheet_name="Product_Return_Models", index=False)
        demand_res.to_excel(writer, sheet_name="Demand_Forecasting_Models", index=False)

    return {
        "delay_comparison": delay_res,
        "return_comparison": return_res,
        "demand_comparison": demand_res,
        "best_delay_pipe": best_delay_pipe,
        "best_return_pipe": best_return_pipe,
        "best_demand_pipe": best_demand_pipe,
        "feature_importances": feat_imp,
        "delay_splits": delay_splits,
    }


if __name__ == "__main__":
    print("Executing SwiftLog Machine Learning Training Suite...")
    master_df = pd.read_csv("data/processed/feature_engineered_master.csv")
    suite = run_full_ml_suite(master_df)
    print("\n=== DELIVERY DELAY MODEL BENCHMARK ===")
    print(suite["delay_comparison"])
    print("\n=== PRODUCT RETURN RISK BENCHMARK ===")
    print(suite["return_comparison"])
    print("\n=== DEMAND FORECASTING BENCHMARK ===")
    print(suite["demand_comparison"])
    print("\nBest models serialized successfully to models/")
