"""Processor for Empty Portfolios optimization."""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
import logging
from .constants import (
    PORTFOLIO_UPDATE_COLUMNS,
    SUCCESS_MESSAGES,
    EXCLUDED_PORTFOLIO_NAMES,
)


class EmptyPortfoliosProcessor:
    """Processes Empty Portfolios optimization logic."""

    def __init__(self):
        self.logger = logging.getLogger("empty_portfolios.processor")
        self.empty_portfolios = []
        self.updated_indices = []  # Track updated indices for results_manager

    def process(self, cleaned_data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """
        Process the optimization logic.

        Args:
            cleaned_data: Dictionary with cleaned DataFrames

        Returns:
            Dictionary with processed DataFrames
        """
        campaigns_df = cleaned_data["Sponsored Products Campaigns"].copy()
        portfolios_df = cleaned_data["Portfolios"].copy()

        # Reset tracking variables
        self.empty_portfolios = []
        self.updated_indices = []

        # Step 1: Find portfolios with campaigns
        portfolios_with_campaigns = set()
        if not campaigns_df.empty:
            # Ensure Portfolio IDs are strings for consistent matching
            campaign_portfolio_ids = (
                campaigns_df["Portfolio ID"].astype(str).str.strip()
            )
            portfolios_with_campaigns = set(campaign_portfolio_ids.unique())

        self.logger.info(
            f"Found {len(portfolios_with_campaigns)} portfolios with campaigns"
        )
        self.logger.info(
            f"Campaign Portfolio IDs: {sorted(list(portfolios_with_campaigns))[:10]}..."
        )  # Show first 10

        # Step 2: Identify empty portfolios
        empty_portfolio_indices = []
        debug_info = []
        excluded_count = 0

        for idx, row in portfolios_df.iterrows():
            portfolio_id = str(row["Portfolio ID"]).strip()
            portfolio_name = str(row["Portfolio Name"]).strip()

            # Check if portfolio has no campaigns
            has_no_campaigns = portfolio_id not in portfolios_with_campaigns

            # Check if name is not numeric
            is_name_not_numeric = not self._is_numeric_string(portfolio_name)

            # Check if portfolio name should be excluded
            is_excluded = self._is_excluded_portfolio(portfolio_name)
            if is_excluded:
                excluded_count += 1

            # Debug info for first 10 portfolios
            if len(debug_info) < 10:
                debug_info.append(
                    {
                        "id": portfolio_id,
                        "name": portfolio_name,
                        "has_campaigns": not has_no_campaigns,
                        "name_is_numeric": not is_name_not_numeric,
                        "is_excluded": is_excluded,
                        "will_be_empty": has_no_campaigns
                        and is_name_not_numeric
                        and not is_excluded,
                    }
                )

            # Only consider empty if: no campaigns, non-numeric name, and not excluded
            if has_no_campaigns and is_name_not_numeric and not is_excluded:
                empty_portfolio_indices.append(idx)
                self.empty_portfolios.append(
                    {
                        "id": portfolio_id,
                        "original_name": portfolio_name,
                        "index": idx,  # Store the index for tracking
                    }
                )

        # Log debug information (use print for immediate console output)
        print(f"\n=== EMPTY PORTFOLIOS DEBUG ===")
        print(f"Found {len(portfolios_with_campaigns)} portfolios with campaigns")
        print(f"Excluded {excluded_count} portfolios (Paused/Terminal)")
        print(f"Portfolio analysis debug (first 10):")
        for info in debug_info:
            print(
                f"  ID: {info['id']}, Name: '{info['name']}', Has Campaigns: {info['has_campaigns']}, Numeric Name: {info['name_is_numeric']}, Excluded: {info['is_excluded']}, Empty: {info['will_be_empty']}"
            )
        print(f"Found {len(empty_portfolio_indices)} empty portfolios")
        print(f"=== END DEBUG ===\n")

        self.logger.info(f"Found {len(empty_portfolio_indices)} empty portfolios")

        # Step 3: Update empty portfolios
        if empty_portfolio_indices:
            # Convert columns to object dtype to avoid pandas warnings
            portfolios_df["Portfolio Name"] = portfolios_df["Portfolio Name"].astype(
                "object"
            )
            portfolios_df["Operation"] = portfolios_df["Operation"].astype("object")
            portfolios_df["Budget Amount"] = portfolios_df["Budget Amount"].astype(
                "object"
            )
            portfolios_df["Budget Start Date"] = portfolios_df[
                "Budget Start Date"
            ].astype("object")

            # Find the smallest unused numeric name
            existing_numeric_names = set()
            for name in portfolios_df["Portfolio Name"]:
                if self._is_numeric_string(str(name)):
                    try:
                        existing_numeric_names.add(int(str(name)))
                    except:
                        pass

            # Update each empty portfolio
            next_number = 1
            for idx in empty_portfolio_indices:
                # Find next available number
                while next_number in existing_numeric_names:
                    next_number += 1

                # Update the portfolio
                portfolios_df.at[idx, "Portfolio Name"] = str(next_number)
                portfolios_df.at[idx, "Operation"] = PORTFOLIO_UPDATE_COLUMNS[
                    "Operation"
                ]
                portfolios_df.at[idx, "Budget Amount"] = PORTFOLIO_UPDATE_COLUMNS[
                    "Budget Amount"
                ]
                portfolios_df.at[idx, "Budget Start Date"] = PORTFOLIO_UPDATE_COLUMNS[
                    "Budget Start Date"
                ]

                # Mark for highlighting
                portfolios_df.at[idx, "_highlight"] = True

                # Track the updated index
                self.updated_indices.append(idx)

                existing_numeric_names.add(next_number)
                next_number += 1

                # Log the update
                self.logger.debug(
                    f"Updated portfolio at index {idx}: "
                    f"'{self.empty_portfolios[len(self.updated_indices) - 1]['original_name']}' -> '{next_number - 1}'"
                )

        self.logger.info(
            SUCCESS_MESSAGES["processing_complete"].format(len(empty_portfolio_indices))
        )
        self.logger.info(f"Updated indices: {self.updated_indices}")

        # Return processed data
        result = {
            "Sponsored Products Campaigns": campaigns_df,  # Already filtered to Entity = Campaign
            "Portfolios": portfolios_df,
        }

        return result

    def _is_numeric_string(self, value: str) -> bool:
        """Check if a string represents a numeric value."""
        try:
            # Remove whitespace and check
            cleaned = str(value).strip()
            if not cleaned:
                return False

            # Try to convert to float
            float(cleaned)
            return True
        except (ValueError, TypeError):
            return False

    def _is_excluded_portfolio(self, portfolio_name: str) -> bool:
        """Check if portfolio name should be excluded from optimization."""
        if not portfolio_name:
            return False

        # Check if portfolio name matches any excluded names (case-insensitive)
        cleaned_name = str(portfolio_name).strip()
        return cleaned_name in EXCLUDED_PORTFOLIO_NAMES

    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return {
            "empty_portfolios_count": len(self.empty_portfolios),
            "empty_portfolios": self.empty_portfolios.copy(),
        }

    def get_updated_indices(self) -> List[int]:
        """
        Get the indices of rows that were updated.

        Returns:
            List of row indices that were modified
        """
        return self.updated_indices.copy()
