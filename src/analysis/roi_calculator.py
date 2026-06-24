"""
ROI Calculator - Calculate return on investment
"""

from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ROICalculator:
    """Calculate ROI for products"""
    
    def __init__(self, config: Dict):
        """
        Initialize calculator
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.prof_config = config.get("profitability", {})
        
        logger.info("✅ ROI Calculator initialized")
    
    def calculate(self, product: Dict) -> float:
        """
        Calculate ROI percentage
        
        Args:
            product: Product data
        
        Returns:
            ROI percentage
        """
        selling_price = product.get("price", 0)
        cogs = product.get("cogs_estimate", 0)
        
        if selling_price <= 0 or cogs <= 0:
            return 0.0
        
        # Calculate Amazon fees
        referral_fee = selling_price * self.prof_config.get("referral_fee_percentage", 15) / 100
        shipping_cost = self.prof_config.get("shipping_cost_per_unit", 2.50)
        prep_cost = self.prof_config.get("prep_cost_per_unit", 0.50)
        
        # Total costs
        total_cost = cogs + referral_fee + shipping_cost + prep_cost
        
        # Profit
        profit = selling_price - total_cost
        
        if cogs <= 0:
            return 0.0
        
        # ROI = (Profit / COGS) * 100
        roi = (profit / cogs) * 100
        
        return round(roi, 2)
    
    def get_break_even_volume(self, 
                             product: Dict,
                             monthly_fixed_costs: float = 0.0) -> int:
        """
        Calculate break-even unit volume
        
        Args:
            product: Product data
            monthly_fixed_costs: Fixed monthly costs
        
        Returns:
            Units needed to break even
        """
        selling_price = product.get("price", 0)
        cogs = product.get("cogs_estimate", 0)
        
        # Calculate profit per unit
        referral_fee = selling_price * self.prof_config.get("referral_fee_percentage", 15) / 100
        shipping_cost = self.prof_config.get("shipping_cost_per_unit", 2.50)
        prep_cost = self.prof_config.get("prep_cost_per_unit", 0.50)
        
        profit_per_unit = selling_price - cogs - referral_fee - shipping_cost - prep_cost
        
        if profit_per_unit <= 0:
            return float('inf')
        
        # Break-even volume
        break_even = int(monthly_fixed_costs / profit_per_unit) + 1
        
        return break_even
    
    def get_profit_breakdown(self, product: Dict) -> Dict:
        """
        Get detailed profit breakdown
        
        Args:
            product: Product data
        
        Returns:
            Profit breakdown dictionary
        """
        selling_price = product.get("price", 0)
        cogs = product.get("cogs_estimate", 0)
        
        referral_fee = selling_price * self.prof_config.get("referral_fee_percentage", 15) / 100
        shipping_cost = self.prof_config.get("shipping_cost_per_unit", 2.50)
        prep_cost = self.prof_config.get("prep_cost_per_unit", 0.50)
        
        total_fees = referral_fee + shipping_cost + prep_cost
        profit = selling_price - cogs - total_fees
        
        profit_margin = (profit / selling_price * 100) if selling_price > 0 else 0
        
        return {
            "selling_price": round(selling_price, 2),
            "cogs": round(cogs, 2),
            "referral_fee": round(referral_fee, 2),
            "shipping_cost": round(shipping_cost, 2),
            "prep_cost": round(prep_cost, 2),
            "total_fees": round(total_fees, 2),
            "profit_per_unit": round(profit, 2),
            "profit_margin_percentage": round(profit_margin, 2)
        }
