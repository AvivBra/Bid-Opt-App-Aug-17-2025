"""Template file reader for portfolio optimizations."""

import pandas as pd
import io
from typing import Dict, Optional
import logging


class TemplateReader:
    """Reads uploaded template files for portfolio optimizations."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def read_template(self, template_bytes: bytes, filename: str = "template.xlsx") -> pd.DataFrame:
        """
        Read template file from bytes.
        
        Args:
            template_bytes: Template file as bytes
            filename: Original filename for logging
            
        Returns:
            DataFrame with template data
            
        Raises:
            ValueError: If template cannot be read or is invalid
        """
        self.logger.info(f"Reading template file: {filename}")
        
        try:
            # Create BytesIO from bytes
            buffer = io.BytesIO(template_bytes)
            
            # Read Excel file
            # Try to read first sheet
            excel_data = pd.read_excel(buffer, sheet_name=0, engine='openpyxl')
            
            if excel_data.empty:
                raise ValueError("Template file is empty")
            
            self.logger.info(f"Template read successfully: {len(excel_data)} rows, {len(excel_data.columns)} columns")
            return excel_data
            
        except Exception as e:
            self.logger.error(f"Failed to read template file {filename}: {str(e)}")
            raise ValueError(f"Cannot read template file: {str(e)}")
    
    def validate_top_asins_template(self, template_df: pd.DataFrame) -> bool:
        """
        Validate that template is suitable for Top ASINs processing.
        
        Args:
            template_df: Template DataFrame
            
        Returns:
            True if valid for Top ASINs processing
        """
        self.logger.info("Validating Top ASINs template")
        
        # Check basic structure
        if template_df.empty:
            self.logger.error("Template is empty")
            return False
        
        # Check for Top ASINs column or use first column
        target_column = None
        if 'Top ASINs' in template_df.columns:
            target_column = 'Top ASINs'
        elif len(template_df.columns) > 0:
            target_column = template_df.columns[0]
            self.logger.info(f"Using first column '{target_column}' as Top ASINs column")
        else:
            self.logger.error("No columns found in template")
            return False
        
        # Check for non-empty ASINs
        asins = template_df[target_column].dropna()
        asins = asins[asins.astype(str).str.strip() != '']
        
        if len(asins) == 0:
            self.logger.error("No valid ASINs found in template")
            return False
        
        # Basic ASIN format validation (Amazon ASINs are typically 10 characters)
        valid_asins = 0
        for asin in asins:
            asin_str = str(asin).strip()
            if len(asin_str) >= 8 and len(asin_str) <= 15:  # Flexible ASIN length check
                valid_asins += 1
        
        if valid_asins == 0:
            self.logger.error("No ASINs appear to have valid format")
            return False
        
        self.logger.info(f"Template validation passed: {valid_asins} valid ASINs found")
        return True
    
    def extract_top_asins(self, template_df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract and normalize Top ASINs from template.
        
        Args:
            template_df: Raw template DataFrame
            
        Returns:
            Normalized DataFrame with Top ASINs
        """
        self.logger.info("Extracting Top ASINs from template")
        
        # Determine which column to use
        if 'Top ASINs' in template_df.columns:
            asin_column = 'Top ASINs'
        else:
            asin_column = template_df.columns[0]
        
        # Extract ASINs
        asins_df = template_df[[asin_column]].copy()
        
        # Normalize column name
        if asin_column != 'Top ASINs':
            asins_df = asins_df.rename(columns={asin_column: 'Top ASINs'})
        
        # Clean data
        asins_df = asins_df.dropna()
        asins_df = asins_df[asins_df['Top ASINs'].astype(str).str.strip() != '']
        
        # Clean ASIN values
        asins_df['Top ASINs'] = asins_df['Top ASINs'].astype(str).str.strip()
        
        # Remove duplicates
        asins_df = asins_df.drop_duplicates()
        
        # Reset index
        asins_df = asins_df.reset_index(drop=True)
        
        self.logger.info(f"Extracted {len(asins_df)} unique ASINs")
        return asins_df