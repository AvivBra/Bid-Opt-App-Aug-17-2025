"""Bid Optimizer page - Complete working version with 6-column layout."""

import streamlit as st
from data.template_generator import TemplateGenerator


class BidOptimizerPage:
    """Main page for Bid Optimizer functionality."""

    def render(self):
        """Render the complete Bid Optimizer page."""

        # Import and apply custom CSS
        from app.ui.layout import apply_custom_css

        apply_custom_css()

        # Create 6 columns layout: [col1 | col2 | col3 | col4 | col5 | col6]
        # שינוי: הוספת עמודה נוספת והתאמת הפרופורציות
        col1, col2, col3, col4, col5, col6 = st.columns([1, 7, 1, 1, 6, 2])

        # TITLE IN SECOND COLUMN FROM LEFT (נשאר אותו דבר)
        with col2:
            st.markdown(
                "<h1 style='text-align: left;'>Bid<br>Optimizer</h1>",
                unsafe_allow_html=True,
            )

        # ALL CONTENT IN FIFTH COLUMN (SECOND FROM RIGHT) - שינוי מ-col4 ל-col5
        with col5:
            # Optimization selection
            st.markdown(
                "<h3 style='text-align: left;'>1.Select Optimization</h3>",
                unsafe_allow_html=True,
            )

            # Use radio buttons for single selection
            optimization = st.radio(
                "Select optimization:",
                ["Zero Sales", "Bids 30 Days", "Bids 60 Days"],
                index=0,  # Default to Zero Sales
                key="optimization_selection",
            )

            # Set flags based on selection
            zero_sales = optimization == "Zero Sales"
            bids_30_days = optimization == "Bids 30 Days"
            bids_60_days = optimization == "Bids 60 Days"

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
            template_gen = TemplateGenerator()
            template_data = template_gen.generate_template()

            st.download_button(
                label="Download Template",
                data=template_data,
                file_name="template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

            # Upload files - template
            template_file = st.file_uploader(
                "Upload Template", type=["xlsx"], key="template_uploader"
            )
            if template_file:
                st.session_state.template_uploaded = True
                st.success("Template uploaded!")

            # Upload files - bulk 60 (only show if Zero Sales selected)
            if zero_sales:
                bulk_60_file = st.file_uploader(
                    "Bulk 60 Days", type=["xlsx", "csv"], key="bulk_60_uploader"
                )
                if bulk_60_file:
                    st.session_state.bulk_60_uploaded = True
                    st.success("Bulk 60 uploaded!")
            elif not zero_sales and not bids_30_days:
                st.button(
                    "Bulk 60 Days (Select Zero Sales first)",
                    disabled=True,
                    use_container_width=True,
                )

            # Upload files - bulk 30 (only show if Bids 30 Days selected)
            if bids_30_days:
                bulk_30_file = st.file_uploader(
                    "Bulk 30 Days", type=["xlsx", "csv"], key="bulk_30_uploader"
                )
                if bulk_30_file:
                    st.session_state.bulk_30_uploaded = True
                    st.success("Bulk 30 uploaded!")
            elif bids_60_days:
                # For Bids 60 Days, show bulk 60 upload
                bulk_60_file_for_60_days = st.file_uploader(
                    "Bulk 60 Days", type=["xlsx", "csv"], key="bulk_60_for_60_days_uploader"
                )
                if bulk_60_file_for_60_days:
                    st.session_state.bulk_60_for_60_days_uploaded = True
                    st.success("Bulk 60 uploaded!")
            elif zero_sales:
                st.button(
                    "Bulk 30 Days (Not needed for Zero Sales)",
                    disabled=True,
                    use_container_width=True,
                )
            else:
                st.button(
                    "Bulk 30 Days (Select Bids 30 Days first)",
                    disabled=True,
                    use_container_width=True,
                )

            # Disabled button - Bulk 7
            st.button(
                "Bulk 7 Days (Coming Soon)",
                disabled=True,
                use_container_width=True,
                help="This feature will be available in a future update",
            )

            # Data Rova button
            st.button(
                "Data Rova (Coming Soon)",
                disabled=True,
                use_container_width=True,
                help="This feature will be available in a future update",
            )

            # Validation Section - Show based on selected optimization
            show_validation = False

            if (
                zero_sales
                and st.session_state.get("template_uploaded")
                and st.session_state.get("bulk_60_uploaded")
            ):
                show_validation = True
                bulk_type = "60"
            elif (
                bids_30_days
                and st.session_state.get("template_uploaded")
                and st.session_state.get("bulk_30_uploaded")
            ):
                show_validation = True
                bulk_type = "30"
            elif (
                bids_60_days
                and st.session_state.get("template_uploaded")
                and st.session_state.get("bulk_60_for_60_days_uploaded")
            ):
                show_validation = True
                bulk_type = "60"

            if show_validation:
                st.markdown(
                    "<h3 style='text-align: center;'>3. Data Validation</h3>",
                    unsafe_allow_html=True,
                )

                # Validation status
                st.success(f"Template and Bulk {bulk_type} files loaded")
                st.info("Ready for processing!")

                # Process button
                if st.button(
                    "Process Files", type="secondary", use_container_width=True
                ):
                    try:
                        with st.spinner("Processing files..."):
                            # Import required modules
                            import pandas as pd
                            from datetime import datetime
                            from business.processors.output_formatter import (
                                OutputFormatter,
                            )

                            # Determine which optimization to use
                            if zero_sales:
                                from business.bid_optimizations.zero_sales.orchestrator import (
                                    ZeroSalesOptimization,
                                )

                                optimization = ZeroSalesOptimization()
                                optimization_name = "Zero Sales"
                            elif bids_30_days:
                                from business.bid_optimizations.bids_30_days.orchestrator import (
                                    Bids30DaysOptimization,
                                )

                                optimization = Bids30DaysOptimization()
                                optimization_name = "Bids 30 Days"
                            else:  # bids_60_days
                                from business.bid_optimizations.bids_60_days.orchestrator import (
                                    Bids60DaysOptimization,
                                )

                                optimization = Bids60DaysOptimization()
                                optimization_name = "Bids 60 Days"

                            # Read template
                            import io

                            template_df = pd.read_excel(
                                io.BytesIO(template_file.read()), sheet_name=None
                            )
                            template_file.seek(0)

                            # Read bulk based on type and optimization
                            if bulk_type == "60" and zero_sales and bulk_60_file:
                                # Zero Sales uses bulk_60_file
                                if bulk_60_file.name.endswith(".csv"):
                                    bulk_df = pd.read_csv(bulk_60_file)
                                else:
                                    bulk_df = pd.read_excel(
                                        bulk_60_file,
                                        sheet_name="Sponsored Products Campaigns",
                                    )
                            elif bulk_type == "60" and bids_60_days and bulk_60_file_for_60_days:
                                # Bids 60 Days uses bulk_60_file_for_60_days
                                if bulk_60_file_for_60_days.name.endswith(".csv"):
                                    bulk_df = pd.read_csv(bulk_60_file_for_60_days)
                                else:
                                    bulk_df = pd.read_excel(
                                        bulk_60_file_for_60_days,
                                        sheet_name="Sponsored Products Campaigns",
                                    )
                            elif bulk_type == "30" and bulk_30_file:
                                # Bids 30 Days uses bulk_30_file
                                if bulk_30_file.name.endswith(".csv"):
                                    bulk_df = pd.read_csv(bulk_30_file)
                                else:
                                    bulk_df = pd.read_excel(
                                        bulk_30_file,
                                        sheet_name="Sponsored Products Campaigns",
                                    )

                            # Process the optimization
                            st.info(f"Processing {optimization_name} optimization...")

                            # Pre-validation filtering (remove rows with State != "enabled")
                            st.info("Pre-filtering data for validation...")
                            bulk_df = optimization.cleaner.pre_validation_filter(bulk_df)

                            # Validate (now on pre-filtered data)
                            is_valid, validation_msg, validation_details = (
                                optimization.validate(template_df, bulk_df)
                            )

                            if not is_valid:
                                st.error(f"Validation failed: {validation_msg}")
                                return

                            # Clean (remaining filters, no duplicate state filtering)
                            cleaned_data, cleaning_details = optimization.clean(
                                template_df, bulk_df
                            )

                            # Process
                            optimization_results = optimization.process(
                                template_df, cleaned_data
                            )

                            # DEBUG: Check what process() returned
                            print(f"[DEBUG UI] optimization.process() returned:")
                            print(f"[DEBUG UI]   Type: {type(optimization_results)}")
                            if isinstance(optimization_results, dict):
                                print(f"[DEBUG UI]   Keys: {list(optimization_results.keys())}")
                                for key, df in optimization_results.items():
                                    if hasattr(df, 'shape'):
                                        print(f"[DEBUG UI]   {key}: {df.shape} rows x cols")
                                    else:
                                        print(f"[DEBUG UI]   {key}: {type(df)}")
                            else:
                                print(f"[DEBUG UI]   Value: {optimization_results}")

                            # Format output
                            formatter = OutputFormatter()
                            working_file, clean_file = formatter.create_output_files(
                                optimization_results, optimization_name
                            )

                            # DEBUG: Check what create_output_files() returned
                            print(f"[DEBUG UI] OutputFormatter.create_output_files() returned:")
                            print(f"[DEBUG UI]   working_file type: {type(working_file)}")
                            print(f"[DEBUG UI]   working_file size: {len(working_file.getvalue()) if hasattr(working_file, 'getvalue') else 'N/A'} bytes")
                            print(f"[DEBUG UI]   clean_file type: {type(clean_file)}")
                            print(f"[DEBUG UI]   clean_file size: {len(clean_file.getvalue()) if hasattr(clean_file, 'getvalue') else 'N/A'} bytes")

                            # Show results
                            st.markdown(
                                "<h3 style='text-align: center;'>4. Results</h3>",
                                unsafe_allow_html=True,
                            )

                            st.success(
                                f"{optimization_name} optimization completed successfully!"
                            )

                            # Get statistics
                            stats = optimization.get_statistics()
                            if stats:
                                st.info(
                                    f"Processed: {stats.get('rows_processed', 0)} rows | "
                                    f"Modified: {stats.get('rows_modified', 0)} bids"
                                )

                                # Show additional stats for Bids 30 Days and Bids 60 Days
                                if (
                                    (bids_30_days or bids_60_days)
                                    and stats.get("rows_to_harvesting", 0) > 0
                                ):
                                    st.info(
                                        f"Moved to For Harvesting: {stats.get('rows_to_harvesting', 0)} rows"
                                    )

                            # Download buttons
                            col1, col2 = st.columns(2)

                            # DEBUG: Final check before download button
                            print(f"[DEBUG UI] Before download button:")
                            print(f"[DEBUG UI]   working_file variable type: {type(working_file)}")
                            print(f"[DEBUG UI]   working_file size: {len(working_file.getvalue()) if hasattr(working_file, 'getvalue') else 'N/A'} bytes")

                            with col1:
                                st.download_button(
                                    label="Download Working File",
                                    data=working_file,
                                    file_name=f"working_file_{optimization_name.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    use_container_width=True,
                                )

                            with col2:
                                st.download_button(
                                    label="Download Clean File",
                                    data=clean_file,
                                    file_name=f"clean_file_{optimization_name.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    use_container_width=True,
                                )

                    except Exception as e:
                        st.error(f"Error processing files: {str(e)}")
                        import traceback

                        st.code(traceback.format_exc())


# Required for page registration
def show():
    """Show function required for page registration."""
    page = BidOptimizerPage()
    page.render()
