"""Portfolio validation between template and bulk files."""

import pandas as pd
from typing import Dict, List, Set, Optional
from business.common.excluded_portfolios import EXCLUDED_PORTFOLIOS


class PortfolioValidator:
    """Validator for portfolio matching between template and bulk files."""

    def __init__(self):
        """Initialize the portfolio validator."""
        self.excluded_portfolios = set(EXCLUDED_PORTFOLIOS)

    def validate(self, template_df: pd.DataFrame, bulk_df: pd.DataFrame) -> Dict:
        """
        Validate portfolios between template and bulk files.

        Args:
            template_df: Template DataFrame with portfolio definitions
            bulk_df: Bulk DataFrame with campaign data

        Returns:
            Dictionary with validation results
        """
        result = {
            "valid": False,
            "missing_portfolios": [],
            "excluded_portfolios": [],
            "ignored_portfolios": [],
            "total_template": 0,
            "total_bulk": 0,
            "matched": 0,
        }

        try:
            # Get portfolios from template
            template_portfolios = self._get_template_portfolios(template_df)
            result["total_template"] = len(template_portfolios)

            # Get portfolios from bulk
            bulk_portfolios = self._get_bulk_portfolios(bulk_df)
            result["total_bulk"] = len(bulk_portfolios)

            # Find missing portfolios
            missing = bulk_portfolios - template_portfolios

            # Filter out excluded portfolios
            missing_non_excluded = missing - self.excluded_portfolios
            result["missing_portfolios"] = list(missing_non_excluded)

            # Track excluded portfolios that were found
            result["excluded_portfolios"] = list(missing & self.excluded_portfolios)

            # Find ignored portfolios
            result["ignored_portfolios"] = self._get_ignored_portfolios(template_df)

            # Calculate matched
            result["matched"] = len(bulk_portfolios & template_portfolios)

            # Determine if valid
            result["valid"] = len(result["missing_portfolios"]) == 0

        except Exception as e:
            result["error"] = str(e)
            result["valid"] = False

        return result

    def _get_template_portfolios(self, df: pd.DataFrame) -> Set[str]:
        """Extract portfolio names from template."""
        if "Portfolio Name" not in df.columns:
            return set()

        portfolios = df["Portfolio Name"].dropna().unique()
        return set(portfolios)

    def _get_bulk_portfolios(self, df: pd.DataFrame) -> Set[str]:
        """Extract portfolio names from bulk file."""
        column_name = None

        # Try different possible column names
        possible_names = [
            "Portfolio Name (Informational only)",
            "Portfolio Name",
            "Portfolio",
            "portfolio name (informational only)",
            "portfolio name",
        ]

        for name in possible_names:
            if name in df.columns:
                column_name = name
                break

        if column_name is None:
            return set()

        portfolios = df[column_name].dropna().unique()
        return set(portfolios)

    def _get_ignored_portfolios(self, template_df: pd.DataFrame) -> List[str]:
        """Get portfolios marked as 'Ignore' in template."""
        if "Base Bid" not in template_df.columns:
            return []

        ignored_df = template_df[
            template_df["Base Bid"].astype(str).str.lower() == "ignore"
        ]

        if "Portfolio Name" in ignored_df.columns:
            return ignored_df["Portfolio Name"].tolist()

        return []

    def check_portfolio_exists(
        self, portfolio_name: str, template_df: pd.DataFrame
    ) -> bool:
        """Check if a specific portfolio exists in template."""
        template_portfolios = self._get_template_portfolios(template_df)
        return portfolio_name in template_portfolios

    def is_excluded(self, portfolio_name: str) -> bool:
        """Check if a portfolio is in the excluded list."""
        return portfolio_name in self.excluded_portfolios


# Standalone function for backward compatibility
def validate_portfolios(template_df: pd.DataFrame, bulk_df: pd.DataFrame) -> Dict:
    """
    Validate portfolios between template and bulk files.

    Args:
        template_df: Template DataFrame with portfolio definitions
        bulk_df: Bulk DataFrame with campaign data

    Returns:
        Dictionary with validation results including:
        - valid: bool indicating if validation passed
        - missing_portfolios: list of missing portfolio names
        - excluded_portfolios: list of excluded portfolios found
        - ignored_portfolios: list of ignored portfolios
        - total_template: total portfolios in template
        - total_bulk: total portfolios in bulk
        - matched: number of matched portfolios
    """
    validator = PortfolioValidator()
    return validator.validate(template_df, bulk_df)


def check_missing_portfolios(
    template_df: pd.DataFrame, bulk_df: pd.DataFrame
) -> List[str]:
    """
    Get list of portfolios in bulk but not in template.

    Args:
        template_df: Template DataFrame
        bulk_df: Bulk DataFrame

    Returns:
        List of missing portfolio names
    """
    result = validate_portfolios(template_df, bulk_df)
    return result.get("missing_portfolios", [])


def get_ignored_portfolios(template_df: pd.DataFrame) -> List[str]:
    """
    Get list of portfolios marked as 'Ignore'.

    Args:
        template_df: Template DataFrame

    Returns:
        List of ignored portfolio names
    """
    validator = PortfolioValidator()
    return validator._get_ignored_portfolios(template_df)


def is_portfolio_excluded(portfolio_name: str) -> bool:
    """
    Check if a portfolio is in the excluded list.

    Args:
        portfolio_name: Name of portfolio to check

    Returns:
        True if portfolio is excluded
    """
    return portfolio_name in EXCLUDED_PORTFOLIOS
