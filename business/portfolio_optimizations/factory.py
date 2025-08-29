"""Factory for Portfolio Optimization discovery and instantiation."""

import importlib
import pkgutil
from typing import Dict, List, Type, Optional, Any
import logging
from pathlib import Path

from .portfolio_base_optimization import PortfolioBaseOptimization


class PortfolioOptimizationFactory:
    """
    Factory class for discovering and instantiating portfolio optimizations.
    
    Automatically discovers optimization modules and provides a unified interface
    for creating optimization instances.
    """
    
    def __init__(self):
        self.logger = logging.getLogger("portfolio_optimization.factory")
        self._optimization_registry: Dict[str, Dict[str, Any]] = {}
        self._discover_optimizations()
    
    def _discover_optimizations(self) -> None:
        """
        Automatically discover all available optimization modules.
        
        Looks for orchestrator.py files in subdirectories and registers them.
        """
        try:
            base_path = Path(__file__).parent
            self.logger.debug(f"Scanning for optimizations in: {base_path}")
            
            # Scan each subdirectory for orchestrator modules
            for item in base_path.iterdir():
                if item.is_dir() and not item.name.startswith('__'):
                    orchestrator_file = item / "orchestrator.py"
                    constants_file = item / "constants.py"
                    
                    if orchestrator_file.exists():
                        optimization_name = item.name
                        self.logger.debug(f"Found optimization: {optimization_name}")
                        
                        # Try to register this optimization
                        self._register_optimization(optimization_name, item)
        
        except Exception as e:
            self.logger.error(f"Error discovering optimizations: {str(e)}")
    
    def _register_optimization(self, optimization_name: str, optimization_path: Path) -> None:
        """
        Register a discovered optimization.
        
        Args:
            optimization_name: Name of the optimization (folder name)
            optimization_path: Path to the optimization folder
        """
        try:
            # Import the orchestrator module
            module_path = f"business.portfolio_optimizations.{optimization_name}.orchestrator"
            orchestrator_module = importlib.import_module(module_path)
            
            # Find the orchestrator class (should end with 'Orchestrator')
            orchestrator_class = None
            for attr_name in dir(orchestrator_module):
                attr = getattr(orchestrator_module, attr_name)
                if (isinstance(attr, type) and 
                    attr_name.endswith('Orchestrator') and 
                    attr_name != 'PortfolioBaseOptimization'):
                    orchestrator_class = attr
                    break
            
            if orchestrator_class:
                # Try to import constants for metadata
                try:
                    constants_module_path = f"business.portfolio_optimizations.{optimization_name}.constants"
                    constants_module = importlib.import_module(constants_module_path)
                    
                    # Extract metadata from constants
                    metadata = {
                        "success_messages": getattr(constants_module, 'SUCCESS_MESSAGES', {}),
                        "error_messages": getattr(constants_module, 'ERROR_MESSAGES', {}),
                        "required_columns": getattr(constants_module, 'REQUIRED_COLUMNS', []),
                        "target_entity": getattr(constants_module, 'TARGET_ENTITY', None),
                        "highlight_color": getattr(constants_module, 'HIGHLIGHT_COLOR', None),
                    }
                except ImportError:
                    metadata = {}
                
                # Enhance metadata with configuration information
                try:
                    from config.portfolio_config import get_optimization_config
                    config_metadata = get_optimization_config(optimization_name)
                    metadata.update(config_metadata)
                except ImportError:
                    pass  # Config not available, use default metadata
                
                # Register the optimization
                self._optimization_registry[optimization_name] = {
                    "name": optimization_name,
                    "display_name": self._format_display_name(optimization_name),
                    "orchestrator_class": orchestrator_class,
                    "module_path": module_path,
                    "metadata": metadata,
                    "enabled": metadata.get("enabled", True),
                    "category": metadata.get("category", "general"),
                    "result_type": metadata.get("result_type", "unknown"),
                    "help_text": metadata.get("help_text", metadata.get("description", "No description available"))
                }
                
                self.logger.info(f"Registered optimization: {optimization_name}")
            else:
                self.logger.warning(f"No orchestrator class found in {module_path}")
                
        except ImportError as e:
            self.logger.warning(f"Could not import {optimization_name}: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error registering {optimization_name}: {str(e)}")
    
    def _format_display_name(self, optimization_name: str) -> str:
        """
        Convert optimization folder name to user-friendly display name.
        
        Uses configuration registry for consistent naming.
        
        Args:
            optimization_name: Folder name (e.g., "campaigns_without_portfolios")
            
        Returns:
            Display name (e.g., "Campaigns w/o Portfolios")
        """
        try:
            from config.portfolio_config import get_optimization_display_name
            return get_optimization_display_name(optimization_name)
        except ImportError:
            # Fallback to manual mapping if config not available
            name_mappings = {
                "campaigns_without_portfolios": "Campaigns w/o Portfolios",
                "empty_portfolios": "Empty Portfolios"
            }
            
            if optimization_name in name_mappings:
                return name_mappings[optimization_name]
            
            # Default: Replace underscores with spaces and title case
            return optimization_name.replace('_', ' ').title()
    
    def get_available_optimizations(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all available optimizations.
        
        Returns:
            Dictionary with optimization info keyed by optimization name
        """
        return self._optimization_registry.copy()
    
    def get_enabled_optimizations(self) -> Dict[str, Dict[str, Any]]:
        """
        Get only enabled optimizations.
        
        Returns:
            Dictionary with enabled optimization info
        """
        return {
            name: info for name, info in self._optimization_registry.items() 
            if info.get("enabled", True)
        }
    
    def create_optimization(self, optimization_name: str) -> Optional[Any]:
        """
        Create an instance of the specified optimization.
        
        Args:
            optimization_name: Name of the optimization to create
            
        Returns:
            Orchestrator instance or None if not found
        """
        if optimization_name not in self._optimization_registry:
            self.logger.error(f"Optimization not found: {optimization_name}")
            return None
        
        try:
            orchestrator_class = self._optimization_registry[optimization_name]["orchestrator_class"]
            instance = orchestrator_class()
            
            self.logger.debug(f"Created optimization instance: {optimization_name}")
            return instance
            
        except Exception as e:
            self.logger.error(f"Error creating {optimization_name}: {str(e)}")
            return None
    
    def is_optimization_available(self, optimization_name: str) -> bool:
        """
        Check if an optimization is available and enabled.
        
        Args:
            optimization_name: Name of the optimization
            
        Returns:
            True if available and enabled
        """
        return (optimization_name in self._optimization_registry and 
                self._optimization_registry[optimization_name].get("enabled", True))
    
    def get_optimization_metadata(self, optimization_name: str) -> Dict[str, Any]:
        """
        Get metadata for a specific optimization.
        
        Args:
            optimization_name: Name of the optimization
            
        Returns:
            Metadata dictionary
        """
        if optimization_name not in self._optimization_registry:
            return {}
        
        return self._optimization_registry[optimization_name].get("metadata", {})
    
    def get_display_name(self, optimization_name: str) -> str:
        """
        Get the display name for an optimization.
        
        Args:
            optimization_name: Internal optimization name
            
        Returns:
            User-friendly display name
        """
        if optimization_name not in self._optimization_registry:
            return optimization_name
        
        return self._optimization_registry[optimization_name].get("display_name", optimization_name)


# Global factory instance
_factory_instance = None

def get_portfolio_optimization_factory() -> PortfolioOptimizationFactory:
    """
    Get the global portfolio optimization factory instance.
    
    Returns:
        PortfolioOptimizationFactory instance
    """
    global _factory_instance
    if _factory_instance is None:
        _factory_instance = PortfolioOptimizationFactory()
    return _factory_instance