"""Results manager for merging optimization patches."""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
import logging
import time
from .contracts import OptimizationResult, MergeConflict, MergeError
from .constants import (
    PROTECTED_COLUMNS,
    CONDITIONALLY_PROTECTED_COLUMNS,
    COL_PORTFOLIO_ID,
    MAX_CELL_UPDATES,
    MAX_MERGE_TIME_SECONDS,
    ERROR_MESSAGES,
)


class ResultsManager:
    """Manages merging of optimization results."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.conflicts = []
        self.updated_indices = {}

    def merge_all(
        self,
        original_data: Dict[str, pd.DataFrame],
        optimization_results: List[OptimizationResult],
    ) -> Tuple[Dict[str, pd.DataFrame], Dict[str, Any]]:
        """
        Merge all optimization results into the original data.

        Args:
            original_data: Original data sheets
            optimization_results: List of optimization results to merge

        Returns:
            Tuple of (merged data, merge report)
        """
        start_time = time.time()
        self.logger.info(f"Starting merge of {len(optimization_results)} results")

        # Reset tracking
        self.conflicts = []
        self.updated_indices = {sheet: set() for sheet in original_data.keys()}

        # Create working copy
        merged_data = {sheet: df.copy() for sheet, df in original_data.items()}

        # Track statistics
        total_cells_updated = 0
        total_rows_updated = 0

        # Apply each optimization result
        for i, result in enumerate(optimization_results):
            self.logger.info(
                f"Applying result {i + 1}/{len(optimization_results)}: {result.result_type}"
            )

            cells_updated = self._apply_patch(
                merged_data, result.patch, result.merge_keys, optimization_index=i, result_type=result.result_type
            )

            total_cells_updated += cells_updated

        # Count total unique rows updated
        for sheet, indices in self.updated_indices.items():
            total_rows_updated += len(indices)

        # Create Terminal sheet if campaigns were modified
        print("TERMINAL DEBUG: About to call _create_terminal_sheet_if_needed")
        self._create_terminal_sheet_if_needed(merged_data, optimization_results)
        print("TERMINAL DEBUG: Finished calling _create_terminal_sheet_if_needed")

        # Check time limit
        elapsed_time = time.time() - start_time
        if elapsed_time > MAX_MERGE_TIME_SECONDS:
            raise MergeError(ERROR_MESSAGES["merge_timeout"])

        # Create report
        merge_report = {
            "total_rows_updated": total_rows_updated,
            "total_cells_updated": total_cells_updated,
            "conflicts": self.conflicts,
            "updated_indices": {
                sheet: list(indices) for sheet, indices in self.updated_indices.items()
            },
            "merge_time_seconds": elapsed_time,
        }

        # Fix column order for Portfolios sheet to match expected file format
        self._fix_portfolios_column_order(merged_data)

        self.logger.info(
            f"Merge complete: {total_rows_updated} rows, {total_cells_updated} cells updated"
        )
        return merged_data, merge_report

    def _apply_patch(
        self,
        data: Dict[str, pd.DataFrame],
        patch: Any,  # PatchData
        merge_keys: List[str],
        optimization_index: int,
        result_type: str = None,
    ) -> int:
        """
        Apply a single patch to the data.

        Args:
            data: Data to update (modified in place)
            patch: Patch to apply
            merge_keys: Keys to use for merging
            optimization_index: Index of the optimization (for conflict tracking)

        Returns:
            Number of cells updated
        """
        cells_updated = 0
        sheet_name = patch.sheet_name

        if sheet_name not in data:
            self.logger.warning(f"Sheet {sheet_name} not found, skipping patch")
            return 0

        df = data[sheet_name]

        for update in patch.updates:
            # Find the row to update
            row_idx = self._find_row(
                df, update.key_column, update.key_value, update.row_index
            )

            if row_idx is None:
                self.logger.warning(
                    f"Row not found for {update.key_column}={update.key_value}"
                )
                continue

            # Apply cell changes
            for column, new_value in update.cell_changes.items():
                # Check if column is protected
                if column in PROTECTED_COLUMNS:
                    self.logger.warning(f"Skipping protected column: {column}")
                    continue
                
                # Check if column is conditionally protected
                if column in CONDITIONALLY_PROTECTED_COLUMNS:
                    # Allow Portfolio ID updates for campaigns_without_portfolios optimization
                    if column == COL_PORTFOLIO_ID and result_type == "campaigns":
                        self.logger.info(f"Allowing Portfolio ID update for campaigns optimization")
                    else:
                        self.logger.warning(f"Skipping conditionally protected column: {column} for result_type: {result_type}")
                        continue

                if column not in df.columns:
                    # Add new column if it doesn't exist
                    self.logger.info(
                        f"Adding new column {column} to sheet {sheet_name}"
                    )
                    df[column] = ""

                # Check for conflict
                old_value = df.at[row_idx, column]
                if pd.notna(old_value) and old_value != new_value and old_value != "":
                    # Check if this cell was already updated
                    if row_idx in self.updated_indices[sheet_name]:
                        conflict = MergeConflict(
                            sheet_name=sheet_name,
                            row_index=row_idx,
                            column_name=column,
                            first_value=old_value,
                            second_value=new_value,
                            resolution="last_wins",
                        )
                        self.conflicts.append(conflict)
                        
                        # Enhanced conflict logging with user-friendly messages
                        if column == "Portfolio Name":
                            self.logger.info(
                                f"⚠️  Portfolio naming conflict: Row {row_idx+1} portfolio name changed "
                                f"from '{old_value}' to '{new_value}' (last optimization wins)"
                            )
                        elif column == "Portfolio ID":
                            self.logger.info(
                                f"⚠️  Portfolio assignment conflict: Row {row_idx+1} campaign moved "
                                f"from portfolio '{old_value}' to '{new_value}' (last optimization wins)"
                            )
                        elif column == "Operation":
                            self.logger.info(
                                f"⚠️  Operation conflict: Row {row_idx+1} operation changed "
                                f"from '{old_value}' to '{new_value}' (last optimization wins)"
                            )
                        else:
                            self.logger.info(
                                f"⚠️  Data conflict: Row {row_idx+1} {column} changed "
                                f"from '{old_value}' to '{new_value}' (last optimization wins)"
                            )

                # Apply update with proper dtype handling to eliminate pandas warnings
                try:
                    # Convert column to object type first to prevent dtype warnings
                    if df[column].dtype != 'object':
                        df[column] = df[column].astype('object')
                    
                    # Apply update with special formatting for numeric fields
                    if new_value is None or new_value == "":
                        df.at[row_idx, column] = ""
                    else:
                        # Convert to string and handle numeric formatting
                        str_value = str(new_value)
                        
                        # Remove .0 suffix from numeric values
                        if str_value.endswith('.0') and str_value.replace('.0', '').replace('-', '').isdigit():
                            str_value = str_value.replace('.0', '')
                        
                        df.at[row_idx, column] = str_value
                        
                except Exception as e:
                    # Fallback: force string conversion with .0 removal
                    str_value = str(new_value) if new_value is not None else ""
                    if str_value.endswith('.0') and str_value.replace('.0', '').replace('-', '').isdigit():
                        str_value = str_value.replace('.0', '')
                    df.at[row_idx, column] = str_value
                    self.logger.warning(f"Dtype conversion issue for {column}, using fallback: {e}")
                cells_updated += 1

                # Track updated row
                self.updated_indices[sheet_name].add(row_idx)

        return cells_updated

    def _find_row(
        self,
        df: pd.DataFrame,
        key_column: str,
        key_value: str,
        expected_index: int = None,
    ) -> Optional[int]:
        """
        Find a row in the dataframe by key.

        Args:
            df: DataFrame to search
            key_column: Column to search in
            key_value: Value to search for
            expected_index: Expected row index (for validation)

        Returns:
            Row index or None if not found
        """
        if key_column not in df.columns:
            return None

        # Convert key_value to string for comparison
        key_value_str = str(key_value)

        # Find matching rows
        mask = df[key_column].astype(str) == key_value_str
        matching_indices = df[mask].index.tolist()

        if not matching_indices:
            return None

        # If expected index provided, validate
        if expected_index is not None and expected_index in matching_indices:
            return expected_index

        # Return first match
        return matching_indices[0]

    def get_updated_indices(self) -> Dict[str, List[int]]:
        """Get dictionary of updated row indices by sheet."""
        return {sheet: list(indices) for sheet, indices in self.updated_indices.items()}
    
    def get_conflict_summary(self) -> Dict[str, Any]:
        """
        Generate user-friendly conflict summary for UI display.
        
        Returns:
            Dictionary with conflict statistics and user-friendly messages
        """
        if not self.conflicts:
            return {
                "total_conflicts": 0,
                "by_type": {},
                "messages": [],
                "user_message": "✅ No conflicts detected - all optimizations applied cleanly"
            }
        
        # Group conflicts by type
        by_type = {}
        user_messages = []
        
        for conflict in self.conflicts:
            conflict_type = conflict.column_name
            if conflict_type not in by_type:
                by_type[conflict_type] = 0
            by_type[conflict_type] += 1
        
        # Generate user-friendly messages
        for conflict_type, count in by_type.items():
            if conflict_type == "Portfolio Name":
                user_messages.append(f"📝 {count} portfolio naming conflicts (renamed portfolios got new names)")
            elif conflict_type == "Portfolio ID":  
                user_messages.append(f"🔄 {count} portfolio assignment conflicts (campaigns reassigned)")
            elif conflict_type == "Operation":
                user_messages.append(f"⚙️ {count} operation conflicts (update operations prioritized)")
            else:
                user_messages.append(f"📊 {count} {conflict_type} conflicts (last value used)")
        
        # Overall message
        total = len(self.conflicts)
        if total <= 5:
            severity = "✅"
            overall_msg = f"{severity} {total} minor conflicts resolved automatically"
        elif total <= 20:
            severity = "⚠️"
            overall_msg = f"{severity} {total} conflicts detected and resolved (review recommended)"
        else:
            severity = "🔴"
            overall_msg = f"{severity} {total} conflicts detected (data review strongly recommended)"
        
        return {
            "total_conflicts": total,
            "by_type": by_type,
            "messages": user_messages,
            "user_message": overall_msg,
            "severity": severity
        }
    
    def _create_terminal_sheet_if_needed(self, merged_data: Dict[str, pd.DataFrame], optimization_results: List[Any]):
        """
        Create Terminal sheet and move modified campaigns there if campaigns_without_portfolios was run.
        
        Args:
            merged_data: The merged data to modify
            optimization_results: List of optimization results to check
        """
        print("TERMINAL DEBUG: _create_terminal_sheet_if_needed method called!")
        self.logger.info("DEBUG: _create_terminal_sheet_if_needed called")
        from .constants import SHEET_CAMPAIGNS_CLEANED, SHEET_TERMINAL, COL_CAMPAIGN_ID
        
        # Check if campaigns_without_portfolios optimization was run specifically
        campaigns_result = None
        self.logger.info(f"DEBUG: Checking {len(optimization_results)} optimization results")
        for result in optimization_results:
            self.logger.info(f"DEBUG: Result type: {getattr(result, 'result_type', 'NO_TYPE')}")
            # Only create Terminal sheet for campaigns_without_portfolios, not organize_top_campaigns
            if (hasattr(result, 'result_type') and result.result_type == "campaigns" and
                hasattr(result, 'patch') and hasattr(result.patch, 'sheet_name') and 
                result.patch.sheet_name == "Campaign"):
                # Additional check to ensure this is campaigns_without_portfolios
                # by checking if the strategy name or messages contain the right indication
                is_campaigns_without_portfolios = any(
                    'without portfolios' in str(msg).lower() or 'campaigns_without_portfolios' in str(msg).lower()
                    for msg in getattr(result, 'messages', [])
                )
                if is_campaigns_without_portfolios:
                    campaigns_result = result
                    break
        
        if campaigns_result is None:
            self.logger.info("Campaigns without portfolios optimization not run, skipping Terminal sheet creation")
            return
        
        # Check if Campaign sheet exists
        if SHEET_CAMPAIGNS_CLEANED not in merged_data:
            self.logger.warning(f"Sheet {SHEET_CAMPAIGNS_CLEANED} not found, cannot create Terminal sheet")
            return
        
        campaigns_df = merged_data[SHEET_CAMPAIGNS_CLEANED].copy()
        
        # Extract Campaign IDs from the optimization result instead of using row indices
        # This ensures we get exactly the campaigns that were targeted by the optimization
        updated_campaign_ids = []
        for update in campaigns_result.patch.updates:
            updated_campaign_ids.append(str(update.key_value))
        
        self.logger.info(f"DEBUG: Campaign IDs from optimization result: {updated_campaign_ids}")
        
        if not updated_campaign_ids:
            self.logger.info("No campaign IDs found in optimization result, skipping Terminal sheet creation")
            return
        
        # Find campaigns by Campaign ID (not by row index)
        campaign_id_mask = campaigns_df[COL_CAMPAIGN_ID].astype(str).isin(updated_campaign_ids)
        terminal_campaigns = campaigns_df[campaign_id_mask]
        
        if len(terminal_campaigns) == 0:
            self.logger.warning("No campaigns found matching the updated Campaign IDs")
            return
        
        self.logger.info(f"Creating Terminal sheet with {len(terminal_campaigns)} campaigns using Campaign ID matching")
        self.logger.info(f"Terminal Campaign IDs: {terminal_campaigns[COL_CAMPAIGN_ID].astype(str).tolist()}")
        
        # Create Terminal sheet with campaigns found by Campaign ID
        terminal_df = terminal_campaigns.copy()
        
        # Ensure all Terminal sheet campaigns have Operation = "update"
        # This is critical for bulk upload - all campaigns in Terminal sheet must have Operation = "update"
        from .constants import COL_OPERATION, OPERATION_UPDATE
        
        # Force set Operation = "update" using multiple approaches to ensure it works
        try:
            # Method 1: Direct assignment
            terminal_df[COL_OPERATION] = OPERATION_UPDATE
            
            # Method 2: Explicit row-by-row assignment as backup
            for idx in range(len(terminal_df)):
                terminal_df.iloc[idx, terminal_df.columns.get_loc(COL_OPERATION)] = OPERATION_UPDATE
            
            # Method 3: Reset index and assign (in case of index issues)
            terminal_df = terminal_df.reset_index(drop=True)
            terminal_df[COL_OPERATION] = OPERATION_UPDATE
            
            self.logger.info(f"Successfully set Operation = '{OPERATION_UPDATE}' for all {len(terminal_df)} Terminal campaigns using multiple methods")
            
            # Verify the fix worked
            operation_values = terminal_df[COL_OPERATION].tolist()
            non_update_count = sum(1 for val in operation_values if pd.isna(val) or str(val) != OPERATION_UPDATE)
            if non_update_count > 0:
                self.logger.error(f"FAILED: {non_update_count} rows still don't have Operation='{OPERATION_UPDATE}': {operation_values}")
            else:
                self.logger.info(f"SUCCESS: All {len(terminal_df)} rows have Operation='{OPERATION_UPDATE}'")
                
        except Exception as e:
            self.logger.error(f"Error setting Operation column: {e}")
            # Fallback: create new DataFrame with explicit Operation column
            terminal_df[COL_OPERATION] = OPERATION_UPDATE
        
        # Remove modified campaigns from original Campaign sheet using Campaign ID matching
        campaigns_df_filtered = campaigns_df[~campaign_id_mask].copy()
        
        # Update the merged data
        merged_data[SHEET_CAMPAIGNS_CLEANED] = campaigns_df_filtered
        merged_data[SHEET_TERMINAL] = terminal_df
        
        self.logger.info(f"Terminal sheet created: {len(terminal_df)} rows moved, {len(campaigns_df_filtered)} rows remain in Campaign sheet")
    
    def _fix_portfolios_column_order(self, merged_data: Dict[str, pd.DataFrame]) -> None:
        """
        Fix the column order in Portfolios sheet to match expected file format.
        
        Expected order: Portfolio Name, Old Portfolio Name, ..., Camp Count (at end)
        """
        if "Portfolios" not in merged_data:
            return
            
        portfolios_df = merged_data["Portfolios"]
        
        # Define the expected column order
        expected_order = [
            'Product', 'Entity', 'Operation', 'Portfolio ID', 'Portfolio Name', 
            'Old Portfolio Name ', 'Budget Amount', 'Budget Currency Code', 
            'Budget Policy', 'Budget Start Date', 'Budget End Date', 
            'State (Informational only)', 'In Budget (Informational only)', 'Camp Count'
        ]
        
        # Check if we have all the expected columns
        current_columns = list(portfolios_df.columns)
        
        # Only reorder if we have the problematic columns (Old Portfolio Name  and Camp Count)
        if 'Old Portfolio Name ' in current_columns and 'Camp Count' in current_columns:
            # Filter expected_order to only include columns that actually exist
            available_expected_columns = [col for col in expected_order if col in current_columns]
            
            # Add any additional columns that aren't in our expected list (to preserve them)
            additional_columns = [col for col in current_columns if col not in expected_order]
            final_order = available_expected_columns + additional_columns
            
            # Reorder the DataFrame columns
            portfolios_df = portfolios_df[final_order]
            merged_data["Portfolios"] = portfolios_df
            
            self.logger.info(f"Fixed Portfolios column order: Old Portfolio Name moved from position {current_columns.index('Old Portfolio Name ')} to position {final_order.index('Old Portfolio Name ')}")
