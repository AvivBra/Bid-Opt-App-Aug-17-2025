"""Base processor for campaign creation."""

import pandas as pd
from typing import Dict, List, Optional
from abc import ABC, abstractmethod
import logging
from datetime import datetime


class BaseCampaignProcessor(ABC):
    """Base class for campaign processors."""

    def __init__(self):
        """Initialize base processor."""
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Amazon bulk file columns
        self.columns = [
            "Product", "Entity", "Operation", "Campaign ID", "Ad Group ID",
            "Portfolio ID", "Ad ID", "Keyword ID", "Product Targeting ID",
            "Campaign Name", "Ad Group Name", "Start Date", "End Date",
            "Targeting Type", "State", "Daily Budget", "SKU", "ASIN",
            "Ad Group Default Bid", "Bid", "Keyword Text", "Native Language Keyword",
            "Native Language Locale", "Match Type", "Bidding Strategy",
            "Placement", "Percentage", "Product Targeting Expression"
        ]

    @abstractmethod
    def process(self, template_df: pd.DataFrame, session_table: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Process campaign data and create output sheets.
        
        Args:
            template_df: Template DataFrame
            session_table: Filtered session table for this campaign
            
        Returns:
            Dictionary with sheet names and DataFrames
        """
        pass

    @abstractmethod
    def get_campaign_id(self, asin: str, product_type: str, niche: str) -> str:
        """Generate campaign ID."""
        pass

    @abstractmethod
    def get_daily_budget(self) -> float:
        """Get daily budget for this campaign type."""
        pass

    @abstractmethod
    def get_default_bid(self) -> float:
        """Get default bid for this campaign type."""
        pass

    def create_empty_row(self) -> Dict:
        """Create empty row with all columns."""
        return {col: "" for col in self.columns}

    def create_campaign_rows(self, template_df: pd.DataFrame, session_table: pd.DataFrame) -> List[Dict]:
        """Create campaign entity rows."""
        rows = []
        processed_campaigns = set()
        
        for _, template_row in template_df.iterrows():
            asin = str(template_row.get("My ASIN", ""))
            product_type = str(template_row.get("Product Type", ""))
            niche = str(template_row.get("Niche", ""))
            
            if not asin or not product_type or not niche:
                continue
                
            campaign_id = self.get_campaign_id(asin, product_type, niche)
            
            # Only create one row per unique campaign
            if campaign_id not in processed_campaigns:
                row = self.create_empty_row()
                row["Product"] = "Sponsored Products"
                row["Entity"] = "Campaign"
                row["Operation"] = "Create"
                row["Campaign ID"] = campaign_id
                row["Campaign Name"] = campaign_id
                row["Start Date"] = datetime.now().strftime("%Y%m%d")
                row["Targeting Type"] = "MANUAL"
                row["State"] = "enabled"
                row["Daily Budget"] = str(self.get_daily_budget())
                row["Bidding Strategy"] = "Dynamic bids - down only"
                
                rows.append(row)
                processed_campaigns.add(campaign_id)
        
        return rows

    def create_ad_group_rows(self, template_df: pd.DataFrame, session_table: pd.DataFrame) -> List[Dict]:
        """Create ad group entity rows."""
        rows = []
        processed_ad_groups = set()
        
        for _, template_row in template_df.iterrows():
            asin = str(template_row.get("My ASIN", ""))
            product_type = str(template_row.get("Product Type", ""))
            niche = str(template_row.get("Niche", ""))
            
            if not asin or not product_type or not niche:
                continue
                
            campaign_id = self.get_campaign_id(asin, product_type, niche)
            ad_group_id = asin
            
            # Only create one row per unique ad group
            key = f"{campaign_id}_{ad_group_id}"
            if key not in processed_ad_groups:
                row = self.create_empty_row()
                row["Product"] = "Sponsored Products"
                row["Entity"] = "Ad Group"
                row["Operation"] = "Create"
                row["Campaign ID"] = campaign_id
                row["Campaign Name"] = campaign_id
                row["Ad Group ID"] = ad_group_id
                row["Ad Group Name"] = ad_group_id
                row["State"] = "enabled"
                row["Ad Group Default Bid"] = str(self.get_default_bid())
                
                rows.append(row)
                processed_ad_groups.add(key)
        
        return rows

    def create_product_ad_rows(self, template_df: pd.DataFrame, session_table: pd.DataFrame) -> List[Dict]:
        """Create product ad entity rows."""
        rows = []
        processed_ads = set()
        
        for _, template_row in template_df.iterrows():
            asin = str(template_row.get("My ASIN", ""))
            product_type = str(template_row.get("Product Type", ""))
            niche = str(template_row.get("Niche", ""))
            
            if not asin or not product_type or not niche:
                continue
                
            campaign_id = self.get_campaign_id(asin, product_type, niche)
            ad_group_id = asin
            
            # Only create one row per unique product ad
            key = f"{campaign_id}_{ad_group_id}_{asin}"
            if key not in processed_ads:
                row = self.create_empty_row()
                row["Product"] = "Sponsored Products"
                row["Entity"] = "Product Ad"
                row["Operation"] = "Create"
                row["Campaign ID"] = campaign_id
                row["Campaign Name"] = campaign_id
                row["Ad Group ID"] = ad_group_id
                row["Ad Group Name"] = ad_group_id
                row["ASIN"] = asin
                row["State"] = "enabled"
                
                rows.append(row)
                processed_ads.add(key)
        
        return rows

    def get_bid_from_template(self, template_row: pd.Series, bid_column: str, default: float = 0.30) -> float:
        """Get bid value from template row."""
        bid = template_row.get(bid_column, default)
        if pd.isna(bid) or bid <= 0:
            return default
        return float(bid)
