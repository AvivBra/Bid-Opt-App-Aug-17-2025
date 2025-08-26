"""Data Rova file reader for Campaign Creator."""

import pandas as pd
from typing import Dict, Optional, Tuple, Set


class DataRovaReader:
    """Handles reading and processing Data Rova file."""
    
    def __init__(self):
        """Initialize Data Rova reader."""
        self.required_columns = [
            'Keyword',
            'Keyword Monthly Sales', 
            'Keyword Conversion'
        ]
        
        self.all_columns = [
            'Keyword',
            'Keyword Monthly Clicks',
            'Keyword Monthly Sales',
            'Keyword Conversion',
            'Top ASIN',
            'Top ASIN Monthly Clicks',
            'Top ASIN Monthly Sales',
            'Top ASIN Conversion',
            'DSTR'
        ]
    
    def read_file(self, file) -> Tuple[Optional[pd.DataFrame], str]:
        """
        Read Data Rova file.
        
        Returns:
            Tuple of (dataframe, error message if any)
        """
        try:
            # Check file size
            file.seek(0, 2)
            size = file.tell()
            file.seek(0)
            
            if size > 40 * 1024 * 1024:  # 40MB
                return None, "קובץ גדול מדי"
            
            if size == 0:
                return None, "קובץ ריק"
            
            # Read file based on type
            if file.name.endswith('.xlsx'):
                df = pd.read_excel(file)
            elif file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                return None, "פורמט לא תקין"
            
            if df.empty:
                return None, "קובץ ריק"
            
            # Check for required columns
            missing_cols = [col for col in self.required_columns if col not in df.columns]
            if missing_cols:
                return None, f"חסרות כותרות: {', '.join(missing_cols)}"
            
            return df, ""
            
        except Exception as e:
            return None, f"Error reading file: {str(e)}"
    
    def get_keyword_data(self, df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """
        Extract keyword data from Data Rova.
        
        Returns:
            Dictionary mapping keyword -> {cvr: float, sales: float}
        """
        keyword_data = {}
        
        if not all(col in df.columns for col in self.required_columns):
            return keyword_data
        
        for _, row in df.iterrows():
            keyword = str(row.get('Keyword', '')).strip()
            if not keyword:
                continue
            
            try:
                cvr = float(row.get('Keyword Conversion', 0))
                sales = float(row.get('Keyword Monthly Sales', 0))
                
                keyword_data[keyword] = {
                    'cvr': cvr,
                    'sales': sales
                }
            except (ValueError, TypeError):
                # Skip rows with invalid numeric data
                continue
        
        return keyword_data
    
    def find_matching_keywords(self, keywords: Set[str], df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """
        Find keywords from Data Dive that exist in Data Rova.
        
        Args:
            keywords: Set of keywords from Data Dive
            df: Data Rova dataframe
            
        Returns:
            Dictionary of matching keywords with their data
        """
        all_keyword_data = self.get_keyword_data(df)
        matching = {}
        
        for keyword in keywords:
            if keyword in all_keyword_data:
                matching[keyword] = all_keyword_data[keyword]
        
        return matching
    
    def find_missing_keywords(self, keywords: Set[str], df: pd.DataFrame) -> Set[str]:
        """
        Find keywords that don't exist in Data Rova.
        
        Args:
            keywords: Set of keywords from Data Dive
            df: Data Rova dataframe
            
        Returns:
            Set of missing keywords
        """
        if 'Keyword' not in df.columns:
            return keywords
        
        rova_keywords = set(df['Keyword'].dropna().astype(str).str.strip().tolist())
        return keywords - rova_keywords
    
    def get_all_keywords(self, df: pd.DataFrame) -> Set[str]:
        """
        Get all keywords from Data Rova.
        
        Returns:
            Set of all keywords
        """
        if 'Keyword' not in df.columns:
            return set()
        
        return set(df['Keyword'].dropna().astype(str).str.strip().tolist())