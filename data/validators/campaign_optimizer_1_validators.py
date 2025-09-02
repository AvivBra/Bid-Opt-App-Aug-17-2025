"""Campaign Optimizer 1 validation logic."""

import pandas as pd
from io import BytesIO
from typing import List, NamedTuple
import logging

from config.campaign_optimizer_1_config import (
    REQUIRED_SHEETS, REQUIRED_COLUMNS, MAX_FILE_SIZE_MB, ERROR_MESSAGES
)

logger = logging.getLogger(__name__)


class ValidationResult(NamedTuple):
    """Validation result container."""
    is_valid: bool
    errors: List[str]
    warnings: List[str] = []


class CampaignOptimizer1Validator:
    """Validator for Campaign Optimizer 1 input files."""
    
    def validate_input_file(self, file_bytes: bytes) -> ValidationResult:
        """
        Validate uploaded Excel file for Campaign Optimizer 1 processing.
        
        Args:
            file_bytes: Raw file content
            
        Returns:
            ValidationResult with validation status and any errors
        """
        errors = []
        warnings = []
        
        try:
            # Check file size
            file_size_mb = len(file_bytes) / (1024 * 1024)
            if file_size_mb > MAX_FILE_SIZE_MB:
                errors.append(ERROR_MESSAGES["file_too_large"])
                return ValidationResult(False, errors, warnings)
            
            # Try to read as Excel
            try:
                excel_data = pd.read_excel(BytesIO(file_bytes), sheet_name=None)
            except Exception as e:
                errors.append(f"{ERROR_MESSAGES['invalid_format']}: {str(e)}")
                return ValidationResult(False, errors, warnings)
            
            # Validate required sheets
            missing_sheets = []
            for sheet_name in REQUIRED_SHEETS:
                if sheet_name not in excel_data:
                    missing_sheets.append(sheet_name)
            
            if missing_sheets:
                for sheet in missing_sheets:
                    errors.append(ERROR_MESSAGES["missing_sheet"].format(sheet))
                return ValidationResult(False, errors, warnings)
            
            # Validate columns in main sheet
            main_sheet = excel_data[REQUIRED_SHEETS[0]]  # "Sponsored Products Campaigns"
            missing_columns = []
            
            for col in REQUIRED_COLUMNS:
                if col not in main_sheet.columns:
                    missing_columns.append(col)
            
            if missing_columns:
                errors.append(ERROR_MESSAGES["missing_columns"].format(", ".join(missing_columns)))
                return ValidationResult(False, errors, warnings)
            
            # Check for campaign data
            campaign_rows = main_sheet[main_sheet["Entity"] == "Campaign"]
            if len(campaign_rows) == 0:
                errors.append(ERROR_MESSAGES["no_campaign_data"])
                return ValidationResult(False, errors, warnings)
            
            # Data quality warnings
            self._add_data_quality_warnings(main_sheet, warnings)
            
            logger.info(f"Validation passed. Found {len(campaign_rows)} campaign rows.")
            return ValidationResult(True, errors, warnings)
            
        except Exception as e:
            logger.error(f"Validation error: {e}")
            errors.append(f"Validation failed: {str(e)}")
            return ValidationResult(False, errors, warnings)
    
    def _add_data_quality_warnings(self, df: pd.DataFrame, warnings: List[str]):
        """Add data quality warnings to validation result."""
        
        # Check for missing ACOS values
        campaign_df = df[df["Entity"] == "Campaign"]
        missing_acos = campaign_df["ACOS"].isna().sum()
        if missing_acos > 0:
            warnings.append(f"Found {missing_acos} campaigns with missing ACOS values")
        
        # Check for missing Daily Budget values
        missing_budget = campaign_df["Daily Budget"].isna().sum()
        if missing_budget > 0:
            warnings.append(f"Found {missing_budget} campaigns with missing Daily Budget values")
        
        # Check for missing Units values
        missing_units = campaign_df["Units"].isna().sum()
        if missing_units > 0:
            warnings.append(f"Found {missing_units} campaigns with missing Units values")
    
    def validate_processing_result(self, processed_data: dict) -> ValidationResult:
        """
        Validate processing results before output generation.
        
        Args:
            processed_data: Dictionary of processed sheet data
            
        Returns:
            ValidationResult indicating if processing results are valid
        """
        errors = []
        warnings = []
        
        try:
            # Check required output sheets
            if "Campaign" not in processed_data:
                errors.append("Missing 'Campaign' sheet in processed data")
                return ValidationResult(False, errors, warnings)
            
            campaign_df = processed_data["Campaign"]
            
            # Check data integrity
            if len(campaign_df) == 0:
                errors.append("No campaign data in processed results")
                return ValidationResult(False, errors, warnings)
            
            # Check required columns exist
            output_required_cols = ["Units", "ACOS", "Daily Budget", "Operation"]
            missing_output_cols = []
            
            for col in output_required_cols:
                if col not in campaign_df.columns:
                    missing_output_cols.append(col)
            
            if missing_output_cols:
                errors.append(f"Missing output columns: {', '.join(missing_output_cols)}")
                return ValidationResult(False, errors, warnings)
            
            # Check if any optimizations were applied
            updated_campaigns = campaign_df["Operation"].notna().sum()
            if updated_campaigns == 0:
                warnings.append("No campaigns were updated during processing")
            
            logger.info(f"Processing validation passed. {updated_campaigns} campaigns updated.")
            return ValidationResult(True, errors, warnings)
            
        except Exception as e:
            logger.error(f"Processing validation error: {e}")
            errors.append(f"Processing validation failed: {str(e)}")
            return ValidationResult(False, errors, warnings)