# Path: app/ui/components/file_cards.py
"""File status cards component for displaying uploaded files information."""

import streamlit as st
from typing import Dict, Optional, Any
from datetime import datetime
import pandas as pd


def render_file_cards() -> None:
    """
    Render file status cards showing uploaded files information.
    Used in Phase 2 for showing file status in the UI.
    """
    col1, col2 = st.columns(2)

    with col1:
        render_template_card()

    with col2:
        render_bulk_card()


def render_template_card() -> None:
    """Render Template file status card."""
    template_file = st.session_state.get("template_file")

    if template_file:
        render_file_card(
            title="TEMPLATE",
            file_name=template_file.name
            if hasattr(template_file, "name")
            else "Template.xlsx",
            status="uploaded",
            details=get_template_details(),
        )
    else:
        render_empty_card("TEMPLATE", "No template uploaded")


def render_bulk_card() -> None:
    """Render Bulk file status card."""
    # Check which bulk file is uploaded
    bulk_types = ["bulk_7", "bulk_30", "bulk_60"]
    bulk_file = None
    bulk_type = None

    for bt in bulk_types:
        file = st.session_state.get(f"{bt}_file")
        if file:
            bulk_file = file
            bulk_type = bt
            break

    if bulk_file:
        days = bulk_type.split("_")[1] if bulk_type else "60"
        render_file_card(
            title=f"BULK {days} DAYS",
            file_name=bulk_file.name
            if hasattr(bulk_file, "name")
            else f"Bulk_{days}.xlsx",
            status="uploaded",
            details=get_bulk_details(bulk_type),
        )
    else:
        render_empty_card("BULK", "No bulk file uploaded")


