import pytest
from src.phase2.product_research import ProductResearchEngine


def test_product_research_initialization():
    """Test product research engine initialization"""
    config = {"research": {}, "output": {}}
    engine = ProductResearchEngine(config)
    assert engine is not None


def test_product_filtering():
    """Test product filtering"""
    config = {
        "research": {
            "min_profit_margin": 15,
            "min_monthly_revenue": 2000,
            "max_sellers_count": 50,
            "min_review_count": 50,
            "min_rating": 4.0
        },
        "output": {}
    }
    
    engine = ProductResearchEngine(config)
    
    # Test products
    products = [
        {"margin_percentage": 20, "monthly_revenue_estimate": 3000, "sellers_count": 20,
         "review_count": 100, "rating": 4.5},
        {"margin_percentage": 5, "monthly_revenue_estimate": 1000, "sellers_count": 60,
         "review_count": 30, "rating": 3.5},
    ]
    
    filtered = engine._filter_products(products)
    assert len(filtered) == 1


if __name__ == "__main__":
    pytest.main([__file__])
