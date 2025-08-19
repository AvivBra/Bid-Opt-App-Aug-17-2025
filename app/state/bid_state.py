"""Bid optimization state management."""

import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional, Tuple
from utils.file_utils import get_dataframe_info, estimate_processing_time


class BidState:
    """Manages state for bid optimization process."""
    
    def __init__(self):
        self.session_keys = {
            'template': {
                'uploaded': 'template_uploaded',
                'data': 'template_data',
                'info': 'template_info'
            },
            'bulk_60': {
                'uploaded': 'bulk_60_uploaded',
                'data': 'bulk_60_data', 
                'info': 'bulk_60_info'
            },
            'bulk_7': {
                'uploaded': 'bulk_7_uploaded',
                'data': 'bulk_7_data',
                'info': 'bulk_7_info'
            },
            'bulk_30': {
                'uploaded': 'bulk_30_uploaded',
                'data': 'bulk_30_data',
                'info': 'bulk_30_info'
            }
        }
    
    def store_file_data(self, file_type: str, data: Any, info: Dict[str, Any]) -> bool:
        """Store file data in session state."""
        
        if file_type not in self.session_keys:
            return False
        
        keys = self.session_keys[file_type]
        
        st.session_state[keys['uploaded']] = True
        st.session_state[keys['data']] = data
        st.session_state[keys['info']] = info
        
        return True
    
    def get_file_data(self, file_type: str) -> Tuple[bool, Optional[Any], Dict[str, Any]]:
        """Get file data from session state."""
        
        if file_type not in self.session_keys:
            return False, None, {}
        
        keys = self.session_keys[file_type]
        
        uploaded = st.session_state.get(keys['uploaded'], False)
        data = st.session_state.get(keys['data'], None)
        info = st.session_state.get(keys['info'], {})
        
        return uploaded, data, info
    
    def clear_file_data(self, file_type: str) -> bool:
        """Clear file data from session state."""
        
        if file_type not in self.session_keys:
            return False
        
        keys = self.session_keys[file_type]
        
        for key in keys.values():
            if key in st.session_state:
                del st.session_state[key]
        
        return True
    
    def clear_all_files(self) -> None:
        """Clear all file data from session state."""
        
        for file_type in self.session_keys:
            self.clear_file_data(file_type)
    
    def has_required_files(self) -> bool:
        """Check if required files for processing are uploaded."""
        
        template_uploaded = st.session_state.get('template_uploaded', False)
        bulk_60_uploaded = st.session_state.get('bulk_60_uploaded', False)
        
        return template_uploaded and bulk_60_uploaded
    
    def get_processing_readiness(self) -> Dict[str, Any]:
        """Get detailed readiness status for processing."""
        
        readiness = {
            'ready': False,
            'template_status': 'missing',
            'bulk_status': 'missing',
            'issues': [],
            'estimated_time': 0
        }
        
        # Check template
        template_uploaded, template_data, template_info = self.get_file_data('template')
        if template_uploaded and template_data:
            readiness['template_status'] = 'ready'
            readiness['template_portfolios'] = template_info.get('portfolios', 0)
        elif template_uploaded:
            readiness['template_status'] = 'error'
            readiness['issues'].append("Template file uploaded but data not available")
        
        # Check bulk file
        bulk_uploaded, bulk_data, bulk_info = self.get_file_data('bulk_60')
        if bulk_uploaded and bulk_data is not None:
            readiness['bulk_status'] = 'ready'
            readiness['bulk_rows'] = bulk_info.get('rows', 0)
            
            # Estimate processing time
            readiness['estimated_time'] = estimate_processing_time(bulk_info.get('rows', 0))
        elif bulk_uploaded:
            readiness['bulk_status'] = 'error'
            readiness['issues'].append("Bulk file uploaded but data not available")
        
        # Overall readiness
        readiness['ready'] = (
            readiness['template_status'] == 'ready' and 
            readiness['bulk_status'] == 'ready' and
            len(readiness['issues']) == 0
        )
        
        return readiness
    
    def get_file_summary(self) -> Dict[str, Dict[str, Any]]:
        """Get summary of all uploaded files."""
        
        summary = {}
        
        for file_type in self.session_keys:
            uploaded, data, info = self.get_file_data(file_type)
            
            if uploaded:
                summary[file_type] = {
                    'uploaded': True,
                    'filename': info.get('filename', 'unknown'),
                    'size_mb': info.get('size_mb', 0),
                    'info': info
                }
                
                # Add data-specific info
                if file_type == 'template' and data:
                    port_values = data.get('Port Values')
                    if port_values is not None:
                        summary[file_type]['portfolios'] = len(port_values)
                        summary[file_type]['data_available'] = True
                    else:
                        summary[file_type]['data_available'] = False
                
                elif file_type.startswith('bulk') and data is not None:
                    summary[file_type]['rows'] = len(data)
                    summary[file_type]['columns'] = len(data.columns)
                    summary[file_type]['data_available'] = True
                else:
                    summary[file_type]['data_available'] = False
            else:
                summary[file_type] = {
                    'uploaded': False,
                    'data_available': False
                }
        
        return summary
    
    def validate_data_compatibility(self) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate that template and bulk data are compatible."""
        
        details = {
            'portfolio_matches': [],
            'portfolio_mismatches': [],
            'zero_sales_candidates': 0,
            'issues': [],
            'warnings': []
        }
        
        # Get data
        template_uploaded, template_data, _ = self.get_file_data('template')
        bulk_uploaded, bulk_data, _ = self.get_file_data('bulk_60')
        
        if not template_uploaded or not bulk_uploaded:
            return False, "Both template and bulk files required", details
        
        if template_data is None or bulk_data is None:
            return False, "File data not available", details
        
        # Get portfolio lists
        try:
            template_portfolios = set(template_data['Port Values']['Portfolio Name'].astype(str).str.strip())
            
            # Find portfolio column in bulk data (case-insensitive)
            portfolio_col = None
            for col in bulk_data.columns:
                if 'portfolio' in col.lower():
                    portfolio_col = col
                    break
            
            if portfolio_col is None:
                details['issues'].append("No portfolio column found in bulk file")
                return False, "Portfolio column not found in bulk file", details
            
            bulk_portfolios = set(bulk_data[portfolio_col].astype(str).str.strip())
            
            # Find matches and mismatches
            details['portfolio_matches'] = list(template_portfolios & bulk_portfolios)
            details['portfolio_mismatches'] = list(template_portfolios - bulk_portfolios)
            
            # Count zero sales candidates if Units column exists
            units_col = None
            for col in bulk_data.columns:
                if 'units' in col.lower():
                    units_col = col
                    break
            
            if units_col:
                try:
                    zero_units = bulk_data[units_col] == 0
                    details['zero_sales_candidates'] = zero_units.sum()
                except Exception:
                    details['warnings'].append("Could not analyze Units column for zero sales")
            
            # Validation results
            if len(details['portfolio_matches']) == 0:
                return False, "No matching portfolios found between template and bulk file", details
            
            if len(details['portfolio_mismatches']) > len(details['portfolio_matches']):
                details['warnings'].append(f"Many template portfolios not found in bulk: {len(details['portfolio_mismatches'])}")
            
            success_msg = f"Data compatible: {len(details['portfolio_matches'])} matching portfolios"
            if details['zero_sales_candidates'] > 0:
                success_msg += f", {details['zero_sales_candidates']} zero sales candidates"
            
            return True, success_msg, details
            
        except Exception as e:
            return False, f"Error validating compatibility: {str(e)}", details
    
    def get_optimization_config(self) -> Dict[str, Any]:
        """Get configuration for optimization processing."""
        
        config = {
            'selected_optimizations': st.session_state.get('selected_optimizations', ['zero_sales']),
            'zero_sales_enabled': 'zero_sales' in st.session_state.get('selected_optimizations', []),
            'processing_mode': 'standard',  # or 'fast', 'thorough'
            'output_format': 'working_file'  # or 'clean_file', 'both'
        }
        
        return config