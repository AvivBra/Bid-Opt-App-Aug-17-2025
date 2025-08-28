"""Keyword campaign processor for all keyword-based campaigns."""

import pandas as pd
from typing import Dict, List
from .base_processor import BaseCampaignProcessor
import logging


class KeywordProcessor(BaseCampaignProcessor):
    """Processor for all keyword-based campaigns (Testing, Phrase, Broad, Halloween variants)."""

    def __init__(self, campaign_type: str):
        """Initialize keyword processor with specific campaign type.
        
        Args:
            campaign_type: Type of campaign (Testing, Phrase, Broad, Halloween Testing, etc.)
        """
        super().__init__()
        self.campaign_type = campaign_type
        self.logger = logging.getLogger(f"{self.__class__.__name__}.{campaign_type}")
        
        # Set campaign-specific configurations
        self.bid_column = self._get_bid_column()
        self.match_type = self._get_match_type()
        self.campaign_prefix = self._get_campaign_prefix()

    def _get_bid_column(self) -> str:
        """Get the bid column name for this campaign type."""
        bid_columns = {
            "Testing": "Testing Bid",
            "Phrase": "Phrase Bid",
            "Broad": "Broad Bid",
            "Halloween Testing": "Halloween Testing Bid",
            "Halloween Phrase": "Halloween Phrase Bid",
            "Halloween Broad": "Halloween Broad Bid"
        }
        return bid_columns.get(self.campaign_type, "Testing Bid")

    def _get_match_type(self) -> str:
        """Get the match type for this campaign type."""
        match_types = {
            "Testing": "exact",
            "Phrase": "phrase",
            "Broad": "broad",
            "Halloween Testing": "exact",
            "Halloween Phrase": "phrase",
            "Halloween Broad": "broad"
        }
        return match_types.get(self.campaign_type, "exact")

    def _get_campaign_prefix(self) -> str:
        """Get the campaign ID prefix for this campaign type."""
        prefixes = {
            "Testing": "Testing",
            "Phrase": "Phrase",
            "Broad": "Broad",
            "Halloween Testing": "Testing | Halloween",
            "Halloween Phrase": "Halloween Phrase",
            "Halloween Broad": "Halloween Broad"
        }
        return prefixes.get(self.campaign_type, "Testing")

    def get_campaign_id(self, asin: str, product_type: str, niche: str) -> str:
        """Generate campaign ID for this campaign type."""
        return f"{self.campaign_prefix} | {asin} | {product_type} | {niche}"

    def get_daily_budget(self) -> float:
        """Get daily budget - always 1.00 for all keyword campaigns."""
        return 1.00

    def get_default_bid(self) -> float:
        """Get default bid - always 0.15 for all keyword campaigns."""
        return 0.15

    def get_bid_from_template(self, template_row: pd.Series, bid_column: str, default_bid: float) -> float:
        """Get bid value from template row.
        
        Args:
            template_row: Row from template DataFrame
            bid_column: Name of bid column to use
            default_bid: Default bid if not found
            
        Returns:
            Bid value as float
        """
        try:
            bid_value = template_row.get(bid_column, default_bid)
            if pd.isna(bid_value) or bid_value == "" or bid_value == 0:
                return default_bid
            return float(bid_value)
        except (ValueError, TypeError):
            self.logger.warning(f"Invalid bid value in {bid_column}, using default: {default_bid}")
            return default_bid

    def process(self, template_df: pd.DataFrame, session_table: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Process keyword campaign data.
        
        Args:
            template_df: Template DataFrame
            session_table: Filtered session table
            
        Returns:
            Dictionary with sheet names and DataFrames
        """
        # Create sheets
        campaign_df = pd.DataFrame(self.create_campaign_rows(template_df, session_table))
        ad_group_df = pd.DataFrame(self.create_ad_group_rows(template_df, session_table))
        product_ad_df = pd.DataFrame(self.create_product_ad_rows(template_df, session_table))
        keyword_df = pd.DataFrame(self.create_keyword_rows(template_df, session_table))
        
        # For sheets with single representative row (Campaign, Ad Group, Product Ad),
        # keep only the first keyword for each campaign
        if not keyword_df.empty:
            # Get first keyword for each campaign
            first_keywords = keyword_df.groupby("Campaign ID").first().reset_index()
            
            # Add first keyword to non-keyword sheets for representation
            if not campaign_df.empty:
                campaign_df = self._add_keyword_columns(campaign_df, first_keywords)
            if not ad_group_df.empty:
                ad_group_df = self._add_keyword_columns(ad_group_df, first_keywords)
            if not product_ad_df.empty:
                product_ad_df = self._add_keyword_columns(product_ad_df, first_keywords)
        
        return {
            "Campaign": campaign_df,
            "Ad Group": ad_group_df,
            "Product Ad": product_ad_df,
            "Keyword": keyword_df
        }

    def create_campaign_rows(self, template_df: pd.DataFrame, session_table: pd.DataFrame) -> List[Dict]:
        """Create campaign entity rows."""
        rows = []
        campaigns_processed = set()
        
        for _, template_row in template_df.iterrows():
            asin = str(template_row.get("My ASIN", ""))
            product_type = str(template_row.get("Product Type", ""))
            niche = str(template_row.get("Niche", ""))
            
            if not asin or not product_type or not niche:
                continue
            
            campaign_id = self.get_campaign_id(asin, product_type, niche)
            
            # Only create one row per campaign
            if campaign_id in campaigns_processed:
                continue
            campaigns_processed.add(campaign_id)
            
            row = self.create_empty_row()
            row["Product"] = "Sponsored Products"
            row["Entity"] = "Campaign"
            row["Operation"] = "Create"
            row["Campaign ID"] = campaign_id
            row["Campaign Name"] = campaign_id
            row["Campaign Daily Budget"] = str(self.get_daily_budget())
            row["Campaign Start Date"] = pd.Timestamp.now().strftime("%Y%m%d")
            row["Campaign Targeting Type"] = "MANUAL"
            row["Campaign Status"] = "enabled"
            row["Campaign Bidding Strategy"] = "Dynamic bids - down only"
            
            rows.append(row)
        
        return rows

    def create_ad_group_rows(self, template_df: pd.DataFrame, session_table: pd.DataFrame) -> List[Dict]:
        """Create ad group entity rows."""
        rows = []
        ad_groups_processed = set()
        
        for _, template_row in template_df.iterrows():
            asin = str(template_row.get("My ASIN", ""))
            product_type = str(template_row.get("Product Type", ""))
            niche = str(template_row.get("Niche", ""))
            
            if not asin or not product_type or not niche:
                continue
            
            campaign_id = self.get_campaign_id(asin, product_type, niche)
            ad_group_id = asin
            
            # Only create one row per ad group
            ad_group_key = f"{campaign_id}|{ad_group_id}"
            if ad_group_key in ad_groups_processed:
                continue
            ad_groups_processed.add(ad_group_key)
            
            row = self.create_empty_row()
            row["Product"] = "Sponsored Products"
            row["Entity"] = "Ad Group"
            row["Operation"] = "Create"
            row["Campaign ID"] = campaign_id
            row["Ad Group ID"] = ad_group_id
            row["Ad Group Name"] = ad_group_id
            row["Ad Group Default Bid"] = str(self.get_default_bid())
            row["Ad Group Status"] = "enabled"
            
            rows.append(row)
        
        return rows

    def create_product_ad_rows(self, template_df: pd.DataFrame, session_table: pd.DataFrame) -> List[Dict]:
        """Create product ad entity rows."""
        rows = []
        ads_processed = set()
        
        for _, template_row in template_df.iterrows():
            asin = str(template_row.get("My ASIN", ""))
            product_type = str(template_row.get("Product Type", ""))
            niche = str(template_row.get("Niche", ""))
            
            if not asin or not product_type or not niche:
                continue
            
            campaign_id = self.get_campaign_id(asin, product_type, niche)
            ad_group_id = asin
            
            # Only create one row per product ad
            ad_key = f"{campaign_id}|{ad_group_id}"
            if ad_key in ads_processed:
                continue
            ads_processed.add(ad_key)
            
            row = self.create_empty_row()
            row["Product"] = "Sponsored Products"
            row["Entity"] = "Product Ad"
            row["Operation"] = "Create"
            row["Campaign ID"] = campaign_id
            row["Ad Group ID"] = ad_group_id
            row["ASIN"] = asin
            row["Status"] = "enabled"
            
            rows.append(row)
        
        return rows

    def create_keyword_rows(self, template_df: pd.DataFrame, session_table: pd.DataFrame) -> List[Dict]:
        """Create keyword entity rows."""
        rows = []
        processed_keywords = set()
        
        self.logger.info(f"Template has {len(template_df)} rows")
        self.logger.info(f"Session table has {len(session_table)} rows")
        
        # Get unique campaign configurations from template
        for template_idx, template_row in template_df.iterrows():
            asin = str(template_row.get("My ASIN", ""))
            product_type = str(template_row.get("Product Type", ""))
            niche = str(template_row.get("Niche", ""))
            
            self.logger.info(f"Template row {template_idx}: ASIN='{asin}', Product Type='{product_type}', Niche='{niche}'")
            
            if not asin or not product_type or not niche:
                self.logger.warning(f"Skipping template row {template_idx}: missing required fields")
                continue
            
            campaign_id = self.get_campaign_id(asin, product_type, niche)
            ad_group_id = asin
            
            # Get bid value for this campaign
            bid = self.get_bid_from_template(template_row, self.bid_column, self.get_default_bid())
            self.logger.info(f"Campaign ID: '{campaign_id}', Bid: {bid}")
            
            # Filter session table for this campaign's keywords
            campaign_keywords = session_table[
                (session_table["ASIN"] == asin) &
                (session_table["Product Type"] == product_type) &
                (session_table["Niche"] == niche)
            ]
            
            self.logger.info(f"Found {len(campaign_keywords)} matching keywords for {asin}")
            
            # Create keyword row for each target that's not an ASIN
            for _, session_row in campaign_keywords.iterrows():
                target = str(session_row.get("target", ""))
                
                # Skip if target is an ASIN (starts with B0)
                if target.startswith("B0"):
                    continue
                
                # Check if keyword has required Data Rova info
                kw_sales = session_row.get("kw sales", 0)
                kw_cvr = session_row.get("kw cvr", 0)
                
                self.logger.info(f"Keyword '{target}': sales={kw_sales}, cvr={kw_cvr}")
                
                # Only include keywords meeting thresholds
                if kw_sales > 0 and kw_cvr > 0.08:
                    row = self.create_empty_row()
                    row["Product"] = "Sponsored Products"
                    row["Entity"] = "Keyword"
                    row["Operation"] = "Create"
                    row["Campaign ID"] = campaign_id
                    row["Campaign Name"] = campaign_id
                    row["Ad Group ID"] = ad_group_id
                    row["Ad Group Name"] = ad_group_id
                    row["Keyword Text"] = target
                    row["Match Type"] = self.match_type
                    row["State"] = "enabled"
                    row["Bid"] = str(bid)
                    
                    rows.append(row)
                    processed_keywords.add(target)
                    self.logger.info(f"Added keyword '{target}' with Campaign ID '{campaign_id}'")
        
        # Check for unprocessed keywords that might need fallback handling
        all_session_keywords = set()
        for _, session_row in session_table.iterrows():
            target = str(session_row.get("target", ""))
            if not target.startswith("B0") and target:
                kw_sales = session_row.get("kw sales", 0)
                kw_cvr = session_row.get("kw cvr", 0)
                if kw_sales > 0 and kw_cvr > 0.08:
                    all_session_keywords.add(target)
        
        unprocessed = all_session_keywords - processed_keywords
        if unprocessed:
            self.logger.warning(f"Keywords not matched to any template row: {list(unprocessed)}")
        
        self.logger.info(f"Created {len(rows)} keyword rows from {len(processed_keywords)} unique keywords")
        return rows

    def _add_keyword_columns(self, df: pd.DataFrame, keyword_df: pd.DataFrame) -> pd.DataFrame:
        """Add keyword columns to non-keyword entity sheets.
        
        Args:
            df: DataFrame to add keyword columns to
            keyword_df: DataFrame with keyword data
            
        Returns:
            DataFrame with keyword columns added
        """
        if df.empty or keyword_df.empty:
            return df
        
        # Merge with first keyword for each campaign
        df = df.merge(
            keyword_df[["Campaign ID", "Keyword Text", "Match Type", "Bid"]],
            on="Campaign ID",
            how="left"
        )
        
        # Ensure Bid column exists even if no keywords
        if "Bid" not in df.columns:
            df["Bid"] = ""
        
        return df