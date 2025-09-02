import pandas as pd
from io import BytesIO
from ..campaign_optimizer_1.constants import SHEET_CAMPAIGN

class CampaignOptimizer1Service:
    """
    Service for generating Excel output files for Campaign Optimizer 1.
    """
    
    def generate_excel_output(self, processed_data: dict) -> bytes:
        """
        Generate Excel file from processed campaign data.
        
        Args:
            processed_data: Dictionary of sheet_name -> DataFrame
            
        Returns:
            bytes: Excel file content
        """
        output_buffer = BytesIO()
        
        with pd.ExcelWriter(output_buffer, engine='openpyxl') as writer:
            # Write Campaign sheet
            if SHEET_CAMPAIGN in processed_data:
                processed_data[SHEET_CAMPAIGN].to_excel(
                    writer, 
                    sheet_name=SHEET_CAMPAIGN, 
                    index=False
                )
            
            # Write Sheet3 (preserve if exists, otherwise create empty)
            if "Sheet3" in processed_data:
                processed_data["Sheet3"].to_excel(
                    writer,
                    sheet_name="Sheet3",
                    index=False
                )
            else:
                # Create empty Sheet3 to match expected output format
                empty_df = pd.DataFrame({"Version": [], "Version (1.0)": []})
                empty_df.to_excel(
                    writer,
                    sheet_name="Sheet3", 
                    index=False
                )
        
        output_buffer.seek(0)
        return output_buffer.getvalue()
    
    def validate_output_structure(self, processed_data: dict) -> bool:
        """
        Validate that processed data has expected structure.
        
        Args:
            processed_data: Dictionary of sheet_name -> DataFrame
            
        Returns:
            bool: True if structure is valid
        """
        # Must have Campaign sheet
        if SHEET_CAMPAIGN not in processed_data:
            return False
        
        campaign_df = processed_data[SHEET_CAMPAIGN]
        
        # Check required columns exist
        required_columns = ["Units", "ACOS", "Daily Budget", "Operation"]
        for col in required_columns:
            if col not in campaign_df.columns:
                return False
        
        return True