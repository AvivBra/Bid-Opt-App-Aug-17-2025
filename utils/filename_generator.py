"""Filename generation utilities."""

from datetime import datetime
from config.constants import OUTPUT_FILE_PREFIX, TIMESTAMP_FORMAT


def generate_output_filename(optimization_type: str = "Working") -> str:
    """Generate timestamped filename for output files."""
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    return f"{OUTPUT_FILE_PREFIX} {timestamp}.xlsx"


def generate_template_filename() -> str:
    """Generate filename for template download."""
    return "Bid_Optimizer_Template.xlsx"


def generate_campaign_optimizer_1_filename() -> str:
    """Generate timestamped filename for Campaign Optimizer 1 output files."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"campaign-optimizer-1-{timestamp}.xlsx"


def generate_backup_filename(original_filename: str) -> str:
    """Generate backup filename with timestamp."""
    name, ext = original_filename.rsplit('.', 1) if '.' in original_filename else (original_filename, '')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{name}_backup_{timestamp}.{ext}" if ext else f"{name}_backup_{timestamp}"


def clean_filename(filename: str) -> str:
    """Clean filename for safe filesystem usage."""
    if not filename:
        return "unnamed_file"
    
    # Remove problematic characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove extra spaces and dots
    filename = filename.strip(' .')
    
    # Limit length
    if len(filename) > 100:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = f"{name[:90]}.{ext}" if ext else name[:100]
    
    return filename or "unnamed_file"