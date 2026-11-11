"""
Person 2: Database and Catalogue Management Module
Provides mock database operations, inventory search, product comparison,
stock checks, and customer shortlisting.
"""

from typing import Any, Dict, List, Optional

# Sample Catalogue - Clearly labeled as sample/demo data
SAMPLE_CATALOGUE: List[Dict[str, Any]] = [
    {
        "product_id": "1",
        "name": "Samsung Galaxy M34 5G",
        "category": "smartphone",
        "brand": "Samsung",
        "price": 16999,
        "ram_gb": 8,
        "storage_gb": 128,
        "stock": 15,
        "rating": 4.3,
        "specs": {
            "display": "6.5-inch 120Hz Super AMOLED",
            "battery": "6000 mAh Monster Battery",
            "processor": "Exynos 1280 Octa-Core",
            "camera": "50MP No Shake Cam (OIS) + 8MP + 2MP",
            "os": "Android 13, One UI 5.1",
            "charger_in_box": False,
        },
        "compatible_accessories": ["5", "6", "7"],
        "recommendation_reason": "Top pick under ₹18,000 offering 8GB RAM, 120Hz sAMOLED display, and massive 6000 mAh battery."
    },
    {
        "product_id": "2",
        "name": "Redmi Note 13 5G",
        "category": "smartphone",
        "brand": "Xiaomi",
        "price": 17999,
        "ram_gb": 8,
        "storage_gb": 256,
        "stock": 22,
        "rating": 4.2,
        "specs": {
            "display": "6.67-inch 120Hz AMOLED, Slim Bezel",
            "battery": "5000 mAh Battery with 33W Fast Charge",
            "processor": "MediaTek Dimensity 6080 5G",
            "camera": "108MP 3X In-Sensor Zoom Triple Camera",
            "os": "MIUI 14 based on Android 13",
            "charger_in_box": True,
        },
        "compatible_accessories": ["5", "6", "8"],
        "recommendation_reason": "High storage capacity (256 GB) with sharp 108MP camera and fast 33W in-box charging."
    },
    {
        "product_id": "3",
        "name": "Realme Narzo 60x 5G",
        "category": "smartphone",
        "brand": "Realme",
        "price": 13499,
        "ram_gb": 6,
        "storage_gb": 128,
        "stock": 8,
        "rating": 4.1,
        "specs": {
            "display": "6.72-inch 120Hz Ultra Smooth Display",
            "battery": "5000 mAh with 33W SUPERVOOC Charge",
            "processor": "MediaTek Dimensity 6100+ 5G",
            "camera": "50MP AI Primary Camera",
            "os": "Realme UI 4.0 based on Android 13",
            "charger_in_box": True,
        },
        "compatible_accessories": ["5", "6"],
        "recommendation_reason": "Budget-friendly 5G smartphone with smooth 120Hz screen, although RAM is 6 GB."
    },
    {
        "product_id": "4",
        "name": "OnePlus Nord CE 3 Lite 5G",
        "category": "smartphone",
        "brand": "OnePlus",
        "price": 19499,
        "ram_gb": 8,
        "storage_gb": 128,
        "stock": 10,
        "rating": 4.4,
        "specs": {
            "display": "6.72-inch 120Hz FHD+ Adaptive Display",
            "battery": "5000 mAh with 67W SUPERVOOC Endurance",
            "processor": "Qualcomm Snapdragon 695 5G",
            "camera": "108MP Main Sensor + 2MP Depth + 2MP Macro",
            "os": "OxygenOS 13.1 based on Android 13",
            "charger_in_box": True,
        },
        "compatible_accessories": ["5", "6"],
        "recommendation_reason": "Slightly over ₹18,000 budget, but offers super-fast 67W charging and OxygenOS fluidity."
    },
    {
        "product_id": "5",
        "name": "Samsung 25W USB-C Power Adapter",
        "category": "accessory",
        "brand": "Samsung",
        "price": 1299,
        "ram_gb": None,
        "storage_gb": None,
        "stock": 45,
        "rating": 4.6,
        "specs": {
            "type": "Wall Charger",
            "interface": "USB Type-C",
            "power_output": "25W Super Fast Charging (PD 3.0 PPS)",
            "cable_included": False
        },
        "compatible_with": ["1", "2", "3", "4"],
        "recommendation_reason": "Official 25W Power Adapter, recommended for Samsung Galaxy M34 which does not include a charger."
    },
    {
        "product_id": "6",
        "name": "Samsung Galaxy Buds2 Wireless Earbuds",
        "category": "accessory",
        "brand": "Samsung",
        "price": 5499,
        "ram_gb": None,
        "storage_gb": None,
        "stock": 14,
        "rating": 4.5,
        "specs": {
            "type": "TWS Earbuds",
            "connectivity": "Bluetooth 5.2",
            "noise_cancellation": "Active Noise Cancellation (ANC)",
            "battery_life": "Up to 20 hours with charging case"
        },
        "compatible_with": ["1", "2", "3", "4"],
        "recommendation_reason": "Seamless pairing with Galaxy devices and high quality active noise cancellation."
    },
    {
        "product_id": "7",
        "name": "Spigen Rugged Armor Case for Galaxy M34 5G",
        "category": "accessory",
        "brand": "Spigen",
        "price": 899,
        "ram_gb": None,
        "storage_gb": None,
        "stock": 30,
        "rating": 4.7,
        "specs": {
            "type": "Protective Case",
            "material": "Thermoplastic Polyurethane (TPU)",
            "features": "Air Cushion Technology, Matte black carbon fiber design"
        },
        "compatible_with": ["1"],
        "recommendation_reason": "Military-grade certified drop protection custom tailored for Galaxy M34 5G."
    },
    {
        "product_id": "8",
        "name": "Xiaomi 33W SonicCharge 2.0 Fast Charger",
        "category": "accessory",
        "brand": "Xiaomi",
        "price": 999,
        "ram_gb": None,
        "storage_gb": None,
        "stock": 25,
        "rating": 4.4,
        "specs": {
            "type": "Wall Charger",
            "interface": "USB Type-A with Type-C cable included",
            "power_output": "33W Max SonicCharge",
            "cable_included": True
        },
        "compatible_with": ["2", "3"],
        "recommendation_reason": "Official 33W adapter compatible with Xiaomi / Redmi devices."
    }
]

