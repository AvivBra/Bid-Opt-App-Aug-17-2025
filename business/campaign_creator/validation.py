"""Validation module for Campaign Creator."""

import pandas as pd
from typing import Dict, List, Tuple, Optional, Set
import streamlit as st


class CampaignValidation:
    """Handles validation logic for campaign creation process."""
    
    def __init__(self):
        """Initialize validation with campaign type mappings."""
        self.keyword_campaigns = {
            "Testing",
            "Phrase",
            "Broad",
            "Halloween Testing",
            "Halloween Phrase",
            "Halloween Broad"
        }
        
        self.pt_campaigns = {
            "Testing PT",
            "Expanded",
            "Halloween Testing PT",
            "Halloween Expanded"
        }
        
        self.cvr_threshold = 0.08
        self.sales_threshold = 0
    
    def validate_files(self, 
                       template_df: pd.DataFrame,
                       data_dive_files: List[pd.DataFrame],
                       data_rova_df: Optional[pd.DataFrame],
                       selected_campaigns: List[str]) -> Tuple[bool, str, Optional[Dict]]:
        """
        Main validation entry point.
        
        Returns:
            Tuple of (is_valid, message, validation_data)
        """
        # Check template structure
        is_valid, msg = self._validate_template_structure(template_df)
        if not is_valid:
            return False, msg, None
        
        # Check if keyword campaigns selected but no keywords data
        needs_keywords = any(camp in self.keyword_campaigns for camp in selected_campaigns)
        needs_pt_only = all(camp in self.pt_campaigns for camp in selected_campaigns)
        
        if not data_dive_files:
            if needs_keywords:
                return False, "Data Dive files required for keyword campaigns", None
            if not needs_pt_only:
                return False, "Data Dive files required", None
        
        # Extract all keywords and ASINs from Data Dive
        keywords, asins = self._extract_targets_from_data_dive(data_dive_files)
        
        # Check Data Rova matching
        missing_keywords = set()
        if needs_keywords and keywords:
            if data_rova_df is None:
                missing_keywords = keywords
            else:
                missing_keywords = self._find_missing_keywords(keywords, data_rova_df)
        
        # Check for qualifying keywords
        if needs_keywords and data_rova_df is not None:
            qualifying_keywords = self._find_qualifying_keywords(keywords, data_rova_df)
            if not qualifying_keywords:
                campaign_names = [c for c in selected_campaigns if c in self.keyword_campaigns]
                msg = f"No keyword meets greater than 0 sales and 8% CVR - can't create campaign {', '.join(campaign_names)}"
                return False, msg, None
        
        validation_data = {
            'keywords': keywords,
            'asins': asins,
            'missing_keywords': missing_keywords,
            'needs_keywords': needs_keywords,
            'needs_pt_only': needs_pt_only
        }
        
        return True, "Validation passed", validation_data
    
    def _validate_template_structure(self, template_df: pd.DataFrame) -> Tuple[bool, str]:
        """Validate template has required columns and data."""
        required_cols = ['My ASIN', 'Product Type', 'Niche']
        
        for col in required_cols:
            if col not in template_df.columns:
                return False, f"Missing required column: {col}"
        
        # Check at least one bid column has data
        bid_cols = [col for col in template_df.columns if 'Bid' in col]
        if not bid_cols:
            return False, "No bid columns found in template"
        
        has_bid_data = False
        for col in bid_cols:
            if template_df[col].notna().any():
                has_bid_data = True
                break
        
        if not has_bid_data:
            return False, "At least one bid column must have data"
        
        return True, "Template structure valid"
    
    def _extract_targets_from_data_dive(self, data_dive_files: List[pd.DataFrame]) -> Tuple[Set[str], Set[str]]:
        """Extract keywords and ASINs from Data Dive files."""
        keywords = set()
        asins = set()
        
        for df in data_dive_files:
            # Extract keywords from Search Terms column (second from left)
            if len(df.columns) >= 2:
                search_terms_col = df.columns[1]
                if 'Search Terms' in search_terms_col or search_terms_col == 'Search Terms':
                    keywords.update(df[search_terms_col].dropna().astype(str).tolist())
            
            # Extract ASINs from column headers starting with B0
            for col in df.columns:
                if col.startswith('B0'):
                    asins.add(col)
        
        return keywords, asins
    
    def _find_missing_keywords(self, keywords: Set[str], data_rova_df: pd.DataFrame) -> Set[str]:
        """Find keywords not present in Data Rova."""
        if 'Keyword' not in data_rova_df.columns:
            return keywords
        
        rova_keywords = set(data_rova_df['Keyword'].dropna().astype(str).tolist())
        return keywords - rova_keywords
    
    def _find_qualifying_keywords(self, keywords: Set[str], data_rova_df: pd.DataFrame) -> Set[str]:
        """Find keywords meeting CVR and sales thresholds."""
        if not all(col in data_rova_df.columns for col in ['Keyword', 'Keyword Conversion', 'Keyword Monthly Sales']):
            return set()
        
        qualifying = set()
        for _, row in data_rova_df.iterrows():
            keyword = str(row.get('Keyword', ''))
            if keyword in keywords:
                try:
                    cvr = float(row.get('Keyword Conversion', 0))
                    sales = float(row.get('Keyword Monthly Sales', 0))
                    if cvr > self.cvr_threshold and sales > self.sales_threshold:
                        qualifying.add(keyword)
                except (ValueError, TypeError):
                    continue
        
        return qualifying
    
    def check_edge_cases(self, validation_data: Dict) -> Tuple[bool, Optional[str]]:
        """Check for edge cases that need special handling."""
        missing_count = len(validation_data.get('missing_keywords', []))
        
        if missing_count > 1000:
            return False, "יותר מ-1000 מילים חסרות - לא ניתן לעבד"
        
        if missing_count > 500:
            return True, f"Warning: {missing_count} keywords missing (>500)"
        
        return True, None