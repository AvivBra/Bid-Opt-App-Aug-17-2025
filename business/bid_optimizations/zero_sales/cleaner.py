"""Zero Sales optimization data cleaning."""

import pandas as pd
from typing import Dict, Any, Tuple, List
import logging
from business.common.portfolio_filter import PortfolioFilter


class ZeroSalesCleaner:
    """Cleans data for Zero Sales optimization processing."""

    def __init__(self):
        self.logger = logging.getLogger("optimization.zero_sales.cleaner")
        self.portfolio_filter = PortfolioFilter()

    def clean(
        self,
        template_data: Dict[str, pd.DataFrame],
        bulk_data: pd.DataFrame,
        column_mapping: Dict[str, str],
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Clean and filter data for Zero Sales processing.

        Args:
            template_data: Template data dictionary
            bulk_data: Raw bulk data DataFrame
            column_mapping: Column name mappings

        Returns:
            Tuple of (cleaned_dataframe, cleaning_details)
        """

        cleaning_details = {
            "original_rows": len(bulk_data),
            "final_rows": 0,
            "cleaning_steps": [],
            "filter_details": {},
            "data_quality": {},
            "warnings": [],
        }

        self.logger.info(f"Starting Zero Sales data cleaning: {len(bulk_data)} rows")

        # Step 1: Basic data cleaning
        current_df, basic_details = self._basic_data_cleaning(bulk_data, column_mapping)
        cleaning_details["cleaning_steps"].append(("basic_cleaning", basic_details))

        # Step 2: Apply portfolio filters - FIXED: using correct column name
        portfolio_col = column_mapping.get(
            "portfolio", "Portfolio Name (Informational only)"
        )
        units_col = column_mapping.get("units")

        if portfolio_col and units_col:
            current_df, filter_details = self.portfolio_filter.apply_all_filters(
                current_df, portfolio_col, units_col, template_data
            )
            cleaning_details["filter_details"] = filter_details
            cleaning_details["cleaning_steps"].append(
                ("portfolio_filtering", filter_details)
            )

        # Step 3: Data quality checks
        quality_details = self._perform_quality_checks(current_df, column_mapping)
        cleaning_details["data_quality"] = quality_details
        cleaning_details["cleaning_steps"].append(("quality_checks", quality_details))

        # Step 4: Final data preparation
        current_df, prep_details = self._prepare_for_processing(
            current_df, column_mapping, template_data
        )
        cleaning_details["cleaning_steps"].append(("data_preparation", prep_details))

        # Final statistics
        cleaning_details["final_rows"] = len(current_df)

        success_msg = f"Data cleaning complete: {cleaning_details['original_rows']} -> {cleaning_details['final_rows']} rows"
        self.logger.info(success_msg)

        return current_df, cleaning_details

    def _basic_data_cleaning(
        self, df: pd.DataFrame, column_mapping: Dict[str, str]
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Perform basic data cleaning operations."""

        details = {
            "initial_rows": len(df),
            "empty_rows_removed": 0,
            "duplicate_rows_removed": 0,
            "invalid_values_fixed": 0,
        }

        # Make a copy to avoid modifying original
        cleaned_df = df.copy()

        # Remove completely empty rows
        before = len(cleaned_df)
        cleaned_df = cleaned_df.dropna(how="all")
        details["empty_rows_removed"] = before - len(cleaned_df)

        # Remove duplicate rows
        before = len(cleaned_df)
        cleaned_df = cleaned_df.drop_duplicates()
        details["duplicate_rows_removed"] = before - len(cleaned_df)

        # Clean numeric columns
        numeric_columns = ["units", "clicks", "impressions", "spend", "sales", "orders"]
        for col_type in numeric_columns:
            if col_type in column_mapping:
                col_name = column_mapping[col_type]
                if col_name in cleaned_df.columns:
                    # Convert to numeric, invalid values become NaN
                    cleaned_df[col_name] = pd.to_numeric(
                        cleaned_df[col_name], errors="coerce"
                    )
                    # Fill NaN with 0 for numeric columns
                    cleaned_df[col_name] = cleaned_df[col_name].fillna(0)
                    details["invalid_values_fixed"] += cleaned_df[col_name].isna().sum()

        # FIXED: Clean portfolio names using exact column name
        portfolio_col = column_mapping.get(
            "portfolio", "Portfolio Name (Informational only)"
        )
        if portfolio_col in cleaned_df.columns:
            cleaned_df[portfolio_col] = (
                cleaned_df[portfolio_col].astype(str).str.strip()
            )
            # Remove rows with invalid portfolio names
            cleaned_df = cleaned_df[
                ~cleaned_df[portfolio_col].isin(["nan", "", "None"])
            ]

        details["final_rows"] = len(cleaned_df)

        return cleaned_df, details

    def _perform_quality_checks(
        self, df: pd.DataFrame, column_mapping: Dict[str, str]
    ) -> Dict[str, Any]:
        """Perform data quality checks."""

        quality = {
            "completeness": {},
            "validity": {},
            "consistency": {},
            "overall_score": 0,
        }

        if df.empty:
            return quality

        # Check completeness for critical columns
        critical_columns = ["portfolio", "units", "bid", "campaign", "entity"]
        completeness_scores = []

        for col_type in critical_columns:
            if col_type in column_mapping:
                col_name = column_mapping[col_type]
                if col_name in df.columns:
                    non_null_pct = df[col_name].notna().mean()
                    quality["completeness"][col_type] = non_null_pct
                    completeness_scores.append(non_null_pct)

        # Check validity
        if "bid" in column_mapping:
            bid_col = column_mapping["bid"]
            if bid_col in df.columns:
                valid_bids = df[bid_col].between(0.02, 4.0, inclusive="both")
                quality["validity"]["bid_range"] = valid_bids.mean()

        # Check consistency - FIXED: using correct column name
        portfolio_col = column_mapping.get(
            "portfolio", "Portfolio Name (Informational only)"
        )
        if portfolio_col in df.columns:
            unique_portfolios = df[portfolio_col].nunique()
            quality["consistency"]["unique_portfolios"] = unique_portfolios

        # Calculate overall score
        if completeness_scores:
            quality["overall_score"] = sum(completeness_scores) / len(
                completeness_scores
            )

        return quality

    def _prepare_for_processing(
        self,
        df: pd.DataFrame,
        column_mapping: Dict[str, str],
        template_data: Dict[str, pd.DataFrame],
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Prepare data for processing by adding necessary columns."""

        details = {"columns_added": [], "template_mappings": 0, "rows_prepared": 0}

        if df.empty:
            return df, details

        prepared_df = df.copy()

        # Add template data mapping - FIXED: using correct column name
        portfolio_col = column_mapping.get(
            "portfolio", "Portfolio Name (Informational only)"
        )
        if portfolio_col in prepared_df.columns and "Port Values" in template_data:
            port_values = template_data["Port Values"]

            # Create mapping dictionaries
            base_bid_map = dict(
                zip(port_values["Portfolio Name"], port_values["Base Bid"])
            )
            target_cpa_map = dict(
                zip(port_values["Portfolio Name"], port_values["Target CPA"])
            )

            # Map values
            prepared_df["Template_Base_Bid"] = prepared_df[portfolio_col].map(
                base_bid_map
            )
            prepared_df["Template_Target_CPA"] = prepared_df[portfolio_col].map(
                target_cpa_map
            )

            details["columns_added"] = ["Template_Base_Bid", "Template_Target_CPA"]
            details["template_mappings"] = (
                prepared_df["Template_Base_Bid"].notna().sum()
            )

        # Ensure Entity column exists for split
        if "entity" in column_mapping:
            entity_col = column_mapping["entity"]
            if entity_col not in prepared_df.columns:
                prepared_df["Entity"] = "Unknown"
                details["columns_added"].append("Entity")

        details["rows_prepared"] = len(prepared_df)

        return prepared_df, details

    def get_cleaning_summary(self, cleaning_details: Dict[str, Any]) -> str:
        """Generate a human-readable cleaning summary."""

        summary_lines = [
            f"Data Cleaning Summary:",
            f"Original rows: {cleaning_details.get('original_rows', 0)}",
            f"Final rows: {cleaning_details.get('final_rows', 0)}",
        ]

        # Add step details
        for step_name, step_details in cleaning_details.get("cleaning_steps", []):
            if step_name == "basic_cleaning":
                if step_details.get("empty_rows_removed", 0) > 0:
                    summary_lines.append(
                        f"• Removed {step_details['empty_rows_removed']} empty rows"
                    )
                if step_details.get("duplicate_rows_removed", 0) > 0:
                    summary_lines.append(
                        f"• Removed {step_details['duplicate_rows_removed']} duplicate rows"
                    )

            elif step_name == "portfolio_filtering":
                filtered = step_details.get("total_filtered", 0)
                if filtered > 0:
                    summary_lines.append(
                        f"• Filtered {filtered} rows (excluded/ignored portfolios + non-zero sales)"
                    )

        # Add quality score
        quality_score = cleaning_details.get("data_quality", {}).get("overall_score", 0)
        if quality_score > 0:
            summary_lines.append(f"• Data quality score: {quality_score:.1%}")

        return "\n".join(summary_lines)
