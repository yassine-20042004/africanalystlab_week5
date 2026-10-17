"""Pytest End-to-End Pipeline Integration Test for SwiftLog."""
import pytest
from src.pipeline import SwiftLogMasterPipeline


def test_master_pipeline_initialization():
    pipe = SwiftLogMasterPipeline()
    assert pipe.raw_dir == "data/raw"
    assert pipe.processed_dir == "data/processed"


def test_master_pipeline_execution():
    pipe = SwiftLogMasterPipeline()
    res = pipe.run()
    assert res["validation"]["overall_passed"] is True
    assert res["preprocessing"]["master_shape"] == (5000, 38)
    assert "anova" in res["statistical_tests"]
    assert "best_delay_pipe" in res["machine_learning"]
    assert "briefing_markdown" in res["executive_briefing"]
