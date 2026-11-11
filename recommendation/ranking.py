
def _to_number(value):
    """Convert a value to a number safely."""
    try:
        if value is None or value == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _passes_hard_filters(product, preferences):
    """Remove products that do not satisfy mandatory requirements."""

    price = _to_number(product.get("price"))
    max_price = _to_number(preferences.get("max_price"))

    ram = _to_number(product.get("ram_gb"))
    min_ram = _to_number(preferences.get("min_ram_gb"))

    # Exclude products that exceed the maximum budget
    if max_price is not None:
        if price is None or price > max_price:
            return False

    # Exclude products that do not meet minimum RAM
    if min_ram is not None:
        if ram is None or ram < min_ram:
            return False

    return True


def _calculate_score(product, preferences):
    """Calculate a product match score out of 100."""

    score = 0
    reasons = []

    price = _to_number(product.get("price"))
    max_price = _to_number(preferences.get("max_price"))

    ram = _to_number(product.get("ram_gb"))
    min_ram = _to_number(preferences.get("min_ram_gb"))

    battery = _to_number(product.get("battery_mah"))
    min_battery = _to_number(preferences.get("min_battery_mah"))

    rating = _to_number(product.get("rating"))

    preferred_brand = preferences.get("preferred_brand")

    # Budget score: 30 points
    if max_price is not None and price is not None and max_price > 0:
        score += 30
        reasons.append("Within your stated budget")

    # RAM score: 25 points
    if min_ram is not None and ram is not None and ram >= min_ram:
        score += 25
        reasons.append(f"Meets the {min_ram:g} GB RAM requirement")

    # Battery score: 20 points
    if min_battery is not None and battery is not None:
        if battery >= min_battery:
            score += 20
            reasons.append("Meets your battery requirement")

    # Preferred brand score: 15 points
    if preferred_brand:
        product_brand = str(product.get("brand", "")).strip()

        if product_brand.lower() == str(preferred_brand).strip().lower():
            score += 15
            reasons.append(f"Matches your preferred brand: {preferred_brand}")

    # Customer rating score: 10 points
    if rating is not None:
        score += max(0, min(rating, 5)) / 5 * 10
        reasons.append("Has a listed customer rating")

    return round(score, 1), reasons


def rank_products(products, preferences=None):
    """
    Filter and rank products according to user preferences.

    Returns a list of products sorted by match score.
    """

    preferences = preferences or {}
    ranked_products = []

    for original_product in products:
        product = dict(original_product)

        # Apply mandatory filters
        if not _passes_hard_filters(product, preferences):
            continue

        # Calculate match score
        score, reasons = _calculate_score(product, preferences)

        product["match_score"] = score

        product["recommendation_reason"] = (
            "; ".join(reasons)
            if reasons
            else "No preference details matched; compare the available specifications."
        )

        ranked_products.append(product)

    # Sort by score, then by rating
    ranked_products.sort(
        key=lambda item: (
            item["match_score"],
            _to_number(item.get("rating")) or 0
        ),
        reverse=True
    )

    return ranked_products
