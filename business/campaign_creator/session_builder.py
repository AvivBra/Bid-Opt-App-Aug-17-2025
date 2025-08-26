"""Session state builder for Campaign Creator."""

import pandas as pd
from typing import List, Dict, Set, Optional
import streamlit as st


class SessionBuilder:
    """Builds session state table for campaign processing."""
    
    def __init__(self):
        """Initialize session builder."""
        self.campaign_bid_mapping = {
            'Testing': 'Testing Bid',
            'Testing PT': 'Testing PT Bid',
            'Phrase': 'Phrase Bid',
            'Broad': 'Broad Bid',
            'Expanded': 'Expanded Bid',
            'Halloween Testing': 'Halloween Testing Bid',
            'Halloween Testing PT': 'Halloween Testing PT Bid',
            'Halloween Phrase': 'Halloween Phrase Bid',
            'Halloween Broad': 'Halloween Broad Bid',
            'Halloween Expanded': 'Halloween Expanded Bid'
        }
    
    def build_session_table(self,
                           template_df: pd.DataFrame,
                           targets: Dict[str, Set[str]],
                           selected_campaigns: List[str],
                           keyword_data: Optional[Dict[str, Dict[str, float]]] = None) -> pd.DataFrame:
        """
        Build the main session state table.
        
        Args:
            template_df: Template dataframe
            targets: Dictionary with 'keywords' and 'asins' sets
            selected_campaigns: List of selected campaign types
            keyword_data: Optional keyword data from Data Rova
            
        Returns:
            Session state dataframe
        """
        rows = []
        
        # Get all targets (keywords + ASINs)
        all_targets = targets.get('keywords', set()) | targets.get('asins', set())
        
        # Process each row in template
        for _, template_row in template_df.iterrows():
            asin = template_row.get('My ASIN', '')
            product_type = template_row.get('Product Type', '')
            niche = template_row.get('Niche', '')
            
            # For each selected campaign type
            for campaign_type in selected_campaigns:
                # Get bid value for this campaign type
                bid_column = self.campaign_bid_mapping.get(campaign_type)
                bid_value = None
                
                if bid_column and bid_column in template_row:
                    bid_value = template_row.get(bid_column)
                    # Skip if no bid value for this campaign type
                    if pd.isna(bid_value):
                        continue
                
                # Create row for each target
                for target in all_targets:
                    row = {
                        'target': target,
                        'ASIN': asin,
                        'Product Type': product_type,
                        'Niche': niche,
                        'Campaign type': campaign_type,
                        'Bid': bid_value,
                        'kw cvr': None,
                        'kw sales': None
                    }
                    
                    # Add keyword data if available and target is a keyword
                    if keyword_data and target in keyword_data:
                        row['kw cvr'] = keyword_data[target].get('cvr')
                        row['kw sales'] = keyword_data[target].get('sales')
                    
                    rows.append(row)
        
        # Create dataframe
        df = pd.DataFrame(rows)
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        return df
    
    def update_with_rova_data(self, 
                            session_df: pd.DataFrame,
                            keyword_data: Dict[str, Dict[str, float]]) -> pd.DataFrame:
        """
        Update session table with Data Rova information.
        
        Args:
            session_df: Existing session dataframe
            keyword_data: Keyword data from Data Rova
            
        Returns:
            Updated dataframe
        """
        # Update each row where target matches a keyword in Data Rova
        for idx, row in session_df.iterrows():
            target = row['target']
            if target in keyword_data:
                session_df.at[idx, 'kw cvr'] = keyword_data[target].get('cvr')
                session_df.at[idx, 'kw sales'] = keyword_data[target].get('sales')
        
        return session_df
    
    def filter_for_processing(self,
                             session_df: pd.DataFrame,
                             selected_campaigns: List[str]) -> pd.DataFrame:
        """
        Filter session table for final processing based on campaign requirements.
        
        Args:
            session_df: Session dataframe
            selected_campaigns: List of selected campaign types
            
        Returns:
            Filtered dataframe ready for processing
        """
        keyword_campaigns = {
            'Testing', 'Phrase', 'Broad',
            'Halloween Testing', 'Halloween Phrase', 'Halloween Broad'
        }
        
        pt_campaigns = {
            'Testing PT', 'Expanded',
            'Halloween Testing PT', 'Halloween Expanded'
        }
        
        filtered_rows = []
        
        for _, row in session_df.iterrows():
            campaign_type = row['Campaign type']
            target = row['target']
            
            # Check if target is an ASIN (starts with B0)
            is_asin = str(target).startswith('B0')
            
            if campaign_type in pt_campaigns:
                # PT campaigns - include all ASINs, no keywords needed
                if is_asin:
                    filtered_rows.append(row)
            elif campaign_type in keyword_campaigns:
                # Keyword campaigns - only include if has Data Rova info
                if not is_asin and row['kw cvr'] is not None and row['kw sales'] is not None:
                    # Check thresholds
                    if row['kw cvr'] > 0.08 and row['kw sales'] > 0:
                        filtered_rows.append(row)
            
            # Always include ASINs for any campaign type
            if is_asin:
                filtered_rows.append(row)
        
        if not filtered_rows:
            return pd.DataFrame()
        
        result_df = pd.DataFrame(filtered_rows)
        # Remove duplicates that might have been added
        result_df = result_df.drop_duplicates()
        
        return result_df
    
    def save_to_session_state(self, df: pd.DataFrame):
        """Save dataframe to Streamlit session state."""
        st.session_state.campaign_session_table = df
        st.session_state.campaign_session_table_created = True
    
    def get_from_session_state(self) -> Optional[pd.DataFrame]:
        """Get dataframe from Streamlit session state."""
        if 'campaign_session_table' in st.session_state:
            return st.session_state.campaign_session_table
        return None