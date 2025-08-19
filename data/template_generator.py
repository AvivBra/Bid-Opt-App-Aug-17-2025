"""Template file generation for Bid Optimizer."""

import pandas as pd
import io
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from config.constants import TEMPLATE_REQUIRED_SHEETS, TEMPLATE_PORT_VALUES_COLUMNS


class TemplateGenerator:
    """Generates template Excel files for bid optimization."""
    
    def __init__(self):
        self.port_values_columns = TEMPLATE_PORT_VALUES_COLUMNS
        self.required_sheets = TEMPLATE_REQUIRED_SHEETS
    
    def generate_template(self) -> bytes:
        """Generate a complete template Excel file."""
        
        # Create workbook
        wb = Workbook()
        
        # Remove default sheet
        if 'Sheet' in wb.sheetnames:
            wb.remove(wb['Sheet'])
        
        # Create Port Values sheet
        self._create_port_values_sheet(wb)
        
        # Create Top ASINs sheet
        self._create_top_asins_sheet(wb)
        
        # Save to bytes
        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        
        return buffer.getvalue()
    
    def _create_port_values_sheet(self, wb: Workbook):
        """Create the Port Values sheet with headers and sample data."""
        
        ws = wb.create_sheet("Port Values")
        
        # Headers
        headers = self.port_values_columns
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(start_color="8B5CF6", end_color="8B5CF6", fill_type="solid")
            cell.alignment = Alignment(horizontal="center")
        
        # Sample data with instructions
        sample_data = [
            ["Example Portfolio 1", "0.50", "1.20"],
            ["Example Portfolio 2", "0.75", ""],
            ["Example Portfolio 3", "Ignore", "2.00"],
            ["[Replace with your portfolio names]", "[0.02-4 or 'Ignore']", "[0.01-4 or empty]"]
        ]
        
        for row_idx, row_data in enumerate(sample_data, 2):
            for col_idx, value in enumerate(row_data, 1):
                cell = ws.cell(row=row_idx, column=col_idx, value=value)
                if row_idx == 5:  # Instruction row
                    cell.font = Font(italic=True, color="808080")
        
        # Add instructions below
        ws.cell(row=7, column=1, value="Instructions:").font = Font(bold=True)
        ws.cell(row=8, column=1, value="• Portfolio Name: Must match exactly with Bulk file")
        ws.cell(row=9, column=1, value="• Base Bid: 0.02-4.00 or 'Ignore' to skip portfolio")
        ws.cell(row=10, column=1, value="• Target CPA: 0.01-4.00 or leave empty")
        ws.cell(row=11, column=1, value="• No duplicate portfolio names allowed")
        
        # Column widths
        ws.column_dimensions['A'].width = 25
        ws.column_dimensions['B'].width = 12
        ws.column_dimensions['C'].width = 12
    
    def _create_top_asins_sheet(self, wb: Workbook):
        """Create the Top ASINs sheet (currently empty - for future use)."""
        
        ws = wb.create_sheet("Top ASINs")
        
        # Header
        cell = ws.cell(row=1, column=1, value="Top ASINs Data")
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="8B5CF6", end_color="8B5CF6", fill_type="solid")
        cell.alignment = Alignment(horizontal="center")
        
        # Instructions
        ws.cell(row=3, column=1, value="This sheet is reserved for future ASIN targeting features.")
        ws.cell(row=4, column=1, value="Leave empty for Phase 1 (Zero Sales optimization).")
        
        # Column width
        ws.column_dimensions['A'].width = 50
    
    def validate_template_structure(self, file_data: bytes) -> tuple[bool, str]:
        """Validate that uploaded file has correct template structure."""
        
        try:
            # Read Excel file
            excel_data = pd.read_excel(file_data, sheet_name=None)
            
            # Check required sheets exist
            missing_sheets = []
            for sheet in self.required_sheets:
                if sheet not in excel_data:
                    missing_sheets.append(sheet)
            
            if missing_sheets:
                return False, f"Missing sheets: {', '.join(missing_sheets)}"
            
            # Check Port Values columns
            port_values_df = excel_data['Port Values']
            expected_cols = set(self.port_values_columns)
            actual_cols = set(port_values_df.columns)
            
            if expected_cols != actual_cols:
                missing = expected_cols - actual_cols
                extra = actual_cols - expected_cols
                
                issues = []
                if missing:
                    issues.append(f"Missing columns: {', '.join(missing)}")
                if extra:
                    issues.append(f"Extra columns: {', '.join(extra)}")
                
                return False, "; ".join(issues)
            
            return True, "Template structure is valid"
            
        except Exception as e:
            return False, f"Error reading template: {str(e)}"
    
    def get_sample_portfolios(self) -> list[str]:
        """Get list of sample portfolio names for testing."""
        return [
            "Campaign Alpha Portfolio",
            "Campaign Beta Portfolio", 
            "Campaign Gamma Portfolio",
            "Test Portfolio 1",
            "Test Portfolio 2"
        ]