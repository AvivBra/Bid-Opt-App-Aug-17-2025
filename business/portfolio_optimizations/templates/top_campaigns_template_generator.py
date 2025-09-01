"""Template generator for Organize Top Campaigns optimization."""

import pandas as pd
import io
from typing import Optional
import logging


class TopCampaignsTemplateGenerator:
    """Generates Excel template for Top ASINs input."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_template(self) -> bytes:
        """
        Generate Excel template with single sheet and "Top ASINs" column.
        
        Returns:
            Excel file as bytes
        """
        self.logger.info("Generating Top ASINs template")
        
        # Create DataFrame with single column
        template_df = pd.DataFrame({
            'Top ASINs': [
                # Add some example ASINs as placeholder/guidance
                'B08N5WRWNW',
                'B07QRXF3QV',
                'B09LQRS8TN',
                # Add empty rows for user input
                '', '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', ''
            ]
        })
        
        # Convert to Excel bytes
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            template_df.to_excel(writer, sheet_name='Sheet1', index=False)
        
        buffer.seek(0)
        excel_bytes = buffer.getvalue()
        
        self.logger.info(f"Template generated: {len(excel_bytes)} bytes")
        return excel_bytes
    
    def validate_template(self, template_data: pd.DataFrame) -> bool:
        """
        Validate that uploaded template has correct structure.
        
        Args:
            template_data: DataFrame from uploaded template
            
        Returns:
            True if valid, False otherwise
        """
        self.logger.info("Validating template structure")
        
        # Check if DataFrame is not empty
        if template_data.empty:
            self.logger.error("Template is empty")
            return False
        
        # Check if "Top ASINs" column exists
        if 'Top ASINs' not in template_data.columns:
            # Check if first column can be treated as Top ASINs
            if len(template_data.columns) > 0:
                self.logger.warning(f"'Top ASINs' column not found, using first column: {template_data.columns[0]}")
                return True
            else:
                self.logger.error("No columns found in template")
                return False
        
        # Check if there's at least one non-empty ASIN
        top_asins_col = 'Top ASINs' if 'Top ASINs' in template_data.columns else template_data.columns[0]
        non_empty_asins = template_data[top_asins_col].dropna()
        non_empty_asins = non_empty_asins[non_empty_asins.astype(str).str.strip() != '']
        
        if len(non_empty_asins) == 0:
            self.logger.error("Template contains no non-empty ASINs")
            return False
        
        self.logger.info(f"Template validation passed: {len(non_empty_asins)} ASINs found")
        return True
    
    def normalize_template_data(self, template_data: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize template data to standard format.
        
        Args:
            template_data: Raw template DataFrame
            
        Returns:
            Normalized DataFrame with "Top ASINs" column
        """
        self.logger.info("Normalizing template data")
        
        # Ensure we have the right column name
        if 'Top ASINs' not in template_data.columns:
            # Rename first column to "Top ASINs"
            first_col = template_data.columns[0]
            template_data = template_data.rename(columns={first_col: 'Top ASINs'})
            self.logger.info(f"Renamed column '{first_col}' to 'Top ASINs'")
        
        # Keep only the Top ASINs column
        normalized_df = template_data[['Top ASINs']].copy()
        
        # Remove empty rows
        normalized_df = normalized_df.dropna()
        normalized_df = normalized_df[normalized_df['Top ASINs'].astype(str).str.strip() != '']
        
        # Clean ASIN values
        normalized_df['Top ASINs'] = normalized_df['Top ASINs'].astype(str).str.strip()
        
        # Remove duplicates
        normalized_df = normalized_df.drop_duplicates()
        
        self.logger.info(f"Template data normalized: {len(normalized_df)} unique ASINs")
        return normalized_df