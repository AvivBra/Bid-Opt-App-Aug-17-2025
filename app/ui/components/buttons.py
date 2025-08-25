"""Button components for the application."""

import streamlit as st
from config.constants import BUTTON_WIDTH, BUTTON_HEIGHT


def create_primary_button(
    label: str, key: str = None, disabled: bool = False, help_text: str = None
) -> bool:
    """Create a primary button with standard styling."""

    return st.button(
        label,
        type="primary",
        disabled=disabled,
        use_container_width=True,
        help=help_text,
        key=key,
    )


def create_secondary_button(
    label: str, key: str = None, disabled: bool = False, help_text: str = None
) -> bool:
    """Create a secondary button with standard styling."""

    return st.button(
        label,
        type="secondary",
        disabled=disabled,
        use_container_width=True,
        help=help_text,
        key=key,
    )


def create_download_button(
    label: str, data, filename: str, mime_type: str, key: str = None
) -> bool:
    """Create a download button for files."""

    return st.download_button(
        label=label,
        data=data,
        file_name=filename,
        mime=mime_type,
        use_container_width=True,
        key=key,
    )


def create_icon_button(
    icon: str, label: str, button_type: str = "secondary", **kwargs
) -> bool:
    """Create a button with an icon and label."""

    button_text = f"{icon} {label}"

    if button_type == "primary":
        return create_primary_button(button_text, **kwargs)
    else:
        return create_secondary_button(button_text, **kwargs)


def create_action_buttons():
    """Create common action buttons for the application."""

    col1, col2, col3 = st.columns(3)

    actions = {}

    with col1:
        actions["reset"] = create_secondary_button("Reset", key="reset_button")

    with col2:
        actions["process"] = create_primary_button(
            "Process Files", key="process_button", disabled=not _has_required_files()
        )

    with col3:
        actions["help"] = create_secondary_button("Help", key="help_button")

    return actions


def _has_required_files() -> bool:
    """Check if required files are uploaded."""
    return st.session_state.get("template_uploaded", False) and st.session_state.get(
        "bulk_60_uploaded", False
    )
