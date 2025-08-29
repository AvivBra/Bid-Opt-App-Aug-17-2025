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

            # Dynamic optimization checkboxes - Factory-based discovery
            from business.portfolio_optimizations.factory import get_portfolio_optimization_factory
            
            factory = get_portfolio_optimization_factory()
            available_optimizations = factory.get_enabled_optimizations()
            
            # Generate checkboxes for each available optimization
            selected_optimizations = {}
            for opt_name, opt_info in available_optimizations.items():
                display_name = opt_info.get("display_name", opt_name)
                
                selected = st.checkbox(
                    display_name,
                    value=False,
                    key=f"{opt_name}_selection",
                    help=f"{opt_info.get('metadata', {}).get('description', f'Run {display_name} optimization')}"
                )
                
                selected_optimizations[opt_name] = selected
                
                # Store in session state for processing
                st.session_state[f"{opt_name}_selected"] = selected

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
            any_optimization_selected = any(selected_optimizations.values())

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
                    # Note: Individual optimization selections are already stored in session state by the dynamic checkboxes
                    
                    # Show which optimizations are running
                    selected_opts = []
                    for opt_name, selected in selected_optimizations.items():
                        if selected:
                            display_name = factory.get_display_name(opt_name)
                            selected_opts.append(display_name)
                    
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
                    
                    # Initialize factory and results manager
                    from business.portfolio_optimizations.factory import get_portfolio_optimization_factory
                    from business.portfolio_optimizations.results_manager import PortfolioOptimizationResultsManager
                    from io import BytesIO
                    
                    factory = get_portfolio_optimization_factory()
                    results_manager = PortfolioOptimizationResultsManager()
                    
                    # Get selected optimizations from session state
                    selected_opts = []
                    for opt_name in factory.get_enabled_optimizations().keys():
                        if st.session_state.get(f"{opt_name}_selected", False):
                            selected_opts.append(opt_name)
                    
                    if not selected_opts:
                        self.logger.warning("No optimizations selected")
                        st.warning("No optimizations selected. Please select at least one optimization.")
                        st.session_state.portfolio_processing_status = "error"
                        st.rerun()
                        return
                    
                    self.logger.info(f"Processing {len(selected_opts)} selected optimizations: {selected_opts}")
                    
                    progress_step = 60 / len(selected_opts) if selected_opts else 0
                    current_progress = 30
                    
                    # Process each selected optimization
                    for i, opt_name in enumerate(selected_opts):
                        display_name = factory.get_display_name(opt_name)
                        self.logger.info(f"Starting {display_name} optimization")
                        st.info(f"Processing {display_name} optimization...")
                        
                        try:
                            # Create orchestrator instance
                            orchestrator = factory.create_optimization(opt_name)
                            if orchestrator is None:
                                self.logger.error(f"Failed to create orchestrator for {opt_name}")
                                st.error(f"Failed to initialize {display_name} optimization")
                                continue
                            
                            self.logger.debug(f"{display_name} orchestrator instantiated")
                            
                            # Run optimization with standardized interface
                            self.logger.debug(f"Calling run with data: {list(all_sheets.keys())}")
                            processed_df, processing_details = orchestrator.run(all_sheets, combined_mode=True)
                            
                            self.logger.info(f"{display_name} result: DataFrame is not None: {processed_df is not None}")
                            if processed_df is not None:
                                self.logger.debug(f"Processed DataFrame: {len(processed_df)} rows")
                            self.logger.debug(f"Processing details: {processing_details}")
                            
                            # Determine result type based on optimization
                            result_type = "portfolios" if "portfolios" in opt_name.lower() else "campaigns"
                            
                            # Add result to results manager
                            results_manager.add_result(
                                optimization_name=opt_name,
                                processed_df=processed_df,
                                details=processing_details,
                                result_type=result_type
                            )
                            
                            if processed_df is not None:
                                self.logger.info(f"{display_name} completed successfully")
                                st.success(f"{display_name} processing completed!")
                            else:
                                self.logger.error(f"{display_name} returned None DataFrame")
                                st.error(f"{display_name} error: No data returned")
                                
                        except Exception as e:
                            self.logger.error(f"{display_name} exception: {str(e)}")
                            import traceback
                            self.logger.debug(f"{display_name} traceback: {traceback.format_exc()}")
                            st.error(f"{display_name} error: {str(e)}")
                            
                            # Add failed result to manager
                            results_manager.add_result(
                                optimization_name=opt_name,
                                processed_df=None,
                                details={"error": str(e), "summary": {"success": False, "message": f"Failed: {str(e)}"}}
                            )
                        
                        # Update progress
                        current_progress += progress_step
                        progress_bar.progress(int(current_progress))
                    
                    progress_bar.progress(90)
                    
                    # Create combined output using results manager
                    if results_manager.has_any_successful_results():
                        self.logger.info("Creating combined output file from multiple optimizations")
                        try:
                            combined_file, summary_details = results_manager.create_combined_output(all_sheets)
                            
                            if combined_file:
                                st.session_state.portfolio_working_file = combined_file.getvalue()
                                st.session_state.portfolio_output_generated = True
                                
                                # Log summary
                                successful_count = summary_details.get("successful_optimizations", 0)
                                total_count = summary_details.get("total_optimizations", 0)
                                campaigns_updated = summary_details.get("campaigns_updated", 0)
                                portfolios_updated = summary_details.get("portfolios_updated", 0)
                                
                                self.logger.info(f"Combined output file created successfully: {successful_count}/{total_count} optimizations")
                                self.logger.info(f"Updates: {campaigns_updated} campaigns, {portfolios_updated} portfolios")
                                
                                # Show success message
                                success_msg = f"✅ Combined output file created successfully! ({successful_count}/{total_count} optimizations completed)"
                                if campaigns_updated > 0:
                                    success_msg += f"\n📊 Updated {campaigns_updated} campaigns"
                                if portfolios_updated > 0:
                                    success_msg += f"\n📁 Updated {portfolios_updated} portfolios"
                                
                                st.info(success_msg)
                            else:
                                error_msg = summary_details.get("error", "Unknown error creating combined file")
                                self.logger.error(f"Failed to create combined output file: {error_msg}")
                                st.error(f"Failed to create combined output file: {error_msg}")
                        except Exception as e:
                            self.logger.error(f"Error creating combined file: {str(e)}")
                            import traceback
                            self.logger.debug(f"Combined file traceback: {traceback.format_exc()}")
                            st.error(f"Error creating combined file: {str(e)}")
                    else:
                        failed_opts = results_manager.get_failed_optimizations()
                        self.logger.warning(f"No successful optimizations to combine. Failed: {len(failed_opts)}")
                        
                        error_msg = "No optimizations completed successfully. No output file generated."
                        if failed_opts:
                            error_details = "\n".join([f"• {name}: {msg}" for name, msg in failed_opts])
                            error_msg += f"\n\nFailed optimizations:\n{error_details}"
                        
                        st.error(error_msg)
                    
                    # Final processing steps
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
                    st.error("No output file available")

                # Reset button
                if st.button("Start New Optimization", key="btn_new_portfolio", use_container_width=True):
                    # Clear relevant session state
                    keys_to_clear = [key for key in st.session_state.keys() if key.startswith("portfolio_")]
                    for key in keys_to_clear:
                        if key != "portfolio_optimizer_logger":  # Keep the logger
                            del st.session_state[key]
                    st.rerun()
