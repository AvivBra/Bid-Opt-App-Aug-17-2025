"""Validation section UI component."""

import streamlit as st
from data.validators.portfolio_validator import PortfolioValidator
from app.state.bid_state import BidState
from app.ui.layout import create_section_header, create_status_message
from app.ui.components.buttons import create_primary_button


class ValidationSection:
    """Handles data validation UI and processing."""
    
    def __init__(self):
        self.portfolio_validator = PortfolioValidator()
        self.bid_state = BidState()
    
    def render(self):
        """Render the validation section."""
        
        create_section_header("Data Validation", "✓")
        
        # Check if files are ready for validation
        if not self.bid_state.has_required_files():
            create_status_message("Upload Template and Bulk files to begin validation", "info")
            return
        
        # Get file data
        template_uploaded, template_data, template_info = self.bid_state.get_file_data('template')
        bulk_uploaded, bulk_data, bulk_info = self.bid_state.get_file_data('bulk_60')
        
        if not template_data or bulk_data is None:
            create_status_message("File data not available - please re-upload files", "error")
            return
        
        # File status summary
        self._render_file_status(template_info, bulk_info)
        
        st.markdown("---")
        
        # Portfolio validation
        self._render_portfolio_validation(template_data, bulk_data)
        
        st.markdown("---")
        
        # Optimization selection
        self._render_optimization_selection()
        
        st.markdown("---")
        
        # Processing readiness
        self._render_processing_readiness()
    
    def _render_file_status(self, template_info: dict, bulk_info: dict):
        """Render file status information."""
        
        st.markdown("#### 📄 File Status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Template File:**")
            create_status_message(
                f"✓ {template_info.get('portfolios', 0)} portfolios loaded", 
                "success"
            )
            st.caption(f"File: {template_info.get('filename', 'Unknown')}")
            st.caption(f"Size: {template_info.get('size_mb', 0):.1f} MB")
        
        with col2:
            st.markdown("**Bulk File:**")
            create_status_message(
                f"✓ {bulk_info.get('rows', 0):,} rows loaded", 
                "success"
            )
            st.caption(f"File: {bulk_info.get('filename', 'Unknown')}")
            st.caption(f"Size: {bulk_info.get('size_mb', 0):.1f} MB")
            
            # Show zero sales readiness
            if bulk_info.get('zero_sales_ready', False):
                st.success("🎯 Ready for Zero Sales optimization")
            else:
                st.warning("⚠️ May not be suitable for Zero Sales")
    
    def _render_portfolio_validation(self, template_data: dict, bulk_data):
        """Render portfolio matching validation."""
        
        st.markdown("#### 🎯 Portfolio Matching")
        
        # Run validation
        with st.spinner("Validating portfolio matching..."):
            valid, msg, details = self.portfolio_validator.validate_portfolio_matching(
                template_data, bulk_data
            )
        
        # Display results
        if valid:
            create_status_message(msg, "success")
        else:
            create_status_message(msg, "error")
            return
        
        # Show matching statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Matching Portfolios", 
                len(details.get('matching_portfolios', [])),
                help="Portfolios found in both template and bulk files"
            )
        
        with col2:
            st.metric(
                "Missing in Bulk", 
                len(details.get('missing_in_bulk', [])),
                help="Template portfolios not found in bulk file"
            )
        
        with col3:
            st.metric(
                "Zero Sales Candidates", 
                details.get('zero_sales_candidates', 0),
                help="Rows with 0 units (eligible for Zero Sales optimization)"
            )
        
        # Show warnings
        if details.get('warnings'):
            for warning in details['warnings']:
                st.warning(f"⚠️ {warning}")
        
        # Expandable details
        with st.expander("📊 Detailed Portfolio Analysis", expanded=False):
            self._render_portfolio_details(details)
        
        # Store validation results
        st.session_state.validation_complete = True
        st.session_state.validation_results = details
    
    def _render_portfolio_details(self, details: dict):
        """Render detailed portfolio analysis."""
        
        tab1, tab2, tab3 = st.tabs(["Matching", "Missing", "Summary"])
        
        with tab1:
            st.markdown("**Portfolios found in both files:**")
            matching = details.get('matching_portfolios', [])
            if matching:
                for portfolio in matching[:10]:  # Show first 10
                    st.write(f"✓ {portfolio}")
                if len(matching) > 10:
                    st.caption(f"... and {len(matching) - 10} more portfolios")
            else:
                st.info("No matching portfolios found")
        
        with tab2:
            st.markdown("**Template portfolios not found in bulk file:**")
            missing = details.get('missing_in_bulk', [])
            if missing:
                for portfolio in missing[:10]:  # Show first 10
                    st.write(f"❌ {portfolio}")
                if len(missing) > 10:
                    st.caption(f"... and {len(missing) - 10} more portfolios")
            else:
                st.success("All template portfolios found in bulk file!")
        
        with tab3:
            st.markdown("**Validation Summary:**")
            st.write(f"• Template portfolios: {len(details.get('template_portfolios', []))}")
            st.write(f"• Bulk portfolios: {len(details.get('bulk_portfolios', []))}")
            st.write(f"• Excluded portfolios: {len(details.get('excluded_portfolios', []))}")
            st.write(f"• Processing ready: {'Yes' if details.get('processing_ready') else 'No'}")
    
    def _render_optimization_selection(self):
        """Render optimization selection checkboxes."""
        
        st.markdown("#### ⚙️ Optimization Selection")
        
        # Get current selection
        selected = st.session_state.get('selected_optimizations', ['zero_sales'])
        
        # Zero Sales (only active optimization)
        zero_sales_enabled = st.checkbox(
            "Zero Sales Optimization", 
            value='zero_sales' in selected,
            help="Optimize bids for products with 0 units sold",
            key="zero_sales_checkbox"
        )
        
        # Other optimizations (disabled for Phase 1)
        other_optimizations = [
            ("Portfolio Bid Optimization", "Coming in Phase 2"),
            ("Budget Optimization", "Coming in Phase 2"),
            ("Keyword Optimization", "Coming in Phase 2"),
            ("ASIN Targeting", "Coming in Phase 2")
        ]
        
        for opt_name, help_text in other_optimizations:
            st.checkbox(
                opt_name,
                value=False,
                disabled=True,
                help=help_text,
                key=f"{opt_name.lower().replace(' ', '_')}_checkbox"
            )
        
        # Update session state
        new_selection = []
        if zero_sales_enabled:
            new_selection.append('zero_sales')
        
        st.session_state.selected_optimizations = new_selection
        
        # Show selection summary
        if new_selection:
            st.success(f"✓ Selected: {len(new_selection)} optimization(s)")
        else:
            st.warning("⚠️ No optimizations selected")
    
    def _render_processing_readiness(self):
        """Render processing readiness status."""
        
        st.markdown("#### 🚀 Processing Readiness")
        
        readiness = self.bid_state.get_processing_readiness()
        
        # Overall status
        if readiness['ready']:
            create_status_message("✅ Ready to process files", "success")
            
            # Show processing estimate
            if readiness.get('estimated_time', 0) > 0:
                st.info(f"⏱️ Estimated processing time: {readiness['estimated_time']} seconds")
        else:
            create_status_message("❌ Not ready for processing", "error")
            
            # Show issues
            for issue in readiness.get('issues', []):
                st.error(f"• {issue}")
        
        # Processing summary
        with st.expander("📋 Processing Summary", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Template Status:**", readiness['template_status'].title())
                if readiness.get('template_portfolios'):
                    st.write("**Portfolios:**", readiness['template_portfolios'])
            
            with col2:
                st.write("**Bulk Status:**", readiness['bulk_status'].title())
                if readiness.get('bulk_rows'):
                    st.write("**Rows:**", f"{readiness['bulk_rows']:,}")
        
        # Store readiness in session
        st.session_state.processing_ready = readiness['ready']
    
    def get_validation_status(self) -> dict:
        """Get current validation status."""
        return {
            'complete': st.session_state.get('validation_complete', False),
            'results': st.session_state.get('validation_results', {}),
            'ready': st.session_state.get('processing_ready', False)
        }