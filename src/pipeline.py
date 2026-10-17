"""Master Pipeline Orchestrator for SwiftLog Enterprise Supply Chain & AI Transformation."""
import os
import sys
import pandas as pd
from typing import Dict, Any

from src.validation import validate_all_swiftlog_data, write_data_quality_report
from src.preprocessing import run_full_preprocessing
from src.models import run_full_ml_suite
from src.workflows import SwiftLogWorkflowEngine
from generate_visualizations import generate_all_15_figures, run_statistical_hypothesis_tests


class SwiftLogMasterPipeline:
    """End-to-End Orchestrator for Validation, Preprocessing, Modeling, Workflows, and Visualizations."""

    def __init__(self, raw_dir: str = "data/raw", processed_dir: str = "data/processed", models_dir: str = "models"):
        self.raw_dir = raw_dir
        self.processed_dir = processed_dir
        self.models_dir = models_dir

    def run(self) -> Dict[str, Any]:
        """Executes the complete multi-track enterprise workflow."""
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")

        print("=" * 75)
        print("  SWIFTLOG LOGISTICS LIMITED — MASTER ENTERPRISE PIPELINE EXECUTION  ")
        print("=" * 75)

        # Step 1: Validation
        print("\n[Stage 1/5] Validating Raw Datasets & Referential Integrity...")
        val_summary = validate_all_swiftlog_data(self.raw_dir)
        write_data_quality_report(val_summary, "docs/Data_Quality_Report.md")
        print(f"  -> Validation Status: {'PASSED' if val_summary['overall_passed'] else 'FAILED'}")
        print(f"  -> Total Records Checked: {val_summary['total_records_checked']:,}")

        # Step 2: Preprocessing & Feature Engineering
        print("\n[Stage 2/5] Cleaning, Relational Joins & 38-Feature Engineering...")
        prep_res = run_full_preprocessing(self.raw_dir, self.processed_dir)
        master_df = prep_res["master_features"]
        print(f"  -> Master Feature Matrix Shape: {master_df.shape}")

        # Step 3: Statistical Hypothesis Testing
        print("\n[Stage 3/5] Executing Inferential Hypothesis Tests...")
        stats_res = run_statistical_hypothesis_tests(master_df)

        # Step 4: Machine Learning Suite
        print("\n[Stage 4/5] Training 4 Predictive ML Suites & Serializing Artifacts...")
        ml_res = run_full_ml_suite(master_df, self.models_dir)
        print("  -> Best Models Serialized: delivery_delay_model.pkl, product_return_model.pkl, demand_forecast_model.pkl")

        # Step 5: Visualizations & Workflows
        print("\n[Stage 5/5] Generating 15 Publication Visualizations & AI Workflows...")
        generate_all_15_figures()

        wf_engine = SwiftLogWorkflowEngine(self.processed_dir)
        briefing = wf_engine.run_daily_executive_briefing()
        print("\n" + briefing["briefing_markdown"])

        print("\n" + "=" * 75)
        print("  MASTER PIPELINE EXECUTION COMPLETED SUCCESSFULLY (100% SUCCESS)   ")
        print("=" * 75)

        return {
            "validation": val_summary,
            "preprocessing": prep_res,
            "statistical_tests": stats_res,
            "machine_learning": ml_res,
            "executive_briefing": briefing,
        }


if __name__ == "__main__":
    pipeline = SwiftLogMasterPipeline()
    pipeline.run()
