"""Results manager for merging optimization patches."""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
import logging
import time
from .contracts import OptimizationResult, MergeConflict, MergeError
from .constants import (
    PROTECTED_COLUMNS,
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
                merged_data, result.patch, result.merge_keys, optimization_index=i
            )

            total_cells_updated += cells_updated

        # Count total unique rows updated
        for sheet, indices in self.updated_indices.items():
            total_rows_updated += len(indices)

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
                if column in PROTECTED_COLUMNS:
                    self.logger.warning(f"Skipping protected column: {column}")
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
                    
                    # Then apply the update
                    if isinstance(new_value, (int, float)) and str(new_value).replace('.', '').isdigit():
                        # For numeric values, ensure proper conversion
                        df.at[row_idx, column] = str(new_value).replace('.0', '') if str(new_value).endswith('.0') else str(new_value)
                    else:
                        # For string values, ensure string type
                        df.at[row_idx, column] = str(new_value) if new_value is not None else ""
                except Exception as e:
                    # Fallback: force string conversion
                    df.at[row_idx, column] = str(new_value) if new_value is not None else ""
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
