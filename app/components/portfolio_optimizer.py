"""Portfolio Optimizer page - Based on Bid Optimizer layout."""

import streamlit as st
import pandas as pd
import logging
from datetime import datetime
from data.template_generator import TemplateGenerator

# Set up logging for terminal debugging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [PortfolioOptimizer] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class PortfolioOptimizerPage:
    """Main page for Portfolio Optimizer functionality."""

    def __init__(self):
        self.logger = logging.getLogger("PortfolioOptimizer")

    def render(self):
        """Render the complete Portfolio Optimizer page."""

        # Import and apply custom CSS
        from app.ui.layout import apply_custom_css

        apply_custom_css()

        # Create 6 columns layout: [col1 | col2 | col3 | col4 | col5 | col6]
        col1, col2, col3, col4, col5, col6 = st.columns([1, 7, 1, 1, 6, 2])

        # TITLE IN SECOND COLUMN FROM LEFT
        with col2:
            st.markdown(
                "<h1 style='text-align: left;'>Portfolio<br>Optimizer</h1>",
                unsafe_allow_html=True,
            )

        # ALL CONTENT IN FIFTH COLUMN (SECOND FROM RIGHT)
        with col5:
            # Optimization selection
            st.markdown(
                "<h3 style='text-align: left;'>1.Select Optimization</h3>",
                unsafe_allow_html=True,
            )

            # Optimization checkboxes - Allow multiple selections
            empty_portfolios = st.checkbox(
                "Empty Portfolios",
                value=False,
                key="empty_portfolios_selection",
            )
            
            campaigns_without_portfolios = st.checkbox(
                "Campaigns w/o Portfolios",
                value=False,
                key="campaigns_without_portfolios_selection",
            )

            st.markdown(
                """
                <div style='height: 150px;'></div>
                """,
                unsafe_allow_html=True,
            )

            # Upload Files section
            st.markdown(
                "<h3 style='text-align: left;'>2.Upload Files</h3>",
                unsafe_allow_html=True,
            )

            # Only need Bulk file for Empty Portfolios (no template needed)
            uploaded_bulk = st.file_uploader(
                "Bulk 60 Days",
                type=["xlsx", "csv"],
                key="portfolio_bulk_60_upload",
                help="Excel or CSV file with Sponsored Products Campaigns data",
            )

            if uploaded_bulk:
                self.logger.info(f"File upload started: {uploaded_bulk.name}")
                try:
                    import pandas as pd
                    import io
                    
                    # Parse the uploaded file into DataFrame
                    if uploaded_bulk.name.endswith(".csv"):
                        self.logger.debug("Parsing CSV file")
                        bulk_df = pd.read_csv(uploaded_bulk)
                    else:
                        self.logger.debug("Parsing Excel file")
                        # Read the Excel file with all sheets first to check structure
                        bulk_data = pd.read_excel(
                            io.BytesIO(uploaded_bulk.read()), sheet_name=None
                        )
                        uploaded_bulk.seek(0)  # Reset file pointer
                        
                        sheet_names = list(bulk_data.keys())
                        self.logger.debug(f"Excel sheets found: {sheet_names}")
                        
                        # Get the Sponsored Products Campaigns sheet
                        if "Sponsored Products Campaigns" in bulk_data:
                            bulk_df = bulk_data["Sponsored Products Campaigns"]
                            self.logger.debug("Using 'Sponsored Products Campaigns' sheet")
                        else:
                            # Try to find the main sheet with campaigns data
                            if sheet_names:
                                bulk_df = bulk_data[sheet_names[0]]  # Use first sheet
                                self.logger.warning(f"'Sponsored Products Campaigns' not found, using first sheet: {sheet_names[0]}")
                            else:
                                raise ValueError("No valid sheets found in Excel file")
                    
                    # Store both file and parsed DataFrame
                    st.session_state.portfolio_bulk_60_file = uploaded_bulk
                    st.session_state.portfolio_bulk_60_df = bulk_df
                    st.session_state.portfolio_bulk_60_uploaded = True
                    
                    self.logger.info(f"File parsed successfully: {len(bulk_df)} rows, {len(bulk_df.columns)} columns")
                    self.logger.debug(f"DataFrame columns: {list(bulk_df.columns)[:10]}...")  # Show first 10 columns
                    
                    st.success(f"Bulk 60 uploaded! Found {len(bulk_df)} rows.")
                    
                except Exception as e:
                    self.logger.error(f"File parsing failed: {str(e)}")
                    import traceback
                    self.logger.debug(f"Full traceback: {traceback.format_exc()}")
                    st.error(f"Error reading file: {str(e)}")
                    st.session_state.portfolio_bulk_60_uploaded = False

            st.markdown(
                """
                <div style='height: 150px;'></div>
                """,
                unsafe_allow_html=True,
            )

            # Process Files section
            st.markdown(
                "<h3 style='text-align: left;'>3.Process Files</h3>",
                unsafe_allow_html=True,
            )

            # Check if files are ready
            files_ready = st.session_state.get("portfolio_bulk_60_uploaded", False)
            any_optimization_selected = empty_portfolios or campaigns_without_portfolios

            # Process button
            if st.button(
                "Process Files",
                key="btn_process_portfolio",
                use_container_width=True,
                disabled=not files_ready or not any_optimization_selected,
            ):
                if files_ready and any_optimization_selected:
                    st.session_state.portfolio_processing_started = True
                    st.session_state.portfolio_processing_status = "processing"
                    st.session_state.empty_portfolios_selected = empty_portfolios
                    st.session_state.campaigns_without_portfolios_selected = campaigns_without_portfolios
                    
                    # Show which optimizations are running
                    selected_opts = []
                    if empty_portfolios:
                        selected_opts.append("Empty Portfolios")
                    if campaigns_without_portfolios:
                        selected_opts.append("Campaigns w/o Portfolios")
                    
                    self.logger.info(f"Starting processing with optimizations: {selected_opts}")
                    self.logger.debug(f"Files ready: {files_ready}, Any selected: {any_optimization_selected}")
                    
                    st.success(f"Processing {' and '.join(selected_opts)} optimization(s)...")
                    st.rerun()
                else:
                    if not files_ready:
                        st.error("Please upload Bulk 60 file first")
                    if not any_optimization_selected:
                        st.error("Please select at least one optimization")

            # Show processing status
            if st.session_state.get("portfolio_processing_status") == "processing":
                st.info("⏳ Processing... This may take a few seconds.")
                progress_bar = st.progress(0)
                
                try:
                    self.logger.info("=== PROCESSING STARTED ===")
                    # Get the uploaded file data - we need all sheets for Empty Portfolios
                    bulk_file = st.session_state.get("portfolio_bulk_60_file")
                    bulk_df = st.session_state.get("portfolio_bulk_60_df")
                    if bulk_df is None or bulk_file is None:
                        self.logger.error("No bulk file data found in session state")
                        st.error("No bulk file data found. Please upload file again.")
                        st.session_state.portfolio_processing_status = "error"
                        st.rerun()
                        return
                    
                    self.logger.debug(f"Retrieved DataFrame: {len(bulk_df)} rows, {len(bulk_df.columns)} columns")
                    
                    # Read all sheets from the Excel file for orchestrators that need multiple sheets
                    try:
                        import io
                        bulk_file.seek(0)  # Reset file pointer
                        all_sheets = pd.read_excel(io.BytesIO(bulk_file.read()), sheet_name=None)
                        bulk_file.seek(0)  # Reset again for future use
                        
                        self.logger.debug(f"All Excel sheets loaded: {list(all_sheets.keys())}")
                        for sheet_name, sheet_df in all_sheets.items():
                            self.logger.debug(f"Sheet '{sheet_name}': {len(sheet_df)} rows")
                    except Exception as e:
                        self.logger.warning(f"Could not read all sheets: {str(e)}, using single DataFrame")
                        all_sheets = {"Sponsored Products Campaigns": bulk_df}
                    progress_bar.progress(20)
                    
                    # Import orchestrators
                    from business.portfolio_optimizations.empty_portfolios.orchestrator import EmptyPortfoliosOrchestrator
                    from business.portfolio_optimizations.campaigns_without_portfolios.orchestrator import CampaignsWithoutPortfoliosOrchestrator
                    from io import BytesIO
                    
                    output_data = {}
                    combined_results = []
                    
                    progress_bar.progress(30)
                    
                    # Process Empty Portfolios if selected
                    if st.session_state.get("empty_portfolios_selected", False):
                        self.logger.info("Starting Empty Portfolios optimization")
                        st.info("Processing Empty Portfolios optimization...")
                        
                        try:
                            empty_orchestrator = EmptyPortfoliosOrchestrator()
                            self.logger.debug("EmptyPortfoliosOrchestrator instantiated")
                            
                            # Use all sheets for Empty Portfolios (needs both Portfolios and Campaigns sheets)
                            self.logger.debug(f"Calling run_optimization with data: {list(all_sheets.keys())}")
                            
                            success, message, output_bytes = empty_orchestrator.run_optimization(all_sheets)
                            
                            self.logger.info(f"Empty Portfolios result: success={success}")
                            self.logger.debug(f"Message: {message}")
                            self.logger.debug(f"Output bytes length: {len(output_bytes) if output_bytes else 0}")
                            
                            if success and output_bytes:
                                from io import BytesIO
                                output_file = BytesIO(output_bytes)
                                combined_results.append({
                                    "type": "empty_portfolios", 
                                    "output_file": output_file, 
                                    "message": message
                                })
                                output_data["output_file"] = output_file
                                self.logger.info("Empty Portfolios completed successfully")
                                st.success(message)
                            else:
                                self.logger.error(f"Empty Portfolios failed: {message}")
                                st.error(f"Empty Portfolios processing failed: {message}")
                        except Exception as e:
                            self.logger.error(f"Empty Portfolios exception: {str(e)}")
                            import traceback
                            self.logger.debug(f"Empty Portfolios traceback: {traceback.format_exc()}")
                            st.error(f"Empty Portfolios error: {str(e)}")
                    
                    progress_bar.progress(60)
                    
                    # Process Campaigns without Portfolios if selected
                    if st.session_state.get("campaigns_without_portfolios_selected", False):
                        self.logger.info("Starting Campaigns without Portfolios optimization")
                        st.info("Processing Campaigns w/o Portfolios optimization...")
                        
                        try:
                            campaigns_orchestrator = CampaignsWithoutPortfoliosOrchestrator()
                            self.logger.debug("CampaignsWithoutPortfoliosOrchestrator instantiated")
                            
                            # Use all sheets for Campaigns w/o Portfolios (mainly needs Campaigns sheet)
                            self.logger.debug(f"Calling run with data: {list(all_sheets.keys())}")
                            
                            # Pass combined_with_empty_portfolios=True to get full DataFrame with all columns
                            processed_df, processing_details = campaigns_orchestrator.run(all_sheets, combined_with_empty_portfolios=True)
                            
                            self.logger.info(f"Campaigns w/o Portfolios result: DataFrame is not None: {processed_df is not None}")
                            if processed_df is not None:
                                self.logger.debug(f"Processed DataFrame: {len(processed_df)} rows")
                            self.logger.debug(f"Processing details: {processing_details}")
                            
                            if processed_df is not None:
                                # Store the DataFrame directly for combined file creation
                                combined_results.append({
                                    "type": "campaigns_without_portfolios",
                                    "processed_df": processed_df,
                                    "details": processing_details
                                })
                                
                                # Also generate output file for individual download
                                from io import BytesIO
                                output_file = BytesIO()
                                with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                                    processed_df.to_excel(writer, sheet_name='Sponsored Products Campaigns', index=False)
                                output_file.seek(0)
                                output_data["output_file"] = output_file
                                self.logger.info("Campaigns w/o Portfolios completed successfully")
                                st.success("Campaigns w/o Portfolios processing completed!")
                            else:
                                self.logger.error("Campaigns w/o Portfolios returned None DataFrame")
                                st.error("Campaigns w/o Portfolios processing failed")
                        except Exception as e:
                            self.logger.error(f"Campaigns w/o Portfolios exception: {str(e)}")
                            import traceback
                            self.logger.debug(f"Campaigns w/o Portfolios traceback: {traceback.format_exc()}")
                            st.error(f"Campaigns w/o Portfolios error: {str(e)}")
                    
                    progress_bar.progress(90)
                    
                    # Create combined output file from all optimization results
                    self.logger.debug(f"File combination: combined_results count = {len(combined_results)}")
                    
                    if combined_results:
                        self.logger.info("Creating combined output file from multiple optimizations")
                        try:
                            combined_file = self._create_combined_output_file(combined_results, all_sheets)
                            if combined_file:
                                st.session_state.portfolio_working_file = combined_file
                                st.session_state.portfolio_output_generated = True
                                self.logger.info(f"Combined output file created successfully ({len(combined_results)} optimization(s))")
                                st.info(f"✅ Combined output file created successfully! ({len(combined_results)} optimization(s) completed)")
                            else:
                                self.logger.error("Failed to create combined output file")
                                st.error("Failed to create combined output file")
                        except Exception as e:
                            self.logger.error(f"Error creating combined file: {str(e)}")
                            import traceback
                            self.logger.debug(f"Combined file creation traceback: {traceback.format_exc()}")
                            st.error(f"Error creating combined file: {str(e)}")
                    else:
                        self.logger.warning("No optimizations in combined_results")
                        st.warning("⚠️ No optimizations were processed successfully")
                    
                    # Final session state check
                    has_working_file = st.session_state.get("portfolio_working_file") is not None
                    self.logger.info(f"Final check - Working file in session state: {has_working_file}")
                    
                    progress_bar.progress(100)
                    
                    # Mark as complete
                    st.session_state.portfolio_processing_status = "complete"
                    self.logger.info("=== PROCESSING COMPLETED SUCCESSFULLY ===")
                    st.rerun()
                    
                except Exception as e:
                    import traceback
                    error_details = f"Processing failed: {str(e)}\n\nFull error:\n{traceback.format_exc()}"
                    self.logger.error(f"=== PROCESSING FAILED ===")
                    self.logger.error(f"Error: {str(e)}")
                    self.logger.debug(f"Full traceback: {traceback.format_exc()}")
                    
                    st.error(f"Processing failed: {str(e)}")
                    st.error("Full error details:")
                    st.code(traceback.format_exc())
                    st.session_state.portfolio_processing_status = "error"
                    st.session_state.portfolio_processing_error = error_details
                    # Don't rerun immediately to keep error visible
                    return

            elif st.session_state.get("portfolio_processing_status") == "error":
                st.error("❌ Processing failed!")
                error_msg = st.session_state.get("portfolio_processing_error", "Unknown error")
                st.error("Error details:")
                st.code(error_msg)
                
                # Reset button for errors
                if st.button("Try Again", key="btn_retry_portfolio", use_container_width=True):
                    st.session_state.portfolio_processing_status = None
                    st.session_state.portfolio_processing_error = None
                    st.rerun()

            elif st.session_state.get("portfolio_processing_status") == "complete":
                st.success("✅ Processing complete!")

                # Download section
                st.markdown(
                    """
                    <div style='height: 50px;'></div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    "<h3 style='text-align: left;'>4.Download Results</h3>",
                    unsafe_allow_html=True,
                )

                # Check if we have output file data
                working_file = st.session_state.get("portfolio_working_file")
                if working_file:
                    from datetime import datetime
                    st.download_button(
                        label="Download Working File",
                        data=working_file,
                        file_name=f"portfolio_optimizer_working_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                    )
                else:
                    st.error("No output file available. Please process files first.")

                # Reset button
                if st.button("Reset", key="btn_reset_portfolio", use_container_width=True):
                    # Clear all portfolio-specific state
                    keys_to_clear = [
                        "portfolio_bulk_60_file",
                        "portfolio_bulk_60_uploaded",
                        "portfolio_processing_started",
                        "portfolio_processing_status",
                        "portfolio_output_generated",
                    ]
                    for key in keys_to_clear:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
    
    def _create_combined_output_file(self, combined_results, all_sheets):
        """
        Create a combined Excel file from all optimization results.
        
        Args:
            combined_results: List of results from different optimizations
            all_sheets: Original Excel sheets from input file
            
        Returns:
            BytesIO object with combined Excel file
        """
        from io import BytesIO
        from config.optimization_config import apply_text_format_before_write
        
        try:
            self.logger.debug("Starting combined file creation")
            
            # START WITH ENTITY=CAMPAIGN FILTERED DATA - only include Campaign entities
            if "Sponsored Products Campaigns" in all_sheets:
                campaigns_sheet_data = all_sheets["Sponsored Products Campaigns"][all_sheets["Sponsored Products Campaigns"]["Entity"] == "Campaign"].copy()
            else:
                campaigns_sheet_data = None
            portfolios_sheet_data = all_sheets["Portfolios"].copy() if "Portfolios" in all_sheets else None
            
            self.logger.debug(f"Starting with original data: {len(campaigns_sheet_data) if campaigns_sheet_data is not None else 0} campaigns, {len(portfolios_sheet_data) if portfolios_sheet_data is not None else 0} portfolios")
            
            # Apply optimization results using direct DataFrames
            for result in combined_results:
                result_type = result.get("type", "unknown")
                
                if result_type == "empty_portfolios":
                    self.logger.debug("Processing Empty Portfolios result")
                    
                    # Extract portfolios sheet from Empty Portfolios result
                    if "output_file" in result:
                        try:
                            result["output_file"].seek(0)
                            empty_sheets = pd.read_excel(result["output_file"], sheet_name=None)
                            result["output_file"].seek(0)
                            
                            # Update portfolios sheet with any changes from Empty Portfolios
                            if "Portfolios" in empty_sheets:
                                portfolios_sheet_data = empty_sheets["Portfolios"]
                                self.logger.debug(f"Updated Portfolios sheet from Empty Portfolios: {len(portfolios_sheet_data)} rows")
                        except Exception as e:
                            self.logger.warning(f"Could not extract sheets from Empty Portfolios result: {e}")
                
                elif result_type == "campaigns_without_portfolios":
                    self.logger.debug("Processing Campaigns w/o Portfolios result")
                    
                    # Use the direct processed DataFrame - this contains all optimizations on full data!
                    if "processed_df" in result and campaigns_sheet_data is not None:
                        processed_df = result["processed_df"]
                        self.logger.debug(f"Using processed DataFrame with {len(processed_df)} rows")
                        
                        # The processed_df contains optimizations applied to full data, but we need only Entity=Campaign
                        campaigns_sheet_data = processed_df[processed_df["Entity"] == "Campaign"].copy()
                        self.logger.info(f"Applied Campaigns w/o Portfolios optimizations: {len(campaigns_sheet_data)} campaigns (Entity=Campaign filtered)")
            
            self.logger.debug(f"Final data: {len(campaigns_sheet_data) if campaigns_sheet_data is not None else 0} campaigns, {len(portfolios_sheet_data) if portfolios_sheet_data is not None else 0} portfolios")
            
            # Create combined Excel file
            output_file = BytesIO()
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # Write Sponsored Products Campaigns sheet (required)
                if campaigns_sheet_data is not None:
                    # Apply text formatting to prevent scientific notation
                    campaigns_formatted = apply_text_format_before_write(campaigns_sheet_data)
                    campaigns_formatted.to_excel(writer, sheet_name='Sponsored Products Campaigns', index=False)
                    self.logger.debug(f"Wrote Campaigns sheet with {len(campaigns_sheet_data)} rows")
                
                # Write Portfolios sheet (if available)
                if portfolios_sheet_data is not None:
                    # Apply text formatting to prevent scientific notation
                    portfolios_formatted = apply_text_format_before_write(portfolios_sheet_data)
                    portfolios_formatted.to_excel(writer, sheet_name='Portfolios', index=False)
                    self.logger.debug(f"Wrote Portfolios sheet with {len(portfolios_sheet_data)} rows")
            
            output_file.seek(0)
            self.logger.info("Combined Excel file created successfully")
            return output_file
            
        except Exception as e:
            self.logger.error(f"Error in _create_combined_output_file: {str(e)}")
            import traceback
            self.logger.debug(f"Full traceback: {traceback.format_exc()}")
            return None
