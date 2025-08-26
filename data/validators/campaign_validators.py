"""Campaign-specific validators."""

import pandas as pd
from typing import List, Tuple, Optional, Set


class CampaignTemplateValidator:
    """Validates campaign template files."""
    
    def __init__(self):
        """Initialize validator."""
        self.required_columns = ['My ASIN', 'Product Type', 'Niche']
        self.bid_columns = [
            'Testing Bid',
            'Testing PT Bid',
            'Phrase Bid',
            'Broad Bid',
            'Expanded Bid',
            'Halloween Testing Bid',
            'Halloween Testing PT Bid',
            'Halloween Phrase Bid',
            'Halloween Broad Bid',
            'Halloween Expanded Bid'
        ]
    
    def validate(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """
        Validate campaign template structure and data.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if dataframe is empty
        if df.empty:
            return False, "Template is empty"
        
        # Check required columns
        missing_cols = [col for col in self.required_columns if col not in df.columns]
        if missing_cols:
            return False, f"Missing required columns: {', '.join(missing_cols)}"
        
        # Check if required columns have data
        for col in self.required_columns:
            if df[col].isna().all():
                return False, f"Column '{col}' has no data"
        
        # Check bid columns exist
        existing_bid_cols = [col for col in self.bid_columns if col in df.columns]
        if not existing_bid_cols:
            return False, "No bid columns found in template"
        
        # Check at least one bid column has data
        has_bid_data = False
        for col in existing_bid_cols:
            if df[col].notna().any():
                has_bid_data = True
                break
        
        if not has_bid_data:
            return False, "At least one bid column must have data"
        
        # Validate bid values are numeric where present
        for col in existing_bid_cols:
            non_na_values = df[col].dropna()
            if len(non_na_values) > 0:
                try:
                    pd.to_numeric(non_na_values)
                except ValueError:
                    return False, f"Non-numeric values found in {col}"
        
        return True, "Template validation passed"


class CampaignDataValidator:
    """Validates campaign data consistency."""
    
    def __init__(self):
        """Initialize validator."""
        self.keyword_campaigns = {
            'Testing', 'Phrase', 'Broad',
            'Halloween Testing', 'Halloween Phrase', 'Halloween Broad'
        }
        self.pt_campaigns = {
            'Testing PT', 'Expanded',
            'Halloween Testing PT', 'Halloween Expanded'
        }
    
    def validate_campaign_data_requirements(self,
                                           selected_campaigns: List[str],
                                           has_keywords: bool,
                                           has_qualifying_keywords: bool) -> Tuple[bool, Optional[str]]:
        """
        Validate that selected campaigns have required data.
        
        Args:
            selected_campaigns: List of selected campaign types
            has_keywords: Whether any keywords exist
            has_qualifying_keywords: Whether any keywords meet thresholds
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        keyword_camps_selected = [c for c in selected_campaigns if c in self.keyword_campaigns]
        pt_camps_selected = [c for c in selected_campaigns if c in self.pt_campaigns]
        
        # If only PT campaigns selected, no keywords needed
        if pt_camps_selected and not keyword_camps_selected:
            return True, None
        
        # If keyword campaigns selected, check for qualifying keywords
        if keyword_camps_selected:
            if not has_keywords:
                return False, f"Can't create {', '.join(keyword_camps_selected)} with no keywords"
            
            if not has_qualifying_keywords:
                return False, f"Can't create {', '.join(keyword_camps_selected)} with no DR keywords info"
        
        return True, None
    
    def validate_file_limits(self,
                           num_files: int,
                           num_missing_keywords: int) -> Tuple[bool, Optional[str]]:
        """
        Validate file and data limits.
        
        Args:
            num_files: Number of Data Dive files
            num_missing_keywords: Number of keywords missing from Data Rova
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if num_files > 20:
            return False, "Maximum 20 Data Dive files allowed"
        
        if num_missing_keywords > 1000:
            return False, "יותר מ-1000 מילים חסרות"
        
        return True, None
    
    def get_warning_messages(self, num_missing_keywords: int) -> Optional[str]:
        """
        Get warning messages for non-critical issues.
        
        Args:
            num_missing_keywords: Number of keywords missing from Data Rova
            
        Returns:
            Warning message if applicable
        """
        if num_missing_keywords > 500:
            return f"Warning: {num_missing_keywords} keywords missing (>500)"
        
        return None