def render_file_card(
    title: str, file_name: str, status: str, details: Dict[str, Any]
) -> None:
    """
    Render a single file status card.

    Args:
        title: Card title
        file_name: Name of the uploaded file
        status: Upload status
        details: Additional file details
    """
    # Card container with custom styling
    with st.container():
        st.markdown(
            f"""
            <div style="
                background-color: #1A1A1A;
                border: 1px solid #2D2D2D;
                border-radius: 4px;
                padding: 16px;
                margin-bottom: 16px;
            ">
                <h4 style="
                    color: #E5E5E5;
                    margin: 0 0 8px 0;
                    font-size: 14px;
                    text-transform: uppercase;
                ">{title}</h4>
                <p style="
                    color: #10B981;
                    margin: 0 0 8px 0;
                    font-size: 12px;
                ">{status.upper()}</p>
                <p style="
                    color: #A1A1A1;
                    margin: 0;
                    font-size: 11px;
                    word-break: break-all;
                ">{file_name}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # File details
        if details:
            render_file_details(details)


def render_empty_card(title: str, message: str) -> None:
    """
    Render an empty file card when no file is uploaded.

    Args:
        title: Card title
        message: Empty state message
    """
    with st.container():
        st.markdown(
            f"""
            <div style="
                background-color: #1A1A1A;
                border: 1px solid #2D2D2D;
                border-radius: 4px;
                padding: 16px;
                margin-bottom: 16px;
                min-height: 100px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <h4 style="
                    color: #E5E5E5;
                    margin: 0 0 8px 0;
                    font-size: 14px;
                    text-transform: uppercase;
                ">{title}</h4>
                <p style="
                    color: #666666;
                    margin: 0;
                    font-size: 12px;
                ">{message}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_file_details(details: Dict[str, Any]) -> None:
    """
    Render additional file details below the card.

    Args:
        details: Dictionary of detail labels and values
    """
    details_html = ""
    for label, value in details.items():
        if value is not None:
            details_html += f"""
                <div style="
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 4px;
                    font-size: 11px;
                ">
                    <span style="color: #A1A1A1;">{label}:</span>
                    <span style="color: #E5E5E5;">{value}</span>
                </div>
            """

    if details_html:
        st.markdown(
            f"""
            <div style="
                background-color: #0F0F0F;
                border: 1px solid #2D2D2D;
                border-radius: 4px;
                padding: 8px;
                margin-top: 8px;
                font-size: 11px;
            ">
                {details_html}
            </div>
            """,
            unsafe_allow_html=True,
        )


def get_template_details() -> Dict[str, Any]:
    """
    Get details about the uploaded template file.

    Returns:
        Dictionary with template file details
    """
    template_df = st.session_state.get("template_df")

    if not template_df:
        return {}

    details = {}

    # Check if it's a dict of sheets
    if isinstance(template_df, dict):
        # Count portfolios in Port Values sheet
        if "Port Values" in template_df:
            port_values = template_df["Port Values"]
            if not port_values.empty:
                details["Portfolios"] = len(port_values)

                # Count non-ignored portfolios
                if "Base Bid" in port_values.columns:
                    non_ignored = port_values[
                        port_values["Base Bid"].astype(str).str.upper() != "IGNORE"
                    ]
                    details["Active"] = len(non_ignored)
                    details["Ignored"] = len(port_values) - len(non_ignored)

        # Check for Top ASINs sheet
        if "Top ASINs" in template_df:
            top_asins = template_df["Top ASINs"]
            if not top_asins.empty:
                details["Top ASINs"] = len(top_asins)

        # Check for Delete for 60 sheet
        if "Delete for 60" in template_df:
            delete_for_60 = template_df["Delete for 60"]
            if not delete_for_60.empty:
                keyword_count = (
                    delete_for_60["Keyword ID"].notna().sum()
                    if "Keyword ID" in delete_for_60.columns
                    else 0
                )
                product_count = (
                    delete_for_60["Product Targeting ID"].notna().sum()
                    if "Product Targeting ID" in delete_for_60.columns
                    else 0
                )
                if keyword_count > 0:
                    details["Keywords"] = keyword_count
                if product_count > 0:
                    details["Product Targets"] = product_count

    return details


def get_bulk_details(bulk_type: Optional[str]) -> Dict[str, Any]:
    """
    Get details about the uploaded bulk file.

    Args:
        bulk_type: Type of bulk file (bulk_7, bulk_30, bulk_60)

    Returns:
        Dictionary with bulk file details
    """
    if not bulk_type:
        return {}

    bulk_df = st.session_state.get(f"{bulk_type}_df")

    if bulk_df is None or bulk_df.empty:
        return {}

    details = {"Total Rows": f"{len(bulk_df):,}", "Columns": len(bulk_df.columns)}

    # Count unique portfolios
    if "Portfolio" in bulk_df.columns:
        unique_portfolios = bulk_df["Portfolio"].nunique()
        details["Portfolios"] = unique_portfolios

    # Count rows with Units = 0 (for Zero Sales)
    if "Units" in bulk_df.columns:
        zero_units = len(bulk_df[bulk_df["Units"] == 0])
        if zero_units > 0:
            details["Zero Sales"] = f"{zero_units:,}"

    # File size estimate (rough calculation)
    size_mb = bulk_df.memory_usage(deep=True).sum() / (1024 * 1024)
    details["Size"] = f"{size_mb:.1f} MB"

    return details


def create_file_status_summary() -> str:
    """
    Create a summary text of all uploaded files.

    Returns:
        Summary string for display
    """
    files = []

    if st.session_state.get("template_file"):
        files.append("Template")

    for days in ["7", "30", "60"]:
        if st.session_state.get(f"bulk_{days}_file"):
            files.append(f"Bulk {days}")
            break

    if files:
        return " | ".join(files)
    else:
        return "No files uploaded"


def check_files_ready() -> bool:
    """
    Check if required files are uploaded for processing.

    Returns:
        True if both template and at least one bulk file are uploaded
    """
    has_template = st.session_state.get("template_file") is not None
    has_bulk = any(
        st.session_state.get(f"bulk_{days}_file") is not None
        for days in ["7", "30", "60"]
    )

    return has_template and has_bulk


def clear_file_cards() -> None:
    """Clear all file-related session state."""
    keys_to_clear = [
        "template_file",
        "template_df",
        "bulk_7_file",
        "bulk_7_df",
        "bulk_30_file",
        "bulk_30_df",
        "bulk_60_file",
        "bulk_60_df",
    ]

    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
