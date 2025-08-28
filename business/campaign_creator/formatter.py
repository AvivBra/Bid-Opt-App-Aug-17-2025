"""Campaign output formatter."""

import pandas as pd
from typing import Dict, List, Optional, Tuple
import logging


class CampaignFormatter:
    """Formats campaign data for output."""
    
    def __init__(self):
        """Initialize campaign formatter."""
        self.logger = logging.getLogger(__name__)
        
        # Column order for Amazon bulk upload (32 columns total)
        self.column_order = [
            "Product",                          # 1
            "Entity",                          # 2
            "Operation",                       # 3
            "Campaign ID",                     # 4
            "Ad Group ID",                     # 5
            "Portfolio ID",                    # 6
            "Ad ID",                          # 7
            "Keyword ID",                      # 8
            "Product Targeting ID",            # 9
            "Campaign Name",                   # 10
            "Ad Group Name",                   # 11
            "Start Date",                      # 12
            "End Date",                        # 13
            "Targeting Type",                  # 14
            "State",                          # 15
            "Daily Budget",                    # 16
            "SKU",                            # 17
            "ASIN",                           # 18
            "Ad Group Default Bid",            # 19
            "Bid",                            # 20
            "Keyword Text",                    # 21
            "Native Language Keyword",         # 22
            "Native Language Locale",          # 23
            "Match Type",                      # 24
            "Bidding Strategy",                # 25
            "Placement",                       # 26
            "Percentage",                      # 27
            "Product Targeting Expression"    # 28
        ]
    
    def format_sheets(self, sheets_data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """Format all sheets for output.
        
        Args:
            sheets_data: Dictionary of sheet names to DataFrames
            
        Returns:
            Formatted dictionary of DataFrames
        """
        formatted_sheets = {}
        
        for sheet_name, df in sheets_data.items():
            if df is None or df.empty:
                self.logger.warning(f"Skipping empty sheet: {sheet_name}")
                formatted_sheets[sheet_name] = pd.DataFrame(columns=self.column_order)
            else:
                formatted_df = self.format_dataframe(df, sheet_name)
                formatted_sheets[sheet_name] = formatted_df
        
        return formatted_sheets
    
    def format_dataframe(self, df: pd.DataFrame, entity_type: str) -> pd.DataFrame:
        """Format a single DataFrame for output.
        
        Args:
            df: DataFrame to format
            entity_type: Type of entity (Campaign, Ad Group, etc.)
            
        Returns:
            Formatted DataFrame
        """
        # Create new dataframe with correct column order
        formatted_df = pd.DataFrame()
        
        # Add columns in the correct order
        for col in self.column_order:
            if col in df.columns:
                formatted_df[col] = df[col].fillna("")
            else:
                formatted_df[col] = ""
        
        # Clean up data types and formatting
        formatted_df = self._clean_data_types(formatted_df, entity_type)
        
        # Remove duplicate rows
        formatted_df = formatted_df.drop_duplicates()
        
        # Sort by Campaign ID and Ad Group ID for better organization
        sort_columns = []
        if "Campaign ID" in formatted_df.columns:
            sort_columns.append("Campaign ID")
        if "Ad Group ID" in formatted_df.columns and entity_type != "Campaign":
            sort_columns.append("Ad Group ID")
        if "Keyword Text" in formatted_df.columns and entity_type == "Keyword":
            sort_columns.append("Keyword Text")
        
        if sort_columns:
            formatted_df = formatted_df.sort_values(by=sort_columns)
        
        # Reset index
        formatted_df = formatted_df.reset_index(drop=True)
        
        # Log formatting summary
        self.logger.info(f"Formatted {entity_type} sheet: {len(formatted_df)} rows")
        
        return formatted_df
    
    def _clean_data_types(self, df: pd.DataFrame, entity_type: str) -> pd.DataFrame:
        """Clean and standardize data types.
        
        Args:
            df: DataFrame to clean
            entity_type: Type of entity
            
        Returns:
            Cleaned DataFrame
        """
        # Convert numeric columns to strings with proper formatting
        numeric_columns = ["Daily Budget", "Bid", "Ad Group Default Bid", "Percentage"]
        
        for col in numeric_columns:
            if col in df.columns:
                # Convert to numeric first, then to string
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna("")
                # Format non-empty values
                df.loc[df[col] != "", col] = df.loc[df[col] != "", col].apply(
                    lambda x: f"{float(x):.2f}" if x != "" and pd.notna(x) else ""
                )
        
        # Ensure text columns are strings
        text_columns = [
            "Campaign ID", "Ad Group ID", "Campaign Name", "Ad Group Name",
            "Keyword Text", "ASIN", "SKU", "Product Targeting Expression"
        ]
        
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).replace('nan', '')
        
        # Standardize State values
        if "State" in df.columns:
            df["State"] = df["State"].str.lower().replace({'': 'enabled', 'nan': 'enabled'})
        
        # Standardize Entity values
        if "Entity" in df.columns:
            entity_map = {
                "campaign": "Campaign",
                "ad group": "Ad Group",
                "product ad": "Product Ad",
                "keyword": "Keyword"
            }
            df["Entity"] = df["Entity"].str.lower().map(entity_map).fillna(df["Entity"])
        
        # Ensure Start Date format (YYYYMMDD)
        if "Start Date" in df.columns:
            df["Start Date"] = df["Start Date"].astype(str).replace('nan', '')
            # Validate date format
            df["Start Date"] = df["Start Date"].apply(self._validate_date_format)
        
        # Clean Match Type
        if "Match Type" in df.columns:
            df["Match Type"] = df["Match Type"].str.lower().replace({'': '', 'nan': ''})
        
        return df
    
    def _validate_date_format(self, date_str: str) -> str:
        """Validate and format date string to YYYYMMDD.
        
        Args:
            date_str: Date string to validate
            
        Returns:
            Formatted date string or empty string
        """
        if not date_str or date_str == 'nan' or date_str == '':
            return ''
        
        # Remove any non-numeric characters
        date_str = ''.join(filter(str.isdigit, str(date_str)))
        
        # Check if it's 8 digits (YYYYMMDD)
        if len(date_str) == 8:
            return date_str
        
        return ''
    
    def validate_output(self, sheets_data: Dict[str, pd.DataFrame]) -> Tuple[bool, List[str]]:
        """Validate formatted output before export.
        
        Args:
            sheets_data: Dictionary of formatted DataFrames
            
        Returns:
            Tuple of (is_valid, list_of_warnings)
        """
        warnings = []
        
        # Check for required sheets
        required_sheets = ["Campaign", "Ad Group", "Product Ad", "Keyword"]
        missing_sheets = [s for s in required_sheets if s not in sheets_data or sheets_data[s].empty]
        
        if missing_sheets:
            warnings.append(f"Missing or empty sheets: {', '.join(missing_sheets)}")
        
        # Validate each sheet
        for sheet_name, df in sheets_data.items():
            if df.empty:
                continue
            
            # Check for required columns based on entity type
            if sheet_name == "Campaign":
                required_cols = ["Campaign ID", "Campaign Name", "Daily Budget", "Targeting Type"]
            elif sheet_name == "Ad Group":
                required_cols = ["Campaign ID", "Ad Group ID", "Ad Group Name"]
            elif sheet_name == "Product Ad":
                required_cols = ["Campaign ID", "Ad Group ID", "ASIN"]
            elif sheet_name == "Keyword":
                required_cols = ["Campaign ID", "Ad Group ID", "Keyword Text", "Match Type", "Bid"]
            else:
                continue
            
            missing_values = []
            for col in required_cols:
                if col in df.columns:
                    empty_count = df[col].replace('', pd.NA).isna().sum()
                    if empty_count > 0:
                        missing_values.append(f"{col} ({empty_count} rows)")
            
            if missing_values:
                warnings.append(f"{sheet_name}: Missing values in {', '.join(missing_values)}")
        
        # Return True if no critical errors (warnings are ok)
        is_valid = len([w for w in warnings if "Missing or empty sheets" in w]) == 0
        
        return is_valid, warnings