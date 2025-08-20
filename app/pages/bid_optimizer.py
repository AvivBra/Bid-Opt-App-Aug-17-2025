"""Bid Optimizer page - Complete working version."""

import streamlit as st
from data.template_generator import TemplateGenerator


class BidOptimizerPage:
    """Main page for Bid Optimizer functionality."""

    def render(self):
        """Render the complete Bid Optimizer page."""

        # Page title - CENTERED
        st.markdown(
            "<h1 style='text-align: center;'>Bid Optimizer</h1>", unsafe_allow_html=True
        )
        # Optimization selection - CENTERED
        st.markdown(
            "<h3 style='text-align: center;'>1.Select Optimization</h3>",
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            zero_sales = st.checkbox("Zero Sales", value=True, key="opt_zero_sales")

        st.markdown("---")

        # הוסף כותרת Upload Files
        st.markdown(
            "<h3 style='text-align: center;'>2. Upload Files</h3>",
            unsafe_allow_html=True,
        )

        # Download Template button - CENTERED ON TOP
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # יצירת Template data
            template_gen = TemplateGenerator()
            template_data = template_gen.generate_template()

            # כפתור הורדה אמיתי
            st.download_button(
                label="Download Template",
                data=template_data,
                file_name="template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

        # Space before upload buttons
        st.markdown("")

        # Upload files row - both active uploaders side by side
        col1, col2 = st.columns(2)
        with col1:
            template_file = st.file_uploader(
                "Upload Template", type=["xlsx"], key="template_uploader"
            )
            if template_file:
                st.session_state.template_uploaded = True
                st.success("Template uploaded!")

        with col2:
            bulk_file = st.file_uploader(
                "Bulk 60 Days", type=["xlsx", "csv"], key="bulk_uploader"
            )
            if bulk_file:
                st.session_state.bulk_60_uploaded = True
                st.success("Bulk 60 uploaded!")

        # Disabled buttons row 1
        col1, col2 = st.columns(2)
        with col1:
            st.button(
                "Bulk 7 Days (Coming Soon)",
                disabled=True,
                use_container_width=True,
                help="This feature will be available in a future update",
            )
        with col2:
            st.button(
                "Bulk 30 Days (Coming Soon)",
                disabled=True,
                use_container_width=True,
                help="This feature will be available in a future update",
            )

        # Data Rova button - CENTERED
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.button(
                "Data Rova (Coming Soon)",
                disabled=True,
                use_container_width=True,
                help="This feature will be available in a future update",
            )

        st.markdown("---")

        # Validation Section - Only show if files uploaded
        if st.session_state.get("template_uploaded") and st.session_state.get(
            "bulk_60_uploaded"
        ):
            st.markdown(
                "<h3 style='text-align: center;'>3. Data Validation</h3>",
                unsafe_allow_html=True,
            )

            # Validation status
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.success("Template and Bulk files loaded")
                st.info("Ready for processing!")

                # Process button - עיבוד אמיתי במקום מוק
                if st.button("Process Files", type="primary", use_container_width=True):
                    try:
                        with st.spinner("Processing files..."):
                            # Import required modules
                            import pandas as pd
                            from datetime import datetime
                            from business.bid_optimizations.zero_sales.orchestrator import (
                                ZeroSalesOptimization,
                            )
                            from business.processors.output_formatter import (
                                OutputFormatter,
                            )
                            from data.writers.excel_writer import ExcelWriter
                            from data.readers.excel_reader import ExcelReader

                            # Initialize components
                            excel_reader = ExcelReader()
                            zero_sales = ZeroSalesOptimization()
                            formatter = OutputFormatter()
                            excel_writer = ExcelWriter()

                            # Read template data
                            success, msg, template_data = (
                                excel_reader.read_template_file(template_file.read())
                            )
                            if not success:
                                st.error(f"Template read error: {msg}")
                                st.stop()

                            # Read bulk data
                            success_bulk, msg_bulk, bulk_data = (
                                excel_reader.read_bulk_file(
                                    bulk_file.read(), bulk_file.name
                                )
                            )
                            if not success_bulk:
                                st.error(f"Bulk read error: {msg_bulk}")
                                st.stop()

                            # Validate
                            valid, msg, details = zero_sales.validate(
                                template_data, bulk_data
                            )
                            if not valid:
                                st.error(f"Validation failed: {msg}")
                                st.stop()

                            # Clean
                            cleaned_data, cleaning_details = zero_sales.clean(
                                template_data, bulk_data
                            )

                            # Process
                            optimization_results = zero_sales.process(
                                template_data, cleaned_data
                            )

                            # Format output
                            formatted_results = formatter.format_for_output(
                                optimization_results
                            )

                            # Prepare for Excel
                            final_sheets = formatter.prepare_for_excel(
                                formatted_results
                            )

                            # Create Excel file
                            working_file = excel_writer.write_excel(final_sheets)

                            # Save to session state
                            st.session_state.working_file = working_file
                            st.session_state.processing_complete = True
                            st.session_state.output_stats = (
                                formatter.calculate_statistics(formatted_results)
                            )

                            st.rerun()

                    except Exception as e:
                        st.error(f"Processing error: {str(e)}")
                        import traceback

                        with st.expander("Error details"):
                            st.code(traceback.format_exc())

            st.markdown("---")

        # Output Section - Only show if processing complete
        if st.session_state.get("processing_complete"):
            st.markdown(
                "<h3 style='text-align: center;'>4. Download Output</h3>",
                unsafe_allow_html=True,
            )

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.success("Processing complete!")

                # Show statistics if available
                if stats := st.session_state.get("output_stats"):
                    col_stat1, col_stat2 = st.columns(2)
                    with col_stat1:
                        st.metric("Total Rows", f"{stats.get('total_rows', 0):,}")
                    with col_stat2:
                        st.metric("Rows Modified", f"{stats.get('rows_modified', 0):,}")

                # Download Working File - קובץ אמיתי במקום מוק
                working_file = st.session_state.get("working_file")
                if working_file:
                    from datetime import datetime

                    timestamp = datetime.now().strftime("%Y-%m-%d | %H-%M")
                    st.download_button(
                        "Download Working File",
                        data=working_file,
                        file_name=f"Auto Optimized Bulk | Working | {timestamp}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                    )
                else:
                    st.button(
                        "Download Working File (Process first)",
                        disabled=True,
                        use_container_width=True,
                        help="Process files first to generate output",
                    )

                # Clean File - still disabled
                st.button(
                    "Download Clean File (Coming Soon)",
                    disabled=True,
                    use_container_width=True,
                    help="File generation will be available in a future update",
                )

                # Reset button
                if st.button("Reset", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()
