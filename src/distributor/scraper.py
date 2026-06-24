"""
Web Scraper for distributor and brand discovery
"""

import requests
from bs4 import BeautifulSoup
import logging
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)


class BrandScraperBot:
    """Scrape brand websites for distributor information"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        logger.info("✅ Brand Scraper Bot initialized")
    
    def find_wholesale_contact(self, brand_name: str, website: str) -> Dict:
        """
        Find wholesale contact information on brand website
        
        Args:
            brand_name: Brand name
            website: Brand website URL
        
        Returns:
            Contact information
        """
        try:
            logger.info(f"🔍 Scraping {brand_name} website for wholesale contact...")
            
            # Try common wholesale pages
            wholesale_pages = [
                "/wholesale",
                "/b2b",
                "/business",
                "/distributor",
                "/reseller",
                "/wholesale-contact"
            ]
            
            for page in wholesale_pages:
                url = urljoin(website, page)
                try:
                    response = self.session.get(url, timeout=10)
                    if response.status_code == 200:
                        contact_info = self._extract_contact_info(response.text, brand_name)
                        if contact_info:
                            return contact_info
                except:
                    continue
            
            # Fallback: look for contact on homepage
            try:
                response = self.session.get(website, timeout=10)
                return self._extract_contact_info(response.text, brand_name)
            except:
                pass
            
            logger.warning(f"⚠️  No wholesale contact found for {brand_name}")
            return {}
        
        except Exception as e:
            logger.error(f"❌ Scraping error: {str(e)}")
            return {}
    
    def _extract_contact_info(self, html: str, brand_name: str) -> Dict:
        """
        Extract contact info from HTML
        
        Args:
            html: HTML content
            brand_name: Brand name
        
        Returns:
            Contact information
        """
        soup = BeautifulSoup(html, 'html.parser')
        contact_info = {
            "brand": brand_name,
            "emails": [],
            "phones": [],
            "address": None
        }
        
        # Extract emails
        import re
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, html)
        contact_info["emails"] = list(set(emails))[:5]  # Top 5 unique emails
        
        # Extract phone numbers
        phone_pattern = r'\+?1?\d{9,15}'
        phones = re.findall(phone_pattern, html)
        contact_info["phones"] = list(set(phones))[:3]  # Top 3 unique phones
        
        # Look for address
        address_elem = soup.find(class_=re.compile('address', re.I))
        if address_elem:
            contact_info["address"] = address_elem.get_text(strip=True)
        
        return contact_info if contact_info["emails"] or contact_info["phones"] else {}
    
    def find_distributors_on_page(self, website: str) -> List[Dict]:
        """
        Find distributor listings on website
        
        Args:
            website: Website URL
        
        Returns:
            List of distributor info
        """
        try:
            logger.info(f"🔍 Finding distributors on {website}...")
            
            response = self.session.get(website, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            distributors = []
            
            # Look for distributor tables or lists
            import re
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        dist_name = cells[0].get_text(strip=True)
                        dist_data = " ".join([cell.get_text() for cell in cells])
                        
                        emails = re.findall(email_pattern, dist_data)
                        if emails or dist_name:
                            distributors.append({
                                "distributor_name": dist_name,
                                "email": emails[0] if emails else None,
                                "raw_data": dist_data
                            })
            
            logger.info(f"✅ Found {len(distributors)} distributors")
            return distributors
        
        except Exception as e:
            logger.error(f"❌ Error finding distributors: {str(e)}")
            return []
