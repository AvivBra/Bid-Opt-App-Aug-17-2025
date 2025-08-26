"""Checklist component for optimization selection."""

import streamlit as st
from typing import List, Dict


class OptimizationChecklist:
    """Component for displaying and managing optimization selections."""

    # Define all optimizations with their status
    OPTIMIZATIONS = [
        {
            "name": "Zero Sales",
            "enabled": True,
            "description": "Optimize bids for products with zero sales",
            "bulk_type": "60",
        },
        {
            "name": "Bids 30 Days",
            "enabled": True,
            "description": "Optimize bids for products with sales in last 30 days",
            "bulk_type": "30",
        },
        {
            "name": "Bids 60 Days",
            "enabled": True,
            "description": "Optimize bids for products with sales in last 60 days",
            "bulk_type": "60",
        },
        {"name": "Low Impressions", "enabled": False, "description": "Coming Soon"},
        {"name": "High ACOS", "enabled": False, "description": "Coming Soon"},
        {"name": "Top Performers", "enabled": False, "description": "Coming Soon"},
        {"name": "Negative Keywords", "enabled": False, "description": "Coming Soon"},
        {"name": "Bid Adjustments", "enabled": False, "description": "Coming Soon"},
        {"name": "Budget Optimization", "enabled": False, "description": "Coming Soon"},
        {
            "name": "Placement Optimization",
            "enabled": False,
            "description": "Coming Soon",
        },
        {"name": "Dayparting", "enabled": False, "description": "Coming Soon"},
        {
            "name": "Search Term Optimization",
            "enabled": False,
            "description": "Coming Soon",
        },
        {"name": "Product Targeting", "enabled": False, "description": "Coming Soon"},
        {"name": "Campaign Structure", "enabled": False, "description": "Coming Soon"},
        {"name": "Keyword Harvesting", "enabled": False, "description": "Coming Soon"},
        {"name": "Bid Rules", "enabled": False, "description": "Coming Soon"},
    ]

    def __init__(self):
        """Initialize the checklist component."""
        self._init_state()

    def _init_state(self):
        """Initialize session state for selections."""
        if "selected_optimizations" not in st.session_state:
            st.session_state.selected_optimizations = []
        if "active_bulk_type" not in st.session_state:
            st.session_state.active_bulk_type = None

    def render(self) -> List[str]:
        """
        Render the optimization checklist with single selection only.

        When one optimization is selected, all others become disabled.
        Returns:
            List of selected optimization names (max 1)
        """
        selected = []

        # Check if any optimization is currently selected
        currently_selected = st.session_state.get("selected_optimizations", [])
        has_selection = len(currently_selected) > 0

        # Create two columns for better layout
        col1, col2 = st.columns(2)

        for i, opt in enumerate(self.OPTIMIZATIONS):
            # Determine which column to use
            col = col1 if i % 2 == 0 else col2

            with col:
                if opt["enabled"]:
                    # Check if this optimization is selected
                    is_selected = opt["name"] in currently_selected

                    # Disable if another optimization is selected
                    is_disabled = has_selection and not is_selected

                    # Render checkbox
                    if is_disabled:
                        # Show as disabled
                        st.checkbox(
                            opt["name"],
                            key=f"opt_{opt['name'].replace(' ', '_')}_disabled",
                            value=False,
                            disabled=True,
                            help=f"{opt.get('description', '')} - Deselect current optimization first",
                        )
                    else:
                        # Active checkbox
                        checkbox_value = st.checkbox(
                            opt["name"],
                            key=f"opt_{opt['name'].replace(' ', '_')}",
                            value=is_selected,
                            help=opt.get("description", ""),
                        )

                        if checkbox_value:
                            selected.append(opt["name"])

                            # Set active bulk type
                            if "bulk_type" in opt:
                                st.session_state.active_bulk_type = opt["bulk_type"]
                else:
                    # Coming Soon checkbox (always disabled)
                    st.checkbox(
                        f"{opt['name']} (Coming Soon)",
                        key=f"opt_{opt['name'].replace(' ', '_')}_disabled",
                        disabled=True,
                        help=opt["description"],
                    )

        # Update session state
        st.session_state.selected_optimizations = selected

        # Clear bulk data if optimization changed
        if selected != currently_selected:
            self._handle_optimization_change(selected)

        return selected

    def _handle_optimization_change(self, new_selection: List[str]):
        """
        Handle optimization change - clear bulk data and update bulk type.

        Args:
            new_selection: New list of selected optimizations
        """
        # Clear bulk data from session
        if "bulk_60_df" in st.session_state:
            del st.session_state.bulk_60_df
        if "bulk_30_df" in st.session_state:
            del st.session_state.bulk_30_df
        if "bulk_60_uploaded" in st.session_state:
            st.session_state.bulk_60_uploaded = False
        if "bulk_30_uploaded" in st.session_state:
            st.session_state.bulk_30_uploaded = False

        # Update active bulk type
        if new_selection:
            opt_info = self.get_optimization_info(new_selection[0])
            if opt_info and "bulk_type" in opt_info:
                st.session_state.active_bulk_type = opt_info["bulk_type"]
        else:
            st.session_state.active_bulk_type = None

        # Reset validation
        if "validation_passed" in st.session_state:
            st.session_state.validation_passed = False

    def get_selected(self) -> List[str]:
        """Get currently selected optimizations."""
        return st.session_state.get("selected_optimizations", [])

    def set_selected(self, optimizations: List[str]):
        """Set selected optimizations."""
        # Ensure only one selection
        if len(optimizations) > 1:
            optimizations = optimizations[:1]
        st.session_state.selected_optimizations = optimizations

    def clear_all(self):
        """Clear all selections."""
        st.session_state.selected_optimizations = []
        st.session_state.active_bulk_type = None

    def select_all_enabled(self):
        """Not applicable - only one selection allowed."""
        pass

    def is_any_selected(self) -> bool:
        """Check if any optimization is selected."""
        return len(st.session_state.get("selected_optimizations", [])) > 0

    @staticmethod
    def get_optimization_info(name: str) -> Dict:
        """Get information about a specific optimization."""
        for opt in OptimizationChecklist.OPTIMIZATIONS:
            if opt["name"] == name:
                return opt
        return None

    @staticmethod
    def get_active_bulk_type() -> str:
        """Get the bulk type for active optimization."""
        return st.session_state.get("active_bulk_type", None)


# Standalone function for backward compatibility
def render_optimization_checklist() -> List[str]:
    """
    Render the optimization checklist.

    Returns:
        List of selected optimization names
    """
    checklist = OptimizationChecklist()
    return checklist.render()


# Additional helper functions
def get_selected_optimizations() -> List[str]:
    """Get currently selected optimizations."""
    return st.session_state.get("selected_optimizations", [])


def set_selected_optimizations(optimizations: List[str]):
    """Set selected optimizations."""
    # Ensure only one selection
    if len(optimizations) > 1:
        optimizations = optimizations[:1]
    st.session_state.selected_optimizations = optimizations


def is_any_optimization_selected() -> bool:
    """Check if any optimization is selected."""
    return len(st.session_state.get("selected_optimizations", [])) > 0


def clear_optimization_selections():
    """Clear all optimization selections."""
    st.session_state.selected_optimizations = []
    st.session_state.active_bulk_type = None


def get_active_bulk_type() -> str:
    """Get the bulk type for active optimization."""
    return st.session_state.get("active_bulk_type", None)
