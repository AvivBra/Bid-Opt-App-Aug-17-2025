"""Portfolio filtering utilities."""

import pandas as pd
from typing import List, Set, Tuple, Dict, Any
from business.common.excluded_portfolios import (
    EXCLUDED_PORTFOLIOS,
    is_excluded_portfolio,
)
import logging


class PortfolioFilter:
    """Filters portfolios based on various criteria."""

    def __init__(self):
        self.logger = logging.getLogger("portfolio_filter")
        self.excluded_portfolios = set(EXCLUDED_PORTFOLIOS)

    def filter_excluded_portfolios(
        self, df: pd.DataFrame, portfolio_col: str
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Filter out excluded 'Flat' portfolios from bulk data.

        Args:
            df: Bulk data DataFrame
            portfolio_col: Name of portfolio column (should be 'Portfolio Name (Informational only)')

        Returns:
            Tuple of (filtered_dataframe, filter_details)
        """

        details = {
            "original_rows": len(df),
            "excluded_portfolios": [],
            "filtered_rows": 0,
            "remaining_rows": 0,
        }

        if df.empty or portfolio_col not in df.columns:
            # FIXED: Try exact column name if provided column not found
            if (
                portfolio_col not in df.columns
                and "Portfolio Name (Informational only)" in df.columns
            ):
                portfolio_col = "Portfolio Name (Informational only)"
            else:
                return df, details

        try:
            # Create exclusion mask
            portfolio_series = df[portfolio_col].astype(str).str.strip()
            exclusion_mask = portfolio_series.apply(is_excluded_portfolio)

            # Track excluded portfolios
            excluded_portfolios = portfolio_series[exclusion_mask].unique().tolist()
            details["excluded_portfolios"] = excluded_portfolios
            details["filtered_rows"] = exclusion_mask.sum()

            # Filter data
            filtered_df = df[~exclusion_mask].copy()
            details["remaining_rows"] = len(filtered_df)

            self.logger.info(
                f"Filtered out {details['filtered_rows']} rows from {len(excluded_portfolios)} excluded portfolios"
            )

            return filtered_df, details

        except Exception as e:
            self.logger.error(f"Error filtering excluded portfolios: {str(e)}")
            return df, details

    def filter_ignored_portfolios(
        self,
        df: pd.DataFrame,
        portfolio_col: str,
        template_data: Dict[str, pd.DataFrame],
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Filter out portfolios marked as 'Ignore' in template.

        Args:
            df: Bulk data DataFrame
            portfolio_col: Name of portfolio column
            template_data: Template data with Port Values sheet

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

        try:
            # Get ignored portfolios from template
            ignored_portfolios = self._get_ignored_portfolios(template_data)

            if not ignored_portfolios:
                details["remaining_rows"] = len(df)
                return df, details

            # Filter out ignored portfolios
            portfolio_series = df[portfolio_col].astype(str).str.strip()
            ignore_mask = portfolio_series.isin(ignored_portfolios)

            # Track details
            details["ignored_portfolios"] = list(ignored_portfolios)
            details["filtered_rows"] = ignore_mask.sum()

            # Filter data
            filtered_df = df[~ignore_mask].copy()
            details["remaining_rows"] = len(filtered_df)

            self.logger.info(
                f"Filtered out {details['filtered_rows']} rows from {len(ignored_portfolios)} ignored portfolios"
            )

            return filtered_df, details

        except Exception as e:
            self.logger.error(f"Error filtering ignored portfolios: {str(e)}")
            return df, details

    def filter_zero_sales_candidates(
        self, df: pd.DataFrame, units_col: str
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Filter to only rows with Units = 0 (zero sales).

        Args:
            df: Bulk data DataFrame
            units_col: Name of units column

        Returns:
            Tuple of (filtered_dataframe, filter_details)
        """

        details = {
            "original_rows": len(df),
            "zero_sales_rows": 0,
            "non_zero_sales_rows": 0,
        }

        if df.empty or units_col not in df.columns:
            return df, details

        try:
            # Filter to Units = 0
            zero_sales_mask = df[units_col] == 0

            # Track details
            details["zero_sales_rows"] = zero_sales_mask.sum()
            details["non_zero_sales_rows"] = (~zero_sales_mask).sum()

            # Filter data
            filtered_df = df[zero_sales_mask].copy()

            self.logger.info(
                f"Filtered to {details['zero_sales_rows']} zero sales rows out of {len(df)} total"
            )

            return filtered_df, details

        except Exception as e:
            self.logger.error(f"Error filtering zero sales candidates: {str(e)}")
            return df, details

    def apply_all_filters(
        self,
        df: pd.DataFrame,
        portfolio_col: str,
        units_col: str,
        template_data: Dict[str, pd.DataFrame],
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Apply all filters in sequence.

        Args:
            df: Bulk data DataFrame
            portfolio_col: Name of portfolio column (should be 'Portfolio Name (Informational only)')
            units_col: Name of units column
            template_data: Template data dictionary

        Returns:
            Tuple of (filtered_dataframe, combined_filter_details)
        """

        combined_details = {
            "original_rows": len(df),
            "final_rows": 0,
            "excluded_filter": {},
            "ignored_filter": {},
            "zero_sales_filter": {},
            "total_filtered": 0,
        }

        current_df = df.copy()

        # FIXED: Ensure we're using the correct column name
        if (
            portfolio_col not in current_df.columns
            and "Portfolio Name (Informational only)" in current_df.columns
        ):
            portfolio_col = "Portfolio Name (Informational only)"

        # Step 1: Filter excluded portfolios
        current_df, excluded_details = self.filter_excluded_portfolios(
            current_df, portfolio_col
        )
        combined_details["excluded_filter"] = excluded_details

        # Step 2: Filter ignored portfolios
        current_df, ignored_details = self.filter_ignored_portfolios(
            current_df, portfolio_col, template_data
        )
        combined_details["ignored_filter"] = ignored_details

        # Step 3: Filter to zero sales only
        current_df, zero_details = self.filter_zero_sales_candidates(
            current_df, units_col
        )
        combined_details["zero_sales_filter"] = zero_details

        # Calculate final statistics
        combined_details["final_rows"] = len(current_df)
        combined_details["total_filtered"] = len(df) - len(current_df)

        self.logger.info(
            f"Applied all filters: {len(df)} -> {len(current_df)} rows ({combined_details['total_filtered']} filtered)"
        )

        return current_df, combined_details

    def _get_ignored_portfolios(
        self, template_data: Dict[str, pd.DataFrame]
    ) -> Set[str]:
        """Get set of portfolios marked as 'Ignore' in template."""

        try:
            port_values = template_data.get("Port Values")
            if port_values is None or port_values.empty:
                return set()

            # Find portfolios with Base Bid = 'Ignore'
            base_bids = port_values["Base Bid"].astype(str).str.strip().str.lower()
            ignored_mask = base_bids == "ignore"

            ignored_portfolios = (
                port_values[ignored_mask]["Portfolio Name"].astype(str).str.strip()
            )

            return set(ignored_portfolios)

        except Exception as e:
            self.logger.error(f"Error getting ignored portfolios: {str(e)}")
            return set()

    def get_filter_summary(self, filter_details: Dict[str, Any]) -> str:
        """Generate human-readable filter summary."""

        summary_parts = []

        # Original rows
        summary_parts.append(
            f"Started with {filter_details.get('original_rows', 0)} rows"
        )

        # Excluded portfolios
        if "excluded_filter" in filter_details:
            excluded = filter_details["excluded_filter"]
            if excluded.get("filtered_rows", 0) > 0:
                summary_parts.append(
                    f"Excluded {excluded['filtered_rows']} rows from {len(excluded.get('excluded_portfolios', []))} flat portfolios"
                )

        # Ignored portfolios
        if "ignored_filter" in filter_details:
            ignored = filter_details["ignored_filter"]
            if ignored.get("filtered_rows", 0) > 0:
                summary_parts.append(
                    f"Ignored {ignored['filtered_rows']} rows from {len(ignored.get('ignored_portfolios', []))} portfolios"
                )

        # Zero sales filter
        if "zero_sales_filter" in filter_details:
            zero_sales = filter_details["zero_sales_filter"]
            summary_parts.append(
                f"Kept {zero_sales.get('zero_sales_rows', 0)} zero sales rows"
            )

        # Final result
        summary_parts.append(f"Result: {filter_details.get('final_rows', 0)} rows")

        return " | ".join(summary_parts)
