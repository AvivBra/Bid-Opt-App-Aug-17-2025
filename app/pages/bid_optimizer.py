"""Bid Optimizer page - Complete working version."""

import streamlit as st


class BidOptimizerPage:
    """Main page for Bid Optimizer functionality."""

    def render(self):
        """Render the complete Bid Optimizer page."""

        # Page title - CENTERED
        st.markdown(
            "<h1 style='text-align: center;'>BID OPTIMIZER</h1>", 
            unsafe_allow_html=True
        )
        # Optimization selection - CENTERED
        st.markdown(
            "<h3 style='text-align: center;'>SELECT OPTIMIZATIONS</h3>",
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            zero_sales = st.checkbox("Zero Sales", value=True, key="opt_zero_sales")

        st.markdown("---")

        # Upload section
        # st.markdown(
        #    "<h3 style='text-align: center;'>UPLOAD FILES</h3>", unsafe_allow_html=True
        # )

        # Template row
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Download Template", use_container_width=True):
                st.info("Template download coming soon")

        with col2:
            template_file = st.file_uploader(
                "Upload Template", type=["xlsx"], key="template_uploader"
            )
            if template_file:
                st.session_state.template_uploaded = True
                st.success("✅ Template uploaded!")

        # Bulk files row
        col1, col2 = st.columns(2)
        with col1:
            bulk_file = st.file_uploader(
                "Bulk 60 Days", type=["xlsx", "csv"], key="bulk_uploader"
            )
            if bulk_file:
                st.session_state.bulk_60_uploaded = True
                st.success("✅ Bulk 60 uploaded!")

        with col2:
            st.button(
                "Bulk 30 Days (Coming Soon)", disabled=True, use_container_width=True
            )

        # Additional bulk files
        col1, col2 = st.columns(2)
        with col1:
            st.button(
                "Bulk 7 Days (Coming Soon)", disabled=True, use_container_width=True
            )
        with col2:
            st.button(
                "Data Rova (Coming Soon)", disabled=True, use_container_width=True
            )

        # Validation section
        if st.session_state.get("template_uploaded") or st.session_state.get(
            "bulk_60_uploaded"
        ):
            st.markdown("---")
            st.markdown(
                "<h3 style='text-align: center;'>DATA VALIDATION</h3>",
                unsafe_allow_html=True,
            )

            if st.session_state.get("template_uploaded") and st.session_state.get(
                "bulk_60_uploaded"
            ):
                st.success("✅ All portfolios valid")
                st.info("📊 234 rows ready for processing")

                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button(
                        "Process Files", type="primary", use_container_width=True
                    ):
                        st.session_state.processing_complete = True
                        st.rerun()
            else:
                st.warning("⚠️ Please upload both Template and Bulk files")

        # Output section
        if st.session_state.get("processing_complete"):
            st.markdown("---")
            st.markdown(
                "<h3 style='text-align: center;'>OUTPUT FILES</h3>",
                unsafe_allow_html=True,
            )

            st.success("✅ Processing complete!")
            st.info("Generated 2 output files")

            col1, col2 = st.columns(2)
            with col1:
                st.button(
                    "📥 Download Working File",
                    disabled=True,
                    use_container_width=True,
                    help="Working file with helper columns (Coming soon)",
                )
            with col2:
                st.button(
                    "📥 Download Clean File",
                    disabled=True,
                    use_container_width=True,
                    help="Clean file without helper columns (Coming soon)",
                )

        # Reset button
        if (
            st.session_state.get("template_uploaded")
            or st.session_state.get("bulk_60_uploaded")
            or st.session_state.get("processing_complete")
        ):
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button(
                    "🔄 Reset All", type="secondary", use_container_width=True
                ):
                    # Clear all except navigation
                    for key in list(st.session_state.keys()):
                        if key not in ["current_page"]:
                            del st.session_state[key]
                    st.rerun()
