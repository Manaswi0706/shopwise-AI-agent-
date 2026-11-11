
from recommendation.ranking import rank_products


def test_rank_products_filters_by_budget_and_ram():
    products = [
        {
            "name": "Phone A",
            "price": 18000,
            "ram_gb": 8,
            "rating": 4.5
        },
        {
            "name": "Phone B",
            "price": 25000,
            "ram_gb": 8,
            "rating": 4.8
        },
        {
            "name": "Phone C",
            "price": 15000,
            "ram_gb": 4,
            "rating": 4.2
        }
    ]

    preferences = {
        "max_price": 20000,
        "min_ram_gb": 8
    }

    result = rank_products(products, preferences)

    assert len(result) == 1
    assert result[0]["name"] == "Phone A"


def test_rank_products_adds_score_and_reason():
    products = [
        {
            "name": "Phone A",
            "price": 18000,
            "ram_gb": 8,
            "rating": 5
        }
    ]

    result = rank_products(products)

    assert "match_score" in result[0]
    assert "recommendation_reason" in result[0]
    assert result[0]["match_score"] == 10


def test_rank_products_empty_list():
    result = rank_products([])

    assert result == []


def test_rank_products_missing_ram_is_excluded_when_required():
    products = [
        {
            "name": "Phone A",
            "price": 15000,
            "rating": 4.5
        }
    ]

    preferences = {
        "min_ram_gb": 8
    }

    result = rank_products(products, preferences)

    assert result == []
