import pandas as pd
from .constants import (
    ENTITY_CAMPAIGN, STATE_PAUSED, SHEET_SPONSORED_PRODUCTS_CAMPAIGNS, 
    SHEET_CAMPAIGN, COL_ENTITY, COL_STATE, COL_CAMPAIGN_STATE, COL_AD_GROUP_STATE
)

class CampaignOptimizer1Cleaner:
    """
    Implements the 3-step cleaning process for Campaign Optimizer 1:
    1. Filter Entity = Campaign from Sponsored Products Campaigns sheet
    2. Remove non-Campaign sheets  
    3. Remove paused campaigns
    """
    
    def clean(self, all_sheets: dict) -> dict:
        """
        Clean the input data according to Campaign Optimizer 1 specifications.
        
        Args:
            all_sheets: Dictionary of sheet_name -> DataFrame
            
        Returns:
            Dictionary with cleaned sheets
        """
        cleaned_sheets = {}
        
        # Step 1: Extract Campaign entities from Sponsored Products Campaigns
        if SHEET_SPONSORED_PRODUCTS_CAMPAIGNS in all_sheets:
            sponsored_df = all_sheets[SHEET_SPONSORED_PRODUCTS_CAMPAIGNS]
            
            # Filter for Entity = Campaign only
            campaign_df = sponsored_df[sponsored_df[COL_ENTITY] == ENTITY_CAMPAIGN].copy()
            
            # Step 3: Remove paused campaigns
            campaign_df = self._remove_paused_campaigns(campaign_df)
            
            cleaned_sheets[SHEET_CAMPAIGN] = campaign_df
        
        # Step 2: Keep only Campaign sheet and preserve Sheet3 if it exists
        if "Sheet3" in all_sheets:
            cleaned_sheets["Sheet3"] = all_sheets["Sheet3"]
        
        return cleaned_sheets
    
    def _remove_paused_campaigns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove campaigns where any of these conditions are true:
        - State = paused
        - Campaign State (Informational only) = paused  
        - Ad Group State (Informational only) = paused
        """
        # Create mask for rows to keep (not paused)
        mask = True
        
        # Check State column
        if COL_STATE in df.columns:
            mask = mask & (df[COL_STATE] != STATE_PAUSED)
        
        # Check Campaign State column
        if COL_CAMPAIGN_STATE in df.columns:
            mask = mask & (df[COL_CAMPAIGN_STATE] != STATE_PAUSED)
            
        # Check Ad Group State column  
        if COL_AD_GROUP_STATE in df.columns:
            mask = mask & (df[COL_AD_GROUP_STATE] != STATE_PAUSED)
        
        return df[mask].copy()