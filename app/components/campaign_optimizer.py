"""Campaign Creator page with validation logic."""

import streamlit as st
import pandas as pd
from data.campaign_template_generator import CampaignTemplateGenerator
from data.readers.excel_reader import ExcelReader
from business.campaign_creator.validation import CampaignValidation
from business.campaign_creator.data_dive_reader import DataDiveReader
from business.campaign_creator.data_rova_reader import DataRovaReader
from business.campaign_creator.session_builder import SessionBuilder
from business.campaign_creator.orchestrator import CampaignCreatorOrchestrator
from data.validators.campaign_validators import CampaignTemplateValidator


class CampaignOptimizerPage:
    """Main page for Campaign Creator functionality."""

    def __init__(self):
        """Initialize Campaign Creator page."""
        self.validation = CampaignValidation()
        self.data_dive_reader = DataDiveReader()
        self.data_rova_reader = DataRovaReader()
        self.session_builder = SessionBuilder()
        self.orchestrator = CampaignCreatorOrchestrator()
        self.template_validator = CampaignTemplateValidator()

    def render(self):
        """Render the complete Campaign Creator page."""

        # Import and apply custom CSS
        from app.ui.layout import apply_custom_css

        apply_custom_css()

        # Create 6 columns layout: [col1 | col2 | col3 | col4 | col5 | col6]
        col1, col2, col3, col4, col5, col6 = st.columns([1, 7, 1, 1, 6, 2])

        # TITLE IN SECOND COLUMN FROM LEFT
        with col2:
            st.markdown(
                "<h1 style='text-align: left;'>Campaign Creator</h1>",
                unsafe_allow_html=True,
            )

        # ALL CONTENT IN FIFTH COLUMN (SECOND FROM RIGHT)
        with col5:
            # Optimization selection
            st.markdown(
                "<h3 style='text-align: left;'>1. Select Optimization</h3>",
                unsafe_allow_html=True,
            )

            # Use checkboxes for multiple selection
            st.write("Select optimization(s):")

            # Store selections in session state
            testing = st.checkbox("Testing", value=False, key="testing_checkbox")
            testing_pt = st.checkbox(
                "Testing PT", value=False, key="testing_pt_checkbox"
            )
            phrase = st.checkbox("Phrase", value=False, key="phrase_checkbox")
            broad = st.checkbox("Broad", value=False, key="broad_checkbox")
            expanded = st.checkbox("Expanded", value=False, key="expanded_checkbox")
            halloween_testing = st.checkbox(
                "Halloween Testing", value=False, key="halloween_testing_checkbox"
            )
            halloween_testing_pt = st.checkbox(
                "Halloween Testing PT", value=False, key="halloween_testing_pt_checkbox"
            )
            halloween_phrase = st.checkbox(
                "Halloween Phrase", value=False, key="halloween_phrase_checkbox"
            )
            halloween_broad = st.checkbox(
                "Halloween Broad", value=False, key="halloween_broad_checkbox"
            )
            halloween_expanded = st.checkbox(
                "Halloween Expanded", value=False, key="halloween_expanded_checkbox"
            )

            # Collect selected campaigns
            selected_campaigns = []
            if testing:
                selected_campaigns.append("Testing")
            if testing_pt:
                selected_campaigns.append("Testing PT")
            if phrase:
                selected_campaigns.append("Phrase")
            if broad:
                selected_campaigns.append("Broad")
            if expanded:
                selected_campaigns.append("Expanded")
            if halloween_testing:
                selected_campaigns.append("Halloween Testing")
            if halloween_testing_pt:
                selected_campaigns.append("Halloween Testing PT")
            if halloween_phrase:
                selected_campaigns.append("Halloween Phrase")
            if halloween_broad:
                selected_campaigns.append("Halloween Broad")
            if halloween_expanded:
                selected_campaigns.append("Halloween Expanded")

            st.session_state.selected_campaigns = selected_campaigns

            st.markdown(
                """
                <div style='height: 150px;'></div>
                """,
                unsafe_allow_html=True,
            )

            # Upload Files section
            st.markdown(
                "<h3 style='text-align: left;'>2. Upload Files</h3>",
                unsafe_allow_html=True,
            )

            # Download Template button
            template_gen = CampaignTemplateGenerator()
            template_data = template_gen.generate_template()

            st.download_button(
                label="Download Template",
                data=template_data,
                file_name="campaign_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

            # Upload Template
            template_file = st.file_uploader(
                "Upload Template", type=["xlsx"], key="campaign_template_uploader"
            )

            if template_file:
                try:
                    template_df = pd.read_excel(
                        template_file, sheet_name="Campaign Configuration"
                    )
                    is_valid, msg = self.template_validator.validate(template_df)
                    if is_valid:
                        st.session_state.campaign_template_df = template_df
                        st.session_state.campaign_template_uploaded = True
                        st.success("Template uploaded successfully!")
                    else:
                        st.error(f"Template validation failed: {msg}")
                        st.session_state.campaign_template_uploaded = False
                except Exception as e:
                    st.error(f"Error reading template: {str(e)}")
                    st.session_state.campaign_template_uploaded = False

            # Data Dive upload - Multiple files
            data_dive_files = st.file_uploader(
                "Data Dive (up to 20 files)",
                type=["xlsx", "csv"],
                key="data_dive_uploader",
                accept_multiple_files=True,
            )

            if data_dive_files:
                dataframes, error = self.data_dive_reader.read_files(data_dive_files)
                if error:
                    st.error(error)
                    st.session_state.data_dive_dataframes = None
                else:
                    st.session_state.data_dive_dataframes = dataframes
                    st.session_state.data_dive_uploaded = True
                    targets = self.data_dive_reader.get_all_targets(dataframes)
                    st.session_state.data_dive_targets = targets
                    st.success(
                        f"{len(data_dive_files)} Data Dive files uploaded! Found {len(targets['keywords'])} keywords and {len(targets['asins'])} ASINs"
                    )

            # Data Rova upload
            data_rova_file = st.file_uploader(
                "Data Rova (optional)", type=["xlsx", "csv"], key="data_rova_uploader"
            )

            if data_rova_file:
                df, error = self.data_rova_reader.read_file(data_rova_file)
                if error:
                    st.error(error)
                    st.session_state.data_rova_df = None
                else:
                    st.session_state.data_rova_df = df
                    st.session_state.data_rova_uploaded = True
                    st.success("Data Rova uploaded!")

            # Validation Section
            if st.session_state.get(
                "campaign_template_uploaded"
            ) and st.session_state.get("data_dive_uploaded"):
                st.markdown(
                    "<h3 style='text-align: left;'>3. Data Validation</h3>",
                    unsafe_allow_html=True,
                )

                # Run validation
                template_df = st.session_state.get("campaign_template_df")
                data_dive_dataframes = st.session_state.get("data_dive_dataframes", [])
                data_rova_df = st.session_state.get("data_rova_df")
                selected = st.session_state.get("selected_campaigns", [])

                if template_df is not None and data_dive_dataframes and selected:
                    # Validate files
                    is_valid, msg, validation_data = self.validation.validate_files(
                        template_df, data_dive_dataframes, data_rova_df, selected
                    )

                    if not is_valid:
                        st.error(msg)
                    else:
                        # Check for missing keywords
                        missing_keywords = validation_data.get(
                            "missing_keywords", set()
                        )

                        if missing_keywords and validation_data.get("needs_keywords"):
                            # Check edge cases
                            edge_valid, edge_msg = self.validation.check_edge_cases(
                                validation_data
                            )

                            if not edge_valid:
                                st.error(edge_msg)
                            else:
                                if edge_msg:  # Warning message
                                    st.warning(edge_msg)

                                # Show missing keywords in expandable section
                                with st.expander(
                                    f"⚠️ {len(missing_keywords)} keywords missing DR info - Click to view"
                                ):
                                    keywords_text = "\n".join(sorted(missing_keywords))
                                    st.text_area(
                                        "Copy these keywords to search in Data Rova:",
                                        value=keywords_text,
                                        height=200,
                                        help="Select all (Ctrl+A) and copy (Ctrl+C)",
                                    )

                                st.info(
                                    "You can either upload Data Rova file or proceed without these keywords"
                                )
                        else:
                            st.success("✅ All validations passed!")
                            st.info("Ready for processing!")

                # Build session table if validation passed
                if template_df is not None and data_dive_dataframes:
                    targets = st.session_state.get("data_dive_targets", {})

                    # Get keyword data from Data Rova if available
                    keyword_data = {}
                    if data_rova_df is not None:
                        keyword_data = self.data_rova_reader.get_keyword_data(
                            data_rova_df
                        )

                    # Build session table
                    session_table = self.session_builder.build_session_table(
                        template_df, targets, selected, keyword_data
                    )

                    # Save to session state
                    self.session_builder.save_to_session_state(session_table)

            # Process button section
            st.markdown(
                """
                <div style='height: 50px;'></div>
                """,
                unsafe_allow_html=True,
            )

            # Process button - enabled when minimum requirements met
            process_enabled = (
                st.session_state.get("campaign_template_uploaded", False)
                and st.session_state.get("data_dive_uploaded", False)
                and len(st.session_state.get("selected_campaigns", [])) > 0
            )

            if st.button(
                "Process Files",
                use_container_width=True,
                disabled=not process_enabled,
                key="campaign_process_button",
            ):
                # Real campaign processing
                with st.spinner("Processing campaigns..."):
                    try:
                        # Get data from session state
                        template_df = st.session_state.get("campaign_template_df")
                        data_dive_targets = st.session_state.get("data_dive_targets", {})
                        data_rova_df = st.session_state.get("data_rova_df")
                        selected = st.session_state.get("selected_campaigns", [])
                        
                        # Set up logging to capture debug info
                        import logging
                        import io
                        log_stream = io.StringIO()
                        handler = logging.StreamHandler(log_stream)
                        handler.setLevel(logging.INFO)
                        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
                        handler.setFormatter(formatter)
                        
                        # Add handler to relevant loggers
                        processor_logger = logging.getLogger('business.campaign_creator.processors.halloween_testing')
                        processor_logger.addHandler(handler)
                        processor_logger.setLevel(logging.INFO)
                        
                        orchestrator_logger = logging.getLogger('business.campaign_creator.orchestrator')
                        orchestrator_logger.addHandler(handler)
                        orchestrator_logger.setLevel(logging.INFO)
                        
                        # Use the original UI campaign names - the orchestrator will handle conversion
                        # Process campaigns
                        success, output_file, error = self.orchestrator.process_multiple_campaigns(
                            selected, template_df, data_dive_targets, data_rova_df
                        )
                        
                        # Show logs for debugging
                        logs = log_stream.getvalue()
                        if logs:
                            st.text_area("Processing Debug Info:", logs, height=300)
                        
                        if success:
                            # Store the generated file in session state
                            st.session_state.campaign_bulk_file = output_file
                            st.session_state.campaign_processing_complete = True
                            st.success("✅ Campaign processing complete!")
                        else:
                            st.error(f"❌ Processing failed: {error}")
                            st.session_state.campaign_processing_complete = False
                            
                    except Exception as e:
                        st.error(f"❌ Unexpected error during processing: {str(e)}")
                        st.session_state.campaign_processing_complete = False

            # Output Files section
            if st.session_state.get("campaign_processing_complete", False):
                st.markdown(
                    """
                    <div style='height: 50px;'></div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    "<h3 style='text-align: left;'>5. Output Files</h3>",
                    unsafe_allow_html=True,
                )

                # Check if we have a bulk file to download
                bulk_file = st.session_state.get("campaign_bulk_file")
                if bulk_file:
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"campaign_bulk_{timestamp}.xlsx"
                    
                    st.download_button(
                        label="Download Campaign Bulk File",
                        data=bulk_file.getvalue(),
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                        key="campaign_download_button",
                    )
                else:
                    st.error("No bulk file available. Please process campaigns first.")
