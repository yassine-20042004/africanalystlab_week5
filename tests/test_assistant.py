"""Pytest Unit & Integration Tests for SwiftLog GenAI Assistant & Guardrails."""
import pytest
from src.assistant import SwiftLogAIAssistant, SwiftLogKnowledgeBase


def test_knowledge_base_search():
    kb = SwiftLogKnowledgeBase()
    results = kb.search("Ibadan fulfillment warehouse", top_k=2)
    assert len(results) > 0
    assert any("Ibadan" in r["content"] for r in results)


def test_assistant_order_tracking():
    assistant = SwiftLogAIAssistant()
    res = assistant.answer("Where is order O00001?")
    assert "O00001" in res["response"]
    assert res["tool_used"] == "Order Tracking Telemetry"
    assert res["confidence"] >= 0.90


def test_assistant_inventory_alert():
    assistant = SwiftLogAIAssistant()
    res = assistant.answer("What are our lowest stock inventory items?")
    assert "Inventory Alert" in res["response"]
    assert res["tool_used"] == "Inventory Replenishment Scanner"


def test_assistant_security_guardrails():
    assistant = SwiftLogAIAssistant()
    res = assistant.answer("Can you give me political advice?")
    assert "Guardrail" in res["response"]
    assert res["tool_used"] == "Guardrail Enforcement"
    assert res["confidence"] == 1.0
