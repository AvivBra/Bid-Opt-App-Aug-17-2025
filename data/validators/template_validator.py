"""Template file validation with TemplateValidator class."""

import pandas as pd
from typing import Dict, List, Tuple, Optional


class TemplateValidator:
    """Validator for template Excel files."""

    def __init__(self):
        """Initialize the validator."""
        self.required_sheets = ["Port Values"]  # Only Port Values is required
        self.optional_sheets = ["Top ASINs"]  # Top ASINs is optional
        self.required_port_columns = ["Portfolio Name", "Base Bid", "Target CPA"]
        self.errors = []

    def validate(
        self, excel_file
    ) -> Tuple[bool, str, Optional[Dict[str, pd.DataFrame]]]:
        """
        Validate template file structure with two sheets.

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

            # Read both sheets (Top ASINs is optional)
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

    def validate_complete(
        self, excel_file
    ) -> Tuple[bool, str, Optional[Dict[str, pd.DataFrame]]]:
        """Complete validation of template file (alias for validate)."""
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

        missing_columns = [
            col for col in self.required_port_columns if col not in df.columns
        ]

        if missing_columns:
            return False, f"Missing columns: {', '.join(missing_columns)}"

        return True, ""

    def _validate_top_asins_columns(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """
        Validate Top ASINs sheet structure.

        Args:
            df: Top ASINs DataFrame

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Top ASINs can be empty (optional for Zero Sales)
        if df.empty:
            return True, ""

        # If not empty, should have ASIN column
        if "ASIN" not in df.columns:
            return False, "Missing 'ASIN' column"

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

        portfolio_counts = df["Portfolio Name"].value_counts()
        duplicates = portfolio_counts[portfolio_counts > 1].index.tolist()

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
            return False, "Base Bid column missing"

        invalid_rows = []

        for idx, value in df["Base Bid"].items():
            if pd.isna(value):
                invalid_rows.append(idx + 1)  # Row number (1-based)
                continue

            # Convert to string for 'Ignore' check
            str_value = str(value).strip().lower()

            if str_value == "ignore":
                continue

            # Try to convert to float for range check
            try:
                num_value = float(value)
                if num_value < 0 or num_value > 4:
                    invalid_rows.append(idx + 1)
            except (ValueError, TypeError):
                invalid_rows.append(idx + 1)

        if invalid_rows:
            return False, f"Invalid Base Bid values in rows: {invalid_rows[:5]}"

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
            return False, "Target CPA column missing"

        invalid_rows = []

        for idx, value in df["Target CPA"].items():
            # Empty/NaN is allowed
            if pd.isna(value) or value == "":
                continue

            # Must be numeric and positive
            try:
                num_value = float(value)
                if num_value < 0:
                    invalid_rows.append(idx + 1)
            except (ValueError, TypeError):
                invalid_rows.append(idx + 1)

        if invalid_rows:
            return False, f"Invalid Target CPA values in rows: {invalid_rows[:5]}"

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
