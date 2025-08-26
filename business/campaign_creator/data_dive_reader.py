"""Data Dive file reader for Campaign Creator."""

import pandas as pd
from typing import List, Dict, Set, Tuple, Optional
from io import BytesIO


class DataDiveReader:
    """Handles reading and processing Data Dive files."""
    
    def __init__(self):
        """Initialize Data Dive reader."""
        self.ignored_columns = ['SV Relev.']
        self.max_files = 20
    
    def read_files(self, uploaded_files: List) -> Tuple[List[pd.DataFrame], str]:
        """
        Read multiple Data Dive files.
        
        Args:
            uploaded_files: List of uploaded file objects
            
        Returns:
            Tuple of (list of dataframes, error message if any)
        """
        if len(uploaded_files) > self.max_files:
            return [], f"Maximum {self.max_files} files allowed"
        
        dataframes = []
        
        for file in uploaded_files:
            df, error = self._read_single_file(file)
            if error:
                return [], f"Error in file {file.name}: {error}"
            if df is not None:
                dataframes.append(df)
        
        if not dataframes:
            return [], "No valid data found in uploaded files"
        
        return dataframes, ""
    
    def _read_single_file(self, file) -> Tuple[Optional[pd.DataFrame], str]:
        """Read a single Data Dive file."""
        try:
            # Check file size
            file.seek(0, 2)  # Go to end
            size = file.tell()
            file.seek(0)  # Reset to beginning
            
            if size > 40 * 1024 * 1024:  # 40MB
                return None, "File too large (max 40MB)"
            
            if size == 0:
                return None, "File is empty"
            
            # Read based on file type
            if file.name.endswith('.xlsx'):
                df = pd.read_excel(file)
            elif file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                return None, "Invalid format (use Excel or CSV)"
            
            if df.empty:
                return None, "No data in file"
            
            if df.shape[0] == 0 or df.shape[1] == 0:
                return None, "File has no rows or columns"
            
            # Check for headers
            if df.columns.tolist() == list(range(len(df.columns))):
                return None, "Missing column headers"
            
            return df, ""
            
        except Exception as e:
            return None, str(e)
    
    def extract_keywords(self, dataframes: List[pd.DataFrame]) -> Set[str]:
        """Extract unique keywords from all Data Dive files."""
        keywords = set()
        
        for df in dataframes:
            # Search Terms is the second column from left
            if len(df.columns) >= 2:
                search_terms_col = df.columns[1]
                # Extract keywords
                if 'Search Terms' in str(search_terms_col) or search_terms_col == 'Search Terms':
                    terms = df[search_terms_col].dropna().astype(str)
                    # Filter out empty strings and add to set
                    keywords.update([k.strip() for k in terms if k.strip()])
        
        return keywords
    
    def extract_asins(self, dataframes: List[pd.DataFrame]) -> Set[str]:
        """Extract ASINs from column headers starting with B0."""
        asins = set()
        
        for df in dataframes:
            for col in df.columns:
                col_str = str(col).strip()
                if col_str.startswith('B0'):
                    # Extract just the ASIN part (first word if there are spaces)
                    asin = col_str.split()[0] if ' ' in col_str else col_str
                    asins.add(asin)
        
        return asins
    
    def get_all_targets(self, dataframes: List[pd.DataFrame]) -> Dict[str, Set[str]]:
        """
        Extract all targets (keywords and ASINs) from Data Dive files.
        
        Returns:
            Dictionary with 'keywords' and 'asins' sets
        """
        return {
            'keywords': self.extract_keywords(dataframes),
            'asins': self.extract_asins(dataframes)
        }