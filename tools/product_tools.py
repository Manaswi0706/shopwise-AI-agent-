"""
Agent Tools Definition Module
Provides clean wrapper functions with structured logging for the agent orchestrator.
"""

from typing import Any, Dict, List, Optional
from database.products import (
    search_products,
    check_stock,
    compare_products,
    add_to_shortlist,
    get_shortlist,
    get_product_by_id,
)
from recommendation.ranker import rank_products, check_compatibility


def tool_search_catalogue(
    query: Optional[str] = None,
    max_price: Optional[float] = None,
    min_ram: Optional[int] = None,
    category: Optional[str] = None,
    brand: Optional[str] = None
) -> Dict[str, Any]:
    """Search sample catalogue for products matching the given constraints."""
    items = search_products(
        query=query,
        max_price=max_price,
        min_ram=min_ram,
        category=category,
        brand=brand
    )
    return {
        "tool_name": "search_products",
        "parameters": {
            "query": query,
            "max_price": max_price,
            "min_ram": min_ram,
            "category": category,
            "brand": brand,
        },
        "count": len(items),
        "results": items,
    }


def tool_check_stock(product_id: str) -> Dict[str, Any]:
    """Check inventory stock levels for a sample product."""
    res = check_stock(product_id)
    return {
        "tool_name": "check_stock",
        "parameters": {"product_id": product_id},
        "result": res,
    }


def tool_compare_products(product_id_1: str, product_id_2: str) -> Dict[str, Any]:
    """Compare two products in the catalogue."""
    res = compare_products(product_id_1, product_id_2)
    return {
        "tool_name": "compare_products",
        "parameters": {"product_id_1": product_id_1, "product_id_2": product_id_2},
        "result": res,
    }


def tool_check_compatibility(device_id: str, accessory_id: str) -> Dict[str, Any]:
    """Check compatibility between host device and accessory."""
    res = check_compatibility(device_id, accessory_id)
    return {
        "tool_name": "check_compatibility",
        "parameters": {"device_id": device_id, "accessory_id": accessory_id},
        "result": res,
    }


def tool_add_to_shortlist(product_id: str, customer_id: str = "demo-user") -> Dict[str, Any]:
    """Save a product to customer shortlist."""
    res = add_to_shortlist(product_id, customer_id)
    return {
        "tool_name": "add_to_shortlist",
        "parameters": {"product_id": product_id, "customer_id": customer_id},
        "result": res,
    }


def tool_get_shortlist(customer_id: str = "demo-user") -> Dict[str, Any]:
    """Retrieve customer's shortlisted products."""
    res = get_shortlist(customer_id)
    return {
        "tool_name": "get_shortlist",
        "parameters": {"customer_id": customer_id},
        "result": res,
    }


def tool_rank_products(
    products: List[Dict[str, Any]],
    preferences: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Rank products based on preferences."""
    ranked = rank_products(products, preferences)
    return {
        "tool_name": "rank_products",
        "parameters": {"preferences": preferences, "input_count": len(products)},
        "ranked_count": len(ranked),
        "results": ranked,
    }
