"""Template file validation utilities."""

import pandas as pd
from typing import Dict, List, Tuple, Optional


class TemplateValidator:
    """Validates template Excel files for bid optimization."""

    def __init__(self):
        """Initialize the validator."""
        self.required_sheets = ["Port Values"]  # Only Port Values is required
        self.optional_sheets = ["Top ASINs", "Delete for 60"]  # Top ASINs and Delete for 60 are optional
        self.required_port_columns = ["Portfolio Name", "Base Bid", "Target CPA"]
        self.required_delete_for_60_columns = ["Keyword ID", "Product Targeting ID"]
        self.errors = []

    def validate(
        self, excel_file
    ) -> Tuple[bool, str, Optional[Dict[str, pd.DataFrame]]]:
        """
        Validate template file structure with sheets.

        Args:
            excel_file: Excel file object or path

        Returns:
            Tuple of (is_valid, error_message, dataframes_dict)
        """
        self.errors = []

        try:
            # Read Excel file
            excel_data = pd.ExcelFile(excel_file)

            # Check required sheets exist
            sheet_names = excel_data.sheet_names
            missing_sheets = [s for s in self.required_sheets if s not in sheet_names]

            if missing_sheets:
                return (
                    False,
                    f"Missing required sheets: {', '.join(missing_sheets)}",
                    None,
                )

            # Read sheets (Top ASINs and Delete for 60 are optional)
            dataframes = {}

            # Validate Port Values sheet (required)
            port_values_df = pd.read_excel(excel_file, sheet_name="Port Values")
            valid, error = self._validate_port_values_columns(port_values_df)
            if not valid:
                return False, f"Port Values sheet error: {error}", None
            dataframes["Port Values"] = port_values_df

            # Check and validate Top ASINs sheet if exists (optional)
            if "Top ASINs" in sheet_names:
                top_asins_df = pd.read_excel(excel_file, sheet_name="Top ASINs")
                valid, error = self._validate_top_asins_columns(top_asins_df)
                if not valid:
                    return False, f"Top ASINs sheet error: {error}", None
                dataframes["Top ASINs"] = top_asins_df
            else:
                # Create empty DataFrame for Top ASINs if not present
                dataframes["Top ASINs"] = pd.DataFrame(columns=["ASIN"])

            # Check and validate Delete for 60 sheet if exists (optional)
            if "Delete for 60" in sheet_names:
                delete_for_60_df = pd.read_excel(excel_file, sheet_name="Delete for 60")
                valid, error = self._validate_delete_for_60_columns(delete_for_60_df)
                if not valid:
                    return False, f"Delete for 60 sheet error: {error}", None
                dataframes["Delete for 60"] = delete_for_60_df
            else:
                # Create empty DataFrame for Delete for 60 if not present
                dataframes["Delete for 60"] = pd.DataFrame(columns=["Keyword ID", "Product Targeting ID"])

            # Check for duplicate portfolios in Port Values
            duplicates = self._check_duplicate_portfolios(port_values_df)
            if duplicates:
                return (
                    False,
                    f"Duplicate portfolio names found: {', '.join(duplicates[:3])}",
                    None,
                )

            # Validate data values
            valid, error = self._validate_template_data(port_values_df)
            if not valid:
                return False, error, None

            return True, "Template is valid", dataframes

        except Exception as e:
            return False, f"Error reading template: {str(e)}", None

    def validate_structure(
        self, excel_file
    ) -> Tuple[bool, str, Optional[Dict[str, pd.DataFrame]]]:
        """Alias for validate method for backward compatibility."""
        return self.validate(excel_file)

    def _validate_port_values_columns(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """
        Validate Port Values sheet has required columns.

        Args:
            df: Port Values DataFrame

        Returns:
            Tuple of (is_valid, error_message)
        """
        if df.empty:
            return False, "Port Values sheet is empty"

        expected_cols = set(self.required_port_columns)
        actual_cols = set(df.columns)

        if not expected_cols.issubset(actual_cols):
            missing = expected_cols - actual_cols
            return False, f"Missing columns: {', '.join(missing)}"

        return True, ""

    def _validate_top_asins_columns(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """
        Validate Top ASINs sheet structure.

        Args:
            df: Top ASINs DataFrame

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Top ASINs is optional and can be empty for Phase 1
        if df.empty:
            return True, ""

        # If not empty, check for ASIN column
        if "ASIN" not in df.columns:
            return False, "Missing ASIN column"

        return True, ""

    def _validate_delete_for_60_columns(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """
        Validate Delete for 60 sheet has required columns.
        
        Args:
            df: Delete for 60 DataFrame
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if df.empty:
            return True, ""  # Empty sheet is valid for optional sheet
            
        expected_cols = set(self.required_delete_for_60_columns)
        actual_cols = set(df.columns)
        
        if not expected_cols.issubset(actual_cols):
            missing = expected_cols - actual_cols
            return False, f"Missing columns: {', '.join(missing)}"
            
        return True, ""

    def _check_duplicate_portfolios(self, df: pd.DataFrame) -> List[str]:
        """
        Check for duplicate portfolio names.

        Args:
            df: Port Values DataFrame

        Returns:
            List of duplicate portfolio names
        """
        if "Portfolio Name" not in df.columns:
            return []

        portfolio_names = df["Portfolio Name"].dropna()
        duplicates = portfolio_names[portfolio_names.duplicated()].unique().tolist()

        return duplicates

    def _validate_base_bid_values(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """
        Validate Base Bid values are in valid range or 'Ignore'.

        Args:
            df: Port Values DataFrame

        Returns:
            Tuple of (is_valid, error_message)
        """
        if "Base Bid" not in df.columns:
            return True, ""  # Column is required but checked elsewhere

        for idx, value in df["Base Bid"].items():
            if pd.isna(value):
                return False, f"Row {idx + 2}: Base Bid cannot be empty"

            # Check if it's 'Ignore' (case insensitive)
            if str(value).lower() == "ignore":
                continue

            # Try to convert to float and check range
            try:
                bid_value = float(value)
                if bid_value < 0.02 or bid_value > 4.00:
                    return (
                        False,
                        f"Row {idx + 2}: Base Bid must be between 0.02 and 4.00",
                    )
            except (ValueError, TypeError):
                return (
                    False,
                    f"Row {idx + 2}: Base Bid must be a number or 'Ignore'",
                )

        return True, ""

    def _validate_target_cpa_values(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """
        Validate Target CPA values (can be empty or numeric).

        Args:
            df: Port Values DataFrame

        Returns:
            Tuple of (is_valid, error_message)
        """
        if "Target CPA" not in df.columns:
            return True, ""  # Column is required but checked elsewhere

        for idx, value in df["Target CPA"].items():
            # Target CPA can be empty
            if pd.isna(value) or str(value).strip() == "":
                continue

            # Try to convert to float and check range
            try:
                cpa_value = float(value)
                if cpa_value < 0.01:
                    return (
                        False,
                        f"Row {idx + 2}: Target CPA must be at least 0.01",
                    )
                if cpa_value > 9999.99:
                    return (
                        False,
                        f"Row {idx + 2}: Target CPA must be less than 10000",
                    )
            except (ValueError, TypeError):
                return False, f"Row {idx + 2}: Target CPA must be a number or empty"

        return True, ""

    def _validate_template_data(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """
        Validate all data values in template.

        Args:
            df: Port Values DataFrame

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate Base Bid
        valid, error = self._validate_base_bid_values(df)
        if not valid:
            return False, error

        # Validate Target CPA
        valid, error = self._validate_target_cpa_values(df)
        if not valid:
            return False, error

        # Check at least one non-ignored portfolio
        if "Base Bid" in df.columns:
            non_ignored = df[df["Base Bid"].astype(str).str.lower() != "ignore"]
            if non_ignored.empty:
                return False, "All portfolios are set to 'Ignore'"

        return True, ""

    def get_errors(self) -> List[str]:
        """Get list of validation errors."""
        return self.errors


# Backward compatibility - keep the standalone functions as well
def validate_template_structure(
    excel_file,
) -> Tuple[bool, str, Optional[Dict[str, pd.DataFrame]]]:
    """Validate template file structure with two sheets."""
    validator = TemplateValidator()
    return validator.validate(excel_file)


def check_required_sheets(sheet_names: List[str]) -> Tuple[bool, List[str]]:
    """Check if required sheets exist."""
    required = ["Port Values", "Top ASINs"]
    missing = [s for s in required if s not in sheet_names]
    return len(missing) == 0, missing


def validate_port_values_columns(df: pd.DataFrame) -> Tuple[bool, str]:
    """Validate Port Values sheet has required columns."""
    validator = TemplateValidator()
    return validator._validate_port_values_columns(df)


def validate_top_asins_columns(df: pd.DataFrame) -> Tuple[bool, str]:
    """Validate Top ASINs sheet structure."""
    validator = TemplateValidator()
    return validator._validate_top_asins_columns(df)


def check_duplicate_portfolios(df: pd.DataFrame) -> List[str]:
    """Check for duplicate portfolio names."""
    validator = TemplateValidator()
    return validator._check_duplicate_portfolios(df)


def validate_base_bid_values(df: pd.DataFrame) -> Tuple[bool, str]:
    """Validate Base Bid values are in valid range or 'Ignore'."""
    validator = TemplateValidator()
    return validator._validate_base_bid_values(df)


def validate_target_cpa_values(df: pd.DataFrame) -> Tuple[bool, str]:
    """Validate Target CPA values (can be empty or numeric)."""
    validator = TemplateValidator()
    return validator._validate_target_cpa_values(df)


def validate_template_data(df: pd.DataFrame) -> Tuple[bool, str]:
    """Validate all data values in template."""
    validator = TemplateValidator()
    return validator._validate_template_data(df)