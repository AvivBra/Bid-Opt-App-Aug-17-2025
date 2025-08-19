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

    def render(self) -> List[str]:
        """
        Render the optimization checklist.

        Returns:
            List of selected optimization names
        """
        selected = []

        # Create two columns for better layout
        col1, col2 = st.columns(2)

        for i, opt in enumerate(self.OPTIMIZATIONS):
            # Determine which column to use
            col = col1 if i % 2 == 0 else col2

            with col:
                if opt["enabled"]:
                    # Enabled checkbox
                    is_selected = st.checkbox(
                        opt["name"],
                        key=f"opt_{opt['name'].replace(' ', '_')}",
                        help=opt.get("description", ""),
                    )
                    if is_selected:
                        selected.append(opt["name"])
                else:
                    # Disabled checkbox with "Coming Soon"
                    st.checkbox(
                        f"{opt['name']} (Coming Soon)",
                        key=f"opt_{opt['name'].replace(' ', '_')}_disabled",
                        disabled=True,
                        help=opt["description"],
                    )

        # Update session state
        st.session_state.selected_optimizations = selected

        return selected

    def get_selected(self) -> List[str]:
        """Get currently selected optimizations."""
        return st.session_state.get("selected_optimizations", [])

    def set_selected(self, optimizations: List[str]):
        """Set selected optimizations."""
        st.session_state.selected_optimizations = optimizations

    def clear_all(self):
        """Clear all selections."""
        st.session_state.selected_optimizations = []

    def select_all_enabled(self):
        """Select all enabled optimizations."""
        enabled = [opt["name"] for opt in self.OPTIMIZATIONS if opt["enabled"]]
        st.session_state.selected_optimizations = enabled

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
    st.session_state.selected_optimizations = optimizations


def is_any_optimization_selected() -> bool:
    """Check if any optimization is selected."""
    return len(st.session_state.get("selected_optimizations", [])) > 0


def clear_optimization_selections():
    """Clear all optimization selections."""
    st.session_state.selected_optimizations = []
