"""Portfolio Optimizer page - Based on Bid Optimizer layout."""

import streamlit as st
from data.template_generator import TemplateGenerator


class PortfolioOptimizerPage:
    """Main page for Portfolio Optimizer functionality."""

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

            # Use checkbox for selection - Only Empty Portfolios for now
            empty_portfolios = st.checkbox(
                "Empty Portfolios",
                value=False,
                key="portfolio_optimization_selection",
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
                st.success("Bulk 60 uploaded!")
                st.session_state.portfolio_bulk_60_file = uploaded_bulk
                st.session_state.portfolio_bulk_60_uploaded = True

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

            # Process button
            if st.button(
                "Process Files",
                key="btn_process_portfolio",
                use_container_width=True,
                disabled=not files_ready or not empty_portfolios,
            ):
                if files_ready and empty_portfolios:
                    st.session_state.portfolio_processing_started = True
                    st.session_state.portfolio_processing_status = "processing"
                    st.success("Processing Empty Portfolios optimization...")
                    st.rerun()
                else:
                    if not files_ready:
                        st.error("Please upload Bulk 60 file first")
                    if not empty_portfolios:
                        st.error("Please select an optimization")

            # Show processing status
            if st.session_state.get("portfolio_processing_status") == "processing":
                st.info("⏳ Processing... This may take a few seconds.")
                progress_bar = st.progress(0)
                for i in range(100):
                    progress_bar.progress(i + 1)
                
                # Mark as complete after progress
                st.session_state.portfolio_processing_status = "complete"
                st.session_state.portfolio_output_generated = True
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

                if st.button(
                    "Download Working File",
                    key="btn_download_portfolio_working",
                    use_container_width=True,
                ):
                    st.success("Download will start automatically...")

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
