"""
Helium 10 API Integration
Integrate with Helium 10 for keyword research and sales estimates
"""

import requests
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class Helium10:
    """Helium 10 API client"""
    
    BASE_URL = "https://api.helium10.com/v1"
    
    def __init__(self, api_key: str):
        """
        Initialize Helium 10 client
        
        Args:
            api_key: Helium 10 API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
        logger.info("✅ Helium 10 API initialized")
    
    def get_product_research(self, keyword: str, marketplace: str = "amazon_us") -> Dict:
        """
        Get product research data
        
        Args:
            keyword: Search keyword
            marketplace: Marketplace (amazon_us, amazon_uk, etc.)
        
        Returns:
            Product research data
        """
        try:
            payload = {
                "keyword": keyword,
                "marketplace": marketplace
            }
            
            logger.info(f"📊 Requesting product research for: {keyword}")
            response = self.session.post(f"{self.BASE_URL}/product-research", json=payload)
            response.raise_for_status()
            
            return response.json()
        
        except Exception as e:
            logger.error(f"❌ Helium 10 error: {str(e)}")
            return {}
    
    def get_keyword_data(self, keyword: str, marketplace: str = "amazon_us") -> Dict:
        """
        Get keyword research data
        
        Args:
            keyword: Search keyword
            marketplace: Marketplace
        
        Returns:
            Keyword data
        """
        try:
            payload = {
                "keyword": keyword,
                "marketplace": marketplace
            }
            
            logger.info(f"🔍 Researching keyword: {keyword}")
            response = self.session.post(f"{self.BASE_URL}/keyword-data", json=payload)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "keyword": keyword,
                "search_volume": data.get("search_volume", 0),
                "revenue_estimate": data.get("revenue_estimate", 0),
                "trend": data.get("trend", "stable"),
                "keyword_difficulty": data.get("keyword_difficulty", 0)
            }
        
        except Exception as e:
            logger.error(f"❌ Keyword research error: {str(e)}")
            return {}
    
    def get_estimated_monthly_sales(self, asin: str, marketplace: str = "amazon_us") -> Dict:
        """
        Get estimated monthly sales for ASIN
        
        Args:
            asin: Amazon ASIN
            marketplace: Marketplace
        
        Returns:
            Sales estimate data
        """
        try:
            payload = {
                "asin": asin,
                "marketplace": marketplace
            }
            
            logger.info(f"📈 Getting sales estimate for ASIN: {asin}")
            response = self.session.post(f"{self.BASE_URL}/sales-estimate", json=payload)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "asin": asin,
                "monthly_sales": data.get("monthly_sales", 0),
                "monthly_revenue": data.get("monthly_revenue", 0),
                "confidence_level": data.get("confidence", "low")
            }
        
        except Exception as e:
            logger.error(f"❌ Sales estimate error: {str(e)}")
            return {}
    
    def get_competitor_analysis(self, keyword: str, marketplace: str = "amazon_us") -> List[Dict]:
        """
        Get competitor analysis
        
        Args:
            keyword: Search keyword
            marketplace: Marketplace
        
        Returns:
            List of competitor data
        """
        try:
            payload = {
                "keyword": keyword,
                "marketplace": marketplace,
                "limit": 20
            }
            
            logger.info(f"🏆 Analyzing competitors for: {keyword}")
            response = self.session.post(f"{self.BASE_URL}/competitors", json=payload)
            response.raise_for_status()
            
            competitors = response.json().get("competitors", [])
            
            return [
                {
                    "asin": comp.get("asin"),
                    "title": comp.get("title"),
                    "price": comp.get("price"),
                    "rating": comp.get("rating"),
                    "reviews": comp.get("reviews"),
                    "estimated_sales": comp.get("estimated_sales")
                }
                for comp in competitors
            ]
        
        except Exception as e:
            logger.error(f"❌ Competitor analysis error: {str(e)}")
            return []
    
    def get_listing_optimization_score(self, asin: str, marketplace: str = "amazon_us") -> Dict:
        """
        Get listing optimization score
        
        Args:
            asin: Amazon ASIN
            marketplace: Marketplace
        
        Returns:
            Optimization score data
        """
        try:
            payload = {
                "asin": asin,
                "marketplace": marketplace
            }
            
            logger.info(f"🎯 Getting listing score for ASIN: {asin}")
            response = self.session.post(f"{self.BASE_URL}/listing-score", json=payload)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "asin": asin,
                "overall_score": data.get("overall_score", 0),
                "title_score": data.get("title_score", 0),
                "bullet_score": data.get("bullet_score", 0),
                "description_score": data.get("description_score", 0),
                "suggestions": data.get("suggestions", [])
            }
        
        except Exception as e:
            logger.error(f"❌ Listing score error: {str(e)}")
            return {}
