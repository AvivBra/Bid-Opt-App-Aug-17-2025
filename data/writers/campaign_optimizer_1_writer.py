"""Campaign Optimizer 1 Excel output writer."""

import pandas as pd
from io import BytesIO
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class CampaignOptimizer1Writer:
    """Excel writer for Campaign Optimizer 1 output files."""
    
    def write_excel_output(self, processed_data: Dict[str, pd.DataFrame]) -> bytes:
        """
        Write processed data to Excel format matching expected output structure.
        
        Args:
            processed_data: Dictionary of sheet_name -> DataFrame
            
        Returns:
            bytes: Excel file content
        """
        output_buffer = BytesIO()
        
        try:
            with pd.ExcelWriter(output_buffer, engine='openpyxl') as writer:
                # Write Campaign sheet (main output)
                if "Campaign" in processed_data:
                    campaign_df = processed_data["Campaign"]
                    
                    # Ensure proper data types for output
                    campaign_df = self._format_campaign_data(campaign_df)
                    
                    campaign_df.to_excel(
                        writer,
                        sheet_name="Campaign",
                        index=False
                    )
                    logger.info(f"Wrote Campaign sheet with {len(campaign_df)} rows")
                
                # Write Sheet3 (preserve structure from input or create empty)
                if "Sheet3" in processed_data and not processed_data["Sheet3"].empty:
                    processed_data["Sheet3"].to_excel(
                        writer,
                        sheet_name="Sheet3",
                        index=False
                    )
                    logger.info("Wrote Sheet3 with existing data")
                else:
                    # Create empty Sheet3 to match expected output format
                    empty_sheet3 = pd.DataFrame({
                        "Version": [],
                        "Version (1.0)": []
                    })
                    empty_sheet3.to_excel(
                        writer,
                        sheet_name="Sheet3",
                        index=False
                    )
                    logger.info("Wrote empty Sheet3")
            
            output_buffer.seek(0)
            return output_buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Error writing Excel output: {e}")
            raise
    
    def _format_campaign_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Format campaign data to match expected output types and values.
        
        Args:
            df: Campaign DataFrame to format
            
        Returns:
            Formatted DataFrame
        """
        formatted_df = df.copy()
        
        try:
            # Ensure numeric columns are properly formatted
            if "Daily Budget" in formatted_df.columns:
                # Convert to integer for budget values (1, 3, 5)
                formatted_df["Daily Budget"] = pd.to_numeric(
                    formatted_df["Daily Budget"], 
                    errors='coerce'
                ).fillna(1).astype(int)
            
            if "Units" in formatted_df.columns:
                # Ensure Units are integers
                formatted_df["Units"] = pd.to_numeric(
                    formatted_df["Units"], 
                    errors='coerce'
                ).fillna(0).astype(int)
            
            if "ACOS" in formatted_df.columns:
                # Ensure ACOS is float with proper precision
                formatted_df["ACOS"] = pd.to_numeric(
                    formatted_df["ACOS"], 
                    errors='coerce'
                ).round(4)
            
            # Handle Operation column
            if "Operation" in formatted_df.columns:
                # Replace NaN with empty string for non-updated campaigns
                formatted_df["Operation"] = formatted_df["Operation"].fillna("")
            
            logger.info("Campaign data formatting completed")
            return formatted_df
            
        except Exception as e:
            logger.warning(f"Error formatting campaign data: {e}")
            # Return original data if formatting fails
            return df
    
    def validate_output_structure(self, processed_data: Dict[str, pd.DataFrame]) -> bool:
        """
        Validate that processed data has the correct structure for output.
        
        Args:
            processed_data: Dictionary of sheet data
            
        Returns:
            bool: True if structure is valid for output
        """
        try:
            # Must have Campaign sheet
            if "Campaign" not in processed_data:
                logger.error("Missing Campaign sheet in processed data")
                return False
            
            campaign_df = processed_data["Campaign"]
            
            # Check minimum required columns for output
            required_cols = ["Units", "ACOS", "Daily Budget"]
            missing_cols = []
            
            for col in required_cols:
                if col not in campaign_df.columns:
                    missing_cols.append(col)
            
            if missing_cols:
                logger.error(f"Missing required columns in Campaign sheet: {missing_cols}")
                return False
            
            # Check data integrity
            if len(campaign_df) == 0:
                logger.error("Campaign sheet is empty")
                return False
            
            logger.info("Output structure validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Output structure validation error: {e}")
            return False