# In-memory customer shortlist store
_SHORTLIST_STORE: Dict[str, List[str]] = {}


def get_product_by_id(product_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve a single product by its unique string ID."""
    p_id_str = str(product_id).strip()
    for product in SAMPLE_CATALOGUE:
        if str(product.get("product_id")) == p_id_str:
            return dict(product)
    return None


def search_products(
    query: Optional[str] = None,
    max_price: Optional[float] = None,
    min_ram: Optional[int] = None,
    category: Optional[str] = None,
    brand: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Search catalogue products matching given filters.
    All matching is non-destructive and queries sample demo data.
    """
    results: List[Dict[str, Any]] = []

    for item in SAMPLE_CATALOGUE:
        # Category filter
        if category and item.get("category", "").lower() != category.lower():
            continue

        # Max price filter
        price = item.get("price")
        if max_price is not None and price is not None and price > max_price:
            continue

        # Min RAM filter (only applicable if product has RAM specification)
        ram = item.get("ram_gb")
        if min_ram is not None:
            if ram is None or ram < min_ram:
                continue

        # Brand filter
        if brand and brand.lower() not in item.get("brand", "").lower():
            continue

        # Text query filter
        if query:
            q = query.lower()
            name_match = q in item.get("name", "").lower()
            brand_match = q in item.get("brand", "").lower()
            cat_match = q in item.get("category", "").lower()
            desc_match = any(q in str(v).lower() for v in item.get("specs", {}).values())
            if not (name_match or brand_match or cat_match or desc_match):
                continue

        results.append(dict(item))

    return results


def check_stock(product_id: str) -> Dict[str, Any]:
    """Check inventory stock levels for a sample product."""
    product = get_product_by_id(product_id)
    if not product:
        return {
            "product_id": str(product_id),
            "found": False,
            "status": "Product not found in catalogue",
            "stock_count": 0
        }

    count = product.get("stock", 0)
    status = "In Stock" if count > 0 else "Out of Stock"
    return {
        "product_id": str(product_id),
        "found": True,
        "product_name": product.get("name"),
        "stock_count": count,
        "status": status,
        "is_available": count > 0
    }


def compare_products(product_id_1: str, product_id_2: str) -> Dict[str, Any]:
    """Compare two products across key specifications and pricing."""
    p1 = get_product_by_id(product_id_1)
    p2 = get_product_by_id(product_id_2)

    if not p1 or not p2:
        return {
            "success": False,
            "error": f"One or both products not found: ID {product_id_1}, ID {product_id_2}"
        }

    p1_price = p1.get("price", 0)
    p2_price = p2.get("price", 0)
    price_diff = abs(p1_price - p2_price)

    if p1_price < p2_price:
        price_verdict = f"{p1.get('name')} is ₹{price_diff:,.0f} cheaper than {p2.get('name')}."
    elif p2_price < p1_price:
        price_verdict = f"{p2.get('name')} is ₹{price_diff:,.0f} cheaper than {p1.get('name')}."
    else:
        price_verdict = "Both products have identical pricing."

    comparison_matrix = {
        "Price": {
            p1.get("name"): f"₹{p1.get('price'):,.0f}",
            p2.get("name"): f"₹{p2.get('price'):,.0f}"
        },
        "RAM": {
            p1.get("name"): f"{p1.get('ram_gb')} GB" if p1.get("ram_gb") else "N/A",
            p2.get("name"): f"{p2.get('ram_gb')} GB" if p2.get("ram_gb") else "N/A"
        },
        "Storage": {
            p1.get("name"): f"{p1.get('storage_gb')} GB" if p1.get("storage_gb") else "N/A",
            p2.get("name"): f"{p2.get('storage_gb')} GB" if p2.get("storage_gb") else "N/A"
        },
        "Rating": {
            p1.get("name"): f"{p1.get('rating')} / 5.0",
            p2.get("name"): f"{p2.get('rating')} / 5.0"
        },
        "Stock": {
            p1.get("name"): f"{p1.get('stock')} units available",
            p2.get("name"): f"{p2.get('stock')} units available"
        }
    }

    # Add extra specs if available
    all_spec_keys = set(p1.get("specs", {}).keys()).union(set(p2.get("specs", {}).keys()))
    for key in sorted(all_spec_keys):
        spec_label = key.replace("_", " ").title()
        comparison_matrix[spec_label] = {
            p1.get("name"): str(p1.get("specs", {}).get(key, "-")),
            p2.get("name"): str(p2.get("specs", {}).get(key, "-"))
        }

    return {
        "success": True,
        "product_1": {"id": p1.get("product_id"), "name": p1.get("name")},
        "product_2": {"id": p2.get("product_id"), "name": p2.get("name")},
        "price_verdict": price_verdict,
        "matrix": comparison_matrix
    }


def add_to_shortlist(product_id: str, customer_id: str = "demo-user") -> Dict[str, Any]:
    """Add a product to the user's shortlisted favorites."""
    p_id_str = str(product_id).strip()
    product = get_product_by_id(p_id_str)
    if not product:
        return {
            "success": False,
            "message": f"Product ID {p_id_str} does not exist in sample catalogue."
        }

    c_id = customer_id.strip() if customer_id else "demo-user"
    if c_id not in _SHORTLIST_STORE:
        _SHORTLIST_STORE[c_id] = []

    if p_id_str not in _SHORTLIST_STORE[c_id]:
        _SHORTLIST_STORE[c_id].append(p_id_str)
        msg = f"Added '{product.get('name')}' (ID: {p_id_str}) to shortlist for {c_id}."
    else:
        msg = f"'{product.get('name')}' is already in the shortlist for {c_id}."

    return {
        "success": True,
        "customer_id": c_id,
        "product_id": p_id_str,
        "product_name": product.get("name"),
        "message": msg,
        "shortlist_count": len(_SHORTLIST_STORE[c_id])
    }


def get_shortlist(customer_id: str = "demo-user") -> Dict[str, Any]:
    """Retrieve all shortlisted items for a given customer."""
    c_id = customer_id.strip() if customer_id else "demo-user"
    product_ids = _SHORTLIST_STORE.get(c_id, [])

    items = []
    for pid in product_ids:
        p = get_product_by_id(pid)
        if p:
            items.append({
                "product_id": p.get("product_id"),
                "name": p.get("name"),
                "price": p.get("price"),
                "ram_gb": p.get("ram_gb"),
                "stock": p.get("stock")
            })

    return {
        "customer_id": c_id,
        "count": len(items),
        "items": items
    }
