"""Excluded portfolios list - these portfolios are always filtered out."""

# List of 13 portfolios to exclude from all optimizations
# These are the actual portfolio names from the specification - Case Sensitive!
EXCLUDED_PORTFOLIOS = [
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
    "Winter Clothing / Flat 15",
    "Flat 10",
    "Flat 20 | Winter Clothing",
]

# Alias for backward compatibility
FLAT_PORTFOLIOS = EXCLUDED_PORTFOLIOS


def is_excluded_portfolio(portfolio_name: str) -> bool:
    """
    Check if a portfolio is in the excluded list.

    Args:
        portfolio_name: Name of the portfolio to check

    Returns:
        True if the portfolio should be excluded
    """
    return portfolio_name in EXCLUDED_PORTFOLIOS


def get_excluded_portfolios() -> list:
    """
    Get the list of excluded portfolios.

    Returns:
        List of excluded portfolio names
    """
    return EXCLUDED_PORTFOLIOS.copy()


def get_excluded_count() -> int:
    """
    Get the count of excluded portfolios.

    Returns:
        Number of excluded portfolios
    """
    return len(EXCLUDED_PORTFOLIOS)


# Export the list for easy import
__all__ = [
    "EXCLUDED_PORTFOLIOS",
    "FLAT_PORTFOLIOS",
    "is_excluded_portfolio",
    "get_excluded_portfolios",
    "get_excluded_count",
]
