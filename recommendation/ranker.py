"""
Person 3: Recommendation Engine & Compatibility Module
Handles scoring and ranking candidate products against user preferences
and evaluating device-accessory compatibility.
"""

from typing import Any, Dict, List, Optional
from database.products import get_product_by_id


def rank_products(
    products: List[Dict[str, Any]],
    preferences: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Score and rank products based on user requirements and constraints.
    Adds 'match_score' (0-100) and 'recommendation_reason' to each item.
    """
    if not products:
        return []

    prefs = preferences or {}
    budget = prefs.get("max_price") or prefs.get("budget")
    min_ram = prefs.get("min_ram")
    preferred_brand = prefs.get("preferred_brand")

    ranked: List[Dict[str, Any]] = []

    for item in products:
        prod = dict(item)
        score = 50.0  # baseline score
        reasons = []

        # 1. Budget Evaluation (Weight: up to 30 points)
        price = prod.get("price")
        if budget is not None and price is not None:
            if price <= budget:
                savings = budget - price
                budget_score = 25.0 + min(5.0, (savings / budget) * 10)
                score += budget_score
                reasons.append(f"Within budget (₹{price:,.0f} <= ₹{budget:,.0f})")
            else:
                over = price - budget
                penalty = min(30.0, (over / budget) * 40.0)
                score -= penalty
                reasons.append(f"Exceeds budget by ₹{over:,.0f}")
        elif price is not None:
            score += 15.0

        # 2. RAM & Specification Evaluation (Weight: up to 20 points)
        ram = prod.get("ram_gb")
        if min_ram is not None and ram is not None:
            if ram >= min_ram:
                score += 20.0
                reasons.append(f"Meets RAM requirement ({ram} GB >= {min_ram} GB)")
            else:
                score -= 15.0
                reasons.append(f"Below target RAM ({ram} GB < {min_ram} GB)")
        elif ram is not None:
            score += min(20.0, ram * 2.0)

        # 3. Rating & Customer Satisfaction (Weight: up to 15 points)
        rating = prod.get("rating", 4.0)
        score += (rating / 5.0) * 15.0

        # 4. In-Stock Availability (Weight: up to 10 points)
        stock = prod.get("stock", 0)
        if stock > 0:
            score += 10.0
        else:
            score -= 20.0
            reasons.append("Currently out of stock")

        # 5. Brand Preference Match (Weight: up to 10 points)
        if preferred_brand and preferred_brand.lower() in prod.get("brand", "").lower():
            score += 10.0
            reasons.append(f"Matches preferred brand '{prod.get('brand')}'")

        # Normalize score into integer 0-100
        final_score = int(max(0, min(100, round(score))))
        prod["match_score"] = final_score

        # Combine specific reasons or fall back to default
        if reasons:
            prod["recommendation_reason"] = ". ".join(reasons) + "."
        elif not prod.get("recommendation_reason"):
            prod["recommendation_reason"] = "Good overall specifications in sample catalogue."

        ranked.append(prod)

    # Sort descending by match_score, then ascending by price
    ranked.sort(key=lambda x: (x.get("match_score", 0), -(x.get("price") or 999999)), reverse=True)
    return ranked


def check_compatibility(device_id: str, accessory_id: str) -> Dict[str, Any]:
    """
    Check hardware / software compatibility between a host device and an accessory.
    """
    dev = get_product_by_id(device_id)
    acc = get_product_by_id(accessory_id)

    if not dev or not acc:
        return {
            "compatible": False,
            "device": {"id": str(device_id), "name": dev.get("name") if dev else "Unknown Device"},
            "accessory": {"id": str(accessory_id), "name": acc.get("name") if acc else "Unknown Accessory"},
            "status": "Item not found in sample catalogue",
            "details": f"Could not verify compatibility because ID '{device_id}' or '{accessory_id}' is missing."
        }

    dev_compat_list = [str(x) for x in dev.get("compatible_accessories", [])]
    acc_compat_list = [str(x) for x in acc.get("compatible_with", [])]

    is_compatible = (str(accessory_id) in dev_compat_list) or (str(device_id) in acc_compat_list)

    if is_compatible:
        details = (
            f"'{acc.get('name')}' is verified compatible with '{dev.get('name')}'. "
            f"Both use matching interfaces/protocols ({acc.get('specs', {}).get('interface', 'standard')})."
        )
    else:
        details = (
            f"'{acc.get('name')}' does not have official compatibility registered with '{dev.get('name')}'. "
            "Verify connector types or dimensions before purchasing."
        )

    return {
        "compatible": is_compatible,
        "device": {"id": dev.get("product_id"), "name": dev.get("name"), "category": dev.get("category")},
        "accessory": {"id": acc.get("product_id"), "name": acc.get("name"), "category": acc.get("category")},
        "status": "Compatible" if is_compatible else "Not Verified Compatible",
        "details": details
    }
