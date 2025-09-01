"""Data structure cleaning for Portfolio Optimizations."""

import pandas as pd
from typing import Dict, Tuple
import logging
from .constants import COL_ENTITY, SHEET_PORTFOLIOS

logger = logging.getLogger(__name__)


def clean_data_structure(all_sheets: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """
    Clean and restructure the data according to preprocessing logic.
    
    Per PRD preprocessing-logic.md:
    1. Create separate "Campaigns" sheet from Entity="Campaign" rows
    2. Create separate "Product Ad" sheet from Entity="Product Ad" rows  
    3. Remove original "Sponsored Products Campaigns" sheet
    4. Keep only: Portfolios, Campaigns, Product Ad sheets
    
    Args:
        all_sheets: Dictionary of sheet name to DataFrame
        
    Returns:
        Cleaned dictionary with restructured sheets
    """
    logger.info("Starting data structure cleaning")
    
    # Get the source sheet (Sponsored Products Campaigns)
    source_sheet_name = "Sponsored Products Campaigns"
    
    if source_sheet_name not in all_sheets:
        logger.warning(f"Source sheet '{source_sheet_name}' not found - skipping cleaning")
        return all_sheets
    
    source_df = all_sheets[source_sheet_name].copy()
    
    if source_df.empty:
        logger.info(f"Source sheet '{source_sheet_name}' is empty - skipping cleaning")
        return all_sheets
    
    # Check if Entity column exists
    if COL_ENTITY not in source_df.columns:
        logger.error(f"Entity column not found in {source_sheet_name}")
        raise ValueError(f"Entity column not found in {source_sheet_name}")
    
    # Step 1 & 2: Split campaigns and product ads into separate sheets
    campaigns_df, product_ads_df = _split_campaigns_sheet(source_df)
    
    # Step 3 & 4: Create cleaned structure with only required sheets
    cleaned_sheets = _create_cleaned_structure(all_sheets, campaigns_df, product_ads_df)
    
    logger.info(f"Data structure cleaning completed. Final sheets: {list(cleaned_sheets.keys())}")
    
    return cleaned_sheets


def _split_campaigns_sheet(source_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split the Sponsored Products Campaigns sheet into Campaigns and Product Ad sheets.
    
    Args:
        source_df: Source DataFrame from Sponsored Products Campaigns
        
    Returns:
        Tuple of (campaigns_df, product_ads_df)
    """
    logger.info("Splitting campaigns sheet by Entity type")
    
    # Extract campaigns (Entity = "Campaign")
    campaigns_mask = source_df[COL_ENTITY] == "Campaign"
    campaigns_df = source_df[campaigns_mask].copy()
    
    # Extract product ads (Entity = "Product Ad")  
    product_ads_mask = source_df[COL_ENTITY] == "Product Ad"
    product_ads_df = source_df[product_ads_mask].copy()
    
    # Log statistics
    total_rows = len(source_df)
    campaigns_count = len(campaigns_df)
    product_ads_count = len(product_ads_df)
    other_entities_count = total_rows - campaigns_count - product_ads_count
    
    logger.info(f"Entity split results:")
    logger.info(f"  Total rows: {total_rows}")
    logger.info(f"  Campaign rows: {campaigns_count}")
    logger.info(f"  Product Ad rows: {product_ads_count}")
    logger.info(f"  Other entity rows (will be removed): {other_entities_count}")
    
    if other_entities_count > 0:
        # Log which entity types are being removed
        other_entities = source_df[~(campaigns_mask | product_ads_mask)][COL_ENTITY].unique()
        logger.info(f"  Entity types being removed: {list(other_entities)}")
    
    return campaigns_df, product_ads_df


def _create_cleaned_structure(
    all_sheets: Dict[str, pd.DataFrame],
    campaigns_df: pd.DataFrame, 
    product_ads_df: pd.DataFrame
) -> Dict[str, pd.DataFrame]:
    """
    Create the final cleaned structure with only required sheets.
    
    Args:
        all_sheets: Original sheets dictionary
        campaigns_df: DataFrame for new Campaigns sheet
        product_ads_df: DataFrame for new Product Ad sheet
        
    Returns:
        Dictionary with only required sheets
    """
    logger.info("Creating cleaned structure with required sheets only")
    
    cleaned_sheets = {}
    
    # Always include Portfolios sheet if it exists
    if SHEET_PORTFOLIOS in all_sheets:
        cleaned_sheets[SHEET_PORTFOLIOS] = all_sheets[SHEET_PORTFOLIOS].copy()
        logger.info(f"Preserved {SHEET_PORTFOLIOS} sheet: {len(cleaned_sheets[SHEET_PORTFOLIOS])} rows")
    else:
        logger.warning(f"{SHEET_PORTFOLIOS} sheet not found - this may cause issues")
    
    # Add Campaigns sheet (only if not empty)
    if not campaigns_df.empty:
        cleaned_sheets["Campaigns"] = campaigns_df
        logger.info(f"Created Campaigns sheet: {len(campaigns_df)} rows")
    else:
        logger.info("No Campaign entities found - Campaigns sheet will be empty")
        cleaned_sheets["Campaigns"] = campaigns_df  # Include even if empty for consistency
    
    # Add Product Ad sheet (only if not empty) 
    if not product_ads_df.empty:
        cleaned_sheets["Product Ad"] = product_ads_df
        logger.info(f"Created Product Ad sheet: {len(product_ads_df)} rows")
    else:
        logger.info("No Product Ad entities found - Product Ad sheet will be empty")
        cleaned_sheets["Product Ad"] = product_ads_df  # Include even if empty for consistency
    
    # Log removed sheets
    original_sheets = set(all_sheets.keys())
    final_sheets = set(cleaned_sheets.keys())
    removed_sheets = original_sheets - final_sheets
    
    if removed_sheets:
        logger.info(f"Removed sheets: {list(removed_sheets)}")
    
    return cleaned_sheets


def validate_cleaned_structure(cleaned_sheets: Dict[str, pd.DataFrame]) -> bool:
    """
    Validate that the cleaned structure meets requirements.
    
    Args:
        cleaned_sheets: Cleaned sheets dictionary
        
    Returns:
        True if structure is valid
        
    Raises:
        ValueError: If structure is invalid
    """
    required_sheets = [SHEET_PORTFOLIOS, "Campaigns", "Product Ad"]
    
    # Check all required sheets exist
    for sheet_name in required_sheets:
        if sheet_name not in cleaned_sheets:
            raise ValueError(f"Required sheet missing after cleaning: {sheet_name}")
    
    # Check no extra sheets exist
    extra_sheets = set(cleaned_sheets.keys()) - set(required_sheets)
    if extra_sheets:
        raise ValueError(f"Extra sheets found after cleaning: {list(extra_sheets)}")
    
    # Check Entity column exists in campaign-related sheets
    for sheet_name in ["Campaigns", "Product Ad"]:
        if not cleaned_sheets[sheet_name].empty:
            if COL_ENTITY not in cleaned_sheets[sheet_name].columns:
                raise ValueError(f"Entity column missing in {sheet_name} sheet")
    
    logger.info("Cleaned structure validation passed")
    return True