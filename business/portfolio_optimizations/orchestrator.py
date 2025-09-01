"""Orchestrator for portfolio optimizations."""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import logging
import time
from .factory import get_portfolio_optimization_factory
from .results_manager import ResultsManager
from .service import PortfolioOptimizationService
from .contracts import OptimizationResult, RunReport, ValidationError, OptimizationError
from .constants import (
    SHEET_CAMPAIGNS, SHEET_PORTFOLIOS, SHEET_CAMPAIGNS_CLEANED,
    COL_ENTITY, COL_CAMPAIGN_ID, COL_PORTFOLIO_ID,
    SUCCESS_MESSAGES, ERROR_MESSAGES, REQUIRED_SHEETS_AFTER_CLEANING
)
from .cleaning import clean_data_structure, validate_cleaned_structure


class PortfolioOptimizationOrchestrator:
    """Orchestrates the portfolio optimization process."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.factory = get_portfolio_optimization_factory()
        self.results_manager = ResultsManager()
        self.service = PortfolioOptimizationService()
    
    def run_optimizations(
        self,
        all_sheets: Dict[str, pd.DataFrame],
        selected_optimizations: List[str]
    ) -> Tuple[Dict[str, pd.DataFrame], RunReport]:
        """
        Run selected optimizations on the data.
        
        Args:
            all_sheets: Dictionary of sheet name to DataFrame
            selected_optimizations: List of optimization names to run
            
        Returns:
            Tuple of (merged data, run report)
        """
        start_time = time.time()
        self.logger.info(f"Starting optimizations: {selected_optimizations}")
        
        try:
            # Step 1: Validate and clean data
            cleaned_sheets = self._validate_and_clean(all_sheets)
            
            # Step 2: Get ordered strategies
            ordered_strategies = self.factory.get_ordered_strategies(selected_optimizations)
            
            # Step 3: Run each strategy
            optimization_results = []
            failed_optimizations = []
            optimization_details = {}
            
            for strategy_name in ordered_strategies:
                try:
                    result = self._run_single_optimization(strategy_name, cleaned_sheets)
                    if result:
                        optimization_results.append(result)
                        optimization_details[strategy_name] = {
                            "status": "success",
                            "metrics": result.metrics,
                            "messages": result.messages
                        }
                except Exception as e:
                    self.logger.error(f"Optimization {strategy_name} failed: {str(e)}")
                    failed_optimizations.append(strategy_name)
                    optimization_details[strategy_name] = {
                        "status": "failed",
                        "error": str(e)
                    }
            
            # Step 4: Merge results
            merged_data, merge_report = self.results_manager.merge_all(
                cleaned_sheets,
                optimization_results
            )
            
            # Step 5: Create run report with enhanced conflict information
            execution_time = time.time() - start_time
            conflict_summary = self.results_manager.get_conflict_summary()
            
            run_report = RunReport(
                total_optimizations=len(ordered_strategies),
                successful_optimizations=len(optimization_results),
                failed_optimizations=failed_optimizations,
                total_rows_updated=merge_report["total_rows_updated"],
                total_cells_updated=merge_report["total_cells_updated"],
                conflicts=merge_report["conflicts"],
                execution_time_seconds=execution_time,
                optimization_details=optimization_details
            )
            
            # Add conflict summary for UI display
            run_report.conflict_summary = conflict_summary
            
            self.logger.info(f"Optimizations complete in {execution_time:.2f} seconds")
            return merged_data, run_report
            
        except Exception as e:
            self.logger.error(f"Orchestration failed: {str(e)}")
            raise OptimizationError(f"Orchestration failed: {str(e)}")
    
    def _validate_and_clean(self, all_sheets: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """
        Validate and clean the input data.
        
        Args:
            all_sheets: Raw input data
            
        Returns:
            Cleaned and restructured data
        """
        self.logger.info("Validating and cleaning data")
        
        # Step 1: Initial validation - check original required sheets exist
        required_sheets = [SHEET_CAMPAIGNS, SHEET_PORTFOLIOS]
        for sheet in required_sheets:
            if sheet not in all_sheets:
                raise ValidationError(ERROR_MESSAGES["missing_sheet"].format(sheet))
        
        # Step 2: Clean data content (remove extra spaces, convert types)
        content_cleaned = self._clean_data_content(all_sheets)
        
        # Step 3: Restructure data according to preprocessing logic
        structure_cleaned = clean_data_structure(content_cleaned)
        
        # Step 4: Validate cleaned structure
        validate_cleaned_structure(structure_cleaned)
        
        self.logger.info(SUCCESS_MESSAGES["structure_cleaning_complete"])
        return structure_cleaned
    
    def _clean_data_content(self, all_sheets: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """
        Clean data content (spaces, types) without changing structure.
        
        Args:
            all_sheets: Input data
            
        Returns:
            Content-cleaned data
        """
        cleaned = {}
        for sheet_name, df in all_sheets.items():
            cleaned_df = df.copy()
            
            # Clean string columns
            for col in cleaned_df.columns:
                if cleaned_df[col].dtype == 'object':
                    cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
                    cleaned_df[col] = cleaned_df[col].replace('nan', '')
            
            cleaned[sheet_name] = cleaned_df
        
        self.logger.info(SUCCESS_MESSAGES["cleaning_complete"])
        return cleaned
    
    def _run_single_optimization(
        self,
        strategy_name: str,
        data: Dict[str, pd.DataFrame]
    ) -> Optional[OptimizationResult]:
        """
        Run a single optimization strategy.
        
        Args:
            strategy_name: Name of the strategy
            data: Input data
            
        Returns:
            Optimization result or None if failed
        """
        self.logger.info(f"Running optimization: {strategy_name}")
        
        # Create strategy
        strategy = self.factory.create_strategy(strategy_name)
        if not strategy:
            raise OptimizationError(f"Strategy not found: {strategy_name}")
        
        # Run strategy
        result = strategy.run(data)
        
        self.logger.info(f"Optimization {strategy_name} complete: {result.metrics}")
        return result
    
    def create_output_file(
        self,
        merged_data: Dict[str, pd.DataFrame],
        updated_indices: Dict[str, List[int]]
    ) -> bytes:
        """
        Create the output Excel file.
        
        Args:
            merged_data: Merged data with all updates
            updated_indices: Dictionary of sheet name to list of updated row indices
            
        Returns:
            Bytes of the Excel file
        """
        return self.service.create_output_file(merged_data, updated_indices)