"""
Database Manager for storing research data
"""

import sqlite3
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manage SQLite database for research data"""
    
    def __init__(self, db_path: str = "data/wholesale_automation.db"):
        """
        Initialize database
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
        logger.info(f"✅ Database initialized: {db_path}")
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                asin TEXT UNIQUE,
                product_name TEXT,
                brand TEXT,
                category TEXT,
                price REAL,
                monthly_sales INTEGER,
                margin_percentage REAL,
                sellers_count INTEGER,
                rating REAL,
                bsr INTEGER,
                cogs REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Distributors table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS distributors (
                id INTEGER PRIMARY KEY,
                distributor_name TEXT UNIQUE,
                brand TEXT,
                email TEXT,
                phone TEXT,
                website TEXT,
                authorization_status TEXT,
                verified BOOLEAN DEFAULT 0,
                risk_level TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Opportunities table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS opportunities (
                id INTEGER PRIMARY KEY,
                product_id INTEGER,
                distributor_id INTEGER,
                opportunity_score REAL,
                roi_percentage REAL,
                rank TEXT,
                recommendation TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(product_id) REFERENCES products(id),
                FOREIGN KEY(distributor_id) REFERENCES distributors(id)
            )
        """)
        
        # Research runs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS research_runs (
                id INTEGER PRIMARY KEY,
                run_name TEXT,
                categories TEXT,
                products_count INTEGER,
                distributors_found INTEGER,
                opportunities_scored INTEGER,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def insert_product(self, product: Dict) -> int:
        """
        Insert product record
        
        Args:
            product: Product data
        
        Returns:
            Product ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO products
                (asin, product_name, brand, category, price, monthly_sales, 
                 margin_percentage, sellers_count, rating, bsr, cogs)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                product.get("asin"),
                product.get("product_name"),
                product.get("brand"),
                product.get("category"),
                product.get("price"),
                product.get("monthly_sales_estimate"),
                product.get("margin_percentage"),
                product.get("sellers_count"),
                product.get("rating"),
                product.get("bsr"),
                product.get("cogs_estimate")
            ))
            
            conn.commit()
            product_id = cursor.lastrowid
            logger.info(f"✅ Product inserted: {product.get('asin')}")
            return product_id
        
        except Exception as e:
            logger.error(f"❌ Error inserting product: {str(e)}")
            return -1
        finally:
            conn.close()
    
    def insert_distributor(self, distributor: Dict) -> int:
        """
        Insert distributor record
        
        Args:
            distributor: Distributor data
        
        Returns:
            Distributor ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO distributors
                (distributor_name, brand, email, phone, website, 
                 authorization_status, verified, risk_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                distributor.get("distributor_name"),
                distributor.get("brand"),
                distributor.get("email"),
                distributor.get("phone"),
                distributor.get("website"),
                distributor.get("authorization_status"),
                distributor.get("verified", False),
                distributor.get("risk_level", "medium")
            ))
            
            conn.commit()
            distributor_id = cursor.lastrowid
            logger.info(f"✅ Distributor inserted: {distributor.get('distributor_name')}")
            return distributor_id
        
        except Exception as e:
            logger.error(f"❌ Error inserting distributor: {str(e)}")
            return -1
        finally:
            conn.close()
    
    def get_products(self, limit: int = 100) -> List[Dict]:
        """
        Get products from database
        
        Args:
            limit: Maximum number of results
        
        Returns:
            List of products
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM products ORDER BY margin_percentage DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()
    
    def get_distributors(self, brand: Optional[str] = None) -> List[Dict]:
        """
        Get distributors from database
        
        Args:
            brand: Optional brand filter
        
        Returns:
            List of distributors
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            if brand:
                cursor.execute("SELECT * FROM distributors WHERE brand = ? ORDER BY created_at DESC", (brand,))
            else:
                cursor.execute("SELECT * FROM distributors ORDER BY created_at DESC")
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()
    
    def get_opportunities(self, limit: int = 50) -> List[Dict]:
        """
        Get top opportunities
        
        Args:
            limit: Maximum number of results
        
        Returns:
            List of opportunities
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT o.*, p.product_name, p.asin, p.brand, d.distributor_name, d.email, d.phone
                FROM opportunities o
                JOIN products p ON o.product_id = p.id
                JOIN distributors d ON o.distributor_id = d.id
                ORDER BY o.opportunity_score DESC
                LIMIT ?
            """, (limit,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()
