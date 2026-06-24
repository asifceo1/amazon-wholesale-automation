"""
Keepa API Integration
Integrate with Keepa for historical pricing and sales data
"""

import requests
import time
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from functools import lru_cache

logger = logging.getLogger(__name__)


class KeepaPro:
    """Keepa API client for product research"""
    
    BASE_URL = "https://api.keepa.com"
    
    def __init__(self, api_key: str):
        """
        Initialize Keepa API client
        
        Args:
            api_key: Keepa API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.rate_limit_remaining = 100
        logger.info("✅ Keepa API initialized")
    
    def query_product(self, asin: str, domain: str = "US") -> Dict:
        """
        Query product data from Keepa
        
        Args:
            asin: Amazon ASIN
            domain: Amazon domain (US, UK, DE, etc.)
        
        Returns:
            Product data from Keepa
        """
        try:
            params = {
                "key": self.api_key,
                "domain": domain,
                "asin": asin,
                "stats": "30,60,90,180,365,all",
                "offers": "0",
                "history": "price,sales"
            }
            
            logger.info(f"📡 Querying Keepa for ASIN: {asin}")
            response = self.session.get(f"{self.BASE_URL}/product", params=params)
            
            # Update rate limit
            if "keepaliveToken" in response.headers:
                self.rate_limit_remaining = int(response.headers.get("X-RateLimit-Remaining", 100))
            
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") != 0:
                logger.error(f"❌ Keepa error: {data.get('message', 'Unknown error')}")
                return {}
            
            return self._parse_keepa_response(data.get("products", [{}])[0])
        
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Keepa API error: {str(e)}")
            return {}
    
    def query_products_batch(self, asins: List[str]) -> List[Dict]:
        """
        Query multiple products
        
        Args:
            asins: List of ASINs
        
        Returns:
            List of product data
        """
        results = []
        for asin in asins:
            result = self.query_product(asin)
            results.append(result)
            
            # Rate limiting
            if self.rate_limit_remaining < 10:
                logger.warning("⏳ Rate limit approaching, waiting...")
                time.sleep(60)
        
        return results
    
    def get_estimated_sales(self, asin: str) -> Dict:
        """
        Get estimated monthly sales
        
        Args:
            asin: Product ASIN
        
        Returns:
            Sales data
        """
        try:
            product = self.query_product(asin)
            sales_history = product.get("sales_history", [])
            
            if not sales_history:
                return {"monthly_sales": 0, "confidence": "low"}
            
            # Calculate average from last 30 days
            recent_sales = sales_history[-30:]
            avg_sales = sum(recent_sales) / len(recent_sales) if recent_sales else 0
            
            return {
                "monthly_sales": int(avg_sales * 30),
                "confidence": "medium",
                "data_points": len(sales_history)
            }
        
        except Exception as e:
            logger.error(f"❌ Error calculating sales: {str(e)}")
            return {"monthly_sales": 0, "confidence": "low"}
    
    def get_price_history(self, asin: str, days: int = 90) -> List[Tuple[datetime, float]]:
        """
        Get price history
        
        Args:
            asin: Product ASIN
            days: Number of days to retrieve
        
        Returns:
            List of (date, price) tuples
        """
        try:
            product = self.query_product(asin)
            price_history = product.get("price_history", [])
            
            # Convert timestamps and prices
            history = []
            for timestamp, price in price_history[-days:]:
                date = datetime.fromtimestamp(timestamp / 1000)
                history.append((date, price))
            
            return history
        
        except Exception as e:
            logger.error(f"❌ Error retrieving price history: {str(e)}")
            return []
    
    def get_bsr_data(self, asin: str) -> Dict:
        """
        Get Best Seller Rank data
        
        Args:
            asin: Product ASIN
        
        Returns:
            BSR data
        """
        try:
            product = self.query_product(asin)
            
            return {
                "current_bsr": product.get("bsr"),
                "bsr_history": product.get("bsr_history", []),
                "category": product.get("category", "Unknown")
            }
        
        except Exception as e:
            logger.error(f"❌ Error retrieving BSR: {str(e)}")
            return {}
    
    def search_by_keyword(self, keyword: str, domain: str = "US") -> List[str]:
        """
        Search products by keyword
        
        Args:
            keyword: Search keyword
            domain: Amazon domain
        
        Returns:
            List of ASINs
        """
        try:
            params = {
                "key": self.api_key,
                "domain": domain,
                "type": "search",
                "term": keyword,
                "stats": "30,90,180,365,all"
            }
            
            logger.info(f"🔍 Searching Keepa for: {keyword}")
            response = self.session.get(f"{self.BASE_URL}/search", params=params)
            response.raise_for_status()
            data = response.json()
            
            asins = []
            for product in data.get("products", []):
                if product.get("asin"):
                    asins.append(product["asin"])
            
            logger.info(f"✅ Found {len(asins)} products")
            return asins
        
        except Exception as e:
            logger.error(f"❌ Search error: {str(e)}")
            return []
    
    def _parse_keepa_response(self, product_data: Dict) -> Dict:
        """
        Parse Keepa response into useful format
        
        Args:
            product_data: Raw product data from Keepa
        
        Returns:
            Parsed product data
        """
        return {
            "asin": product_data.get("asin"),
            "title": product_data.get("title"),
            "brand": product_data.get("brand"),
            "category": product_data.get("category", [])[0] if product_data.get("category") else None,
            "current_price": product_data.get("current_price", [None, None])[1] / 100 if product_data.get("current_price") else None,
            "bsr": product_data.get("bsr", [None, None])[0] if product_data.get("bsr") else None,
            "rating": product_data.get("rating", [None, None])[1] / 10 if product_data.get("rating") else None,
            "reviews": product_data.get("reviews", [None, None])[1] if product_data.get("reviews") else None,
            "bsr_history": product_data.get("bsr", [[], []])[1],
            "price_history": product_data.get("price", [[], []])[1],
            "sales_history": product_data.get("sales", [[], []])[1]
        }
