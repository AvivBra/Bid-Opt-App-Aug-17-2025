"""Contracts for Portfolio Optimizations module."""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Literal
import pandas as pd


@dataclass
class CellUpdate:
    """Represents a single cell update."""
    row_index: int
    key_column: str
    key_value: str
    cell_changes: Dict[str, Any]


@dataclass
class PatchData:
    """Represents updates for a single sheet."""
    sheet_name: str
    updates: List[CellUpdate]


@dataclass
class OptimizationResult:
    """Result from a single optimization strategy."""
    result_type: Literal["campaigns", "portfolios"]
    merge_keys: List[str]
    patch: PatchData
    metrics: Dict[str, int] = field(default_factory=dict)
    messages: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize default values."""
        if not self.metrics:
            self.metrics = {
                "rows_checked": 0,
                "rows_updated": 0,
                "cells_updated": 0
            }
        if not self.messages:
            self.messages = []


@dataclass
class MergeConflict:
    """Represents a merge conflict."""
    sheet_name: str
    row_index: int
    column_name: str
    first_value: Any
    second_value: Any
    resolution: str = "last_wins"


@dataclass
class RunReport:
    """Report of the entire optimization run."""
    total_optimizations: int
    successful_optimizations: int
    failed_optimizations: List[str]
    total_rows_updated: int
    total_cells_updated: int
    conflicts: List[MergeConflict]
    execution_time_seconds: float
    optimization_details: Dict[str, Dict[str, Any]]


class OptimizationStrategy:
    """Base contract for all optimization strategies."""
    
    def run(self, all_sheets: Dict[str, pd.DataFrame]) -> OptimizationResult:
        """
        Run the optimization on the provided data.
        
        Args:
            all_sheets: Dictionary of sheet name to DataFrame
            
        Returns:
            OptimizationResult with patches to apply
        """
        raise NotImplementedError("Each strategy must implement run()")
    
    def get_name(self) -> str:
        """Get the name of this optimization."""
        raise NotImplementedError("Each strategy must implement get_name()")
    
    def get_description(self) -> str:
        """Get a description of what this optimization does."""
        raise NotImplementedError("Each strategy must implement get_description()")
    
    def get_required_sheets(self) -> List[str]:
        """Get list of required sheet names."""
        raise NotImplementedError("Each strategy must implement get_required_sheets()")


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


class MergeError(Exception):
    """Raised when merge fails."""
    pass


class OptimizationError(Exception):
    """Raised when optimization fails."""
    pass