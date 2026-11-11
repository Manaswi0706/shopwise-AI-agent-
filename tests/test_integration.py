"""
Integration tests for SmartCart AI agent and backend modules.
Validates the data contract agreed between Person 1, 2, 3, and 4.
"""

import sys
import os

# Add root directory to sys.path so imports mirror production execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.orchestrator import run_smartcart_agent
from database.products import (
    search_products,
    get_product_by_id,
    compare_products,
    check_stock,
    add_to_shortlist,
    get_shortlist,
    SAMPLE_CATALOGUE,
)
from recommendation.ranker import rank_products, check_compatibility


def test_catalogue_structure():
    """Verify sample catalogue is properly structured with required fields."""
    assert len(SAMPLE_CATALOGUE) > 0
    for product in SAMPLE_CATALOGUE:
        assert "product_id" in product
        assert "name" in product
        assert "category" in product
        assert "price" in product
        assert "stock" in product


def test_agent_contract_keys():
    """Verify that run_smartcart_agent returns all required interface keys."""
    result = run_smartcart_agent("Find phones under ₹18,000", session_id="test-session")

    expected_keys = [
        "answer",
        "requirements",
        "plan",
        "tool_results",
        "execution_trace",
        "ranked_products",
        "evaluation",
    ]
    for key in expected_keys:
        assert key in result, f"Missing expected key: {key}"

    assert isinstance(result["answer"], str)
    assert isinstance(result["requirements"], dict)
    assert isinstance(result["plan"], dict)
    assert "goal" in result["plan"]
    assert "steps" in result["plan"]
    assert isinstance(result["tool_results"], list)
    assert isinstance(result["execution_trace"], list)
    assert isinstance(result["ranked_products"], list)
    assert isinstance(result["evaluation"], dict)


def test_demo_prompt_1_search():
    """Test demo prompt 1: 'Find a phone under ₹18,000 with at least 8 GB RAM'."""
    prompt = "Find a phone under 18000 with at least 8 GB RAM"
    result = run_smartcart_agent(prompt, session_id="demo")

    assert len(result["ranked_products"]) > 0
    for prod in result["ranked_products"]:
        assert prod.get("price") <= 18000
        assert prod.get("ram_gb") >= 8
        assert "match_score" in prod
        assert "recommendation_reason" in prod


def test_demo_prompt_2_comparison():
    """Test demo prompt 2: 'Compare the top two options'."""
    prompt = "Compare the top two options"
    result = run_smartcart_agent(prompt, session_id="demo")

    assert "compare" in result["requirements"]["intent"]
    assert len(result["tool_results"]) > 0
    assert "vs" in result["answer"] or "Option" in result["answer"] or "Comparison" in result["answer"]


def test_demo_prompt_3_accessory_compatibility():
    """Test demo prompt 3: 'Find an accessory for product ID 1 and check compatibility'."""
    prompt = "Find an accessory for product ID 1 and check compatibility"
    result = run_smartcart_agent(prompt, session_id="demo")

    assert result["requirements"]["intent"] == "accessory_compatibility"
    assert len(result["ranked_products"]) > 0
    # Check compatibility verification
    compat_tools = [t for t in result["tool_results"] if t.get("tool_name") == "check_compatibility"]
    assert len(compat_tools) > 0


def test_demo_prompt_4_shortlist():
    """Test demo prompt 4: 'Add product ID 1 to my shortlist'."""
    cust_id = "test-user-shortlist"
    prompt = "Add product ID 1 to my shortlist"
    result = run_smartcart_agent(prompt, session_id=cust_id)

    assert result["requirements"]["intent"] == "shortlist"
    shortlist_data = get_shortlist(cust_id)
    assert shortlist_data["count"] >= 1
    shortlisted_ids = [item["product_id"] for item in shortlist_data["items"]]
    assert "1" in shortlisted_ids


def test_direct_comparison():
    """Test direct database compare_products function."""
    comp = compare_products("1", "2")
    assert comp["success"] is True
    assert "matrix" in comp
    assert "Price" in comp["matrix"]
    assert "RAM" in comp["matrix"]


def test_compatibility_checker():
    """Test compatibility logic between device and accessory."""
    # Product 1 is Samsung Galaxy M34, Product 5 is Samsung 25W Charger
    compat = check_compatibility("1", "5")
    assert compat["compatible"] is True

    # Check non-compatible or non-existent device
    invalid = check_compatibility("999", "5")
    assert invalid["compatible"] is False
