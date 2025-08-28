"""Keyword campaign validator for all keyword-based campaigns."""

import pandas as pd
from typing import Dict, List, Tuple
from .base_validator import BaseCampaignValidator
import logging


class KeywordValidator(BaseCampaignValidator):
    """Validator for all keyword-based campaigns."""

    def __init__(self, campaign_type: str):
        """Initialize keyword validator with specific campaign type.
        
        Args:
            campaign_type: Type of campaign (Testing, Phrase, Broad, Halloween variants)
        """
        super().__init__()
        self.campaign_type = campaign_type
        self.logger = logging.getLogger(f"{self.__class__.__name__}.{campaign_type}")
        
        # CVR and sales thresholds for keyword campaigns
        self.cvr_threshold = 0.08
        self.sales_threshold = 0

    def validate(self, template_df: pd.DataFrame = None, 
                session_table: pd.DataFrame = None,
                data_rova_df: pd.DataFrame = None) -> Tuple[bool, List[str]]:
        """Validate keyword campaign data.
        
        Args:
            template_df: Template DataFrame
            session_table: Session table with campaign data
            data_rova_df: Data Rova DataFrame (optional)
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Check template
        if template_df is None or template_df.empty:
            errors.append(f"{self.campaign_type}: No template data provided")
            return False, errors
        
        # Check session table
        if session_table is None or session_table.empty:
            errors.append(f"{self.campaign_type}: No session data available")
            return False, errors
        
        # Validate required template columns
        required_template_cols = ["My ASIN", "Product Type", "Niche", self._get_bid_column()]
        missing_template_cols = [col for col in required_template_cols if col not in template_df.columns]
        if missing_template_cols:
            errors.append(f"{self.campaign_type}: Missing template columns: {', '.join(missing_template_cols)}")
        
        # Validate required session table columns
        required_session_cols = ["target", "ASIN", "Product Type", "Niche", "kw cvr", "kw sales"]
        missing_session_cols = [col for col in required_session_cols if col not in session_table.columns]
        if missing_session_cols:
            errors.append(f"{self.campaign_type}: Missing session columns: {', '.join(missing_session_cols)}")
        
        # Check if there are any valid keywords
        if not errors:
            valid_keywords = self._get_valid_keywords(session_table)
            if valid_keywords.empty:
                errors.append(f"{self.campaign_type}: No keywords meet CVR ({self.cvr_threshold}) and sales ({self.sales_threshold}) thresholds")
        
        is_valid = len(errors) == 0
        return is_valid, errors

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

    def _get_valid_keywords(self, session_table: pd.DataFrame) -> pd.DataFrame:
        """Get keywords that meet CVR and sales thresholds.
        
        Args:
            session_table: Session table with keyword data
            
        Returns:
            DataFrame with valid keywords
        """
        # Filter for non-ASIN targets
        keywords_df = session_table[~session_table["target"].str.startswith("B0", na=False)]
        
        # Apply CVR and sales thresholds
        valid_keywords = keywords_df[
            (keywords_df["kw cvr"] > self.cvr_threshold) &
            (keywords_df["kw sales"] > self.sales_threshold)
        ]
        
        return valid_keywords

    def validate_bid_values(self, template_df: pd.DataFrame) -> List[str]:
        """Validate bid values in template.
        
        Args:
            template_df: Template DataFrame
            
        Returns:
            List of error messages
        """
        errors = []
        bid_column = self._get_bid_column()
        
        if bid_column not in template_df.columns:
            errors.append(f"{self.campaign_type}: Bid column '{bid_column}' not found in template")
            return errors
        
        # Check for invalid bid values
        bid_values = template_df[bid_column]
        
        # Check for negative values
        negative_bids = bid_values[bid_values < 0]
        if not negative_bids.empty:
            errors.append(f"{self.campaign_type}: Found {len(negative_bids)} negative bid values")
        
        # Check for extremely high values (over $100)
        high_bids = bid_values[bid_values > 100]
        if not high_bids.empty:
            errors.append(f"{self.campaign_type}: Found {len(high_bids)} bid values over $100")
        
        return errors

    def validate_keywords_have_rova_data(self, session_table: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Check if keywords have required Data Rova information.
        
        Args:
            session_table: Session table with keyword data
            
        Returns:
            Tuple of (has_data, missing_keywords)
        """
        # Filter for non-ASIN targets
        keywords_df = session_table[~session_table["target"].str.startswith("B0", na=False)]
        
        # Check for keywords missing CVR or sales data
        missing_cvr = keywords_df[
            (keywords_df["kw cvr"].isna()) | 
            (keywords_df["kw cvr"] == 0)
        ]
        
        missing_sales = keywords_df[
            (keywords_df["kw sales"].isna()) | 
            (keywords_df["kw sales"] == 0)
        ]
        
        missing_keywords = []
        
        if not missing_cvr.empty:
            missing_keywords.extend(missing_cvr["target"].unique().tolist())
        
        if not missing_sales.empty:
            missing_keywords.extend(missing_sales["target"].unique().tolist())
        
        # Remove duplicates
        missing_keywords = list(set(missing_keywords))
        
        has_data = len(missing_keywords) == 0
        return has_data, missing_keywords