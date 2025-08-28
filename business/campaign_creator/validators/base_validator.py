"""Base validator for campaign creation."""

from abc import ABC, abstractmethod
import pandas as pd
from typing import Optional, Tuple
import logging


class BaseCampaignValidator(ABC):
    """Base class for campaign validators."""
    
    def __init__(self):
        """Initialize base validator."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.required_template_columns = [
            "My ASIN",
            "Product Type", 
            "Niche"
        ]
        self.required_session_columns = [
            "target",
            "ASIN",
            "Product Type",
            "Niche",
            "Campaign type",
            "Bid"
        ]
    
    @abstractmethod
    def validate(
        self,
        template_df: pd.DataFrame,
        session_table: pd.DataFrame,
        data_rova_df: Optional[pd.DataFrame] = None
    ) -> Tuple[bool, Optional[str]]:
        """Validate campaign data.
        
        Args:
            template_df: Template dataframe
            session_table: Session table with all data
            data_rova_df: Optional Data Rova dataframe
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        pass
    
    def validate_template_columns(self, template_df: pd.DataFrame) -> Tuple[bool, Optional[str]]:
        """Validate template has required columns."""
        missing_cols = []
        for col in self.required_template_columns:
            if col not in template_df.columns:
                missing_cols.append(col)
        
        if missing_cols:
            return False, f"Template missing required columns: {', '.join(missing_cols)}"
        return True, None
    
    def validate_session_columns(self, session_table: pd.DataFrame) -> Tuple[bool, Optional[str]]:
        """Validate session table has required columns."""
        missing_cols = []
        for col in self.required_session_columns:
            if col not in session_table.columns:
                missing_cols.append(col)
        
        if missing_cols:
            return False, f"Session table missing required columns: {', '.join(missing_cols)}"
        return True, None
    
    def validate_data_completeness(
        self, 
        template_df: pd.DataFrame,
        bid_column: str
    ) -> Tuple[bool, Optional[str]]:
        """Validate data completeness for campaign."""
        # Check if bid column exists
        if bid_column not in template_df.columns:
            return False, f"Bid column '{bid_column}' not found in template"
        
        # Check if there are any rows with valid bids
        valid_bids = template_df[bid_column].dropna()
        valid_bids = valid_bids[valid_bids > 0]
        
        if valid_bids.empty:
            return False, f"No valid bids found in '{bid_column}'"
        
        # Check for required fields in rows with valid bids
        rows_with_bids = template_df[template_df[bid_column].notna() & (template_df[bid_column] > 0)]
        
        for idx, row in rows_with_bids.iterrows():
            if pd.isna(row.get("My ASIN")) or str(row.get("My ASIN")).strip() == "":
                return False, f"Row {idx + 2}: Missing ASIN for row with bid"
            if pd.isna(row.get("Product Type")) or str(row.get("Product Type")).strip() == "":
                return False, f"Row {idx + 2}: Missing Product Type for row with bid"
            if pd.isna(row.get("Niche")) or str(row.get("Niche")).strip() == "":
                return False, f"Row {idx + 2}: Missing Niche for row with bid"
        
        return True, None