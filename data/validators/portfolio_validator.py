"""Portfolio validation utilities - WITHOUT STATISTICS."""

import pandas as pd
from typing import Tuple, Dict, Any, Set, List
from business.common.excluded_portfolios import get_excluded_portfolios_set


class PortfolioValidator:
    """Validates portfolio matching between template and bulk files."""

    def __init__(self):
        self.excluded_portfolios = get_excluded_portfolios_set()

    def validate_portfolio_matching(
        self, template_data: Dict[str, pd.DataFrame], bulk_data: pd.DataFrame
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validate portfolio matching between template and bulk files.

        Returns:
            Tuple of (is_valid, message, details)
        """

        details = {
            "template_portfolios": [],
            "bulk_portfolios": [],
            "missing_in_template": [],
            "missing_in_bulk": [],
            "matching_portfolios": [],
            "ignored_portfolios": [],
            "excluded_portfolios": list(self.excluded_portfolios),
            # REMOVED: Statistics that were displayed on UI
            # "zero_sales_candidates": 0,
            # "processing_ready": 0,
        }

        # Get template portfolios
        if "Port Values" not in template_data:
            return False, "Port Values sheet not found", details

        port_values = template_data["Port Values"]

        if port_values.empty:
            return False, "Port Values sheet is empty", details

        # Extract portfolio names from template
        template_portfolios = set()
        ignored_portfolios = set()

        if "Portfolio Name" in port_values.columns:
            for idx, row in port_values.iterrows():
                portfolio = str(row["Portfolio Name"]).strip()
                if portfolio and portfolio != "nan":
                    template_portfolios.add(portfolio)

                    # Check if ignored (case insensitive for 'ignore')
                    base_bid = str(row.get("Base Bid", "")).strip()
                    if base_bid.lower() == "ignore":
                        ignored_portfolios.add(portfolio)

        details["template_portfolios"] = list(template_portfolios)
        details["ignored_portfolios"] = list(ignored_portfolios)

        # Get bulk portfolios - using exact column name
        bulk_portfolios = set()
        portfolio_col = "Portfolio Name (Informational only)"

        # Check if the exact column exists
        if portfolio_col in bulk_data.columns:
            bulk_portfolios = set(
                bulk_data[portfolio_col].dropna().astype(str).str.strip().unique()
            )
            bulk_portfolios.discard("nan")
            bulk_portfolios.discard("")
        else:
            # Fallback: Try to find column containing "portfolio" (case-insensitive)
            for col in bulk_data.columns:
                if "portfolio" in col.lower():
                    portfolio_col = col
                    bulk_portfolios = set(
                        bulk_data[portfolio_col]
                        .dropna()
                        .astype(str)
                        .str.strip()
                        .unique()
                    )
                    bulk_portfolios.discard("nan")
                    bulk_portfolios.discard("")
                    break

        details["bulk_portfolios"] = list(bulk_portfolios)

        # Check for missing portfolios - EXCLUDING the Flat portfolios
        # Portfolios in bulk but not in template (and not in excluded list)
        missing_in_template = (
            bulk_portfolios - template_portfolios - self.excluded_portfolios
        )
        details["missing_in_template"] = list(missing_in_template)

        # Portfolios in template but not in bulk (for info only)
        missing_in_bulk = (
            template_portfolios - bulk_portfolios - self.excluded_portfolios
        )
        details["missing_in_bulk"] = list(missing_in_bulk)

        # Check matching portfolios
        matching = template_portfolios & bulk_portfolios
        details["matching_portfolios"] = list(matching)

        # REMOVED: Statistics calculations that were displayed on UI
        # These calculations were causing confusion with incorrect counts

        # Count zero sales candidates - REMOVED
        # if "Units" in bulk_data.columns:
        #     zero_sales = bulk_data[bulk_data["Units"] == 0]
        #     details["zero_sales_candidates"] = len(zero_sales)

        # Calculate processing ready count - REMOVED
        # active_portfolios = template_portfolios - ignored_portfolios
        # if portfolio_col in bulk_data.columns and active_portfolios:
        #     portfolios_to_process = active_portfolios - self.excluded_portfolios
        #     processing_ready = bulk_data[
        #         bulk_data[portfolio_col].isin(portfolios_to_process)
        #     ]
        #     details["processing_ready"] = len(processing_ready)

        # Determine if valid
        if missing_in_template:
            return (
                False,
                f"Missing {len(missing_in_template)} portfolios in template",
                details,
            )

        if len(ignored_portfolios) == len(template_portfolios):
            return False, "All portfolios are set to 'Ignore'", details

        # Success
        active_count = len(template_portfolios) - len(ignored_portfolios)
        return (
            True,
            f"Portfolios valid: {active_count} active, {len(ignored_portfolios)} ignored",
            details,
        )

    def get_active_portfolios(self, template_data: Dict[str, pd.DataFrame]) -> Set[str]:
        """Get set of active (non-ignored) portfolios."""

        if "Port Values" not in template_data:
            return set()

        port_values = template_data["Port Values"]
        active_portfolios = set()

        if (
            "Portfolio Name" in port_values.columns
            and "Base Bid" in port_values.columns
        ):
            for idx, row in port_values.iterrows():
                portfolio = str(row["Portfolio Name"]).strip()
                base_bid = str(row.get("Base Bid", "")).strip()

                # Portfolio is active if Base Bid is not 'Ignore' (case insensitive)
                if portfolio and portfolio != "nan" and base_bid.lower() != "ignore":
                    active_portfolios.add(portfolio)

        return active_portfolios

    def check_portfolio_in_excluded_list(self, portfolio_name: str) -> bool:
        """Check if a portfolio is in the excluded list."""
        return portfolio_name in self.excluded_portfolios
