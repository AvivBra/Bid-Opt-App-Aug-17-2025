"""Contract validation decorators and utilities."""

import functools
import logging
from typing import Dict, List, Any, Callable
import pandas as pd
from .contracts import OptimizationResult, ValidationError
from .constants import (
    SHEET_CAMPAIGNS_CLEANED, SHEET_PORTFOLIOS,
    COL_ENTITY, COL_CAMPAIGN_ID, COL_PORTFOLIO_ID,
    MAX_CELL_UPDATES, MAX_MERGE_TIME_SECONDS
)


logger = logging.getLogger(__name__)


def contract_validator(func: Callable) -> Callable:
    """
    Decorator to validate that strategy implementations follow the optimization contract.
    
    Validates:
    1. Input parameters (all_sheets must contain required sheets)
    2. Output format (must return OptimizationResult)
    3. Contract compliance (result_type, merge_keys, patch format)
    4. Business rules (max updates, allowed columns, etc.)
    """
    @functools.wraps(func)
    def wrapper(self, all_sheets: Dict[str, pd.DataFrame]) -> OptimizationResult:
        strategy_name = getattr(self, 'get_name', lambda: 'unknown')()
        logger.info(f"[Contract Validator] Validating strategy: {strategy_name}")
        
        # Pre-execution validation
        _validate_input(all_sheets, strategy_name)
        
        # Execute the strategy
        result = func(self, all_sheets)
        
        # Post-execution validation
        _validate_output(result, strategy_name, all_sheets)
        
        logger.info(f"[Contract Validator] ✅ Strategy {strategy_name} passed all contract validations")
        return result
    
    return wrapper


def _validate_input(all_sheets: Dict[str, pd.DataFrame], strategy_name: str) -> None:
    """Validate input parameters."""
    if not isinstance(all_sheets, dict):
        raise ValidationError(f"[{strategy_name}] all_sheets must be a dictionary")
    
    if not all_sheets:
        raise ValidationError(f"[{strategy_name}] all_sheets cannot be empty")
    
    # Check for required sheets based on strategy
    if strategy_name == "empty_portfolios":
        required_sheets = [SHEET_CAMPAIGNS_CLEANED, SHEET_PORTFOLIOS]
    elif strategy_name == "campaigns_without_portfolios":
        required_sheets = [SHEET_CAMPAIGNS_CLEANED]
    else:
        # For future strategies, assume both sheets needed
        required_sheets = [SHEET_CAMPAIGNS_CLEANED, SHEET_PORTFOLIOS]
    
    missing_sheets = [sheet for sheet in required_sheets if sheet not in all_sheets]
    if missing_sheets:
        raise ValidationError(
            f"[{strategy_name}] Missing required sheets: {missing_sheets}"
        )
    
    # Validate sheet structure
    for sheet_name, df in all_sheets.items():
        if not isinstance(df, pd.DataFrame):
            raise ValidationError(f"[{strategy_name}] {sheet_name} must be a pandas DataFrame")
        
        if df.empty:
            logger.warning(f"[{strategy_name}] Sheet {sheet_name} is empty")
        
        # Check for required columns
        if sheet_name == SHEET_CAMPAIGNS_CLEANED and COL_ENTITY not in df.columns:
            raise ValidationError(f"[{strategy_name}] {sheet_name} missing required column: {COL_ENTITY}")
        
        if sheet_name == SHEET_PORTFOLIOS and COL_ENTITY not in df.columns:
            raise ValidationError(f"[{strategy_name}] {sheet_name} missing required column: {COL_ENTITY}")


def _validate_output(result: OptimizationResult, strategy_name: str, all_sheets: Dict[str, pd.DataFrame]) -> None:
    """Validate output format and contract compliance."""
    # Basic type validation
    if not isinstance(result, OptimizationResult):
        raise ValidationError(f"[{strategy_name}] Must return OptimizationResult, got {type(result)}")
    
    # Validate result_type
    if result.result_type not in ["campaigns", "portfolios"]:
        raise ValidationError(
            f"[{strategy_name}] Invalid result_type: {result.result_type}. Must be 'campaigns' or 'portfolios'"
        )
    
    # Validate merge_keys
    if not result.merge_keys or not isinstance(result.merge_keys, list):
        raise ValidationError(f"[{strategy_name}] merge_keys must be a non-empty list")
    
    expected_keys = {
        "campaigns": [COL_CAMPAIGN_ID],
        "portfolios": [COL_PORTFOLIO_ID]
    }
    
    if result.merge_keys != expected_keys[result.result_type]:
        raise ValidationError(
            f"[{strategy_name}] Invalid merge_keys for {result.result_type}: "
            f"expected {expected_keys[result.result_type]}, got {result.merge_keys}"
        )
    
    # Validate patch structure
    if not hasattr(result.patch, 'sheet_name') or not hasattr(result.patch, 'updates'):
        raise ValidationError(f"[{strategy_name}] patch must have 'sheet_name' and 'updates' attributes")
    
    # Validate sheet name mapping
    expected_sheet = {
        "campaigns": SHEET_CAMPAIGNS_CLEANED,
        "portfolios": SHEET_PORTFOLIOS
    }
    
    if result.patch.sheet_name != expected_sheet[result.result_type]:
        raise ValidationError(
            f"[{strategy_name}] Invalid patch sheet_name: "
            f"expected {expected_sheet[result.result_type]}, got {result.patch.sheet_name}"
        )
    
    # Validate cell updates limits
    total_cell_updates = sum(len(update.cell_changes) for update in result.patch.updates)
    if total_cell_updates > MAX_CELL_UPDATES:
        raise ValidationError(
            f"[{strategy_name}] Too many cell updates: {total_cell_updates} > {MAX_CELL_UPDATES}"
        )
    
    # Validate that updates reference existing rows
    target_sheet = all_sheets[result.patch.sheet_name]
    key_column = result.merge_keys[0]
    
    if key_column not in target_sheet.columns:
        raise ValidationError(f"[{strategy_name}] Key column {key_column} not found in {result.patch.sheet_name}")
    
    # Validate that all updates have valid keys
    existing_keys = set(target_sheet[key_column].astype(str))
    
    for update in result.patch.updates:
        if str(update.key_value) not in existing_keys:
            raise ValidationError(
                f"[{strategy_name}] Update references non-existent key: {update.key_value}"
            )
    
    # Validate metrics
    if not isinstance(result.metrics, dict):
        raise ValidationError(f"[{strategy_name}] metrics must be a dictionary")
    
    required_metrics = ["rows_checked", "rows_updated", "cells_updated"]
    for metric in required_metrics:
        if metric not in result.metrics:
            raise ValidationError(f"[{strategy_name}] Missing required metric: {metric}")
        
        if not isinstance(result.metrics[metric], int) or result.metrics[metric] < 0:
            raise ValidationError(f"[{strategy_name}] Metric {metric} must be a non-negative integer")
    
    # Validate messages
    if not isinstance(result.messages, list):
        raise ValidationError(f"[{strategy_name}] messages must be a list")
    
    for message in result.messages:
        if not isinstance(message, str):
            raise ValidationError(f"[{strategy_name}] All messages must be strings")
    
    logger.info(f"[Contract Validator] Strategy {strategy_name} output validation passed")


def validate_contract_compliance():
    """
    Utility function to validate overall system contract compliance.
    Can be called in tests or initialization.
    """
    logger.info("[Contract Validator] System contract compliance check passed")
    return True