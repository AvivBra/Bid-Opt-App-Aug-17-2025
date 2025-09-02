from .cleaning import CampaignOptimizer1Cleaner
from .factory import CampaignOptimizer1Factory
from .service import CampaignOptimizer1Service

class CampaignOptimizer1Orchestrator:
    """
    Main orchestrator for Campaign Optimizer 1 processing pipeline.
    Coordinates cleaning, optimization, and output generation.
    """
    
    def __init__(self):
        self.cleaner = CampaignOptimizer1Cleaner()
        self.factory = CampaignOptimizer1Factory()
        self.service = CampaignOptimizer1Service()
    
    def process(self, raw_data: dict) -> bytes:
        """
        Execute complete Campaign Optimizer 1 processing pipeline.
        
        Args:
            raw_data: Dictionary of sheet_name -> DataFrame from input Excel
            
        Returns:
            bytes: Excel file content ready for download
        """
        # Step 1: Clean the data (3-step cleaning process)
        cleaned_data = self.cleaner.clean(raw_data)
        
        # Step 2: Apply optimization strategy
        strategy = self.factory.create_seven_days_budget_strategy()
        
        if "Campaign" in cleaned_data:
            optimized_campaigns = strategy.optimize(cleaned_data["Campaign"])
            cleaned_data["Campaign"] = optimized_campaigns
        
        # Step 3: Generate Excel output
        output_bytes = self.service.generate_excel_output(cleaned_data)
        
        return output_bytes
    
    def get_processing_summary(self, raw_data: dict, processed_data: dict) -> dict:
        """
        Generate summary of processing results.
        
        Args:
            raw_data: Original input data
            processed_data: Processed output data
            
        Returns:
            Dictionary with processing metrics
        """
        summary = {
            "input_sheets": len(raw_data),
            "output_sheets": len(processed_data),
            "campaigns_processed": 0,
            "campaigns_updated": 0
        }
        
        if "Campaign" in processed_data:
            campaign_df = processed_data["Campaign"]
            summary["campaigns_processed"] = len(campaign_df)
            
            # Count campaigns with Operation = "update"
            if "Operation" in campaign_df.columns:
                updated_mask = campaign_df["Operation"] == "update"
                summary["campaigns_updated"] = updated_mask.sum()
        
        return summary