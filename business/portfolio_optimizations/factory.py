"""Factory for creating optimization strategies."""

import logging
from typing import Dict, List, Optional, Any
from .contracts import OptimizationStrategy
from .strategies import EmptyPortfoliosStrategy, CampaignsWithoutPortfoliosStrategy
from .constants import OPTIMIZATION_ORDER


class PortfolioOptimizationFactory:
    """Factory for creating and managing portfolio optimization strategies."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._strategies = {}
        self._register_strategies()
    
    def _register_strategies(self):
        """Register all available optimization strategies."""
        # Register each strategy
        strategies = [
            EmptyPortfoliosStrategy(),
            CampaignsWithoutPortfoliosStrategy()
        ]
        
        for strategy in strategies:
            name = strategy.get_name()
            self._strategies[name] = strategy
            self.logger.info(f"Registered strategy: {name}")
    
    def create_strategy(self, strategy_name: str) -> Optional[OptimizationStrategy]:
        """
        Create an instance of the specified strategy.
        
        Args:
            strategy_name: Name of the strategy to create
            
        Returns:
            Strategy instance or None if not found
        """
        if strategy_name not in self._strategies:
            self.logger.error(f"Strategy not found: {strategy_name}")
            return None
        
        self.logger.info(f"Creating strategy: {strategy_name}")
        return self._strategies[strategy_name]
    
    def get_available_strategies(self) -> List[str]:
        """Get list of available strategy names."""
        return list(self._strategies.keys())
    
    def get_enabled_optimizations(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all enabled optimizations with their metadata.
        
        Returns:
            Dictionary of optimization name to metadata
        """
        result = {}
        for name, strategy in self._strategies.items():
            result[name] = {
                "display_name": self._get_display_name(name),
                "description": strategy.get_description(),
                "required_sheets": strategy.get_required_sheets(),
                "enabled": True,
                "metadata": {
                    "description": strategy.get_description()
                }
            }
        return result
    
    def get_display_name(self, strategy_name: str) -> str:
        """
        Get display name for a strategy.
        
        Args:
            strategy_name: Internal strategy name
            
        Returns:
            Human-readable display name
        """
        return self._get_display_name(strategy_name)
    
    def _get_display_name(self, strategy_name: str) -> str:
        """Convert strategy name to display name."""
        display_names = {
            "empty_portfolios": "Empty Portfolios",
            "campaigns_without_portfolios": "Campaigns w/o Portfolios"
        }
        return display_names.get(strategy_name, strategy_name.replace("_", " ").title())
    
    def get_ordered_strategies(self, selected_strategies: List[str]) -> List[str]:
        """
        Get strategies in the correct execution order.
        
        Args:
            selected_strategies: List of selected strategy names
            
        Returns:
            Ordered list of strategy names
        """
        # Sort by predefined order
        ordered = []
        for strategy in OPTIMIZATION_ORDER:
            if strategy in selected_strategies:
                ordered.append(strategy)
        
        # Add any strategies not in the predefined order
        for strategy in selected_strategies:
            if strategy not in ordered:
                ordered.append(strategy)
        
        return ordered


# Singleton instance
_factory_instance = None


def get_portfolio_optimization_factory() -> PortfolioOptimizationFactory:
    """Get the singleton factory instance."""
    global _factory_instance
    if _factory_instance is None:
        _factory_instance = PortfolioOptimizationFactory()
    return _factory_instance