"""Template validator for Organize Top Campaigns optimization."""

import pandas as pd
from typing import List, Tuple, Optional
import logging
import re


class TopCampaignsTemplateValidator:
    """Validates template files for Organize Top Campaigns optimization."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def validate_template(self, template_df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Comprehensive validation of Top ASINs template.
        
        Args:
            template_df: Template DataFrame to validate
            
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        self.logger.info("Validating Top ASINs template")
        
        errors = []
        
        # Basic structure validation
        structure_valid = self._validate_structure(template_df, errors)
        
        if not structure_valid:
            return False, errors
        
        # Content validation
        content_valid = self._validate_content(template_df, errors)
        
        # ASIN format validation
        format_valid = self._validate_asin_formats(template_df, errors)
        
        is_valid = structure_valid and content_valid and format_valid
        
        if is_valid:
            self.logger.info("Template validation passed")
        else:
            self.logger.error(f"Template validation failed: {errors}")
        
        return is_valid, errors
    
    def _validate_structure(self, template_df: pd.DataFrame, errors: List[str]) -> bool:
        """Validate basic template structure."""
        if template_df.empty:
            errors.append("Template file is empty")
            return False
        
        if len(template_df.columns) == 0:
            errors.append("Template has no columns")
            return False
        
        # Check for expected column name or use first column
        has_top_asins_column = 'Top ASINs' in template_df.columns
        if not has_top_asins_column and len(template_df.columns) > 0:
            self.logger.info(f"'Top ASINs' column not found, will use first column: {template_df.columns[0]}")
        
        return True
    
    def _validate_content(self, template_df: pd.DataFrame, errors: List[str]) -> bool:
        """Validate template content."""
        # Determine column to check
        target_column = 'Top ASINs' if 'Top ASINs' in template_df.columns else template_df.columns[0]
        
        # Check for non-empty values
        non_empty_values = template_df[target_column].dropna()
        non_empty_values = non_empty_values[non_empty_values.astype(str).str.strip() != '']
        
        if len(non_empty_values) == 0:
            errors.append("Template contains no non-empty ASIN values")
            return False
        
        # Check for minimum number of ASINs
        if len(non_empty_values) < 1:
            errors.append("Template must contain at least 1 ASIN")
            return False
        
        # Check for maximum reasonable number of ASINs
        if len(non_empty_values) > 10000:
            errors.append("Template contains too many ASINs (maximum 10,000)")
            return False
        
        return True
    
    def _validate_asin_formats(self, template_df: pd.DataFrame, errors: List[str]) -> bool:
        """Validate ASIN formats."""
        target_column = 'Top ASINs' if 'Top ASINs' in template_df.columns else template_df.columns[0]
        
        asins = template_df[target_column].dropna()
        asins = asins[asins.astype(str).str.strip() != '']
        
        invalid_asins = []
        valid_asin_count = 0
        
        for asin in asins:
            asin_str = str(asin).strip()
            
            if self._is_valid_asin_format(asin_str):
                valid_asin_count += 1
            else:
                invalid_asins.append(asin_str)
        
        # Allow some flexibility - at least 50% should have valid ASIN format
        if valid_asin_count < len(asins) * 0.5:
            errors.append(f"Too many ASINs have invalid format. Valid ASINs: {valid_asin_count}, Invalid: {len(invalid_asins)}")
            
            # Show first few invalid ASINs as examples
            example_invalid = invalid_asins[:5]
            errors.append(f"Example invalid ASINs: {example_invalid}")
            return False
        
        # Warn about invalid ASINs but don't fail validation
        if invalid_asins:
            self.logger.warning(f"Found {len(invalid_asins)} ASINs with potentially invalid format")
        
        return True
    
    def _is_valid_asin_format(self, asin: str) -> bool:
        """
        Check if ASIN has valid format.
        
        Amazon ASINs are typically 10 characters: 1 letter + 9 alphanumeric
        But we'll be more flexible to accommodate variations.
        """
        if not asin:
            return False
        
        # Basic length check (ASINs are typically 10 characters)
        if len(asin) < 8 or len(asin) > 15:
            return False
        
        # Should contain only alphanumeric characters
        if not re.match(r'^[A-Z0-9]+$', asin.upper()):
            return False
        
        # Should start with a letter (typical ASIN format)
        if not asin[0].isalpha():
            return False
        
        return True
    
    def get_clean_asins(self, template_df: pd.DataFrame) -> List[str]:
        """
        Extract clean list of ASINs from template.
        
        Args:
            template_df: Template DataFrame
            
        Returns:
            List of clean ASIN strings
        """
        target_column = 'Top ASINs' if 'Top ASINs' in template_df.columns else template_df.columns[0]
        
        asins = template_df[target_column].dropna()
        asins = asins[asins.astype(str).str.strip() != '']
        
        # Clean and deduplicate
        clean_asins = []
        seen_asins = set()
        
        for asin in asins:
            clean_asin = str(asin).strip().upper()
            
            if clean_asin and clean_asin not in seen_asins:
                clean_asins.append(clean_asin)
                seen_asins.add(clean_asin)
        
        self.logger.info(f"Extracted {len(clean_asins)} clean unique ASINs")
        return clean_asins
    
    def validate_and_extract(self, template_df: pd.DataFrame) -> Tuple[bool, List[str], Optional[List[str]]]:
        """
        Validate template and extract ASINs in one call.
        
        Args:
            template_df: Template DataFrame
            
        Returns:
            Tuple of (is_valid, error_messages, clean_asins_list)
        """
        is_valid, errors = self.validate_template(template_df)
        
        if is_valid:
            clean_asins = self.get_clean_asins(template_df)
            return True, [], clean_asins
        else:
            return False, errors, None