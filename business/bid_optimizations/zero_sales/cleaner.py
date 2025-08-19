"""Zero Sales optimization data cleaning."""

import pandas as pd
from typing import Dict, Any, Tuple, List
import logging
from business.common.portfolio_filter import PortfolioFilter


class ZeroSalesCleaner:
    """Cleans data for Zero Sales optimization processing."""
    
    def __init__(self):
        self.logger = logging.getLogger("optimization.zero_sales.cleaner")
        self.portfolio_filter = PortfolioFilter()
    
    def clean(self, template_data: Dict[str, pd.DataFrame], bulk_data: pd.DataFrame, column_mapping: Dict[str, str]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Clean and filter data for Zero Sales processing.
        
        Args:
            template_data: Template data dictionary
            bulk_data: Raw bulk data DataFrame
            column_mapping: Column name mappings
            
        Returns:
            Tuple of (cleaned_dataframe, cleaning_details)
        """
        
        cleaning_details = {
            'original_rows': len(bulk_data),
            'final_rows': 0,
            'cleaning_steps': [],
            'filter_details': {},
            'data_quality': {},
            'warnings': []
        }
        
        self.logger.info(f"Starting Zero Sales data cleaning: {len(bulk_data)} rows")
        
        # Step 1: Basic data cleaning
        current_df, basic_details = self._basic_data_cleaning(bulk_data, column_mapping)
        cleaning_details['cleaning_steps'].append(('basic_cleaning', basic_details))
        
        # Step 2: Apply portfolio filters
        portfolio_col = column_mapping.get('portfolio')
        units_col = column_mapping.get('units')
        
        if portfolio_col and units_col:
            current_df, filter_details = self.portfolio_filter.apply_all_filters(
                current_df, portfolio_col, units_col, template_data
            )
            cleaning_details['filter_details'] = filter_details
            cleaning_details['cleaning_steps'].append(('portfolio_filtering', filter_details))
        
        # Step 3: Data quality checks
        quality_details = self._perform_quality_checks(current_df, column_mapping)
        cleaning_details['data_quality'] = quality_details
        cleaning_details['cleaning_steps'].append(('quality_checks', quality_details))
        
        # Step 4: Final data preparation
        current_df, prep_details = self._prepare_for_processing(current_df, column_mapping, template_data)
        cleaning_details['cleaning_steps'].append(('data_preparation', prep_details))
        
        # Final statistics
        cleaning_details['final_rows'] = len(current_df)
        
        success_msg = f"Data cleaning complete: {cleaning_details['original_rows']} -> {cleaning_details['final_rows']} rows"
        self.logger.info(success_msg)
        
        return current_df, cleaning_details
    
    def _basic_data_cleaning(self, df: pd.DataFrame, column_mapping: Dict[str, str]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Perform basic data cleaning operations."""
        
        details = {
            'empty_rows_removed': 0,
            'duplicate_rows_removed': 0,
            'invalid_data_cleaned': 0
        }
        
        current_df = df.copy()
        
        # Remove completely empty rows
        empty_mask = current_df.isnull().all(axis=1)
        empty_count = empty_mask.sum()
        if empty_count > 0:
            current_df = current_df[~empty_mask]
            details['empty_rows_removed'] = empty_count
            self.logger.info(f"Removed {empty_count} empty rows")
        
        # Remove duplicate rows
        initial_count = len(current_df)
        current_df = current_df.drop_duplicates()
        duplicate_count = initial_count - len(current_df)
        if duplicate_count > 0:
            details['duplicate_rows_removed'] = duplicate_count
            self.logger.info(f"Removed {duplicate_count} duplicate rows")
        
        # Clean critical columns
        portfolio_col = column_mapping.get('portfolio')
        if portfolio_col and portfolio_col in current_df.columns:
            # Clean portfolio names
            original_count = len(current_df)
            current_df[portfolio_col] = current_df[portfolio_col].astype(str).str.strip()
            current_df = current_df[current_df[portfolio_col] != '']
            current_df = current_df[current_df[portfolio_col] != 'nan']
            cleaned_count = original_count - len(current_df)
            if cleaned_count > 0:
                details['invalid_data_cleaned'] += cleaned_count
        
        units_col = column_mapping.get('units')
        if units_col and units_col in current_df.columns:
            # Ensure units column is numeric
            current_df[units_col] = pd.to_numeric(current_df[units_col], errors='coerce')
        
        bid_col = column_mapping.get('bid')
        if bid_col and bid_col in current_df.columns:
            # Ensure bid column is numeric
            current_df[bid_col] = pd.to_numeric(current_df[bid_col], errors='coerce')
        
        return current_df, details
    
    def _perform_quality_checks(self, df: pd.DataFrame, column_mapping: Dict[str, str]) -> Dict[str, Any]:
        """Perform data quality checks on cleaned data."""
        
        quality = {
            'total_rows': len(df),
            'portfolio_quality': {},
            'units_quality': {},
            'bid_quality': {},
            'overall_score': 0.0
        }
        
        if df.empty:
            return quality
        
        # Portfolio column quality
        portfolio_col = column_mapping.get('portfolio')
        if portfolio_col and portfolio_col in df.columns:
            null_count = df[portfolio_col].isnull().sum()
            empty_count = (df[portfolio_col].astype(str).str.strip() == '').sum()
            unique_count = df[portfolio_col].nunique()
            
            quality['portfolio_quality'] = {
                'null_count': null_count,
                'empty_count': empty_count,
                'unique_portfolios': unique_count,
                'quality_score': 1.0 - (null_count + empty_count) / len(df)
            }
        
        # Units column quality
        units_col = column_mapping.get('units')
        if units_col and units_col in df.columns:
            null_count = df[units_col].isnull().sum()
            zero_count = (df[units_col] == 0).sum()
            negative_count = (df[units_col] < 0).sum()
            
            quality['units_quality'] = {
                'null_count': null_count,
                'zero_count': zero_count,
                'negative_count': negative_count,
                'quality_score': 1.0 - null_count / len(df)
            }
        
        # Bid column quality
        bid_col = column_mapping.get('bid')
        if bid_col and bid_col in df.columns:
            null_count = df[bid_col].isnull().sum()
            zero_count = (df[bid_col] == 0).sum()
            negative_count = (df[bid_col] < 0).sum()
            
            quality['bid_quality'] = {
                'null_count': null_count,
                'zero_count': zero_count,
                'negative_count': negative_count,
                'quality_score': 1.0 - null_count / len(df)
            }
        
        # Calculate overall quality score
        scores = []
        for key in ['portfolio_quality', 'units_quality', 'bid_quality']:
            if quality[key] and 'quality_score' in quality[key]:
                scores.append(quality[key]['quality_score'])
        
        if scores:
            quality['overall_score'] = sum(scores) / len(scores)
        
        return quality
    
    def _prepare_for_processing(
        self, 
        df: pd.DataFrame, 
        column_mapping: Dict[str, str], 
        template_data: Dict[str, pd.DataFrame]
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Prepare data for final processing."""
        
        prep_details = {
            'portfolios_mapped': 0,
            'bid_data_added': 0,
            'helper_columns_added': [],
            'processing_ready': False
        }
        
        if df.empty:
            return df, prep_details
        
        current_df = df.copy()
        
        # Add template data mapping
        template_mapping, mapping_count = self._create_template_mapping(current_df, column_mapping, template_data)
        if template_mapping is not None:
            # Merge with template data
            portfolio_col = column_mapping.get('portfolio')
            if portfolio_col:
                current_df = current_df.merge(
                    template_mapping, 
                    left_on=portfolio_col, 
                    right_on='Portfolio Name', 
                    how='left',
                    suffixes=('', '_template')
                )
                prep_details['portfolios_mapped'] = mapping_count
                prep_details['helper_columns_added'].extend(['Base Bid', 'Target CPA'])
        
        # Add helper columns for processing
        helper_cols = self._add_helper_columns(current_df, column_mapping)
        prep_details['helper_columns_added'].extend(helper_cols)
        
        # Validate readiness for processing
        portfolio_col = column_mapping.get('portfolio')
        units_col = column_mapping.get('units')
        bid_col = column_mapping.get('bid')
        
        if all(col in current_df.columns for col in [portfolio_col, units_col, bid_col]):
            valid_rows = (
                current_df[portfolio_col].notna() &
                current_df[units_col].notna() &
                current_df[bid_col].notna()
            )
            prep_details['processing_ready'] = valid_rows.sum() > 0
        
        return current_df, prep_details
    
    def _create_template_mapping(
        self, 
        df: pd.DataFrame, 
        column_mapping: Dict[str, str], 
        template_data: Dict[str, pd.DataFrame]
    ) -> Tuple[pd.DataFrame, int]:
        """Create mapping DataFrame from template data."""
        
        try:
            port_values = template_data.get('Port Values')
            if port_values is None or port_values.empty:
                return None, 0
            
            # Select relevant columns
            mapping_cols = ['Portfolio Name', 'Base Bid', 'Target CPA']
            template_mapping = port_values[mapping_cols].copy()
            
            # Clean the mapping data
            template_mapping['Portfolio Name'] = template_mapping['Portfolio Name'].astype(str).str.strip()
            template_mapping = template_mapping.dropna(subset=['Portfolio Name'])
            template_mapping = template_mapping[template_mapping['Portfolio Name'] != '']
            
            return template_mapping, len(template_mapping)
            
        except Exception as e:
            self.logger.error(f"Error creating template mapping: {str(e)}")
            return None, 0
    
    def _add_helper_columns(self, df: pd.DataFrame, column_mapping: Dict[str, str]) -> List[str]:
        """Add helper columns for Zero Sales processing."""
        
        helper_cols = []
        
        try:
            # Add processing flags
            df['ZS_Candidate'] = True  # Mark as zero sales candidate
            helper_cols.append('ZS_Candidate')
            
            # Add bid change tracking
            df['Original_Bid'] = df[column_mapping.get('bid', '')].copy()
            helper_cols.append('Original_Bid')
            
            # Add processing timestamp
            df['Processed_Date'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            helper_cols.append('Processed_Date')
            
            # Add bid calculation case (to be filled during processing)
            df['Bid_Case'] = ''
            helper_cols.append('Bid_Case')
            
            # Add calculation notes (to be filled during processing)
            df['Calculation_Notes'] = ''
            helper_cols.append('Calculation_Notes')
            
        except Exception as e:
            self.logger.error(f"Error adding helper columns: {str(e)}")
        
        return helper_cols
    
    def get_cleaning_summary(self, cleaning_details: Dict[str, Any]) -> str:
        """Generate human-readable cleaning summary."""
        
        summary_lines = [
            f"Data Cleaning Summary:",
            f"Original rows: {cleaning_details.get('original_rows', 0)}",
            f"Final rows: {cleaning_details.get('final_rows', 0)}"
        ]
        
        # Add step details
        for step_name, step_details in cleaning_details.get('cleaning_steps', []):
            if step_name == 'basic_cleaning':
                if step_details.get('empty_rows_removed', 0) > 0:
                    summary_lines.append(f"• Removed {step_details['empty_rows_removed']} empty rows")
                if step_details.get('duplicate_rows_removed', 0) > 0:
                    summary_lines.append(f"• Removed {step_details['duplicate_rows_removed']} duplicate rows")
            
            elif step_name == 'portfolio_filtering':
                filtered = step_details.get('total_filtered', 0)
                if filtered > 0:
                    summary_lines.append(f"• Filtered {filtered} rows (excluded/ignored portfolios + non-zero sales)")
        
        # Add quality score
        quality_score = cleaning_details.get('data_quality', {}).get('overall_score', 0)
        if quality_score > 0:
            summary_lines.append(f"• Data quality score: {quality_score:.1%}")
        
        return "\n".join(summary_lines)