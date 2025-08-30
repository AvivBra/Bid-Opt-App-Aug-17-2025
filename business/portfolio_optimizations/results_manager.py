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
        result_type: str = "campaigns",
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
            "success": processed_df is not None
            and details.get("summary", {}).get("success", False),
        }

        self.combined_results.append(result)

        # Update processing summary
        self.processing_summary[optimization_name] = {
            "success": result["success"],
            "message": details.get("summary", {}).get("message", "Unknown status"),
            "processing_stats": details.get("processing", {}),
            "result_type": result_type,
        }

        self.logger.info(
            f"Added result for {optimization_name}: {'Success' if result['success'] else 'Failed'}"
        )

    def create_combined_output(
        self, original_sheets: Dict[str, pd.DataFrame]
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

            # Keep ALL original data with ALL columns
            campaigns_data = None
            if "Sponsored Products Campaigns" in original_sheets:
                campaigns_data = original_sheets["Sponsored Products Campaigns"].copy()
                self.logger.info(
                    f"[DEBUG] Original campaigns_data shape: {campaigns_data.shape}"
                )

            portfolios_data = None
            if "Portfolios" in original_sheets:
                portfolios_data = original_sheets["Portfolios"].copy()
                self.logger.info(
                    f"[DEBUG] Original portfolios_data shape: {portfolios_data.shape}"
                )

            # Apply optimizations in order - CHAINING TRANSFORMATIONS
            campaigns_updated_count = 0
            portfolios_updated_count = 0

            for result in self.combined_results:
                if not result["success"]:
                    self.logger.warning(
                        f"Skipping failed optimization: {result['optimization_name']}"
                    )
                    continue

                optimization_name = result["optimization_name"]
                processed_df = result["processed_df"]
                result_type = result["result_type"]

                # Get updated indices if provided
                updated_indices = result["details"].get("updated_indices", [])

                self.logger.info(
                    f"[DEBUG] ========== Processing {optimization_name} =========="
                )
                self.logger.info(f"[DEBUG] Result type: {result_type}")
                self.logger.info(
                    f"[DEBUG] Processed_df shape: {processed_df.shape if processed_df is not None else 'None'}"
                )
                self.logger.info(
                    f"[DEBUG] Updated indices count: {len(updated_indices)}"
                )

                if (
                    result_type == "campaigns"
                    and processed_df is not None
                    and campaigns_data is not None
                ):
                    # FIX: Use updated_indices if available for precise merging
                    if updated_indices:
                        # Direct update using known indices
                        self.logger.info(
                            f"[DEBUG] Using {len(updated_indices)} updated indices for precise merge"
                        )

                        for idx in updated_indices:
                            if (
                                idx in processed_df.index
                                and idx in campaigns_data.index
                            ):
                                # Update the entire row from processed_df
                                campaigns_data.loc[idx] = processed_df.loc[idx]

                        campaigns_updated_count += len(updated_indices)
                        self.logger.info(
                            f"Applied {optimization_name}: updated {len(updated_indices)} campaign rows"
                        )

                    else:
                        # Fallback to the original logic if no indices provided
                        self.logger.info(
                            "[DEBUG] No updated indices provided, using entity-based merge"
                        )

                        # Only update Campaign entity rows
                        processed_campaigns = processed_df[
                            processed_df["Entity"] == "Campaign"
                        ].copy()

                        # Ensure indices match
                        if not processed_campaigns.index.equals(
                            campaigns_data[campaigns_data["Entity"] == "Campaign"].index
                        ):
                            self.logger.warning(
                                "[DEBUG] Index mismatch, resetting indices"
                            )
                            processed_campaigns = processed_campaigns.reset_index(
                                drop=True
                            )
                            campaigns_data = campaigns_data.reset_index(drop=True)

                        # Update matching rows
                        updated_rows = 0
                        for idx in processed_campaigns.index:
                            if idx in campaigns_data.index:
                                # Update entire row
                                for col in processed_campaigns.columns:
                                    if col in campaigns_data.columns:
                                        campaigns_data.loc[idx, col] = (
                                            processed_campaigns.loc[idx, col]
                                        )
                                updated_rows += 1

                        campaigns_updated_count += updated_rows
                        self.logger.info(
                            f"Applied {optimization_name}: updated {updated_rows} campaign rows"
                        )

                elif (
                    result_type == "portfolios"
                    and processed_df is not None
                    and portfolios_data is not None
                ):
                    self.logger.info(f"[DEBUG] Updating portfolios...")

                    # FIX: Handle portfolios updates correctly
                    if updated_indices:
                        # Use provided indices for precise update
                        self.logger.info(
                            f"[DEBUG] Using {len(updated_indices)} updated indices for portfolios"
                        )

                        for idx in updated_indices:
                            if (
                                idx in processed_df.index
                                and idx in portfolios_data.index
                            ):
                                portfolios_data.loc[idx] = processed_df.loc[idx]

                        portfolios_updated_count += len(updated_indices)

                    else:
                        # Update all rows from processed_df
                        # Ensure indices match
                        if not processed_df.index.equals(portfolios_data.index):
                            self.logger.warning(
                                "[DEBUG] Portfolio index mismatch, resetting indices"
                            )
                            processed_df = processed_df.reset_index(drop=True)
                            portfolios_data = portfolios_data.reset_index(drop=True)

                        # Update all matching rows
                        updated_portfolio_rows = 0
                        for idx in processed_df.index:
                            if idx in portfolios_data.index:
                                # Check if row actually changed
                                original_row = portfolios_data.loc[idx]
                                new_row = processed_df.loc[idx]

                                # Update if different
                                if not original_row.equals(new_row):
                                    for col in processed_df.columns:
                                        if col in portfolios_data.columns:
                                            portfolios_data.loc[idx, col] = (
                                                processed_df.loc[idx, col]
                                            )
                                    updated_portfolio_rows += 1

                        portfolios_updated_count += updated_portfolio_rows

                    # Use the count from processing details if available
                    actual_count = (
                        result["details"]
                        .get("processing", {})
                        .get("empty_portfolios_count", 0)
                    )
                    if actual_count > 0:
                        portfolios_updated_count = actual_count

                    self.logger.info(
                        f"Applied {optimization_name} to portfolios: {portfolios_updated_count} updates"
                    )

            # Create output file
            output_file = self._create_excel_file(campaigns_data, portfolios_data)

            # Build summary
            summary_details = {
                "total_optimizations": len(self.combined_results),
                "successful_optimizations": sum(
                    1 for r in self.combined_results if r["success"]
                ),
                "campaigns_updated": campaigns_updated_count,
                "portfolios_updated": portfolios_updated_count,
                "campaigns_total": len(campaigns_data)
                if campaigns_data is not None
                else 0,
                "portfolios_total": len(portfolios_data)
                if portfolios_data is not None
                else 0,
                "processing_summary": self.processing_summary,
                "sheets_created": [],
            }

            if campaigns_data is not None and len(campaigns_data) > 0:
                summary_details["sheets_created"].append("Sponsored Products Campaigns")

            if portfolios_data is not None and len(portfolios_data) > 0:
                summary_details["sheets_created"].append("Portfolios")

            self.logger.info(f"[DEBUG] ========== FINAL SUMMARY ==========")
            self.logger.info(
                f"[DEBUG] Combined output created: {len(summary_details['sheets_created'])} sheets"
            )
            self.logger.info(
                f"[DEBUG] Total campaigns updated: {campaigns_updated_count}"
            )
            self.logger.info(
                f"[DEBUG] Total portfolios updated: {portfolios_updated_count}"
            )

            return output_file, summary_details

        except Exception as e:
            self.logger.error(f"Error creating combined output: {str(e)}")
            import traceback

            self.logger.debug(f"Full traceback: {traceback.format_exc()}")

            error_details = {
                "error": str(e),
                "processing_summary": self.processing_summary,
                "successful_optimizations": sum(
                    1 for r in self.combined_results if r["success"]
                ),
                "total_optimizations": len(self.combined_results),
            }

            return None, error_details

    def _create_excel_file(
        self,
        campaigns_data: Optional[pd.DataFrame],
        portfolios_data: Optional[pd.DataFrame],
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

        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            # Write Sponsored Products Campaigns sheet (with ALL entities and columns)
            if campaigns_data is not None and len(campaigns_data) > 0:
                # Apply text formatting to prevent scientific notation
                campaigns_formatted = apply_text_format_before_write(campaigns_data)
                campaigns_formatted.to_excel(
                    writer, sheet_name="Sponsored Products Campaigns", index=False
                )
                self.logger.debug(
                    f"Wrote Campaigns sheet with {len(campaigns_data)} rows, {len(campaigns_data.columns)} columns"
                )

            # Write Portfolios sheet (with ALL columns)
            if portfolios_data is not None and len(portfolios_data) > 0:
                # Apply text formatting to prevent scientific notation
                portfolios_formatted = apply_text_format_before_write(portfolios_data)
                portfolios_formatted.to_excel(
                    writer, sheet_name="Portfolios", index=False
                )
                self.logger.debug(
                    f"Wrote Portfolios sheet with {len(portfolios_data)} rows, {len(portfolios_data.columns)} columns"
                )

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
