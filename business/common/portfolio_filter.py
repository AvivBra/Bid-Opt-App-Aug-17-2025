"""Portfolio filtering utilities for bid optimizations."""

import pandas as pd
from typing import Dict, Any, Tuple, List, Optional
import logging


class PortfolioFilter:
    """Handles portfolio-related filtering operations."""

    def __init__(self):
        self.logger = logging.getLogger("common.portfolio_filter")

        # 10 excluded portfolios (case sensitive)
        self.excluded_portfolios = [
            "Flat 30",
            "Flat 25",
            "Flat 40",
            "Flat 25 | Opt",
            "Flat 30 | Opt",
            "Flat 20",
            "Flat 15",
            "Flat 40 | Opt",
            "Flat 20 | Opt",
            "Flat 15 | Opt",
        ]

    def filter_excluded_portfolios(
        self,
        df: pd.DataFrame,
        portfolio_col: str = "Portfolio Name (Informational only)",
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Remove rows from excluded 'Flat' portfolios.

        Args:
            df: DataFrame to filter
            portfolio_col: Name of portfolio column

        Returns:
            Tuple of (filtered_dataframe, filter_details)
        """

        details = {
            "original_rows": len(df),
            "excluded_portfolios": self.excluded_portfolios.copy(),
            "filtered_rows": 0,
            "remaining_rows": 0,
        }

        if df.empty:
            return df, details

        if portfolio_col not in df.columns:
            self.logger.warning(f"Portfolio column '{portfolio_col}' not found")
            details["error"] = "Portfolio column not found"
            return df, details

        # Filter out excluded portfolios (case sensitive)
        excluded_mask = df[portfolio_col].isin(self.excluded_portfolios)
        filtered_df = df[~excluded_mask].copy()

        details["filtered_rows"] = excluded_mask.sum()
        details["remaining_rows"] = len(filtered_df)

        if details["filtered_rows"] > 0:
            self.logger.info(
                f"Filtered out {details['filtered_rows']} rows from excluded portfolios"
            )

        return filtered_df, details

    def filter_ignored_portfolios(
        self,
        df: pd.DataFrame,
        template_data: Dict[str, pd.DataFrame],
        portfolio_col: str = "Portfolio Name (Informational only)",
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Remove rows from portfolios marked as 'Ignore' in template.

        Args:
            df: Bulk data DataFrame
            template_data: Template data with Port Values sheet
            portfolio_col: Name of portfolio column

        Returns:
            Tuple of (filtered_dataframe, filter_details)
        """

        details = {
            "original_rows": len(df),
            "ignored_portfolios": [],
            "filtered_rows": 0,
            "remaining_rows": 0,
        }

        if df.empty:
            return df, details

        if portfolio_col not in df.columns:
            self.logger.warning(f"Portfolio column '{portfolio_col}' not found")
            details["error"] = "Portfolio column not found"
            return df, details

        # Get Port Values sheet
        port_values = template_data.get("Port Values", pd.DataFrame())

        if port_values.empty:
            self.logger.warning("Port Values sheet is empty")
            details["error"] = "Port Values sheet empty"
            return df, details

        # Find portfolios with Base Bid = 'Ignore'
        if "Base Bid" not in port_values.columns:
            self.logger.warning("Base Bid column not found in Port Values")
            details["error"] = "Base Bid column not found"
            return df, details

        # Convert Base Bid to string and check for 'Ignore' (case insensitive)
        port_values["Base Bid"] = port_values["Base Bid"].astype(str)
        ignored_mask = port_values["Base Bid"].str.lower() == "ignore"
        ignored_portfolios = port_values[ignored_mask]["Portfolio Name"].tolist()

        details["ignored_portfolios"] = ignored_portfolios

        if ignored_portfolios:
            # Filter out ignored portfolios
            ignored_data_mask = df[portfolio_col].isin(ignored_portfolios)
            filtered_df = df[~ignored_data_mask].copy()

            details["filtered_rows"] = ignored_data_mask.sum()
            details["remaining_rows"] = len(filtered_df)

            if details["filtered_rows"] > 0:
                self.logger.info(
                    f"Filtered out {details['filtered_rows']} rows from "
                    f"{len(ignored_portfolios)} ignored portfolios"
                )

            return filtered_df, details

        details["remaining_rows"] = len(df)
        return df, details

    def validate_portfolio_match(
        self,
        bulk_df: pd.DataFrame,
        template_data: Dict[str, pd.DataFrame],
        portfolio_col: str = "Portfolio Name (Informational only)",
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validate that all portfolios in bulk exist in template.

        Args:
            bulk_df: Bulk data DataFrame
            template_data: Template data with Port Values sheet
            portfolio_col: Name of portfolio column

        Returns:
            Tuple of (is_valid, message, details)
        """

        details = {
            "bulk_portfolios": set(),
            "template_portfolios": set(),
            "missing_portfolios": set(),
            "excluded_portfolios_found": set(),
            "ignored_portfolios_found": set(),
        }

        # Get unique portfolios from bulk
        if portfolio_col in bulk_df.columns:
            details["bulk_portfolios"] = set(bulk_df[portfolio_col].dropna().unique())
        else:
            return (
                False,
                f"Portfolio column '{portfolio_col}' not found in bulk",
                details,
            )

        # Get portfolios from template
        port_values = template_data.get("Port Values", pd.DataFrame())
        if not port_values.empty and "Portfolio Name" in port_values.columns:
            details["template_portfolios"] = set(
                port_values["Portfolio Name"].dropna().unique()
            )
        else:
            return False, "Port Values sheet or Portfolio Name column missing", details

        # Find missing portfolios
        missing = details["bulk_portfolios"] - details["template_portfolios"]

        # Remove excluded portfolios from missing
        missing = missing - set(self.excluded_portfolios)

        details["missing_portfolios"] = missing

        # Check for excluded portfolios in bulk
        details["excluded_portfolios_found"] = details["bulk_portfolios"] & set(
            self.excluded_portfolios
        )

        # Check for ignored portfolios
        if "Base Bid" in port_values.columns:
            port_values["Base Bid"] = port_values["Base Bid"].astype(str)
            ignored_mask = port_values["Base Bid"].str.lower() == "ignore"
            ignored_portfolios = set(
                port_values[ignored_mask]["Portfolio Name"].tolist()
            )
            details["ignored_portfolios_found"] = (
                details["bulk_portfolios"] & ignored_portfolios
            )

        if missing:
            return False, f"Missing portfolios in template: {missing}", details

        return True, "All portfolios validated", details

    def is_flat_portfolio(self, portfolio_name: str) -> bool:
        """
        Check if a portfolio is in the excluded list.

        Args:
            portfolio_name: Name of the portfolio

        Returns:
            True if the portfolio should be excluded
        """
        return portfolio_name in self.excluded_portfolios

    def get_excluded_list(self) -> List[str]:
        """
        Get the list of excluded portfolios.

        Returns:
            List of excluded portfolio names
        """
        return self.excluded_portfolios.copy()

    def count_filtered(
        self,
        df: pd.DataFrame,
        portfolio_col: str = "Portfolio Name (Informational only)",
    ) -> Dict[str, int]:
        """
        Count how many rows would be filtered by various criteria.

        Args:
            df: DataFrame to analyze
            portfolio_col: Name of portfolio column

        Returns:
            Dictionary with counts
        """

        counts = {
            "total_rows": len(df),
            "excluded_portfolios": 0,
            "unique_portfolios": 0,
        }

        if portfolio_col in df.columns:
            # Count rows from excluded portfolios
            excluded_mask = df[portfolio_col].isin(self.excluded_portfolios)
            counts["excluded_portfolios"] = excluded_mask.sum()

            # Count unique portfolios
            counts["unique_portfolios"] = df[portfolio_col].nunique()

        return counts
