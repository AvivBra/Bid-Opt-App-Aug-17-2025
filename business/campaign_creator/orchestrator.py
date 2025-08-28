"""Orchestrator for Campaign Creator module."""

import pandas as pd
from typing import Dict, List, Optional, Tuple
from io import BytesIO
import logging

from .processors import get_processor
from .validators import get_validator
from .builder import CampaignBuilder
from .formatter import CampaignFormatter
from .session_builder import SessionBuilder
from .validation import CampaignValidation
from data.writers.campaign_bulk_writer import CampaignBulkWriter


class CampaignCreatorOrchestrator:
    """Orchestrates the campaign creation process."""

    def __init__(self):
        """Initialize orchestrator."""
        self.logger = logging.getLogger(__name__)
        self.session_builder = SessionBuilder()
        self.validation = CampaignValidation()
        self.builder = CampaignBuilder()
        self.formatter = CampaignFormatter()
        self.bulk_writer = CampaignBulkWriter()

    def process_campaign(
        self,
        campaign_type: str,
        template_df: pd.DataFrame,
        session_table: pd.DataFrame,
        data_rova_df: Optional[pd.DataFrame] = None,
    ) -> Tuple[bool, Optional[BytesIO], Optional[str]]:
        """Process a single campaign type.
        
        Args:
            campaign_type: Type of campaign (e.g., 'halloween_testing')
            template_df: Template dataframe
            session_table: Session table with all data
            data_rova_df: Optional Data Rova dataframe
            
        Returns:
            Tuple of (success, output_file, error_message)
        """
        try:
            # Get validator for campaign type
            validator = get_validator(campaign_type)
            if not validator:
                return False, None, f"No validator found for {campaign_type}"

            # Validate campaign data
            is_valid, error = validator.validate(template_df, session_table, data_rova_df)
            if not is_valid:
                return False, None, error

            # Get processor for campaign type
            processor = get_processor(campaign_type)
            if not processor:
                return False, None, f"No processor found for {campaign_type}"

            # Filter session table for this campaign
            filtered_table = self._filter_for_campaign(session_table, campaign_type)
            if filtered_table.empty:
                return False, None, f"No valid data for {campaign_type}"

            # Process campaign data
            sheets_data = processor.process(template_df, filtered_table)

            # Format output
            formatted_sheets = self.formatter.format_sheets(sheets_data)

            # Write to Excel
            output_file = self.bulk_writer.write(formatted_sheets)

            return True, output_file, None

        except Exception as e:
            self.logger.error(f"Error processing campaign {campaign_type}: {str(e)}")
            return False, None, str(e)

    def process_multiple_campaigns(
        self,
        selected_campaigns: List[str],
        template_df: pd.DataFrame,
        data_dive_targets: Dict,
        data_rova_df: Optional[pd.DataFrame] = None,
    ) -> Tuple[bool, Optional[BytesIO], Optional[str]]:
        """Process multiple campaign types.
        
        Args:
            selected_campaigns: List of selected campaign types
            template_df: Template dataframe
            data_dive_targets: Dictionary with keywords and ASINs
            data_rova_df: Optional Data Rova dataframe
            
        Returns:
            Tuple of (success, output_file, error_message)
        """
        try:
            # Build session table
            keyword_data = {}
            if data_rova_df is not None:
                from .data_rova_reader import DataRovaReader
                reader = DataRovaReader()
                keyword_data = reader.get_keyword_data(data_rova_df)

            session_table = self.session_builder.build_session_table(
                template_df, data_dive_targets, selected_campaigns, keyword_data
            )

            if session_table.empty:
                return False, None, "No valid data in session table"

            # Process each campaign and collect results
            all_sheets = {}
            for ui_campaign_type in selected_campaigns:
                # Convert UI campaign name to processor format
                processor_campaign_type = self._ui_to_processor_name(ui_campaign_type)
                
                validator = get_validator(processor_campaign_type)
                if not validator:
                    self.logger.warning(f"No validator for {processor_campaign_type}")
                    continue

                is_valid, error = validator.validate(template_df, session_table, data_rova_df)
                if not is_valid:
                    self.logger.warning(f"Validation failed for {processor_campaign_type}: {error}")
                    continue

                processor = get_processor(processor_campaign_type)
                if not processor:
                    self.logger.warning(f"No processor for {processor_campaign_type}")
                    continue

                # Filter using UI campaign name (matches session table)
                filtered_table = self._filter_for_campaign(session_table, ui_campaign_type)
                if filtered_table.empty:
                    self.logger.warning(f"No data for {ui_campaign_type} after filtering")
                    continue

                sheets = processor.process(template_df, filtered_table)
                
                # Merge sheets
                for sheet_name, df in sheets.items():
                    if sheet_name in all_sheets:
                        all_sheets[sheet_name] = pd.concat([all_sheets[sheet_name], df], ignore_index=True)
                    else:
                        all_sheets[sheet_name] = df

            if not all_sheets:
                return False, None, "No campaigns could be processed"

            # Format and write output
            formatted_sheets = self.formatter.format_sheets(all_sheets)
            output_file = self.bulk_writer.write(formatted_sheets)

            return True, output_file, None

        except Exception as e:
            self.logger.error(f"Error processing campaigns: {str(e)}")
            return False, None, str(e)

    def _ui_to_processor_name(self, ui_campaign_type: str) -> str:
        """Convert UI campaign name to processor format.
        
        Args:
            ui_campaign_type: Campaign name from UI (e.g., "Halloween Testing")
            
        Returns:
            Processor format name (e.g., "halloween_testing")
        """
        mapping = {
            "Halloween Testing": "halloween_testing",
            "Halloween Phrase": "halloween_phrase", 
            "Halloween Broad": "halloween_broad",
            "Halloween Expanded": "halloween_expanded",
            "Testing": "testing",
            "Testing PT": "testing_pt",
            "Phrase": "phrase",
            "Broad": "broad",
            "Expanded": "expanded"
        }
        return mapping.get(ui_campaign_type, ui_campaign_type.lower().replace(" ", "_"))

    def _filter_for_campaign(self, session_table: pd.DataFrame, ui_campaign_type: str) -> pd.DataFrame:
        """Filter session table for specific campaign type.
        
        Args:
            session_table: Full session table
            ui_campaign_type: UI campaign name (matches session table format)
            
        Returns:
            Filtered dataframe
        """
        # Filter by campaign type (session table stores UI names)
        filtered = session_table[session_table["Campaign type"] == ui_campaign_type].copy()
        
        # Additional filtering based on campaign requirements
        if "testing" in ui_campaign_type.lower() or "phrase" in ui_campaign_type.lower() or "broad" in ui_campaign_type.lower():
            if "pt" not in ui_campaign_type.lower():
                # Keyword campaigns - filter by sales and CVR
                filtered = filtered[
                    (filtered["kw sales"] > 0) & (filtered["kw cvr"] > 0.08)
                ]
        
        return filtered

    def validate_prerequisites(
        self,
        template_df: pd.DataFrame,
        data_dive_targets: Dict,
        selected_campaigns: List[str],
        data_rova_df: Optional[pd.DataFrame] = None,
    ) -> Tuple[bool, Optional[str]]:
        """Validate prerequisites before processing.
        
        Args:
            template_df: Template dataframe
            data_dive_targets: Dictionary with keywords and ASINs
            selected_campaigns: List of selected campaign types
            data_rova_df: Optional Data Rova dataframe
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check template
        if template_df is None or template_df.empty:
            return False, "No template data"

        # Check required template columns
        required_cols = ["My ASIN", "Product Type", "Niche"]
        missing = [col for col in required_cols if col not in template_df.columns]
        if missing:
            return False, f"Template missing columns: {', '.join(missing)}"

        # Check Data Dive targets
        if not data_dive_targets or (not data_dive_targets.get("keywords") and not data_dive_targets.get("asins")):
            return False, "No targets from Data Dive"

        # Check campaign selection
        if not selected_campaigns:
            return False, "No campaigns selected"

        # Check if keyword campaigns need Data Rova
        keyword_campaigns = ["testing", "phrase", "broad", "halloween_testing", "halloween_phrase", "halloween_broad"]
        needs_rova = any(c in keyword_campaigns for c in selected_campaigns)
        
        if needs_rova and (data_rova_df is None or data_rova_df.empty):
            keyword_camp_names = [c for c in selected_campaigns if c in keyword_campaigns]
            return False, f"Data Rova required for: {', '.join(keyword_camp_names)}"

        return True, None
