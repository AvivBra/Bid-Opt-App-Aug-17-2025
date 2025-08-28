"""Product Targeting campaign validator for all product-based campaigns."""

import pandas as pd
from typing import Dict, List, Tuple
from .base_validator import BaseCampaignValidator
import logging


class ProductTargetingValidator(BaseCampaignValidator):
    """Validator for all Product Targeting campaigns."""

    def __init__(self, campaign_type: str):
        """Initialize product targeting validator with specific campaign type.
        
        Args:
            campaign_type: Type of campaign (Testing PT, Expanded, Halloween Testing PT, Halloween Expanded)
        """
        super().__init__()
        self.campaign_type = campaign_type
        self.logger = logging.getLogger(f"{self.__class__.__name__}.{campaign_type}")
        
        # Product targeting campaigns don't need CVR/sales thresholds like keywords
        self.requires_data_rova = False

    def validate(self, template_df: pd.DataFrame = None, 
                session_table: pd.DataFrame = None,
                data_rova_df: pd.DataFrame = None) -> Tuple[bool, List[str]]:
        """Validate product targeting campaign data.
        
        Args:
            template_df: Template DataFrame
            session_table: Session table with campaign data
            data_rova_df: Data Rova DataFrame (not required for PT campaigns)
            
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
        required_session_cols = ["target", "ASIN", "Product Type", "Niche"]
        missing_session_cols = [col for col in required_session_cols if col not in session_table.columns]
        if missing_session_cols:
            errors.append(f"{self.campaign_type}: Missing session columns: {', '.join(missing_session_cols)}")
        
        # Check if there are any valid ASIN targets
        if not errors:
            valid_asins = self._get_valid_asins(session_table)
            if valid_asins.empty:
                errors.append(f"{self.campaign_type}: No ASIN targets found (ASINs must start with 'B0')")
        
        # Validate bid values
        if not errors:
            bid_errors = self.validate_bid_values(template_df)
            errors.extend(bid_errors)
        
        is_valid = len(errors) == 0
        return is_valid, errors

    def _get_bid_column(self) -> str:
        """Get the bid column name for this campaign type."""
        bid_columns = {
            "Testing PT": "Testing PT Bid",
            "Expanded": "Expanded Bid",
            "Halloween Testing PT": "Halloween Testing PT Bid",
            "Halloween Expanded": "Halloween Expanded Bid"
        }
        return bid_columns.get(self.campaign_type, "Testing PT Bid")

    def _get_valid_asins(self, session_table: pd.DataFrame) -> pd.DataFrame:
        """Get ASIN targets from session table.
        
        Args:
            session_table: Session table with targeting data
            
        Returns:
            DataFrame with valid ASIN targets
        """
        # Filter for ASIN targets (start with B0)
        asins_df = session_table[session_table["target"].str.startswith("B0", na=False)]
        
        return asins_df

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
        bid_values = template_df[bid_column].dropna()
        
        if bid_values.empty:
            errors.append(f"{self.campaign_type}: No bid values found in '{bid_column}' column")
            return errors
        
        # Convert to numeric, handling non-numeric values
        try:
            numeric_bids = pd.to_numeric(bid_values, errors='coerce')
            
            # Check for non-numeric values
            non_numeric = bid_values[numeric_bids.isna()]
            if not non_numeric.empty:
                errors.append(f"{self.campaign_type}: Found {len(non_numeric)} non-numeric bid values")
            
            # Check valid numeric bids
            valid_bids = numeric_bids.dropna()
            if not valid_bids.empty:
                # Check for negative values
                negative_bids = valid_bids[valid_bids < 0]
                if not negative_bids.empty:
                    errors.append(f"{self.campaign_type}: Found {len(negative_bids)} negative bid values")
                
                # Check for values below minimum (0.02)
                low_bids = valid_bids[valid_bids < 0.02]
                if not low_bids.empty:
                    errors.append(f"{self.campaign_type}: Found {len(low_bids)} bid values below minimum (0.02)")
                
                # Check for extremely high values (over 1.5 based on spec update)
                high_bids = valid_bids[valid_bids > 1.5]
                if not high_bids.empty:
                    errors.append(f"{self.campaign_type}: Found {len(high_bids)} bid values above maximum (1.5)")
                    
        except Exception as e:
            errors.append(f"{self.campaign_type}: Error validating bid values: {str(e)}")
        
        return errors

    def validate_template_asin_coverage(self, template_df: pd.DataFrame, session_table: pd.DataFrame) -> List[str]:
        """Validate that template ASINs have corresponding ASIN targets.
        
        Args:
            template_df: Template DataFrame
            session_table: Session table with ASIN targets
            
        Returns:
            List of warning messages
        """
        warnings = []
        
        # Get template ASINs
        template_asins = set(template_df["My ASIN"].dropna().astype(str))
        
        # Get session table data grouped by template ASIN
        session_grouped = session_table.groupby(["ASIN", "Product Type", "Niche"])
        
        for _, template_row in template_df.iterrows():
            asin = str(template_row.get("My ASIN", ""))
            product_type = str(template_row.get("Product Type", ""))
            niche = str(template_row.get("Niche", ""))
            
            if not asin or not product_type or not niche:
                continue
            
            # Check if this template configuration has any ASIN targets
            try:
                campaign_data = session_grouped.get_group((asin, product_type, niche))
                asin_targets = campaign_data[campaign_data["target"].str.startswith("B0", na=False)]
                
                if asin_targets.empty:
                    warnings.append(
                        f"{self.campaign_type}: No ASIN targets found for template "
                        f"ASIN '{asin}' | Product Type '{product_type}' | Niche '{niche}'"
                    )
            except KeyError:
                warnings.append(
                    f"{self.campaign_type}: No session data found for template "
                    f"ASIN '{asin}' | Product Type '{product_type}' | Niche '{niche}'"
                )
        
        return warnings

    def validate_asin_format(self, session_table: pd.DataFrame) -> List[str]:
        """Validate ASIN target format.
        
        Args:
            session_table: Session table with ASIN targets
            
        Returns:
            List of error messages
        """
        errors = []
        
        # Get targets that should be ASINs (start with B0)
        potential_asins = session_table[session_table["target"].str.startswith("B0", na=False)]
        
        for _, row in potential_asins.iterrows():
            asin = str(row["target"])
            
            # Basic ASIN format validation
            if len(asin) != 10:
                errors.append(f"{self.campaign_type}: Invalid ASIN format '{asin}' (should be 10 characters)")
            elif not asin.startswith("B0"):
                errors.append(f"{self.campaign_type}: Invalid ASIN format '{asin}' (should start with 'B0')")
            elif not asin[2:].isalnum():
                errors.append(f"{self.campaign_type}: Invalid ASIN format '{asin}' (should be alphanumeric after 'B0')")
        
        return errors

    def get_validation_summary(self, template_df: pd.DataFrame, session_table: pd.DataFrame) -> Dict[str, int]:
        """Get validation summary statistics.
        
        Args:
            template_df: Template DataFrame  
            session_table: Session table
            
        Returns:
            Dictionary with validation statistics
        """
        summary = {
            "template_rows": len(template_df) if template_df is not None else 0,
            "session_rows": len(session_table) if session_table is not None else 0,
            "total_targets": 0,
            "asin_targets": 0,
            "campaigns_with_targets": 0
        }
        
        if session_table is not None and not session_table.empty:
            summary["total_targets"] = len(session_table["target"].dropna().unique())
            summary["asin_targets"] = len(
                session_table[session_table["target"].str.startswith("B0", na=False)]["target"].unique()
            )
            
            # Count campaigns that have at least one ASIN target
            campaign_groups = session_table.groupby(["ASIN", "Product Type", "Niche"])
            campaigns_with_asins = 0
            
            for _, group in campaign_groups:
                if any(group["target"].str.startswith("B0", na=False)):
                    campaigns_with_asins += 1
            
            summary["campaigns_with_targets"] = campaigns_with_asins
        
        return summary