"""Results Manager for intelligently combining multiple portfolio optimization results."""

import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
import logging
from io import BytesIO

from config.optimization_config import apply_text_format_before_write


class PortfolioOptimizationResultsManager:
    """
    Manager for combining results from multiple portfolio optimizations.
    
    Handles intelligent merging of DataFrames, preserves all original data,
    and ensures proper column formatting for Excel output.
    """
    
    def __init__(self):
        self.logger = logging.getLogger("portfolio_optimization.results_manager")
        self.combined_results: List[Dict[str, Any]] = []
        self.processing_summary: Dict[str, Any] = {}
    
    def add_result(
        self,
        optimization_name: str,
        processed_df: Optional[pd.DataFrame],
        details: Dict[str, Any],
        result_type: str = "campaigns"
    ) -> None:
        """
        Add a result from an optimization.
        
        Args:
            optimization_name: Name of the optimization
            processed_df: Processed DataFrame (can be None if failed)
            details: Processing details from orchestrator
            result_type: Type of result ("campaigns", "portfolios", etc.)
        """
        result = {
            "optimization_name": optimization_name,
            "processed_df": processed_df,
            "details": details,
            "result_type": result_type,
            "success": processed_df is not None and details.get("summary", {}).get("success", False)
        }
        
        self.combined_results.append(result)
        
        # Update processing summary
        self.processing_summary[optimization_name] = {
            "success": result["success"],
            "message": details.get("summary", {}).get("message", "Unknown status"),
            "processing_stats": details.get("processing", {}),
            "result_type": result_type
        }
        
        self.logger.info(f"Added result for {optimization_name}: {'Success' if result['success'] else 'Failed'}")
    
    def create_combined_output(
        self,
        original_sheets: Dict[str, pd.DataFrame]
    ) -> Tuple[Optional[BytesIO], Dict[str, Any]]:
        """
        Create combined Excel output from all optimization results.
        
        Args:
            original_sheets: Original Excel sheets from uploaded file
            
        Returns:
            Tuple of (output_file, summary_details)
        """
        try:
            self.logger.info("Creating combined output file...")
            
            # Start with original data - Entity=Campaign filtered for campaigns sheet
            campaigns_data = None
            if "Sponsored Products Campaigns" in original_sheets:
                campaigns_data = original_sheets["Sponsored Products Campaigns"]
                campaigns_data = campaigns_data[campaigns_data["Entity"] == "Campaign"].copy()
            
            portfolios_data = original_sheets.get("Portfolios", pd.DataFrame()).copy() if "Portfolios" in original_sheets else None
            
            # Apply optimizations in order
            campaigns_updated_count = 0
            portfolios_updated_count = 0
            
            for result in self.combined_results:
                if not result["success"]:
                    self.logger.warning(f"Skipping failed optimization: {result['optimization_name']}")
                    continue
                
                optimization_name = result["optimization_name"]
                processed_df = result["processed_df"]
                result_type = result["result_type"]
                
                self.logger.info(f"Applying {optimization_name} results...")
                
                if result_type == "campaigns" and processed_df is not None and campaigns_data is not None:
                    # For campaigns optimizations - use processed data directly
                    # The processed_df should already be Entity=Campaign filtered with optimizations applied
                    campaigns_data = processed_df[processed_df["Entity"] == "Campaign"].copy()
                    campaigns_updated_count += result["details"].get("processing", {}).get("campaigns_updated", 0)
                    self.logger.info(f"Applied {optimization_name} to campaigns: {len(campaigns_data)} rows")
                
                elif result_type == "portfolios" and processed_df is not None and portfolios_data is not None:
                    # For portfolio optimizations - merge with existing portfolios data
                    portfolios_data = processed_df.copy()
                    portfolios_updated_count += result["details"].get("processing", {}).get("empty_portfolios_count", 0)
                    self.logger.info(f"Applied {optimization_name} to portfolios: {len(portfolios_data)} rows")
            
            # Create output file
            output_file = self._create_excel_file(campaigns_data, portfolios_data)
            
            # Build summary
            summary_details = {
                "total_optimizations": len(self.combined_results),
                "successful_optimizations": sum(1 for r in self.combined_results if r["success"]),
                "campaigns_updated": campaigns_updated_count,
                "portfolios_updated": portfolios_updated_count,
                "campaigns_total": len(campaigns_data) if campaigns_data is not None else 0,
                "portfolios_total": len(portfolios_data) if portfolios_data is not None else 0,
                "processing_summary": self.processing_summary,
                "sheets_created": []
            }
            
            if campaigns_data is not None and len(campaigns_data) > 0:
                summary_details["sheets_created"].append("Sponsored Products Campaigns")
            
            if portfolios_data is not None and len(portfolios_data) > 0:
                summary_details["sheets_created"].append("Portfolios")
            
            self.logger.info(f"Combined output created: {len(summary_details['sheets_created'])} sheets")
            
            return output_file, summary_details
            
        except Exception as e:
            self.logger.error(f"Error creating combined output: {str(e)}")
            import traceback
            self.logger.debug(f"Full traceback: {traceback.format_exc()}")
            
            error_details = {
                "error": str(e),
                "processing_summary": self.processing_summary,
                "successful_optimizations": sum(1 for r in self.combined_results if r["success"]),
                "total_optimizations": len(self.combined_results)
            }
            
            return None, error_details
    
    def _create_excel_file(
        self,
        campaigns_data: Optional[pd.DataFrame],
        portfolios_data: Optional[pd.DataFrame]
    ) -> BytesIO:
        """
        Create Excel file with proper formatting.
        
        Args:
            campaigns_data: Campaigns DataFrame
            portfolios_data: Portfolios DataFrame
            
        Returns:
            BytesIO object with Excel file
        """
        output_file = BytesIO()
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Write Sponsored Products Campaigns sheet (required)
            if campaigns_data is not None and len(campaigns_data) > 0:
                # Apply text formatting to prevent scientific notation
                campaigns_formatted = apply_text_format_before_write(campaigns_data)
                campaigns_formatted.to_excel(writer, sheet_name='Sponsored Products Campaigns', index=False)
                self.logger.debug(f"Wrote Campaigns sheet with {len(campaigns_data)} rows")
            
            # Write Portfolios sheet (if available)
            if portfolios_data is not None and len(portfolios_data) > 0:
                # Apply text formatting to prevent scientific notation
                portfolios_formatted = apply_text_format_before_write(portfolios_data)
                portfolios_formatted.to_excel(writer, sheet_name='Portfolios', index=False)
                self.logger.debug(f"Wrote Portfolios sheet with {len(portfolios_data)} rows")
        
        output_file.seek(0)
        return output_file
    
    def get_processing_summary(self) -> Dict[str, Any]:
        """
        Get summary of all processing results.
        
        Returns:
            Dictionary with processing summary
        """
        return self.processing_summary.copy()
    
    def get_successful_optimizations(self) -> List[str]:
        """
        Get list of successful optimization names.
        
        Returns:
            List of successful optimization names
        """
        return [
            result["optimization_name"] 
            for result in self.combined_results 
            if result["success"]
        ]
    
    def get_failed_optimizations(self) -> List[Tuple[str, str]]:
        """
        Get list of failed optimizations with error messages.
        
        Returns:
            List of tuples (optimization_name, error_message)
        """
        failed = []
        for result in self.combined_results:
            if not result["success"]:
                error_msg = result["details"].get("error", "Unknown error")
                failed.append((result["optimization_name"], error_msg))
        return failed
    
    def has_any_successful_results(self) -> bool:
        """
        Check if any optimizations were successful.
        
        Returns:
            True if at least one optimization succeeded
        """
        return any(result["success"] for result in self.combined_results)
    
    def clear_results(self) -> None:
        """Clear all stored results."""
        self.combined_results.clear()
        self.processing_summary.clear()
        self.logger.info("Cleared all results")