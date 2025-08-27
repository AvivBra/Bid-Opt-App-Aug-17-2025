"""Halloween Testing campaign processor."""

import pandas as pd
from typing import Dict, List
from .base_processor import BaseCampaignProcessor


class HalloweenTestingProcessor(BaseCampaignProcessor):
    """Processor for Halloween Testing campaigns."""

    def __init__(self):
        """Initialize Halloween Testing processor."""
        super().__init__()
        self.campaign_type = "halloween_testing"
        self.bid_column = "Halloween Testing Bid"

    def get_campaign_id(self, asin: str, product_type: str, niche: str) -> str:
        """Generate campaign ID for Halloween Testing."""
        return f"Testing | Halloween | {asin} | {product_type} | {niche}"

    def get_daily_budget(self) -> float:
        """Get daily budget for Halloween Testing."""
        return 1.00

    def get_default_bid(self) -> float:
        """Get default bid for Halloween Testing."""
        return 0.15

    def process(self, template_df: pd.DataFrame, session_table: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Process Halloween Testing campaign data.
        
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

    def create_keyword_rows(self, template_df: pd.DataFrame, session_table: pd.DataFrame) -> List[Dict]:
        """Create keyword entity rows for Halloween Testing."""
        rows = []
        
        # Get unique campaign configurations from template
        for _, template_row in template_df.iterrows():
            asin = str(template_row.get("My ASIN", ""))
            product_type = str(template_row.get("Product Type", ""))
            niche = str(template_row.get("Niche", ""))
            
            if not asin or not product_type or not niche:
                continue
            
            campaign_id = self.get_campaign_id(asin, product_type, niche)
            ad_group_id = asin
            
            # Get bid value for this campaign
            bid = self.get_bid_from_template(template_row, self.bid_column, self.get_default_bid())
            
            # Filter session table for this campaign's keywords
            campaign_keywords = session_table[
                (session_table["ASIN"] == asin) &
                (session_table["Product Type"] == product_type) &
                (session_table["Niche"] == niche)
            ]
            
            # Create keyword row for each target that's not an ASIN
            for _, session_row in campaign_keywords.iterrows():
                target = str(session_row.get("target", ""))
                
                # Skip if target is an ASIN (starts with B0)
                if target.startswith("B0"):
                    continue
                
                # Check if keyword has required Data Rova info
                kw_sales = session_row.get("kw sales", 0)
                kw_cvr = session_row.get("kw cvr", 0)
                
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
                    row["Match Type"] = "exact"
                    row["State"] = "enabled"
                    row["Bid"] = str(bid)
                    
                    rows.append(row)
        
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
