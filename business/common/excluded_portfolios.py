"""Excluded portfolios list for bid optimization."""

from typing import List, Set


def get_excluded_portfolios() -> List[str]:
    """
    Get list of 10 'Flat' portfolios that should be excluded from processing.
    
    These portfolios are filtered out during Zero Sales optimization
    as specified in the PRD requirements.
    
    Returns:
        List of portfolio names to exclude
    """
    
    # The 10 predefined 'Flat' portfolios that should be filtered out
    # These names are based on common Amazon Ads flat bidding portfolio conventions
    excluded_portfolios = [
        "Flat Portfolio",
        "Flat Bidding Portfolio", 
        "Manual Flat Portfolio",
        "Flat CPC Portfolio",
        "Static Bid Portfolio",
        "Fixed Bid Portfolio",
        "Flat Rate Portfolio",
        "Manual Bidding Portfolio",
        "No Auto Bid Portfolio",
        "Flat Targeting Portfolio"
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
    
    # Exact match (case-insensitive)
    if portfolio_name.strip().lower() in {p.lower() for p in excluded_set}:
        return True
    
    # Partial match for common flat portfolio patterns
    portfolio_lower = portfolio_name.lower().strip()
    
    flat_patterns = [
        'flat portfolio',
        'flat bidding', 
        'manual flat',
        'static bid',
        'fixed bid',
        'flat rate',
        'no auto bid'
    ]
    
    for pattern in flat_patterns:
        if pattern in portfolio_lower:
            return True
    
    return False


def filter_excluded_portfolios(portfolio_list: List[str]) -> List[str]:
    """
    Filter out excluded portfolios from a list.
    
    Args:
        portfolio_list: List of portfolio names
        
    Returns:
        Filtered list with excluded portfolios removed
    """
    
    return [p for p in portfolio_list if not is_portfolio_excluded(p)]


def get_exclusion_stats(portfolio_list: List[str]) -> dict:
    """
    Get statistics about exclusions in a portfolio list.
    
    Args:
        portfolio_list: List of portfolio names
        
    Returns:
        Dictionary with exclusion statistics
    """
    
    total = len(portfolio_list)
    excluded = [p for p in portfolio_list if is_portfolio_excluded(p)]
    excluded_count = len(excluded)
    
    return {
        'total_portfolios': total,
        'excluded_count': excluded_count,
        'included_count': total - excluded_count,
        'exclusion_rate': (excluded_count / total) * 100 if total > 0 else 0,
        'excluded_portfolios': excluded
    }