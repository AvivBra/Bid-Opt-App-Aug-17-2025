"""Campaign builder for creating campaign structures."""

import pandas as pd
from typing import Dict, List, Optional
import logging


class CampaignBuilder:
    """Builds campaign structures from processed data."""
    
    def __init__(self):
        """Initialize campaign builder."""
        self.logger = logging.getLogger(__name__)
    
    def build_campaign_structure(
        self,
        sheets_data: Dict[str, pd.DataFrame],
        campaign_type: str
    ) -> Dict[str, pd.DataFrame]:
        """Build complete campaign structure with all entities.
        
        Args:
            sheets_data: Dictionary of DataFrames from processor
            campaign_type: Type of campaign being built
            
        Returns:
            Dictionary with structured campaign data
        """
        try:
            # Validate input data
            if not sheets_data:
                self.logger.error("No sheets data provided")
                return {}
            
            # Expected sheets for campaign
            expected_sheets = ["Campaign", "Ad Group", "Product Ad", "Keyword"]
            
            # Check for missing sheets
            missing_sheets = [sheet for sheet in expected_sheets if sheet not in sheets_data]
            if missing_sheets:
                self.logger.warning(f"Missing sheets for {campaign_type}: {missing_sheets}")
            
            # Build structure
            structured_data = {}
            
            for sheet_name, df in sheets_data.items():
                if df is None or df.empty:
                    self.logger.warning(f"Empty or None DataFrame for sheet: {sheet_name}")
                    structured_data[sheet_name] = pd.DataFrame()
                else:
                    # Ensure proper column order
                    structured_df = self._ensure_column_order(df, sheet_name)
                    structured_data[sheet_name] = structured_df
            
            # Validate relationships between entities
            self._validate_entity_relationships(structured_data)
            
            return structured_data
        
        except Exception as e:
            self.logger.error(f"Error building campaign structure: {str(e)}")
            return sheets_data  # Return original data if building fails
    
    def _ensure_column_order(self, df: pd.DataFrame, entity_type: str) -> pd.DataFrame:
        """Ensure columns are in correct order for Amazon bulk upload.
        
        Args:
            df: DataFrame to reorder
            entity_type: Type of entity (Campaign, Ad Group, etc.)
            
        Returns:
            DataFrame with columns in correct order
        """
        # Standard column order for Amazon bulk files
        standard_columns = [
            "Product", "Entity", "Operation", "Campaign ID", "Ad Group ID",
            "Portfolio ID", "Ad ID", "Keyword ID", "Product Targeting ID",
            "Campaign Name", "Ad Group Name", "Start Date", "End Date",
            "Targeting Type", "State", "Daily Budget", "SKU", "ASIN",
            "Ad Group Default Bid", "Bid", "Keyword Text", "Native Language Keyword",
            "Native Language Locale", "Match Type", "Bidding Strategy",
            "Placement", "Percentage", "Product Targeting Expression"
        ]
        
        # Create new dataframe with standard column order
        ordered_df = pd.DataFrame()
        
        for col in standard_columns:
            if col in df.columns:
                ordered_df[col] = df[col]
            else:
                ordered_df[col] = ""
        
        # Add any extra columns that aren't in standard list (for debugging)
        extra_cols = [col for col in df.columns if col not in standard_columns]
        if extra_cols:
            self.logger.debug(f"Extra columns in {entity_type}: {extra_cols}")
            for col in extra_cols:
                ordered_df[col] = df[col]
        
        return ordered_df
    
    def _validate_entity_relationships(self, structured_data: Dict[str, pd.DataFrame]) -> bool:
        """Validate relationships between campaign entities.
        
        Args:
            structured_data: Dictionary of structured DataFrames
            
        Returns:
            True if relationships are valid
        """
        try:
            # Get dataframes
            campaigns_df = structured_data.get("Campaign", pd.DataFrame())
            ad_groups_df = structured_data.get("Ad Group", pd.DataFrame())
            product_ads_df = structured_data.get("Product Ad", pd.DataFrame())
            keywords_df = structured_data.get("Keyword", pd.DataFrame())
            
            # Skip validation if any required sheet is empty
            if campaigns_df.empty or ad_groups_df.empty:
                self.logger.warning("Cannot validate relationships: Campaign or Ad Group sheet is empty")
                return True
            
            # Validate Campaign IDs match across sheets
            campaign_ids = set(campaigns_df["Campaign ID"].unique())
            
            if not ad_groups_df.empty:
                ad_group_campaign_ids = set(ad_groups_df["Campaign ID"].unique())
                if not ad_group_campaign_ids.issubset(campaign_ids):
                    self.logger.warning("Ad Groups reference non-existent campaigns")
            
            if not product_ads_df.empty:
                product_ad_campaign_ids = set(product_ads_df["Campaign ID"].unique())
                if not product_ad_campaign_ids.issubset(campaign_ids):
                    self.logger.warning("Product Ads reference non-existent campaigns")
            
            if not keywords_df.empty:
                keyword_campaign_ids = set(keywords_df["Campaign ID"].unique())
                if not keyword_campaign_ids.issubset(campaign_ids):
                    self.logger.warning("Keywords reference non-existent campaigns")
            
            # Validate Ad Group IDs
            if not ad_groups_df.empty:
                ad_group_ids = set(ad_groups_df["Ad Group ID"].unique())
                
                if not product_ads_df.empty:
                    product_ad_group_ids = set(product_ads_df["Ad Group ID"].unique())
                    if not product_ad_group_ids.issubset(ad_group_ids):
                        self.logger.warning("Product Ads reference non-existent ad groups")
                
                if not keywords_df.empty:
                    keyword_ad_group_ids = set(keywords_df["Ad Group ID"].unique())
                    if not keyword_ad_group_ids.issubset(ad_group_ids):
                        self.logger.warning("Keywords reference non-existent ad groups")
            
            return True
        
        except Exception as e:
            self.logger.error(f"Error validating entity relationships: {str(e)}")
            return False
    
    def merge_campaign_data(
        self,
        campaigns_list: List[Dict[str, pd.DataFrame]]
    ) -> Dict[str, pd.DataFrame]:
        """Merge data from multiple campaigns into single structure.
        
        Args:
            campaigns_list: List of campaign data dictionaries
            
        Returns:
            Merged dictionary with all campaigns
        """
        if not campaigns_list:
            return {}
        
        if len(campaigns_list) == 1:
            return campaigns_list[0]
        
        merged_data = {}
        
        # Get all unique sheet names
        all_sheets = set()
        for campaign_data in campaigns_list:
            all_sheets.update(campaign_data.keys())
        
        # Merge each sheet
        for sheet_name in all_sheets:
            sheet_dfs = []
            
            for campaign_data in campaigns_list:
                if sheet_name in campaign_data and not campaign_data[sheet_name].empty:
                    sheet_dfs.append(campaign_data[sheet_name])
            
            if sheet_dfs:
                merged_data[sheet_name] = pd.concat(sheet_dfs, ignore_index=True)
            else:
                merged_data[sheet_name] = pd.DataFrame()
        
        return merged_data