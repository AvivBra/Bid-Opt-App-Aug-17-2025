"""Portfolio validation utilities - SIMPLIFIED."""

import pandas as pd
from typing import Tuple, Dict, Any, Set, List
from business.common.excluded_portfolios import EXCLUDED_PORTFOLIOS


class PortfolioValidator:
    """Validates portfolio matching between template and bulk files."""

    def __init__(self):
        self.excluded_portfolios = EXCLUDED_PORTFOLIOS

    def validate_portfolio_matching(
        self, template_data: Dict[str, pd.DataFrame], bulk_data: pd.DataFrame
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        SIMPLIFIED portfolio matching validation.

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
            "zero_sales_candidates": 0,
            "processing_ready": 0,
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

                    # Check if ignored
                    base_bid = str(row.get("Base Bid", "")).lower()
                    if base_bid == "ignore":
                        ignored_portfolios.add(portfolio)

        details["template_portfolios"] = list(template_portfolios)
        details["ignored_portfolios"] = list(ignored_portfolios)

        # Get bulk portfolios
        bulk_portfolios = set()
        portfolio_col = None

        # Find portfolio column in bulk
        for col in bulk_data.columns:
            if "portfolio" in col.lower():
                portfolio_col = col
                break

        if portfolio_col:
            bulk_portfolios = set(
                bulk_data[portfolio_col].dropna().astype(str).str.strip().unique()
            )
            bulk_portfolios.discard("nan")
            bulk_portfolios.discard("")

        details["bulk_portfolios"] = list(bulk_portfolios)

        # Check for missing portfolios
        missing_in_template = (
            bulk_portfolios - template_portfolios - set(self.excluded_portfolios)
        )
        details["missing_in_template"] = list(missing_in_template)

        missing_in_bulk = (
            template_portfolios - bulk_portfolios - set(self.excluded_portfolios)
        )
        details["missing_in_bulk"] = list(missing_in_bulk)

        # Check matching
        matching = template_portfolios & bulk_portfolios
        details["matching_portfolios"] = list(matching)

        # Count zero sales candidates (simplified)
        if "Units" in bulk_data.columns:
            zero_sales = bulk_data[bulk_data["Units"] == 0]
            details["zero_sales_candidates"] = len(zero_sales)

        # Calculate processing ready count
        active_portfolios = template_portfolios - ignored_portfolios
        if portfolio_col and active_portfolios:
            processing_ready = bulk_data[
                bulk_data[portfolio_col].isin(active_portfolios)
            ]
            details["processing_ready"] = len(processing_ready)

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
        active = set()

        if (
            "Portfolio Name" in port_values.columns
            and "Base Bid" in port_values.columns
        ):
            for idx, row in port_values.iterrows():
                portfolio = str(row["Portfolio Name"]).strip()
                base_bid = str(row["Base Bid"]).lower()

                if portfolio and portfolio != "nan" and base_bid != "ignore":
                    active.add(portfolio)

        return active
