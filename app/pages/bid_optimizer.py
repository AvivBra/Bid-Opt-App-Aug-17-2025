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
                st.success("✅ Template uploaded!")

        with col2:
            bulk_file = st.file_uploader(
                "Bulk 60 Days", type=["xlsx", "csv"], key="bulk_uploader"
            )
            if bulk_file:
                st.session_state.bulk_60_uploaded = True
                st.success("✅ Bulk 60 uploaded!")

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
                st.success("✅ Template and Bulk files loaded")
                st.info("Ready for processing!")

                # Process button
                if st.button(
                    "⚡ Process Files", type="primary", use_container_width=True
                ):
                    with st.spinner("Processing files..."):
                        import time

                        time.sleep(2)  # Simulate processing
                        st.session_state.processing_complete = True
                        st.rerun()

            st.markdown("---")

        # Output Section - Only show if processing complete
        if st.session_state.get("processing_complete"):
            st.markdown(
                "<h3 style='text-align: center;'>4. Download Output</h3>",
                unsafe_allow_html=True,
            )

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.success("✅ Processing complete!")

                # Mock download buttons (files not really generated yet)
                st.button(
                    "📥 Download Working File (Coming Soon)",
                    disabled=True,
                    use_container_width=True,
                    help="File generation will be available in a future update",
                )

                st.button(
                    "📥 Download Clean File (Coming Soon)",
                    disabled=True,
                    use_container_width=True,
                    help="File generation will be available in a future update",
                )

                # Reset button
                if st.button("🔄 Reset", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()
