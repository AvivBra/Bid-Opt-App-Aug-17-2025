"""Halloween Testing campaign validator."""

import pandas as pd
from typing import Optional, Tuple
from .base_validator import BaseCampaignValidator


class HalloweenTestingValidator(BaseCampaignValidator):
    """Validator for Halloween Testing campaigns."""
    
    def __init__(self):
        """Initialize Halloween Testing validator."""
        super().__init__()
        self.campaign_type = "Halloween Testing"
        self.bid_column = "Halloween Testing Bid"
        self.cvr_threshold = 0.08
        self.sales_threshold = 0
    
    def validate(
        self,
        template_df: pd.DataFrame,
        session_table: pd.DataFrame,
        data_rova_df: Optional[pd.DataFrame] = None
    ) -> Tuple[bool, Optional[str]]:
        """Validate Halloween Testing campaign data.
        
        Args:
            template_df: Template dataframe
            session_table: Session table with all data
            data_rova_df: Optional Data Rova dataframe
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate template structure
        is_valid, error = self.validate_template_columns(template_df)
        if not is_valid:
            return False, error
        
        # Validate session table structure
        is_valid, error = self.validate_session_columns(session_table)
        if not is_valid:
            return False, error
        
        # Check if template is empty
        if template_df.empty:
            return False, "Template is empty"
        
        # Check if session table is empty
        if session_table.empty:
            return False, "Session table is empty"
        
        # Validate data completeness
        is_valid, error = self.validate_data_completeness(template_df, self.bid_column)
        if not is_valid:
            return False, error
        
        # Filter session table for Halloween Testing campaigns
        halloween_data = session_table[session_table["Campaign type"] == self.campaign_type]
        
        if halloween_data.empty:
            return False, f"No data found for {self.campaign_type} campaign"
        
        # Check if we have any valid keywords
        valid_keywords = self._get_valid_keywords(halloween_data)
        
        if valid_keywords.empty:
            self.logger.warning(f"No valid keywords found for {self.campaign_type} (all below thresholds)")
            # This is a warning, not an error - campaign can proceed with just ASINs if any
            
        # Check if we have any targets at all (keywords or ASINs)
        all_targets = halloween_data["target"].dropna()
        if all_targets.empty:
            return False, f"No targets (keywords or ASINs) found for {self.campaign_type}"
        
        # Log validation summary
        keyword_count = len(valid_keywords)
        asin_count = len(halloween_data[halloween_data["target"].str.startswith("B0", na=False)])
        total_count = len(all_targets)
        
        self.logger.info(
            f"Halloween Testing validation passed: "
            f"{keyword_count} valid keywords, {asin_count} ASINs, "
            f"{total_count} total targets"
        )
        
        return True, None
    
    def _get_valid_keywords(self, session_data: pd.DataFrame) -> pd.DataFrame:
        """Get keywords that meet CVR and sales thresholds.
        
        Args:
            session_data: Filtered session data for this campaign
            
        Returns:
            DataFrame of valid keywords
        """
        # Filter out ASINs (keep only keywords)
        keywords_df = session_data[~session_data["target"].str.startswith("B0", na=False)].copy()
        
        if keywords_df.empty:
            return pd.DataFrame()
        
        # Check for Data Rova columns
        if "kw cvr" not in keywords_df.columns or "kw sales" not in keywords_df.columns:
            self.logger.warning("Data Rova columns (kw cvr, kw sales) not found")
            return pd.DataFrame()
        
        # Apply thresholds
        valid_keywords = keywords_df[
            (keywords_df["kw cvr"] > self.cvr_threshold) & 
            (keywords_df["kw sales"] > self.sales_threshold)
        ]
        
        return valid_keywords