"""Download buttons component for output files."""

import streamlit as st
from typing import Optional
from io import BytesIO


def create_download_button(
    label: str,
    data: Optional[BytesIO] = None,
    file_name: str = "",
    mime_type: str = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    disabled: bool = False,
    help_text: Optional[str] = None,
) -> None:
    """
    Create a download button that handles real file downloads.

    Args:
        label: Button label text
        data: File data as BytesIO
        file_name: Name for downloaded file
        mime_type: MIME type of file
        disabled: Whether button is disabled
        help_text: Help tooltip text
    """
    if disabled or data is None:
        # Show disabled button
        st.button(
            label=label,
            disabled=True,
            help=help_text or "File not available for download",
            use_container_width=True,
        )
    else:
        # Real download button using Streamlit's download_button
        st.download_button(
            label=label,
            data=data,
            file_name=file_name,
            mime=mime_type,
            use_container_width=True,
            help=help_text or f"Download {file_name}",
        )


def render_download_section() -> None:
    """Render the download buttons section."""
    st.markdown("###Download Files")

    col1, col2 = st.columns(2)

    with col1:
        create_working_button()

    with col2:
        create_clean_button()

    # Apply custom styles
    apply_download_styles()


def create_working_button() -> None:
    """Create Working File download button."""
    # In phase 6, this is just a mock disabled button
    working_file = st.session_state.get("working_file")

    if st.session_state.get("processing_status") == "complete":
        # Show as "ready" but still disabled (no real file yet)
        st.button(
            "Download Working File",
            disabled=True,
            help="Working file with helper columns (Feature coming soon)",
            use_container_width=True,
            type="primary",
        )
    else:
        create_download_button(
            label="Download Working File",
            disabled=True,
            help_text="Process files first to generate output",
        )


def create_clean_button() -> None:
    """Create Clean File download button (always disabled)."""
    create_download_button(
        label="Download Clean File",
        disabled=True,
        help_text="Clean file without helper columns",
    )


def apply_download_styles() -> None:
    """Apply standard site button styles (removed custom styles for consistency)."""
    # No custom styles - use site's default button styling for consistency
    pass
