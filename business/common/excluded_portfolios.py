"""Excluded portfolios list for bid optimization."""

from typing import List, Set


def get_excluded_portfolios() -> List[str]:
    """
    Get list of 10 'Flat' portfolios that should be excluded from processing.

    These portfolios are filtered out during Zero Sales optimization
    as specified in the PRD requirements.

    Returns:
        List of portfolio names to exclude (Case Sensitive!)
    """

    # The 10 predefined 'Flat' portfolios that must be filtered out
    # EXACT names as specified in PRD - Case Sensitive!
    excluded_portfolios = [
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

    return excluded_portfolios


def get_excluded_portfolios_set() -> Set[str]:
    """Get excluded portfolios as a set for faster lookups."""
    return set(get_excluded_portfolios())


def is_portfolio_excluded(portfolio_name: str) -> bool:
    """
    Check if a portfolio name should be excluded from processing.

    Args:
        portfolio_name: Name of the portfolio to check

    Returns:
        True if portfolio should be excluded, False otherwise
    """

    if not portfolio_name:
        return False

    excluded_set = get_excluded_portfolios_set()

    # Exact match only (Case Sensitive as per PRD)
    return portfolio_name in excluded_set


def filter_excluded_portfolios(portfolio_list: List[str]) -> List[str]:
    """
    Filter out excluded portfolios from a list.

    Args:
        portfolio_list: List of portfolio names

    Returns:
        Filtered list with excluded portfolios removed
    """

    excluded_set = get_excluded_portfolios_set()
    return [p for p in portfolio_list if p not in excluded_set]


def get_exclusion_stats(portfolio_list: List[str]) -> dict:
    """
    Get statistics about exclusions in a portfolio list.

    Args:
        portfolio_list: List of portfolio names to check

    Returns:
        Dictionary with exclusion statistics
    """

    excluded_set = get_excluded_portfolios_set()

    excluded_found = [p for p in portfolio_list if p in excluded_set]

    return {
        "total_portfolios": len(portfolio_list),
        "excluded_count": len(excluded_found),
        "excluded_names": excluded_found,
        "remaining_count": len(portfolio_list) - len(excluded_found),
    }
