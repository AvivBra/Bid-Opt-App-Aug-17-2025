"""Campaign Optimizer page - UI only version."""

import streamlit as st
import time
from data.template_generator import TemplateGenerator


class CampaignOptimizerPage:
    """Main page for Campaign Optimizer functionality."""

    def render(self):
        """Render the complete Campaign Optimizer page."""

        # Import and apply custom CSS
        from app.ui.layout import apply_custom_css

        apply_custom_css()

        # Create 6 columns layout: [col1 | col2 | col3 | col4 | col5 | col6]
        col1, col2, col3, col4, col5, col6 = st.columns([1, 7, 1, 1, 6, 2])

        # TITLE IN SECOND COLUMN FROM LEFT
        with col2:
            st.markdown(
                "<h1 style='text-align: left;'>Campaign Optimizer</h1>",
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
            
            testing = st.checkbox(
                "Testing",
                value=False,
                key="testing_checkbox",
            )
            
            testing_pt = st.checkbox(
                "Testing PT",
                value=False,
                key="testing_pt_checkbox",
            )
            
            phrase = st.checkbox(
                "Phrase",
                value=False,
                key="phrase_checkbox",
            )
            
            broad = st.checkbox(
                "Broad",
                value=False,
                key="broad_checkbox",
            )
            
            expanded = st.checkbox(
                "Expanded",
                value=False,
                key="expanded_checkbox",
            )
            
            halloween_testing = st.checkbox(
                "Halloween Testing",
                value=False,
                key="halloween_testing_checkbox",
            )
            
            halloween_phrase = st.checkbox(
                "Halloween Phrase",
                value=False,
                key="halloween_phrase_checkbox",
            )
            
            halloween_broad = st.checkbox(
                "Halloween Broad",
                value=False,
                key="halloween_broad_checkbox",
            )
            
            halloween_expanded = st.checkbox(
                "Halloween Expanded",
                value=False,
                key="halloween_expanded_checkbox",
            )

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
                file_name="campaign_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

            # Upload files - template
            template_file = st.file_uploader(
                "Upload Template", type=["xlsx"], key="campaign_template_uploader"
            )
            if template_file:
                st.session_state.campaign_template_uploaded = True
                st.success("Template uploaded!")

            # Data Rova upload
            data_rova_file = st.file_uploader(
                "Data Rova", type=["xlsx", "csv"], key="data_rova_uploader"
            )
            if data_rova_file:
                st.session_state.data_rova_uploaded = True
                st.success("Data Rova uploaded!")

            # Data Dive upload  
            data_dive_file = st.file_uploader(
                "Data Dive", type=["xlsx", "csv"], key="data_dive_uploader"
            )
            if data_dive_file:
                st.session_state.data_dive_uploaded = True
                st.success("Data Dive uploaded!")

            # Validation Section - Show based on uploaded files
            show_validation = False

            if st.session_state.get("campaign_template_uploaded"):
                show_validation = True

            if show_validation:
                st.markdown(
                    "<h3 style='text-align: left;'>3. Data Validation</h3>",
                    unsafe_allow_html=True,
                )

                # Validation status
                st.success("Template loaded")
                st.info("Ready for processing!")

            # Process button section
            st.markdown(
                """
                <div style='height: 50px;'></div>
                """,
                unsafe_allow_html=True,
            )

            # Process button - enabled only when template is uploaded
            process_enabled = st.session_state.get("campaign_template_uploaded", False)
            
            if st.button(
                "Process Files",
                use_container_width=True,
                disabled=not process_enabled,
                key="campaign_process_button"
            ):
                # Mock processing with progress bar
                with st.spinner("Processing..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.02)  # 2 seconds total
                        progress_bar.progress(i + 1)
                    
                    st.session_state.campaign_processing_complete = True
                    st.success("Processing complete!")

            # Output Files section - only show after processing
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

                # Mock download button (doesn't actually download anything)
                st.button(
                    "Download Campaign Bulk File",
                    use_container_width=True,
                    key="campaign_download_button"
                )